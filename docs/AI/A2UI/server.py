"""
A2UI Full-Stack Demo Server
===========================
FastAPI server that serves both the frontend and A2UI SSE streams.

Run with: python server.py
Visit: http://localhost:8000
"""

import json
import asyncio
from pathlib import Path
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse


# =============================================================================
# Application Setup
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown events."""
    print("🚀 A2UI Demo Server starting...")
    print("📍 Visit http://localhost:8000")
    yield
    print("👋 Server shutting down...")

app = FastAPI(title="A2UI Demo", lifespan=lifespan)

# Get the directory containing this script
BASE_DIR = Path(__file__).parent

# Mount static files (web folder)
app.mount("/static", StaticFiles(directory=BASE_DIR / "web"), name="static")


# =============================================================================
# A2UI Generators
# =============================================================================

async def generate_profile_card() -> AsyncGenerator[dict, None]:
    """Generate profile card UI stream."""
    
    # Root structure
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "profile_card"]}}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    # Header
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "header", "component": {"Text": {"text": {"literalString": "🚀 A2UI Profile Demo"}, "usageHint": "h1"}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    # Card structure
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "profile_card", "component": {"Card": {"child": "card_content", "elevation": "high"}}}
        ]}
    })}
    await asyncio.sleep(0.05)
    
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "card_content", "component": {"Column": {"children": {"explicitList": ["avatar_row", "bio", "stats_row", "action_row"]}}}}
        ]}
    })}
    await asyncio.sleep(0.05)
    
    # Avatar row
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "avatar_row", "component": {"Row": {"children": {"explicitList": ["avatar", "name_col"]}, "alignment": "start"}}},
            {"id": "avatar", "component": {"Image": {"url": {"literalString": "https://api.dicebear.com/7.x/avataaars/svg?seed=A2UI"}, "alt": {"literalString": "Avatar"}}}},
            {"id": "name_col", "component": {"Column": {"children": {"explicitList": ["name", "handle"]}}}},
            {"id": "name", "component": {"Text": {"text": {"path": "user.name"}, "usageHint": "h2"}}},
            {"id": "handle", "component": {"Text": {"text": {"path": "user.handle"}, "usageHint": "caption"}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    # Bio
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "bio", "component": {"Text": {"text": {"path": "user.bio"}, "usageHint": "body"}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    # Stats
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "stats_row", "component": {"Row": {"children": {"explicitList": ["stat_followers", "stat_following", "stat_posts"]}, "alignment": "spaceBetween"}}},
            {"id": "stat_followers", "component": {"Column": {"children": {"explicitList": ["followers_num", "followers_label"]}, "alignment": "center"}}},
            {"id": "followers_num", "component": {"Text": {"text": {"path": "stats.followers"}, "usageHint": "h3"}}},
            {"id": "followers_label", "component": {"Text": {"text": {"literalString": "Followers"}, "usageHint": "caption"}}},
            {"id": "stat_following", "component": {"Column": {"children": {"explicitList": ["following_num", "following_label"]}, "alignment": "center"}}},
            {"id": "following_num", "component": {"Text": {"text": {"path": "stats.following"}, "usageHint": "h3"}}},
            {"id": "following_label", "component": {"Text": {"text": {"literalString": "Following"}, "usageHint": "caption"}}},
            {"id": "stat_posts", "component": {"Column": {"children": {"explicitList": ["posts_num", "posts_label"]}, "alignment": "center"}}},
            {"id": "posts_num", "component": {"Text": {"text": {"path": "stats.posts"}, "usageHint": "h3"}}},
            {"id": "posts_label", "component": {"Text": {"text": {"literalString": "Posts"}, "usageHint": "caption"}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    # Actions
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "action_row", "component": {"Row": {"children": {"explicitList": ["follow_btn", "message_btn"]}, "alignment": "center"}}},
            {"id": "follow_btn", "component": {"Button": {"label": {"literalString": "Follow"}, "action": {"name": "follow"}, "style": "primary"}}},
            {"id": "message_btn", "component": {"Button": {"label": {"literalString": "Message"}, "action": {"name": "message"}, "style": "secondary"}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    # Data model
    yield {"event": "a2ui", "data": json.dumps({
        "dataModelUpdate": {"contents": {
            "user": {
                "name": "Alex Developer",
                "handle": "@alex_dev",
                "bio": "Building the future with A2UI 🚀 | Open source enthusiast | Coffee lover ☕"
            },
            "stats": {
                "followers": "12.5K",
                "following": "892",
                "posts": "347"
            }
        }}
    })}
    
    # Begin rendering
    yield {"event": "a2ui", "data": json.dumps({
        "beginRendering": {"root": "root"}
    })}


async def generate_counter_app() -> AsyncGenerator[dict, None]:
    """Generate interactive counter UI."""
    
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "counter_card"]}, "alignment": "center"}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "header", "component": {"Text": {"text": {"literalString": "⚡ Interactive Counter"}, "usageHint": "h1"}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "counter_card", "component": {"Card": {"child": "card_content", "elevation": "high"}}},
            {"id": "card_content", "component": {"Column": {"children": {"explicitList": ["count_display", "button_row", "reset_btn"]}, "alignment": "center"}}},
            {"id": "count_display", "component": {"Text": {"text": {"path": "count"}, "usageHint": "h1"}}},
            {"id": "button_row", "component": {"Row": {"children": {"explicitList": ["dec_btn", "inc_btn"]}, "alignment": "center", "spacing": "medium"}}},
            {"id": "dec_btn", "component": {"Button": {"label": {"literalString": "−"}, "action": {"name": "decrement"}, "style": "secondary"}}},
            {"id": "inc_btn", "component": {"Button": {"label": {"literalString": "+"}, "action": {"name": "increment"}, "style": "primary"}}},
            {"id": "reset_btn", "component": {"Button": {"label": {"literalString": "Reset"}, "action": {"name": "reset"}, "style": "danger"}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    yield {"event": "a2ui", "data": json.dumps({
        "dataModelUpdate": {"contents": {"count": "0"}}
    })}
    
    yield {"event": "a2ui", "data": json.dumps({
        "beginRendering": {"root": "root"}
    })}


async def generate_restaurant_finder() -> AsyncGenerator[dict, None]:
    """Generate restaurant finder demo."""
    
    # Header
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "search_card", "results_header", "results_list"]}}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "header", "component": {"Text": {"text": {"literalString": "🍽️ Restaurant Finder"}, "usageHint": "h1"}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    # Search card
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "search_card", "component": {"Card": {"child": "search_form"}}},
            {"id": "search_form", "component": {"Row": {"children": {"explicitList": ["search_input", "search_btn"]}, "alignment": "center"}}},
            {"id": "search_input", "component": {"TextField": {"label": {"literalString": "Search"}, "placeholder": {"literalString": "Pizza, Sushi, Burgers..."}, "action": {"name": "search_change"}}}},
            {"id": "search_btn", "component": {"Button": {"label": {"literalString": "🔍 Search"}, "action": {"name": "search"}, "style": "primary"}}}
        ]}
    })}
    await asyncio.sleep(0.2)
    
    # Results header
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "results_header", "component": {"Text": {"text": {"path": "resultsTitle"}, "usageHint": "h2"}}}
        ]}
    })}
    
    # Restaurant cards
    restaurants = [
        {"id": "r1", "name": "Pasta Paradise", "cuisine": "Italian", "rating": "4.8", "price": "$$"},
        {"id": "r2", "name": "Sushi Supreme", "cuisine": "Japanese", "rating": "4.9", "price": "$$$"},
        {"id": "r3", "name": "Taco Town", "cuisine": "Mexican", "rating": "4.5", "price": "$"},
    ]
    
    result_ids = [f"restaurant_{r['id']}" for r in restaurants]
    
    yield {"event": "a2ui", "data": json.dumps({
        "surfaceUpdate": {"components": [
            {"id": "results_list", "component": {"Column": {"children": {"explicitList": result_ids}}}}
        ]}
    })}
    await asyncio.sleep(0.1)
    
    for r in restaurants:
        rid = f"restaurant_{r['id']}"
        await asyncio.sleep(0.15)  # Stagger for visual effect
        
        yield {"event": "a2ui", "data": json.dumps({
            "surfaceUpdate": {"components": [
                {"id": rid, "component": {"Card": {"child": f"{rid}_content"}}},
                {"id": f"{rid}_content", "component": {"Row": {"children": {"explicitList": [f"{rid}_info", f"{rid}_book"]}, "alignment": "spaceBetween"}}},
                {"id": f"{rid}_info", "component": {"Column": {"children": {"explicitList": [f"{rid}_name", f"{rid}_meta"]}}}},
                {"id": f"{rid}_name", "component": {"Text": {"text": {"literalString": r["name"]}, "usageHint": "h3"}}},
                {"id": f"{rid}_meta", "component": {"Text": {"text": {"literalString": f"{r['cuisine']} • ⭐ {r['rating']} • {r['price']}"}, "usageHint": "caption"}}},
                {"id": f"{rid}_book", "component": {"Button": {"label": {"literalString": "Book"}, "action": {"name": f"book_{r['id']}"}, "style": "primary"}}}
            ]}
        })}
    
    await asyncio.sleep(0.1)
    
    yield {"event": "a2ui", "data": json.dumps({
        "dataModelUpdate": {"contents": {
            "resultsTitle": f"Found {len(restaurants)} restaurants nearby"
        }}
    })}
    
    yield {"event": "a2ui", "data": json.dumps({
        "beginRendering": {"root": "root"}
    })}


# =============================================================================
# Routes
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main index page."""
    return FileResponse(BASE_DIR / "web" / "index.html")


