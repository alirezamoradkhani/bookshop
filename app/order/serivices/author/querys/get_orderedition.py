from app.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition


async def get_order_edition(uow:UnitOfWork, token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        books = await uow.bookauthor.get_by_author_id(current_user.id)
        for book in books:
            editions = await uow.edition.get_by_book_id(book_id=book.book_id)
        return await uow.orderedition.get_orderedition_by_list_of_edition(editions=editions)