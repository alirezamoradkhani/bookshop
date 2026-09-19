from dataclasses import dataclass
from datetime import datetime

from app.user.models.enums import Role, UserPlan


@dataclass
class BaseUser:
    id: int | None = None
    username: str = ""
    email: str = ""
    password: str = ""
    role: Role = Role.USER
    wallet_amount: int = 0
    is_deleted: bool = False


@dataclass
class User(BaseUser):
    plan: UserPlan = UserPlan.BRONZE
    plan_expire: datetime | None = None


@dataclass
class Author(BaseUser):
    role: Role = Role.AUTHOR


@dataclass
class Admin(BaseUser):
    role: Role = Role.ADMIN
