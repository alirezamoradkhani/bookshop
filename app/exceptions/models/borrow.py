from app.exceptions.base import DomainException

class BorrowNotFound(DomainException):
    status_code=404
    def __init__(self):
        super().__init__(message="Borrow not found",
            code="BORROW_NOT_FOUND")
        
class BorrowAlreadyReturned(DomainException):
    status_code=400
    def __init__(self):
        super().__init__(message="Borrow already returned",
            code="BORROW_ALREADY_RETURNED")

class ActiveBorrowExists(DomainException):
    status_code = 409
    def __init__(self):
        super().__init__(message="You already have an active borrow for this edition",
            code="ACTIVE_BORROW_EXISTS")
