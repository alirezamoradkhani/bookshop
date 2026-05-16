from app.workers.consumers.order.order_item_reject_consumer import OrderItemRejectConsumer
from app.workers.runners.base_runner import base_runner

async def run_order_item_reject_consumer(broker, uow_factory):

    consumer = OrderItemRejectConsumer()
    event_type = "OrderItemRejected"
    await base_runner(broker, uow_factory, consumer, event_type)


#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده