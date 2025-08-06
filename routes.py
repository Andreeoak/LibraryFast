from fastapi import Body, FastAPI, HTTPException, Depends
#from Database.mockData import Library
from Interfaces.ibook  import NewBook, PartialBookUpdate
from Utils.validationRules import validateObjectId, transformMongoDocument
from bson import ObjectId
from Database.ConnectDB import getCollection
from typing import Optional
from starlette import status

# python -m uvicorn routes:app --reload  //development: dont use --reload on prod and aways specify the --host 

app = FastAPI()
# Get the books collection
collection = getCollection()

''' No Need for Local Storage
books_available = Library.getInventory()
books_by_id_dict = {book.get("_id"): book for book in books_available}
'''

@app.get("/books", status_code=status.HTTP_200_OK)
async def getBooksByFilter(
    title: Optional[str] = None,
    category: Optional[str] = None,
    author: Optional[str] = None,
    min_rating: Optional[int] = None,
    max_rating: Optional[int] = None
):
    # Start with all books
    query = {}

    # Apply filters dynamically
    if title:
        query["title"] = {"$regex": title, "$options": "i"}  # Case-insensitive
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if author:
        query["author"] = {"$regex": author, "$options": "i"}
        
    ratings_filter = {}
    if min_rating is not None:
        ratings_filter["$gte"] = min_rating
    if max_rating is not None:
        ratings_filter["$lte"] = max_rating
    if ratings_filter:
        query["ratings"] = ratings_filter

    # Execute the query
    books = list(collection.find(query))
    return [transformMongoDocument(book) for book in books]
 
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)    
async def getBookById(book_id:str = Depends(validateObjectId)):
    book = collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail=f"No book found with ID {book_id}")
    return transformMongoDocument(book)
    
@app.post("/books/create/", status_code=status.HTTP_201_CREATED)
async def createNewBook(new_book: NewBook = Body(...)):
    book_dict = new_book.model_dump()  
    result = collection.insert_one(book_dict)
    book_dict["_id"] = str(result.inserted_id)
    return {"message": "Book created", "book": transformMongoDocument(book_dict)}
    
    
@app.put("/books/{book_id}/update/", status_code=status.HTTP_204_NO_CONTENT)
async def updateBookById( book_id:str = Depends(validateObjectId), update_data: PartialBookUpdate = Body(...)):
    update_fields = update_data.model_dump(exclude_unset=True)
    if not update_fields:
        book = collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=404, detail=f"No book found with ID {book_id}")
        return {"message": "No fields provided for update", "book": book}
    result = collection.update_one({"_id": ObjectId(book_id)}, {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"No book found with ID {book_id}")
    updated_book = collection.find_one({"_id": ObjectId(book_id)})
    return {"message": "Book updated", "book": transformMongoDocument(updated_book)}


@app.delete("/books/{book_id}/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def deleteBookByID(book_id:str = Depends(validateObjectId)):
    result = collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"No book found with ID {book_id}")
    return {"message": f"Book with ID {book_id} deleted successfully"}
