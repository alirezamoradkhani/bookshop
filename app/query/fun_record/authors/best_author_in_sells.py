from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,desc
from app.models import *


async def best_author_in_sell(db: AsyncSession):
    result = await db.execute(
    select(
        Author.id,
        BaseUser.username,
        func.count(OrderEdition.edition_id).label("total_sales")
    )
    .join(BaseUser,BaseUser.id == Author.id)
    .join(BookAuthor, BookAuthor.author_id == Author.id)
    .join(Book, Book.id ==BookAuthor.book_id)
    .join(Edition, Edition.book_id == Book.id)
    .join(OrderEdition, OrderEdition.edition_id == Edition.id)
    .join(Order, Order.id == OrderEdition.order_id)
    .where(
        Order.state == OrderState.DONE,
        OrderEdition.state == OrderItemState.DONE
    )
    .group_by(Author.id, BaseUser.username)
    .order_by(desc("total_sales")).limit(20)
)
    return result.all()