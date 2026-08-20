from pydantic import BaseModel, ConfigDict
from datetime import datetime

class WaitlistResponse(BaseModel):
    id: int
    user_id: int
    edition_id: int
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)

class BorrowResponse(BaseModel):
    id: int
    user_id: int
    edition_id: int
    status: str
    borrowed_at: datetime
    due_at: datetime
    returned_at: datetime | None = None
    is_overdue: bool
    model_config = ConfigDict(from_attributes=True)
