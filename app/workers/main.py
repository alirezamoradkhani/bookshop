import asyncio

from app.unit_of_work import UnitOfWork
from app.database import SessionLocal
from app.broker.redis_broker import RedisBroker
from app.broker.rabit_broker import RabbitMQBroker
from app.workers.all_runner import all_runner
from app.workers.outbox_worker import run_outbox_worker
from app.core.setting import settings


redis_broker = RedisBroker(url=settings.redis_url)
rabit_broker = RabbitMQBroker(url=settings.rabbitmq_url)


def uow_factory():
    db = SessionLocal()
    return UnitOfWork(db)

async def main():

    await asyncio.gather(
        all_runner(broker=rabit_broker,uow_factory=uow_factory),
        run_outbox_worker(broker=rabit_broker,uow_factory=uow_factory),
    )


if __name__ == "__main__":
    
    asyncio.run(main())