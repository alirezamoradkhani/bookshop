# domain/exceptions/inventory.py
from app.exceptions.base import DomainException

class EditionNotFound(DomainException):
    status_code = 404
    def __init__(self):
        super().__init__(
            message="Edition not found",
            code="EDITION_NOT_FOUND"
        )


class EditionOutOfStock(DomainException):
    status_code = 400
    def __init__(self):
        super().__init__(
            message="Edition is out of stock",
            code="EDITION_OUT_OF_STOCK"
        )

class InvalidAmount(DomainException):
    status_code = 400
    def __init__(self):
        super().__init__(
            message="Invalid amount",
            code="INVALID_AMOUNT")
        
class InvalidPrice(DomainException):
    status_code = 400
    def __init__(self):
        super().__init__(
            message="Invalid price",
            code="INVALID_PRICE")