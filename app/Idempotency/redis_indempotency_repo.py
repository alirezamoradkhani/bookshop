import json
import redis.asyncio as redis
from secrets import token_urlsafe


class RedisIdempotencyRepository:

    def __init__(self, client: redis.Redis):
        self.client = client

    async def get(self, key: str):
        data = await self.client.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value, ttl: int):
        if hasattr(value, "model_dump"):  # Pydantic v2
            value = value.model_dump(mode="json")
        elif hasattr(value, "dict"):  # Pydantic v1
            value = value.dict()

        await self.client.set(key, json.dumps(value), ex=ttl)

    async def set_if_not_exists(self, key: str, ttl: int) -> str | None:
        token = token_urlsafe(24)
        acquired = await self.client.set(key, token, ex=ttl, nx=True)
        return token if acquired else None

    async def delete_if_owner(self, key: str, token: str):
        script = """
        if redis.call('get', KEYS[1]) == ARGV[1] then
            return redis.call('del', KEYS[1])
        end
        return 0
        """
        await self.client.eval(script, 1, key, token)
