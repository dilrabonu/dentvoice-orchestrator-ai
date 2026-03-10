from __future__ import annotations

import json
import asyncio
from typing import Optional

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream

from core.config import settings
from core.dialog_manager.manager import DialogManager, DialogTurn
from core.session.redis_store import RedisSessionStore
from core.telephony.twilio_events import parse_twilio_event, TwilioStart, TwilioMedia
from core.audio.resampler import TwilioAudioDecoder, TwilioAudioEncoder
from core.audio.vad import EnergyVAD
from core.stt.streaming_client import StubSTTClient
from core.tts.streaming_client import StubTTSClient
from observability.logging import setup_logger, kv, mask_phone
from tools.interfaces import ClinicTools

router = APIRouter()
logger = setup_logger("twilio_ws", settings.log_level)


def build_twilio_router(tools: ClinicTools, session_store: RedisSessionStore) -> APIRouter:
    """
    Build Twilio webhook + websocket routes.
    """

    @router.post(settings.twilio_incoming_path)
    async def twilio_incoming(request: Request) -> Response:
        """
        Twilio Voice webhook: returns TwiML to start Media Stream.

        Production note:
          - PUBLIC_BASE_URL must be a valid HTTPS domain (or tunnel in dev).
          - Stream url must be WSS.
        """
        form = await request.form()
        call_sid = str(form.get("CallSid", ""))
        from_phone = str(form.get("From", ""))
        logger.info("incoming_call " + kv(call_sid=call_sid, from_phone=mask_phone(from_phone)))

        ws_url = settings.public_base_url.replace("https://", "wss://").replace("http://", "ws://")
        ws_url = f"{ws_url}{settings.twilio_stream_path}?call_id={call_sid}"

        vr = VoiceResponse()
        connect = Connect()
        connect.append(Stream(url=ws_url))
        vr.append(connect)

        return Response(content=str(vr), media_type="application/xml")

    @router.websocket(settings.twilio_stream_path)
    async def twilio_stream(ws: WebSocket) -> None:
        """
        Twilio Media Streams websocket.
        Receives JSON events: start/media/stop, and can send outbound audio events.
        """
        await ws.accept()

        decoder = TwilioAudioDecoder()
        encoder = TwilioAudioEncoder()
        vad = EnergyVAD(rms_threshold=500, silence_frames_to_end=12)

        stt = StubSTTClient()
        tts = StubTTSClient()

        stream_sid: Optional[str] = None
        call_id: Optional[str] = ws.query_params.get("call_id")

        # Audio buffer for one utterance (PCM16 16k)
        utter_buf = bytearray()

        # For barge-in: cancel current TTS task when user starts speaking
        tts_task: Optional[asyncio.Task] = None
        tts_cancel_event = asyncio.Event()

        async def stop_tts_if_any() -> None:
            nonlocal tts_task
            if tts_task and not tts_task.done():
                tts_cancel_event.set()
                tts_task.cancel()
                # Optional: send a control event (some setups use "clear"/"mark")
                # We keep it safe: just stop sending further audio.
            tts_task = None
            tts_cancel_event.clear()

        async def send_tts(text: str) -> None:
            """
            Stream TTS audio chunks back to Twilio.
            """
            nonlocal stream_sid
            if not stream_sid:
                return

            async for chunk in tts.synthesize_stream(text):
                if tts_cancel_event.is_set():
                    break

                payload = encoder.pcm16_16k_to_ulaw8k_b64(chunk.pcm16_16k)
                msg = {
                    "event": "media",
                    "streamSid": stream_sid,
                    "media": {"payload": payload},
                }
                await ws.send_text(json.dumps(msg))

                # Small pacing to avoid flooding
                await asyncio.sleep(0.02)

        try:
            while True:
                raw = await ws.receive_text()
                msg = json.loads(raw)

                etype, eobj = parse_twilio_event(msg)

                if etype == "start":
                    start: TwilioStart = eobj  # type: ignore
                    stream_sid = start.stream_sid
                    call_id = call_id or start.call_sid

                    logger.info("ws_start " + kv(call_id=call_id, stream_sid=stream_sid))

                    # Load existing session (if any)
                    session = await session_store.get(call_id=call_id, default_doctor=settings.default_doctor)

                    dm = DialogManager(
                        tools=tools,
                        default_doctor=settings.default_doctor,
                        app_timezone=settings.app_timezone,
                        session=session,
                    )

                    # Greet immediately (no user speech needed)
                    greet = dm.handle(DialogTurn(user_text="__start__", call_id=call_id, turn_id=0))
                    await session_store.set(call_id, dm.export_session())

                    # Speak greeting
                    await stop_tts_if_any()
                    tts_task = asyncio.create_task(send_tts(greet.text))

                elif etype == "media":
                    media: TwilioMedia = eobj  # type: ignore
                    pcm16_16k = decoder.decode_ulaw8k_to_pcm16_16k(media.payload_b64)

                    decision = vad.process_frame(pcm16_16k)

                    # BARGE-IN: if speech begins, stop TTS fast
                    if decision.is_speech:
                        await stop_tts_if_any()

                    utter_buf.extend(pcm16_16k)

                    if decision.is_end_of_utterance:
                        if not call_id:
                            continue

                        # Final STT on buffered utterance
                        stt_res = await stt.transcribe_final(bytes(utter_buf))
                        utter_buf.clear()

                        # Reload session + run dialog
                        session = await session_store.get(call_id=call_id, default_doctor=settings.default_doctor)
                        dm = DialogManager(
                            tools=tools,
                            default_doctor=settings.default_doctor,
                            app_timezone=settings.app_timezone,
                            session=session,
                        )

                        # turn_id: for now we can increment using Redis later; MVP uses 1
                        resp = dm.handle(DialogTurn(user_text=stt_res.text, call_id=call_id, turn_id=1))
                        await session_store.set(call_id, dm.export_session())

                        # Speak agent response
                        await stop_tts_if_any()
                        tts_task = asyncio.create_task(send_tts(resp.text))

                        # If handoff requested, you will later do Twilio transfer or SIP handoff
                        if resp.handoff:
                            logger.info("handoff_requested " + kv(call_id=call_id))

                elif etype == "stop":
                    logger.info("ws_stop " + kv(call_id=call_id))
                    await stop_tts_if_any()
                    break

        except WebSocketDisconnect:
            logger.info("ws_disconnect " + kv(call_id=call_id))
            await stop_tts_if_any()

    return router