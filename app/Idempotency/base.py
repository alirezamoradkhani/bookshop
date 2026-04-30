from abc import ABC, abstractmethod

class IdempotencyRepository(ABC):

    @abstractmethod
    async def get(self, key: str) -> dict | None:
        pass

    @abstractmethod
    async def set(self, key: str, value: dict, ttl: int):
        pass

    @abstractmethod
    async def set_if_not_exists(self, key: str, ttl: int) -> bool:
        pass