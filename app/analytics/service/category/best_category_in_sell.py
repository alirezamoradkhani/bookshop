from app.unit_of_work import UnitOfWork
from app.query.fun_record.category.best_category_in_sell import best_category_in_sell as query

async def best_author_in_income(uow:UnitOfWork):
    return await query(uow.db)