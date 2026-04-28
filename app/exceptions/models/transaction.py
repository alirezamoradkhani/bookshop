from app.exceptions.base import DomainException

class InsufficientFunds(DomainException):
    def __init__(self):
        super().__init__(
            message="Insufficient funds in wallet",
            code="INSUFFICIENT_FUNDS"
        )