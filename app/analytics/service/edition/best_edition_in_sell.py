from app.unit_of_work import UnitOfWork
from app.query.fun_record.editions.best_edition_in_sell import best_edition_in_sell as query

async def best_author_in_income(uow:UnitOfWork):
    async with uow:
        return await query(uow.db)