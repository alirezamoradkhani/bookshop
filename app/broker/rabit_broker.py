import json
import aio_pika
from app.broker.base import BaseBroker


class RabbitMQBroker(BaseBroker):

    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(
            "events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

    async def _ensure_connected(self):
        if not self.connection:
            await self.connect()

    async def publish(self, topic: str, message: dict):
        await self._ensure_connected()

        assert self.exchange is not None

        await self.exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=topic
        )

    async def subscribe(self, topic: str):
        await self._ensure_connected()

        assert self.channel is not None

        queue = await self.channel.declare_queue(
            name=topic,
            durable=True
        )

        await queue.bind(
            self.exchange,
            routing_key=topic
        )

        return queue