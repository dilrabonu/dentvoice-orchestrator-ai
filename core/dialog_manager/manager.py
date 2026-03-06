from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from core.dialog_manager.prompts import Copy
from core.dialog_manager.states import DialogState, Intent, Slots
from core.session.models import SessionState
from core.time_utils import resolve_date_token
from tools.interfaces import ClinicTools


@dataclass
class DialogTurn:
    user_text: str
    call_id: str
    turn_id: int


@dataclass
class DialogResponse:
    text: str
    state: DialogState
    handoff: bool = False


class DialogManager:
    """
    Dialog manager for handling user interactions.
    - Session-backed (state/slots survive across requests)
    - TODAY/TOMORROW resolved using configured timezone
    """

    def __init__(
        self,
        tools: ClinicTools,
        default_doctor: str,
        app_timezone: str,
        session: Optional[SessionState] = None,
    ) -> None:
        self._tools = tools
        self._default_doctor = default_doctor
        self._tz = app_timezone

        if session is None:
            self._state = DialogState.GREETING
            self._intent = Intent.UNKNOWN
            self._slots = Slots(doctor=default_doctor)
            self._stt_retry_count = 0
        else:
            self._state = session.state
            self._intent = session.intent
            self._slots = session.slots
            self._stt_retry_count = session.stt_retry_count

        self._cached_slot_options: List[str] = []

    def export_session(self) -> SessionState:
        """
        Export current dialog snapshot for persistence (Redis).
        """
        return SessionState(
            state=self._state,
            intent=self._intent,
            slots=self._slots,
            stt_retry_count=self._stt_retry_count,
        )

    def handle(self, turn: DialogTurn) -> DialogResponse:
        text = (turn.user_text or "").strip()

        if not text:
            return self._recover_or_handoff()

        if self._state == DialogState.GREETING:
            self._state = DialogState.INTENT_ROUTING
            return DialogResponse(text=Copy.GREETING, state=self._state)

        if self._state == DialogState.INTENT_ROUTING:
            self._intent = self._classify_intent(text)
            if self._intent == Intent.LOCATION:
                return self._handle_location()
            if self._intent == Intent.PREPARATION:
                return self._handle_preparation()
            if self._intent == Intent.PRICE:
                return DialogResponse(text=Copy.PRICE_POLICY, state=self._state)
            if self._intent == Intent.BOOKING:
                self._state = DialogState.COLLECT_SLOTS
                return DialogResponse(text=Copy.ASK_SERVICE, state=self._state)

            return self._recover_or_handoff()

        if self._state == DialogState.COLLECT_SLOTS:
            if self._slots.service is None:
                service = self._extract_service(text)
                if service is None:
                    return DialogResponse(text=Copy.ASK_SERVICE, state=self._state)
                self._slots.service = service
                return DialogResponse(text=Copy.ASK_DATE, state=self._state)

            if self._slots.date is None:
                date = self._extract_date(text)
                if date is None:
                    return DialogResponse(text=Copy.ASK_DATE, state=self._state)

                # Phase 2: resolve TODAY/TOMORROW to real ISO date
                resolved = resolve_date_token(date, tz_name=self._tz)
                if len(resolved.iso_date) != 10:
                    return DialogResponse(text=Copy.ASK_DATE, state=self._state)

                self._slots.date = resolved.iso_date
                self._state = DialogState.OFFER_SLOTS
                return self._offer_slots()

            if self._slots.time is None:
                time = self._extract_time(text)
                if time is None:
                    return self._offer_slots()
                self._slots.time = time
                self._state = DialogState.CONFIRM_ACTION
                return DialogResponse(
                    text=Copy.CONFIRM_BOOKING.format(
                        date=self._slots.date,
                        time=self._slots.time,
                        service=self._slots.service,
                        doctor=self._slots.doctor,
                    ),
                    state=self._state,
                )

            if self._slots.name is None:
                self._slots.name = text
                self._state = DialogState.EXECUTE_ACTION
                return self._execute_booking(call_id=turn.call_id, turn_id=turn.turn_id)

            return self._recover_or_handoff()

        if self._state == DialogState.OFFER_SLOTS:
            self._state = DialogState.COLLECT_SLOTS
            return self.handle(turn)

        if self._state == DialogState.CONFIRM_ACTION:
            if self._is_affirm(text):
                self._state = DialogState.EXECUTE_ACTION
                return self._execute_booking(call_id=turn.call_id, turn_id=turn.turn_id)
            if self._is_negative(text):
                self._slots.time = None
                self._state = DialogState.OFFER_SLOTS
                return self._offer_slots()
            return DialogResponse(text="Iltimos, 'ha' yoki 'yo‘q' deb ayting.", state=self._state)

        if self._state == DialogState.EXECUTE_ACTION:
            self._state = DialogState.WRAP_UP
            return DialogResponse(text="Bron jarayoni yakunlandi. Yana nimadir kerakmi?", state=self._state)

        if self._state == DialogState.WRAP_UP:
            self._state = DialogState.INTENT_ROUTING
            return DialogResponse(text="Yana qanday yordam bera olaman?", state=self._state)

        return self._recover_or_handoff()

    # ---- unchanged helpers (intent/tools/extractors/recovery) ----
    # (sizdagi Phase 1 koddan ko‘chirib qoladi)
    # Pastga qisqartirib beraman: siz aynan o‘sha funksiyalarni qoldirasiz.

    def _handle_location(self) -> DialogResponse:
        loc = self._tools.get_location()
        return DialogResponse(
            text=Copy.LOCATION.format(address=loc["address"], landmark=loc["landmark"]),
            state=self._state,
        )

    def _handle_preparation(self) -> DialogResponse:
        service = self._extract_service(self._slots.service or "") or self._slots.service
        if not service:
            return DialogResponse(text=Copy.ASK_SERVICE, state=self._state)

        prep = self._tools.get_preparation(service)
        bullets = "; ".join(prep["instructions"])
        return DialogResponse(text=Copy.PREP.format(instructions=bullets), state=self._state)

    def _offer_slots(self) -> DialogResponse:
        assert self._slots.date and self._slots.service
        slots = self._tools.get_available_slots(self._slots.date, self._slots.service)
        if not slots:
            self._slots.date = None
            return DialogResponse(text="Bu kunda bo‘sh vaqt yo‘q. Boshqa sanani ayting.", state=self._state)

        self._cached_slot_options = [s.time for s in slots][:3]
        return DialogResponse(
            text=f"Bo‘sh vaqtlar: {', '.join(self._cached_slot_options)}. Qaysi birini tanlaysiz?",
            state=self._state,
        )

    def _execute_booking(self, call_id: str, turn_id: int) -> DialogResponse:
        if not (self._slots.service and self._slots.date and self._slots.time):
            self._state = DialogState.COLLECT_SLOTS
            return DialogResponse(text=Copy.ASK_SERVICE, state=self._state)

        if not self._slots.name:
            self._state = DialogState.COLLECT_SLOTS
            return DialogResponse(text=Copy.ASK_NAME, state=self._state)

        phone = self._slots.phone or "UNKNOWN"
        idem_key = f"{call_id}:{turn_id}:create_booking"

        self._tools.upsert_customer(name=self._slots.name, phone=phone)
        result = self._tools.create_booking(
            date=self._slots.date,
            time=self._slots.time,
            service=self._slots.service,
            name=self._slots.name,
            phone=phone,
            idem_key=idem_key,
            doctor=self._slots.doctor,
        )

        if not result.get("ok"):
            self._slots.time = None
            self._state = DialogState.OFFER_SLOTS
            return DialogResponse(text=result.get("message", Copy.RECOVERY), state=self._state)

        self._state = DialogState.WRAP_UP
        return DialogResponse(
            text=Copy.BOOKED.format(date=result["date"], time=result["time"]),
            state=self._state,
        )

    def _classify_intent(self, text: str) -> Intent:
        t = text.lower()
        if any(k in t for k in ["yoz", "bron", "qabul", "uchrashuv", "zapisk"]):
            return Intent.BOOKING
        if any(k in t for k in ["manzil", "qayerda", "location", "adres"]):
            return Intent.LOCATION
        if any(k in t for k in ["tayyorgarlik", "nima qilish", "preparation"]):
            return Intent.PREPARATION
        if any(k in t for k in ["narx", "qancha", "price", "stoimost"]):
            return Intent.PRICE
        return Intent.UNKNOWN

    def _extract_service(self, text: str) -> Optional[str]:
        t = text.lower()
        for s in self._tools.get_services():
            if s in t:
                return s
        if "kons" in t:
            return "konsultatsiya"
        if "davol" in t:
            return "tish davolash"
        if "tozal" in t:
            return "tish tozalash"
        return None

    def _extract_date(self, text: str) -> Optional[str]:
        t = text.lower()
        if "bugun" in t:
            return "TODAY"
        if "ertaga" in t:
            return "TOMORROW"
        if len(text) == 10 and text[4] == "-" and text[7] == "-":
            return text
        return None

    def _extract_time(self, text: str) -> Optional[str]:
        if len(text) == 5 and text[2] == ":":
            return text
        if text.isdigit() and 0 <= int(text) <= 23:
            return f"{int(text):02d}:00"
        return None

    def _is_affirm(self, text: str) -> bool:
        t = text.lower()
        return t in {"ha", "xa", "yes", "да", "haa"} or "tasdiq" in t

    def _is_negative(self, text: str) -> bool:
        t = text.lower()
        return t in {"yo‘q", "yoq", "no", "нет"} or "kerak emas" in t

    def _recover_or_handoff(self) -> DialogResponse:
        self._stt_retry_count += 1
        if self._stt_retry_count <= 2:
            self._state = DialogState.RECOVERY
            return DialogResponse(text=Copy.RECOVERY, state=self._state)
        self._state = DialogState.HANDOFF
        return DialogResponse(text=Copy.HANDOFF, state=self._state, handoff=True)