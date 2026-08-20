from pydantic import BaseModel, Field

class EditionCreate(BaseModel):
    book_id: int
    price: int = Field(ge=0)
    amount: int = Field(default=0, ge=0)
    language: list[str] = Field(min_length=1)
    specefic_edition_title: str | None = None
    isbn: str | None = None
    description: str | None = None
