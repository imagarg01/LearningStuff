"""
A2UI Example 03: Event Handling
===============================
Demonstrates handling user interactions in A2UI.

This example shows how to:
1. Define actions on interactive components
2. Handle userAction events from clients
3. Update UI in response to user interactions
"""

import json
from typing import Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum


# =============================================================================
# Event Types
# =============================================================================

class ActionType(str, Enum):
    """Common action types in A2UI."""
    CLICK = "click"
    SUBMIT = "submit"
    CHANGE = "change"
    SELECT = "select"


@dataclass
class UserAction:
    """
    Represents a userAction message from the client.
    
    This is what the client sends when a user interacts with a component.
    """
    surface_id: str
    action_name: str
    component_id: str
    data: dict = field(default_factory=dict)
    
    @classmethod
    def from_json(cls, json_str: str) -> "UserAction":
        """Parse a userAction message from JSON."""
        msg = json.loads(json_str)
        action = msg.get("userAction", {})
        return cls(
            surface_id=action.get("surfaceId", "main"),
            action_name=action.get("action", {}).get("name", ""),
            component_id=action.get("action", {}).get("componentId", ""),
            data=action.get("data", {})
        )


@dataclass
class ClientError:
    """
    Represents an error message from the client.
    """
    surface_id: str
    code: str
    message: str
    details: dict = field(default_factory=dict)
    
    @classmethod
    def from_json(cls, json_str: str) -> "ClientError":
        """Parse an error message from JSON."""
        msg = json.loads(json_str)
        error = msg.get("error", {})
        return cls(
            surface_id=error.get("surfaceId", "main"),
            code=error.get("code", "UNKNOWN"),
            message=error.get("message", ""),
            details=error.get("details", {})
        )


# =============================================================================
# A2UI Agent with Event Handling
# =============================================================================

class A2UIInteractiveAgent:
    """
    An A2UI agent that handles user interactions.
    
    Demonstrates the event loop:
    1. Agent sends UI
    2. User interacts (clicks, types, etc.)
    3. Client sends userAction
    4. Agent processes and responds with updated UI
    """
    
    def __init__(self):
        self.messages: list[str] = []
        self.handlers: dict[str, Callable] = {}
        self.state: dict = {}
    
    def _emit(self, message: dict):
        """Add a message to the output stream."""
        self.messages.append(json.dumps(message))
    
    def clear_messages(self):
        """Clear the message buffer."""
        self.messages = []
    
    # =========================================================================
    # Component Generation
    # =========================================================================
    
    def add_component(self, id: str, component_type: str, props: dict):
        """Add a component to the surface."""
        self._emit({
            "surfaceUpdate": {
                "components": [{"id": id, "component": {component_type: props}}]
            }
        })
    
    def add_button(self, id: str, label: str, action_name: str, 
                   style: str = "primary", disabled: bool = False):
        """
        Add a Button with an action.
        
        The `action_name` is what gets sent back in userAction.
        """
        props = {
            "label": {"literalString": label},
            "action": {"name": action_name},
            "style": style
        }
        if disabled:
            props["disabled"] = {"literalString": "true"}
        self.add_component(id, "Button", props)
    
    def add_text_field(self, id: str, label: str, placeholder: str,
                       action_name: str, value_path: str = None):
        """
        Add a TextField with change action.
        
        When user types, client sends userAction with new value.
        """
        props = {
            "label": {"literalString": label},
            "placeholder": {"literalString": placeholder},
            "action": {"name": action_name}
        }
        if value_path:
            props["value"] = {"path": value_path}
        self.add_component(id, "TextField", props)
    
    def add_checkbox(self, id: str, label: str, action_name: str, 
                     checked_path: str = None):
        """Add a Checkbox with toggle action."""
        props = {
            "label": {"literalString": label},
            "action": {"name": action_name}
        }
        if checked_path:
            props["checked"] = {"path": checked_path}
        self.add_component(id, "Checkbox", props)
    
    def add_text(self, id: str, text: str, hint: str = None):
        """Add static text."""
        props = {"text": {"literalString": text}}
        if hint:
            props["usageHint"] = hint
        self.add_component(id, "Text", props)
    
    def add_text_bound(self, id: str, path: str, hint: str = None):
        """Add data-bound text."""
        props = {"text": {"path": path}}
        if hint:
            props["usageHint"] = hint
        self.add_component(id, "Text", props)
    
    def add_column(self, id: str, children: list[str]):
        """Add a Column layout."""
        self.add_component(id, "Column", {
            "children": {"explicitList": children}
        })
    
    def add_row(self, id: str, children: list[str]):
        """Add a Row layout."""
        self.add_component(id, "Row", {
            "children": {"explicitList": children}
        })
    
    def add_card(self, id: str, child_id: str):
        """Add a Card container."""
        self.add_component(id, "Card", {"child": child_id})
    
    def set_data(self, data: dict):
        """Update the data model."""
        self._emit({"dataModelUpdate": {"contents": data}})
    
    def begin_rendering(self, root_id: str):
        """Signal rendering can begin."""
        self._emit({"beginRendering": {"root": root_id}})
    
    # =========================================================================
    # Event Handling
    # =========================================================================
    
    def on(self, action_name: str, handler: Callable[[UserAction], None]):
        """
        Register a handler for an action.
        
        Example:
            agent.on("submit_form", self.handle_submit)
        """
        self.handlers[action_name] = handler
    
    def handle_event(self, event_json: str) -> list[str]:
        """
        Process an incoming event from the client.
        
        Returns the response messages to send back.
        """
        self.clear_messages()
        
        # Parse the event
        data = json.loads(event_json)
        
        if "userAction" in data:
            action = UserAction.from_json(event_json)
            handler = self.handlers.get(action.action_name)
            
            if handler:
                handler(action)
            else:
                print(f"⚠️ No handler for action: {action.action_name}")
        
        elif "error" in data:
            error = ClientError.from_json(event_json)
            print(f"❌ Client error: {error.code} - {error.message}")
        
        return self.messages
    
    def print_stream(self):
        """Print the current message stream."""
        for msg in self.messages:
            print(msg)


