"""
A2UI Example 05: Restaurant Finder
==================================
A complete demo inspired by Google's restaurant finder example.

This example shows a full implementation including:
1. Search form with input
2. Loading states
3. Dynamic result list
4. Interactive booking flow
5. Event handling throughout
"""

import json
import random
from typing import Optional
from dataclasses import dataclass, field


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class Restaurant:
    """Restaurant data model."""
    id: str
    name: str
    cuisine: str
    rating: float
    price_range: str
    distance: str
    image_url: str
    available_times: list[str] = field(default_factory=list)


# Sample data
RESTAURANTS = [
    Restaurant(
        id="rest_1",
        name="Pasta Paradise",
        cuisine="Italian",
        rating=4.8,
        price_range="$$",
        distance="0.3 mi",
        image_url="https://example.com/pasta.jpg",
        available_times=["6:00 PM", "7:00 PM", "8:00 PM"]
    ),
    Restaurant(
        id="rest_2", 
        name="Sushi Supreme",
        cuisine="Japanese",
        rating=4.9,
        price_range="$$$",
        distance="0.5 mi",
        image_url="https://example.com/sushi.jpg",
        available_times=["6:30 PM", "7:30 PM", "9:00 PM"]
    ),
    Restaurant(
        id="rest_3",
        name="Taco Town",
        cuisine="Mexican",
        rating=4.5,
        price_range="$",
        distance="0.8 mi",
        image_url="https://example.com/tacos.jpg",
        available_times=["5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM"]
    ),
    Restaurant(
        id="rest_4",
        name="Burger Barn",
        cuisine="American",
        rating=4.3,
        price_range="$$",
        distance="1.2 mi",
        image_url="https://example.com/burger.jpg",
        available_times=["5:30 PM", "7:30 PM"]
    ),
]


# =============================================================================
# A2UI Restaurant Agent
# =============================================================================

