from app.unit_of_work import UnitOfWork
from app.query.fun_record.authors.best_author_in_sells import best_author_in_sell as query
from app.analytics.schemas.outputs import Best_author_in_sell

async def best_author_in_sell(uow:UnitOfWork):
    async with uow:
        rows = await query(uow.db)
    return [
        Best_author_in_sell(**row._mapping)
        for row in rows
    ]