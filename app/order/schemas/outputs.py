from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    user_id: int
    state: str
    final_price: int
    date: str
    class Config:
        orm_mode = True