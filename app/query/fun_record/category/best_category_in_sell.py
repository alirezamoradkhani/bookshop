from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,desc
from app.models import *


async def best_category_in_sell(db: AsyncSession):
    result = await db.execute(
        select(BookCategory.category.label("categorys"),
               func.count(OrderEdition.order_edition_id).label("total_sales"))
               .join(Book,Book.id == BookCategory.book_id)
               .join(Edition,Edition.book_id == Book.id)
               .join(OrderEdition,OrderEdition.edition_id == Edition.id)
               .where(OrderEdition.state == OrderItemState.DONE)
                      .group_by(BookCategory.category)
                      .order_by(desc("total_sales")).limit(20)
    )
    return result.all()
