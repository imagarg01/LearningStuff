import os
import asyncio
from dotenv import load_dotenv
from copilot import CopilotClient

# Load environment variables (GITHUB_TOKEN)
load_dotenv()

async def main():
    # Initialize the client
    # Expects GITHUB_TOKEN in env or can be passed explicitly
    client = CopilotClient()

    # Create a session
    session = await client.create_session()

    # Send a message
    print("User: Hello, who are you?")
    response = await session.send("Hello, who are you?")

    # Print the response
    print(f"Copilot: {response.content}")

if __name__ == "__main__":
    asyncio.run(main())
