# REST API

Representational State Transfer (REST) - the most widely used API architecture.

---

## REST Fundamentals

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: GET /api/users/123
    Server->>Client: 200 OK + JSON
    
    Client->>Server: POST /api/users
    Server->>Client: 201 Created
    
    Client->>Server: PUT /api/users/123
    Server->>Client: 200 OK
    
    Client->>Server: DELETE /api/users/123
    Server->>Client: 204 No Content
```

---

## HTTP Methods

| Method | CRUD | Description | Idempotent | Safe |
|--------|------|-------------|------------|------|
| **GET** | Read | Retrieve resource | ✓ | ✓ |
| **POST** | Create | Create new resource | ✗ | ✗ |
| **PUT** | Update | Replace entire resource | ✓ | ✗ |
| **PATCH** | Update | Partial update | ✗ | ✗ |
| **DELETE** | Delete | Remove resource | ✓ | ✗ |
| **HEAD** | - | GET without body | ✓ | ✓ |
| **OPTIONS** | - | Get allowed methods | ✓ | ✓ |

### Idempotency

```python
# Idempotent: calling multiple times has same effect
PUT /users/123 {"name": "John"}  # Always results in same state

# Not idempotent: each call creates new resource
POST /users {"name": "John"}  # Creates new user each time
```

---

## HTTP Status Codes

### Success (2xx)

| Code | Name | Use Case |
|------|------|----------|
| **200** | OK | Successful GET, PUT, PATCH |
| **201** | Created | Successful POST |
| **202** | Accepted | Async processing started |
| **204** | No Content | Successful DELETE |

### Redirection (3xx)

| Code | Name | Use Case |
|------|------|----------|
| **301** | Moved Permanently | Resource moved |
| **304** | Not Modified | Cached response valid |

### Client Errors (4xx)

| Code | Name | Use Case |
|------|------|----------|
| **400** | Bad Request | Invalid syntax |
| **401** | Unauthorized | Authentication required |
| **403** | Forbidden | Authenticated but not allowed |
| **404** | Not Found | Resource doesn't exist |
| **405** | Method Not Allowed | HTTP method not supported |
| **409** | Conflict | Resource conflict |
| **422** | Unprocessable Entity | Validation failed |
| **429** | Too Many Requests | Rate limited |

### Server Errors (5xx)

| Code | Name | Use Case |
|------|------|----------|
| **500** | Internal Server Error | Server error |
| **502** | Bad Gateway | Upstream error |
| **503** | Service Unavailable | Temporarily down |
| **504** | Gateway Timeout | Upstream timeout |

---

## REST Constraints

REST is defined by six architectural constraints:

### 1. Client-Server

```mermaid
graph LR
    Client["Client<br/>(UI)"] <-->|HTTP| Server["Server<br/>(Data)"]
```

Separation of concerns - UI and data storage are independent.

### 2. Stateless

Each request contains all information needed to process it.

```python
# ❌ Bad: Server maintains session state
GET /cart

# ✓ Good: Client sends all context
GET /cart?user_id=123
# Or use JWT token in header
Authorization: Bearer <token>
```

### 3. Cacheable

Responses must indicate if they're cacheable.

```http
HTTP/1.1 200 OK
Cache-Control: max-age=3600
ETag: "abc123"
```

### 4. Uniform Interface

| Principle | Description |
|-----------|-------------|
| Resource identification | URLs identify resources |
| Resource manipulation | HTTP methods define operations |
| Self-descriptive messages | Content-Type, Accept headers |
| HATEOAS | Links in responses |

### 5. Layered System

```mermaid
graph LR
    Client --> CDN --> LB["Load Balancer"] --> App["Application"]
```

### 6. Code on Demand (Optional)

Server can send executable code (JavaScript).

---

## URL Design

### Resource Naming

```bash
# Resources are nouns (plural)
GET /users
GET /users/123
GET /users/123/orders
GET /users/123/orders/456

# Avoid verbs in URLs
❌ GET /getUser/123
❌ POST /createUser
✓ GET /users/123
✓ POST /users
```

### Query Parameters

```bash
# Filtering
GET /users?status=active&role=admin

# Pagination
GET /users?page=2&limit=20
GET /users?offset=20&limit=20
GET /users?cursor=abc123

# Sorting
GET /users?sort=name         # Ascending
GET /users?sort=-created_at  # Descending
GET /users?sort=name,-age    # Multiple

# Field selection
GET /users?fields=id,name,email

