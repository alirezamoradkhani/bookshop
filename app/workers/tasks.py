from app.order.serivices.checks.mark_orderedition_as_done import mark_orderedition_as_done
from app.order.serivices.checks.mark_orderedition_as_rejected import mark_orderedition_as_rejected
from app.order.serivices.checks.mark_orderedition_as_forcereject import mark_orderedition_as_forcereject
from app.order.serivices.checks.mark_order_as_inprogres import mark_ordere_as_inprogres
from app.order.serivices.checks.mark_order_as_done import mark_ordere_as_inprogres

from app.borrow.services.checks.mark_borrow_as_overdue import mark_borrow_as_overdue
from app.unit_of_work import UnitOfWork

async def order_tasks():
    async with UnitOfWork() as uow:
        await mark_orderedition_as_done(uow)
        await mark_orderedition_as_rejected(uow)
        await mark_orderedition_as_forcereject(uow)
        await mark_ordere_as_inprogres(uow)
        await mark_ordere_as_inprogres(uow)

async def borrow_task():
    async with UnitOfWork as uow:
        mark_borrow_as_overdue(uow)