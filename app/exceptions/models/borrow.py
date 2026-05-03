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