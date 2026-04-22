from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from app.workers.tasks import order_tasks

scheduler = AsyncIOScheduler()

scheduler.add_job(
    order_tasks,
    "interval",
    minutes=5
)