"""
Dialog Manager States
"""
from enum import Enum, auto

class DialogState(Enum):
    GREETING = auto()
    INTENT_ROUTING = auto()
    COLLECT_SLOTS = auto()
    CHECK_SLOTS_TOOL = auto()
    OFFER_ALTERNATIVES = auto()
    CONFIRM_ACTION = auto()