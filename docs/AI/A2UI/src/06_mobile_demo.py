"""
A2UI Example 06: Mobile Demo
============================
Demonstrates A2UI component generation for mobile platforms.

This example shows how to:
1. Generate mobile-optimized components (touch-friendly sizing)
2. Use mobile-specific components (BottomSheet, SwipeableRow)
3. Implement mobile navigation patterns (tab bars, bottom nav)
4. Create pull-to-refresh enabled lists
"""

import json
from typing import Optional


class MobileA2UIGenerator:
    """
    A2UI generator optimized for mobile platforms.
    
    Generates components with mobile-specific properties and patterns.
    """
    
    def __init__(self, platform: str = "react-native", surface_id: Optional[str] = None):
        self.platform = platform  # "react-native" or "flutter"
        self.surface_id = surface_id
        self.messages: list[str] = []
        
    def _emit(self, message: dict):
        """Emit a JSONL message."""
        self.messages.append(json.dumps(message))
        
    def add_component(self, id: str, component_type: str, props: dict) -> "MobileA2UIGenerator":
        """Add a component to the surface."""
        message = {
            "surfaceUpdate": {
                "components": [{
                    "id": id,
                    "component": {component_type: props}
                }]
            }
        }
        if self.surface_id:
            message["surfaceUpdate"]["surfaceId"] = self.surface_id
        self._emit(message)
        return self
    
    # Standard Components (Mobile-Optimized)
    
    def add_text(self, id: str, text: str, usage_hint: str = "body") -> "MobileA2UIGenerator":
        """Add a Text component with mobile-appropriate styling."""
        return self.add_component(id, "Text", {
            "text": {"literalString": text},
            "usageHint": usage_hint
        })
    
    def add_button(self, id: str, label: str, action: str, 
                   style: str = "primary", full_width: bool = False) -> "MobileA2UIGenerator":
        """Add a touch-friendly Button component."""
        props = {
            "label": {"literalString": label},
            "action": {"name": action},
            "style": style
        }
        if full_width:
            props["fullWidth"] = True
        return self.add_component(id, "Button", props)
    
    def add_column(self, id: str, children: list[str], 
                   alignment: str = "start", padding: str = "medium") -> "MobileA2UIGenerator":
        """Add a Column with mobile-friendly padding."""
        return self.add_component(id, "Column", {
            "children": {"explicitList": children},
            "alignment": alignment,
            "padding": padding
        })
    
    def add_row(self, id: str, children: list[str], 
                alignment: str = "center", spacing: str = "medium") -> "MobileA2UIGenerator":
        """Add a Row layout."""
        return self.add_component(id, "Row", {
            "children": {"explicitList": children},
            "alignment": alignment,
            "spacing": spacing
        })
    
    def add_card(self, id: str, child: str, elevation: str = "medium") -> "MobileA2UIGenerator":
        """Add a Card with elevation."""
        return self.add_component(id, "Card", {
            "child": child,
            "elevation": elevation
        })
    
    def add_image(self, id: str, url: str, alt: str = "", fit: str = "cover") -> "MobileA2UIGenerator":
        """Add an Image component."""
        props = {
            "url": {"literalString": url},
            "fit": fit
        }
        if alt:
            props["alt"] = {"literalString": alt}
        return self.add_component(id, "Image", props)
    
    # Mobile-Specific Components
    
    def add_bottom_sheet(self, id: str, child: str, 
                         snap_points: list[str] = None,
                         initial_snap: int = 1,
                         dismissible: bool = True) -> "MobileA2UIGenerator":
        """Add a BottomSheet component for modal content."""
        return self.add_component(id, "BottomSheet", {
            "child": child,
            "snapPoints": snap_points or ["25%", "50%", "90%"],
            "initialSnap": initial_snap,
            "dismissible": dismissible
        })
    
    def add_swipeable_row(self, id: str, child: str,
                          left_actions: list[str] = None,
                          right_actions: list[str] = None) -> "MobileA2UIGenerator":
        """Add a SwipeableRow with swipe actions."""
        props = {"child": child}
        if left_actions:
            props["leftActions"] = {"explicitList": left_actions}
        if right_actions:
            props["rightActions"] = {"explicitList": right_actions}
        return self.add_component(id, "SwipeableRow", props)
    
    def add_fab(self, id: str, icon: str, action: str,
                position: str = "bottomRight") -> "MobileA2UIGenerator":
        """Add a FloatingActionButton."""
        return self.add_component(id, "FloatingActionButton", {
            "icon": {"literalString": icon},
            "action": {"name": action},
            "position": position
        })
    
    def add_pull_to_refresh(self, id: str, child: str, 
                            action: str = "refresh") -> "MobileA2UIGenerator":
        """Wrap content with PullToRefresh."""
        return self.add_component(id, "PullToRefresh", {
            "child": child,
            "action": {"name": action}
        })
    
    def add_tab_bar(self, id: str, tabs: list[dict]) -> "MobileA2UIGenerator":
        """Add a TabBar for mobile navigation.
        
        tabs: [{"label": "Home", "icon": "home", "content": "home_content"}]
        """
        return self.add_component(id, "TabBar", {
            "tabs": tabs
        })
    
    # Data & Rendering
    
    def set_data(self, data: dict) -> "MobileA2UIGenerator":
        """Set the data model."""
        message = {"dataModelUpdate": {"contents": data}}
        if self.surface_id:
            message["dataModelUpdate"]["surfaceId"] = self.surface_id
        self._emit(message)
        return self
    
    def begin_rendering(self, root_id: str) -> "MobileA2UIGenerator":
        """Signal to begin rendering."""
        message = {"beginRendering": {"root": root_id}}
        if self.surface_id:
            message["beginRendering"]["surfaceId"] = self.surface_id
        self._emit(message)
        return self
    
    def to_jsonl(self) -> str:
        """Get JSONL output."""
        return "\n".join(self.messages)
    
    def print_stream(self):
        """Print the message stream."""
        for msg in self.messages:
            print(msg)


