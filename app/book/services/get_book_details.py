from fastapi import HTTPException
import app.book.models.model as model
import app.book.schemas.inputs as inputs
import app.book.models.enums as enums
from app.user.models.enums import Role

from app.unit_of_work import UnitOfWork

async def book_detail(uow:UnitOfWork,book_id: int):
    book = await uow.book.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    bookauthor = await uow.bookauthor.get_by_book_id(book_id=book_id)
    authors = []
    for author in bookauthor:
        user = await uow.baseusers.get_by_id(author.author_id)
        if user:
            authors.append(user.username)

    return {"id":book.id,
            "title":book.title,
            "category":book.category,
            "authors": authors
    }