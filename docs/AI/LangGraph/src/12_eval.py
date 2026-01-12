import asyncio
import os
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# --- 1. The System Under Test (Your Agent) ---

class State(TypedDict):
    messages: Annotated[list, add_messages]

target_llm = ChatOpenAI(model="gpt-3.5-turbo")

def simple_agent(state: State):
    return {"messages": [target_llm.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("agent", simple_agent)
builder.add_edge(START, "agent")
builder.add_edge("agent", END)
agent_graph = builder.compile()

# --- 2. The Judge (Evaluator) ---

judge_llm = ChatOpenAI(model="gpt-4")

judgement_prompt = ChatPromptTemplate.from_template("""
You are an unbiased grader.
Evaluate the following AI response based on the user question and expected answer.
Give a score from 1 to 5, where 5 is perfect.

User Question: {question}
Expected Answer (Key facts): {expected}
AI Response: {result}

Return ONLY the number (1-5).
""")

async def evaluate_response(question, expected, result):
    # Ask GPT-4 to score it
    score_msg = await judge_llm.ainvoke(
        judgement_prompt.format(question=question, expected=expected, result=result)
    )
    try:
        return int(score_msg.content.strip())
    except:
        return 0

# --- 3. The Evaluation Loop ---

dataset = [
    {
        "question": "What is the capital of France?",
        "expected": "Paris"
    },
    {
        "question": "Who wrote Hamlet?",
        "expected": "William Shakespeare"
    },
    {
        "question": "What is 2 + 2?",
        "expected": "4"
    }
]

async def run_eval():
    print("--- Starting Evaluation ---")
    total_score = 0
    
    for item in dataset:
        print(f"\nTesting: {item['question']}")
        
        # 1. Run Agent
        inputs = {"messages": [("user", item['question'])]}
        output = await agent_graph.ainvoke(inputs)
        result_text = output["messages"][-1].content
        print(f"  > Agent said: {result_text}")
        
        # 2. Run Judge
        score = await evaluate_response(item['question'], item['expected'], result_text)
        print(f"  > Judge Score: {score}/5")
        
        total_score += score

    avg_score = total_score / len(dataset)
    print(f"\n--- Final Results ---")
    print(f"Average Score: {avg_score:.2f} / 5.0")

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
         print("Please set OPENAI_API_KEY to run this example.")
    else:
        asyncio.run(run_eval())
