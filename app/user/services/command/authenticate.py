from app.security import verify_password, create_access_token
import app.user.schemas.inputs as inputs
from app.exceptions.models.user import InvalidCredentials

from app.unit_of_work import UnitOfWork


async def login_by_user_pass(uow:UnitOfWork,user: inputs.UserLogin):
    async with uow:
        user_in = await uow.baseusers.get_by_username(user.username)
        if user_in is None or not verify_password(user.password, user_in.password):
            raise InvalidCredentials
        user_in = await uow.baseusers.get_by_username(name=user.username)
        token_data = {
        "user_id": user_in.id,
    }
        access_token = create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}
    
# async def login_by_otp(uow:UnitOfWork,otp: str,email:str):
#     if not await verify_otp(email=email,otp=otp):
#             raise InvalidOTP
#     async with uow:
#         user_in = await uow.baseusers.get_by_email(email)
#         token_data = {
#         "user_id": user_in.id,
#     }
#     access_token = create_access_token(token_data)
#     return {"access_token": access_token, "token_type": "bearer"}