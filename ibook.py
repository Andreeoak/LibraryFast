from pydantic import BaseModel

# Missing/extra/invalid field	Auto 422 response from FastAPI

class NewBook(BaseModel):
    title: str
    author: str
    category: str
    description: str
    
# Book model including generated id
class Book(NewBook):
    id: str
    