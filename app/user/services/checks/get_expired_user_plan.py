from app.unit_of_work import UnitOfWork
from datetime import datetime
async def get_expired_user_plan(uow:UnitOfWork):
    now = datetime.utcnow()
    users = await uow.user.get_plan_by_exp_date(now=now)
    return users