"""
MCP Example 04: MCP App (UI) Server
===================================
A server demonstrating how to attach a UI to a tool (MCP App).

This example shows:
1. Defining a tool with `_meta.ui.resourceUri`
2. Implementing the `resources/read` endpoint to serve HTML
3. Simulating the client/host flow of discovering and fetching the UI
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Callable

# =============================================================================
# Core MCP Server Logic (Enhanced with Resources)
# =============================================================================

@dataclass
class Tool:
    """An MCP tool definition."""
    name: str
    description: str
    inputSchema: dict
    _meta: Optional[dict] = None  # Added for MCP App support

@dataclass
class Resource:
    """An MCP resource definition."""
    uri: str
    name: str
    mimeType: str

@dataclass
class ResourceContent:
    """Content of a resource."""
    uri: str
    mimeType: str
    text: str

class MCPServer:
    """
    A simple MCP server implementation supporting Tools and Resources.
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, Tool] = {}
        self.tool_handlers: Dict[str, Callable] = {}
        self.resources: Dict[str, Resource] = {}
        self.resource_handlers: Dict[str, Callable] = {}
    
    def register_tool(self, tool: Tool, handler: Callable):
        """Register a tool with its handler."""
        self.tools[tool.name] = tool
        self.tool_handlers[tool.name] = handler

    def register_resource(self, resource: Resource, handler: Callable):
        """Register a resource with its handler."""
        self.resources[resource.uri] = resource
        self.resource_handlers[resource.uri] = handler
    
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
            elif method == "resources/list":
                result = self._handle_list_resources()
            elif method == "resources/read":
                result = self._handle_read_resource(params)
            else:
                return self._error_response(request_id, -32601, f"Unknown method: {method}")
            
            return self._success_response(request_id, result)
        
        except Exception as e:
            return self._error_response(request_id, -32000, str(e))
    
    def _handle_initialize(self, params: dict) -> dict:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {"listChanged": False},
                "resources": {"subscribe": False}
            },
            "serverInfo": {"name": self.name, "version": self.version}
        }
    
    def _handle_list_tools(self) -> dict:
        # Convert dataclass to dict, including _meta if present
        tools_list = []
        for tool in self.tools.values():
            t_dict = asdict(tool)
            # Remove _meta if it's None to keep response clean
            if t_dict["_meta"] is None:
                del t_dict["_meta"]
            tools_list.append(t_dict)
        return {"tools": tools_list}
    
    def _handle_call_tool(self, params: dict) -> dict:
        name = params.get("name")
        args = params.get("arguments", {})
        if name not in self.tool_handlers:
            raise ValueError(f"Unknown tool: {name}")
        
        result = self.tool_handlers[name](args)
        # Wrap string result in list format
        if isinstance(result, str):
            return {"content": [{"type": "text", "text": result}]}
        return {"content": result}

    def _handle_list_resources(self) -> dict:
        return {"resources": [asdict(r) for r in self.resources.values()]}

    def _handle_read_resource(self, params: dict) -> dict:
        uri = params.get("uri")
        if uri not in self.resource_handlers:
            raise ValueError(f"Unknown resource: {uri}")
        
        content = self.resource_handlers[uri]()
        return {"contents": [asdict(content)]}
    
    def _success_response(self, request_id: Any, result: Any) -> dict:
        return {"jsonrpc": "2.0", "result": result, "id": request_id}
    
    def _error_response(self, request_id: Any, code: int, message: str) -> dict:
        return {"jsonrpc": "2.0", "error": {"code": code, "message": message}, "id": request_id}


# =============================================================================
# Example Implementation: Simple UI Form via MCP App
# =============================================================================

def create_app_server():
    server = MCPServer("mcp-app-demo", "1.0.0")
    
    # 1. Define the UI Resource URI
    ui_uri = "internal://ui/feedback-form"
    
    # 2. Register the Tool with the UI link
    server.register_tool(
        Tool(
            name="submit_feedback",
            description="Submit user feedback",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": ["bug", "feature", "other"]},
                    "details": {"type": "string"}
                },
                "required": ["category", "details"]
            },
            _meta={
                "ui": {
                    "resourceUri": ui_uri
                }
            }
        ),
        lambda args: f"Received {args['category']} feedback: {args['details']}"
    )
    
    # 3. Register the Resource that provides the HTML UI
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: sans-serif; padding: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input, select, textarea { width: 100%; padding: 8px; }
            button { background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h2>Submit Feedback</h2>
        <form id="feedbackForm">
            <div class="form-group">
                <label>Category</label>
                <select name="category">
                    <option value="bug">Bug Report</option>
                    <option value="feature">Feature Request</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="form-group">
                <label>Details</label>
                <textarea name="details" rows="4"></textarea>
            </div>
            <button type="submit">Submit</button>
        </form>
        <script>
            // In a real MCP App, you would use the @mcp-ui/client library
            // to send this data back to the host.
            // client.callTool("submit_feedback", formData);
        </script>
    </body>
    </html>
    """
    
    server.register_resource(
        Resource(uri=ui_uri, name="Feedback Form UI", mimeType="text/html"),
        lambda: ResourceContent(uri=ui_uri, mimeType="text/html", text=html_content)
    )
    
    return server

def simulate_session():
    server = create_app_server()
    print("=" * 70)
    print("MCP App (UI) Demo")
    print("=" * 70)
    
    # 1. Initialize
    print("\n📡 Request: initialize")
    server.handle_request({"jsonrpc": "2.0", "method": "initialize", "id": 1})
    print("✓ Server initialized")

    # 2. List Tools (Client sees the _meta tag)
    print("\n📋 Request: tools/list")
    print("-" * 50)
    resp = server.handle_request({"jsonrpc": "2.0", "method": "tools/list", "id": 2})
    
    tools = resp["result"]["tools"]
    print(f"Server returned {len(tools)} tool(s).")
    for t in tools:
        print(f"- Tool: {t['name']}")
        if "_meta" in t:
            print(f"  Start UI at: {t['_meta']['ui']['resourceUri']}")
    
    # 3. Fetch UI (Client fetches the HTML)
    print("\n🎨 Request: resources/read (Fetch UI)")
    print("-" * 50)
    ui_uri = tools[0]["_meta"]["ui"]["resourceUri"]
    
    resp = server.handle_request({
        "jsonrpc": "2.0", 
        "method": "resources/read", 
        "params": {"uri": ui_uri},
        "id": 3
    })
    
    content = resp["result"]["contents"][0]
    print(f"Received UI Content ({content['mimeType']}):")
    print(content['text'][:150] + "... (truncated)")

    # 4. Submit Data (Simulating the UI calling the tool)
    print("\n🚀 Request: tools/call (UI submits data)")
    print("-" * 50)
    resp = server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "submit_feedback",
            "arguments": {"category": "feature", "details": "Dark mode support"}
        },
        "id": 4
    })
    print("Result:", resp["result"]["content"][0]["text"])

if __name__ == "__main__":
    simulate_session()
