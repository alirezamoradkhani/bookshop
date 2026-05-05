from app.workers.consumers.borrow.borrow_create_consumer import BorrowCreatedConsumer
from app.workers.runners.base_runner import base_runner
async def run_borrow_create_consumer(broker,uow_factory):

    consumer = BorrowCreatedConsumer()
    event_type = "BorrowCreated"
    await base_runner(broker, uow_factory, consumer, event_type)
