import app.borrow.models.model as model
from app.user.models.enums import Role,UserPlan
from datetime import datetime, timedelta, timezone
from app.exceptions.models.user import InvalidTokenUser,OnlyUserHavePrimition,PlanPermissionDenied
from app.exceptions.models.borrow import ActiveBorrowExists
from app.exceptions.models.edition import EditionNotFound, EditionOutOfStock

from app.core.unit_of_work import UnitOfWork
from app.events.borrow.borrow_events import BorrowCreatedEvent
from app.events.base import event_to_payload
from app.outbox.model import OutboxEvent

async def get_user_borrows(uow: UnitOfWork, token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id=token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition
        return await uow.borrow.get_by_user_id(current_user.id)

async def borrow_edition(uow:UnitOfWork,token_data:dict,edition_id:int):
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
        edition = await uow.edition.get_by_id(edition_id=edition_id, for_update=True)
        if edition is None:
            raise EditionNotFound
        if await uow.borrow.get_active_by_user_and_edition(current_user.id, edition.id):
            raise ActiveBorrowExists
        if edition.amount < 1:
            raise EditionOutOfStock
        plan = await uow.user.get_plan_by_id(current_user.id)
        if plan == UserPlan.BRONZE:
            raise PlanPermissionDenied
        elif plan ==UserPlan.SILVER :
            day = 7
        elif plan == UserPlan.GOLD:
            day = 14
        elif plan == UserPlan.PLATINUM:
            day = 30
        now = datetime.utcnow()
        due_at = now + timedelta(days=day)
        new_borrow = model.Borrow(user_id=current_user.id,edition_id=edition.id,borrowed_at=now,due_at=due_at)
        await uow.borrow.create(new_borrow=new_borrow)
        await uow.flush()
        amount = edition.amount
        await uow.edition.update_amount(edition=edition,new_amount=amount-1)
        event = BorrowCreatedEvent(
            borrow_id=new_borrow.id,
            edition_id=edition.id,
            user_id=current_user.id,
        )
        await uow.outbox.add(OutboxEvent(
            event_type=event.event_type,
            payload=event_to_payload(event),
        ))
        return new_borrow
