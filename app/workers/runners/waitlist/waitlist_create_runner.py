from app.workers.consumers.waitlist.waitlist_create_consumer import WaitlistCreateConsumer
from app.workers.runners.base_runner import base_runner

async def run_waitlist_create_consumer(broker, uow_factory):

    consumer = WaitlistCreateConsumer()
    event_type = "WaitlistCreate"
    await base_runner(broker, uow_factory, consumer, event_type)


#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده