# app/workers/dispatcher.py

import json
import logging
from app.workers.registry import CONSUMER_REGISTRY


MAX_RETRY = 3
logger = logging.getLogger(__name__)


async def dispatch_message(message, broker, uow_factory):
    retry = int((message.headers or {}).get("retry", 0))

    try:
        event = json.loads(message.body)

        event_type = event.get("event_type")
        logger.info("Dispatching event %s", event_type)

        consumer_cls = CONSUMER_REGISTRY.get(event_type)

        if not consumer_cls:
            await message.reject(requeue=False)
            return

        consumer = consumer_cls()
        async with uow_factory() as uow:
            await consumer.process(event, uow)

        await message.ack()
        

    except Exception:

        retry += 1
        logger.exception("Consumer failed; retry=%s", retry)

        try:
            if retry < MAX_RETRY:
                await broker.retry(message, retry)
            else:
                await broker.send_to_dlq(message)

            await message.ack()

        except Exception:
            logger.exception("Broker retry handling failed")
            await message.nack(requeue=True)