# =============================================================================
# Example: Mobile Task List App
# =============================================================================

def create_mobile_task_list():
    """
    Creates a mobile-optimized task list with:
    - Pull-to-refresh
    - Swipeable task rows (delete on swipe)
    - Floating action button to add tasks
    - Bottom sheet for task details
    
    UI Structure:
    
    root (Column)
    ├── header (Row)
    │   └── title (Text)
    ├── refresh_wrapper (PullToRefresh)
    │   └── task_list (Column)
    │       ├── task_row_1 (SwipeableRow)
    │       ├── task_row_2 (SwipeableRow)
    │       └── task_row_3 (SwipeableRow)
    ├── add_fab (FloatingActionButton)
    └── detail_sheet (BottomSheet)
    """
    
    gen = MobileA2UIGenerator(platform="react-native")
    
    # Root structure
    gen.add_column("root", ["header", "refresh_wrapper", "add_fab"])
    
    # Header
    gen.add_row("header", ["title"], alignment="center")
    gen.add_text("title", "📋 My Tasks", usage_hint="h1")
    
    # Pull-to-refresh wrapper
    gen.add_pull_to_refresh("refresh_wrapper", "task_list", action="refresh_tasks")
    
    # Task list
    gen.add_column("task_list", ["task_row_1", "task_row_2", "task_row_3"])
    
    # Swipeable task rows
    for i in range(1, 4):
        # Delete action (revealed on swipe)
        gen.add_button(f"delete_action_{i}", "🗑️ Delete", f"delete_task_{i}", style="danger")
        
        # Task card content
        gen.add_card(f"task_card_{i}", f"task_content_{i}")
        gen.add_column(f"task_content_{i}", [f"task_title_{i}", f"task_due_{i}"])
        gen.add_text(f"task_title_{i}", f"Task {i}: Complete mobile demo", usage_hint="h3")
        gen.add_text(f"task_due_{i}", "Due: Tomorrow", usage_hint="caption")
        
        # Wrap in swipeable row
        gen.add_swipeable_row(
            f"task_row_{i}",
            f"task_card_{i}",
            right_actions=[f"delete_action_{i}"]
        )
    
    # Floating action button
    gen.add_fab("add_fab", "plus", "add_task")
    
    # Data model
    gen.set_data({
        "tasks": [
            {"id": 1, "title": "Complete mobile demo", "done": False},
            {"id": 2, "title": "Review A2UI docs", "done": True},
            {"id": 3, "title": "Test on device", "done": False}
        ]
    })
    
    gen.begin_rendering("root")
    return gen


