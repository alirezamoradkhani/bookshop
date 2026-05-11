import redis.asyncio as redis

from app.Idempotency.redis_indempotency_repo import RedisIdempotencyRepository
from app.Idempotency.service import IdempotencyService
from app.Idempotency.main import build_idempotency_handler
from app.core.setting import settings
from app.dependency_injection.container import Container

# redis_client = redis.Redis.from_url(
#     settings.redis_url,
#     decode_responses=True
# )

container = Container()
redis_client = container.redis()

def get_idempotency_handler():
    repo = RedisIdempotencyRepository(redis_client)
    service = IdempotencyService(repo)

    return build_idempotency_handler(service)