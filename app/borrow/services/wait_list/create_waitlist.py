from fastapi import HTTPException
from app.user.models.enums import Role,UserPlan
from app.borrow.models.model import Waitlist
from app.unit_of_work import UnitOfWork
from datetime import datetime


async def add_to_wait_list(uow:UnitOfWork,token_data:dict,edition_id):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        if current_user.role != Role.USER:
            raise HTTPException(status_code=400, detail="only User have permission to borrow.")
        edition = await uow.edition.get_by_id(edition_id=edition_id)
        if edition is None:
            raise HTTPException(status_code=400, detail="edition not found")
        if edition.amount > 1:
            raise HTTPException(status_code=400, detail="edition amount is not 0 ")
        plan = await uow.user.get_plan_by_id(current_user.id)
        if plan == UserPlan.BRONZE:
            raise HTTPException(status_code=400, detail="bronze User dose not have permission to borrow.")
        now = datetime.utcnow()
        new_waitlist = Waitlist(user_id=current_user.id,edition_id=edition_id,create_at=now)
        await uow.waitlist.create(waitlist=new_waitlist)
        return Waitlist