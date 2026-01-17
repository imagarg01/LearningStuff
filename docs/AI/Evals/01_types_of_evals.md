# Types of Evals

Just like traditional software testing has a pyramid (Unit -> Integration -> E2E), AI systems have a hierarchy of evaluations.

## 1. Unit Evals (Atomic Level)

These test individual components in isolation. They are fast, cheap, and specific.

* **Scope**: A single prompt, a specific tool execution, or a helper function.
* **Example**: Testing if a "Summarization Prompt" actually produces a summary within the token limit.
* **Metric**: Length check, keyword presence, JSON schema validation.

## 2. Integration Evals (Flow Level)

These test how multiple components work together, such as a chain of composition or a RAG retrieval plus generation.

* **Scope**: A chain of 2-3 steps. E.g., Retrieve Documents -> Re-rank -> Generate Answer.
* **Example**: Testing if the RAG system retrieves the correct document for a specific query and generates a grounded answer.
* **Metric**: Retrieval Recall@K, Faithfulness (did the answer come from the context?).

## 3. End-to-End (E2E) Evals (System Level)

These simulate a real user interaction with the full agent.

* **Scope**: The entire conversation flow, often multi-turn.
* **Example**: A user asks the agent to "Book a flight to Paris and find a hotel." The eval checks if the agent successfully calls the flight and hotel APIs with correct parameters.
* **Metric**: Goal completion rate, User satisfaction score (simulated).

## 4. Online vs. Offline Evals

### Offline Evals (Development Time)

* **When**: Run before deployment (CI/CD).
* **Data**: curated datasets (Golden Datasets).
* **Goal**: Prevent regressions, sanity check changes.

### Online Evals (Runtime)

* **When**: Run on live production traffic.
* **Data**: Real user queries.
* **Goal**: Monitoring, gathering data for future offline evals.
* **Examples**:
  * **Implicit feedback**: Did the user copy the code? Did they re-phrase the query (bad sign)?
  * **Explicit feedback**: Thumbs up/down.
  * **LLM Monitor**: A smaller/cheaper model checking high-risk interactions in the background for safety violations.
