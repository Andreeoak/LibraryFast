from bson import ObjectId
from fastapi import HTTPException

async def validateObjectId(id_str: str) -> str:
    if not ObjectId.is_valid(id_str):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    return id_str

def transformMongoDocument(doc): #solves serialization problem
    doc["_id"] = str(doc["_id"])
    return doc