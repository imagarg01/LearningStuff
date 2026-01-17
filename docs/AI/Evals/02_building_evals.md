# Building and Running Evals

Building an evaluation pipeline requires three key components: **Datasets**, **Metrics**, and **Tooling**.

## 1. Dataset Creation (The "What")

Your evals are only as good as your data.

* **Hand-Curated (Golden)**: High-quality examples written by experts. Expensive but trustworthy. Best for "Unit Evals" of core behavior.
* **Synthetic Data**: Use a strong model (like GPT-4) to generate test cases.
  * *Technique*: Ask GPT-4 to "Generate 50 complex customer support queries about refund policies."
  * *Pros*: Fast, scalable. *Cons*: potential bias, lacks real-world messiness.
* **Log-Based (Real World)**: Anonymized production logs. This is the gold standard for "Coverage."
  * *Process*: Take a failed production conversation -> Add it to the test suite -> Fix the bug.

## 2. Choosing the Right Metric (The "How")

### Deterministic Metrics (Code-based)

Fast, cheap, and typically binary.

* **Exact Match**: String equality (rarely useful for conversational text).
* **Regex**: "Does the output contain an email address pattern?"
* **JSON Validity**: "Is the output valid JSON and does it have the key 'user_id'?"
* **Code Execution**: "Does the generated Python code run and pass unit tests?"

### Model-Based Metrics (LLM-as-a-Judge)

Using an LLM to evaluate another LLM's output. Slower and more expensive, but captures nuance.

* **Reference-based**: Compare the actual output to a "Golden Answer" and score similarity (1-5).
* **Reference-free**: Evaluate qualities like "Helpfulness", "Tone", or "Coherence" without a ground truth.
* **Rubrics**: Provide detailed criteria to the Judge (e.g., "Give a score of 1 if the answer is rude, 5 if it is polite and helpful").

### Embedding-Based Metrics

* **Cosine Similarity**: Convert Output and Reference to vectors and measure distance. Good for semantic closeness, bad for ensuring factual accuracy of specific details.

## 3. Tooling (The "Where")

You don't always need a complex SaaS platform.

* **Simple Scripts**: A Python script iterating over a list of prompts is a great start (see examples in `src/`).
* **Pytest**: Use standard testing frameworks. Treat prompts as inputs and LLM calls as functions to test.
* **Specialized Libraries**:
  * **Ragas**: specialized for RAG pipelines.
  * **DeepEval**: unit testing framework for LLMs.
  * **Promptfoo**: CLI tool for comparing prompts/models side-by-side.
