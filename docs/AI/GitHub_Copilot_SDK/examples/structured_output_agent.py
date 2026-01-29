import os
import asyncio
import json
from dotenv import load_dotenv
from copilot import CopilotClient
from pydantic import BaseModel, Field

load_dotenv()

# Define the desired structure using Pydantic
class MovieReview(BaseModel):
    title: str = Field(description="The title of the movie")
    rating: int = Field(description="Rating out of 10")
    sentiment: str = Field(description="One of: Positive, Negative, Neutral")

async def main():
    client = CopilotClient()
    session = await client.create_session()

    query = "Review the movie 'Inception'. likely a masterpiece."
    print(f"User: {query}")

    # Request structured output matching the Pydantic model
    # Note: Method name 'send_structured' is hypothetical based on common SDK patterns
    # If not available, usually done via prompt engineering + response_format param
    try:
        response = await session.send(
            query,
            response_format=MovieReview
        )
        
        # Copilot returns a parsed object or dict
        print("\n--- Structured Output ---")
        print(response.parsed) 
        # or response.content depending on SDK implementation
        
    except Exception as e:
        print(f"Error (SDK might differ in structured output impl): {e}")

if __name__ == "__main__":
    asyncio.run(main())
