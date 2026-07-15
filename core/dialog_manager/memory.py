from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass
class SessionSlots:
    doctor: str | None = None
    service: str | None = None
    date: str | None = None
    time: str | None = None
    customer_name: str | None = None
    customer_phone: str | None = None

    def missing_fields(self) -> list[str]:
        required = ["service", "date", "time", "customer_name", "customer_phone"]
        return [f for f in required if getattr(self, f) is None]

    def as_dict(self) -> dict[str, Any]:
        return