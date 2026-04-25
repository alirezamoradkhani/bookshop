from pydantic import BaseModel

class BaseUserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    wallet_amount: int
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id:int
    plan: str
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True