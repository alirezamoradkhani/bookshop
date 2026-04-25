class BaseConsumer:

    async def handle(self, event: dict, uow):
        try:
            await self.process(event, uow)
        except Exception as e:
            await self.on_error(event, e)
            raise

    async def process(self, event: dict, uow):
        raise NotImplementedError

    async def on_error(self, event: dict, error: Exception):
        print(f"consumer error: {error}")