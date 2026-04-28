from app.exceptions.base import DomainException

class WaitListNotFound(DomainException):
    status_code = 404
    def __init__(self):
        super().__init__(
            message="Waitlist not found",
            code="WAITLIST_NOT_FOUND"
        )

class AlreadyInWaitList(DomainException):
    status_code = 404
    def __init__(self):
        super().__init__(
            message="user alrady Waitlist",
            code="USER_ALREADY_WAITLIST"
        )