@app.get("/profile", response_class=HTMLResponse)
async def profile_page():
    """Serve profile demo page."""
    return FileResponse(BASE_DIR / "web" / "profile.html")


@app.get("/counter", response_class=HTMLResponse)
async def counter_page():
    """Serve counter demo page."""
    return FileResponse(BASE_DIR / "web" / "counter.html")


@app.get("/restaurant", response_class=HTMLResponse)
async def restaurant_page():
    """Serve restaurant finder demo page."""
    return FileResponse(BASE_DIR / "web" / "restaurant.html")


@app.get("/api/profile/stream")
async def profile_stream():
    """SSE endpoint for profile card."""
    return EventSourceResponse(generate_profile_card())


@app.get("/api/counter/stream")
async def counter_stream():
    """SSE endpoint for counter app."""
    return EventSourceResponse(generate_counter_app())


@app.get("/api/restaurant/stream")
async def restaurant_stream():
    """SSE endpoint for restaurant finder."""
    return EventSourceResponse(generate_restaurant_finder())


@app.post("/api/action")
async def handle_action(request: Request):
    """Handle user actions from the frontend."""
    data = await request.json()
    action = data.get("userAction", {}).get("action", {})
    action_name = action.get("name", "")
    
    print(f"📥 Action received: {action_name}")
    
    # In a real app, you'd process the action and return updated UI
    return {"status": "ok", "action": action_name}


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
