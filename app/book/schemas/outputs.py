from pydantic import BaseModel

class BookResponse(BaseModel):
    id : int
    title: str
    class Config:
        from_attributes = True

class BookDetails(BaseModel):
    id: int
    title: str
    categorys: list[str]
    authors : list[str]
    class Config:
        from_attributes = True