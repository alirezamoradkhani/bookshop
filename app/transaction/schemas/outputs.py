from datetime import datetime

from pydantic import BaseModel, ConfigDict

class BaseUserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    wallet_amount: int
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    plan: str
    plan_expire: datetime | None = None
    model_config = ConfigDict(from_attributes=True)