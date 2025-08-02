from fastapi import FastAPI
from mockData import Library

# python -m uvicorn books:app --reload

app = FastAPI()
booksAvailable = Library.getInventory()

@app.get("/")
async def first_call():
    return booksAvailable