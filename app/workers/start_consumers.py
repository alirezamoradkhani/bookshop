# app/workers/start_consumers.py

import asyncio

from app.broker.rabit_broker import RabbitMQBroker
from app.workers.registry import CONSUMER_REGISTRY
from app.workers.dispatcheer import dispatch_message
from app.database import SessionLocal
from app.unit_of_work import UnitOfWork
from app.core.setting import settings
from app.dependency_injection.container import Container

container = Container()


# rabbit = RabbitMQBroker(settings.rabbitmq_url)


# def uow_factory():
#     return UnitOfWork(SessionLocal())

print("[consumer] worker starting", flush=True)
async def start_consumers():

    await container.init_resources()

    rabbit = await container.rabbitmq()
    uow_factory = container.uow

    async def handler(msg):
        print("[handler] called", flush=True)

        try:
            await dispatch_message(msg, rabbit, uow_factory)
        except Exception as e:
            print(f"[handler] crash={repr(e)}", flush=True)

        print("🔥 GOT MESSAGE", flush=True)
        
    print(len(CONSUMER_REGISTRY), flush=True)
    for event_type in CONSUMER_REGISTRY:
        print("before subscribe", event_type, flush=True)
        queue = await rabbit.subscribe(event_type)
        print("QUEUE:", queue.name, flush=True)
        print("EVENT TYPE:", event_type, flush=True)
        print("after subscribe", event_type, flush=True)
        print(type(queue),flush=True)
        print(queue,flush=True)
        await queue.consume(handler)

        print(f"[consumer] started => {event_type}")
    

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_consumers())