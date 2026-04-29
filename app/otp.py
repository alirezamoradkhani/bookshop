import redis.asyncio as redis
import random
from fastapi import Depends
from app.redis import get_redis

async def send_otp(otp):
    print("otp: ", otp)

async def create_otp(email: str,redis_client=Depends(get_redis)):
    otp = str(random.randint(100000, 999999))

    await redis_client.set(f"otp:{email}", otp, ex=120)

    await send_otp(otp=otp)

    return otp

async def verify_otp(email: str, otp: str,redis_client=Depends(get_redis)):
    saved_otp = await redis_client.get(f"otp:{email}")
    if saved_otp is None:
        return False
    if saved_otp == otp:
        await redis_client.delete(f"otp:{email}")
        return True
    return False

#its turned to async