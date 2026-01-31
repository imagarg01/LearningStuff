"""
Pydantic Example 01: Basic AI Structure
=======================================
This example demonstrates:
1. Defining a Pydantic model for an AI agent's output.
2. Generating a JSON schema from that model (what you'd send to an LLM).
3. Simulating an AI response and validating it.
4. Handling validation errors (simulating "hallucinations").

Dependencies: pydantic
"""

import json
from pydantic import BaseModel, Field, ValidationError

# =============================================================================
# 1. Define the Schema (The "Contract" for the AI)
# =============================================================================

class UserProfile(BaseModel):
    """
    A structured user profile extracted from natural language text.
    """
    full_name: str = Field(..., description="The user's full name")
    age: int = Field(..., description="The user's age in years")
    skills: list[str] = Field(default_factory=list, description="List of technical skills mentioned")
    is_available: bool = Field(False, description="Whether the user is explicitly available for work")

def demonstrate_schema_generation():
    print("\n--- 1. Generating Schema for LLM ---")
    print("This JSON Schema tells the LLM exactly what format to produce:")
    
    # helper to get schema (method varies slightly by Pydantic version)
    schema = UserProfile.model_json_schema()
    print(json.dumps(schema, indent=2))

# =============================================================================
# 2. Extracting from "Perfect" AI Output
# =============================================================================

def simulate_perfect_extraction():
    print("\n--- 2. Simulating Perfect AI Extraction ---")
    
    # Imagine the AI read: "Alice is a 30 year old Python developer looking for work."
    # And it generated this JSON string:
    llm_response_str = """
    {
        "full_name": "Alice Smith",
        "age": 30,
        "skills": ["Python", "Django", "AI"],
        "is_available": true
    }
    """
    
    print(f"Raw LLM Output: {llm_response_str.strip()}")
    
    # Validate and Parse
    try:
        profile = UserProfile.model_validate_json(llm_response_str)
        print("\n✅ Validated Object:")
        print(f"Name: {profile.full_name}")
        print(f"Age: {profile.age} (Type: {type(profile.age).__name__})")
        print(f"Skills: {', '.join(profile.skills)}")
    except ValidationError as e:
        print(f"❌ Validation Failed: {e}")

# =============================================================================
# 3. Handling "Hallucinations" (Validation Errors)
# =============================================================================

def simulate_hallucination():
    print("\n--- 3. Handling AI Hallucinations (Validation Errors) ---")
    
    # Imagine the AI read: "Bob is twenty years old."
    # LLMs notoriously struggle with types (returning "twenty" instead of 20)
    bad_llm_response = """
    {
        "full_name": "Bob Jones",
        "age": "twenty", 
        "skills": "Math"
    }
    """
    # Note: 'skills' should be a list, 'age' should be int
    
    print(f"Raw Bad Output: {bad_llm_response.strip()}")
    
    try:
        UserProfile.model_validate_json(bad_llm_response)
    except ValidationError as e:
        print("\n❌ CAUGHT ERROR! Pydantic saved us from bad data:")
        # In a real agent, you would send this error back to the LLM to fix it!
        print(e.json(indent=2))

if __name__ == "__main__":
    demonstrate_schema_generation()
    simulate_perfect_extraction()
    simulate_hallucination()
