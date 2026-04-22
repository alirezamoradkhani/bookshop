from app.book.models.model import Book,BookAuthor
from app.book.models.enums import Category
from app.unit_of_work import UnitOfWork

async def seed_book(uow:UnitOfWork):
    book1 = Book(title="string", Category=Category.ART)
    await uow.book.create_book(new_book=book1)
    await uow.flush()
    author1 = await uow.baseusers.get_by_username("b")
    author2 = await uow.baseusers.get_by_username("c")
    bookauthor1 = BookAuthor(book_id=book1.id,author_id=author1.id)
    bookauthor2 = BookAuthor(book_id=book1.id,author_id=author2.id)
    await uow.bookauthor.create(bookauthor1)
    await uow.bookauthor.create(bookauthor2)