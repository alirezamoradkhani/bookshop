from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from app.workers.tasks import mark_ordere_dition_as_done

scheduler = AsyncIOScheduler()

scheduler.add_job(
    mark_ordere_dition_as_done,
    "interval",
    minutes=5
)