from dataclasses import dataclass


@dataclass
class Edition:
    id: int | None = None
    book_id: int = 0
    price: int = 0
    amount: int = 0
    isbn: str | None = None
    description: str | None = None
    specefic_edition_title: str | None = None
    is_deleted: bool = False


@dataclass
class EditionLanguage:
    id: int | None = None
    edition_id: int = 0
    language: str = ""
