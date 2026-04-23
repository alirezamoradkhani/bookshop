# domain/exceptions/user.py
from app.exeptions.base import DomainException


class UserNotFound(DomainException):
    def __init__(self):
        super().__init__(
            message="User not found",
            code="USER_NOT_FOUND"
        )


class InvalidTokenUser(DomainException):
    def __init__(self):
        super().__init__(
            message="Invalid token user",
            code="INVALID_TOKEN_USER"
        )


class UserPermissionDenied(DomainException):
    def __init__(self):
        super().__init__(
            message="User does not have permission",
            code="USER_PERMISSION_DENIED"
        )


class OnlyUserCanBuy(DomainException):
    def __init__(self):
        super().__init__(
            message="Only users can buy books",
            code="ONLY_USER_CAN_BUY"
        )