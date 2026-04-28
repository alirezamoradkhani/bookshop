from app.user.models.enums import UserPlan
from app.borrow.models.model import Waitlist
from app.unit_of_work import UnitOfWork
from datetime import datetime


async def get_qualified_waitlist(uow:UnitOfWork,edition_id):
    async with uow:
        qualified_waitlist = await uow.waitlist.get_by_edition_id_and_user_plan(edition_id=edition_id,user_plan=UserPlan.PLATINUM)
        if qualified_waitlist is not None:
            return qualified_waitlist
        else:
            qualified_waitlist = await uow.waitlist.get_by_edition_id_and_user_plan(edition_id=edition_id,user_plan=UserPlan.GOLD)
            if qualified_waitlist is not None:
                return qualified_waitlist
            else:
                qualified_waitlist = await uow.waitlist.get_by_edition_id_and_user_plan(edition_id=edition_id,user_plan=UserPlan.SILVER)
                return qualified_waitlist