# =============================================================================
# Example: Mobile Navigation with Tabs
# =============================================================================

def create_mobile_tab_navigation():
    """
    Creates a mobile app with bottom tab navigation.
    
    UI Structure:
    
    root (Column)
    └── tab_nav (TabBar)
        ├── Tab: Home → home_content
        ├── Tab: Search → search_content
        └── Tab: Profile → profile_content
    """
    
    gen = MobileA2UIGenerator(platform="flutter")
    
    # Root with tab bar
    gen.add_column("root", ["tab_nav"])
    
    # Tab bar with navigation
    gen.add_tab_bar("tab_nav", [
        {"label": "Home", "icon": "home", "content": "home_content"},
        {"label": "Search", "icon": "search", "content": "search_content"},
        {"label": "Profile", "icon": "person", "content": "profile_content"}
    ])
    
    # Home tab content
    gen.add_column("home_content", ["home_header", "home_cards"])
    gen.add_text("home_header", "Welcome Back!", usage_hint="h1")
    gen.add_column("home_cards", ["recent_card", "featured_card"])
    gen.add_card("recent_card", "recent_content")
    gen.add_text("recent_content", "Your recent activity", usage_hint="body")
    gen.add_card("featured_card", "featured_content")
    gen.add_text("featured_content", "Featured items", usage_hint="body")
    
    # Search tab content
    gen.add_column("search_content", ["search_input", "search_results"])
    gen.add_component("search_input", "TextField", {
        "label": {"literalString": "Search"},
        "placeholder": {"literalString": "Type to search..."},
        "action": {"name": "search"}
    })
    gen.add_text("search_results", "Search results will appear here", usage_hint="caption")
    
    # Profile tab content
    gen.add_column("profile_content", ["avatar_row", "profile_name", "settings_btn"])
    gen.add_row("avatar_row", ["avatar_image"], alignment="center")
    gen.add_image("avatar_image", "https://example.com/avatar.jpg", "Profile photo")
    gen.add_text("profile_name", "John Doe", usage_hint="h2")
    gen.add_button("settings_btn", "⚙️ Settings", "open_settings", full_width=True)
    
    gen.set_data({})
    gen.begin_rendering("root")
    return gen


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("A2UI Mobile Demo Examples")
    print("=" * 70)
    
    print("\n📱 Example 1: Mobile Task List with Swipeable Rows")
    print("-" * 70)
    task_gen = create_mobile_task_list()
    task_gen.print_stream()
    print(f"\nTotal messages: {len(task_gen.messages)}")
    
    print("\n" + "=" * 70)
    
    print("\n📱 Example 2: Tab Navigation App")
    print("-" * 70)
    tab_gen = create_mobile_tab_navigation()
    tab_gen.print_stream()
    print(f"\nTotal messages: {len(tab_gen.messages)}")
    
    print("\n" + "=" * 70)
    print("\nThese JSONL streams can be consumed by:")
    print("  • React Native A2UI renderer")
    print("  • Flutter A2UI renderer")
    print("\nMobile-specific components used:")
    print("  • PullToRefresh - Native pull gesture")
    print("  • SwipeableRow - Swipe actions (iOS/Android)")
    print("  • FloatingActionButton - Material FAB")
    print("  • TabBar - Bottom navigation")
