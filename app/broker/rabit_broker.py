import asyncio
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

        self._connect_lock = asyncio.Lock()

    async def connect(self):

        async with self._connect_lock:

            if self.connection and not self.connection.is_closed:
                return

            self.connection = await aio_pika.connect_robust(
                self.url,
            )

            self.channel = await self.connection.channel()

            await self.channel.set_qos(
                prefetch_count=10,
            )

            self.exchange = await self.channel.declare_exchange(
                "events",
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )

            self.dlq_exchange = await self.channel.declare_exchange(
                "dlq",
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )

    async def publish(
        self,
        topic: str,
        message: dict,
    ):

        await self.connect()
        assert self.exchange is not None
        await self.exchange.publish(

            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),

            routing_key=topic,
        )

    async def subscribe(
        self,
        topic: str,
    ):

        await self.connect()
        assert self.exchange is not None
        queue = await self.channel.declare_queue(
            topic,
            durable=True,
        )

        await queue.bind(
            self.exchange,
            routing_key=topic,
        )
        assert self.dlq_exchange is not None
        dlq_queue = await self.channel.declare_queue(
            f"{topic}.dlq",
            durable=True,
        )

        await dlq_queue.bind(
            self.dlq_exchange,
            routing_key=topic,
        )

        return queue
    
    async def retry(
        self,
        message,
        retry_count: int,
    ):

        await self.connect()
        assert self.exchange is not None

        headers = dict(message.headers or {})

        headers["retry"] = retry_count

        await self.exchange.publish(

            aio_pika.Message(
                body=message.body,
                headers=headers,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),

            routing_key=message.routing_key,
        )

    async def send_to_dlq(
        self,
        message,
    ):

        await self.connect()
        assert self.dlq_exchange is not None
        await self.dlq_exchange.publish(

            aio_pika.Message(
                body=message.body,
                headers=message.headers,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),

            routing_key=message.routing_key,
        )
    
    async def close(self):

        if self.connection:

            await self.connection.close()