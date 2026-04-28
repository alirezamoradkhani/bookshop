from app.exceptions.base import DomainException

class OrderNotFound(DomainException):
    def __init__(self):
        super().__init__(
            message="Order not found",
            code="ORDER_NOT_FOUND"
        )


class OrderDoesNotBelongToUser(DomainException):
    def __init__(self):
        super().__init__(
            message="You are not the owner of this order",
            code="ORDER_DOES_NOT_BELONG_TO_USER"
        )


class OrderNotCancelable(DomainException):
    def __init__(self):
        super().__init__(
            message="You do not have permission to cancel this order",
            code="ORDER_NOT_CANCELABLE"
        )


class InvalidOrderItemState(DomainException):
    def __init__(self):
        super().__init__(
            message="Invalid order item state",
            code="INVALID_ORDER_ITEM_STATE"
        )


