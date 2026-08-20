from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from app.user.models.enums import Role

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)
    email: EmailStr
    role: Role = Role.USER

class UserLogin(BaseModel):
    username: str
    password: str = Field(min_length=1, max_length=128)

class UserPlanUpgrade(str, Enum):
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"

class SearchAuthor(BaseModel):
    id: int | None = None
    name: str | None = None
