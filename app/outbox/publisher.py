from app.unit_of_work import UnitOfWork
from app.broker.redis_broker import RedisBroker
# from app.broker.rabit_broker import RabbitMQBroker

async def publish_outbox_events(uow:UnitOfWork, broker:RedisBroker):

    processed_count = 0

    async with uow:

        events = await uow.outbox.get_unprocessed(limit=50)

        for event in events:
            try:
                await broker.publish(
                    topic=event.event_type,
                    message=event.payload
                )

                event.processed = True
                processed_count += 1

            except Exception as e:
                print(f"publish failed {event.id}: {e}")
                continue

        # await uow.commit()

    return processed_count