import app.book.models.model as model
from app.user.models.enums import Role
from app.external_API.providers.open_library.service import OpenLibraryProvider
from app.exceptions.models.user import InvalidOTP, AuthorNotFound, OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.book import BookNotFound
from app.exceptions.models.external_service import ExternalServiceCanNotFound

from app.unit_of_work import UnitOfWork

async def import_book(uow:UnitOfWork,ext_book_id: str ,token_data:dict,provider:OpenLibraryProvider):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidOTP
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        
        external_books = await provider.search_by_author(author=current_user.username)
        if external_books == []:
            raise ExternalServiceCanNotFound
        external_book = next(
            (b for b in external_books if b.ext_book_id == ext_book_id),
            None
        )
        
        if external_book is None:
            raise ExternalServiceCanNotFound
        if current_user.username not in external_book.authors:
            raise UserPermissionDenied
        book = model.Book(title=external_book.title)
        await uow.book.create_book(book)
        await uow.flush()

        author_names = external_book.authors
        authors = await uow.author.get_by_names(author_names)
        author_map = {a.username: a for a in authors}

        for name in author_names:
            if name not in author_map:
                raise AuthorNotFound
        book_authors = [
            model.BookAuthor(
                book_id=book.id,
                author_id=author_map[name].id
            )
            for name in author_names
        ]
        await uow.bookauthor.create_many(book_authors)

        work = await provider.get_work(work_id=external_book.ext_book_id)
        categorys = work.subjects
        categorys.append("imported")
        book_categories = [
            model.BookCategory(book_id=book.id, category=category.lower())
            for category in categorys
        ]
        await uow.bookcategory.create_many(book_categories)
        return book
        
