from pydantic import BaseModel

class BookResponse(BaseModel):
    id : int
    title: str
    category: str
    class Config:
        from_attributes = True

class BookDetails(BaseModel):
    id: int
    title: str
    category: str
    authors : list[str]
    class Config:
        from_attributes = True