from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"

class UserPlan(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"