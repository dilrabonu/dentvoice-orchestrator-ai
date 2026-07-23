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


