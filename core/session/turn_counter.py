from __future__ import annotations

from redis.asyncio import Redis

class TurnCounter:
    """
    Redis-backed atomic turn counter.

    Key:
    turn: {call_id} -> integer

    We keep TTL aligned with session TTL so it disappears automatically.
    """
    def __init__(self, redis: Redis, ttl_seconds: int) -> None:
        self._redis = redis
        self._ttl = ttl_seconds

    def key(slef, call_id: str) -> str:
        return f"turn:{call_id}"

    async def next_turn_id(self, call_id: str) -> int:
        """
        Automatically increment and return the next turn_id.
        """
        key = self._key(call_id)
        value = await self._redis.incr(key)

        await self._redis.expire(key, self._ttl)
        return int(value)

    async def reset(self, call_id: str) -> None:
        await self._redis.delete(self._key(call_id))