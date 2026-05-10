from app.workers.consumers.book.book_create_consumer import BookCreateConsumer
from app.workers.consumers.book.book_update_consumer import BookUpdateConsumer
from app.workers.consumers.book.book_delete_consumer import BookDeleteConsumer
from app.workers.consumers.order.order_Cancel_consumer import OrderCancelConsumer
from app.workers.consumers.order.order_item_accept_consumer import OrderItemAcceptConsumer
from app.workers.consumers.order.order_item_reject_consumer import OrderItemRejectConsumer
from app.workers.consumers.order.order_create_consumer import OrderCreateConsumer
from app.workers.consumers.user.user_create_consumer import UserCreateConsumer
from app.workers.consumers.waitlist.waitlist_create_consumer import WaitlistCreate
from app.workers.consumers.borrow.borrow_create_consumer import BorrowCreatedConsumer
from app.workers.consumers.borrow.borrow_return_consumer import BorrowReturnedConsumer
from app.workers.consumers.borrow.borrow_overdue_consomer import BorrowOverdueConsumer

CONSUMER_REGISTRY = {
    BookCreateConsumer.event_type: BookCreateConsumer,
    BookUpdateConsumer.event_type: BookUpdateConsumer,
    BookDeleteConsumer.event_type: BookDeleteConsumer,
    OrderCancelConsumer.event_type: OrderCancelConsumer,
    OrderItemAcceptConsumer.event_type: OrderItemAcceptConsumer,
    OrderItemRejectConsumer.event_type: OrderItemRejectConsumer,
    OrderCreateConsumer.event_type: OrderCreateConsumer,
    UserCreateConsumer.event_type: UserCreateConsumer,
    WaitlistCreate.event_type: WaitlistCreate,
    BorrowCreatedConsumer.event_type: BorrowCreatedConsumer,
    BorrowReturnedConsumer.event_type: BorrowReturnedConsumer,
    BorrowOverdueConsumer.event_type: BorrowOverdueConsumer,
}