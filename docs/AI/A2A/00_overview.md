# A2A (Agent-to-Agent Protocol)

A2A is an open protocol enabling **communication and interoperability between AI agents**. It allows agents to collaborate on tasks without sharing internal implementation details.

> [!NOTE]
> **Created by**: Google (a2aproject)  
> **Status**: Active development  
> **SDKs**: Python, Go, JavaScript, Java, .NET

## The Problem

As AI agents proliferate, they need to **work together**:

```mermaid
graph LR
    subgraph "Without A2A"
        A1[Travel Agent] --> Custom1[Custom API]
        A2[Calendar Agent] --> Custom2[Different API]
        A3[Email Agent] --> Custom3[Another API]
    end
```

**Issues:**

- No standard for agent-to-agent communication
- Agents can't discover each other's capabilities
- Complex custom integrations for each pair

## The Solution: A2A

A2A provides a **standardized protocol** for agent communication:

```mermaid
graph TB
    subgraph "With A2A"
        subgraph "Agents"
            A1[Travel Agent]
            A2[Calendar Agent]
            A3[Email Agent]
        end
        
        A2A[A2A Protocol]
        
        A1 <-->|Tasks| A2A
        A2 <-->|Tasks| A2A
        A3 <-->|Tasks| A2A
        A2A <-->|Collaborate| A1
        A2A <-->|Collaborate| A2
        A2A <-->|Collaborate| A3
    end
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Agent Cards** | Standardized capability discovery |
| **Tasks** | Structured work units |
| **JSON-RPC 2.0** | Standard communication protocol |
| **Streaming** | SSE for real-time updates |
| **Push Notifications** | Async task updates |
| **Opacity** | Agents keep internals private |

## Why A2A?

| Goal | How A2A Helps |
|------|---------------|
| **Break Silos** | Connect agents across ecosystems |
| **Enable Collaboration** | Multi-agent task completion |
| **Open Standards** | Community-driven development |
| **Preserve Opacity** | No shared memory or logic |

## Core Concepts

### Agent Cards

Every A2A agent publishes an **Agent Card** describing its capabilities:

```json
{
    "name": "Travel Planning Agent",
    "description": "Book flights, hotels, and create itineraries",
    "url": "https://travel-agent.example.com",
    "capabilities": {
        "streaming": true,
        "pushNotifications": true
    },
    "skills": [
        {
            "id": "book_flight",
            "name": "Book Flight",
            "description": "Search and book flights"
        },
        {
            "id": "create_itinerary",
            "name": "Create Itinerary",
            "description": "Plan a complete trip"
        }
    ]
}
```

### Tasks

Work is organized into **Tasks** that can span multiple messages:

```mermaid
sequenceDiagram
    participant Client as Client Agent
    participant Server as Server Agent
    
    Client->>Server: tasks/send (new task)
    Server-->>Client: Task accepted
    
    Server-->>Client: Task status: working
    Server-->>Client: Task artifact: results
    Server-->>Client: Task status: completed
```

### Messages

Tasks contain **Messages** with rich content:

```json
{
    "role": "user",
    "parts": [
        {
            "type": "text",
            "text": "Find me a flight to Tokyo"
        },
        {
            "type": "file",
            "mimeType": "application/pdf",
            "data": "base64..."
        }
    ]
}
```

## Communication Patterns

```mermaid
graph TD
    subgraph "A2A Communication"
        Sync[Synchronous<br/>Request/Response]
        Stream[Streaming<br/>SSE]
        Push[Push<br/>Notifications]
    end
```

| Pattern | Use Case |
|---------|----------|
| **Sync** | Simple queries, quick tasks |
| **Streaming** | Long-running tasks, progress |
| **Push** | Async updates, background work |

## Protocol Relationships

```mermaid
graph TD
    subgraph "AI Protocol Stack"
        MCP[MCP<br/>AI ↔ Tools]
        A2A[A2A<br/>Agent ↔ Agent]
        A2UI[A2UI<br/>Agent → UI]
        UCP[UCP<br/>Agent → Commerce]
    end
    
    MCP --> A2A
    A2A --> A2UI
    A2A --> UCP
```

| Protocol | Purpose |
|----------|---------|
| **MCP** | Connect AI to tools |
| **A2A** | Connect agents to agents |
| **A2UI** | Render UI from agents |
| **UCP** | Commerce operations |

## Quick Start

```bash
# Install A2A SDK
pip install a2a-sdk

# Create an agent
from a2a import Agent, AgentCard

agent = Agent(
    card=AgentCard(
        name="My Agent",
        skills=[...]
    )
)
```

## Next Steps

| Document | Description |
|----------|-------------|
| [01_agent_cards.md](./01_agent_cards.md) | Discovery and capabilities |
| [02_tasks.md](./02_tasks.md) | Task lifecycle |
| [03_communication.md](./03_communication.md) | JSON-RPC, streaming |
| [04_security.md](./04_security.md) | Auth and security |
| [05_pros_and_cons.md](./05_pros_and_cons.md) | Analysis |
