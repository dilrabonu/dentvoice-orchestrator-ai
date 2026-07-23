from __future__ import annotations

import uuid
from datetime import datetime, timedelta

from observability.logging_config import get_logger
from tools.schemas import Booking, Customer

logger = get_logger(__name__)

DEFAULT_DOCTOR = "MuhammadRaufxon"

_SERVICES = ["konsultatsiya", "tish davolash", "tish tozalash", "ko'rik"]

_PRICES = {
    "konsultatsiya": 0,
    "tish davolash": 0,
    "tish tozalash": 0,
    "ko'rik": 0,
}

_PREPARATION = {"konsultatsiya": "Konsultatsiyaga oldindan ovqatlanib kelsangiz bo'ladi, maxsus tayyorgarlik shart emas.",
    "tish davolash": "Davolashdan oldin 2 soat og'ir ovqat yemaslikni tavsiya qilamiz.",
    "tish tozalash": "Tish tozalashdan oldin maxsus tayyorgarlik talab qilinmaydi.",
}

_LOCATION = "Manzil: Uchko'prik tumani, Markaziy stadion yonida"


# In-memory fake tables
_customers: dict[str, Customer] = {}
_bookings: dict[str, Booking] = {}
_idempotency_cache: dict[str, dict] = {}
_booked_slots: set[tuple[str, str, str]] = set()  # (doctor, date, time)

_ALL_DAY_SLOTS = ["09:00", "10:30", "11:30", "13:00", "15:00", "16:30", "18:00"]


def get_services() -> list[str]:
    return list(_SERVICES)

def get_available_slots(date: str, service: str) -> list[str]:
    
