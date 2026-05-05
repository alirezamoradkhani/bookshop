from app.workers.consumers.edition.edition_update_consumer import EditionUpdateConsumer
from app.workers.runners.base_runner import base_runner

async def run_edition_update_consumer(broker, uow_factory):

    consumer = EditionUpdateConsumer()
    event_type = "EditionUpdated"
    await base_runner(broker, uow_factory, consumer, event_type)


#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده