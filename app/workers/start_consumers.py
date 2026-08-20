import asyncio
import logging

from app.dependency_injection.container import Container
from app.workers.dispatcheer import dispatch_message
from app.workers.registry import CONSUMER_REGISTRY


logger = logging.getLogger(__name__)
container = Container()


async def start_consumers():
    await container.init_resources()
    rabbit = await container.rabbitmq()
    uow_factory = container.uow

    async def handler(message):
        try:
            await dispatch_message(message, rabbit, uow_factory)
        except Exception:
            logger.exception("Consumer handler crashed")

    for event_type in CONSUMER_REGISTRY:
        queue = await rabbit.subscribe(event_type)
        await queue.consume(handler)
        logger.info("Consumer started for %s", event_type)

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_consumers())
