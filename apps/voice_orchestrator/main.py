from __future__ import annotations

from fastapi import FastAPI
from redis.asyncio import Redis

from apps.voice_orchestrator.api import build_router
from core.config import settings
from core.session.redis_store import RedisSessionStore
from observability.logging import setup_logger
from tools.fake_backend import FakeClinicBackend

logger = setup_logger("oqtabassum", settings.log_level)

app = FastAPI(title="OqTabassum Voice Orchestrator (Phase 2)")


def _build_app() -> None:
    tools = FakeClinicBackend(
        default_doctor=settings.default_doctor,
        pricing_mode=settings.pricing_mode,
    )

    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    store = RedisSessionStore(redis=redis, ttl_seconds=settings.session_ttl_seconds)

    app.include_router(
        build_router(
            tools=tools,
            session_store=store,
            default_doctor=settings.default_doctor,
            app_timezone=settings.app_timezone,
        )
    )


_build_app()