import json
import redis.asyncio as redis
from app.broker.base import BaseBroker

class RedisBroker(BaseBroker):

    def __init__(self, url: str):
        self.redis = redis.from_url(url)

    async def publish(self, topic: str, message: dict):
        await self.redis.publish(
            topic,
            json.dumps(message)
        )

    async def subscribe(self, topic: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(topic)
        return pubsub