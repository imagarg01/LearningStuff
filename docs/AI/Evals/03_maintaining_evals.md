# Maintaining Evals: The Hard Part

Creating evals is easy; maintaining them as your product evolves is the real challenge. Here is how to keep your sanity.

## The Challenges

1. **Drift**: The underlying models change (OpenAI updates logic), your prompts change, and user behavior changes.
2. **Flakiness**: LLMs are probabilistic. A test might fail 1 out of 10 times. Is it a bug or just noise?
3. **Cost/Latency**: Running 1000 GPT-4 evals on every git commit is expensive and slow.

## Best Practices

### 1. Treat Evals as Code

* Store your datasets (JSONL/CSV) in Git (or use DVC for large files).
* Version your prompts alongside your code.
* Review eval changes in Pull Requests.

### 2. Hierarchical Testing (CI/CD Strategy)

* **Smoke Tests (Pre-commit/PR)**: Run 10-20 critical deterministic tests. Must be fast (< 1 min).
* **Nightly Tests**: Run the full suite (100s of cases), including expensive LLM-as-a-judge metrics.
* **Staging Tests**: Run E2E tests against the deployed staging environment.

### 3. Dealing with Flakiness

* **Pass@K**: Instead of verifying one run, run the prompt 5 times. If it passes 4/5, it's green.
* **Strict vs Loose Asserts**: Use looser constraints for creative tasks (semantic similarity) and strict constraints for structured tasks (JSON schema).

### 4. Dynamic Datasets

* Don't just have a static file. Continuously ingest "hard examples" from production.
* Regularly "prune" easy tests that never fail to save time/cost.
* **Test Expansion**: If a user reports a bug, immediately add a regression test case for it.

### 5. Judge the Judge

* Your "LLM Judge" can also be wrong.
* Periodically audit a sample of the Judge's decisions (human review) to ensure it aligns with human preference.
