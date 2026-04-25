from pydantic import BaseModel
from datetime import datetime

class OrderResponse(BaseModel):
    id: int
    user_id: int
    state: str
    final_price: int
    date: datetime
    class Config:
        from_attributes = True