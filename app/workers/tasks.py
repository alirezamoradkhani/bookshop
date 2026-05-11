from app.order.serivices.checks.mark_orderedition_as_done import mark_orderedition_as_done
from app.order.serivices.checks.mark_orderedition_as_rejected import mark_orderedition_as_rejected
from app.order.serivices.checks.mark_orderedition_as_forcereject import mark_orderedition_as_forcereject
from app.order.serivices.checks.mark_order_as_inprogres import mark_ordere_as_inprogres
from app.order.serivices.checks.mark_order_as_done import mark_ordere_as_done
from app.user.services.checks.dowgrade_expired_plan import downgrade_expired_plan

from app.borrow.services.checks.mark_borrow_as_overdue import mark_borrow_as_overdue
from app.dependency_injection.container import Container

container = Container()

async def order_tasks():
    await container.init_resources()
    uow_factory = container.uow
    async with uow_factory() as uow:
        await mark_orderedition_as_done(uow)
        await mark_orderedition_as_rejected(uow)
        await mark_orderedition_as_forcereject(uow)
        await mark_ordere_as_done(uow)
        await mark_ordere_as_inprogres(uow)
    

async def borrow_task():
    await container.init_resources()
    uow_factory = container.uow
    async with uow_factory() as uow:
        await mark_borrow_as_overdue(uow)


async def plan_task():
    await container.init_resources()
    uow_factory = container.uow
    async with uow_factory() as uow:
        await downgrade_expired_plan(uow)