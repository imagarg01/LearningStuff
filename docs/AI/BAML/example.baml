// 1. Define your Data Models (Schemas)
class Resume {
  name: string
  email: string
  skills: Skill[]
  experience_years: int
}

class Skill {
  name: string
  level: SkillLevel
}

enum SkillLevel {
  Beginner
  Intermediate
  Expert
}

// 2. Define the Function Signature (The "Contract")
function ExtractResume(text: string) -> Resume {
  // 3. The Prompt implementation
  client "openai/gpt-4" // Use this model
  prompt #"
    Extract the resume details from the text below.
    
    RETURN FORMAT JSON:
    {{ ctx.output_format }}

    RESUME TEXT:
    {{ text }}
  "#
}
