"""
REST API Example with FastAPI
Demonstrates CRUD operations, pagination, and error handling.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Users API",
    description="REST API example demonstrating best practices",
    version="1.0.0"
)

# Database (in-memory)
users_db: dict = {}
next_id = 1


# Models
class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserList(BaseModel):
    data: list[User]
    total: int
    page: int
    per_page: int


class ErrorResponse(BaseModel):
    error: dict


# Endpoints
@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to Users API", "docs": "/docs"}


@app.post("/users", response_model=User, status_code=201, tags=["Users"])
def create_user(user: UserCreate):
    """Create a new user."""
    global next_id
    
    # Check for duplicate email
    for u in users_db.values():
        if u["email"] == user.email:
            raise HTTPException(status_code=409, detail="Email already exists")
    
    now = datetime.utcnow()
    new_user = {
        "id": next_id,
        "name": user.name,
        "email": user.email,
        "created_at": now,
        "updated_at": now
    }
    users_db[next_id] = new_user
    next_id += 1
    
    return new_user


@app.get("/users", response_model=UserList, tags=["Users"])
def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page")
):
    """List users with pagination."""
    all_users = list(users_db.values())
    total = len(all_users)
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated = all_users[start:end]
    
    return UserList(
        data=paginated,
        total=total,
        page=page,
        per_page=per_page
    )


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int):
    """Get a user by ID."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.put("/users/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, user: UserUpdate):
    """Update a user."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing = users_db[user_id]
    
    if user.name is not None:
        existing["name"] = user.name
    if user.email is not None:
        existing["email"] = user.email
    
    existing["updated_at"] = datetime.utcnow()
    
    return existing


@app.delete("/users/{user_id}", status_code=204, tags=["Users"])
def delete_user(user_id: int):
    """Delete a user."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return None


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
