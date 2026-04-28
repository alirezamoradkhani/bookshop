from app.exceptions.base import DomainException

class OrderEditionNotFound(DomainException):
    def __init__(self):
        super().__init__(
            message="Order edition not found",
            code="ORDER_EDITION_NOT_FOUND"
        )


class OrderEditionPermissionDenied(DomainException):
    def __init__(self):
        super().__init__(
            message="This is not your order edition",
            code="ORDER_EDITION_PERMISSION_DENIED"
        )