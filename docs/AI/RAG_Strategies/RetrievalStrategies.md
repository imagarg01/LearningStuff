# RAG Retrieval Strategies

Retrieval is the "R" in RAG (Retrieval-Augmented Generation). The quality of your generation is fundamentally limited by the quality of your retrieval. If the LLM doesn't get the right context, no amount of prompt engineering can save it (garbage in, garbage out).

This document details various retrieval strategies, ranging from basic to advanced, and provides a guide on when to select which.

---

## 1. Foundations: Sparse vs. Dense Retrieval

### Sparse Retrieval (Keyword Search / BM25)

This is the traditional search method (like Lucene/Elasticsearch). It maps words to documents based on exact keyword matching.

- **Mechanism**: Approaches like TF-IDF or **BM25** (Best Matching 25) calculate relevance based on how often a term appears in a document relative to the entire corpus.
- **Pros**:
  - precise for specific keywords (identifiers, names, acronyms).
  - Explainable.
  - Computationally cheap.
- **Cons**:
  - Fails with synonyms (e.g., "car" won't match "automobile").
  - Ignores semantic meaning.

### Dense Retrieval (Vector Search)

This uses Deep Learning models (Embeddings) to represent text as high-dimensional vectors. Use cosine similarity to find "nearest neighbors".

- **Mechanism**: A Bi-Encoder model converts the query and documents into vectors.
- **Pros**:
  - Captures semantic meaning (e.g., "fast" matches "quick").
  - Handles multilingual queries well.
- "Out of domain" problems: if the embedding model wasn't trained on your specific jargon, it might map concepts poorly.

### Choosing an Embedding Model (MTEB)

Not all embeddings are created equal. Use **MTEB (Massive Text Embedding Benchmark)** to choose.

- **Leaderboard**: [Hugging Face MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- **Key Dimensions**:
  - **Performance**: Look for high scores in "Retrieval".
  - **Context Window**: 512 (BERT) vs 8192 (OpenAI).
  - **Dimensions**:
    - **1536** (OpenAI default): High quality, expensive storage.
    - **384** (MiniLM): Fast, cheap, good for simple use cases.
  - **Matryoshka Embeddings**: Newer models (like `text-embedding-3`) let you shorten vectors (e.g., 1024 -> 256) while keeping most performance.

---

## 2. Advanced Strategies

### Hybrid Search

**Strategy**: Combine Sparse and Dense retrieval to get the best of both worlds.

- **How it works**: Run BM25 and Vector Search in parallel. Combine their scores.
- **Fusion Algorithms**:
  - **Reciprocal Rank Fusion (RRF)**: Rank-based method. sum(1 / (k + rank)). Robust and doesn't require normalizing disparate scores.
  - **Convex Combination**: weighted_score = alpha *dense_score + (1 - alpha)* sparse_score.

### Re-ranking (Two-Stage Retrieval)

**Strategy**: Retrieve a large set of candidates cheaply, then sort the best ones using a more expensive, accurate model.

- **Stage 1 (Retrieval)**: Get top 50-100 results using Hybrid or Dense search (Bi-Encoder). Fast.
- **Stage 2 (Re-ranking)**: Use a **Cross-Encoder**.
  - A Cross-Encoder takes the pair `(Query, Document)` as input and outputs a relevance score. Integrating the query and document early allows for deep interaction between their tokens (self-attention).
- **Benefit**: dramatically improves precision.
- **Cost**: Slower and more expensive than Bi-encoders. Only run on the top N candidates.

### Query Transformations

Often the user's query is poorly formulated for retrieval. We can transform it before searching.

1. **Query Expansion / Multi-Query**:
    - Use an LLM to generate synonyms or alternative phrasings of the query.
    - Retrieve for *all* variations and dedup/pool the results.
2. **Query Decomposition**:
    - Break a complex question ("Compare the revenue of Apple and Microsoft in 2023") into sub-questions ("What was Apple's revenue in 2023?", "What was MSFT's?").
    - Retrieve and answer individually.
3. **HyDE (Hypothetical Document Embeddings)**:
    - Ask LLM to *hallucinate* a hypothetical answer to the question.
    - Embed the *answer*, not the question.
    - **Why?** The answer is semantically closer to the documents you want to find than the question is.

### Contextual Retrieval

**Problem**: When you chunk a document, a chunk might say "The company revenue grew by 5%". Without the parent document context, we don't know *which* company.
**Strategy (Anthropic's approach)**:

- Pre-process: Use an LLM to generate a minimal explanation of the context for each chunk *before* embedding.
- Prepend: "This chunk is from the 2023 Financial Report of Acme Corp..." -> "The company revenue grew..."
- Result: The chunk is now retrievable by queries about "Acme Corp" even if the chunk didn't mention it.

### Metadata Filtering (Self-Querying)

**Strategy**: Use document attributes (Date, Author, Category) to narrow the search space.

- **Pre-filtering**: Filter *before* vector search. fast, but if filter is too strict, you might get zero results.
- **Post-filtering**: Retrieve first, then filter. Can result in retrieving N docs, filtering them all out, and returning nothing.
- **Self-Querying**: Use an LLM to extract filters from the user's natural language question (e.g., "Show me emails from last week" -> `{ "date": "> now-7d", "type": "email" }`).

---

## 3. Supervised Retrieval

When generic models aren't enough, you can "teach" the system your domain.

### Fine-tuning Embedding Models

- **What**: Adapt the Bi-encoder (e.g., BERT-based) on your specific data.
- **Data Needed**: `(Positive_Query, Positive_Document)` pairs (and ideally negatives).
- **Use Case**: Highly specialized domains (Structure biology, ancient law) where general semantic relationships don't hold.
- **Architecture**: Contrastive Learning (MNRL - Multiple Negatives Ranking Loss).

### Learning to Rank (LTR)

- **What**: Train a specialized model just for the ranking phase.
- **Models**:
  - **XGBoost / LightGBM**: Feature-based ranking. Features can be BM25 score, cosine similarity, document freshness, click-through rate (CTR), etc.
  - **Deep Learning**: Fine-tuning a Cross-Encoder specifically for ranking your documents.
- **Use Case**: E-commerce, large-scale search engines where you have user interaction data (clicks).

---

## 4. Selection Guide: When to choose what?

| Use Case / Constraint | Recommended Strategy | Why? |
| :--- | :--- | :--- |
| **Simple / PoC** | **Naive Dense Retrieval** | Use a standard vector DB. Fast to set up. Good enough for 80% of general cases. |
| **Specific Identifiers** (Product SKUs, Names) | **Hybrid Search (Dense + Sparse)** | Vector search fails at exact matches; BM25 complements it perfectly. |
| **Ambush of Precision** | **Re-ranking** | If users complain irrelevant docs are in top 3 positions. |
| **Complex User Queries** | **Query Decomposition / Multi-Query** | If one single vector lookup can't capture the multi-faceted intent. |
| **Domain Mismatch** (e.g., Medical codes) | **Fine-tuning Embeddings** | Generic models won't know that "Code 123" is related to "Disease X". |
| **Latency Critical (<50ms)** | **Sparse or Dense Only (No Re-ranking)** | Re-ranking or HyDE adds significant latency (hundreds of ms). |
| **Small Chunks losing meaning** | **Contextual Retrieval** | Adds parent context so chunks stand on their own. |

### Summary Flowchart

1. **Start** with **Naive RAG** (Standard Embeddings).
2. *Verification*: Are results good? -> Done.
3. *Issue*: Misses exact keywords? -> Add **Hybrid (BM25)**.
4. *Issue*: Top results are loosely related but not precise? -> Add **Re-ranking**.
5. *Issue*: Questions are too vague or complex? -> Add **Query Transformations**.
6. *Issue*: Domain jargon is completely misunderstood? -> **Fine-tune Embeddings**.

---

## 5. Expert Strategies (State of the Art)

### GraphRAG (Knowledge Graphs + Vector)

**Problem**: Vector search fails at "Global Questions" (e.g., "What are the main themes in this dataset?") or "Multi-hop Reasoning" where documents don't explicitly overlap but share entities.
**Strategy**:

- Build a **Knowledge Graph** (Nodes = Entities, Edges = Relationships) from your documents.
- Use **Community Detection** (Leiden algorithm) to cluster related entities.
- **Retrieval**:
  - **Local Search**: Traverse edges to find related concepts (e.g., "Apple" -> "Tim Cook" -> "Biography").
  - **Global Search**: Summarize entire communities to answer high-level questions.

### ColBERT (Late Interaction)

**Problem**: Bi-Encoders are fast but lose nuance (compressing 500 words into 1 vector). Cross-Encoders are accurate but slow (full O(n^2) attention).
**Strategy**:

- **Late Interaction**: Encode query and document tokens *independently* (like Bi-Encoder) but keep *all* token vectors (MaxSim operation).
- **Mechanism**: Calculates a "MaxSim" matrix between every query token and every document token.
- **Result**: Accuracy close to GPT-4 re-ranking with latency close to standard vector search.

### Agentic RAG

**Problem**: Naive RAG is a linear pipeline. If retrieval fails, generation fails.
**Strategy**: Turn the RAG system into an **Agent** that can use tools.

- **Self-RAG**: The model generates a "Critique Token" evaluating its own retrieval. If low quality, it re-writes the query.
- **Corrective RAG (CRAG)**: An external evaluator checks the document relevance.
  - *Correct*: Proceed to generate.
  - *Incorrect*: Search the Web (Google Search Tool).
  - *Ambiguous*: Ask clarifying question.

---

## 6. References & Further Reading

### Key Papers

- **Original RAG Paper**: [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- **DPR (Dense Passage Retrieval)**: [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906) - The foundation of dense retrieval.
- **HyDE**: [Precise Zero-Shot Dense Retrieval without Relevance Labels](https://arxiv.org/abs/2212.10496)
- **Lost in the Middle**: [How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) - Why re-ranking and context precision matter.

### Useful Articles & Guides

- [Pinecone Learning Center](https://www.pinecone.io/learn/) - Excellent visual guides on Vector Search and RAG.
- [LangChain RAG Docs](https://python.langchain.com/docs/expression_language/cookbook/retrieval) - Practical implementation patterns.
- [Anthropic: Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) - Source for the Contextual Retrieval strategy.
