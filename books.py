from fastapi import FastAPI
from mockData import Library

# python -m uvicorn books:app --reload  //development: dont use --reload on prod and aways specify the --host 

app = FastAPI()
books_available = Library.getInventory()


@app.get("/books")
async def getAllBooks():
    return books_available

@app.get("/books/{title}")
async def getBookByTitle(title: str): 
    return [book for book in books_available if (book.get("title").casefold() == title.casefold())]
        

@app.get("/books/")
async def getBooksByCategory(category: str):
    return [book for book in books_available if(book.get("category").casefold() == category.casefold())]


@app.get("/books/{book_author}/")
async def getBooksByCategoryFromAuthor(book_author:str, category:str):
    return [book for book in books_available 
            if(book.get("category").casefold() == category.casefold()
               and
               book.get("author").casefold() == book_author.casefold())
            ]