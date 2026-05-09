from app.dependency_injection.container import Container

container = Container()

async def get_uow():
    yield container.uow()

async def get_openlibrary():
    yield container.openlibrary()