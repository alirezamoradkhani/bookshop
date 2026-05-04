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