from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.order.models import model
from app.order.models import enums
from datetime import datetime

class OrderEditionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self,orderedition: model.OrderEdition):
        self.db.add(orderedition)

    async def update_state(self,new_state:enums.OrderItemState,orderedition: model.OrderEdition):
        orderedition.state = new_state
        orderedition.last_modify = datetime.utcnow()
    
    async def get_by_order_id(self,order_id:int):
        result = await self.db.execute(select(model.OrderEdition).where(model.OrderEdition.order_id == order_id))
        return result.scalars().all()
    async def get_by_order_edition_id(self,order_edition_id:int):
        result = await self.db.execute(select(model.OrderEdition).where(model.OrderEdition.order_edition_id == order_edition_id))
        return result.scalar_one_or_none()