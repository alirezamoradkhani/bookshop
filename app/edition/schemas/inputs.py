from pydantic import BaseModel

class EditionCreate(BaseModel):
    book_id: int
    price: int
    amount: int | None
    language: list[str]
    specefic_edition_title: str | None = None
    isbn: str | None = None
    description: str | None = None