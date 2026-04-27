import json
from app.workers.consumers.edition.edition_delete_consumer import EditionDeleteConsumer
import asyncio

async def run_edition_delete_consumer(broker, uow_factory):

    consumer = EditionDeleteConsumer()

    while True:
        try:
            pubsub = await broker.subscribe("EditionDeleted")

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

#ایونت های پابلیش شده با تایپ مشخص رو میگیره و کارهای مورد نیاز اونو انجام میده