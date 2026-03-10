from __future__ import annotations

import audioop
from dataclasses import dataclass

@dataclassclass VadDecision:
    is_speech: bool
    is_end_of_utterance: bool

class EnergyVAD:
    """
    Lightweight VAD based on RMS energy.

    Strategy:
    - compute RMS on small frames
    - speech if RMS > threshold
    - end-of-utterance after N consecutive silent frames

    """

    def __init__(
        self,
        rms_threshold: int = 500,
        silence_frames_to_end: int = 12,
    ) -> None:
        self._thr = rms_threshold
        self._silence_frames_to_end = silence_frames_to_end

        self._in_speech = False
        self._silent_count = 0

    def process_frame(self, pcm16_16k: bytes) -> VadDecision:
        """
        Process a PCM16 frame and decide speech/end.

        Args:
        pcm16_16k: PCM16 16kHz mono bytes (any small chunk)

        Returns:
        VadDecision with speech and end-of-utterance flags
        """
        rms = audioop.rms(pcm16_16k, 2)
        is_speech = rms > self._thr 

        if is_speech:
            self._in_speech = True
            self._silent_count = 0
            return VadDecision(is_speech=True, is_end_of_utterance=False)

        # silence
        if self._in_speech:
            self._silent_count += 1
            if self._silent_count >= self._silence_frames_to_end:
                self._in_speech = False
                self._silent_count = 0
                return VadDecision(is_speech=False, is_end_of_utterance=True)
                
        return VadDecision(is_speech=False, is_end_of_utterance=False)