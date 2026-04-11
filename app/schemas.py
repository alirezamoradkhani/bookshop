from pydantic import BaseModel, EmailStr
from enum import Enum as pyEnum


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str 

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    wallet_amount: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str  

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class BookUpdate(BaseModel):
    title: str
    author_id: int | None = None
    amount: int | None = None

class BookCreate(BaseModel):
    title: str
    authors_id: list [int] | None = None
    amount: int | None = None
    price: int
    category: str | None = None

class BookResponse(BaseModel):
    id : int
    title: str
    author_id: list[int]
    amount: int
    price: int
    category: str
    class Config:
        orm_mode = True

class BookSearch(BaseModel):
    id : int | None = None
    title: str | None = None
    author_id: list[int] | None = None
    price: int | None = None
    category: str | None = None
    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    book_id: int
    customer_id: int
    id: int
    state: str
    price: int
    date: str
    class Config:
        orm_mode = True

class OrderState(str, pyEnum):
    WAITFORSELLER = "waitforseller"
    INPROCCES = "inprocces"
    DONE = "done"
    CANCELED = "canceled"

class WalletInfoResponse(BaseModel):
    wallet_amount: int
    transactions: list[dict]