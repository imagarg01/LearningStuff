"""
A2UI Example 01: Basic Agent
============================
Demonstrates generating simple A2UI JSONL messages.

This example shows how to:
1. Create A2UI component structures
2. Generate JSONL output
3. Build a simple profile card UI
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum


# =============================================================================
# A2UI Message Types
# =============================================================================

class UsageHint(str, Enum):
    """Text styling hints for the client renderer."""
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    BODY = "body"
    CAPTION = "caption"


@dataclass
class LiteralString:
    """A literal string value (not data-bound)."""
    literalString: str


@dataclass
class BoundPath:
    """A data-bound value referencing data model."""
    path: str


@dataclass 
class ExplicitList:
    """Explicit list of child component IDs."""
    explicitList: list[str]


# =============================================================================
# Component Definitions
# =============================================================================

@dataclass
class TextComponent:
    """A2UI Text component for displaying text."""
    text: LiteralString | BoundPath
    usageHint: Optional[str] = None


@dataclass
class ButtonComponent:
    """A2UI Button component for user actions."""
    label: LiteralString | BoundPath
    action: dict = field(default_factory=dict)
    style: Optional[str] = None


@dataclass
class ColumnComponent:
    """A2UI Column component for vertical layout."""
    children: ExplicitList
    alignment: Optional[str] = None


@dataclass
class RowComponent:
    """A2UI Row component for horizontal layout."""
    children: ExplicitList
    alignment: Optional[str] = None
    spacing: Optional[str] = None


@dataclass
class CardComponent:
    """A2UI Card container component."""
    child: str  # ID of child component
    elevation: Optional[str] = None


@dataclass
class ImageComponent:
    """A2UI Image component."""
    url: LiteralString | BoundPath
    alt: Optional[LiteralString] = None


# =============================================================================
# A2UI Messages
# =============================================================================

@dataclass
class ComponentDef:
    """A single component definition."""
    id: str
    component: dict


@dataclass
class SurfaceUpdate:
    """surfaceUpdate message for adding/updating components."""
    components: list[ComponentDef]
    surfaceId: Optional[str] = None


@dataclass
class DataModelUpdate:
    """dataModelUpdate message for updating data."""
    contents: dict
    surfaceId: Optional[str] = None


@dataclass
class BeginRendering:
    """beginRendering message to signal render start."""
    root: str
    surfaceId: Optional[str] = None
    catalog: Optional[str] = None


# =============================================================================
# A2UI Generator
# =============================================================================

class A2UIGenerator:
    """
    Simple A2UI message generator.
    
    Generates JSONL (newline-delimited JSON) messages for A2UI clients.
    """
    
    def __init__(self, surface_id: Optional[str] = None):
        self.surface_id = surface_id
        self.messages: list[str] = []
        
    def _to_dict(self, obj: Any) -> dict:
        """Convert dataclass to dict, filtering None values."""
        if hasattr(obj, '__dataclass_fields__'):
            result = {}
            for key, value in asdict(obj).items():
                if value is not None:
                    result[key] = value
            return result
        return obj
    
    def add_component(self, id: str, component_type: str, props: dict) -> "A2UIGenerator":
        """Add a component to the surface."""
        component_def = {
            "id": id,
            "component": {component_type: self._to_dict(props) if hasattr(props, '__dataclass_fields__') else props}
        }
        
        message = {"surfaceUpdate": {"components": [component_def]}}
        if self.surface_id:
            message["surfaceUpdate"]["surfaceId"] = self.surface_id
            
        self.messages.append(json.dumps(message))
        return self
    
    def add_text(self, id: str, text: str, usage_hint: Optional[str] = None) -> "A2UIGenerator":
        """Add a Text component."""
        props = {"text": {"literalString": text}}
        if usage_hint:
            props["usageHint"] = usage_hint
        return self.add_component(id, "Text", props)
    
    def add_button(self, id: str, label: str, action_name: str, style: str = "primary") -> "A2UIGenerator":
        """Add a Button component."""
        props = {
            "label": {"literalString": label},
            "action": {"name": action_name},
            "style": style
        }
        return self.add_component(id, "Button", props)
    
    def add_column(self, id: str, children: list[str], alignment: str = "start") -> "A2UIGenerator":
        """Add a Column layout component."""
        props = {
            "children": {"explicitList": children},
            "alignment": alignment
        }
        return self.add_component(id, "Column", props)
    
    def add_row(self, id: str, children: list[str], alignment: str = "center") -> "A2UIGenerator":
        """Add a Row layout component."""
        props = {
            "children": {"explicitList": children},
            "alignment": alignment
        }
        return self.add_component(id, "Row", props)
    
    def add_card(self, id: str, child_id: str, elevation: str = "medium") -> "A2UIGenerator":
        """Add a Card container component."""
        props = {
            "child": child_id,
            "elevation": elevation
        }
        return self.add_component(id, "Card", props)
    
    def add_image(self, id: str, url: str, alt: Optional[str] = None) -> "A2UIGenerator":
        """Add an Image component."""
        props = {"url": {"literalString": url}}
        if alt:
            props["alt"] = {"literalString": alt}
        return self.add_component(id, "Image", props)
    
    def set_data(self, data: dict) -> "A2UIGenerator":
        """Send a dataModelUpdate message."""
        message = {"dataModelUpdate": {"contents": data}}
        if self.surface_id:
            message["dataModelUpdate"]["surfaceId"] = self.surface_id
        self.messages.append(json.dumps(message))
        return self
    
    def begin_rendering(self, root_id: str) -> "A2UIGenerator":
        """Send the beginRendering message."""
        message = {"beginRendering": {"root": root_id}}
        if self.surface_id:
            message["beginRendering"]["surfaceId"] = self.surface_id
        self.messages.append(json.dumps(message))
        return self
    
    def to_jsonl(self) -> str:
        """Get the JSONL output (newline-separated JSON)."""
        return "\n".join(self.messages)
    
    def print_stream(self):
        """Print messages as they would be streamed."""
        for msg in self.messages:
            print(msg)


# =============================================================================
# Example: Create a Profile Card
# =============================================================================

def create_profile_card():
    """
    Creates a simple profile card UI demonstrating A2UI basics.
    
    UI Structure:
    
    root (Column)
    └── profile_card (Card)
        └── card_content (Column)
            ├── header_row (Row)
            │   ├── avatar (Image)
            │   └── name_column (Column)
            │       ├── name_text (Text)
            │       └── handle_text (Text)
            ├── bio_text (Text)
            └── actions_row (Row)
                ├── follow_btn (Button)
                └── message_btn (Button)
    """
    
    generator = A2UIGenerator()
    
    # Build from root to leaves (order matters for streaming)
    generator.add_column("root", ["profile_card"])
    generator.add_card("profile_card", "card_content")
    generator.add_column("card_content", ["header_row", "bio_text", "actions_row"])
    
    # Header with avatar and name
    generator.add_row("header_row", ["avatar", "name_column"], alignment="center")
    generator.add_image("avatar", "https://example.com/avatar.jpg", alt="User avatar")
    generator.add_column("name_column", ["name_text", "handle_text"], alignment="start")
    generator.add_text("name_text", "Alice Johnson", usage_hint="h3")
    generator.add_text("handle_text", "@alice_dev", usage_hint="caption")
    
    # Bio
    generator.add_text("bio_text", "Building the future with A2UI 🚀")
    
    # Action buttons
    generator.add_row("actions_row", ["follow_btn", "message_btn"], alignment="center")
    generator.add_button("follow_btn", "Follow", "follow_user", style="primary")
    generator.add_button("message_btn", "Message", "send_message", style="secondary")
    
    # Add empty data model and signal rendering
    generator.set_data({})
    generator.begin_rendering("root")
    
    return generator


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("A2UI Basic Agent Example")
    print("=" * 60)
    print()
    print("Generating Profile Card UI...")
    print()
    print("JSONL Stream Output:")
    print("-" * 60)
    
    generator = create_profile_card()
    generator.print_stream()
    
    print("-" * 60)
    print()
    print(f"Total messages: {len(generator.messages)}")
    print()
    print("This JSONL stream would be sent to an A2UI client,")
    print("which renders each component using its native widget library.")
