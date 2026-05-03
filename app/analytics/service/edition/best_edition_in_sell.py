from app.unit_of_work import UnitOfWork
from app.query.fun_record.editions.best_edition_in_sell import best_edition_in_sell as query

from app.analytics.schemas.outputs import Best_edition_in_sell
async def best_edition_in_sell(uow:UnitOfWork):
    async with uow:
        rows = await query(uow.db)
    return [
        Best_edition_in_sell(**row._mapping)
        for row in rows
    ]