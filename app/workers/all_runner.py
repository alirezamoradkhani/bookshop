# app/workers/all_runner.py

import asyncio
import app.workers.consumers
from app.workers.runners.runner import run_consumer
from app.workers.consumers.base import BaseConsumer


async def all_runner(
    broker,
    uow_factory,
):
    print("Starting all consumers...", flush=True)
    tasks = [

        run_consumer(
            broker=broker,
            uow_factory=uow_factory,
            consumer_cls=consumer_cls,
        )

        for consumer_cls in BaseConsumer.registry
    ]
    print(f"Registered consumers: {len(tasks)}", flush=True)
    await asyncio.gather(*tasks)