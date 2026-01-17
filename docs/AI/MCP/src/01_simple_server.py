"""
MCP Example 01: Simple Server
=============================
A minimal MCP server demonstrating the basic structure.

This example shows:
1. Server initialization
2. Tool listing
3. Tool execution
4. Stdio transport simulation
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class Tool:
    """An MCP tool definition."""
    name: str
    description: str
    inputSchema: dict


@dataclass
class TextContent:
    """Text content result."""
    type: str = "text"
    text: str = ""


@dataclass
class ToolResult:
    """Result of a tool call."""
    content: list


class SimpleMCPServer:
    """
    A simple MCP server implementation.
    
    Demonstrates the core patterns:
    - Tool registration
    - Request handling
    - Response formatting
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: dict[str, Tool] = {}
        self.handlers: dict[str, callable] = {}
    
    def register_tool(self, tool: Tool, handler: callable):
        """Register a tool with its handler."""
        self.tools[tool.name] = tool
        self.handlers[tool.name] = handler
    
    def handle_request(self, request: dict) -> dict:
        """Process a JSON-RPC request and return response."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                result = self._handle_initialize(params)
            elif method == "tools/list":
                result = self._handle_list_tools()
            elif method == "tools/call":
                result = self._handle_call_tool(params)
            else:
                return self._error_response(request_id, -32601, f"Unknown method: {method}")
            
            return self._success_response(request_id, result)
        
        except Exception as e:
            return self._error_response(request_id, -32000, str(e))
    
    def _handle_initialize(self, params: dict) -> dict:
        """Handle initialize request."""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {"listChanged": False}
            },
            "serverInfo": {
                "name": self.name,
                "version": self.version
            }
        }
    
    def _handle_list_tools(self) -> dict:
        """Handle tools/list request."""
        return {
            "tools": [asdict(tool) for tool in self.tools.values()]
        }
    
    def _handle_call_tool(self, params: dict) -> dict:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.handlers:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        result = self.handlers[tool_name](arguments)
        
        return {
            "content": [asdict(result)] if isinstance(result, TextContent) else result
        }
    
    def _success_response(self, request_id: Any, result: Any) -> dict:
        """Create a success response."""
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }
    
    def _error_response(self, request_id: Any, code: int, message: str) -> dict:
        """Create an error response."""
        return {
            "jsonrpc": "2.0",
            "error": {"code": code, "message": message},
            "id": request_id
        }
    
    def run_stdio(self):
        """Run server with stdio transport (simulation)."""
        print(f"[{self.name}] MCP Server ready (stdio mode)", file=sys.stderr)
        
        # In real implementation, would read from stdin
        # For demo, we simulate requests
        pass


# =============================================================================
# Example Usage
# =============================================================================

def create_demo_server():
    """Create a simple demo server with one tool."""
    
    server = SimpleMCPServer("demo-server", "1.0.0")
    
    # Register a simple greeting tool
    server.register_tool(
        Tool(
            name="greet",
            description="Generate a greeting message",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name to greet"
                    }
                },
                "required": ["name"]
            }
        ),
        lambda args: TextContent(text=f"Hello, {args['name']}! Welcome to MCP.")
    )
    
    # Register a calculator tool
    server.register_tool(
        Tool(
            name="calculate",
            description="Perform basic arithmetic",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    },
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
    
    return server


def simulate_mcp_session():
    """Simulate an MCP session with requests and responses."""
    
    server = create_demo_server()
    
    print("=" * 70)
    print("MCP Simple Server Demo")
    print("=" * 70)
    
    # 1. Initialize
    print("\n📡 Request: initialize")
    print("-" * 50)
    response = server.handle_request({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "Demo Client", "version": "1.0.0"}
        },
        "id": 1
    })
    print(json.dumps(response, indent=2))
    
    # 2. List tools
    print("\n📋 Request: tools/list")
    print("-" * 50)
    response = server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    })
    print(json.dumps(response, indent=2))
    
    # 3. Call greet tool
    print("\n🔧 Request: tools/call (greet)")
    print("-" * 50)
    response = server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "greet",
            "arguments": {"name": "Developer"}
        },
        "id": 3
    })
    print(json.dumps(response, indent=2))
    
    # 4. Call calculate tool
    print("\n🔧 Request: tools/call (calculate)")
    print("-" * 50)
    response = server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "calculate",
            "arguments": {"operation": "multiply", "a": 7, "b": 6}
        },
        "id": 4
    })
    print(json.dumps(response, indent=2))
    
    print("\n" + "=" * 70)
    print("✅ MCP session complete!")


if __name__ == "__main__":
    simulate_mcp_session()
