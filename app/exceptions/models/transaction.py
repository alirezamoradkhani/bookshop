from app.exceptions.base import DomainException

class InsufficientFunds(DomainException):
    status_code = 400
    def __init__(self):
        super().__init__(
            message="Insufficient funds in wallet",
            code="INSUFFICIENT_FUNDS"
        )

class ReciverNotFound(DomainException):
    status_code = 404
    def __init__(self):
        super().__init__(
            message="Reciver not found",
            code="RECIVER_NOT_FOUND")