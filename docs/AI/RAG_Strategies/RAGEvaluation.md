# RAG Evaluation: Moving Beyond "Vibes"

Building a RAG pipeline is easy. Making it production-ready is hard. The biggest challenge is **evaluation**.

Without metrics, you are developing based on "vibes" — you tweak a prompt, it looks better for one query, but you don't know if it broke ten others.

---

## 1. The RAG Triad Metrics

The standard for measuring RAG quality is to evaluate three core components of the pipeline:

### A. Context Recall (Is the answer *in* the retrieval?)

- **Question**: Did we retrieve all the necessary information to answer the user's query?
- **Failure Mode**: The answer is "I don't know" or the model hallucinates because the facts weren't found.
- **Improved by**: Better embeddings, Hybrid Search, Query Expansion.

### B. Context Precision (Is the retrieval *noise-free*?)

- **Question**: What is the signal-to-noise ratio in the retrieved chunks?
- **Failure Mode**: The model gets distracted by irrelevant information in the context and gives a wrong answer ("Lost in the Middle" phenomenon).
- **Improved by**: Re-ranking, smaller chunk sizes.

### C. Faithfulness (Is the answer *grounded*?)

- **Question**: Is the generated answer derived *solely* from the retrieved context?
- **Failure Mode**: Hallucinations. The model ignores the context and answers from its pre-trained memory (which might be outdated or wrong).
- **Improved by**: Strict System Prompts ("Answer only using the provided context").

### D. Answer Relevance (Did we *answer* the user?)

- **Question**: Is the generated answer actualy helpful and relevant to the original query?
- **Failure Mode**: The model evades the question or gives a factually correct but irrelevant answer.

---

## 2. Traditional IR Metrics (Pure Retrieval)

Before judging the *answer*, judge the *retrieval*. These metrics don't need an LLM, just positive `(Query, Document)` pairs.

### A. MRR (Mean Reciprocal Rank)

- **Question**: "On average, at what rank (1st, 2nd, 3rd...) does the first relevant document appear?"
- **Formula**: `1/Rank`. If result is #1, score=1.0. If #2, score=0.5. If #10, score=0.1.
- **Why**: Good for cases where the user only looks at the top result (e.g., search bar).

### B. NDCG (Normalized Discounted Cumulative Gain)

- **Question**: "Are the relevant documents at the top, and unrelated ones at the bottom?"
- **Why**: Unlike MRR (binary), NDCG handles graded relevance (Perfect match > Related > Irrelevant).

### C. Hit Rate (Recall@K)

- **Question**: "Does the relevant document appear *at all* in the top K results?"
- **Formula**: `1` if present in top-K, `0` otherwise.

---

## 3. Evaluation Frameworks

You don't need to write these metrics from scratch. Use existing frameworks.

### Ragas (Retrieval Augmented Generation Assessment)

- **Philosophy**: Uses an LLM (GPT-4 or similar) as a judge to score your pipeline on the metrics above.
- **How it works**:
    1. You provide a dataset of `(Question, Answer, Contexts, GroundTruth)`.
    2. Ragas prompts the "Judge LLM" to grade the components (0.0 to 1.0).
    3. Example: To measure *Faithfulness*, it asks the Judge: "Break down the answer into statements. For each statement, verify if it is supported by the context."

### TruLens

- **Philosophy**: Similar "LLM-as-a-judge" approach but focuses on "Feedback Functions" and offers a dashboard to visualize traces.
- **Key Concept**: "RAG Triad" visualization (Context Relevance, Groundedness, Answer Relevance).

---

## 3. Creating a Golden Dataset

You cannot evaluate without data. You need a "Golden Dataset" or "Ground Truth".

### How to build it?

1. **Manual**: Collect real user queries and have experts write the ideal answers. (High quality, expensive).
2. **Synthetic (LLM-generated)**:
    - Feed your chunks to GPT-4.
    - Ask it: "Generate a question that can be answered by this specific chunk."
    - Ask it: "Generate the answer."
    - Result: A synthetic `(Question, GroundTruth, Context)` triplet.
3. **Cold Start**: Start with 50 synthetic questions. As users use your app, log their queries. Manually rate the answers to build up a real dataset over time.

