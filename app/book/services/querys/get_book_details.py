from app.exceptions.models.book import BookNotFound 

from app.unit_of_work import UnitOfWork

async def book_detail(uow:UnitOfWork,book_id: int):
    book = await uow.book.get_by_id(book_id)
    if book is None:
        raise BookNotFound
    bookauthor = await uow.bookauthor.get_by_book_id(book_id=book_id)
    authors = []
    for author in bookauthor:
        user = await uow.baseusers.get_by_id(author.author_id)
        if user:
            authors.append(user.username)
    categorys = []
    for category in await uow.bookcategory.get_by_book_id(book_id=book_id):
        categorys.append(category)

    return {"id":book.id,
            "title":book.title,
            "categorys":categorys,
            "authors": authors
    }