# Retrieval-Augmented Generation (RAG) — Executive Entry Point

There are three core retrieval paradigms in modern AI engineering:

## 1. Sparse (Lexical) Retrieval

About 50 years old, relying on exact keyword matching and statistical term weighting via **TF-IDF** or **BM25** (Best Matching 25). TF-IDF measures the importance of a word in a document relative to a corpus, while BM25 improves upon TF-IDF by adding **term frequency saturation** and **document length normalization**.

- **Pros**:
  - Simple, fast, deterministic, and highly scalable (inverted index)
  - Cost-effective (does not require neural embedding models)
  - Excels at exact matches: SKU numbers, error codes, function names, and legal citations
- **Cons**:
  - Cannot handle synonyms or paraphrases ("automobile" vs. "car")
  - Lacks semantic context and word-order awareness

## 2. Dense (Semantic Vector) Retrieval

Relying on neural embeddings and vector similarity. Text chunks are passed through an embedding model to create high-dimensional dense vectors, and similarity is measured using Cosine Similarity or Dot Product via Approximate Nearest Neighbor (ANN / HNSW) indexes.

- **Pros**:
  - Captures semantic meaning, intent, and cross-lingual similarity
  - Handles synonyms and conceptual queries well
  - Strong baseline for unstructured knowledge bases
- **Cons**:
  - Can miss exact rare identifiers, SKUs, or domain jargon
  - Embedding space compression loses fine-grained structural relationships

## 3. Hybrid Search, Cross-Encoder Reranking, & Agentic/Graph Retrieval (Modern Production Standard)

Production RAG systems rarely rely on Sparse or Dense retrieval alone. Instead, they combine multiple retrieval stages and structural reasoning:

1. **Hybrid Search + Reciprocal Rank Fusion (RRF)**: Executes Sparse (BM25) and Dense (Vector) retrieval in parallel and merges the ranked lists using RRF:
   $$\text{RRF\_Score}(d) = \sum_{m \in \{\text{BM25}, \text{Dense}\}} \frac{1}{k + \text{rank}_m(d)} \quad (k \approx 60)$$
2. **Cross-Encoder / Late-Interaction Reranking**: Takes the top-50 candidates from Hybrid Search and scores query-document pairs jointly with a Cross-Encoder or ColBERT model to select the highest-precision top-5 chunks.
3. **Vectorless / Reasoning-Based RAG (PageIndex)**: Navigates hierarchical document trees (Table-of-Contents / ASTs) via agentic reasoning rather than flat chunking—ideal for long financial or legal PDFs where "similarity $\neq$ relevance".
4. **GraphRAG & Context Graphs**: Connects entities, temporal rules, and organizational decision traces into a traversable graph for multi-hop reasoning.
5. **Recursive Language Models (RLM)**: Treats massive corpora ($10\text{M}+$ tokens) as an external REPL environment where the root LLM writes code and spawns sub-LLM queries recursively instead of stuffing the prompt.

---

## Deep-Dive Modules in Act III (Memory, Context, & Knowledge Grounding)

* **Master Narrative Index:** [00_Master_Story_and_Index.md](./00_Master_Story_and_Index.md)
* **Comprehensive RAG Playbook (7 Strategies):** [RAG_Strategies/RetrievalStrategies.md](./RAG_Strategies/RetrievalStrategies.md)
* **Vectorless / Tree-Index RAG:** [RAG/VectorlessRAG.md](./RAG/VectorlessRAG.md)
* **Organizational Decision Lineage (Context Graphs):** [Context_Graph/ContextGraph.md](./Context_Graph/ContextGraph.md)
* **Beyond Context Limits (Recursive Language Models):** [RLM/RecursiveLanguageModels.md](./RLM/RecursiveLanguageModels.md)