class RestaurantFinderAgent:
    """
    A complete A2UI agent for finding and booking restaurants.
    
    Demonstrates:
    - Multi-view navigation (search → results → booking → confirmation)
    - Form handling
    - Dynamic list rendering
    - State management
    """
    
    def __init__(self):
        self.messages: list[str] = []
        self.state = {
            "view": "search",  # search | results | booking | confirmation
            "query": "",
            "cuisine_filter": "all",
            "results": [],
            "selected_restaurant": None,
            "booking": {
                "time": None,
                "guests": 2,
                "name": "",
                "phone": ""
            }
        }
    
    def _emit(self, msg: dict):
        """Add message to stream."""
        self.messages.append(json.dumps(msg))
    
    def clear(self):
        """Clear message buffer."""
        self.messages = []
        
    def print_stream(self):
        """Print JSONL stream."""
        for msg in self.messages:
            print(msg)
    
    # =========================================================================
    # Component Helpers
    # =========================================================================
    
    def _literal(self, value: str) -> dict:
        return {"literalString": value}
    
    def _bound(self, path: str) -> dict:
        return {"path": path}
    
    def _component(self, id: str, type: str, props: dict):
        """Add a component."""
        self._emit({
            "surfaceUpdate": {
                "components": [{"id": id, "component": {type: props}}]
            }
        })
    
    def _text(self, id: str, text: str, hint: str = None):
        props = {"text": self._literal(text)}
        if hint:
            props["usageHint"] = hint
        self._component(id, "Text", props)
    
    def _text_bound(self, id: str, path: str, hint: str = None):
        props = {"text": self._bound(path)}
        if hint:
            props["usageHint"] = hint
        self._component(id, "Text", props)
    
    def _column(self, id: str, children: list[str], alignment: str = None):
        props = {"children": {"explicitList": children}}
        if alignment:
            props["alignment"] = alignment
        self._component(id, "Column", props)
    
    def _row(self, id: str, children: list[str], alignment: str = None, spacing: str = None):
        props = {"children": {"explicitList": children}}
        if alignment:
            props["alignment"] = alignment
        if spacing:
            props["spacing"] = spacing
        self._component(id, "Row", props)
    
    def _card(self, id: str, child: str, elevation: str = "medium"):
        self._component(id, "Card", {"child": child, "elevation": elevation})
    
    def _button(self, id: str, label: str, action: str, style: str = "primary"):
        self._component(id, "Button", {
            "label": self._literal(label),
            "action": {"name": action},
            "style": style
        })
    
    def _text_field(self, id: str, label: str, placeholder: str, action: str, value_path: str = None):
        props = {
            "label": self._literal(label),
            "placeholder": self._literal(placeholder),
            "action": {"name": action}
        }
        if value_path:
            props["value"] = self._bound(value_path)
        self._component(id, "TextField", props)
    
    def _dropdown(self, id: str, label: str, action: str, options_path: str, selected_path: str = None):
        props = {
            "label": self._literal(label),
            "options": self._bound(options_path),
            "action": {"name": action}
        }
        if selected_path:
            props["selected"] = self._bound(selected_path)
        self._component(id, "Dropdown", props)
    
    def _image(self, id: str, url: str, alt: str = None):
        props = {"url": self._literal(url)}
        if alt:
            props["alt"] = self._literal(alt)
        self._component(id, "Image", props)
    
    def _set_data(self, data: dict):
        self._emit({"dataModelUpdate": {"contents": data}})
    
    def _begin_render(self, root: str = "root"):
        self._emit({"beginRendering": {"root": root}})
    
    # =========================================================================
    # Views
    # =========================================================================
    
    def build_search_view(self):
        """Build the initial search form."""
        
        # Root layout
        self._column("root", ["header", "search_card"])
        
        # Header
        self._text("header", "🍽️ Restaurant Finder", hint="h1")
        
        # Search card
        self._card("search_card", "search_form")
        self._column("search_form", [
            "search_title",
            "location_field",
            "cuisine_dropdown",
            "guests_row",
            "search_btn"
        ])
        
        self._text("search_title", "Find your perfect dining spot", hint="h2")
        
        # Form fields
        self._text_field(
            "location_field", 
            "Location", 
            "Enter city or address",
            "location_change",
            "form.location"
        )
        
        self._dropdown(
            "cuisine_dropdown",
            "Cuisine Type",
            "cuisine_change",
            "cuisineOptions",
            "form.cuisine"
        )
        
        # Guests row
        self._row("guests_row", ["guests_label", "guests_minus", "guests_count", "guests_plus"], 
                  alignment="center", spacing="medium")
        self._text("guests_label", "Guests:", hint="body")
        self._button("guests_minus", "−", "decrease_guests", style="secondary")
        self._text_bound("guests_count", "form.guests", hint="h3")
        self._button("guests_plus", "+", "increase_guests", style="secondary")
        
        # Search button
        self._button("search_btn", "🔍 Search Restaurants", "search", style="primary")
        
        # Initial data
        self._set_data({
            "cuisineOptions": ["All", "Italian", "Japanese", "Mexican", "American", "Chinese", "Indian"],
            "form": {
                "location": "",
                "cuisine": "All",
                "guests": 2
            }
        })
        
        self._begin_render()
    
    def build_loading_view(self):
        """Show loading state during search."""
        
        self._column("root", ["header", "loading_card"])
        self._text("header", "🍽️ Restaurant Finder", hint="h1")
        
        self._card("loading_card", "loading_content")
        self._column("loading_content", ["loading_spinner", "loading_text"], alignment="center")
        
        self._text("loading_spinner", "⏳", hint="h1")
        self._text("loading_text", "Searching for the best restaurants...", hint="body")
        
        self._begin_render()
    
    def build_results_view(self, restaurants: list[Restaurant]):
        """Build search results view."""
        
        result_ids = [f"restaurant_{r.id}" for r in restaurants]
        
        # Root with results
        self._column("root", ["header", "results_header", "results_list", "back_btn"])
        
        self._text("header", "🍽️ Restaurant Finder", hint="h1")
        self._text_bound("results_header", "resultsTitle", hint="h2")
        
        # Results list
        self._column("results_list", result_ids)
        
        # Build each restaurant card
        for restaurant in restaurants:
            rid = f"restaurant_{restaurant.id}"
            
            self._card(rid, f"{rid}_content")
            self._row(f"{rid}_content", [f"{rid}_image", f"{rid}_info", f"{rid}_action"], 
                     alignment="center", spacing="medium")
            
            # Image
            self._image(f"{rid}_image", restaurant.image_url, alt=restaurant.name)
            
            # Info column
            self._column(f"{rid}_info", [
                f"{rid}_name",
                f"{rid}_cuisine", 
                f"{rid}_meta"
            ])
            self._text(f"{rid}_name", restaurant.name, hint="h3")
            self._text(f"{rid}_cuisine", restaurant.cuisine, hint="body")
            self._row(f"{rid}_meta", [f"{rid}_rating", f"{rid}_price", f"{rid}_distance"])
            self._text(f"{rid}_rating", f"⭐ {restaurant.rating}", hint="caption")
            self._text(f"{rid}_price", restaurant.price_range, hint="caption")
            self._text(f"{rid}_distance", restaurant.distance, hint="caption")
            
            # Book button
            self._button(f"{rid}_action", "Book", f"book_{restaurant.id}", style="primary")
        
        # Back button
        self._button("back_btn", "← New Search", "back_to_search", style="secondary")
        
        # Results data
        self._set_data({
            "resultsTitle": f"Found {len(restaurants)} restaurants",
            "restaurants": [
                {
                    "id": r.id,
                    "name": r.name,
                    "rating": r.rating,
                    "cuisine": r.cuisine
                } for r in restaurants
            ]
        })
        
        self._begin_render()
    
    def build_booking_view(self, restaurant: Restaurant):
        """Build booking form for selected restaurant."""
        
        time_btn_ids = [f"time_{i}" for i in range(len(restaurant.available_times))]
        
        self._column("root", ["header", "restaurant_header", "booking_card", "cancel_btn"])
        
        self._text("header", "🍽️ Restaurant Finder", hint="h1")
        self._text("restaurant_header", f"Booking: {restaurant.name}", hint="h2")
        
        # Booking form
        self._card("booking_card", "booking_form")
        self._column("booking_form", [
            "time_label",
            "time_row",
            "guest_info_title",
            "name_field",
            "phone_field",
            "confirm_btn"
        ])
        
        # Time selection
        self._text("time_label", "Select a time:", hint="h3")
        self._row("time_row", time_btn_ids, spacing="small")
        
        for i, time in enumerate(restaurant.available_times):
            self._button(f"time_{i}", time, f"select_time_{time.replace(':', '').replace(' ', '_')}", 
                        style="secondary")
        
        # Guest information
        self._text("guest_info_title", "Your Information", hint="h3")
        self._text_field("name_field", "Name", "Enter your name", "name_change", "booking.name")
        self._text_field("phone_field", "Phone", "Enter phone number", "phone_change", "booking.phone")
        
        # Confirm button
        self._button("confirm_btn", "✓ Confirm Booking", "confirm_booking", style="primary")
        
        # Cancel button
        self._button("cancel_btn", "← Back to Results", "back_to_results", style="secondary")
        
        self._set_data({
            "booking": {
                "restaurantName": restaurant.name,
                "time": None,
                "name": "",
                "phone": ""
            }
        })
        
        self._begin_render()
    
    def build_confirmation_view(self, restaurant_name: str, time: str, name: str):
        """Build booking confirmation view."""
        
        self._column("root", ["header", "confirmation_card", "new_search_btn"])
        
        self._text("header", "🍽️ Restaurant Finder", hint="h1")
        
        self._card("confirmation_card", "confirmation_content")
        self._column("confirmation_content", [
            "success_icon",
            "success_title",
            "booking_details",
            "confirmation_number"
        ], alignment="center")
        
        self._text("success_icon", "✅", hint="h1")
        self._text("success_title", "Booking Confirmed!", hint="h2")
        
        self._column("booking_details", [
            "detail_restaurant",
            "detail_time",
            "detail_name"
        ])
        self._text("detail_restaurant", f"Restaurant: {restaurant_name}", hint="body")
        self._text("detail_time", f"Time: {time}", hint="body")
        self._text("detail_name", f"Name: {name}", hint="body")
        
        confirmation_num = f"CONF-{random.randint(10000, 99999)}"
        self._text("confirmation_number", f"Confirmation #: {confirmation_num}", hint="h3")
        
        self._button("new_search_btn", "Search for Another Restaurant", "back_to_search", style="primary")
        
        self._set_data({
            "confirmationNumber": confirmation_num
        })
        
        self._begin_render()
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def handle_event(self, event_json: str) -> list[str]:
        """Handle incoming user action."""
        self.clear()
        
        data = json.loads(event_json)
        action = data.get("userAction", {}).get("action", {})
        action_name = action.get("name", "")
        event_data = data.get("userAction", {}).get("data", {})
        
        print(f"  📥 Action: {action_name}")
        
        if action_name == "search":
            self.handle_search()
        
        elif action_name == "back_to_search":
            self.state["view"] = "search"
            self.build_search_view()
        
        elif action_name == "back_to_results":
            self.state["view"] = "results"
            self.build_results_view(self.state["results"])
        
        elif action_name == "increase_guests":
            guests = self.state["booking"]["guests"] + 1
            self.state["booking"]["guests"] = min(guests, 20)
            self._set_data({"form": {"guests": self.state["booking"]["guests"]}})
        
        elif action_name == "decrease_guests":
            guests = self.state["booking"]["guests"] - 1
            self.state["booking"]["guests"] = max(guests, 1)
            self._set_data({"form": {"guests": self.state["booking"]["guests"]}})
        
        elif action_name.startswith("book_"):
            restaurant_id = action_name.replace("book_", "")
            self.handle_book(restaurant_id)
        
        elif action_name.startswith("select_time_"):
            time = action_name.replace("select_time_", "").replace("_", " ").replace("PM", " PM").replace("AM", " AM")
            self.state["booking"]["time"] = time
            self._set_data({"booking": {"time": time}})
        
        elif action_name == "name_change":
            self.state["booking"]["name"] = event_data.get("value", "")
        
        elif action_name == "phone_change":
            self.state["booking"]["phone"] = event_data.get("value", "")
        
        elif action_name == "confirm_booking":
            self.handle_confirm_booking()
        
        return self.messages
    
    def handle_search(self):
        """Process search and show results."""
        self.state["view"] = "results"
        
        # In real app, filter based on search criteria
        results = RESTAURANTS
        self.state["results"] = results
        
        self.build_results_view(results)
    
    def handle_book(self, restaurant_id: str):
        """Start booking flow for a restaurant."""
        restaurant = next((r for r in RESTAURANTS if r.id == restaurant_id), None)
        if restaurant:
            self.state["view"] = "booking"
            self.state["selected_restaurant"] = restaurant
            self.build_booking_view(restaurant)
    
    def handle_confirm_booking(self):
        """Confirm the booking."""
        self.state["view"] = "confirmation"
        restaurant = self.state["selected_restaurant"]
        booking = self.state["booking"]
        
        self.build_confirmation_view(
            restaurant.name,
            booking.get("time", "7:00 PM"),
            booking.get("name", "Guest")
        )


