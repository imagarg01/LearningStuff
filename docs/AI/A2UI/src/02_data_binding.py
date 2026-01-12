"""
A2UI Example 02: Data Binding
=============================
Demonstrates separating UI structure from data using data binding.

This example shows how to:
1. Use bound values (path references) instead of literals
2. Update data independently from components
3. Create reactive UIs that respond to data changes
"""

import json
from typing import Optional, Any


class A2UIDataBindingDemo:
    """
    Demonstrates A2UI's data binding capabilities.
    
    Key Concept: Components reference data using paths like "user.name"
    instead of hardcoded values. This allows updating data without
    resending the entire UI structure.
    """
    
    def __init__(self, surface_id: Optional[str] = None):
        self.surface_id = surface_id
        self.messages: list[str] = []
    
    def _emit(self, message: dict):
        """Add a message to the stream."""
        self.messages.append(json.dumps(message))
    
    # =========================================================================
    # Bound Values vs Literal Values
    # =========================================================================
    
    @staticmethod
    def literal(value: str) -> dict:
        """
        Create a literal (static) value.
        
        Example: The text "Submit" will always be "Submit"
        """
        return {"literalString": value}
    
    @staticmethod
    def bound(path: str) -> dict:
        """
        Create a bound (dynamic) value from data model.
        
        Example: {"path": "user.name"} will display whatever
        value is at data.user.name
        """
        return {"path": path}
    
    # =========================================================================
    # Component Generation with Binding
    # =========================================================================
    
    def add_text_literal(self, id: str, text: str, hint: str = None):
        """Add Text with a LITERAL value (static)."""
        props = {"text": self.literal(text)}
        if hint:
            props["usageHint"] = hint
        
        self._emit({
            "surfaceUpdate": {
                "components": [{"id": id, "component": {"Text": props}}]
            }
        })
    
    def add_text_bound(self, id: str, data_path: str, hint: str = None):
        """Add Text with a BOUND value (dynamic from data model)."""
        props = {"text": self.bound(data_path)}
        if hint:
            props["usageHint"] = hint
        
        self._emit({
            "surfaceUpdate": {
                "components": [{"id": id, "component": {"Text": props}}]
            }
        })
    
    def add_column(self, id: str, children: list[str]):
        """Add a Column layout."""
        self._emit({
            "surfaceUpdate": {
                "components": [{
                    "id": id,
                    "component": {
                        "Column": {
                            "children": {"explicitList": children}
                        }
                    }
                }]
            }
        })
    
    def add_card(self, id: str, child_id: str):
        """Add a Card container."""
        self._emit({
            "surfaceUpdate": {
                "components": [{
                    "id": id,
                    "component": {"Card": {"child": child_id}}
                }]
            }
        })
    
    def add_button(self, id: str, label_path: str, action: str, disabled_path: str = None):
        """Add a Button with bound label and optional disabled state."""
        props = {
            "label": self.bound(label_path),
            "action": {"name": action}
        }
        if disabled_path:
            props["disabled"] = self.bound(disabled_path)
        
        self._emit({
            "surfaceUpdate": {
                "components": [{"id": id, "component": {"Button": props}}]
            }
        })
    
    # =========================================================================
    # Data Model Management
    # =========================================================================
    
    def set_data(self, data: dict):
        """
        Send a dataModelUpdate to set/update data.
        
        This is the key to reactive updates:
        - Components bound to paths in this data will automatically update
        - No need to resend component definitions
        """
        self._emit({"dataModelUpdate": {"contents": data}})
    
    def begin_rendering(self, root_id: str):
        """Signal that rendering can begin."""
        self._emit({"beginRendering": {"root": root_id}})
    
    # =========================================================================
    # Output
    # =========================================================================
    
    def print_stream(self):
        """Print the JSONL stream."""
        for msg in self.messages:
            print(msg)
    
    def clear(self):
        """Clear messages (for demo purposes)."""
        self.messages = []


def demo_data_binding():
    """
    Demonstrates the power of data binding.
    
    Scenario: User profile that can be updated without resending UI
    """
    
    print("=" * 70)
    print("A2UI Data Binding Demonstration")
    print("=" * 70)
    
    demo = A2UIDataBindingDemo()
    
    # =========================================================================
    # Step 1: Build UI Structure (sent once)
    # =========================================================================
    
    print("\n📦 STEP 1: Build UI Structure (components reference data paths)")
    print("-" * 70)
    
    # Root layout
    demo.add_column("root", ["profile_card"])
    demo.add_card("profile_card", "card_content")
    demo.add_column("card_content", ["greeting", "user_name", "user_email", "status", "action_btn"])
    
    # Static text (literal) - won't change
    demo.add_text_literal("greeting", "Welcome,", hint="body")
    
    # Dynamic text (bound) - changes with data
    demo.add_text_bound("user_name", "user.name", hint="h2")
    demo.add_text_bound("user_email", "user.email", hint="caption")
    demo.add_text_bound("status", "user.status", hint="body")
    
    # Button with dynamic label and disabled state
    demo.add_button("action_btn", "actions.buttonLabel", "primary_action", "actions.isDisabled")
    
    print("Component structure (bound values shown as paths):")
    demo.print_stream()
    
    # =========================================================================
    # Step 2: Initial Data
    # =========================================================================
    
    print("\n\n📊 STEP 2: Set Initial Data")
    print("-" * 70)
    
    demo.clear()
    demo.set_data({
        "user": {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "status": "Online ✓"
        },
        "actions": {
            "buttonLabel": "Send Message",
            "isDisabled": False
        }
    })
    demo.begin_rendering("root")
    
    print("Initial data (UI will display these values):")
    demo.print_stream()
    
    # =========================================================================
    # Step 3: Update Only Data (UI Reacts Automatically)
    # =========================================================================
    
    print("\n\n🔄 STEP 3: Update Data Only (no components resent!)")
    print("-" * 70)
    
    demo.clear()
    demo.set_data({
        "user": {
            "name": "Bob Johnson",  # Changed!
            "email": "bob@example.com",  # Changed!
            "status": "Away 💤"  # Changed!
        },
        "actions": {
            "buttonLabel": "Leave Message",  # Changed!
            "isDisabled": False
        }
    })
    
    print("Only sending new data - components automatically update:")
    demo.print_stream()
    
    # =========================================================================
    # Step 4: Partial Update
    # =========================================================================
    
    print("\n\n✏️ STEP 4: Partial Data Update")
    print("-" * 70)
    
    demo.clear()
    demo.set_data({
        "user": {
            "status": "Busy 🔴"  # Only update status
        },
        "actions": {
            "isDisabled": True,  # Disable the button
            "buttonLabel": "User Busy"
        }
    })
    
    print("Partial update - only changed values sent:")
    demo.print_stream()


