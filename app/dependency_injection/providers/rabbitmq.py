import aio_pika
from app.core.setting import settings
from app.broker.rabit_broker import RabbitMQBroker


async def get_rabbitmq_connection():
    broker = RabbitMQBroker(settings.rabbitmq_url)
    return broker