"""
A2UI Example 04: Streaming UI
=============================
Demonstrates progressive/streaming UI rendering.

This example shows how to:
1. Stream A2UI messages as JSONL
2. Implement Server-Sent Events (SSE) for real-time updates
3. Build UI progressively for responsive UX
"""

import json
import time
import asyncio
from typing import Generator, AsyncGenerator


# =============================================================================
# JSONL Streaming Basics
# =============================================================================

def generate_jsonl_stream() -> Generator[str, None, None]:
    """
    Generator that yields A2UI messages one at a time.
    
    This simulates how an LLM or agent would stream UI components.
    """
    
    # Message 1: Root container
    yield json.dumps({
        "surfaceUpdate": {
            "components": [{
                "id": "root",
                "component": {
                    "Column": {
                        "children": {"explicitList": ["header", "content", "footer"]}
                    }
                }
            }]
        }
    })
    
    # Message 2: Header
    yield json.dumps({
        "surfaceUpdate": {
            "components": [{
                "id": "header",
                "component": {
                    "Text": {
                        "text": {"literalString": "Loading Results..."},
                        "usageHint": "h1"
                    }
                }
            }]
        }
    })
    
    # Message 3: Content area
    yield json.dumps({
        "surfaceUpdate": {
            "components": [{
                "id": "content",
                "component": {
                    "Column": {
                        "children": {"explicitList": ["item1", "item2", "item3"]}
                    }
                }
            }]
        }
    })
    
    # Messages 4-6: Items (streamed progressively)
    for i in range(1, 4):
        yield json.dumps({
            "surfaceUpdate": {
                "components": [{
                    "id": f"item{i}",
                    "component": {
                        "Card": {
                            "child": f"item{i}_content"
                        }
                    }
                }]
            }
        })
        
        yield json.dumps({
            "surfaceUpdate": {
                "components": [{
                    "id": f"item{i}_content",
                    "component": {
                        "Text": {
                            "text": {"literalString": f"Result #{i}"},
                            "usageHint": "h3"
                        }
                    }
                }]
            }
        })
    
    # Message 7: Footer
    yield json.dumps({
        "surfaceUpdate": {
            "components": [{
                "id": "footer",
                "component": {
                    "Text": {
                        "text": {"literalString": "All results loaded ✓"},
                        "usageHint": "caption"
                    }
                }
            }]
        }
    })
    
    # Message 8: Data model
    yield json.dumps({
        "dataModelUpdate": {
            "contents": {
                "resultCount": 3,
                "loadTime": "0.5s"
            }
        }
    })
    
    # Message 9: Begin rendering
    yield json.dumps({
        "beginRendering": {"root": "root"}
    })


def demo_basic_streaming():
    """
    Demonstrates basic JSONL streaming.
    """
    
    print("=" * 70)
    print("Basic JSONL Streaming")
    print("=" * 70)
    print()
    print("Each line is a complete JSON message that can be parsed immediately.")
    print("The client renders progressively as each line arrives.")
    print()
    print("-" * 70)
    
    for i, message in enumerate(generate_jsonl_stream(), 1):
        print(f"[Message {i}] {message}")
        time.sleep(0.1)  # Simulate network delay
    
    print("-" * 70)
    print("\n✓ Streaming complete!")


# =============================================================================
# Async Streaming (SSE-compatible)
# =============================================================================

