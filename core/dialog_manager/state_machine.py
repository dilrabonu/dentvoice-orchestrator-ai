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

    def handle_user_turn(self, user_text: str) -> str:
        self.memory.next_turn()
        logger.info(
            "user_turn",
            call_id=self.call_id,
            state=self.state.name,
            turn=self.memory.turn_index,

        )
        if self.state == DialogState.INTENT_ROUTING:
            return self._route_intent(user_text)
        if self.state == DialogState.COLLECT_SLOTS:
            return self._collect_slots(user_text)
        if self.state == DialogState.OFFER_ALTERNATIVES:
            return self._collect_slots(user_text)
        if self.state == DialogState.CONFIRM_ACTION:
            return self._handle_confirmation(user_text)
        if self.state == DialogState.HANDOFF:
            return "Sizni operatorga ulayapman, biroz kuting..."
        if self.state == DialogState.ENDED:
            return "Qo'ng'iroq yakunlandi. Rahmat!"

        return self._fallback("Kechirasiz, tushunmadim. Qaytadan urinib ko'ring.")

        # Intent routing
    def _route_intent(self, text: str) -> str:
        intent = self._extract_intent(text)

        if intent == Intent.LOCATION:
            self.state = DialogState.WRAP_UP
            return booking_tools.get_location() + "Yana biror narsada yordam bera olamanmi?"

        if intent == Intent.PRICE:
            service = self._extract_service(text)
            if service:
                price = booking_tools.get_price(service)
                self.state = DialogState.WRAP_UP
                return f"{service.capitalize()} narxi: {price}. Yana yordam kerakmi?"
            self.state = DialogState.COLLECT_SLOTS
            return "Qaysi xizmat narxi bilan qiziqasiz? (konsultatsiya / davolash yoki ko'rik)"

        if intent == Intent.PREPARATION:
            service = self._extract_service(text)
            if service:
                prep = booking_tools.get_preparation(service)
                self.state = DialogState.WRAP_UP
                return f"{prep} Yana yordam kerakmi?"
            self.state = DialogState.COLLECT_SLOTS
            return "Qaysi xizmat uchun tayyorlanish kerak? (konsultatsiya / davolash yoki ko'rik)"

        if intent == Intent.BOOKING:
            self.state = DialogState.COLLECT_SLOTS
            return self._next_slot_question()

        return self._fallback(
            "Siz bron qilmoqchimisiz, narx yoki manzil haqida bilishni xohlaysizmi?"
        )

    def _extract_intent(self, text: str) -> Intent:
        t = text.lower()
        if any(k in t for k in ["manzil", "qayerda", "address"]):
            return Intent.LOCATION
        if any(k in t for k in ["narx", "qancha", "price", "necha pul"]):
            return Intent.PRICE
        if any(k in t for k in ["tayyorgarlik", "nima qilish kerak", "oldindan"]):
            return Intent.PREPARATION
        if any(k in t for k in["bron", "yozil", "qabul", "vaqt", "band qil"]):
            return Intent.BOOKING
        return Intent.UNKNOWN

    def _extract_service(self, text: str) -> str | None:
        t = text.lower()
        for service, keywords in _SERVICE_KEYWORDS.items():
            if any(k in t for k in keywords):
                return service
        return None

    # Slot Collection
    def _next_slot_question(self) -> str:
        slots = self.memory.slots
        if slots.service is None:
            return "Qaysi xizmat kerak: konsultatsiya, tish davolash yoki tish tozalash?"
        if slots.date is None:
            return "Qaysi kunga bron qilishni xoxlaysiz? (masalan: bugun, ertaga yoki sana)"
        if slots.time is None:
            return self._offer_slots()
        if slots.customer_name is None:
            return "Ismingizni ayting, iltimos!"
        if slots.customer_phone is None:
            return "Telefon raqamingizni ayting, iltimos"
        return self._confirm_question()

    def _collect_slots(self, text: str) -> str:
        slots = self.memory.slots

        if slots.service is None:
            service = self._extract_service(text)
            if service is None:
                retries = self.memory.bump_retry("service")
                if retries >= MAX_RETRIES:
                    return self._handoff("Xizmat turini aniqlab bo'lmadi")
                return "Kechirasiz, tushunmadim. Konsultatsiy, tish davolash yoki tish tozalashmi birini tanlang"
            slots.service = service
            return self._next_slot_question()

        if slots.date is None:
            slots.date = text.strip()
            return self._next_slot_question()

        if slots.time is None:
            return self._handle_slot_pick(text)

        if slots.customer_name is None:
            slots.customer_name = text.strip()
            return self._next_slot_question()
        
        if slots.customer_phone is None:
            match = _PHONE_RE.search(text)
            if not match:
                retries = self.memory.bump_retry("phone")
                if retries >= MAX_RETRIES:
                    return self._handoff("Telefon raqamini aniqlab bo'lmadi")
                return "Telefon raqamini to'liq kiriting (masalan: +998901234567)"
            slots.customer_phone = match.group(0)
            return self._confirm_question()

        return self._confirm_question()

    def _offer_slots(self) -> str:
        slots = self.memory.slots
        available = booking_tools.get_available_slots(slots.date, slots.service)
        if not available:
            self.state = DialogState.OFFER_ALTERNATIVES
            alt_date, alt_slots = booking_tools.get_next_available(slots.service)
            slots.date = alt_date
            return (
                
            )


