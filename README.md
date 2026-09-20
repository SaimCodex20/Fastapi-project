# FastAPI Project

A secure REST API backend built with Python, FastAPI, SQLAlchemy, SQLite, and JWT authentication.

## 🚀 Features

- User CRUD operations
- User registration
- Secure password hashing with bcrypt
- JWT-based authentication
- Login and logout endpoints
- Protected user profile endpoint
- Users can update their own account
- Users cannot update or delete another user's account
- Request validation with Pydantic
- SQLAlchemy database integration
- SQLite database
- Automated API testing with pytest
- Automatic interactive API documentation

## 🛠️ Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- Passlib
- Bcrypt
- Pytest
- HTTPX
- Uvicorn

## 📁 Project Structure

```text
Fastapi-project/
│
├── main.py
├── auth.py
├── database.py
├── models.py
├── requirements.txt
├── pytest.ini
├── README.md
├── tests/
│   ├── conftest.py
│   └── test_main.py
└── .gitignore