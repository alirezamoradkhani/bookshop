from app.unit_of_work import UnitOfWork
from app.user.models.enums import UserPlan
from app.user.services.checks.get_expired_user_plan import get_expired_user_plan
async def downgrdae_expired_plan(uow:UnitOfWork):
    exp_user_plan = await get_expired_user_plan(uow=uow)
    for user in exp_user_plan:
        await uow.user.change_user_plan(user=user,new_plan=UserPlan.BRONZE)