import asyncio
import logging
from app.Idempotency.exceptions import DuplicateRequestInProgress

logger = logging.getLogger(__name__)


def build_idempotency_handler(
    service,
    lock_ttl: int = 30,
    result_ttl: int = 3600
):

    async def handler(key: str, usecase, *args, **kwargs):
        user = kwargs.get("token_data") or kwargs.get("toke_data") or {}
        user_id = user.get("user_id", "anonymous") if isinstance(user, dict) else "anonymous"
        scoped_key = f"{usecase.__module__}:{usecase.__name__}:{user_id}:{key}"

        # 1. check cache
        cached = await service.get_cached(scoped_key)
        if cached is not None:
            return cached

        # 2. try to acquire lock
        lock_token = await service.acquire_lock(scoped_key, lock_ttl)

        if not lock_token:
            #if its locked before
            # wait for result
            for _ in range(20):
                cached = await service.get_cached(scoped_key)
                if cached is not None:
                    return cached
                await asyncio.sleep(0.1)

            raise DuplicateRequestInProgress()

        # 3. execute safely
        try:
            result = await usecase(*args, **kwargs)

            await service.save_result(scoped_key, result, result_ttl)

            return result

        finally:
            try:
                await service.release_lock(scoped_key, lock_token)
            except Exception:
                logger.exception("Failed to release idempotency lock")

    return handler
