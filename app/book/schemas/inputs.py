from pydantic import BaseModel

class BookUpdate(BaseModel):
    title: str | None = None
    category: str | None = None

class BookCreate(BaseModel):
    title: str
    authors_id: list [int]
    category: str | None = None

class BookSearch(BaseModel):
    title: str | None = None
    authors_id: list[int] | None = None
    category: str | None = None