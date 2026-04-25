from fastapi import HTTPException
import app.borrow.models.model as model
import app.book.schemas.inputs as inputs
import app.borrow.models.enums as enums
from app.user.models.enums import Role,UserPlan
from app.borrow.services.wait_list.get_qualified_waitlist import get_qualified_waitlist
from app.borrow.services.wait_list.give_edition_to_qualified_waitlist import give_edition_to_qualified_wailist
from datetime import datetime, timedelta
from app.events.borrow.borrow_events import BorrowReturnedEvent
from app.outbox.model import OutboxEvent

from app.unit_of_work import UnitOfWork

async def return_borrow(uow:UnitOfWork,token_data:dict,borrow_id:int):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        if current_user.role != Role.USER:
            raise HTTPException(status_code=400, detail="only User have permission to borrow.")
        borrow = await uow.borrow.get_by_id(borrow_id=borrow_id)
        if borrow is None:
            raise HTTPException(status_code=400, detail="borrow not found")
        if borrow.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="this not your borrow")
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
            payload=event.__dict__
        )
        await uow.outbox.add(event=outbox_event)

        return borrow