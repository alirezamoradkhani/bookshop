class IdempotencyException(Exception):
    pass


class DuplicateRequestInProgress(IdempotencyException):
    pass