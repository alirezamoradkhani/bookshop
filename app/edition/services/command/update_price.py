from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.edition import EditionNotFound,InvalidPrice
from app.events.edition.edition_events import EditionUpdatedEvent
from app.outbox.model import OutboxEvent
from app.events.base import event_to_payload



from app.core.unit_of_work import UnitOfWork

async def update_price(uow:UnitOfWork, token_data:dict,edition_id:int, new_price: int):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        
        edition = await uow.edition.get_by_id(edition_id)
        if not edition:
            raise EditionNotFound
        if current_user.role == Role.AUTHOR:
            bookauthor = await uow.bookauthor.get_by_authorid_and_bookid(
                book_id=edition.book_id,
                author_id=current_user.id
            )
            if bookauthor is None:
                raise UserPermissionDenied
        if new_price < 0:
            raise InvalidPrice
        await uow.edition.update_price(edition=edition,new_price=new_price)

        event = EditionUpdatedEvent(edition_id=edition_id)
        outbox_event = OutboxEvent(
            event_type=event.event_type,
            payload=event_to_payload(event=event)
        )
        await uow.outbox.add(event=outbox_event)
    return edition