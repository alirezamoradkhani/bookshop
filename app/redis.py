import redis.asyncio as redis
from app.core.setting import settings

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

async def get_redis():
    return redis_client