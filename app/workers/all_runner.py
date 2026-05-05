from app.workers.runners.borrow.borrow_create_runner import run_borrow_create_consumer
from app.workers.runners.borrow.borrow_return_runner import run_borrow_return_consumer
from app.workers.runners.borrow.borrow_overdue_runner import run_borrow_overdue_consumer
from app.workers.runners.book.book_create_runner import run_book_create_consumer
from app.workers.runners.book.book_update_runner import run_book_update_consumer
from app.workers.runners.book.book_delete_runner import run_book_delete_consumer
from app.workers.runners.edition.edition_create_runner import run_edition_create_consumer
from app.workers.runners.edition.edition_update_runner import run_edition_update_consumer
from app.workers.runners.edition.edition_delete_runner import run_edition_delete_consumer
from app.workers.runners.order.order_create_runner import run_order_create_consumer
from app.workers.runners.order.order_cancel_runner import run_order_cancel_consumer
from app.workers.runners.order.order_item_accept_runner import run_order_item_accept_consumer
from app.workers.runners.order.order_item_reject_runner import run_order_item_reject_consumer
from app.workers.runners.user.user_create_runner import run_user_create_consumer
from app.workers.runners.waitlist.waitlist_create_runner import run_waitlist_create_consumer


async def all_runner(broker, uow_factory):
    await run_borrow_return_consumer(uow_factory=uow_factory,broker=broker)
    await run_borrow_create_consumer(uow_factory=uow_factory,broker=broker)
    await run_borrow_overdue_consumer(uow_factory=uow_factory,broker=broker)
    await run_book_create_consumer(broker=broker,uow_factory=uow_factory)
    await run_book_update_consumer(broker=broker,uow_factory=uow_factory)
    await run_book_delete_consumer(broker=broker,uow_factory=uow_factory)
    await run_edition_create_consumer(broker=broker,uow_factory=uow_factory)
    await run_edition_update_consumer(broker=broker,uow_factory=uow_factory)
    await run_edition_delete_consumer(broker=broker,uow_factory=uow_factory)
    await run_order_create_consumer(broker=broker,uow_factory=uow_factory)
    await run_order_cancel_consumer(broker=broker,uow_factory=uow_factory)
    await run_order_item_accept_consumer(broker=broker,uow_factory=uow_factory)
    await run_order_item_reject_consumer(broker=broker,uow_factory=uow_factory)
    await run_user_create_consumer(broker=broker,uow_factory=uow_factory)
    await run_waitlist_create_consumer(broker=broker,uow_factory=uow_factory)

#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده