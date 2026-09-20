from app.mongo.base import MongoRepository
from app.edition.models.model import Edition
from app.order.models.enums import OrderItemState
from app.order.models.model import OrderEdition
from datetime import datetime, timedelta
from app.mongo.serialization import serialize

class OrderEditionRepository(MongoRepository):
    collection, model = "order_editions", OrderEdition
    enum_fields = {"state": OrderItemState}

    async def create(self, orderedition: OrderEdition):
        return await self._insert(orderedition)

    async def create_many(self, order_editions: list[OrderEdition]):
        for item in order_editions:
            await self._insert(item)

    async def update_state(self, new_state: OrderItemState, orderedition: OrderEdition):
        orderedition.state = new_state
        orderedition.last_modify = datetime.utcnow()

    async def many_update_state(self, order_edition_ids: list[int], new_state: OrderItemState):
        await self.db.collection(self.collection).update_many(
            {"_id": {"$in": order_edition_ids}},
            {"$set": {"state": serialize(new_state), "last_modify": datetime.utcnow()}},
            **self.db.options(),
        )

    async def get_by_order_id(self, order_id: int):
        return await self._find({"order_id": order_id})

    async def get_by_order_edition_id(self, order_edition_id: int):
        return await self._find_one({"_id": order_edition_id})

    async def get_by_state(self, state: OrderItemState):
        return await self._find({"state": serialize(state)})

    async def get_by_last_modify(self, date: datetime):
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        return await self._find({"last_modify": {"$gte": start, "$lt": start + timedelta(days=1)}})

    async def get_by_last_modify_and_state(self, date: datetime, state: OrderItemState):
        return await self._find({"last_modify": {"$lt": date}, "state": serialize(state)})

    async def get_orderedition_by_list_of_edition(self, editions: list[Edition]):
        return await self._find({"edition_id": {"$in": [edition.id for edition in editions]}})

    async def get_by_order_ids(self, order_ids: list[int]):
        return await self._find({"order_id": {"$in": order_ids}})
