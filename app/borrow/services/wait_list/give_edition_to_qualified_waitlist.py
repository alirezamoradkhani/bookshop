from app.user.models.enums import UserPlan
from app.borrow.models.model import Waitlist,Borrow
from app.unit_of_work import UnitOfWork
from datetime import datetime, timedelta
from app.exceptions.models.user import PlanPermissionDenied


async def give_edition_to_qualified_wailist(uow:UnitOfWork,waitlist:Waitlist):
    async with uow:
        now = datetime.utcnow()
        plan = await uow.user.get_plan_by_id(user_id=waitlist.user_id)
        if plan == UserPlan.BRONZE:
            raise PlanPermissionDenied
        elif plan ==UserPlan.SILVER :
            day = 7
        elif plan == UserPlan.GOLD:
            day = 14
        elif plan == UserPlan.PLATINUM:
            day = 30
        due_at = now + timedelta(days=day)
        borrow = Borrow(user_id=waitlist.user_id,edition_id=waitlist.edition_id,borrowed_at=now,due_at=due_at)
        await uow.borrow.create(new_borrow=borrow)