from fastapi import Body, FastAPI, Query, HTTPException
from Database.mockData import Library
from Interfaces.ibook  import NewBook, Book, PartialBookUpdate
from Utils.validationRules import validateObjectId
from bson import ObjectId
from typing import Optional
from bson import ObjectId

# python -m uvicorn books:app --reload  //development: dont use --reload on prod and aways specify the --host 

app = FastAPI()
books_available = Library.getInventory()


@app.get("/books")
async def getBooksByFilter(
    title: Optional[str] = None,
    category: Optional[str] = None,
    author: Optional[str] = None,
    min_rating: Optional[int] = None,
    max_rating: Optional[int] = None
):
    # Start with all books
    results = books_available

    # Apply filters dynamically
    if title:
        results = [book for book in results if book.get("title").casefold() == title.casefold()]
    if category:
        results = [book for book in results if book.get("category").casefold() == category.casefold()]
    if author:
        results = [book for book in results if book.get("author").casefold() == author.casefold()]
    if min_rating is not None:
        results = [book for book in results if book.get("ratings") >= min_rating]
    if max_rating is not None:
        results = [book for book in results if book.get("ratings") <= max_rating]

    return results
        
    
@app.post("/books/create/")
async def createNewBook(new_book: NewBook = Body()):
    new_book = Book(**new_book.model_dump(), id=str(ObjectId())) # Generate unique ID (24-character hexadecimal string - ready for mongoDB)
    books_available.append(new_book)
    return {"message": "Book created", "book": new_book}
    
    
@app.put("/books/{book_id}/update/")
async def updateBookById( book_id:str, update_data: PartialBookUpdate = Body(...)):
    book_id = validateObjectId(book_id)
    for i, book in enumerate(books_available):
        if book.get("_id") == book_id:
            # Merge fields: only update what's provided
            updated_book = book.copy()
            update_fields = update_data.model_dump(exclude_unset=True)
            updated_book.update(update_fields)
            books_available[i] = updated_book
            return {"message": "Book updated", "book": updated_book}
    raise HTTPException(status_code=404, detail=f"No book found with ID {id}")


@app.delete("/books/{book_id}/delete/")
async def deleteBookByID(book_id:str):
    book_id = validateObjectId(book_id)
    for i, book in enumerate(books_available):
        if book.get("_id") == book_id:
            books_available.pop(i)
            return {"message": f"Book with ID {book_id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"No book found with ID {book_id}")