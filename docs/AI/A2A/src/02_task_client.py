"""
A2A Example 02: Task Client
===========================
Demonstrates sending tasks to A2A agents.

This example shows:
1. Creating tasks
2. Sending messages
3. Handling responses
4. Task lifecycle
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional, Any
from enum import Enum


class TaskState(Enum):
    """Task lifecycle states."""
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


@dataclass
class Part:
    """A message part."""
    type: str  # text, file, data
    text: Optional[str] = None
    data: Optional[Any] = None
    mimeType: Optional[str] = None


@dataclass
class Message:
    """An A2A message."""
    role: str  # user, agent
    parts: list[Part] = field(default_factory=list)


@dataclass
class Status:
    """Task status."""
    state: str
    message: Optional[str] = None


@dataclass
class Artifact:
    """Task output artifact."""
    name: str
    parts: list[Part] = field(default_factory=list)
    index: Optional[int] = None
    append: bool = False


@dataclass
class Task:
    """An A2A task."""
    id: str
    sessionId: Optional[str] = None
    status: Status = field(default_factory=lambda: Status(state="submitted"))
    messages: list[Message] = field(default_factory=list)
    artifacts: list[Artifact] = field(default_factory=list)
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, default=str)


class A2AClient:
    """
    A2A client for sending tasks to agents.
    
    Simulates client-side operations:
    - Task creation
    - Message sending
    - Response handling
    """
    
    def __init__(self, agent_url: str):
        self.agent_url = agent_url
        self.tasks: dict[str, Task] = {}
        self._request_id = 0
    
    def create_task(self, session_id: Optional[str] = None) -> Task:
        """Create a new task."""
        task_id = f"task_{uuid.uuid4().hex[:12]}"
        task = Task(
            id=task_id,
            sessionId=session_id or f"session_{uuid.uuid4().hex[:8]}"
        )
        self.tasks[task_id] = task
        return task
    
    def send_message(self, task_id: str, text: str) -> dict:
        """
        Send a message to continue a task.
        
        Returns the JSON-RPC request that would be sent.
        """
        self._request_id += 1
        
        return {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "params": {
                "id": task_id,
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": text}]
                }
            },
            "id": self._request_id
        }
    
    def send_with_file(self, task_id: str, text: str, 
                       file_data: str, mime_type: str) -> dict:
        """Send a message with a file attachment."""
        self._request_id += 1
        
        return {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "params": {
                "id": task_id,
                "message": {
                    "role": "user",
                    "parts": [
                        {"type": "text", "text": text},
                        {"type": "file", "mimeType": mime_type, "data": file_data}
                    ]
                }
            },
            "id": self._request_id
        }
    
    def get_task(self, task_id: str) -> dict:
        """Get task status request."""
        self._request_id += 1
        
        return {
            "jsonrpc": "2.0",
            "method": "tasks/get",
            "params": {"id": task_id},
            "id": self._request_id
        }
    
    def cancel_task(self, task_id: str) -> dict:
        """Cancel a task."""
        self._request_id += 1
        
        return {
            "jsonrpc": "2.0",
            "method": "tasks/cancel",
            "params": {"id": task_id},
            "id": self._request_id
        }
    
    def subscribe_task(self, task_id: str, text: str) -> dict:
        """Send with streaming subscription."""
        self._request_id += 1
        
        return {
            "jsonrpc": "2.0",
            "method": "tasks/sendSubscribe",
            "params": {
                "id": task_id,
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": text}]
                }
            },
            "id": self._request_id
        }


class MockA2AServer:
    """
    Mock A2A server for testing.
    
    Simulates server responses.
    """
    
    def __init__(self):
        self.tasks: dict[str, dict] = {}
    
    def handle_request(self, request: dict) -> dict:
        """Process a JSON-RPC request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        if method == "tasks/send":
            return self._handle_send(params, request_id)
        elif method == "tasks/get":
            return self._handle_get(params, request_id)
        elif method == "tasks/cancel":
            return self._handle_cancel(params, request_id)
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": "Method not found"},
                "id": request_id
            }
    
    def _handle_send(self, params: dict, request_id: int) -> dict:
        """Handle task send."""
        task_id = params["id"]
        message = params.get("message", {})
        
        # Simulate task processing
        user_text = message.get("parts", [{}])[0].get("text", "")
        
        # Create response
        response_text = f"Received: {user_text}"
        
        return {
            "jsonrpc": "2.0",
            "result": {
                "id": task_id,
                "status": {"state": "completed", "message": "Task completed"},
                "artifacts": [
                    {
                        "name": "response",
                        "parts": [{"type": "text", "text": response_text}]
                    }
                ]
            },
            "id": request_id
        }
    
    def _handle_get(self, params: dict, request_id: int) -> dict:
        """Handle task get."""
        task_id = params["id"]
        
        return {
            "jsonrpc": "2.0",
            "result": {
                "id": task_id,
                "status": {"state": "completed"}
            },
            "id": request_id
        }
    
    def _handle_cancel(self, params: dict, request_id: int) -> dict:
        """Handle task cancel."""
        task_id = params["id"]
        
        return {
            "jsonrpc": "2.0",
            "result": {
                "id": task_id,
                "status": {"state": "canceled"}
            },
            "id": request_id
        }


# =============================================================================
# Demo
# =============================================================================

def run_demo():
    """Demonstrate A2A client operations."""
    
    client = A2AClient("https://agent.example.com/a2a")
    server = MockA2AServer()
    
    print("=" * 70)
    print("A2A Task Client Demo")
    print("=" * 70)
    
    # 1. Create task
    print("\n📋 Creating new task...")
    task = client.create_task()
    print(f"  Task ID: {task.id}")
    print(f"  Session: {task.sessionId}")
    
    # 2. Send message
    print("\n📤 Sending message...")
    print("-" * 50)
    request = client.send_message(task.id, "Hello, agent!")
    print("Request:")
    print(json.dumps(request, indent=2))
    
    print("\n📥 Response:")
    response = server.handle_request(request)
    print(json.dumps(response, indent=2))
    
    # 3. Send with file
    print("\n" + "=" * 70)
    print("\n📎 Sending message with file...")
    print("-" * 50)
    request = client.send_with_file(
        task.id, 
        "Analyze this document",
        "base64encodedcontent...",
        "application/pdf"
    )
    print("Request:")
    print(json.dumps(request, indent=2))
    
    # 4. Get task status
    print("\n" + "=" * 70)
    print("\n🔍 Getting task status...")
    print("-" * 50)
    request = client.get_task(task.id)
    print("Request:")
    print(json.dumps(request, indent=2))
    
    response = server.handle_request(request)
    print("\nResponse:")
    print(json.dumps(response, indent=2))
    
    # 5. Streaming subscription
    print("\n" + "=" * 70)
    print("\n📡 Streaming subscription request...")
    print("-" * 50)
    request = client.subscribe_task(task.id, "Long running task")
    print("Request:")
    print(json.dumps(request, indent=2))
    
    print("\n" + "=" * 70)
    print("✅ A2A client demo complete!")


if __name__ == "__main__":
    run_demo()
