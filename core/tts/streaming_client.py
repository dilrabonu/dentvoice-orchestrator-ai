from __future__ import annotations

from dataclasses import dataclass

class StramingTTSClient:
    """
    Interface for streaming TTS.
    for Twilio outbound calls.
    """

    async def synthesize_stream(self, text: str):
        """
        Async generator that yields TTS Chunk objects.
        """
        raise NotImplementedError

class StubTTSClient(StreamingTTSClient):
    """
    Placeholder TTS: returns silence (or tiny beep later)
    """

    async def synthesize_stream(self, text: str):

        silence = b"\x00\x00" * 3200
        yield TTSChunk(pcm16_16k=silence, is_last=True)