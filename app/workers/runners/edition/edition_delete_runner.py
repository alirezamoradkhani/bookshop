import json
from app.workers.consumers.edition.edition_delete_consumer import EditionDeleteConsumer
import asyncio
from app.workers.runners.base_runner import base_runner

async def run_edition_delete_consumer(broker, uow_factory):

    consumer = EditionDeleteConsumer()
    event_type = "EditionDeleted"
    await base_runner(broker, uow_factory, consumer, event_type)


#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده