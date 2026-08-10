"""Voice Activity Detection (Phase 2/4 target).

Drives two things:
  - turn-taking: when has the caller stopped speaking (end of utterance)
  - barge-in: caller started speaking while TTS is playing -> stop TTS
    within ~250ms (Phase 2 latency budget)

Not implemented yet - Phase 1 is text-mode only, no audio path.
"""
from __future__ import annotations

class VoiceActivityDetector:
    def __init__