from fastapi import FastAPI
from mockData import Library

# python -m uvicorn books:app --reload

app = FastAPI()
booksAvailable = Library.getInventory()

@app.get("/books")
async def getAllBooks():
    return booksAvailable

@app.get("/books/{title}")
async def getBookByTitle(title):
    return [book for book in booksAvailable if (book.get("title").casefold() == title.casefold())]
        
         