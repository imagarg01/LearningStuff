import os
import asyncio
from dotenv import load_dotenv
from copilot import CopilotClient

load_dotenv()

async def main():
    client = CopilotClient()
    
    # Sessions maintain state
    session = await client.create_session()

    print("--- Turn 1 ---")
    response1 = await session.send("My name is Ashish.")
    print(f"User: My name is Ashish.\nCopilot: {response1.content}")

    print("\n--- Turn 2 ---")
    # The agent should remember the name from the previous turn
    response2 = await session.send("What is my name?")
    print(f"User: What is my name?\nCopilot: {response2.content}")

if __name__ == "__main__":
    asyncio.run(main())
