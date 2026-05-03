import json
import asyncio
from app.workers.consumers.waitlist.waitlist_create_consumer import WaitlistCreate
from app.workers.runners.base_runner import base_runner

async def run_waitlist_create_consumer(broker, uow_factory):

    consumer = WaitlistCreate()
    event_type = "WaitlistCreate"
    await base_runner(broker, uow_factory, consumer, event_type)


#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده