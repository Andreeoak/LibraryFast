from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

# Missing/extra/invalid field	Auto 422 response from FastAPI

class NewBook(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    category: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=100)
    ratings: int = Field(gt=-1, lt=6)
    
    model_config ={
        "json_schema_extra":{
            "example": {
                "title": "Ulysses",
                "author": "James Joyce",
                "category": "Romance",
                "description": "A day in the life of Leopold Bloom.",
                "ratings": 5
            }
        }
    }
    
# Book model including generated id
class Book(NewBook):
    id: str
    @field_validator("id")
    @classmethod
    def validateObjectId(cls, id: str) ->str:
        if not ObjectId.is_valid(id):
            raise ValueError("Invalid ObjectId format")
        return id
    
class PartialBookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    ratings: Optional[int] = None
    