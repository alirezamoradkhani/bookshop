from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,desc
from app.models import *


async def best_category_in_sell(db: AsyncSession):
    result = await db.execute(
        select(Book.category.label("categorys"),
               func.count(Book.category).label("total_sales"))
               .join(Edition,Edition.book_id == Book.id)
               .join(OrderEdition,OrderEdition.edition_id == Edition.id)
               .join(Order,Order.id == OrderEdition.order_id)
               .where(OrderEdition.state == OrderItemState.DONE,
                      Order.state == OrderState.DONE)
                      .group_by(Book.category)
                      .order_by(desc("total_sales")).limit(20)
    )
    return result.all()
