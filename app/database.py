from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.setting import settings
POSTGRES_DATABASE_URL = settings.database_url
engine = create_engine(POSTGRES_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()