from app.user.models.model import BaseUser
from app.user.models.enums import Role
from app.unit_of_work import UnitOfWork

async def seed_user(uow:UnitOfWork):
    user1 = BaseUser(username = "a", email = "a@e.com",passworld="1",role = Role.USER)
    user2 = BaseUser(username = "b", email = "b@e.com",passworld="1",role = Role.AUTHOR)
    user3 = BaseUser(username = "c", email = "c@e.com",passworld="1",role = Role.AUTHOR)
    await uow.baseusers.create(user1)
    await uow.baseusers.create(user2)
    await uow.baseusers.create(user3)
    print(" Users seeded")