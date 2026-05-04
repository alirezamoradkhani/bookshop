from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
import redis.asyncio as redis
from app.exceptions.models.user import InvalidTokenUser
import random
from passlib.context import CryptContext
from app.core.setting import settings

bearer_scheme = HTTPBearer()

SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True
)

# async def send_otp(email: str):
#     otp = str(random.randint(100000, 999999))

#     await redis_client.set(f"otp:{email}", otp, ex=120)

#     print("OTP:", otp)

#     return otp

# async def verify_otp(email: str, otp: str):
#     saved_otp = await redis_client.get(f"otp:{email}")
#     if saved_otp is None:
#         return False
#     if saved_otp == otp:
#         await redis_client.delete(f"otp:{email}")
#         return True
#     return False

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise InvalidTokenUser
    return payload

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#its turned async