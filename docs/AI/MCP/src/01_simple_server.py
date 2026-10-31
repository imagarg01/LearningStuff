"""
MCP Example 01: Stateless Core, Discovery, Header Routing & Prompts
===================================================================
Demonstrates the 2026-07-28 MCP stateless core architecture:
1. Mandatory capability discovery (`server/discover`) with `ttlMs` caching
2. Self-describing JSON-RPC requests carrying `_meta`
3. Stateless HTTP Header-Based Routing (`MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`)
4. Core primitives: Tools (`tools/list`, `tools/call`) and Prompts (`prompts/list`, `prompts/get`)
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional


@dataclass
class Tool:
    """An MCP tool definition (JSON Schema 2020-12)."""
    name: str
    description: str
    inputSchema: dict


@dataclass
class PromptArgument:
    """An argument for an MCP prompt template."""
    name: str
    description: str
    required: bool = True


@dataclass
class Prompt:
    """An MCP prompt template definition."""
    name: str
    title: str
    description: str
    arguments: list[PromptArgument]


@dataclass
class TextContent:
    """Text content result."""
    type: str = "text"
    text: str = ""


class SimpleMCPServer:
    """
    A stateless MCP server implementation (2026-07-28 specification).

    Demonstrates:
    - Stateless capability discovery (`server/discover`)
    - Header-Based Routing inspection (`MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`)
    - Cacheable list responses (`ttlMs`, `cacheScope`)
    - Tools and Prompts primitives
    """

    def __init__(self, name: str, version: str = "2.0.0"):
        self.name = name
        self.version = version
        self.tools: dict[str, Tool] = {}
        self.tool_handlers: dict[str, Callable] = {}
        self.prompts: dict[str, Prompt] = {}
        self.prompt_handlers: dict[str, Callable] = {}

    def register_tool(self, tool: Tool, handler: Callable):
        """Register a tool with its execution handler."""
        self.tools[tool.name] = tool
        self.tool_handlers[tool.name] = handler

    def register_prompt(self, prompt: Prompt, handler: Callable):
        """Register a reusable prompt template with its handler."""
        self.prompts[prompt.name] = prompt
        self.prompt_handlers[prompt.name] = handler

    def handle_http_request(self, headers: dict, body: dict) -> dict:
        """
        Simulate Stateless HTTP Transport with Header-Based Routing (2026-07-28).
        API Gateways inspect these headers before forwarding to the server.
        """
        proto_ver = headers.get("MCP-Protocol-Version", "2026-07-28")
        mcp_method = headers.get("Mcp-Method", body.get("method"))
        mcp_name = headers.get("Mcp-Name", "-")
        print(f"  [Gateway Header Route] MCP-Protocol-Version={proto_ver} | Mcp-Method={mcp_method} | Mcp-Name={mcp_name}")
        return self.handle_request(body)

    def handle_request(self, request: dict) -> dict:
        """Process a self-describing JSON-RPC request and return a stateless response."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "server/discover":
                result = self._handle_discover(params)
            elif method == "tools/list":
                result = self._handle_list_tools()
            elif method == "tools/call":
                result = self._handle_call_tool(params)
            elif method == "prompts/list":
                result = self._handle_list_prompts()
            elif method == "prompts/get":
                result = self._handle_get_prompt(params)
            else:
                return self._error_response(request_id, -32601, f"Unknown method: {method}")

            return self._success_response(request_id, result)

        except Exception as e:
            return self._error_response(request_id, -32000, str(e))

    def _handle_discover(self, params: dict) -> dict:
        """Handle mandatory server/discover request (2026-07-28 spec)."""
        return {
            "resultType": "complete",
            "supportedVersions": ["2026-07-28"],
            "capabilities": {
                "tools": {},
                "prompts": {}
            },
            "_meta": {
                "io.modelcontextprotocol/serverInfo": {
                    "name": self.name,
                    "version": self.version
                }
            },
            "instructions": "Stateless MCP server providing greeting/math tools and code-review prompt templates.",
            "ttlMs": 3600000,
            "cacheScope": "public"
        }

    def _handle_list_tools(self) -> dict:
        """Handle tools/list request with cacheable ttlMs."""
        return {
            "tools": [asdict(tool) for tool in self.tools.values()],
            "ttlMs": 3600000,
            "cacheScope": "public"
        }

    def _handle_call_tool(self, params: dict) -> dict:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name not in self.tool_handlers:
            return {
                "content": [{"type": "text", "text": f"Unknown tool '{tool_name}'. Use tools/list to see valid tools."}],
                "isError": True
            }

        result = self.tool_handlers[tool_name](arguments)
        return {
            "content": [asdict(result)] if isinstance(result, TextContent) else result,
            "isError": False
        }

    def _handle_list_prompts(self) -> dict:
        """Handle prompts/list request with cacheable ttlMs."""
        return {
            "prompts": [asdict(p) for p in self.prompts.values()],
            "ttlMs": 3600000,
            "cacheScope": "public"
        }

    def _handle_get_prompt(self, params: dict) -> dict:
        """Handle prompts/get request."""
        name = params.get("name")
        arguments = params.get("arguments", {})
        if name not in self.prompt_handlers:
            raise ValueError(f"Unknown prompt: {name}")
        return self.prompt_handlers[name](arguments)

    def _success_response(self, request_id: Any, result: Any) -> dict:
        return {"jsonrpc": "2.0", "result": result, "id": request_id}

    def _error_response(self, request_id: Any, code: int, message: str) -> dict:
        return {"jsonrpc": "2.0", "error": {"code": code, "message": message}, "id": request_id}


