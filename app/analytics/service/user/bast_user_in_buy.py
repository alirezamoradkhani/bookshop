from app.unit_of_work import UnitOfWork
from app.query.fun_record.users.best_user_in_buy import best_user_in_buy as query

async def best_author_in_income(uow:UnitOfWork):
    async with uow:
        return await query(uow.db)