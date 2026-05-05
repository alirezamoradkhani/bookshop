import app.book.models.model as model
from app.user.models.enums import Role
from app.external_API.providers.open_library.service import OpenLibraryProvider
from app.exceptions.models.user import InvalidOTP, AuthorNotFound, OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.book import BookNotFound
from app.exceptions.models.external_service import BookAleadyImported

from app.unit_of_work import UnitOfWork

async def import_book(uow:UnitOfWork,book_title:str ,token_data:dict,provider:OpenLibraryProvider):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidOTP
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        Book_authors = await uow.bookauthor.get_by_author_id(current_user.id)
        for Book_author in Book_authors:
            Book = await uow.book.get_by_id(Book_author.book_id)
            Categorys = await uow.bookcategory.get_by_book_id(Book_author.book_id)
            if Book.title == book_title and "imported" in Categorys:
                raise BookAleadyImported
        external_books = await provider.search_by_title(title=book_title)
        if external_books == []:
            raise BookNotFound
        external_book = external_books[0]
        if current_user.username not in external_book.authors:
            raise UserPermissionDenied
        book = model.Book(title=external_book.title)
        await uow.book.create_book(book)
        await uow.flush()
        for author_name in external_book.authors:
            author = await uow.author.get_by_name(author_name) 
            if author is None:
                raise AuthorNotFound
            book_author = model.BookAuthor(book_id=book.id, author_id = author.id)
            await uow.bookauthor.create(book_author=book_author)
        work = await provider.get_work(work_id=external_book.work_id)
        categorys = work.subjects
        categorys.append("imported")
        for category in categorys:
            book_category = model.BookCategory(book_id = book.id, category = category.lower())
            await uow.bookcategory.create(book_category=book_category)
        return book
        
