import redis.asyncio as redis

from app.Idempotency.redis_indempotency_repo import RedisIdempotencyRepository
from app.Idempotency.service import IdempotencyService
from app.Idempotency.main import build_idempotency_handler


redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)


def get_idempotency_handler():
    repo = RedisIdempotencyRepository(redis_client)
    service = IdempotencyService(repo)

    return build_idempotency_handler(service)