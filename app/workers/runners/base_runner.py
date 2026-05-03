import json
import asyncio


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

async def rabit_base_runner(broker, uow_factory, consumer, event_type: str):

    queue = await broker.subscribe(event_type)

    async with queue.iterator() as queue_iter:

        async for message in queue_iter:

            try:
                event = json.loads(message.body)

                async with uow_factory() as uow:
                    await consumer.handle(event, uow)

            except Exception as e:
                print(f"consumer error: {e}")
                raise

async def base_runner(broker, uow_factory, consumer, event_type: str):
    await rabit_base_runner(broker, uow_factory, consumer, event_type)