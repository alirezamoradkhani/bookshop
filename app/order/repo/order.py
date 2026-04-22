from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.order.models import model
from app.order.models import enums


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_order(self,order:model.Order):
        self.db.add(order)

    async def get_by_id(self,order_id:int):
        result = await self.db.execute(select(model.Order).where(model.Order.id == order_id))
        return result.scalar_one_or_none()
    
    async def update_order_atate(self,order:model.Order, new_state: enums.OrderState):
        order.state = new_state

    async def update_final_price(self,order:model.Order,change: int):
        order.final_price -= change

    async def get_by_state(self,state:enums.OrderState):
        result = await self.db.execute(select(model.Order).where(model.Order.state == state))
        return result.scalars().all()