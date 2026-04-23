from fastapi import HTTPException
from app.user.models.enums import UserPlan
from app.borrow.models.model import Waitlist
from app.unit_of_work import UnitOfWork
from datetime import datetime


async def give_edition_to_qualified_wailist(uow:UnitOfWork,waitlist:Waitlist):
    async with uow:
        ...