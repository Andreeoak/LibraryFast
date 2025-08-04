from pydantic import BaseModel, Field
from typing import Optional

# Missing/extra/invalid field	Auto 422 response from FastAPI

class NewBook(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    category: str = Field(min_length=3)
    description: str = Field(min_lenght=5, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    
# Book model including generated id
class Book(NewBook):
    id: str
    
class PartialBookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[int] = None
    