from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select,func,desc
from app.models import *


async def monthly_income(db:AsyncSession, token_data: dict):
    result = await db.execute(select(BaseUser).where(BaseUser.id == token_data["user_id"], BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != Role.AUTHOR:
        raise HTTPException(status_code=403, detail="Only authors have income")
    result = await db.execute(
        select(BaseUser.id,
               BaseUser.username,
               func.sum(Edition.price).label("monthly_income"))
               .join(BookAuthor,BookAuthor.author_id == BaseUser.id)
               .join(Edition, Edition.book_id == BookAuthor.book_id)
               .join(OrderEdition, OrderEdition.edition_id == Edition.id)
               .join(Order,Order.id == OrderEdition.order_id)
               .where(OrderEdition.state == OrderItemState.DONE,
                      Order.state == OrderState.DONE)
                      .group_by(BaseUser.id, BaseUser.username)
    )
    return result.scalar_one_or_none()