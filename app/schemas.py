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
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str  

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class BookUpdate(BaseModel):
    title: str | None = None
    category: str | None = None

class BookCreate(BaseModel):
    title: str
    authors_id: list [int]
    category: str | None = None

class BookResponse(BaseModel):
    id : int
    title: str
    category: str
    class Config:
        from_attributes = True

class BookSearch(BaseModel):
    id : int | None = None
    title: str | None = None
    author_id: list[int] | None = None
    price: int | None = None
    category: str | None = None
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    state: str
    final_price: int
    date: str
    class Config:
        from_attributes = True

class OrderState(str, pyEnum):
    WAITING = "waiting"
    IN_PROCCESE = "in_proccese"
    DONE = "done"
    CANCELED = "canceled"

class OrderItemState(str, pyEnum):
    WAITING = "waiting"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PREPARING = "preparing"
    DONE = "done"

class EditionCreate(BaseModel):
    book_id: int
    price: int
    amount: int | None
    language: str
    specefic_edition_title: str | None = None

class EditionResponse(BaseModel):
    id: int
    book_id: int
    price: int
    amount: int
    language: str
    specefic_edition_title: str | None = None

class WalletInfoResponse(BaseModel):
    wallet_amount: int
    transactions: list[dict]

class BorrowResponse(BaseModel):
    id:int
    user_id: int
    edition_id: int
    status: str
    borrowed_at: str
    due_at: str
    returned_at: str