async def async_stream_ui() -> AsyncGenerator[str, None]:
    """
    Async generator for Server-Sent Events (SSE).
    
    In production, this would be connected to an LLM that generates
    components as it processes the user's request.
    """
    
    # Simulate initial loading state
    yield json.dumps({
        "surfaceUpdate": {
            "components": [{
                "id": "root",
                "component": {"Column": {"children": {"explicitList": ["loading"]}}}
            }]
        }
    })
    
    yield json.dumps({
        "surfaceUpdate": {
            "components": [{
                "id": "loading",
                "component": {
                    "Text": {"text": {"literalString": "Searching..."}, "usageHint": "h2"}
                }
            }]
        }
    })
    
    yield json.dumps({"beginRendering": {"root": "root"}})
    
    # Simulate processing delay
    await asyncio.sleep(0.3)
    
    # Update to show results are coming
    yield json.dumps({
        "surfaceUpdate": {
            "components": [{
                "id": "root",
                "component": {
                    "Column": {"children": {"explicitList": ["title", "result_list"]}}
                }
            }]
        }
    })
    
    yield json.dumps({
        "surfaceUpdate": {
            "components": [{
                "id": "title",
                "component": {
                    "Text": {"text": {"literalString": "Search Results"}, "usageHint": "h1"}
                }
            }]
        }
    })
    
    # Stream results one by one
    results = [
        {"name": "First Result", "desc": "This is the first result"},
        {"name": "Second Result", "desc": "This is the second result"},
        {"name": "Third Result", "desc": "This is the third result"},
    ]
    
    result_ids = []
    
    for i, result in enumerate(results):
        await asyncio.sleep(0.2)  # Simulate processing time
        
        result_id = f"result_{i}"
        result_ids.append(result_id)
        
        # Update result list
        yield json.dumps({
            "surfaceUpdate": {
                "components": [{
                    "id": "result_list",
                    "component": {
                        "Column": {"children": {"explicitList": result_ids.copy()}}
                    }
                }]
            }
        })
        
        # Add result card
        yield json.dumps({
            "surfaceUpdate": {
                "components": [{
                    "id": result_id,
                    "component": {"Card": {"child": f"{result_id}_content"}}
                }]
            }
        })
        
        yield json.dumps({
            "surfaceUpdate": {
                "components": [
                    {
                        "id": f"{result_id}_content",
                        "component": {
                            "Column": {"children": {"explicitList": [f"{result_id}_name", f"{result_id}_desc"]}}
                        }
                    },
                    {
                        "id": f"{result_id}_name",
                        "component": {
                            "Text": {"text": {"literalString": result["name"]}, "usageHint": "h3"}
                        }
                    },
                    {
                        "id": f"{result_id}_desc",
                        "component": {
                            "Text": {"text": {"literalString": result["desc"]}, "usageHint": "body"}
                        }
                    }
                ]
            }
        })
    
    # Final update
    await asyncio.sleep(0.1)
    yield json.dumps({
        "dataModelUpdate": {"contents": {"totalResults": len(results)}}
    })


async def demo_async_streaming():
    """
    Demonstrates async streaming (SSE-style).
    """
    
    print("\n\n" + "=" * 70)
    print("Async Streaming (SSE-compatible)")
    print("=" * 70)
    print()
    print("Simulates real-time streaming with processing delays.")
    print("In production, this would be sent via Server-Sent Events (SSE).")
    print()
    print("-" * 70)
    
    message_num = 0
    async for message in async_stream_ui():
        message_num += 1
        # Format as SSE event
        print(f"event: a2ui")
        print(f"data: {message}")
        print()  # SSE events separated by blank line
    
    print("-" * 70)
    print(f"\n✓ Streamed {message_num} messages!")


# =============================================================================
# FastAPI SSE Integration Example
# =============================================================================

FASTAPI_EXAMPLE = '''
"""
FastAPI Server-Sent Events (SSE) Example

This shows how to create a real A2UI streaming endpoint.
"""

from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

app = FastAPI()


async def generate_a2ui_stream(query: str):
    """Generate A2UI messages based on user query."""
    
    # Initial UI
    yield {
        "event": "a2ui",
        "data": json.dumps({"surfaceUpdate": {"components": [
            {"id": "root", "component": {"Column": {"children": {"explicitList": ["loading"]}}}}
        ]}})
    }
    
    yield {
        "event": "a2ui", 
        "data": json.dumps({"beginRendering": {"root": "root"}})
    }
    
    # Simulate LLM processing
    await asyncio.sleep(0.5)
    
    # Stream results
    # ... (generate components based on query)
    
    yield {
        "event": "a2ui",
        "data": json.dumps({"dataModelUpdate": {"contents": {"status": "complete"}}})
    }


@app.get("/api/a2ui/stream")
async def stream_a2ui(query: str):
    """
    SSE endpoint for A2UI streaming.
    
    Client connects with:
    const eventSource = new EventSource('/api/a2ui/stream?query=...');
    eventSource.addEventListener('a2ui', (e) => {
        const message = JSON.parse(e.data);
        renderA2UI(message);
    });
    """
    return EventSourceResponse(generate_a2ui_stream(query))
'''


def show_fastapi_example():
    """Display FastAPI integration example."""
    
    print("\n\n" + "=" * 70)
    print("FastAPI SSE Integration Example")
    print("=" * 70)
    print()
    print("Here's how to create a real A2UI streaming endpoint with FastAPI:")
    print()
    print("-" * 70)
    print(FASTAPI_EXAMPLE)
    print("-" * 70)


# =============================================================================
# Progressive Loading Pattern
# =============================================================================

