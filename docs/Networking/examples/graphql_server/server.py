"""
GraphQL Server Example with Strawberry
"""

import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from typing import Optional
from datetime import datetime

# In-memory database
users_db: dict = {}
next_id = 1


# Types
@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    created_at: datetime


@strawberry.input
class CreateUserInput:
    name: str
    email: str


@strawberry.input
class UpdateUserInput:
    name: Optional[str] = None
    email: Optional[str] = None


# Query
@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> Optional[User]:
        """Get a user by ID."""
        return users_db.get(str(id))
    
    @strawberry.field
    def users(self) -> list[User]:
        """Get all users."""
        return list(users_db.values())


# Mutation
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> User:
        """Create a new user."""
        global next_id
        
        user = User(
            id=strawberry.ID(str(next_id)),
            name=input.name,
            email=input.email,
            created_at=datetime.utcnow()
        )
        users_db[str(next_id)] = user
        next_id += 1
        return user
    
    @strawberry.mutation
    def update_user(self, id: strawberry.ID, input: UpdateUserInput) -> Optional[User]:
        """Update a user."""
        user = users_db.get(str(id))
        if not user:
            return None
        
        if input.name is not None:
            user = User(
                id=user.id,
                name=input.name,
                email=user.email,
                created_at=user.created_at
            )
        if input.email is not None:
            user = User(
                id=user.id,
                name=user.name,
                email=input.email,
                created_at=user.created_at
            )
        
        users_db[str(id)] = user
        return user
    
    @strawberry.mutation
    def delete_user(self, id: strawberry.ID) -> bool:
        """Delete a user."""
        if str(id) in users_db:
            del users_db[str(id)]
            return True
        return False


# Create schema and app
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="GraphQL API")
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def root():
    return {"message": "GraphQL API", "endpoint": "/graphql"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
