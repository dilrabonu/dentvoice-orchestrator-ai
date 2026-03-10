from __future__ import annotations

import re
from dataclasses import dataclass

_PRICE_NUMBER_RE = re.compile(r"\b\d[\d\s.,]*\b")

@dataclass(frozen=True)
class ClinicPolicy:
    """
    Hard safety/ product rules for OqTabassum voice agent
    """
    no_price: bool = True
    max_reply_chars: int = 220 # short answer for voice

def enforce_policy(text: str, policy: ClinicPolicy) -> str:
    """
    Enforce response policy:
    - If NO_PRICE: remove/avoid numeric pricing.
    - Keep responses short for TTS latency.
    """

    out = (text or "").strip()

    if policy.no_price:
        # If model accidentlly outputs numbers, replace with policy sentence
        if _PRICE_NUMBER_RE.search(out) and any(k in out.lower() for k in ["so'm", "sum", "narx", "price", "стоим"]):
            out = "Narx ko'rikdan keyin aniq bo'ladi. Xoxlasangiz, ko'rik uchun vaqt bron qilib beraman."

    if len(out) > policy.max_reply_chars:
        out = out[: policy.max_reply_chars].rstrip() + "..."

    return out