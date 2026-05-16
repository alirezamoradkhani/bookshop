# app/workers/outbox_worker.py

import asyncio

from app.broker.rabit_broker import RabbitMQBroker
from app.database import SessionLocal
from app.unit_of_work import UnitOfWork
from app.core.setting import settings
from app.outbox.publisher import publish_outbox_events
from app.dependency_injection.container import Container


container = Container()
# rabbit = RabbitMQBroker(settings.rabbitmq_url)


# def uow_factory():
#     return UnitOfWork(SessionLocal())


async def main():
    await container.init_resources()

    rabbit = await container.rabbitmq()
    uow_factory = container.uow

    while True:

        try:
            async with uow_factory() as uow:
                await publish_outbox_events(uow, rabbit)
                

        except Exception as e:
            print(f"[outbox] error: {e}", flush=True)

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())