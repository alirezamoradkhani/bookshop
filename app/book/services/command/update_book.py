import app.book.schemas.inputs as inputs
from app.book.models import model
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
    
            if book_update.title is not None:
                await uow.book.update_book_title(book=book,title=book_update.title)

            if book_update.categorys is not None:
                existing_categorys = await uow.bookcategory.get_by_book_id(book_id=book_id)
                for new_category in book_update.categorys:
                    if new_category not in existing_categorys:
                        book_category = model.BookCategory(book_id=book.id,category=new_category)
                        await uow.bookcategory.create(book_category=book_category)
                for existing_category in existing_categorys:
                    if existing_category not in book_update.categorys:
                        await uow.bookcategory.delete(existing_category)
        elif current_user.role == Role.ADMIN:
            if book_update.title is not None:
                await uow.book.update_book_title(book=book,title=book_update.title)

            if book_update.categorys is not None:
                existing_categorys = await uow.bookcategory.get_by_book_id(book_id=book_id)
                for new_category in book_update.categorys:
                    if new_category not in existing_categorys:
                        book_category = model.BookCategory(book_id=book.id,category=new_category)
                        await uow.bookcategory.create(book_category=book_category)
                for existing_category in existing_categorys:
                    if existing_category not in book_update.categorys:
                        await uow.bookcategory.delete(existing_category)
        return book