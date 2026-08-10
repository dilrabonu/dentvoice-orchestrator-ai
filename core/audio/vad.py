"""Voice Activity Detection (Phase 2/4 target).

Drives two things:
  - turn-taking: when has the caller stopped speaking (end of utterance)
  - barge-in: caller started speaking while TTS is playing -> stop TTS
    within ~250ms (Phase 2 latency budget)

Not implemented yet - Phase 1 is text-mode only, no audio path.
"""
from __future__ import annotations

class VoiceActivityDetector:
    def __init__(self, sample_rate: int = 16000) -> None:
        self.sample_rate = sample_rate

    def is_speech(self, audio_chunk: bytes) -> bool:
        raise NotImplementedError("Phase 2/4 task - wire up e.g. webrtcvad or Silero VAD")