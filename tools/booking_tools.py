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

_P
