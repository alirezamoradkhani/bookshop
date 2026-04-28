from app.exceptions.base import DomainException

class OrderEditionNotFound(DomainException):
    status_code = 404
    def __init__(self):
        super().__init__(
            message="Order edition not found",
            code="ORDER_EDITION_NOT_FOUND"
        )


class OrderEditionPermissionDenied(DomainException):
    status_code = 403
    def __init__(self):
        super().__init__(
            message="This is not your order edition",
            code="ORDER_EDITION_PERMISSION_DENIED"
        )