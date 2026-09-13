from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}


@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Saim"},
        {"id": 2, "name": "Alex"},
        {"id": 3, "name": "John"}
    ]


class User(BaseModel):
    name: str
    email: str


@app.post("/users")
def create_user(user: User):
    
    return {
        "message": "User created successfully",
        "user": user
    }
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {
        "message": "User deleted successfully",
        "user_id": user_id
    }
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    return {
        "message": "User updated successfully",
        "user_id": user_id,
        "user": user
    }