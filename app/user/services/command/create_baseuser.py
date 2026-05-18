import app.user.models.model as model
from app.core.otp import create_otp, verify_otp
from app.core.security import hash_password
import app.user.schemas.inputs as inputs
import app.user.models.enums as enums
from app.exceptions.models.user import EmailAlreadyRegistered,UsernameAlreadyExists,InvalidOTP

from app.core.unit_of_work import UnitOfWork


async def email_register(uow:UnitOfWork,email: str):
    async with uow:
        if await uow.baseusers.get_by_email(email):
                raise EmailAlreadyRegistered
    await create_otp(email)
    return f"otp sent to {email}"


async def create_user(uow:UnitOfWork,user: inputs.UserCreate,otp: str):
    async with uow:
        if await uow.baseusers.get_by_username(user.username) is not None:
            raise UsernameAlreadyExists
        if not await verify_otp(otp=otp,email=user.email):
                raise InvalidOTP
        if user.role == enums.Role.USER:
            new_user = model.User(
                    username=user.username,
                    email=user.email,
                    password=hash_password(password=user.password),
                    role=user.role
                )
            
        elif user.role == enums.Role.AUTHOR:
             new_user = model.Author(
                    username=user.username,
                    email=user.email,
                    password=hash_password(password=user.password),
                    role=user.role
                )
        await uow.baseusers.create(new_user)
        return new_user

