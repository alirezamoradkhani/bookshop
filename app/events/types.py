# app/events/types.py

class EventTypes:
    USER_CREATED = "UserCreated"

    BOOK_CREATED = "BookCreated"
    BOOK_UPDATED = "BookUpdated"
    BOOK_DELETED = "BookDeleted"

    EDITION_Create = "EditionCreated"
    EDITION_UPDATED = "EditionUpdated"
    EDITION_DELETED = "EditionDeleted"

    ORDER_CREATED = "OrderCreated"
    ORDER_CANCELED = "OrderCanceled"

    BORROW_CREATED = "BorrowCreated"
    BORROW_RETURNED = "BorrowReturned"
    BORROW_OVERDUE = "BorrowOverdue"

    ORDER_ITEM_ACCEPTED = "OrderItemAccepted"
    ORDER_ITEM_REJECTED = "OrderItemRejected"
    WAITLIST_CREATED = "WaitlistCreated"
    WAITLIST_PROMOTED = "WaitlistPromoted"