import app.borrow.models.enums as enums
from app.user.models.enums import Role
from datetime import datetime
from app.events.borrow.borrow_events import BorrowReturnedEvent
from app.events.base import event_to_payload
from app.outbox.model import OutboxEvent
from app.exceptions.models.user import InvalidTokenUser,OnlyUserHavePrimition,UserPermissionDenied
from app.exceptions.models.borrow import BorrowNotFound,BorrowAlreadyReturned
from app.unit_of_work import UnitOfWork

async def return_borrow(uow:UnitOfWork,token_data:dict,borrow_id:int):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition
        
        borrow = await uow.borrow.get_by_id(borrow_id=borrow_id)
        if borrow is None:
            raise BorrowNotFound
        if borrow.user_id != current_user.id:
            raise UserPermissionDenied
        if borrow.status == enums.BorrowStatus.RETURNED:
            raise BorrowAlreadyReturned
        await uow.borrow.update_status(borrow=borrow,new_status=enums.BorrowStatus.RETURNED)
        now = datetime.utcnow()
        await uow.borrow.set_Return_time(borrow=borrow,return_time=now)
        edition = await uow.edition.get_by_id(edition_id=borrow.edition_id)
    
        await uow.edition.update_amount(edition=edition,new_amount=edition.amount+1)
        event = BorrowReturnedEvent(
            edition_id=borrow.edition_id,
            returned_by=current_user.id
        )

        outbox_event = OutboxEvent(
            event_type=event.event_type,
            payload = event_to_payload(event=event)
        )
        await uow.outbox.add(event=outbox_event)

        return borrow