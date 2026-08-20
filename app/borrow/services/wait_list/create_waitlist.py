from app.user.models.enums import Role,UserPlan
from app.borrow.models.model import Waitlist
from app.core.unit_of_work import UnitOfWork
from datetime import datetime, timezone
from app.exceptions.models.user import InvalidTokenUser,OnlyUserHavePrimition,PlanPermissionDenied
from app.exceptions.models.edition import EditionNotFound,EditionOutOfStock
from app.exceptions.models.wait_list import AlreadyInWaitList
from app.events.waitlist.waitlist_evnts import WaitlistCreateEvent
from app.events.base import event_to_payload
from app.outbox.model import OutboxEvent


async def add_to_wait_list(uow:UnitOfWork,token_data:dict,edition_id):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition
        if current_user.plan_expire is not None:
            now = datetime.now(current_user.plan_expire.tzinfo or timezone.utc)
            if current_user.plan_expire <= now:
                raise PlanPermissionDenied
        edition = await uow.edition.get_by_id(edition_id=edition_id)
        if edition is None:
            raise EditionNotFound
        if edition.amount > 0:
            raise EditionOutOfStock
        plan = await uow.user.get_plan_by_id(current_user.id)
        if plan == UserPlan.BRONZE:
            raise PlanPermissionDenied
        if await uow.waitlist.get_by_user_id_and_edition_id(user_id=current_user.id,edition_id=edition.id) is not None:
            raise AlreadyInWaitList
        now = datetime.utcnow()
        new_waitlist = Waitlist(user_id=current_user.id,edition_id=edition_id,created_at=now)
        await uow.waitlist.create(waitlist=new_waitlist)
        await uow.flush()
        event = WaitlistCreateEvent(edition_id=edition.id, user_id=current_user.id)
        await uow.outbox.add(OutboxEvent(
            event_type=event.event_type,
            payload=event_to_payload(event),
        ))
        return new_waitlist