# =============================================================================
# Example Usage
# =============================================================================

def create_demo_server() -> SimpleMCPServer:
    """Create a stateless demo server with tools and prompt templates."""
    server = SimpleMCPServer("demo-stateless-server", "2.0.0")

    # 1. Register greeting tool
    server.register_tool(
        Tool(
            name="greet",
            description="Generate a greeting message",
            inputSchema={
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name to greet"}
                },
                "required": ["name"]
            }
        ),
        lambda args: TextContent(text=f"Hello, {args['name']}! Welcome to Stateless MCP (2026-07-28).")
    )

    # 2. Register calculator tool
    server.register_tool(
        Tool(
            name="calculate",
            description="Perform basic arithmetic",
            inputSchema={
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a", "b"]
            }
        ),
        lambda args: TextContent(
            text=str({
                "add": args["a"] + args["b"],
                "subtract": args["a"] - args["b"],
                "multiply": args["a"] * args["b"],
                "divide": args["a"] / args["b"] if args["b"] != 0 else "Error: Division by zero"
            }.get(args["operation"], "Unknown operation"))
        )
    )

    # 3. Register a reusable Prompt template
    server.register_prompt(
        Prompt(
            name="code_review",
            title="Structured Code Review",
            description="Generate a structured prompt for reviewing code changes",
            arguments=[
                PromptArgument(name="language", description="Programming language", required=True),
                PromptArgument(name="focus", description="Focus area (security, performance)", required=False)
            ]
        ),
        lambda args: {
            "description": f"Code review template for {args.get('language', 'code')}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": (
                            f"Please review this {args['language']} code with a focus on "
                            f"{args.get('focus', 'general quality')}. Highlight bugs and security risks."
                        )
                    }
                }
            ]
        }
    )

    return server


def simulate_mcp_session():
    """Simulate a 2026-07-28 stateless MCP flow with Header-Based Routing."""
    server = create_demo_server()

    default_meta = {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "EnterpriseHost", "version": "2.1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
    }

    print("=" * 70)
    print("MCP Example 01: Stateless Core, Header Routing & Prompts (2026-07-28)")
    print("=" * 70)

    # 1. Stateless Capability Discovery (server/discover)
    print("\n📡 1. Request: server/discover")
    print("-" * 50)
    response = server.handle_http_request(
        headers={"MCP-Protocol-Version": "2026-07-28", "Mcp-Method": "server/discover"},
        body={"jsonrpc": "2.0", "method": "server/discover", "params": {"_meta": default_meta}, "id": 1}
    )
    print(json.dumps(response, indent=2))

    # 2. List tools (with ttlMs caching)
    print("\n📋 2. Request: tools/list (Cacheable via ttlMs)")
    print("-" * 50)
    response = server.handle_http_request(
        headers={"MCP-Protocol-Version": "2026-07-28", "Mcp-Method": "tools/list"},
        body={"jsonrpc": "2.0", "method": "tools/list", "params": {"_meta": default_meta}, "id": 2}
    )
    print(json.dumps(response, indent=2))

    # 3. Call greet tool with Header-Based Routing
    print("\n🔧 3. Request: tools/call (greet)")
    print("-" * 50)
    response = server.handle_http_request(
        headers={"MCP-Protocol-Version": "2026-07-28", "Mcp-Method": "tools/call", "Mcp-Name": "greet"},
        body={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "greet", "arguments": {"name": "Developer"}, "_meta": default_meta},
            "id": 3
        }
    )
    print(json.dumps(response, indent=2))

    # 4. List & Get Prompts
    print("\n📝 4. Request: prompts/get (code_review)")
    print("-" * 50)
    response = server.handle_http_request(
        headers={"MCP-Protocol-Version": "2026-07-28", "Mcp-Method": "prompts/get", "Mcp-Name": "code_review"},
        body={
            "jsonrpc": "2.0",
            "method": "prompts/get",
            "params": {
                "name": "code_review",
                "arguments": {"language": "Java 21", "focus": "structured concurrency"},
                "_meta": default_meta
            },
            "id": 4
        }
    )
    print(json.dumps(response, indent=2))

    print("\n" + "=" * 70)
    print("✅ Stateless MCP session complete!")


if __name__ == "__main__":
    simulate_mcp_session()
