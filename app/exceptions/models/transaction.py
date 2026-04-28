from app.exceptions.base import DomainException

class InsufficientFunds(DomainException):
    status_code = 400
    def __init__(self):
        super().__init__(
            message="Insufficient funds in wallet",
            code="INSUFFICIENT_FUNDS"
        )