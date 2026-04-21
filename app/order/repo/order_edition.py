from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.order.models import model
from app.order.models import enums


class OrderEditionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self,orderedition: model.OrderEdition):
        self.db.add(orderedition)

    async def update_state(self,new_state:enums.OrderItemState,orderedition: model.OrderEdition):
        orderedition.state = new_state
    
    async def get_by_order_id(self,order_id:int):
        result = await self.db.execute(select(model.OrderEdition).where(model.OrderEdition.order_id == order_id))
        return result.scalars().all()