# =============================================================================
# Demo
# =============================================================================

def demo_restaurant_finder():
    """Run the restaurant finder demo."""
    
    print("=" * 70)
    print("Restaurant Finder - Complete A2UI Demo")
    print("=" * 70)
    
    agent = RestaurantFinderAgent()
    
    # Phase 1: Initial Search View
    print("\n\n📱 PHASE 1: Initial Search View")
    print("-" * 70)
    agent.build_search_view()
    print(f"Generated {len(agent.messages)} messages for search view")
    print("\nFirst 3 messages:")
    for msg in agent.messages[:3]:
        print(f"  {msg[:100]}...")
    
    # Phase 2: User searches
    print("\n\n📱 PHASE 2: User clicks 'Search'")
    print("-" * 70)
    response = agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "search", "componentId": "search_btn"},
            "data": {}
        }
    }))
    print(f"Generated {len(response)} messages for results view")
    
    # Phase 3: User books restaurant
    print("\n\n📱 PHASE 3: User clicks 'Book' on Pasta Paradise")
    print("-" * 70)
    response = agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "book_rest_1", "componentId": "restaurant_rest_1_action"},
            "data": {}
        }
    }))
    print(f"Generated {len(response)} messages for booking view")
    
    # Phase 4: User selects time
    print("\n\n📱 PHASE 4: User selects 7:00 PM")
    print("-" * 70)
    response = agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "select_time_700_PM", "componentId": "time_1"},
            "data": {}
        }
    }))
    print(f"Generated {len(response)} messages")
    
    # Phase 5: User enters info and confirms
    print("\n\n📱 PHASE 5: User enters name and confirms")
    print("-" * 70)
    agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "name_change"},
            "data": {"value": "John Smith"}
        }
    }))
    
    response = agent.handle_event(json.dumps({
        "userAction": {
            "action": {"name": "confirm_booking", "componentId": "confirm_btn"},
            "data": {}
        }
    }))
    print(f"Generated {len(response)} messages for confirmation view")
    print("\nFinal confirmation messages:")
    for msg in response:
        print(f"  {msg}")


