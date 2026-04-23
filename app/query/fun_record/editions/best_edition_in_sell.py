from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,desc
from app.models import *


async def best_edition_in_sell(db: AsyncSession):
    result = await db.execute(
        select(Book.id,
               Book.title,
               Edition.id,
               Edition.specefic_edition_title,
               func.count(OrderEdition.id).label("total_sales"))
               .join(Edition,Book.id == Edition.book_id)
               .join(OrderEdition,OrderEdition.edition_id == Edition.id)
               .join(Order,Order.id == OrderEdition.order_id)
               .where(Order.state == OrderState.DONE,
                      OrderEdition.state == OrderItemState.DONE)
                      .group_by(Edition.id, Book.id,Book.title,Edition.specefic_edition_title)
                      .order_by(desc("total_sales")).limit(20)
    )
    return result.all()