# domain/exceptions/user.py
from app.exeptions.base import DomainException


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