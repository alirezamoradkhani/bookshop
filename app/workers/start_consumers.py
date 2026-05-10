# app/workers/start_consumers.py

import asyncio

from app.broker.rabit_broker import RabbitMQBroker
from app.workers.registry import CONSUMER_REGISTRY
from app.workers.dispatcheer import dispatch_message
from app.database import SessionLocal
from app.unit_of_work import UnitOfWork
from app.core.setting import settings


rabbit = RabbitMQBroker(settings.rabbitmq_url)


def uow_factory():
    return UnitOfWork(SessionLocal())


async def start_consumers():

    for event_type in CONSUMER_REGISTRY:

        queue = await rabbit.subscribe(event_type)

        await queue.consume(
            lambda msg: dispatch_message(
                msg,
                rabbit,
                uow_factory,
            )
        )

        print(f"[consumer] started => {event_type}",flush=True)

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_consumers())