# =============================================================================
# Demo: Counter App
# =============================================================================

def demo_counter():
    """
    Simple counter app demonstrating event handling.
    """
    
    print("=" * 70)
    print("Demo 1: Counter App")
    print("=" * 70)
    
    agent = A2UIInteractiveAgent()
    agent.state["count"] = 0
    
    # -------------------------------------------------------------------------
    # Define event handlers
    # -------------------------------------------------------------------------
    
    def handle_increment(action: UserAction):
        """Handler for increment button."""
        agent.state["count"] += 1
        print(f"  ➕ Incremented to {agent.state['count']}")
        # Send updated data
        agent.set_data({"count": agent.state["count"]})
    
    def handle_decrement(action: UserAction):
        """Handler for decrement button."""
        agent.state["count"] -= 1
        print(f"  ➖ Decremented to {agent.state['count']}")
        agent.set_data({"count": agent.state["count"]})
    
    def handle_reset(action: UserAction):
        """Handler for reset button."""
        agent.state["count"] = 0
        print(f"  🔄 Reset to 0")
        agent.set_data({"count": 0})
    
    # Register handlers
    agent.on("increment", handle_increment)
    agent.on("decrement", handle_decrement)
    agent.on("reset", handle_reset)
    
    # -------------------------------------------------------------------------
    # Build initial UI
    # -------------------------------------------------------------------------
    
    print("\n📦 Building Counter UI...")
    
    agent.add_column("root", ["counter_card"])
    agent.add_card("counter_card", "card_content")
    agent.add_column("card_content", ["title", "count_display", "button_row", "reset_btn"])
    
    agent.add_text("title", "Counter", hint="h1")
    agent.add_text_bound("count_display", "count", hint="h2")  # Bound to data
    
    agent.add_row("button_row", ["dec_btn", "inc_btn"])
    agent.add_button("dec_btn", "−", "decrement", style="secondary")
    agent.add_button("inc_btn", "+", "increment", style="primary")
    agent.add_button("reset_btn", "Reset", "reset", style="danger")
    
    # Initial data
    agent.set_data({"count": agent.state["count"]})
    agent.begin_rendering("root")
    
    print("\nInitial JSONL stream:")
    print("-" * 70)
    agent.print_stream()
    
    # -------------------------------------------------------------------------
    # Simulate user interactions
    # -------------------------------------------------------------------------
    
    print("\n\n🖱️ Simulating User Interactions...")
    print("-" * 70)
    
    # Simulate: User clicks + button
    print("\n[User clicks '+' button]")
    response = agent.handle_event(json.dumps({
        "userAction": {
            "surfaceId": "main",
            "action": {"name": "increment", "componentId": "inc_btn"},
            "data": {}
        }
    }))
    print("Response to client:")
    for msg in response:
        print(f"  {msg}")
    
    # Simulate: User clicks + again
    print("\n[User clicks '+' button again]")
    response = agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "increment", "componentId": "inc_btn"}
        }
    }))
    print("Response to client:")
    for msg in response:
        print(f"  {msg}")
    
    # Simulate: User clicks reset
    print("\n[User clicks 'Reset' button]")
    response = agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "reset", "componentId": "reset_btn"}
        }
    }))
    print("Response to client:")
    for msg in response:
        print(f"  {msg}")


# =============================================================================
# Demo: Form with Validation
# =============================================================================

