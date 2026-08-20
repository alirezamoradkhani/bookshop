from app.transaction.schemas.outputs import UserResponse
from app.core.unit_of_work import UnitOfWork
from app.user.schemas.inputs import UserPlanUpgrade
from app.exceptions.models.user import InvalidTokenUser, InvalidPlanChange, OnlyUserHavePrimition
from app.user.models.enums import UserPlan, Role
from datetime import datetime, timedelta


async def upgrade_plan(uow:UnitOfWork,new_plan:UserPlanUpgrade,token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition
        plan_rank = {
            UserPlan.BRONZE: 0,
            UserPlan.SILVER: 1,
            UserPlan.GOLD: 2,
            UserPlan.PLATINUM: 3,
        }
        target_plan = UserPlan(new_plan.value)
        if plan_rank[target_plan] <= plan_rank[current_user.plan]:
            raise InvalidPlanChange
        exp = datetime.utcnow() + timedelta(days=30)
        user = await uow.user.update_plan(new_plan=target_plan,id=current_user.id,ex=exp)
        return UserResponse.model_validate(user).model_dump()
