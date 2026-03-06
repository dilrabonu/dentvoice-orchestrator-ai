from __future__ import annotations

from fastapi import APIRouter

from apps.voice_orchestrator.schemas import ChatRequest, ChatResponse
from core.dialog_manager.manager import DialogManager, DialogTurn
from core.session.redis_store import RedisSessionStore
from tools.interfaces import ClinicTools

router = APIRouter()


def build_router(
    tools: ClinicTools,
    session_store: RedisSessionStore,
    default_doctor: str,
    app_timezone: str,
) -> APIRouter:
    @router.post("/chat", response_model=ChatResponse)
    async def chat(req: ChatRequest) -> ChatResponse:
        session = await session_store.get(call_id=req.call_id, default_doctor=default_doctor)

        dm = DialogManager(
            tools=tools,
            default_doctor=default_doctor,
            app_timezone=app_timezone,
            session=session,
        )

        resp = dm.handle(DialogTurn(user_text=req.user_text, call_id=req.call_id, turn_id=req.turn_id))

        # Persist session after each turn (TTL refresh)
        await session_store.set(req.call_id, dm.export_session())

        return ChatResponse(agent_text=resp.text, state=resp.state.value, handoff=resp.handoff)

    return router