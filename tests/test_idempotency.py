import unittest

from app.Idempotency.service import IdempotencyService


class MemoryRepository:
    def __init__(self):
        self.values = {}
        self.tokens = {}

    async def get(self, key):
        return self.values.get(key)

    async def set(self, key, value, _ttl):
        self.values[key] = value

    async def set_if_not_exists(self, key, _ttl):
        if key in self.tokens:
            return None
        token = f"token-{len(self.tokens) + 1}"
        self.tokens[key] = token
        return token

    async def delete_if_owner(self, key, token):
        if self.tokens.get(key) == token:
            del self.tokens[key]


class IdempotencyTests(unittest.IsolatedAsyncioTestCase):
    async def test_lock_is_exclusive_and_owner_safe(self):
        repository = MemoryRepository()
        service = IdempotencyService(repository)

        first_token = await service.acquire_lock("order-1", ttl=30)
        second_token = await service.acquire_lock("order-1", ttl=30)

        self.assertIsNotNone(first_token)
        self.assertIsNone(second_token)

        await service.release_lock("order-1", "wrong-owner")
        self.assertIn("order-1:lock", repository.tokens)

        await service.release_lock("order-1", first_token)
        self.assertNotIn("order-1:lock", repository.tokens)

    async def test_result_is_cached_under_a_separate_key(self):
        repository = MemoryRepository()
        service = IdempotencyService(repository)

        await service.save_result("order-1", {"id": 10, "status": "created"}, ttl=60)

        self.assertEqual(
            await service.get_cached("order-1"),
            {"id": 10, "status": "created"},
        )
        self.assertNotIn("order-1", repository.values)


if __name__ == "__main__":
    unittest.main()
