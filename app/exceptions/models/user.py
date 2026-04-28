# domain/exceptions/user.py
from app.exceptions.base import DomainException


class InvalidTokenUser(DomainException):
    status_code = 401
    def __init__(self):
        super().__init__(
            message="Invalid token user",
            code="INVALID_TOKEN_USER"
        )


class EmailAlreadyRegistered(DomainException):
    status_code = 409
    def __init__(self):
        super().__init__(
            message="Email already registered",
            code="EMAIL_ALREADY_REGISTERED"
        )


class UsernameAlreadyExists(DomainException):
    status_code = 409
    def __init__(self):
        super().__init__(
            message="Username already exists",
            code="USERNAME_ALREADY_EXISTS"
        )

class InvalidCredentials(DomainException):
    status_code = 401
    def __init__(self):
        super().__init__(
            message="Invalid username or password",
            code="INVALID_CREDENTIALS"
        )


class InvalidOTP(DomainException):
    status_code = 401
    def __init__(self):
        super().__init__(
            message="Invalid OTP",
            code="INVALID_OTP"
        )

class UserNotFound(DomainException):
    def __init__(self):
        super().__init__(
            message="User not found",
            code="USER_NOT_FOUND"
            
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