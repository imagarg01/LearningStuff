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
    response1_event = await session.send_and_wait({"prompt": "My name is Ashish."})
    if response1_event and response1_event.data:
        print(f"User: My name is Ashish.\nCopilot: {getattr(response1_event.data, 'content', '')}")

    print("\n--- Turn 2 ---")
    # The agent should remember the name from the previous turn
    response2_event = await session.send_and_wait({"prompt": "What is my name?"})
    if response2_event and response2_event.data:
        print(f"User: What is my name?\nCopilot: {getattr(response2_event.data, 'content', '')}")

if __name__ == "__main__":
    asyncio.run(main())
