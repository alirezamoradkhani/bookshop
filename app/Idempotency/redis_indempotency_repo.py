import json
import redis.asyncio as redis


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

    async def set_if_not_exists(self, key: str, ttl: int) -> bool:
        return await self.client.set(key, "LOCK", ex=ttl, nx=True)

    async def delete(self, key: str):
        await self.client.delete(key)