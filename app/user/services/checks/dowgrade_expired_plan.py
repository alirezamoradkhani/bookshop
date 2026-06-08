from app.core.unit_of_work import UnitOfWork
from app.user.models.enums import UserPlan
from app.user.services.checks.get_expired_user_plan import get_expired_user_plan
async def downgrade_expired_plan(uow_factory):
    async with uow_factory() as uow:
        exp_user_plan = await get_expired_user_plan(uow=uow)
        
        await uow.user.many_update_plan(user_ids=[user.id for user in exp_user_plan], new_plan=UserPlan.BRONZE)