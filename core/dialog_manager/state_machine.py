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

class DialogSession:
    def __init__(self, call_id: str) -> None:
        self.call_id = call_id
        self.state = DialogState.GREETING
        self.memory: SessionMemory = _store.get_or_create(call_id)
        self.memory.slots.doctor = booking_tools.DEFAULT_DOCTOR

        #Public API
    def start(self) -> str:
        self.state = DialogState.INTENT_ROUTING
        return (
            "Assalomu alaykum! Safir Tishlar klinakasiga xush kelibsiz!"
            "Men sizga bron qilishda, manzil yoki ko'riklar haqida ma'lumot berishda yordam beraman."
            "Sizga qanday yordam kerak?"
        )

    def 