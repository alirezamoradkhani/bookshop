# worker/outbox_worker.py

import asyncio
from app.outbox.publisher import publish_outbox_events

async def run_outbox_worker(uow_factory, broker):

    while True:
        try:
            async with uow_factory() as uow:
                processed_count = await publish_outbox_events(uow, broker)

                # adaptive sleep
                if processed_count == 0:
                    await asyncio.sleep(3)
                else:
                    await asyncio.sleep(0.5)

        except Exception as e:
            print(f"outbox worker error: {e}")
            await asyncio.sleep(2)

#هر 3 ثانیه تابع پابلیش کردن ایونت هارو کال میکنه 
#پابلیش کردن:روی چنل با نام ایونت تایپ مسیچ که اطلاعات ایونت هس رو ارسال میکنه