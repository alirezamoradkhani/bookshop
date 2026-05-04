import json
import asyncio
from app.broker.rabit_broker import RabbitMQBroker

async def redis_base_runner(broker,uow_factory,consumer,event_type:str):

    while True:
            try:
                pubsub = await broker.subscribe(event_type)

                async for message in pubsub.listen():

                    if message["type"] != "message":
                        continue

                    event = json.loads(message["data"])

                    try:
                        async with uow_factory() as uow:
                            await consumer.handle(event, uow)
                    except Exception as e:
                        print(f"consumer error: {e}")

            except Exception as e:
                print(f"consumer worker restart: {e}")
                await asyncio.sleep(2)

async def rabit_base_runner(
    broker,
    uow_factory,
    consumer,
    event_type: str,
):
    queue = await broker.subscribe(event_type)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            retry_count = int((message.headers or {}).get("retry", 0))

            try:
                event = json.loads(message.body)

                async with uow_factory() as uow:
                    await consumer.handle(event, uow)

                await message.ack()

            except Exception as e:
                retry_count += 1
                print(f"consumer error: {e}, retry={retry_count}")

                try:
                    if retry_count < 3:
                        await broker.retry(message, retry_count)
                    else:
                        await broker.send_to_dlq(message)

                    await message.ack()

                except Exception as broker_error:
                    print(f"broker retry/dlq failed: {broker_error}")
                    await message.nack(requeue=True)

async def base_runner(broker, uow_factory, consumer, event_type: str):
    await rabit_base_runner(broker, uow_factory, consumer, event_type)