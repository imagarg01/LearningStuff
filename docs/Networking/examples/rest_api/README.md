# REST API Example

FastAPI server with full CRUD operations.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
# Start server
uvicorn server:app --reload

# Docs: http://localhost:8000/docs
```

## Test

```bash
# Create user
curl -X POST http://localhost:8000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "John", "email": "john@example.com"}'

# Get user
curl http://localhost:8000/users/1

# List users
curl http://localhost:8000/users

# Update user
curl -X PUT http://localhost:8000/users/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john.doe@example.com"}'

# Delete user
curl -X DELETE http://localhost:8000/users/1
```
