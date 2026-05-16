from app.workers.consumers.book.book_create_consumer import BookCreateConsumer
from app.workers.consumers.book.book_update_consumer import BookUpdateConsumer
from app.workers.consumers.book.book_delete_consumer import BookDeleteConsumer
from app.workers.consumers.order.order_Cancel_consumer import OrderCancelConsumer
from app.workers.consumers.order.order_item_accept_consumer import OrderItemAcceptConsumer
from app.workers.consumers.order.order_item_reject_consumer import OrderItemRejectConsumer
from app.workers.consumers.order.order_create_consumer import OrderCreateConsumer
from app.workers.consumers.user.user_create_consumer import UserCreateConsumer
from app.workers.consumers.waitlist.waitlist_create_consumer import WaitlistCreateConsumer
from app.workers.consumers.borrow.borrow_create_consumer import BorrowCreatedConsumer
from app.workers.consumers.borrow.borrow_return_consumer import BorrowReturnedConsumer
from app.workers.consumers.borrow.borrow_overdue_consomer import BorrowOverdueConsumer

from app.events.types import EventTypes
CONSUMER_REGISTRY = {
    EventTypes.USER_CREATED: UserCreateConsumer,
    EventTypes.BOOK_CREATED: BookCreateConsumer,
    EventTypes.BOOK_UPDATED: BookUpdateConsumer,
    EventTypes.BOOK_DELETED: BookDeleteConsumer,
    EventTypes.ORDER_CANCELED: OrderCancelConsumer,
    EventTypes.ORDER_ITEM_ACCEPTED: OrderItemAcceptConsumer,
    EventTypes.ORDER_ITEM_REJECTED: OrderItemRejectConsumer,
    EventTypes.ORDER_CREATED: OrderCreateConsumer,
    EventTypes.USER_CREATED: UserCreateConsumer,
    EventTypes.WAITLIST_CREATED: WaitlistCreateConsumer,
    EventTypes.BORROW_CREATED: BorrowCreatedConsumer,
    EventTypes.BORROW_RETURNED: BorrowReturnedConsumer,
    EventTypes.BORROW_OVERDUE: BorrowOverdueConsumer,
}