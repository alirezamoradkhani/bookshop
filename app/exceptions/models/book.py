from app.exceptions.base import DomainException

class BookNotFound(DomainException):
    status_code = 404
    def __init__(self):
        super().__init__(
            message="Book not found",
            code="BOOK_NOT_FOUND"
        )

class OnlyAuthorCanCreateBook(DomainException):
    status_code=403
    def __init__(self):
        super().__init__(
            message="Only authors have permission to create books.",
            code="ONLY_AUTHOR_CAN_CREATE_BOOK",
        )

