# Module 12: Evaluation (LLM as a Judge)

Evaluating chatbots is harder than traditional software because the output is non-deterministic and semantic. **LLM as a Judge** is a pattern where you use a strong model (like GPT-4) to grade the operational model (like GPT-3.5) based on specific criteria.

## 1. The Dataset

First, you need a dataset of inputs and, ideally, expected outputs or ground truths.

```python
dataset = [
    {"input": "What is LangGraph?", "expected": "A library for building graph-based agents."},
    {"input": "Write a poem about code.", "criteria": "Must rhyme and mention Python."},
]
```

## 2. The Judge

The Judge is just another LLM call. It takes the `input`, the agent's `result`, and the `criteria` (or `expected` answer), and outputs a score or verdict.

**Prompt Pattern:**
> "You are an expert grader. compares the RESULT with the EXPECTED answer. Give a score from 1 to 5."

## 3. Running the Eval

You iterate over your dataset:

1. Run your Agent Graph on the `input`.
2. Capture the output.
3. Run the Judge LLM on the pair (Output, Expected).
4. Aggregate the scores.

## 4. LangSmith

While you can write this loop yourself (as shown in the example), [LangSmith](https://smith.langchain.com/) automates this process, provides a UI for inspecting traces, and helps you curate datasets. It is highly recommended for production apps.
