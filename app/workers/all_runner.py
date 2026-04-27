import json
from app.workers.consumers.borrow.borrow_return_consumer import BorrowReturnedConsumer
from app.workers.runners.borrow.borrow_create_runner import run_borrow_create_consumer
from app.workers.runners.borrow.borrow_return_runner import run_borrow_return_consumer
from app.workers.runners.borrow.borrow_overdue_runner import run_borrow_overdue_consumer
from app.workers.runners.book.book_create_runner import run_book_create_consumer
from app.workers.runners.book.book_update_runner import run_book_update_consumer
from app.workers.runners.book.book_delete_runner import run_book_delete_consumer
from app.workers.runners.edition.edition_create_runner import run_edition_create_consumer


async def all_runner(broker, uow_factory):
    await run_borrow_return_consumer(uow_factory=uow_factory,broker=broker)
    await run_borrow_create_consumer(uow_factory=uow_factory,broker=broker)
    await run_borrow_overdue_consumer(uow_factory=uow_factory,broker=broker)
    await run_book_create_consumer(broker=broker,uow_factory=uow_factory)
    await run_book_update_consumer(broker=broker,uow_factory=uow_factory)
    await run_book_delete_consumer(broker=broker,uow_factory=uow_factory)
    await run_edition_create_consumer(broker=broker,uow_factory=uow_factory)
#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده