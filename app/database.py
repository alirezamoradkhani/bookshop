from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.setting import settings
POSTGRES_DATABASE_URL = settings.database_url
engine = create_async_engine(POSTGRES_DATABASE_URL)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit= False
)


Base = declarative_base()