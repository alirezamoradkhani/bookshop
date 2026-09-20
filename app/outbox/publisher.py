from app.core.unit_of_work import UnitOfWork
import logging
from app.broker.redis_broker import RedisBroker
from app.broker.rabit_broker import RabbitMQBroker

logger = logging.getLogger(__name__)

async def publish_outbox_events(uow:UnitOfWork, broker:RedisBroker | RabbitMQBroker):

    processed_count = 0

    events = await uow.outbox.get_unprocessed(limit=50)

    for event in events:
        try:
            await broker.publish(
                topic=event.event_type,
                message=event.payload
            )

            await uow.outbox.mark_processed(event)
            processed_count += 1

        except Exception:
            logger.exception("Failed to publish outbox event %s", event.id)
            continue

    return processed_count
