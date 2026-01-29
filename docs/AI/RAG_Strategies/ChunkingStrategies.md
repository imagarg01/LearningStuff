# RAG Chunking Strategies

**Chunking** is the process of breaking down large documents into smaller, manageable pieces (chunks) for retrieval. It is the **foundation** of your RAG pipeline.

> "Bad chunking leads to bad retrieval, no matter how good your embedding model is."

If a chunk is too small, it lacks context. If it's too large, it contains noise. If it splits a sentence in half, semantic meaning is lost.

---

## 1. Fixed-Size Chunking (The Baseline)

The simplest method. You split text into chunks of a fixed number of characters or tokens, usually with some overlap to maintain continuity across boundaries.

- **Pros**: Computationally cheap, easy to implement.
- **Cons**: Breaks semantic meaning (e.g., splitting a sentence in the middle).
- **When to use**: Exploratory Data Analysis (EDA), simple PoCs.

### Code Example (LangChain)

```python
from langchain.text_splitter import CharacterTextSplitter

text = "RAG is a technique ... [long text] ..."

# Split by characters (not ideal, but fast)
splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

chunks = splitter.create_documents([text])
```

---

## 2. Recursive Character Chunking (The Standard)

This is the **default recommendation** for most text-based applications. It tries to split on the largest logical separators first (paragraphs `\n\n`), then sentences (`\n`), then words (` `), and finally characters if necessary.

- **Pros**: Keeps related text together (paragraphs remain intact mostly).
- **Cons**: Still doesn't understand the *meaning* of the text, just the structure.

### Code Example

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    # List of separators to try in order
    separators=["\n\n", "\n", " ", ""],
    chunk_size=512,
    chunk_overlap=50,
    length_function=len,
)

chunks = splitter.create_documents([text])
```

---

## 3. Semantic Chunking (The Smart Way)

Instead of splitting by character count, we split by **meaning**. We use an embedding model to calculate the similarity between sentences. If the similarity drops below a threshold (a "topic shift"), we start a new chunk.

- **Pros**: Creates highly coherent chunks.
- **Cons**: Slower (requires model inference), requires tuning the threshold.

### Conceptual Logic

1. Split text into sentences.
2. Embed every sentence.
3. Compare `Sentence[i]` with `Sentence[i+1]`.
4. If `CosineSimilarity < Threshold`, break. Else, merge.

### Code Example (Experimental)

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# Requires an embedding model
embeddings = OpenAIEmbeddings()

splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile" # or "standard_deviation"
)

docs = splitter.create_documents([text])
```

---

## 4. Agentic Chunking (The Expert Way)

Allow an LLM to decide where to split. You treat the text as a stream and ask the LLM: "Does this new sentence belong to the current chunk (Topic A) or is it a start of a new topic?"

- **Pros**: Extremely high quality boundaries.
- **Cons**: Extremely slow and expensive (LLM call per sentence/paragraph).
- **Use Case**: High-value legal contracts or financial reports where accuracy is paramount.

---

## 5. Visual Guide to Splits

Imagine the text:
`"Apple reported huge profits. The stock soared. // Meanwhile, Microsoft announced a new AI tool."`

- **Fixed (Size 5)**: `["Apple", " repor", "ted h"]` -> Garbage.
- **Recursive**: `["Apple reported huge profits.", "The stock soared.", "Meanwhile..."]` -> Better.
- **Semantic**: `["Apple reported huge profits. The stock soared."]`, `["Meanwhile, Microsoft announced a new AI tool."]` -> Best (Separates "Apple financials" from "Microsoft AI").

---

## Summary Recommendation

| Use Case | Strategy | Chunk Size | Overlap |
| :--- | :--- | :--- | :--- |
| **General Text / Docs** | **Recursive Character** | 512 tokens | 10% (50 tokens) |
| **Code** | **Language Specific** (Python/JS splitters) | 1024 tokens | 0% |
| **Imbalanced Topics** | **Semantic Chunking** | Variable | N/A |
| **Conversations** | **Message-based** | 1 session/window | N/A |
