# MCP

An open protocol that standardizes how applications provide context to LLMs. MCP Provides:

1. A growing list of pre-built integrations that your LLM can directly plug into.
2. The flexibility to switch between LLM providers and vendors.
3. Best practices to securing your data within your infrastructure.

MCP follows a client-server architecture, where a host application can connect to multiple MCP servers, each providing different capabilities. This allows for a modular approach to integrating LLMs with various data sources and tools.

## Different Components

### MCP Hosts

Programs like Claude desktop, IDEs, or AI tools that want to access data through MCP.

### MCP Client

Protocol clients that maintain 1:1 connections with servers.

### MCP Servers

Lightweight programs that expose specific capabilities through MCP.

### Local Data Sources

Your computer files, databases, and services that MCP servers can securely access.

### Remote Services

External system over internet, that MCP servers can securely access.

## MCP Servers

It can provide three different capabilities:

1. **Resources**: File-like data that can be read by clients.
2. **Tools**: Functions that can be called by the LLM.
3. **Prompts**: Pre-written templated that help users accomplish specific tasks.

## MCP Clients

The client will:

1. Connect to a server.
2. List the available resources, tools, and prompts.
3. Start an interactive chat session, where you can

- Enter queries.
- See tool executions.

## Core Components

### Protocol layer

Handles message framing, request/response linking, and high-level communication patterns.

### Transport Layer

Handles the actual communication between clients and servers. MSP supports multiple transport mechanisms:

1. Stdio transport

- Uses standard input/output for communication.
- Ideal for local processes

2. HTTP with SSE transport

- Uses Server-Send Events for server-to-client messages.
- HTTP POST for client-to-server messages.

All transports uses JSON-RPC 2.0 to exchange messages.

### Resources

Expose data and content from your servers to LLMs. Resources represent any kind of data that an MCP server wants to make available clients. This can include:

1. File Contents
2. Database records
3. API responses.
4. Live system data
5. Screenshots and Images
6. Log Files.

Resources are indentified using URI that follow the format:

```text
[protocol]://[host]/[path]
```

### Prompts

Create reusable prompt templates and workflows. Prompts enable servers to define resuable templates that can be used by clients to generate specific outputs.

Prompts in MCP are defined templates that can:

- Accept dynamic arguments.
- Include context from resources.
- Chain multiple interactions.
- Guide specific workflows.
- Surface as UI elements.

Prompt structure:

```json
{
  name: string;              // Unique identifier for the prompt
  description?: string;      // Human-readable description
  arguments?: [              // Optional list of arguments
    {
      name: string;          // Argument identifier
      description?: string;  // Argument description
      required?: boolean;    // Whether argument is required
    }
  ]
}
```

### Tools

Enable LLMs to perform actions through your server. Through tools, MCP servers can expose functions that LLMs can call to perform specific actions. This allows LLMs to interact with the server's capabilities directly.

Key aspects of tools:

- **Discovery**: Clients can discover tools through the server. tools/list endpoint.
- **Invocation**: Clients can invoke tools through the server. tools/call endpoint.
- **Flexibility**: Tools can range from simple calculations to complex workflows.

Like resources, tools are identified by unique names and can include descriptions to guide their usage. MCP supports dynamic tool discovery:

1. Client can list available tools at any time.
2. Servers can notify clients when tool change using **_notifications/tools/list_changed_**.
3. Tools can be added, removed at runtime.
4. Tool definitions can be updated at runtime.

### Sampling

Its a powerful feature that allows server to request LLM completions through the client. The sampling flow follow these steps:

1. Server sends a sampling/createMessage request to the client.
2. Client reviews the request and can modify it.
3. Client samples from LLM.
4. Client review the completion.
5. Client returns the result to the server.

Sampling is designed with human oversight in mind:

#### For prompts

1. Clients should show users the proposed prompt.
2. User should be able to modify or reject the prompt.
3. System prompts can be filtered or modified.
4. Context inclusion is controlled by the client.

#### For completions

1. Client should show users the completion.
2. Users should be able to modify or reject the completion.
3. Client can filter or modify the completion.
4. User control which model is used.

### Roots

Root are a concept in MCP that define the boundaries where server can operate. They provide a way for clients to inform servers about relevant resources and their locations.

A root is a URI that a client suggests a server should focus on. When a client connects to a server, it declares which roots the server should work with. While primary used for
filesystem paths, roots can be any valid URI include HTTP URLs.

For example, roots could be:

```text
file:///home/user/Documents
https://api.openai.com/v1/
```

Roots serve several important purposes:

1. **Guidance**: They inform servers about relevant resources and their locations.
2. **Clarity**: Roots make it clear which resources are part of your workspace.
3. **Organization**: Multiple roots let you work with different resources simultaneously.
