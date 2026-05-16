from app.order.serivices.checks.mark_orderedition_as_done import mark_orderedition_as_done
from app.order.serivices.checks.mark_orderedition_as_rejected import mark_orderedition_as_rejected
from app.order.serivices.checks.mark_orderedition_as_forcereject import mark_orderedition_as_forcereject
from app.order.serivices.checks.mark_order_as_inprogres import mark_ordere_as_inprogres
from app.order.serivices.checks.mark_order_as_done import mark_ordere_as_done
from app.user.services.checks.dowgrade_expired_plan import downgrade_expired_plan

from app.borrow.services.checks.mark_borrow_as_overdue import mark_borrow_as_overdue
from app.dependency_injection.container import Container
from asyncio import gather

container = Container()

async def order_tasks():
    await container.init_resources()
    uow_factory = container.uow

    await gather(
        mark_orderedition_as_done(uow_factory),
        mark_orderedition_as_rejected(uow_factory),
        mark_orderedition_as_forcereject(uow_factory),
        mark_ordere_as_done(uow_factory),
        mark_ordere_as_inprogres(uow_factory),
    )

async def borrow_task():
    await container.init_resources()
    uow = container.uow
    await mark_borrow_as_overdue(uow)


async def plan_task():
    await container.init_resources()
    uow = container.uow
    await downgrade_expired_plan(uow)