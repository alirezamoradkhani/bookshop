from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from datetime import datetime
from app.database import Base

class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id = Column(Integer, primary_key=True)

    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)

    processed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)