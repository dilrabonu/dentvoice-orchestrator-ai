from __future__ import annotations

import re

from core.dialog_manager.memory import InMemorySessionStore, SessionMemory
from core.dialog_manager.states import DialogState, Intent
from observability.logging_config import get_logger
from tools import booking_tools

logger = get_logger(__name__)

MAX_RETRIES = 2

_store = InMemorySessionStore()

_SERVICE_KEYWORDS = {
    "konsultatsiya": ["konsultatsiya", "ko'rik", "ko'rik"],
    "tish davolash": ["davolash", "davola"],
    "tish tozalash": ["tozalash", "tozala"],
}

_PHONE_RE = re.compile(r"(\+?998)?\s*\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}")