def demo_form():
    """
    Form with input validation demonstrating complex event handling.
    """
    
    print("\n\n" + "=" * 70)
    print("Demo 2: Contact Form with Validation")
    print("=" * 70)
    
    agent = A2UIInteractiveAgent()
    agent.state = {
        "name": "",
        "email": "",
        "message": "",
        "errors": {},
        "submitted": False
    }
    
    # -------------------------------------------------------------------------
    # Event handlers
    # -------------------------------------------------------------------------
    
    def handle_field_change(action: UserAction):
        """Handle form field changes."""
        field = action.data.get("field", "")
        value = action.data.get("value", "")
        agent.state[field] = value
        
        # Clear error when user types
        if field in agent.state["errors"]:
            del agent.state["errors"][field]
            agent.set_data({"errors": agent.state["errors"]})
        
        print(f"  📝 Field '{field}' changed to: '{value}'")
    
    def handle_submit(action: UserAction):
        """Handle form submission with validation."""
        print("  📤 Form submitted, validating...")
        
        errors = {}
        
        # Validate name
        if not agent.state["name"]:
            errors["name"] = "Name is required"
        
        # Validate email
        email = agent.state["email"]
        if not email:
            errors["email"] = "Email is required"
        elif "@" not in email:
            errors["email"] = "Invalid email format"
        
        # Validate message
        if len(agent.state["message"]) < 10:
            errors["message"] = "Message must be at least 10 characters"
        
        agent.state["errors"] = errors
        
        if errors:
            print(f"  ❌ Validation failed: {errors}")
            agent.set_data({
                "errors": errors,
                "status": "Please fix the errors above",
                "statusType": "error"
            })
        else:
            print("  ✅ Validation passed!")
            agent.state["submitted"] = True
            agent.set_data({
                "errors": {},
                "status": "Message sent successfully!",
                "statusType": "success",
                "formDisabled": True
            })
    
    # Register handlers
    agent.on("field_change", handle_field_change)
    agent.on("submit_form", handle_submit)
    
    # -------------------------------------------------------------------------
    # Build Form UI
    # -------------------------------------------------------------------------
    
    print("\n📦 Building Form UI...")
    
    agent.add_column("root", ["form_card"])
    agent.add_card("form_card", "form_content")
    agent.add_column("form_content", [
        "title",
        "name_field",
        "email_field", 
        "message_field",
        "status_text",
        "submit_btn"
    ])
    
    agent.add_text("title", "Contact Us", hint="h1")
    
    # Form fields with error binding
    agent.add_text_field("name_field", "Name", "Enter your name", "field_change")
    agent.add_text_field("email_field", "Email", "Enter your email", "field_change")
    agent.add_text_field("message_field", "Message", "Your message...", "field_change")
    
    agent.add_text_bound("status_text", "status", hint="body")
    agent.add_button("submit_btn", "Send Message", "submit_form", style="primary")
    
    agent.set_data({
        "status": "",
        "errors": {},
        "formDisabled": False
    })
    agent.begin_rendering("root")
    
    print("\nInitial form structure sent.")
    
    # -------------------------------------------------------------------------
    # Simulate form interaction
    # -------------------------------------------------------------------------
    
    print("\n\n🖱️ Simulating Form Interaction...")
    print("-" * 70)
    
    # User types name
    print("\n[User types in name field]")
    agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "field_change", "componentId": "name_field"},
            "data": {"field": "name", "value": "John Doe"}
        }
    }))
    
    # User types invalid email
    print("\n[User types invalid email]")
    agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "field_change", "componentId": "email_field"},
            "data": {"field": "email", "value": "invalid-email"}
        }
    }))
    
    # User submits form (should fail validation)
    print("\n[User clicks Submit (validation should fail)]")
    response = agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "submit_form", "componentId": "submit_btn"},
            "data": {}
        }
    }))
    print("Response to client:")
    for msg in response:
        print(f"  {msg}")
    
    # User fixes email
    print("\n[User fixes email]")
    agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "field_change", "componentId": "email_field"},
            "data": {"field": "email", "value": "john@example.com"}
        }
    }))
    
    # User adds message
    print("\n[User types message]")
    agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "field_change", "componentId": "message_field"},
            "data": {"field": "message", "value": "Hello! I have a question about A2UI."}
        }
    }))
    
    # User submits again (should succeed)
    print("\n[User clicks Submit (should succeed)]")
    response = agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "submit_form", "componentId": "submit_btn"},
            "data": {}
        }
    }))
    print("Response to client:")
    for msg in response:
        print(f"  {msg}")


if __name__ == "__main__":
    demo_counter()
    demo_form()
    
    print("\n\n" + "=" * 70)
    print("EVENT HANDLING SUMMARY")
    print("=" * 70)
    print("""
1. DEFINING ACTIONS on components:
   {"action": {"name": "button_clicked"}}

2. CLIENT SENDS userAction when user interacts:
   {"userAction": {"action": {"name": "...", "componentId": "..."}, "data": {...}}}

3. AGENT PROCESSES and responds with updated data:
   {"dataModelUpdate": {"contents": {...}}}

4. NO UI RESEND needed - just data updates!
   The bound values automatically reflect new data.
""")
