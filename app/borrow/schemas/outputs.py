from pydantic import BaseModel
from datetime import datetime

class WaitlistResponse(BaseModel):
    id: int
    user_id: int
    edition_id: int
    created_at : datetime
    class config:
        from_attributes = True