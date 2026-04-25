# app/events/types.py

class EventTypes:
    USER_CREATED = "UserCreated"

    BOOK_CREATED = "BookCreated"
    BOOK_UPDATED = "BookUpdated"
    BOOK_DELETED = "BookDeleted"

    ORDER_CREATED = "OrderCreated"
    ORDER_CANCELED = "OrderCanceled"

    BORROW_CREATED = "BorrowCreated"
    BORROW_RETURNED = "BorrowReturned"

    WAITLIST_PROMOTED = "WaitlistPromoted"