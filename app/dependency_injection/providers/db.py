from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

from app.core.setting import settings


engine = create_async_engine(settings.database_url, echo=False)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_session():
    async with SessionLocal() as session:
        yield session

def create_session():
    return SessionLocal()