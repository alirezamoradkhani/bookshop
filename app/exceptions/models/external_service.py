from app.exceptions.base import DomainException


class ExternalServiceError(DomainException):
    status_code = 503

    def __init__(self):
        super().__init__(
            message="External service error",
            code="EXTERNAL_SERVICE_ERROR"
        )


class ExternalServiceTimeout(DomainException):
    status_code = 504

    def __init__(self):
        super().__init__(
            message="External service timeout",
            code="EXTERNAL_SERVICE_TIMEOUT"
        )


class ExternalServiceUnavailable(DomainException):
    status_code = 503

    def __init__(self):
        super().__init__(
            message="External service unavailable",
            code="EXTERNAL_SERVICE_UNAVAILABLE"
        )


class ExternalServiceCanNotFound(DomainException):
    status_code = 404

    def __init__(self):
        super().__init__(
            message="External service can not found",
            code="EXTERNAL_SERVICE_CAN_NOT_FOUND"
        )


class LanguageNotSuported(DomainException):
    status_code = 400

    def __init__(self):
        super().__init__(
            message="Language Not Suported",
            code="LANGUAGE_NOT_SUPORTED"
        )


class BookAleadyImported(DomainException):
    status_code = 409

    def __init__(self):
        super().__init__(
            message="Boook Already Imported",
            code="BOOK_ALREADY_IMPORTED"
        )