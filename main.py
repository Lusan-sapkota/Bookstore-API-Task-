import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
import schemas
import auth
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bookstore API",
    description="A RESTful API for managing a bookstore's inventory",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get(
    "/books/", 
    response_model=schemas.PaginatedBooks, 
    tags=["books"],
    summary="List all books",
    description="Retrieve a paginated list of all books in the system"
)
def read_books(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size
    books = crud.get_books(db, skip=skip, limit=size)
    total = crud.count_books(db)
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "books": books
    }

@app.post(
    "/books/", 
    response_model=schemas.Book, 
    status_code=status.HTTP_201_CREATED,
    tags=["books"],
    summary="Create a new book",
    description="Add a new book to the system"
)
def create_book(
    book: schemas.BookCreate, 
    api_key: str = Depends(auth.get_api_key),
    db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)

@app.get(
    "/books/{book_id}", 
    response_model=schemas.Book, 
    tags=["books"],
    summary="Get a book by ID",
    description="Retrieve details of a specific book by its ID",
    responses={404: {"description": "Book not found"}}
)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put(
    "/books/{book_id}", 
    response_model=schemas.Book, 
    tags=["books"],
    summary="Update a book",
    description="Update the details of an existing book",
    responses={404: {"description": "Book not found"}}
)
def update_book(
    book_id: int, 
    book: schemas.BookCreate, 
    api_key: str = Depends(auth.get_api_key),
    db: Session = Depends(get_db)
):
    db_book = crud.update_book(db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete(
    "/books/{book_id}", 
    response_model=schemas.Book, 
    tags=["books"],
    summary="Delete a book",
    description="Delete a book from the system",
    responses={404: {"description": "Book not found"}}
)
def delete_book(
    book_id: int, 
    api_key: str = Depends(auth.get_api_key),
    db: Session = Depends(get_db)
):
    db_book = crud.delete_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to Bookstore API. Go to /docs for API documentation."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)