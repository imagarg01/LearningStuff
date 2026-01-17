"""
A2A Example 03: Agent Server
============================
Demonstrates a simple A2A agent server.

This example shows:
1. Agent Card serving
2. Task handling
3. Multi-skill agent
4. Response generation
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Callable
from datetime import datetime


@dataclass
class Skill:
    """Agent skill definition."""
    id: str
    name: str
    description: str


@dataclass
class AgentCard:
    """Agent identity card."""
    name: str
    description: str
    url: str
    version: str = "1.0.0"
    capabilities: dict = field(default_factory=lambda: {"streaming": False})
    skills: list[Skill] = field(default_factory=list)


class A2AAgentServer:
    """
    A simple A2A agent server implementation.
    
    Handles:
    - Agent Card requests
    - Task sending
    - Task status queries
    """
    
    def __init__(self, card: AgentCard):
        self.card = card
        self.tasks: dict[str, dict] = {}
        self.skill_handlers: dict[str, Callable] = {}
        
        # Register default handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register skill handlers based on card."""
        for skill in self.card.skills:
            # Default handler echoes
            self.skill_handlers[skill.id] = self._default_handler
    
    def register_handler(self, skill_id: str, handler: Callable):
        """Register a custom skill handler."""
        self.skill_handlers[skill_id] = handler
    
    def _default_handler(self, message: str, skill: str) -> dict:
        """Default skill handler."""
        return {
            "text": f"[{skill}] Processed: {message}"
        }
    
    def get_agent_card(self) -> dict:
        """Return the Agent Card."""
        data = asdict(self.card)
        return data
    
    def handle_request(self, request: dict) -> dict:
        """Process incoming JSON-RPC request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "agent/info":
                result = self.get_agent_card()
            elif method == "tasks/send":
                result = self._handle_task_send(params)
            elif method == "tasks/get":
                result = self._handle_task_get(params)
            elif method == "tasks/cancel":
                result = self._handle_task_cancel(params)
            else:
                return self._error(request_id, -32601, f"Unknown method: {method}")
            
            return {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            }
        
        except Exception as e:
            return self._error(request_id, -32000, str(e))
    
    def _handle_task_send(self, params: dict) -> dict:
        """Handle task send request."""
        task_id = params.get("id") or f"task_{uuid.uuid4().hex[:12]}"
        message = params.get("message", {})
        
        # Extract user message
        user_text = ""
        for part in message.get("parts", []):
            if part.get("type") == "text":
                user_text = part.get("text", "")
                break
        
        # Detect skill from message (simple keyword matching)
        detected_skill = self._detect_skill(user_text)
        
        # Process with handler
        handler = self.skill_handlers.get(detected_skill, self._default_handler)
        result = handler(user_text, detected_skill)
        
        # Store task
        task = {
            "id": task_id,
            "sessionId": params.get("sessionId"),
            "status": {"state": "completed"},
            "messages": [message],
            "artifacts": [
                {
                    "name": "response",
                    "parts": [{"type": "text", "text": result.get("text", "")}]
                }
            ]
        }
        
        # Add data artifact if present
        if "data" in result:
            task["artifacts"].append({
                "name": "data",
                "parts": [{"type": "data", "data": result["data"]}]
            })
        
        self.tasks[task_id] = task
        return task
    
    def _handle_task_get(self, params: dict) -> dict:
        """Handle task get request."""
        task_id = params.get("id")
        
        if task_id not in self.tasks:
            raise ValueError(f"Task not found: {task_id}")
        
        return self.tasks[task_id]
    
    def _handle_task_cancel(self, params: dict) -> dict:
        """Handle task cancel request."""
        task_id = params.get("id")
        
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = {"state": "canceled"}
        
        return {"id": task_id, "status": {"state": "canceled"}}
    
    def _detect_skill(self, text: str) -> str:
        """Simple skill detection based on keywords."""
        text_lower = text.lower()
        
        for skill in self.card.skills:
            # Check if skill name is mentioned
            if skill.id in text_lower or skill.name.lower() in text_lower:
                return skill.id
        
        # Return first skill as default
        return self.card.skills[0].id if self.card.skills else "default"
    
    def _error(self, request_id: int, code: int, message: str) -> dict:
        """Create error response."""
        return {
            "jsonrpc": "2.0",
            "error": {"code": code, "message": message},
            "id": request_id
        }


# =============================================================================
# Example: Weather Agent
# =============================================================================

def create_weather_agent() -> A2AAgentServer:
    """Create a weather information agent."""
    
    card = AgentCard(
        name="Weather Agent",
        description="Provides weather information and forecasts",
        url="https://weather.example.com/a2a",
        capabilities={"streaming": False, "pushNotifications": False},
        skills=[
            Skill("current_weather", "Current Weather", "Get current weather for a city"),
            Skill("forecast", "Weather Forecast", "Get weather forecast for upcoming days"),
            Skill("alerts", "Weather Alerts", "Get active weather alerts")
        ]
    )
    
    server = A2AAgentServer(card)
    
    # Custom handlers
    def handle_current_weather(message: str, skill: str) -> dict:
        # Simulate weather lookup
        return {
            "text": "Current weather in San Francisco: 72°F, Partly Cloudy",
            "data": {
                "city": "San Francisco",
                "temperature": 72,
                "unit": "fahrenheit",
                "condition": "Partly Cloudy",
                "humidity": 65
            }
        }
    
    def handle_forecast(message: str, skill: str) -> dict:
        return {
            "text": "3-day forecast for San Francisco:\n- Today: 72°F, Partly Cloudy\n- Tomorrow: 68°F, Sunny\n- Day 3: 70°F, Sunny",
            "data": {
                "city": "San Francisco",
                "forecast": [
                    {"day": "Today", "high": 72, "condition": "Partly Cloudy"},
                    {"day": "Tomorrow", "high": 68, "condition": "Sunny"},
                    {"day": "Day 3", "high": 70, "condition": "Sunny"}
                ]
            }
        }
    
    def handle_alerts(message: str, skill: str) -> dict:
        return {
            "text": "No active weather alerts for your area.",
            "data": {"alerts": []}
        }
    
    server.register_handler("current_weather", handle_current_weather)
    server.register_handler("forecast", handle_forecast)
    server.register_handler("alerts", handle_alerts)
    
    return server


# =============================================================================
# Demo
# =============================================================================

def run_demo():
    """Demonstrate A2A agent server."""
    
    server = create_weather_agent()
    
    print("=" * 70)
    print("A2A Agent Server Demo")
    print("=" * 70)
    
    # 1. Get Agent Card
    print("\n📇 Agent Card (/.well-known/agent.json)")
    print("-" * 50)
    card = server.get_agent_card()
    print(json.dumps(card, indent=2))
    
    # 2. Handle requests
    print("\n" + "=" * 70)
    print("📨 Request: Current Weather")
    print("-" * 50)
    
    request = {
        "jsonrpc": "2.0",
        "method": "tasks/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": "What's the current weather?"}]
            }
        },
        "id": 1
    }
    print("Request:")
    print(json.dumps(request, indent=2))
    
    response = server.handle_request(request)
    print("\nResponse:")
    print(json.dumps(response, indent=2))
    
    # 3. Forecast request
    print("\n" + "=" * 70)
    print("📨 Request: Weather Forecast")
    print("-" * 50)
    
    request = {
        "jsonrpc": "2.0",
        "method": "tasks/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": "Give me the forecast"}]
            }
        },
        "id": 2
    }
    response = server.handle_request(request)
    print("Response:")
    print(json.dumps(response, indent=2))
    
    # 4. Get task status
    print("\n" + "=" * 70)
    print("📨 Request: Get Task Status")
    print("-" * 50)
    
    task_id = response["result"]["id"]
    request = {
        "jsonrpc": "2.0",
        "method": "tasks/get",
        "params": {"id": task_id},
        "id": 3
    }
    response = server.handle_request(request)
    print(f"Task {task_id} status: {response['result']['status']['state']}")
    
    print("\n" + "=" * 70)
    print("✅ A2A agent server demo complete!")


if __name__ == "__main__":
    run_demo()