---

## Summary Checklist

1. **Stop "eyeballing" results.**
2. **Pip install `ragas` or `trulens-eval`.**
3. **Build a dataset** of at least 50 test cases.
4. **Baseline your current pipeline** (e.g., "Faithfulness: 0.7, Recall: 0.6").
5. **Run experiments**: Change chunk size 500 -> 200. Re-run eval. Did scores go up?

---

## 4. Production: Online Evaluation & Cost

Evaluation doesn't stop at deployment.

### Online Evaluation (User Feedback)

- **Explicit Feedback**: Thumbs Up/Down buttons.
- **Implicit Feedback**:
  - **Acceptance Rate**: Did the user copy the code snippet?
  - **Session Length**: Did the user have to ask 10 clarifying questions (Bad) or just 1 (Good)?
  - **Edit Distance**: If the user edited the generated text, how much did they change?

### Managing Cost & Latency

Running "LLM-as-a-judge" on every production query is prohibitively expensive and slow.

- **Sampling**: Randomly select 5-10% of production logs for detailed Ragas/DeepEval grading.
- **Small Judge**: Use a smaller model (e.g., GPT-4o-mini or Claude Haiku) for the judge instead of the largest model. Distill the large model's judgment into the small one.
- **Asynchronous Eval**: Never run eval in the hot path. Push logs to a queue and evaluate in the background.

---

## 5. Optimization: What Parameters Matter?

To technically ensure your retrieval is "perfect", you must systematically tune these variables:

### A. Chunk Size & Overlap

- **The Trade-off**:
  - **Tiny chunks (<128 tokens)**: Great for pinpoint search ("What is the interest rate?"). Bad for reasoning ("Summarize the risks").
  - **Large chunks (>512 tokens)**: capturing context but adds noise.
- **Strategy**: Don't guess. Sweep chunk sizes [128, 256, 512, 1024] and run your Golden Dataset eval against each.

### B. Top-K (Retrieval Depth)

- **The Trade-off**:
  - **Low K (3)**: High precision needed. If the answer is in chunk #4, you miss it.
  - **High K (20)**: High recall likely, but you might drown the LLM in noise ("Lost in the Middle").
- **Strategy**: Retrieve 50 (Top-N) -> Re-rank -> Pass 5 (Top-K) to LLM.

### C. Hybrid Search Alpha

- **The Knob**: `alpha * Dense + (1-alpha) * Sparse`.
- **Strategy**:
  - User asks keyword-heavy questions (parts numbers, names)? -> **Lower Alpha** (0.2).
  - User asks conceptual questions? -> **Higher Alpha** (0.8).

---

## 6. Maintenance: How to Remain Confident?

"Perfect" today is broken tomorrow if you don't maintain it.

### A. Regression Testing (The "Do No Harm" Rule)

- **Problem**: You add a new marketing PDF. Suddenly, engineering questions start retrieving marketing fluff.
- **Solution**: Run your Golden Dataset (Regression Suite) *every time* you ingest a new batch of documents. If "Faithfulness" drops by >2%, rollback the ingestion.

### B. Data Hygiene (The "Knowledge Conflict" Problem)

- **Problem**: You have "Policy 2023" and "Policy 2024" in the vector DB. Both potentially match "What is the policy?"
- **Solution**:
  - **Time-aware retrieval**: Always filter by `date > X` or boost recent documents.
  - **De-duplication**: Use MinHash or strict hashing to prevent indexing the same document twice.

### C. Golden Dataset Evolution

- A static test set becomes useless.
- **Flywheel**: Every week, take 10 "thumbs down" queries from production, correct them, and add them to your Golden Dataset. Your test suite now covers your actual failure modes.

---

## 7. References & Resources

### Papers

- **Ragas Paper**: [Ragas: Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217)
- **LLM-as-a-Judge**: [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)

### Tools & Docs

- **Ragas Documentation**: [docs.ragas.io](https://docs.ragas.io/)
- **TruLens**: [trulens.org](https://www.trulens.org/)
- **Arize Phoenix**: [Open Source LLM Evals](https://docs.arize.com/phoenix/)
