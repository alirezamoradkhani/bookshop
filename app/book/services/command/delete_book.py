from app.user.models.enums import Role

from app.unit_of_work import UnitOfWork
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.book import BookNotFound


async def delete_book(uow:UnitOfWork,book_id:int, token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        book = await uow.book.get_by_id(book_id)
        if book is None:
            raise BookNotFound
        if current_user.role == Role.AUTHOR:
            if await uow.bookauthor.get_by_authorid_and_bookid(book_id=book_id,author_id=current_user.id) == None:
                raise UserPermissionDenied
            
            await uow.book.delete_book(book=book)
        if current_user.role == Role.ADMIN:
            await uow.book.delete_book(book=book)
        return book