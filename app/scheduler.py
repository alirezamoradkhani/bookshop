from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore
from app.database import SessionLocal
from app.crud import mark_overdue_borrows

scheduler = AsyncIOScheduler()


async def overdue_job():
    async with SessionLocal() as db:
        await mark_overdue_borrows(db)


scheduler.add_job(
    overdue_job,
    "interval",
    minutes=5
)