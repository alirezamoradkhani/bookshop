from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.setting import settings
POSTGRES_DATABASE_URL = settings.database_url
engine = create_async_engine(POSTGRES_DATABASE_URL)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

async def get_db():
    async with SessionLocal() as session:
        yield session


Base = declarative_base()