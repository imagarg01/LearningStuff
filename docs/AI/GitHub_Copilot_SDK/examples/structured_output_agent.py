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

    # Request structured output matching the Pydantic model.
    # The SDK currently doesn't support 'response_format' kwarg.
    # We will use prompt engineering to request JSON.
    schema = json.dumps(MovieReview.model_json_schema(), indent=2)
    full_prompt = f"{query}\n\nRespond with strict JSON matching this schema:\n{schema}"

    try:
        response_event = await session.send_and_wait({"prompt": full_prompt})
        
        if response_event and response_event.data:
            content = getattr(response_event.data, 'content', '')
            print("\n--- Structured Output (Raw) ---")
            print(content)
            
            # Attempt to parse json
            # Note: In a real app, you might need to strip markdown ```json fences
            try:
                # Naive cleanup of code fences
                clean_json = content.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(clean_json)
                print("\n--- Parsed JSON ---")
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("Could not parse JSON from response.")
        
    except Exception as e:
        print(f"Error (SDK might differ in structured output impl): {e}")

if __name__ == "__main__":
    asyncio.run(main())
