from pydantic import BaseModel

class BookResponse(BaseModel):
    id : int
    title: str
    category: str
    class Config:
        orm_mode = True