import os
import asyncio
from dotenv import load_dotenv
from copilot import CopilotClient

load_dotenv()

async def main():
    client = CopilotClient()
    session = await client.create_session()

    query = "Write a short poem about coding."
    print(f"User: {query}\nCopilot (Streaming):")

    # Handler for streaming events
    def handle_event(event):
        if event.type == "assistant.message_delta" and event.data:
             print(getattr(event.data, 'content', ''), end="", flush=True)

    # Subscribe to events
    unsubscribe = session.on(handle_event)

    # Enable streaming in the session config if needed, or just send with mode
    await session.send_and_wait({"prompt": query})
    
    unsubscribe()
    print() # Newline at end

if __name__ == "__main__":
    asyncio.run(main())
