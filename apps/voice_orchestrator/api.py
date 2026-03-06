from __future__ import annotations

from fastapi import APIRouter

from apps.voice_orchestrator.schemas import ChatRequest, ChatResponse
from core.dialog_manager.manager import DialogManager, DialogTurn

router = APIRouter()


def build_router(dm: DialogManager) -> APIRouter:
    @router.post("/chat", response_model=ChatResponse)
    async def chat(req: ChatRequest) -> ChatResponse:
        resp = await dm.handle(
            DialogTurn(
                user_text=req.user_text,
                call_id=req.call_id,
                turn_id=req.turn_id,
            )
        )
        return ChatResponse(
            agent_text=resp.text,
            state=resp.state.value,
            handoff=resp.handoff,
        )

    return router