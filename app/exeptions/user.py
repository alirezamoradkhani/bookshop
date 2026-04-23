from app.exeptions.base import DomainException


class InvalidToken(DomainException):
    def __init__(self):
        super().__init__(
            message="Invalid token",
            code="INVALID_TOKEN"
        )

class UserNotFound(DomainException):
    def __init__(self):
        super().__init__("User not found", "USER_NOT_FOUND")

class EmailAlreadyExists(DomainException):
    def __init__(self):
        super().__init__(
            message="Email already exists",
            code="EMAIL_ALREADY_EXISTS"
        )

class UserPermissionDenied(DomainException):
    def __init__(self):
        super().__init__(
            message="User has no permission",
            code="USER_PERMISSION_DENIED"
        )

class UserPlanRestricted(DomainException):
    def __init__(self):
        super().__init__(
            message="Action not allowed for user plan",
            code="USER_PLAN_RESTRICTED"
        )