"""
Pydantic Example 02: RAG Extractor
==================================
This example simulates a RAG (Retrieval-Augmented Generation) step where we 
extract structured metadata from a retrieved "messy" document (like a Resume).

It demonstrates proper field descriptions, which act as prompts for the AI.

Dependencies: pydantic
"""

from typing import Optional
from pydantic import BaseModel, Field, ValidationError

# =============================================================================
# 1. Define the "Target" Structure (Resume Data)
# =============================================================================

class WorkExperience(BaseModel):
    company: str = Field(..., description="Name of the company")
    role: str = Field(..., description="Job title")
    years: int = Field(..., description="Number of years worked at this role")

class CandidateResume(BaseModel):
    """
    Structured extraction of a candidate's resume.
    """
    name: str = Field(..., description="Full name of the candidate")
    email: Optional[str] = Field(None, description="Contact email address if found")
    
    # Nested models are powerful! The LLM knows it needs a LIST of these objects.
    experience: list[WorkExperience] = Field(
        default_factory=list, 
        description="List of work history entries"
    )
    
    # Enforcing "Reasoning" prevents hallucination
    skills_summary: str = Field(..., description="A 1-sentence summary of technical skills")

# =============================================================================
# 2. Simulate RAG Extraction with Mock Data
# =============================================================================

def rag_extraction_simulation():
    print("--- RAG Extraction Simulation ---")
    
    # 1. RETRIEVAL STEP (Mocked)
    # Assume we retrieved this messy text chunk from a vector DB
    retrieved_text = """
    RESUME: Jane Doe (jane@example.com)
    Software Engineer at TechCorp for 5 years.
    Before that, she was a Jr Dev at StartupInc for 2 years.
    Expert in Python, Rust, and Kubernetes.
    """
    print(f"📄 Retrieved Document:\n{retrieved_text}\n")
    
    # 2. GENERATION STEP (Mocked LLM Response)
    # We pretend the LLM received the Schema + Text and outputted this JSON:
    mock_llm_json = """
    {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "experience": [
            {"company": "TechCorp", "role": "Software Engineer", "years": 5},
            {"company": "StartupInc", "role": "Jr Dev", "years": 2}
        ],
        "skills_summary": "Expert in Python, Rust, and Kubernetes with 7 years of total experience."
    }
    """
    
    print("🤖 AI Extracted JSON:")
    print(mock_llm_json)
    
    # 3. VERIFICATION STEP
    try:
        resume = CandidateResume.model_validate_json(mock_llm_json)
        print("\n✅ Validated & Parsed Object:")
        print(f"Candidate: {resume.name}")
        print(f"Total Companies: {len(resume.experience)}")
        for job in resume.experience:
            print(f"  - {job.role} @ {job.company} ({job.years} yrs)")
        
        # Accessing nested structures is now type-safe!
        print(f"\nSkills: {resume.skills_summary}")
        
    except ValidationError as e:
        print(f"❌ Extraction Failed: {e}")

if __name__ == "__main__":
    rag_extraction_simulation()
