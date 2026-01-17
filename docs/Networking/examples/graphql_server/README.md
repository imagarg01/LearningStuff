# GraphQL Example

Strawberry GraphQL server with queries and mutations.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python server.py
# GraphiQL: http://localhost:8000/graphql
```

## Test Queries

```graphql
# Create user
mutation {
  createUser(input: {name: "John", email: "john@example.com"}) {
    id
    name
  }
}

# Get users
query {
  users {
    id
    name
    email
  }
}

# Get user by ID
query {
  user(id: "1") {
    name
    email
  }
}
```
