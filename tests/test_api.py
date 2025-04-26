import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def test_client():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Use our test DB instead of the main one
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)

def test_create_book(test_client):
    # Test POST /books/ endpoint
    response = test_client.post(
        "/books/",
        headers={"X-API-Token": "mysecrettoken"},
        json={"title": "Test Book", "author": "Test Author", "published_year": 2023}
    )
    assert response.status_code == 201  # Updated to match the status code in main.py
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert data["published_year"] == 2023
    assert "id" in data

    # Return the book ID for other tests
    return data["id"]

def test_read_book(test_client):
    # First create a book
    book_id = test_create_book(test_client)
    
    # Test GET /books/{book_id} endpoint
    response = test_client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["id"] == book_id

def test_read_books(test_client):
    # Create a few books
    test_create_book(test_client)
    test_create_book(test_client)
    
    # Test GET /books/ endpoint
    response = test_client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert len(data["books"]) >= 2

def test_update_book(test_client):
    # First create a book
    book_id = test_create_book(test_client)
    
    # Test PUT /books/{book_id} endpoint
    updated_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "published_year": 2024
    }
    response = test_client.put(
        f"/books/{book_id}",
        headers={"X-API-Token": "mysecrettoken"},
        json=updated_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Book"
    assert data["author"] == "Updated Author"
    assert data["published_year"] == 2024

def test_delete_book(test_client):
    # First create a book
    book_id = test_create_book(test_client)
    
    # Test DELETE /books/{book_id} endpoint
    response = test_client.delete(
        f"/books/{book_id}",
        headers={"X-API-Token": "mysecrettoken"},
    )
    assert response.status_code == 200
    
    # Verify book is deleted
    response = test_client.get(f"/books/{book_id}")
    assert response.status_code == 404

def test_authentication(test_client):
    # Test without token
    response = test_client.post(
        "/books/",
        json={"title": "Unauthorized Book", "author": "Auth Test", "published_year": 2023}
    )
    assert response.status_code == 401
    
    # Test with invalid token
    response = test_client.post(
        "/books/",
        headers={"X-API-Token": "wrongtoken"},
        json={"title": "Unauthorized Book", "author": "Auth Test", "published_year": 2023}
    )
    assert response.status_code == 401