import os
import asyncio
from dotenv import load_dotenv
from copilot import CopilotClient, tool

load_dotenv()

# Define a custom tool
@tool
def calculate_sum(a: int, b: int) -> int:
    """
    Calculates the sum of two integers.
    
    Args:
        a: First integer.
        b: Second integer.
    
    Returns:
        The sum of a and b.
    """
    return a + b

@tool
def get_file_stats(filepath: str) -> str:
    """
    Get file size stats.
    """
    try:
        size = os.path.getsize(filepath)
        return f"File {filepath} is {size} bytes."
    except Exception as e:
        return str(e)

async def main():
    # Initialize client with tools
    client = CopilotClient(tools=[calculate_sum, get_file_stats])
    
    session = await client.create_session()

    # Ask a question requiring the tool
    query = "What is 12345 + 67890?"
    print(f"User: {query}")
    
    # The agent should see the tool, plan to call it, execute it, and return the answer
    response = await session.send(query)
    print(f"Copilot: {response.content}")

    # Ask a question about file stats
    query_file = "check stats for 'requirements.txt'"
    print(f"\nUser: {query_file}")
    response = await session.send(query_file)
    print(f"Copilot: {response.content}")

if __name__ == "__main__":
    asyncio.run(main())
