import json
import redis.asyncio as redis


class RedisIdempotencyRepository:

    def __init__(self, client: redis.Redis):
        self.client = client

    async def get(self, key: str):
        data = await self.client.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict, ttl: int):
        await self.client.set(key, json.dumps(value), ex=ttl)

    async def set_if_not_exists(self, key: str, ttl: int) -> bool:
        return await self.client.set(key, "LOCK", ex=ttl, nx=True)

    async def delete(self, key: str):
        await self.client.delete(key)