# Search
GET /users?q=john
GET /users?search=john
```

---

## Request/Response Examples

### GET - Retrieve Resource

```http
GET /api/v1/users/123 HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer <token>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z",
  "_links": {
    "self": "/api/v1/users/123",
    "orders": "/api/v1/users/123/orders"
  }
}
```

### POST - Create Resource

```http
POST /api/v1/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/users/124

{
  "id": 124,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "created_at": "2024-01-15T11:00:00Z"
}
```

### PUT - Replace Resource

```http
PUT /api/v1/users/123 HTTP/1.1
Content-Type: application/json

{
  "name": "John Smith",
  "email": "john.smith@example.com"
}
```

### PATCH - Partial Update

```http
PATCH /api/v1/users/123 HTTP/1.1
Content-Type: application/json

{
  "name": "John Smith"
}
```

### DELETE - Remove Resource

```http
DELETE /api/v1/users/123 HTTP/1.1
Authorization: Bearer <token>
```

```http
HTTP/1.1 204 No Content
```

---

## HATEOAS

Hypermedia as the Engine of Application State.

```json
{
  "id": 123,
  "name": "John Doe",
  "status": "active",
  "_links": {
    "self": {"href": "/users/123"},
    "orders": {"href": "/users/123/orders"},
    "deactivate": {"href": "/users/123/deactivate", "method": "POST"}
  },
  "_embedded": {
    "recent_orders": [
      {"id": 456, "total": 99.99}
    ]
  }
}
```

---

## Richardson Maturity Model

```mermaid
graph TB
    L3["Level 3: HATEOAS<br/>Hypermedia controls"]
    L2["Level 2: HTTP Verbs<br/>GET, POST, PUT, DELETE"]
    L1["Level 1: Resources<br/>/users, /orders"]
    L0["Level 0: The Swamp<br/>Single endpoint, POST only"]
    
    L0 --> L1 --> L2 --> L3
```

| Level | Description | Example |
|-------|-------------|---------|
| 0 | Single endpoint | `POST /api` |
| 1 | Multiple resources | `GET /users`, `GET /orders` |
| 2 | HTTP verbs | `GET`, `POST`, `PUT`, `DELETE` |
| 3 | Hypermedia | Links in responses |

---

## Versioning Strategies

### URL Versioning (Most Common)

```bash
GET /api/v1/users
GET /api/v2/users
```

### Header Versioning

```http
GET /api/users
Accept: application/vnd.api+json; version=2
```

### Query Parameter

```bash
GET /api/users?version=2
```

---

## Pagination Patterns

### Offset Pagination

```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### Cursor Pagination

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIzfQ==",
    "prev_cursor": "eyJpZCI6MTAzfQ==",
    "has_more": true
  }
}
```

### Link Headers

```http
Link: <https://api.example.com/users?page=3>; rel="next",
      <https://api.example.com/users?page=1>; rel="prev"
```

---

## Error Handling

### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "age",
        "message": "Must be a positive number"
      }
    ],
    "request_id": "req_abc123",
    "documentation_url": "https://docs.api.com/errors/VALIDATION_ERROR"
  }
}
```

### Problem Details (RFC 7807)

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "Email format is invalid",
  "instance": "/users/signup",
  "errors": [
    {"pointer": "/email", "detail": "Invalid format"}
  ]
}
```

---

## OpenAPI/Swagger

```yaml
openapi: 3.0.3
info:
  title: Users API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    
    post:
      summary: Create user
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
      responses:
        '201':
          description: Created

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
```

---

## Authentication

### API Keys

```http
GET /api/users
X-API-Key: sk_live_abc123
```

### Bearer Token (JWT)

```http
GET /api/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### OAuth 2.0

```mermaid
sequenceDiagram
    Client->>Auth Server: Request token
    Auth Server->>Client: Access token
    Client->>API: Request + Bearer token
    API->>Client: Response
```

---

## Rate Limiting

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640000000
```

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds."
  }
}
```

---

## Best Practices

### Do's ✓

- Use nouns for resources
- Use HTTP methods correctly
- Return appropriate status codes
- Version your API
- Implement pagination
- Use HTTPS
- Validate input
- Document with OpenAPI

### Don'ts ✗

- Don't use verbs in URLs
- Don't ignore HTTP methods
- Don't return 200 for errors
- Don't break backwards compatibility
- Don't expose stack traces
- Don't send sensitive data in URLs

---

## Next Steps

- **[gRPC](02_grpc.md)** - High-performance RPC framework
