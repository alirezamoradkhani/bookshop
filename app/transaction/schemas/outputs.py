from pydantic import BaseModel

class BaseUserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    wallet_amount: int
    class Config:
        from_attributes = True