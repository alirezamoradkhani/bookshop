from fastapi import HTTPException
import app.book.models.model as model
import app.book.schemas.inputs as inputs
import app.book.models.enums as enums
from app.user.models.enums import Role

from app.unit_of_work import UnitOfWork

async def create_book(uow:UnitOfWork,new_book:inputs.BookCreate,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        if current_user.role == Role.USER:
            raise HTTPException(status_code=400, detail="User does not have permission to add books.")
        book = model.Book(title=new_book.title, category = new_book.category)
        await uow.book.create_book(book)
        await uow.flush()
        for author_id in new_book.authors_id:
            book_author = model.BookAuthor(book_id=book.id, author_id = author_id)
            await uow.bookauthor.create(book_author=book_author)
        return book
        