def demo_progressive_loading():
    """
    Demonstrates a common pattern: progressive loading with skeleton states.
    """
    
    print("\n\n" + "=" * 70)
    print("Progressive Loading Pattern")
    print("=" * 70)
    print()
    print("Shows skeleton → partial data → complete data flow.")
    print()
    
    class ProgressiveLoader:
        """Demonstrates progressive loading UI pattern."""
        
        def __init__(self):
            self.messages = []
        
        def emit(self, msg: dict):
            self.messages.append(json.dumps(msg))
        
        def phase1_skeleton(self):
            """Phase 1: Show placeholder/skeleton UI immediately."""
            print("\n📦 Phase 1: Skeleton UI (instant)")
            print("-" * 50)
            
            self.emit({"surfaceUpdate": {"components": [
                {"id": "root", "component": {"Column": {"children": {"explicitList": ["card1", "card2", "card3"]}}}}
            ]}})
            
            # Skeleton cards (placeholders)
            for i in range(1, 4):
                self.emit({"surfaceUpdate": {"components": [
                    {"id": f"card{i}", "component": {"Card": {"child": f"skeleton{i}"}}}
                ]}})
                self.emit({"surfaceUpdate": {"components": [
                    {"id": f"skeleton{i}", "component": {"Text": {"text": {"literalString": "Loading..."}, "usageHint": "body"}}}
                ]}})
            
            self.emit({"beginRendering": {"root": "root"}})
            
            for msg in self.messages:
                print(msg)
            self.messages = []
        
        def phase2_partial(self):
            """Phase 2: Replace skeletons with data as it arrives."""
            print("\n📦 Phase 2: Partial Data (as it loads)")
            print("-" * 50)
            
            data = [
                {"title": "Article 1", "preview": "First article preview..."},
                {"title": "Article 2", "preview": "Second article preview..."},
            ]
            
            for i, item in enumerate(data, 1):
                # Replace skeleton with real content
                self.emit({"surfaceUpdate": {"components": [
                    {"id": f"card{i}", "component": {"Card": {"child": f"content{i}"}}},
                    {"id": f"content{i}", "component": {"Column": {"children": {"explicitList": [f"title{i}", f"preview{i}"]}}}},
                    {"id": f"title{i}", "component": {"Text": {"text": {"literalString": item["title"]}, "usageHint": "h3"}}},
                    {"id": f"preview{i}", "component": {"Text": {"text": {"literalString": item["preview"]}, "usageHint": "body"}}}
                ]}})
            
            for msg in self.messages:
                print(msg)
            self.messages = []
        
        def phase3_complete(self):
            """Phase 3: Load remaining content."""
            print("\n📦 Phase 3: Complete (all data loaded)")
            print("-" * 50)
            
            # Final item
            self.emit({"surfaceUpdate": {"components": [
                {"id": "card3", "component": {"Card": {"child": "content3"}}},
                {"id": "content3", "component": {"Column": {"children": {"explicitList": ["title3", "preview3"]}}}},
                {"id": "title3", "component": {"Text": {"text": {"literalString": "Article 3"}, "usageHint": "h3"}}},
                {"id": "preview3", "component": {"Text": {"text": {"literalString": "Third article preview..."}, "usageHint": "body"}}}
            ]}})
            
            self.emit({"dataModelUpdate": {"contents": {"loaded": True, "count": 3}}})
            
            for msg in self.messages:
                print(msg)
    
    loader = ProgressiveLoader()
    loader.phase1_skeleton()
    time.sleep(0.3)
    loader.phase2_partial()
    time.sleep(0.3)
    loader.phase3_complete()


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # Demo 1: Basic streaming
    demo_basic_streaming()
    
    # Demo 2: Async streaming
    asyncio.run(demo_async_streaming())
    
    # Demo 3: Progressive loading pattern
    demo_progressive_loading()
    
    # Show FastAPI example
    show_fastapi_example()
    
    print("\n\n" + "=" * 70)
    print("STREAMING SUMMARY")
    print("=" * 70)
    print("""
1. JSONL FORMAT:
   - Each line is a complete JSON message
   - Parseable immediately as it arrives
   - No need to wait for complete response

2. STREAMING BENEFITS:
   - Perceived performance: UI appears instantly
   - Progressive rendering: Content fills in as loaded
   - Responsive UX: User sees activity immediately

3. IMPLEMENTATION:
   - Use generators/async generators for streaming
   - Send via SSE (Server-Sent Events) or WebSocket
   - Client parses and renders each message

4. PATTERNS:
   - Skeleton → Partial → Complete
   - Loading states for each region
   - Graceful error handling per component
""")
