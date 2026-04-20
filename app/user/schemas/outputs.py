from pydantic import BaseModel

class BaseUserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    wallet_amount: int

class UserResponse(BaseModel):
    id:int
    plan: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str