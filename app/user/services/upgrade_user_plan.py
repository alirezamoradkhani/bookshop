from app.unit_of_work import UnitOfWork
from app.user.schemas.inputs import UserPlanUpgrade
from fastapi import HTTPException
async def upgrade_plan(uow:UnitOfWork,new_plan:UserPlanUpgrade,token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        return await uow.user.update_plan(new_plan=new_plan,id=current_user.id)