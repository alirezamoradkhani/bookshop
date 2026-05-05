import app.borrow.models.model as model
from app.user.models.enums import Role,UserPlan
from datetime import datetime, timedelta
from app.exceptions.models.user import InvalidTokenUser,OnlyUserHavePrimition,PlanPermissionDenied
from app.exceptions.models.edition import EditionNotFound, EditionOutOfStock

from app.unit_of_work import UnitOfWork

async def borrow_edition(uow:UnitOfWork,token_data:dict,edition_id:int):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition
        edition = await uow.edition.get_by_id(edition_id=edition_id)
        if edition is None:
            raise EditionNotFound
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
        amount = edition.amount
        await uow.edition.update_amount(edition=edition,new_amount=amount-1)
        return new_borrow
        