import json
import aio_pika
from app.broker.base import BaseBroker


class RabbitMQBroker(BaseBroker):

    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None
        self.exchange = None
        self.dlq_exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(
            "events",
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        self.dlq_exchange = await self.channel.declare_exchange(
            "dlq-exchange",
            aio_pika.ExchangeType.FANOUT,
            durable=True,
        )

    async def _ensure_connected(self):
        if not self.connection or self.connection.is_closed:
            await self.connect()

    async def publish(self, topic: str, message: dict):
        await self._ensure_connected()
        assert self.exchange is not None
        await self.exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=topic,
        )

    async def subscribe(self, topic: str):
        await self._ensure_connected()
        assert self.channel is not None
        queue = await self.channel.declare_queue(
            name=topic,
            durable=True,
        )

        await queue.bind(self.exchange, routing_key=topic)

        return queue

    async def retry(self, message: aio_pika.IncomingMessage, retry_count: int):
        await self._ensure_connected()

        headers = dict(message.headers or {})
        headers["retry"] = retry_count
        assert self.exchange is not None
        await self.exchange.publish(
            aio_pika.Message(
                body=message.body,
                headers=headers,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=message.routing_key,
        )

    async def send_to_dlq(self, message: aio_pika.IncomingMessage):
        await self._ensure_connected()

        headers = dict(message.headers or {})
        assert self.dlq_exchange is not None
        await self.dlq_exchange.publish(
            aio_pika.Message(
                body=message.body,
                headers=headers,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key="",
        )