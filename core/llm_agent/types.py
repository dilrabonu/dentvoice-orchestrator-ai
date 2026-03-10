from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class LLMMessage:
    role: str # system, user, assistant, tool
    content: str

@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: Dict[str, Any]

@dataclass
class AgentResult:
    """
    Final agent output for the current turn.
    """
    text: str
    handoff: bool = False
    tool_call: Optional[List[ToolCall]] = None