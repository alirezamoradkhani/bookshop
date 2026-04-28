from app.unit_of_work import UnitOfWork
from app.query.fun_record.category.best_category_in_sell import best_category_in_sell as query
from app.analytics.schemas.outputs import Best_category_in_sell

async def best_category_in_sell(uow:UnitOfWork):
    async with uow:
        rows = await query(uow.db)
    return [
        Best_category_in_sell(**row._mapping)
        for row in rows
    ]