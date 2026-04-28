from app.exceptions.base import DomainException

class EditionNotFound(DomainException):
    def __init__(self, edition_id: int):
        super().__init__(
            message=f"Edition with id={edition_id} not found",
            code="EDITION_NOT_FOUND"
        )