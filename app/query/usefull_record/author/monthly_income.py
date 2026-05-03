from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select,func,desc
from app.models import *


async def monthly_income(db:AsyncSession, user:BaseUser):
    result = await db.execute(
        select(BaseUser.id.label("author_id"),
               BaseUser.username.label("aythor_name"),
               func.sum(OrderEdition.price).label("monthly_income"))
               .join(BookAuthor,BookAuthor.author_id == BaseUser.id)
               .join(Edition, Edition.book_id == BookAuthor.book_id)
               .join(OrderEdition, OrderEdition.edition_id == Edition.id)
               .join(Order,Order.id == OrderEdition.order_id)
               .where(OrderEdition.state == OrderItemState.DONE,
                      Order.state == OrderState.DONE,)
                      .group_by(BaseUser.id, BaseUser.username)
    )
    return result.scalar_one_or_none()