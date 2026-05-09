import app.book.models.model as model
import app.book.schemas.inputs as inputs
from app.user.models.enums import Role
from app.exceptions.models.user import InvalidOTP, AuthorNotFound, OnlyAuthorPrimition

from app.unit_of_work import UnitOfWork

async def create_book(uow:UnitOfWork,new_book:inputs.BookCreate,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidOTP
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        book = model.Book(title=new_book.title)
        await uow.book.create_book(book)
        await uow.flush()
        authors = await uow.author.get_by_ids(new_book.authors_id)
        found_ids = {a.id for a in authors}
        missing = set(new_book.authors_id) - found_ids

        if missing:
            raise AuthorNotFound
        book_authors = [
            model.BookAuthor(book_id=book.id,
                            author_id=author.id)for author in authors]
        await uow.bookauthor.create_many(book_authors)
        book_categorys = [
            model.BookCategory(book_id=book.id, category=category.lower()) for category in new_book.categorys
        ]
        await uow.bookcategory.create_many(book_categorys)
        return book
        
