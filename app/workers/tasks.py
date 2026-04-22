from app.order.serivices.checks.mark_orderedition_as_done import mark_orderedition_as_done
from app.unit_of_work import UnitOfWork

async def mark_ordere_dition_as_done():
    async with UnitOfWork() as uow:
        await mark_orderedition_as_done(uow)