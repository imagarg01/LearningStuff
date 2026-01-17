"""
UCP Example 03: MCP Integration
===============================
Demonstrates how UCP capabilities map to MCP tools.

This example shows how to:
1. Define MCP tools that wrap UCP capabilities
2. Handle tool calls from an LLM
3. Return structured responses
"""

import json
from dataclasses import dataclass, field
from typing import Any, Callable
import uuid


# =============================================================================
# MCP Tool Definition (Simplified)
# =============================================================================

@dataclass
class MCPTool:
    """An MCP tool definition."""
    name: str
    description: str
    input_schema: dict
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }


@dataclass
class MCPToolCall:
    """An MCP tool call from an LLM."""
    id: str
    name: str
    arguments: dict


@dataclass
class MCPToolResult:
    """Result of an MCP tool call."""
    tool_call_id: str
    content: Any
    is_error: bool = False


# =============================================================================
# UCP-MCP Tool Registry
# =============================================================================

class UCPMCPServer:
    """
    MCP Server that wraps UCP capabilities as tools.
    
    In production, this would use the official MCP SDK.
    """
    
    def __init__(self, business_name: str, ucp_endpoint: str):
        self.business_name = business_name
        self.ucp_endpoint = ucp_endpoint
        self.tools: dict[str, MCPTool] = {}
        self.handlers: dict[str, Callable] = {}
        
        # Simulated checkout state
        self.checkouts: dict[str, dict] = {}
        
        # Register UCP tools
        self._register_ucp_tools()
    
    def _register_ucp_tools(self):
        """Register UCP capabilities as MCP tools."""
        
        # Create Checkout
        self.register_tool(
            MCPTool(
                name="create_checkout",
                description="Create a new checkout session for purchasing items",
                input_schema={
                    "type": "object",
                    "properties": {
                        "currency": {
                            "type": "string",
                            "description": "Currency code (e.g., USD, EUR)",
                            "default": "USD"
                        },
                        "locale": {
                            "type": "string",
                            "description": "Locale for formatting (e.g., en-US)",
                            "default": "en-US"
                        }
                    }
                }
            ),
            self._handle_create_checkout
        )
        
        # Add Items
        self.register_tool(
            MCPTool(
                name="add_checkout_items",
                description="Add items to an existing checkout session",
                input_schema={
                    "type": "object",
                    "properties": {
                        "checkout_id": {
                            "type": "string",
                            "description": "The checkout session ID"
                        },
                        "items": {
                            "type": "array",
                            "description": "Items to add to the cart",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "product_id": {"type": "string"},
                                    "quantity": {"type": "integer", "default": 1}
                                },
                                "required": ["product_id"]
                            }
                        }
                    },
                    "required": ["checkout_id", "items"]
                }
            ),
            self._handle_add_items
        )
        
        # Calculate
        self.register_tool(
            MCPTool(
                name="calculate_checkout",
                description="Calculate totals including tax and shipping",
                input_schema={
                    "type": "object",
                    "properties": {
                        "checkout_id": {
                            "type": "string",
                            "description": "The checkout session ID"
                        },
                        "shipping_postal_code": {
                            "type": "string",
                            "description": "Postal code for shipping calculation"
                        },
                        "shipping_country": {
                            "type": "string",
                            "description": "Country code (e.g., US)",
                            "default": "US"
                        }
                    },
                    "required": ["checkout_id", "shipping_postal_code"]
                }
            ),
            self._handle_calculate
        )
        
        # Complete Checkout
        self.register_tool(
            MCPTool(
                name="complete_checkout",
                description="Complete the checkout and place the order",
                input_schema={
                    "type": "object",
                    "properties": {
                        "checkout_id": {
                            "type": "string",
                            "description": "The checkout session ID"
                        },
                        "payment_method": {
                            "type": "string",
                            "description": "Payment method ID from user's wallet"
                        }
                    },
                    "required": ["checkout_id", "payment_method"]
                }
            ),
            self._handle_complete
        )
        
        # Get Checkout
        self.register_tool(
            MCPTool(
                name="get_checkout",
                description="Get the current state of a checkout session",
                input_schema={
                    "type": "object",
                    "properties": {
                        "checkout_id": {
                            "type": "string",
                            "description": "The checkout session ID"
                        }
                    },
                    "required": ["checkout_id"]
                }
            ),
            self._handle_get_checkout
        )
    
    def register_tool(self, tool: MCPTool, handler: Callable):
        """Register a tool and its handler."""
        self.tools[tool.name] = tool
        self.handlers[tool.name] = handler
    
    def list_tools(self) -> list[dict]:
        """List all available tools."""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def call_tool(self, tool_call: MCPToolCall) -> MCPToolResult:
        """Execute a tool call."""
        handler = self.handlers.get(tool_call.name)
        if not handler:
            return MCPToolResult(
                tool_call_id=tool_call.id,
                content={"error": f"Unknown tool: {tool_call.name}"},
                is_error=True
            )
        
        try:
            result = handler(tool_call.arguments)
            return MCPToolResult(
                tool_call_id=tool_call.id,
                content=result
            )
        except Exception as e:
            return MCPToolResult(
                tool_call_id=tool_call.id,
                content={"error": str(e)},
                is_error=True
            )
    
    # Tool Handlers (simulate UCP backend)
    
    def _handle_create_checkout(self, args: dict) -> dict:
        checkout_id = f"checkout_{uuid.uuid4().hex[:8]}"
        self.checkouts[checkout_id] = {
            "id": checkout_id,
            "status": "open",
            "currency": args.get("currency", "USD"),
            "items": [],
            "subtotal": 0,
            "tax": 0,
            "shipping": 0,
            "total": 0
        }
        return self.checkouts[checkout_id]
    
    def _handle_add_items(self, args: dict) -> dict:
        checkout = self.checkouts.get(args["checkout_id"])
        if not checkout:
            raise ValueError("Checkout not found")
        
        # Simulated products
        products = {
            "prod_123": {"name": "Widget", "price": 1999},
            "prod_456": {"name": "Gadget", "price": 4999}
        }
        
        for item in args["items"]:
            product = products.get(item["product_id"], {"name": "Unknown", "price": 999})
            qty = item.get("quantity", 1)
            checkout["items"].append({
                "product_id": item["product_id"],
                "name": product["name"],
                "quantity": qty,
                "unit_price": product["price"],
                "total": product["price"] * qty
            })
        
        checkout["subtotal"] = sum(i["total"] for i in checkout["items"])
        return checkout
    
    def _handle_calculate(self, args: dict) -> dict:
        checkout = self.checkouts.get(args["checkout_id"])
        if not checkout:
            raise ValueError("Checkout not found")
        
        # Simple tax calculation (8%)
        checkout["tax"] = int(checkout["subtotal"] * 0.08)
        checkout["shipping"] = 0 if checkout["subtotal"] > 5000 else 599
        checkout["total"] = checkout["subtotal"] + checkout["tax"] + checkout["shipping"]
        
        return checkout
    
    def _handle_complete(self, args: dict) -> dict:
        checkout = self.checkouts.get(args["checkout_id"])
        if not checkout:
            raise ValueError("Checkout not found")
        
        checkout["status"] = "completed"
        checkout["order_id"] = f"order_{uuid.uuid4().hex[:8]}"
        checkout["confirmation"] = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        
        return checkout
    
    def _handle_get_checkout(self, args: dict) -> dict:
        checkout = self.checkouts.get(args["checkout_id"])
        if not checkout:
            raise ValueError("Checkout not found")
        return checkout


# =============================================================================
# Demo: LLM Shopping Flow
# =============================================================================

def simulate_llm_shopping():
    """Simulate an LLM using UCP tools to complete a purchase."""
    
    server = UCPMCPServer("Example Store", "https://api.example.com/ucp")
    
    print("🔧 Available MCP Tools:")
    print("-" * 50)
    for tool in server.list_tools():
        print(f"  • {tool['name']}: {tool['description'][:50]}...")
    
    print("\n" + "=" * 70)
    print("🤖 Simulating LLM Shopping Flow")
    print("=" * 70)
    
    # Step 1: Create checkout
    print("\n[LLM] User wants to buy something. Creating checkout...")
    result = server.call_tool(MCPToolCall(
        id="call_1",
        name="create_checkout",
        arguments={"currency": "USD"}
    ))
    checkout_id = result.content["id"]
    print(f"[Tool] Created checkout: {checkout_id}")
    
    # Step 2: Add items
    print("\n[LLM] Adding items to cart...")
    result = server.call_tool(MCPToolCall(
        id="call_2",
        name="add_checkout_items",
        arguments={
            "checkout_id": checkout_id,
            "items": [
                {"product_id": "prod_123", "quantity": 2},
                {"product_id": "prod_456", "quantity": 1}
            ]
        }
    ))
    print(f"[Tool] Cart subtotal: ${result.content['subtotal']/100:.2f}")
    
    # Step 3: Calculate totals
    print("\n[LLM] Calculating totals for shipping to 94105...")
    result = server.call_tool(MCPToolCall(
        id="call_3",
        name="calculate_checkout",
        arguments={
            "checkout_id": checkout_id,
            "shipping_postal_code": "94105"
        }
    ))
    checkout = result.content
    print(f"[Tool] Subtotal: ${checkout['subtotal']/100:.2f}")
    print(f"[Tool] Tax: ${checkout['tax']/100:.2f}")
    print(f"[Tool] Shipping: ${checkout['shipping']/100:.2f}")
    print(f"[Tool] Total: ${checkout['total']/100:.2f}")
    
    # Step 4: Complete
    print("\n[LLM] User approved. Completing purchase...")
    result = server.call_tool(MCPToolCall(
        id="call_4",
        name="complete_checkout",
        arguments={
            "checkout_id": checkout_id,
            "payment_method": "pm_visa_123"
        }
    ))
    print(f"[Tool] Order placed! Confirmation: {result.content['confirmation']}")
    
    return result.content


if __name__ == "__main__":
    print("=" * 70)
    print("UCP-MCP Integration Demo")
    print("=" * 70)
    
    order = simulate_llm_shopping()
    
    print("\n" + "=" * 70)
    print("📋 Final Order (JSON)")
    print("=" * 70)
    print(json.dumps(order, indent=2))
