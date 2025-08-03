from fastapi import Body, FastAPI
from mockData import Library
from ibook  import NewBook, Book
from bson import ObjectId

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
    
@app.post("/books/create/")
async def createNewBook(new_book: NewBook = Body()):
    new_book = Book(**new_book.model_dump(), id=str(ObjectId())) # Generate unique ID (24-character hexadecimal string - ready for mongoDB)
    books_available.append(Book)
    return {"message": "Book created", "book": new_book}
    