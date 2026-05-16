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
    authors_id : list[int]
    class Config:
        from_attributes = True