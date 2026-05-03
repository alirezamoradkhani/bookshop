import json
from app.workers.consumers.edition.edition_create_consumer import EditionCreateConsumer
import asyncio
from app.workers.runners.base_runner import base_runner

async def run_edition_create_consumer(broker, uow_factory):

    consumer = EditionCreateConsumer()
    event_type = "EditionCreated"
    await base_runner(broker, uow_factory, consumer, event_type)


#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده