from pydantic import BaseModel

class BookUpdate(BaseModel):
    title: str | None = None
    categorys: list[str] | None = None

class BookCreate(BaseModel):
    title: str
    authors_id: list [int]
    categorys: list[str]

class BookSearch(BaseModel):
    title: str | None = None
    author_id: int | None = None
    category: str | None = None
