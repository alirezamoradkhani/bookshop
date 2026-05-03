import json
from app.workers.consumers.order.order_Cancel_consumer import OrderCancelConsumer
import asyncio
from app.workers.runners.base_runner import base_runner

async def run_order_cancel_consumer(broker, uow_factory):

    consumer = OrderCancelConsumer()
    event_type = "OrderCanceled"
    await base_runner(broker, uow_factory, consumer, event_type)


#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده