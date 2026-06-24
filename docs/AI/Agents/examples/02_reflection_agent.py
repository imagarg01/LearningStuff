import os
from typing import Annotated, Sequence, TypedDict
import operator
from pydantic import BaseModel, Field

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# -----------------------------------------------------
# Pattern 2: Evaluator-Optimizer (Reflection) Architecture
# Mapped to Agent Learning Path: Module 05.2
# -----------------------------------------------------

# 1. Define the State
class ReflectionState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    draft: str
    score: int
    feedback: str
    iterations: int # Crucial safety-bound metric to prevent infinite loops

# 2. Define the LLM Models
generator_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
critic_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# The structured output required natively from the Critic LLM
class Critique(BaseModel):
    score: int = Field(description="Score from 1 to 10 on how polite and concise the draft is.")
    feedback: str = Field(description="Specific rules violated or improvements needed.")

critic_llm_structured = critic_llm.with_structured_output(Critique)

# 3. Define the Generator Node
def generator_node(state: ReflectionState):
    iteration = state.get("iterations", 0) + 1
    print(f"\n[NODE: GENERATOR] Attempt {iteration}...")
    
    sys_prompt = "You write emails. Do not use exclamation marks."
    
    if iteration > 1:
        # If we failed before, dynamically inject the Critic's feedback!
        sys_prompt += f"\nCRITIC FEEDBACK on previous draft MUST BE ADDRESSED: {state['feedback']}"
        
    response = generator_llm.invoke([
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": state["messages"][0].content}
    ])
    
    print(f"  -> Draft generated: '{response.content}'")
    return {"draft": response.content, "iterations": iteration}

# 4. Define the Critic Node
def critic_node(state: ReflectionState):
    print("\n[NODE: CRITIC] Evaluating draft...")
    
    evaluation_prompt = f"""
    Evaluate this email draft: "{state['draft']}"
    Rule 1: It must be extremely polite.
    Rule 2: It must NEVER use an exclamation mark!
    
    If it violates Rule 2, the score MUST be under 5.
    If it follows all rules perfectly, score it an 8 or above.
    """
    
    critique = critic_llm_structured.invoke(evaluation_prompt)
    print(f"  -> Critic Score: {critique.score}/10. Feedback: {critique.feedback}")
    
    return {"score": critique.score, "feedback": critique.feedback}

# 5. Define Routing Logic
def evaluation_router(state: ReflectionState):
    print("\n[ROUTE] Checking critic score...")
    
    # If the score is high enough OR we tried too many times (Safety Bound)
    if state["score"] >= 8:
        print("  -> Score >= 8. Approved! Terminating Edge.")
        return END
    if state["iterations"] >= 3:
        print("  -> Safety Bound: Max iterations reached. Forcing termination.")
        return END
        
    print("  -> Score < 8. Routing edge back to Generator.")
    return "generator"

# 6. Build the Reflection DAG
builder = StateGraph(ReflectionState)
builder.add_node("generator", generator_node)
builder.add_node("critic", critic_node)

builder.set_entry_point("generator")
# Generator always goes sequentially to Critic
builder.add_edge("generator", "critic")
# Critic conditionally routes back upstream or concludes
builder.add_conditional_edges("critic", evaluation_router)

print("Compiling Evaluator-Optimizer DAG...")
graph = builder.compile()

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("\n[ERROR] Missing environment variable: OPENAI_API_KEY")
        print("Please run: export OPENAI_API_KEY='sk-...'")
        exit(1)
        
    print("\n--- RUNNING REFLECTION PATTERN ---")
    user_input = "Tell the user their refund was denied because they are past 30 days."
    print(f"User Request: {user_input}")
    
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "iterations": 0
    }
    
    final_state = graph.invoke(initial_state)
    print(f"\n[FINAL APPROVED DRAFT]:\n{final_state['draft']}")
