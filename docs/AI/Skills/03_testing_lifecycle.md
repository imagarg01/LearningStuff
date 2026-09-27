# The Skill Testing Lifecycle

Testing AI skills requires bifurcating the deterministic code from the non-deterministic LLM.

## Prompt-Isolation Testing

You must test the skill's *Description* (the prompt) independently of the execution code.
Create an evaluation dataset of mock intents. Feed only the tool's JSON Schema to the LLM and assert that it accurately selects the tool and formats the parameters without actually running the backend code.

## Property-Based Fuzzing

Because LLMs generate unpredictable outputs, standard mock testing is insufficient for the execution logic. Use property-based testing (e.g., the `Hypothesis` library in Python) to fuzz the deterministic script with massive ranges of edge-case inputs to ensure it gracefully returns semantic errors instead of crashing.

## Fast CI vs. Nightly Evals

* **Fast CI Pipeline (Pull Requests):** Runs static analysis, schema linting, and property-based execution tests. Must complete in < 2 minutes.
* **Nightly Eval Suite:** Runs "End-to-End" (E2E) golden scenarios where the actual Agent is spun up to solve a problem using the skill. Uses "LLM-as-a-Judge" (e.g., GPT-4 or Gemini Pro) to evaluate the trace. Because LLMs are slow and expensive, this runs nightly, not on PRs.
