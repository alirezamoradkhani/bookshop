import app.book.schemas.inputs as inputs
from app.book.models import model
from app.user.models.enums import Role
from app.events.book.book_events import BookUpdatedEvent
from app.events.base import event_to_payload
from app.outbox.model import OutboxEvent
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
               await uow.bookcategory.delete_by_book_id(book_id=book_id)
               book_categorys = [model.BookCategory(book_id=book.id,category=category) for category in book_update.categorys]
               await uow.bookcategory.create_many(items=book_categorys)
        elif current_user.role == Role.ADMIN:
            if book_update.title is not None:
                await uow.book.update_book_title(book=book,title=book_update.title)

            if book_update.categorys is not None:
                await uow.bookcategory.delete_by_book_id(book_id=book_id)
                book_categorys = [model.BookCategory(book_id=book.id,category=category) for category in book_update.categorys]
                await uow.bookcategory.create_many(items=book_categorys)

        event = BookUpdatedEvent(book_id=book.id)
        outbox_event = OutboxEvent(
            event_type=event.event_type,
            payload=event_to_payload(event=event)
        )
        await uow.outbox.add(event=outbox_event)
        return book