from pydantic import BaseModel
from typing import Optional

# Missing/extra/invalid field	Auto 422 response from FastAPI

class NewBook(BaseModel):
    title: str
    author: str
    category: str
    description: str
    
# Book model including generated id
class Book(NewBook):
    id: str
    
class PartialBookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    