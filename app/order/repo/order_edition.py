from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.order.models import model
from app.order.models import enums
from datetime import datetime, timedelta

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
    
    async def get_by_state(self,state:enums.OrderItemState):
        result = await self.db.execute(select(model.OrderEdition).where(model.OrderEdition.state == state))

        return result.scalars().all()
    
    async def get_by_last_modify(self, date: datetime):
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        result = await self.db.execute(
            select(model.OrderEdition).where(
                model.OrderEdition.last_modify >= start,
                model.OrderEdition.last_modify < end
            )
        )
        return result.scalars().all()
    
    async def get_by_last_modify_and_state(self,date:datetime,state:enums.OrderItemState):
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        result = await self.db.execute(select(
            model.OrderEdition)
            .where(model.OrderEdition.last_modify >= start
                   ,model.OrderEdition.last_modify < end
                   ,model.OrderEdition.state == state))
        return result.scalars().all()