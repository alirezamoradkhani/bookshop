from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,desc
from app.models import *

async def best_user_in_buy(db: AsyncSession):
    result = await db.execute(
        select(BaseUser.id,
               BaseUser.username,
               User.plan,
               func.count(OrderEdition).label("total_buys"))
               .join(User,User.id == BaseUser.id)
               .join(Order,Order.user_id == User.id)
               .join(OrderEdition, OrderEdition.order_id == Order.id)
               .where(Order.state == OrderState.DONE, OrderEdition.state == OrderItemState.DONE)
               .group_by(BaseUser.id, BaseUser.username, User.plan)
               .order_by(desc("total_buys")).limit(20)
    )
    return result.all()