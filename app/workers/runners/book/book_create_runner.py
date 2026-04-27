from app.workers.consumers.book.book_create_consumer import BookCreateConsumer
import json
import asyncio

async def run_book_create_consumer(broker,uow_factory):

    consumer = BookCreateConsumer()
    while True:
        try:
            pubsub = await broker.subscribe("BookCreated")

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
