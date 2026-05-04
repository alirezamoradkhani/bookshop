import redis.asyncio as redis

from app.Idempotency.redis_indempotency_repo import RedisIdempotencyRepository
from app.Idempotency.service import IdempotencyService
from app.Idempotency.main import build_idempotency_handler
from app.core.setting import settings

redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True
)

def get_idempotency_handler():
    repo = RedisIdempotencyRepository(redis_client)
    service = IdempotencyService(repo)

    return build_idempotency_handler(service)