def print_full_flow():
    """Print the complete JSONL stream for the initial view."""
    
    print("\n\n" + "=" * 70)
    print("Complete JSONL Stream for Search View")
    print("=" * 70)
    print()
    
    agent = RestaurantFinderAgent()
    agent.build_search_view()
    
    print("# This is the complete JSONL stream sent to the client:")
    print("-" * 70)
    for msg in agent.messages:
        print(msg)
    print("-" * 70)


if __name__ == "__main__":
    demo_restaurant_finder()
    print_full_flow()
    
    print("\n\n" + "=" * 70)
    print("RESTAURANT FINDER SUMMARY")
    print("=" * 70)
    print("""
This demo showcases a complete A2UI application flow:

1. MULTI-VIEW NAVIGATION
   - Search → Results → Booking → Confirmation
   - State-driven view rendering

2. INTERACTIVE COMPONENTS
   - Text fields with data binding
   - Dropdowns for selection
   - Increment/decrement buttons
   - Action buttons with event handlers

3. DYNAMIC LISTS
   - Restaurant results rendered from data
   - Each result has interactive elements

4. STATE MANAGEMENT
   - Agent maintains application state
   - Events update state → trigger UI updates

5. EVENT LOOP
   - User action → Agent processes → New UI streamed

This pattern can be applied to any complex workflow:
- E-commerce checkout
- Form wizards
- Dashboard builders
- Chat bots with rich responses
""")
