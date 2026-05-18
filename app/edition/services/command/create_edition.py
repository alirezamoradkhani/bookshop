from app.edition.models import model
from app.edition.schemas.inputs import EditionCreate
from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.book import BookNotFound
from app.exceptions.models.edition import InvalidPrice, InvalidAmount
from app.events.edition.edition_events import EditionCreatedEvent
from app.events.base import event_to_payload
from app.outbox.model import OutboxEvent

from app.unit_of_work import UnitOfWork

async def create_edition(uow:UnitOfWork,edition:EditionCreate,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        
        book = await uow.book.get_by_id(edition.book_id)

        if book is None:
            raise BookNotFound
        
        if current_user.role == Role.AUTHOR:
            if await uow.bookauthor.get_by_authorid_and_bookid(book_id=book.id,author_id=current_user.id) == None:
                raise UserPermissionDenied
            
        if edition.amount is not None and edition.amount < 0:
            raise InvalidAmount

        if edition.price < 0:
            raise InvalidPrice
        new_edition = model.Edition(
            book_id=edition.book_id
            ,price=edition.price
            ,amount = edition.amount
            ,specefic_edition_title = edition.specefic_edition_title
            ,isbn = edition.isbn
            ,description = edition.description
            )
        await uow.edition.create_edition(new_edition)
        await uow.flush()
        edition_languages = [
            model.EditionLanguage(edition_id=new_edition.id,language=language.lower()) for language in edition.language
        ]
        await uow.editionlanguage.create_many(edition_languages)

        await uow.flush()
        event = EditionCreatedEvent(edition_id=new_edition.id)
        outbox_event = OutboxEvent(
            event_type=event.event_type,
            payload=event_to_payload(event=event)
        )
        await uow.outbox.add(event=outbox_event)
        return new_edition