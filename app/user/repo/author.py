from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.user.models import model

class AuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, id:int):
        new_user = model.Author(id=id)
        self.db.add(new_user)
        return new_user