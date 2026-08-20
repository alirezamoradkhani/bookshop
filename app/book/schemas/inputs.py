from pydantic import BaseModel, Field

class BookUpdate(BaseModel):
    title: str | None = None
    categorys: list[str] | None = None

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    authors_id: list[int] = Field(min_length=1)
    categorys: list[str] = Field(min_length=1)

class BookSearch(BaseModel):
    title: str | None = None
    author_id: int | None = None
    category: str | None = None
