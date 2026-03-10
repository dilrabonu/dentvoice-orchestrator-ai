from __future__ import annotations 

import audioop 
import base64

class TwilioAudioDecoder:
    """
    Decode Twilio Mdeia Streams audio (u-law 8 kHz) into PCM16 16 kHz.
    Twilio inbound audio payload:
    - base64 encoded bytes
    - u-law (G.711 u-law). 8 kHz, mono

    Output:
    - MCM16 little-endian, 16 kHz, mono
    """

    def __ini__(self) -> None:
        self._rate_state = None

    def decode_ulaw8k_to_pcm16_16k(self, payload_b64: str) -> bytes:
        """
        Convert base64 u-law 8k -> PCM16 16k.

        Args:
        payload_b64: base64 string from Twilio "media.payload"

        Returns:
        PCM16 bytes at 16kHz.
        """
        ulaw = base64.b64decode(payload_b64)
        pcm16_8k = audioop.ulaw2lin(ulaw, 2)

        # Resample
        pcm16_16k, self._rate_state = audioop.ratecv(
            pcm16_8k, 2, 1, 8000, 16000, self._rate_state
        )
        return pcm16_16k

class TwilioAudioEncoder:
    """
    Encode PCM16k 16kHz back to u-law 8kHz for Twilio outbound media.
    """

    def __init__(self) -> None:
        self._rate_state = None

    def pcm16_16k_to_ulaw8k_b64(self, pcm16_16k: bytes) -> str:
        """
        Convert PCM16 16k -> u-law 8 k and base64 encode.

        Args:
        pcm16_16k: PCM16 16kHz mono audio bytes

        Returns:
        base64 u-law payload string
        """
        pcm16_8k, self._rate_state = audioop.ratecv(
            pcm16_16k, 2, 1, 16000, 8000, self._rate_state
        )
        ulaw = audioop.lin2ulaw(pcm16_8k, 2)
        return base64.b64encode(ulaw).decode("ascii")
    