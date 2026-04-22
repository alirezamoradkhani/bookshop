from app.edition.models.model import Edition
from app.edition.models.enums import Language
from app.unit_of_work import UnitOfWork

async def seed_book(uow:UnitOfWork):
    edition1 = Edition()