# domain/exceptions/auth.py
from app.exeptions.base import DomainException


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