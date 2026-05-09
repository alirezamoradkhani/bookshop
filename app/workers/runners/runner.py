from app.workers.runners.base_runner import rabit_base_runner


async def run_consumer(
    broker,
    uow_factory,
    consumer_cls,
):
    print(f"Subscribing to {consumer_cls.event_type} events...")
    consumer = consumer_cls()

    await rabit_base_runner(
        broker=broker,
        uow_factory=uow_factory,
        consumer=consumer,
        event_type=consumer_cls.event_type,
    )