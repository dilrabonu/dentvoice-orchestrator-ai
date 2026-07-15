"""
Dialog Manager States
"""
from enum import Enum, auto

class DialogState(Enum):
    GREETING = auto()
    INTENT_ROUTING = auto()