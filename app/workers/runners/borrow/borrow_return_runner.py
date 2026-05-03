import json
from app.workers.consumers.borrow.borrow_return_consumer import BorrowReturnedConsumer
import asyncio
from app.workers.runners.base_runner import base_runner


async def run_borrow_return_consumer(broker, uow_factory):

    consumer = BorrowReturnedConsumer()
    event_type = "BorrowReturned"
    await base_runner(broker, uow_factory, consumer, event_type)

#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده