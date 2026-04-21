from fastapi import HTTPException
import app.book.schemas.inputs as inputs

from app.unit_of_work import UnitOfWork

async def search_books(uow: UnitOfWork, search: inputs.BookSearch):
    async with uow:
        books = await uow.book.search_books(
            title=search.title,
            category=search.category,
            author_ids=search.authors_id
        )
        return books