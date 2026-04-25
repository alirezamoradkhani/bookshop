import asyncio

from app.unit_of_work import UnitOfWork
from app.database import SessionLocal
from app.broker.redis_broker import RedisBroker
from app.workers.runner import run_book_consumer
from app.workers.outbox_worker import run_outbox_worker

broker = RedisBroker(url="redis://localhost:6379")

def uow_factory():
    db = SessionLocal()
    return UnitOfWork(db)

async def main():

    await asyncio.gather(
        run_book_consumer(broker=broker,uow=uow_factory()),
        run_outbox_worker(broker=broker,uow=uow_factory()),
    )


if __name__ == "__main__":
    
    asyncio.run(main())