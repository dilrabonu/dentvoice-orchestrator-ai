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
        return{
            "doctor": self.doctor,
            "service": self.service,
            "date": self.date,
            "time": self.time,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
        }

@dataclass
class SessionMemory:
    call_id: str
    slots: SessionSlots = field(default_factory=SessionSlots)
    retry_counts: dict[str, int] = field(default_factory=dict)
    last_confirmed: dict[str, Any] | None = None
    turn_index: int = 0

    def bump_retry(self, key: str) -> int:
        self.retry_counts[key] = self.retry_counts.get(key, 0) + 1
        return self.retry_counts[key]

    def next_turn(self) -> int:
        self.turn_index += 1
        return self.turn_index

class InMemorySessionStore:
    def __init__(self) -> None:
        