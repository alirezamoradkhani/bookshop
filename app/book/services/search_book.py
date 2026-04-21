from fastapi import HTTPException
import app.book.schemas.inputs as inputs
from app.book.models.enums import Category

from app.unit_of_work import UnitOfWork

async def search_books(uow: UnitOfWork
                ,title: str | None = None
                ,authors_id: list[int] | None = None
                ,category: Category | None = None):
    async with uow:
        books = await uow.book.search_books(
            title=title,
            category=category,
            author_ids=authors_id
        )
        return books