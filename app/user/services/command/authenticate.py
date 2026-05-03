from app.otp import create_otp, verify_otp
from app.security import verify_password, create_access_token
import app.user.schemas.inputs as inputs
from app.exceptions.models.user import InvalidCredentials,InvalidOTP

from app.unit_of_work import UnitOfWork


async def athenticate(uow:UnitOfWork,user: inputs.UserLogin):
    async with uow:
        user_in = await uow.baseusers.get_by_username(user.username)
        if user_in is None or not verify_password(user.password, user_in.password):
            raise InvalidCredentials
        await create_otp(user_in.email)
        return "OTP sent to email"
    
async def verify_email(uow:UnitOfWork,otp: str,email:str):
    if not await verify_otp(email=email,otp=otp):
            raise InvalidOTP
    async with uow:
        user_in = await uow.baseusers.get_by_email(email)
        token_data = {
        "user_id": user_in.id,
    }
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}