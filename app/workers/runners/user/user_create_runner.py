from app.workers.consumers.user.user_create_consumer import UserCreateConsumer
from app.workers.runners.base_runner import base_runner

async def run_user_create_consumer(broker, uow_factory):

    consumer = UserCreateConsumer()
    event_type = "UserCreated"
    await base_runner(broker, uow_factory, consumer, event_type)

#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده