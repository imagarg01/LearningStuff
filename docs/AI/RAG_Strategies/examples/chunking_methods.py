import os
from typing import List
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter, 
    MarkdownHeaderTextSplitter,
    Language
)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

# Sample Text Data
SAMPLE_TEXT = """
Apple released its quarterly earnings report today. Revenue exceeded expectations, driven by strong iPhone 15 sales in Asian markets. 
The stock price jumped 5% in after-hours trading, reaching a new all-time high. 
Analysts have upgraded their price targets, citing robust services growth.

Meanwhile, Microsoft unveiled a new AI Copilot feature for Windows 11. 
This tool integrates deeply with the OS to automate tasks like summarizing emails and generating content. 
Satya Nadella called it "a new era of computing" during the keynote. Azure usage is expected to spike as a result.
"""

SAMPLE_MARKDOWN = """
# RAG Strategies
RAG stands for Retrieval Augmented Generation.

## Chunking
Chunking is the process of breaking text.
### Fixed Size
Fixed size is simple but dumb.
### Semantic
Semantic is smart but slow.

## Embedding
Embeddings turn text into vectors.
"""

SAMPLE_PYTHON = """
class RAGPipeline:
    def __init__(self, model_name):
        self.model = model_name
    
    def retrieve(self, query):
        # Retrieve relevant docs
        return []

def main():
    rag = RAGPipeline("gpt-4")
    print(rag.retrieve("hello"))
"""

def run_recursive_chunking():
    print("\n--- 1. Recursive Character Chunking ---")
    print("(Splits by paragraphs, then sentences. Good for general text.)")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=20,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.create_documents([SAMPLE_TEXT])
    
    for i, chunk in enumerate(chunks):
        print(f"[{i+1}] {chunk.page_content!r}")

def run_markdown_chunking():
    print("\n--- 2. Markdown Header Chunking ---")
    print("(Preserves header hierarchy in metadata. Good for docs.)")
    
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    chunks = splitter.split_text(SAMPLE_MARKDOWN)
    
    for i, chunk in enumerate(chunks):
        print(f"[{i+1}] Content: {chunk.page_content!r}")
        print(f"      Metadata: {chunk.metadata}")

def run_code_chunking():
    print("\n--- 3. Python Code Chunking ---")
    print("(Keeps classes and functions together.)")
    
    splitter = RecursiveCharacterTextSplitter.from_language(
        Language.PYTHON, 
        chunk_size=100, 
        chunk_overlap=0
    )
    chunks = splitter.create_documents([SAMPLE_PYTHON])
    
    for i, chunk in enumerate(chunks):
        print(f"[{i+1}] {chunk.page_content!r}")

def run_semantic_chunking():
    print("\n--- 4. Semantic Chunking (Experimental) ---")
    print("(Splits when topic changes. Using local HF Embeddings - might be slow first run.)")
    
    try:
        # distinct color for semantic chunking
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        splitter = SemanticChunker(
            embeddings, 
            breakpoint_threshold_type="percentile" # Splits at spikes in dissimilarity
        )
        
        chunks = splitter.create_documents([SAMPLE_TEXT])
        for i, chunk in enumerate(chunks):
            print(f"[{i+1}] {chunk.page_content!r}")
            
    except Exception as e:
        print(f"Skipping Semantic Chunking due to error (likely missing dependency or model download): {e}")

def main():
    print("=== RAG Chunking Strategies Demo ===")
    run_recursive_chunking()
    run_markdown_chunking()
    run_code_chunking()
    run_semantic_chunking()

if __name__ == "__main__":
    main()
