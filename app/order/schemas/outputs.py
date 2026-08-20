from pydantic import BaseModel, ConfigDict
from datetime import datetime

class OrderResponse(BaseModel):
    id: int
    user_id: int
    state: str
    final_price: int
    date: datetime
    model_config = ConfigDict(from_attributes=True)

class OrderItemResponse(BaseModel):
    order_edition_id: int
    order_id: int
    edition_id: int
    state: str
    last_modify: datetime
    price: int
    model_config = ConfigDict(from_attributes=True)

class OrderDetailsResponse(OrderResponse):
    items: list[OrderItemResponse]
