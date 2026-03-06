from __future__ import annotations

import json
from typing import Optional

from redis.asyncio import Redis

from core.session.models import SessionState


class RedisSessionStore:
    """
    Redis-backed session storage keyed by call_id.

    Data format:
      key = "sess:{call_id}"
      value = JSON(SessionState.to_dict())
      TTL = settings.session_ttl_seconds
    """

    def __init__(self, redis: Redis, ttl_seconds: int) -> None:
        self._redis = redis
        self._ttl = ttl_seconds

    def _key(self, call_id: str) -> str:
        return f"sess:{call_id}"

    async def get(self, call_id: str, default_doctor: str) -> Optional[SessionState]:
        raw = await self._redis.get(self._key(call_id))
        if not raw:
            return None
        data = json.loads(raw)
        return SessionState.from_dict(data, default_doctor=default_doctor)

    async def set(self, call_id: str, session: SessionState) -> None:
        key = self._key(call_id)
        payload = json.dumps(session.to_dict(), ensure_ascii=False)
        await self._redis.set(key, payload, ex=self._ttl)

    async def delete(self, call_id: str) -> None:
        await self._redis.delete(self._key(call_id))