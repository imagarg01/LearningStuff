There are three retrieval strategies:

1. Sparse Retrieval

About 50 years old, relying on keyword matching. Relies on TF-IDF or BM25 algorithms. TF-IDF stands for Term Frequency-Inverse Document Frequency, which measures the importance of a word in a document relative to a collection of documents. BM25 is an improved- About 50 years old, relying on keyword matching. Relies on TF-IDF or BM25 algorithms.

- Pros are:
- Simple, fast, and scalable
- Cost Effective
- Does not require embeddings

- Cons are:
  - Not handle synonyms
  - Having lack of context

Use where exact match is needed, such as legal or technical documents.

2. Dense Retrieval

About 10 years old, relying on embeddings and vector similarity. Uses models like BERT to create dense vector representations of text. Texts are converted into high-dimensional vectors, and similarity is measured using metrics like cosine similarity. Similarity is calculated using algorithms like approximate nearest neighbors (ANN) or KNN.

- Pros are:
- Better at capturing semantic meaning
- Handles synonyms and context better
- Perfect for chatbots, customer service and research over unstructured knowledge bases.

- Cons are:
  - Can miss rare or Jargon words
