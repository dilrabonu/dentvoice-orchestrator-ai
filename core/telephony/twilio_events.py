from __future__ import annotations 

from dataclasses import dataclass 
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class TwilioStart:
    stream_sid: str
    call_id: str

@dataclass(frozen=True)
class TwilioMedia:
    payload_b64: str 
    track: str

@dataclass(frozen=True)
class TwilioMark:
    name: str

def parse_twilio_event(msg: Dict[str, Any]) -> tuple[str, Optional[object]]:
    """
    Parse Twilio Media Streams event.

    Args:
       msg: JSON dict from WS.

    Returns:
       (event_type, event_obj) where event_obj is one of TwilioStart/TwilioMedia/TwilioMark or None
    """
    event = msg.get("event")
    if event == "start":
        start = msg.get("start") or {}
        return "start", TwilioStart(
            stream_sid=str(start.get("streamSid", "")),
            call_id=str(start.get("callSid", "")),
        )

    if event == "media":
        media = msg.get("media") or {}
        return "media", TwilioMedia(
            payload_b64=str(media.get("payload", "")),
            track=str(media.get("track", "inbound")),
        )

    if event == "mark":
        mark = msg.get("mark") or {}
        return "mark", TwilioMark(name=str(mark.get("name", "")))

    if event == "stop":
        return "stop", None
    
    return str(event), None