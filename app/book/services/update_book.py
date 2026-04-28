import app.book.schemas.inputs as inputs
import app.book.models.enums as enums
from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.book import BookNotFound

from app.unit_of_work import UnitOfWork

async def update_book(uow:UnitOfWork, token_data:dict,book_id:int,book_update:inputs.BookUpdate):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        book = await uow.book.get_by_id(book_id)
        if book is None:
            raise BookNotFound
        elif current_user.role == Role.AUTHOR:
            if await uow.bookauthor.get_by_authorid_and_bookid(book_id=book_id,author_id=current_user.id) == None:
                raise UserPermissionDenied
            if book_update.category is not None:
                new_category = enums.Category(book_update.category)
                await uow.book.update_book_category(book=book,category=new_category)
            if book_update.title is not None:
                await uow.book.update_book_title(book=book,title=book_update.title)
        elif current_user.role == Role.ADMIN:
            if book_update.category is not None:
                new_category = enums.Category(book_update.category)
                await uow.book.update_book_category(book=book,category=new_category)
            if book_update.title is not None:
                await uow.book.update_book_title(book=book,title=book_update.title)
        return book