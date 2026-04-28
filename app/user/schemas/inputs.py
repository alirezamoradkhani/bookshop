from pydantic import BaseModel, EmailStr
from enum import Enum

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str

class UserLogin(BaseModel):
    username:str
    password:str

class UserPlanUpgrade(str, Enum):
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"

class SearchAuthor(BaseModel):
    id: int | None = None
    name: str | None = None