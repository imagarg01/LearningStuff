# Security

A2A provides robust security patterns for **authentication**, **authorization**, and **trust**.

## Overview

```mermaid
graph TD
    subgraph "A2A Security"
        Auth[Authentication<br/>Bearer, OAuth, API Key]
        Authz[Authorization<br/>Scopes, Permissions]
        Trust[Trust<br/>Agent verification]
    end
```

---

## Authentication

### Supported Schemes

| Scheme | Description |
|--------|-------------|
| `bearer` | Bearer token in Authorization header |
| `oauth2` | OAuth 2.0 code flow |
| `apiKey` | API key in header or query |

### Bearer Token

```http
POST /a2a HTTP/1.1
Host: agent.example.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
Content-Type: application/json
```

### Agent Card Declaration

```json
{
    "authentication": {
        "schemes": ["bearer", "oauth2"],
        "oauth2": {
            "authorizationUrl": "https://auth.example.com/authorize",
            "tokenUrl": "https://auth.example.com/token",
            "scopes": {
                "agent:read": "Read agent data",
                "agent:write": "Send tasks to agent"
            }
        }
    }
}
```

---

## OAuth 2.0 Flow

```mermaid
sequenceDiagram
    participant Client
    participant Auth as Auth Server
    participant Agent as Target Agent
    
    Client->>Agent: GET /.well-known/agent.json
    Agent-->>Client: Agent Card (with OAuth config)
    
    Client->>Auth: Authorization request
    Auth-->>Client: Authorization code
    
    Client->>Auth: Token exchange
    Auth-->>Client: Access token
    
    Client->>Agent: POST /a2a + Bearer token
    Agent->>Agent: Validate token
    Agent-->>Client: Response
```

### Token Request

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=abc123
&redirect_uri=https://client.example.com/callback
&client_id=client_xyz
```

### Token Response

```json
{
    "access_token": "eyJhbGciOiJSUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "ref_xyz",
    "scope": "agent:read agent:write"
}
```

---

## Authorization

### Scopes

| Scope | Permission |
|-------|------------|
| `agent:read` | Discover agent, get task status |
| `agent:write` | Create tasks, send messages |
| `agent:admin` | Cancel tasks, manage subscriptions |

### Scope Checking

```json
{
    "authentication": {
        "requiredScopes": {
            "tasks/send": ["agent:write"],
            "tasks/get": ["agent:read"],
            "tasks/cancel": ["agent:admin"]
        }
    }
}
```

---

## Webhook Security

For push notifications, secure webhooks with tokens:

### Registration

```json
{
    "notification": {
        "url": "https://client.example.com/webhooks/a2a",
        "token": "webhook_secret_abc123"
    }
}
```

### Verification

```http
POST /webhooks/a2a HTTP/1.1
Host: client.example.com
X-A2A-Token: webhook_secret_abc123
X-A2A-Signature: sha256=abc123...
```

### Signature Verification

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected}", signature)
```

---

## Trust Model

### Agent Verification

```mermaid
graph LR
    Client[Client Agent]
    Card[Agent Card]
    DNS[DNS Verification]
    TLS[TLS Certificate]
    
    Client --> Card
    Card --> DNS
    DNS --> TLS
```

### Verification Steps

1. Fetch Agent Card from well-known URL
2. Verify TLS certificate is valid
3. Verify domain matches Agent Card URL
4. Check agent reputation (optional)

---

## Rate Limiting

Agents should implement rate limiting:

### Response Headers

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704067200
```

### Error Response

```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32000,
        "message": "Rate limit exceeded",
        "data": {
            "retryAfter": 60,
            "limit": 100
        }
    },
    "id": 1
}
```

---

## Best Practices

### For Client Agents

- ✅ Validate Agent Card before trusting
- ✅ Use short-lived tokens
- ✅ Verify webhook signatures
- ✅ Implement retry with backoff
- ❌ Don't hardcode secrets

### For Server Agents

- ✅ Validate all tokens
- ✅ Implement rate limiting
- ✅ Log all authentication attempts
- ✅ Use HTTPS only
- ❌ Don't expose internal errors

---

## Security Checklist

| Check | Status |
|-------|--------|
| HTTPS required | ☐ |
| Token validation | ☐ |
| Scope enforcement | ☐ |
| Rate limiting | ☐ |
| Webhook signatures | ☐ |
| Error sanitization | ☐ |
| Audit logging | ☐ |

---

## Summary

| Layer | Mechanism |
|-------|-----------|
| **Transport** | TLS 1.3 |
| **Authentication** | Bearer, OAuth 2.0 |
| **Authorization** | Scopes |
| **Webhooks** | Token + Signature |
| **Rate Limiting** | Per-client quotas |

> [!IMPORTANT]
> Always verify agent identity before sharing sensitive data. Use OAuth 2.0 for production deployments.
