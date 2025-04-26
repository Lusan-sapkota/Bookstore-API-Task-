# 📚 Bookstore API

A RESTful API for managing a bookstore's inventory built with FastAPI, SQLAlchemy, and SQLite.

---

## ✨ Features

- ✅ **Complete CRUD operations** for books management
- 🔒 **Token-based authentication** for secure endpoints
- ⚙️ **Input validation** to ensure data integrity
- 📄 **Pagination support** for efficient data retrieval
- ⚠️ **Comprehensive error handling**
- 🐳 **Docker support** for easy deployment

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: SQLite
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Testing**: pytest

---

## 📋 API Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|---------------|
| GET | `/books/` | List all books (with pagination) | No |
| POST | `/books/` | Create a new book | Yes |
| GET | `/books/{book_id}` | Retrieve a specific book | No |
| PUT | `/books/{book_id}` | Update a book | Yes |
| DELETE | `/books/{book_id}` | Delete a book | Yes |

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Bookstore-API-Task-.git
   cd Bookstore-API-Task-
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Linux/macOS
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

### Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t bookstore-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 bookstore-api
   ```

---

## 🔐 Authentication

Protected endpoints require an API token header:

```
X-API-Token: mysecrettoken
```

### Example using curl:

```bash
# Create a new book (protected endpoint)
curl -X POST "http://localhost:8000/books/" \
     -H "X-API-Token: mysecrettoken" \
     -H "Content-Type: application/json" \
     -d '{"title":"The Great Gatsby", "author":"F. Scott Fitzgerald", "published_year":1925}'
```

### Using Swagger UI:

1. Navigate to the docs: http://localhost:8000/docs
2. Click the 🔓 (lock) icon in the top right
3. Enter `mysecrettoken` in the API key field
4. Click "Authorize"

---

## 📝 API Usage Examples

### Create a new book

```bash
curl -X POST "http://localhost:8000/books/" \
     -H "X-API-Token: mysecrettoken" \
     -H "Content-Type: application/json" \
     -d '{"title":"1984", "author":"George Orwell", "published_year":1949}'
```

### Get a list of books with pagination

```bash
curl -X GET "http://localhost:8000/books/?page=1&size=10"
```

### Get a specific book

```bash
curl -X GET "http://localhost:8000/books/1"
```

### Update a book

```bash
curl -X PUT "http://localhost:8000/books/1" \
     -H "X-API-Token: mysecrettoken" \
     -H "Content-Type: application/json" \
     -d '{"title":"1984", "author":"George Orwell", "published_year":1948}'
```

### Delete a book

```bash
curl -X DELETE "http://localhost:8000/books/1" \
     -H "X-API-Token: mysecrettoken"
```

---

## 🧪 Testing

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_api.py
```

---

## 📄 API Documentation

FastAPI generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## ⚙️ Configuration

The API uses a hardcoded token for simplicity. In a production environment, you would want to use environment variables:

```python
# Example of how you might handle this in production
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY", "fallback_key")
```

---

## 📊 Pagination

The `GET /books/` endpoint supports pagination:

- **page**: Page number (default: 1)
- **size**: Items per page (default: 10, max: 100)

Example:
```
GET /books/?page=2&size=15
```

---

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)

---

*Made with ❤️ and FastAPI*