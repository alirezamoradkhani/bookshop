class DomainException(Exception):
    status_code: int = 400  # default

    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(message)