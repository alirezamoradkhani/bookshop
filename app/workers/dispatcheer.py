# app/workers/dispatcher.py

import json
from app.workers.registry import CONSUMER_REGISTRY


MAX_RETRY = 3


async def dispatch_message(message, broker, uow_factory):
    print("[dispatcher] started", flush=True)

    retry = int((message.headers or {}).get("retry", 0))
    print(f"[dispatcher] retry={retry}", flush=True)

    try:
        event = json.loads(message.body)

        event_type = event.get("event_type")
        print(f"[dispatcher] event={event_type}", flush=True)

        consumer_cls = CONSUMER_REGISTRY.get(event_type)

        if not consumer_cls:
            await message.reject(requeue=False)
            return

        consumer = consumer_cls()
        print("[dispatcher] before uow", flush=True)

        async with uow_factory() as uow:
            await consumer.handle(event, uow)

        print("[dispatcher] after uow", flush=True)
        await message.ack()
        

    except Exception as e:

        retry += 1
        print(f"[consumer] error={e}, retry={retry}", flush=True)

        try:
            if retry < MAX_RETRY:
                await broker.retry(message, retry)
            else:
                await broker.send_to_dlq(message)

            await message.ack()

        except Exception as broker_error:
            print(f"[broker] error={broker_error}", flush=True)
            await message.nack(requeue=True)