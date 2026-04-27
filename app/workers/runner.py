import json
from app.workers.consumers.borrow.borrow_return_cunsomer import BorrowReturnedConsumer
import asyncio
from app.workers.runners.borrow.borrow_return_runner import run_book_consumer

async def all_runner(broker, uow_factory):
    await run_book_consumer(uow_factory==uow_factory,broker=broker)
#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده