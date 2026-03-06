from __future__ import annotations

from pydantic import BaseModel, Field 

class ChatRequest(BaseModel):
    call_id: str = Field(..., description="Unique call/session id")
    turn_id: int = Field(..., ge=0, description="Monotonic turn id")
    user_text: str = Field(..., description="User utterance in text form")

class ChatResponse(BaseModel):
    agent_text: str
    state: str
    handoff: bool = False