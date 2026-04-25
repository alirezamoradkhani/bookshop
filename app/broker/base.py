from abc import ABC, abstractmethod

class BaseBroker(ABC):

    @abstractmethod
    async def publish(self, topic: str, message: dict):
        pass

    @abstractmethod
    async def subscribe(self, topic: str):
        pass