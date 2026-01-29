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

    # Assuming a stream=True parameter or a separate stream method
    async for chunk in session.stream(query):
        print(chunk.content, end="", flush=True)
    print() # Newline at end

if __name__ == "__main__":
    asyncio.run(main())
