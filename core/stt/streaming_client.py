from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class STTResult:
    text: str
    is_final: bool
    confidence: float

class StreamingsSTTClient:
    """
    Interface for streaming STT.
    """
    async def transcribe_final(self, pcm16_16k: bytes) -> STTResult:
        raise NotImplementedError

class StubSTTClient(StreamingsSTTClient):
    """
    Placeholder STT: returns a fixed message
    Useful to validate the audio pipeline + orchestrator loop without external APIs.
    """

    async def transcribe_final(self, pcm16_16k: bytes) -> STTResult:
        return STTResult(text="Bron qilmochiman", is_final=True, confidence=0.80)
