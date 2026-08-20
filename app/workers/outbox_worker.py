# app/workers/outbox_worker.py

import asyncio
import logging

from app.outbox.publisher import publish_outbox_events
from app.dependency_injection.container import Container


container = Container()
logger = logging.getLogger(__name__)

async def main():
    await container.init_resources()

    rabbit = await container.rabbitmq()
    uow_factory = container.uow

    while True:

        try:
            async with uow_factory() as uow:
                await publish_outbox_events(uow, rabbit)
                

        except Exception:
            logger.exception("Outbox worker iteration failed")

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
