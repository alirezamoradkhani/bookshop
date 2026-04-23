from fastapi import HTTPException
import app.borrow.models.model as model
import app.book.schemas.inputs as inputs
import app.book.models.enums as enums
from app.user.models.enums import Role,UserPlan
from datetime import datetime, timedelta

from app.unit_of_work import UnitOfWork

async def borrow_edition(uow:UnitOfWork,token_data:dict,edition_id:int):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        if current_user.role != Role.USER:
            raise HTTPException(status_code=400, detail="only User have permission to borrow.")
        edition = await uow.edition.get_by_id(edition_id=edition_id)
        if edition is None:
            raise HTTPException(status_code=400, detail="edition not found")
        if edition.amount < 1:
            raise HTTPException(status_code=400, detail="edition amount is 0 ")
        plan = await uow.user.get_plan_by_id(current_user.id)
        if plan == UserPlan.BRONZE:
            raise HTTPException(status_code=400, detail="bronze User dose not have permission to borrow.")
        elif plan ==UserPlan.SILVER:
            day = 7
        elif plan == UserPlan.GOLD:
            day = 14
        elif plan == UserPlan.PLATINUM:
            day = 30
        now = datetime.utcnow()
        due_at = now + timedelta(days=day)
        new_borrow = model.Borrow(user_id=current_user.id,edition_id=edition.id,borrowed_at=now,due_at=due_at)
        await uow.borrow.create(new_borrow=new_borrow)
        return new_borrow
        