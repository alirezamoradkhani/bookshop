import redis
import random

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

def send_otp(otp):
    print("otp: ", otp)

def create_otp(email: str):
    otp = str(random.randint(100000, 999999))

    redis_client.set(f"otp:{email}", otp, ex=120)

    send_otp(otp=otp)

    return otp

def verify_otp(email: str, otp: str):
    saved_otp = redis_client.get(f"otp:{email}")
    if saved_otp is None:
        return False
    if saved_otp == otp:
        redis_client.delete(f"otp:{email}")
        return True
    return False