import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore

from app.workers.tasks import (
    order_tasks,
    borrow_task,
    plan_task,
)

scheduler = AsyncIOScheduler()


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
    print("Schaduler created.",flush=True)


    scheduler.start()

    print("Scheduler started...",flush=True)

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())