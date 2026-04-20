from app.unit_of_work import UnitOfWork
from app.user.models.enums import UserPlan
from fastapi import HTTPException

async def delete_account(uow:UnitOfWork,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        return await uow.baseusers.soft_delete(current_user)