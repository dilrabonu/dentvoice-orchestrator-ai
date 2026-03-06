from __future__ import annotations 

from dataclasses import dataclass
from typing import List, Optional, Tuple

from core.dialog_manager.prompts import Copy
from core.dialog_manager.states import DialogState, Intent, Slots
from core.session.models import SessionState
from core.time_utils import resolve_data_token
from tools.interfaces import ClinicTools

@dataclass
class DialogTurn:
    user_text: str
    call_id: str
    turn_id: str


@dataclass
class DialogResponse:
    text: str
    state: DialogState
    handoff: bool = False

class DialogManager:
    def __init__(
        self,
        tools: ClinicTools,
        default_doctor: str,
        app_timezone: str,
        session: Optional[SessionState] = None,
    ) -> None:
        self.tools = tools
        self.default_doctor = default_doctor
        self.tz = app_timezone
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

        self._cashed_slot_options: List[str] = []

    def export_session(self) -> SessionState:
        """
        Export current dialog snapshot for persistence.
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

        
        