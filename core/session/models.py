from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from core.dialog_manager.states import DialogState, Intent, Slots


@dataclass
class SessionState:
    """
    Serializable session snapshot. Stored in Redis by call_id.

    Keep it small:
    - state
    - intent
    - slots
    - retry counters
    """
    state: DialogState
    intent: Intent
    slots: Slots
    stt_retry_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Enums serialized to their values
        d["state"] = self.state.value
        d["intent"] = self.intent.value
        return d

    @staticmethod
    def from_dict(data: Dict[str, Any], default_doctor: str) -> "SessionState":
        """
        Restore session from dict. If something missing, fill safe defaults.
        """
        state = DialogState(data.get("state", DialogState.GREETING.value))
        intent = Intent(data.get("intent", Intent.UNKNOWN.value))

        slots_raw = data.get("slots") or {}
        slots = Slots(
            doctor=slots_raw.get("doctor") or default_doctor,
            service=slots_raw.get("service"),
            date=slots_raw.get("date"),
            time=slots_raw.get("time"),
            name=slots_raw.get("name"),
            phone=slots_raw.get("phone"),
            last_confirmed_service=slots_raw.get("last_confirmed_service"),
            last_confirmed_date=slots_raw.get("last_confirmed_date"),
            last_confirmed_time=slots_raw.get("last_confirmed_time"),
        )

        return SessionState(
            state=state,
            intent=intent,
            slots=slots,
            stt_retry_count=int(data.get("stt_retry_count", 0)),
        )