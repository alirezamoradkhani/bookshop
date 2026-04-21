from fastapi import HTTPException
from app.user.models.enums import Role

from app.unit_of_work import UnitOfWork


async def delete_book(uow:UnitOfWork,book_id:int, token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        if current_user.role == Role.USER:
            raise HTTPException(status_code=400, detail="User does not have permission to add books.")
        book = await uow.book.get_by_id(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        if current_user.role == Role.AUTHOR:
            if await uow.bookauthor.get_by_authorid_and_bookid(book_id=book_id,author_id=current_user.id) == None:
                raise HTTPException(status_code=404, detail="you do not have permission to remove this book.")
            
            await uow.book.delete_book(book=book)
        if current_user.role == Role.ADMIN:
            await uow.book.delete_book(book=book)
        return book