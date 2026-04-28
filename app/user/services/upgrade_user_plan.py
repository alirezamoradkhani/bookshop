from app.unit_of_work import UnitOfWork
from app.user.schemas.inputs import UserPlanUpgrade
from app.exceptions.models.user import InvalidOTP


async def upgrade_plan(uow:UnitOfWork,new_plan:UserPlanUpgrade,token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(token_data["user_id"])
        if current_user is None:
            raise InvalidOTP
        return await uow.user.update_plan(new_plan=new_plan,id=current_user.id)