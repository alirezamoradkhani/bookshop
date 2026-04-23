from app.unit_of_work import UnitOfWork
from app.query.fun_record.authors.best_author_in_sells import best_author_in_sell as query


async def monthly_income(uow:UnitOfWork):
    async with uow:
        return await query(uow.db)