def demo_list_binding():
    """
    Demonstrates binding to lists/arrays.
    
    Template-based rendering for dynamic lists.
    """
    
    print("\n\n" + "=" * 70)
    print("List Data Binding with Templates")
    print("=" * 70)
    
    demo = A2UIDataBindingDemo()
    
    # =========================================================================
    # List with template binding
    # =========================================================================
    
    print("\n📋 Creating a list bound to data array")
    print("-" * 70)
    
    # Root structure
    demo._emit({
        "surfaceUpdate": {
            "components": [{
                "id": "root",
                "component": {
                    "Column": {
                        "children": {"explicitList": ["title", "restaurant_list"]}
                    }
                }
            }]
        }
    })
    
    # Static title
    demo.add_text_literal("title", "Nearby Restaurants", hint="h1")
    
    # List with template binding
    demo._emit({
        "surfaceUpdate": {
            "components": [{
                "id": "restaurant_list",
                "component": {
                    "List": {
                        "children": {
                            "template": {
                                "source": {"path": "restaurants"},  # Bound to data array
                                "itemId": "item",  # Variable name for each item
                                "template": "restaurant_card"  # Component to repeat
                            }
                        }
                    }
                }
            }]
        }
    })
    
    # Template for each restaurant
    demo._emit({
        "surfaceUpdate": {
            "components": [{
                "id": "restaurant_card",
                "component": {
                    "Card": {
                        "child": "restaurant_content"
                    }
                }
            }]
        }
    })
    
    demo._emit({
        "surfaceUpdate": {
            "components": [{
                "id": "restaurant_content",
                "component": {
                    "Column": {
                        "children": {"explicitList": ["restaurant_name", "restaurant_rating"]}
                    }
                }
            }]
        }
    })
    
    # In templates, paths are relative to each item
    demo._emit({
        "surfaceUpdate": {
            "components": [{
                "id": "restaurant_name",
                "component": {
                    "Text": {
                        "text": {"path": "item.name"},  # Each item's name
                        "usageHint": "h3"
                    }
                }
            }]
        }
    })
    
    demo._emit({
        "surfaceUpdate": {
            "components": [{
                "id": "restaurant_rating",
                "component": {
                    "Text": {
                        "text": {"path": "item.rating"},  # Each item's rating
                        "usageHint": "caption"
                    }
                }
            }]
        }
    })
    
    print("List template structure:")
    demo.print_stream()
    
    # =========================================================================
    # Populate with data
    # =========================================================================
    
    print("\n\n📊 Sending restaurant data")
    print("-" * 70)
    
    demo.clear()
    demo.set_data({
        "restaurants": [
            {"name": "Pasta Paradise", "rating": "⭐ 4.8"},
            {"name": "Sushi Supreme", "rating": "⭐ 4.9"},
            {"name": "Burger Barn", "rating": "⭐ 4.5"}
        ]
    })
    demo.begin_rendering("root")
    
    print("Data array - list will render 3 cards:")
    demo.print_stream()
    
    # =========================================================================
    # Update list data
    # =========================================================================
    
    print("\n\n🔄 Adding a new restaurant")
    print("-" * 70)
    
    demo.clear()
    demo.set_data({
        "restaurants": [
            {"name": "Pasta Paradise", "rating": "⭐ 4.8"},
            {"name": "Sushi Supreme", "rating": "⭐ 4.9"},
            {"name": "Burger Barn", "rating": "⭐ 4.5"},
            {"name": "Taco Town", "rating": "⭐ 4.7"}  # New!
        ]
    })
    
    print("Updated array - list automatically shows 4 cards:")
    demo.print_stream()


if __name__ == "__main__":
    demo_data_binding()
    demo_list_binding()
    
    print("\n\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
1. LITERAL VALUES: {"literalString": "Hello"}
   - Static text that never changes
   - Use for labels, headers, fixed content

2. BOUND VALUES: {"path": "user.name"}
   - Dynamic values from data model
   - Automatically update when data changes

3. EFFICIENCY:
   - Send component structure ONCE
   - Update data multiple times
   - Client handles reactivity

4. LIST TEMPLATES:
   - Define structure once
   - Bind to data array
   - Automatically renders for each item
""")
