from app.unit_of_work import UnitOfWork
from app.query.fun_record.users.best_user_in_buy import best_user_in_buy as query
from app.analytics.schemas.outputs import Best_user_in_buy

async def best_user_in_buy(uow:UnitOfWork):
    async with uow:
        rows = await query(uow.db)
    return [
        Best_user_in_buy(**row._mapping)
        for row in rows
    ]