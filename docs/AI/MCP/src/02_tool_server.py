"""
MCP Example 02: Tool Server
===========================
An MCP server with multiple tools and JSON Schema validation.

This example demonstrates:
1. Multiple tools with rich schemas
2. Nested input schemas
3. Tool categorization
4. Error handling
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Any
from datetime import datetime


@dataclass
class Tool:
    """MCP tool definition with JSON Schema."""
    name: str
    description: str
    inputSchema: dict


@dataclass
class TextContent:
    """Text content response."""
    type: str = "text"
    text: str = ""


class ToolServer:
    """
    MCP server focused on demonstrating tool patterns.
    
    Categories:
    - Utility tools (time, random)
    - Text tools (format, analyze)
    - Data tools (query simulation)
    """
    
    def __init__(self):
        self.name = "tool-demo-server"
        self.version = "1.0.0"
        self._register_all_tools()
    
    def _register_all_tools(self):
        """Register all available tools."""
        self.tools = {}
        
        # Utility tools
        self.tools["get_current_time"] = Tool(
            name="get_current_time",
            description="Get the current date and time",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone (e.g., UTC, America/New_York)",
                        "default": "UTC"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["iso", "human", "unix"],
                        "default": "human"
                    }
                }
            }
        )
        
        self.tools["generate_id"] = Tool(
            name="generate_id",
            description="Generate a unique identifier",
            inputSchema={
                "type": "object",
                "properties": {
                    "prefix": {
                        "type": "string",
                        "description": "Optional prefix for the ID"
                    },
                    "length": {
                        "type": "integer",
                        "minimum": 4,
                        "maximum": 32,
                        "default": 8
                    }
                }
            }
        )
        
        # Text tools
        self.tools["format_text"] = Tool(
            name="format_text",
            description="Format text with various transformations",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to format"
                    },
                    "operations": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["uppercase", "lowercase", "title", "reverse", "trim"]
                        },
                        "description": "Operations to apply in order"
                    }
                },
                "required": ["text", "operations"]
            }
        )
        
        self.tools["analyze_text"] = Tool(
            name="analyze_text",
            description="Analyze text and return statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze"
                    }
                },
                "required": ["text"]
            }
        )
        
        # Data tools
        self.tools["query_data"] = Tool(
            name="query_data",
            description="Query simulated data store",
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {
                        "type": "string",
                        "enum": ["users", "products", "orders"]
                    },
                    "filters": {
                        "type": "object",
                        "description": "Key-value filters to apply"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 10
                    }
                },
                "required": ["table"]
            }
        )
    
    def list_tools(self) -> list[dict]:
        """Return all tools."""
        return [asdict(tool) for tool in self.tools.values()]
    
    def call_tool(self, name: str, arguments: dict) -> TextContent:
        """Execute a tool and return result."""
        
        if name == "get_current_time":
            return self._handle_get_time(arguments)
        elif name == "generate_id":
            return self._handle_generate_id(arguments)
        elif name == "format_text":
            return self._handle_format_text(arguments)
        elif name == "analyze_text":
            return self._handle_analyze_text(arguments)
        elif name == "query_data":
            return self._handle_query_data(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    # Tool handlers
    
    def _handle_get_time(self, args: dict) -> TextContent:
        now = datetime.now()
        fmt = args.get("format", "human")
        
        if fmt == "iso":
            result = now.isoformat()
        elif fmt == "unix":
            result = str(int(now.timestamp()))
        else:
            result = now.strftime("%A, %B %d, %Y at %I:%M %p")
        
        return TextContent(text=result)
    
    def _handle_generate_id(self, args: dict) -> TextContent:
        import random
        import string
        
        length = args.get("length", 8)
        prefix = args.get("prefix", "")
        
        chars = string.ascii_lowercase + string.digits
        random_part = ''.join(random.choice(chars) for _ in range(length))
        
        result = f"{prefix}_{random_part}" if prefix else random_part
        return TextContent(text=result)
    
    def _handle_format_text(self, args: dict) -> TextContent:
        text = args["text"]
        operations = args["operations"]
        
        for op in operations:
            if op == "uppercase":
                text = text.upper()
            elif op == "lowercase":
                text = text.lower()
            elif op == "title":
                text = text.title()
            elif op == "reverse":
                text = text[::-1]
            elif op == "trim":
                text = text.strip()
        
        return TextContent(text=text)
    
    def _handle_analyze_text(self, args: dict) -> TextContent:
        text = args["text"]
        
        analysis = {
            "character_count": len(text),
            "word_count": len(text.split()),
            "line_count": len(text.splitlines()) or 1,
            "has_numbers": any(c.isdigit() for c in text),
            "has_uppercase": any(c.isupper() for c in text),
        }
        
        return TextContent(text=json.dumps(analysis, indent=2))
    
    def _handle_query_data(self, args: dict) -> TextContent:
        table = args["table"]
        limit = args.get("limit", 10)
        
        # Simulated data
        data = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
                {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
            ],
            "products": [
                {"id": "p1", "name": "Widget", "price": 19.99},
                {"id": "p2", "name": "Gadget", "price": 49.99},
            ],
            "orders": [
                {"id": "o1", "user_id": 1, "total": 69.98},
                {"id": "o2", "user_id": 2, "total": 19.99},
            ]
        }
        
        result = data.get(table, [])[:limit]
        return TextContent(text=json.dumps(result, indent=2))


# =============================================================================
# Demo
# =============================================================================

def run_demo():
    """Demonstrate the tool server."""
    
    server = ToolServer()
    
    print("=" * 70)
    print("MCP Tool Server Demo")
    print("=" * 70)
    
    # List all tools
    print("\n📋 Available Tools:")
    print("-" * 50)
    for tool in server.list_tools():
        print(f"  • {tool['name']}: {tool['description']}")
    
    # Call each tool
    print("\n" + "=" * 70)
    print("🔧 Tool Executions")
    print("=" * 70)
    
    # 1. Get time
    print("\n[get_current_time]")
    result = server.call_tool("get_current_time", {"format": "human"})
    print(f"  → {result.text}")
    
    # 2. Generate ID
    print("\n[generate_id]")
    result = server.call_tool("generate_id", {"prefix": "user", "length": 12})
    print(f"  → {result.text}")
    
    # 3. Format text
    print("\n[format_text]")
    result = server.call_tool("format_text", {
        "text": "  hello world  ",
        "operations": ["trim", "uppercase"]
    })
    print(f"  → {result.text}")
    
    # 4. Analyze text
    print("\n[analyze_text]")
    result = server.call_tool("analyze_text", {
        "text": "Hello World! This is a test message with 123 numbers."
    })
    print(f"  → {result.text}")
    
    # 5. Query data
    print("\n[query_data]")
    result = server.call_tool("query_data", {"table": "users", "limit": 2})
    print(f"  → {result.text}")
    
    print("\n" + "=" * 70)
    print("✅ All tools executed successfully!")


if __name__ == "__main__":
    run_demo()
