from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DialogState(str, Enum):
    GREETING = "GREETING"
    INTENT_ROUTING = "INTENT_ROUTING"
    COLLECT_SLOTS = "COLLECT_SLOTS"
    OFFER_SLOTS = "OFFER_SLOTS"
    CONFIRM_ACTION = "CONFIRM_ACTION"
    EXECUTE_ACTION = "EXECUTE_ACTION"
    WRAP_UP = "WRAP_UP"
    RECOVERY = "RECOVERY"
    HANDOFF = "HANDOFF"


class Intent(str, Enum):
    BOOKING = "BOOKING"
    LOCATION = "LOCATION"
    PREPARATION = "PREPARATION"
    PRICE = "PRICE"
    UNKNOWN = "UNKNOWN"


@dataclass
class Slots:
    doctor: str
    service: Optional[str] = None
    date: Optional[str] = None   # YYYY-MM-DD
    time: Optional[str] = None   # HH:MM
    name: Optional[str] = None
    phone: Optional[str] = None

    last_confirmed_service: Optional[str] = None
    last_confirmed_date: Optional[str] = None
    last_confirmed_time: Optional[str] = None