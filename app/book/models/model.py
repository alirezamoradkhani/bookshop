from dataclasses import dataclass, field


@dataclass
class Book:
    id: int | None = None
    title: str = ""
    is_deleted: bool = False
    external_provider: str | None = None
    external_id: str | None = None
    author_ids: list[int] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)


@dataclass
class BookAuthor:
    id: int | None = None
    book_id: int = 0
    author_id: int = 0


@dataclass
class BookCategory:
    id: int | None = None
    book_id: int = 0
    category: str = ""
