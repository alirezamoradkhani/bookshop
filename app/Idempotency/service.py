class IdempotencyService:

    def __init__(self, repo):
        self.repo = repo

    def _lock_key(self, key: str) -> str:
        return f"{key}:lock"

    def _result_key(self, key: str) -> str:
        return f"{key}:result"

    async def get_cached(self, key: str):
        return await self.repo.get(self._result_key(key))

    async def acquire_lock(self, key: str, ttl: int):
        return await self.repo.set_if_not_exists(self._lock_key(key), ttl)

    async def release_lock(self, key: str):
        await self.repo.delete(self._lock_key(key))

    async def save_result(self, key: str, result: dict, ttl: int):
        await self.repo.set(self._result_key(key), result, ttl)