import asyncio
from app.Idempotency.exceptions import DuplicateRequestInProgress


def build_idempotency_handler(
    service,
    lock_ttl: int = 30,
    result_ttl: int = 3600
):

    async def handler(key: str, usecase, *args, **kwargs):

        # 1. check cache
        cached = await service.get_cached(key)
        if cached is not None:
            return cached

        # 2. try to acquire lock
        locked = await service.acquire_lock(key, lock_ttl)

        if not locked:
            #if its locked before
            # wait for result
            for _ in range(20):
                cached = await service.get_cached(key)
                if cached is not None:
                    return cached
                await asyncio.sleep(0.1)

            raise DuplicateRequestInProgress()

        # 3. execute safely
        try:
            result = await usecase(*args, **kwargs)
            print(result)

            await service.save_result(key, result, result_ttl)

            return result

        finally:
            try:
                await service.release_lock(key)
            except Exception as e:
                print(e)

    return handler