"""Audio decode/resample pipeline (Phase 2/4 target).

Twilio Media Streams sends 8kHz mu-law audio. Whisper and most STT
engines expect 16kHz PCM. This module will:
  1. decode mu-law -> PCM16
  2. resample 8kHz -> 16kHz
  3. (optional) light noise suppression

Not implemented yet - Phase 1 is text-mode only, no audio path.
"""
