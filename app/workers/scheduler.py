from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from app.workers.tasks import order_tasks,borrow_task

scheduler = AsyncIOScheduler()

scheduler.add_job(
    order_tasks,
    "interval",
    minutes=5,
)
scheduler.add_job(
    borrow_task,
    "interval",
    minutes=5,
)