import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from copilot import CopilotClient, define_tool

load_dotenv()

# --- 1. Define Pydantic Models for Inputs ---
class CalculatorParams(BaseModel):
    a: int = Field(description="First integer")
    b: int = Field(description="Second integer")

class FileStatsParams(BaseModel):
    filepath: str = Field(description="Path to the file to check")

# --- 2. Define Tools using @define_tool ---
@define_tool(description="Calculates the sum of two integers.")
def calculate_sum(params: CalculatorParams) -> int:
    return params.a + params.b

@define_tool(description="Get file size stats.")
def get_file_stats(params: FileStatsParams) -> str:
    try:
        size = os.path.getsize(params.filepath)
        return f"File {params.filepath} is {size} bytes."
    except Exception as e:
        return str(e)

async def main():
    # Initialize client
    client = CopilotClient()
    
    # Pass tools when creating the session
    session = await client.create_session({
        "tools": [calculate_sum, get_file_stats]
    })

    # Ask a question requiring the tool
    query = "What is 12345 + 67890?"
    print(f"User: {query}")
    
    # The agent should see the tool, plan to call it, execute it, and return the answer
    response = await session.send_and_wait({"prompt": query})
    if response and response.data:
         print(f"Copilot: {getattr(response.data, 'content', '')}")

    # Ask a question about file stats
    query_file = "check stats for 'requirements.txt'"
    print(f"\nUser: {query_file}")
    response = await session.send_and_wait({"prompt": query_file})
    if response and response.data:
         print(f"Copilot: {getattr(response.data, 'content', '')}")

if __name__ == "__main__":
    asyncio.run(main())
