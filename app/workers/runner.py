import json
from app.workers.consumers.borrow.borrow_return_cunsomer import BorrowReturnedConsumer
from app.workers.runners.borrow.borrow_create_runner import run_borrow_create_consumer
from app.workers.runners.borrow.borrow_return_runner import run_borrow_return_consumer

async def all_runner(broker, uow_factory):
    await run_borrow_return_consumer(uow_factory==uow_factory,broker=broker)
    await run_borrow_create_consumer(uow_factory==uow_factory,broker=broker)
#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده