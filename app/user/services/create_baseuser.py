import app.user.models.model as model
from app.otp import create_otp, verify_otp
from app.security import hash_password
import app.user.schemas.inputs as inputs
import app.user.models.enums as enums
from app.exceptions.models.user import EmailAlreadyRegistered,UsernameAlreadyExists,InvalidOTP

from app.unit_of_work import UnitOfWork


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
        new_user = model.BaseUser(
                username=user.username,
                email=user.email,
                password=hash_password(password=user.password),
                role=user.role
            )
        await uow.baseusers.create(new_user)
        await uow.flush()
        if new_user.role == enums.Role.USER:
            await uow.user.create(new_user.id)
        elif new_user.role == enums.Role.AUTHOR:
            await uow.author.create(new_user.id)
        return new_user

