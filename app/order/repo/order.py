from app.mongo.base import MongoRepository
from app.order.models.enums import OrderState
from app.order.models.model import Order
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class OrderRepository(MongoRepository):
    collection, model = "orders", Order
    enum_fields = {"state": OrderState}

    async def create_order(self, order: Order):
        return await self._insert(order)

    async def get_by_id(self, order_id: int):
        return await self._find_one({"_id": order_id})

    async def update_order_state(self, order: Order, new_state: OrderState):
        return await self._set_fields(order, state=new_state)

    async def update_final_price(self, order: Order, change: int):
        return await self._increment_fields(order, final_price=-change)

    async def many_update_state(self, order_ids: list[int], new_state):
        await self._collection().update_many(
            {"_id": {"$in": order_ids}}, {"$set": {"state": serialize(new_state)}}, **self._options()
        )

    async def get_by_state(self, state: OrderState):
        return await self._find({"state": serialize(state)})

    async def get_by_user_id(self, id: int):
        return await self._find({"user_id": id})
