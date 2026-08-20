import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore

from app.workers.tasks import (
    order_tasks,
    borrow_task,
    plan_task,
)

scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)


async def main():

    scheduler.add_job(
        order_tasks,
        "interval",
        minutes=2,
        misfire_grace_time=30,
    )

    scheduler.add_job(
        borrow_task,
        "interval",
        minutes=2,
        misfire_grace_time=30,
    )

    scheduler.add_job(
        plan_task,
        "interval",
        minutes=2,
        misfire_grace_time=30,
    )
    logger.info("Scheduler created")


    scheduler.start()

    logger.info("Scheduler started")

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
