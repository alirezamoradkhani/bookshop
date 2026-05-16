import app.book.models.model as model

from app.user.models.enums import Role

from app.external_API.providers.open_library.service import (
    OpenLibraryProvider
)

from app.exceptions.models.user import (
    InvalidOTP,
    AuthorNotFound,
    OnlyAuthorPrimition,
    UserPermissionDenied
)

from app.exceptions.models.external_service import (
    BookAleadyImported
)

from app.exceptions.models.external_service import (
    ExternalServiceCanNotFound
)

from app.unit_of_work import UnitOfWork


async def import_book(
    uow: UnitOfWork,
    ext_book_id: str,
    token_data: dict,
    provider: OpenLibraryProvider
):
    async with uow:

        current_user = await uow.baseusers.get_by_id(
            user_id=token_data["user_id"]
        )

        if current_user is None:
            raise InvalidOTP

        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition

        existing_book = await uow.book.get_by_external_id(
            external_provider="openlibrary",
            external_id=ext_book_id
        )

        if existing_book is not None:
            raise BookAleadyImported

        external_books = await provider.search_by_author(
            author=current_user.username
        )

        if not external_books:
            raise ExternalServiceCanNotFound

        external_book = next(
            (
                b for b in external_books
                if b.ext_book_id == ext_book_id
            ),
            None
        )

        if external_book is None:
            raise ExternalServiceCanNotFound

        if current_user.username not in external_book.authors:
            raise UserPermissionDenied

        author_names = external_book.authors

        authors = await uow.author.get_by_names(author_names)

        author_map = {
            a.username: a
            for a in authors
        }

        missing_authors = [
            name for name in author_names
            if name not in author_map
        ]

        if missing_authors:
            raise AuthorNotFound

        work = await provider.get_work(
            work_id=external_book.ext_book_id
        )

        categories = set(
            c.lower()
            for c in work.subjects
        )

        categories.add("imported")

        book = model.Book(
            title=external_book.title,
            external_provider="openlibrary",
            external_id=ext_book_id
        )

        await uow.book.create_book(book)

        await uow.flush()

        book_authors = [
            model.BookAuthor(
                book_id=book.id,
                author_id=author.id
            )
            for author in authors
        ]

        await uow.bookauthor.create_many(book_authors)

        book_categories = [
            model.BookCategory(
                book_id=book.id,
                category=category
            )
            for category in categories
        ]

        await uow.bookcategory.create_many(book_categories)

        return book