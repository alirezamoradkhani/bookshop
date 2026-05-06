import aio_pika
from app.core.setting import settings


async def get_rabbitmq_connection():
    return await aio_pika.connect_robust(settings.rabbitmq_url)