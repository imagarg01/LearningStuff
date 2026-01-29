import asyncio
import re
from typing import List, Dict

# MockTextSplitter to demonstrate Recursive Splitting logic without heavy dependencies
class RecursiveSplitter:
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> List[str]:
        """
        Naive implementation of recursive splitting for demonstration.
        """
        final_chunks = []
        if len(text) <= self.chunk_size:
            return [text]
        
        # Try to find the best separator
        separator = self.separators[-1]
        for sep in self.separators:
            if sep in text:
                separator = sep
                break
        
        # Split
        if separator:
            splits = text.split(separator)
        else:
            splits = list(text) # Character split

        # Merge back up to chunk size
        current_chunk = ""
        for s in splits:
            if len(current_chunk) + len(s) + len(separator) < self.chunk_size:
                current_chunk += (separator if current_chunk else "") + s
            else:
                if current_chunk:
                    final_chunks.append(current_chunk)
                current_chunk = s
        
        if current_chunk:
            final_chunks.append(current_chunk)
            
        return final_chunks

# Semantic Chunking Simulation
def semantic_chunking_simulation(text: str) -> List[str]:
    """
    Simulates semantic chunking by splitting on evident topic shifts 
    (represented here by double newlines or specific markers for the example).
    In reality, this uses cosine similarity of embeddings.
    """
    # Simulate embedding-based decision: "Apple" vs "Microsoft" are different topics
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_topic = []
    
    for sentence in sentences:
        if "Microsoft" in sentence and any("Apple" in s for s in current_topic):
            # Simulated Topic Shift detected
            chunks.append(" ".join(current_topic))
            current_topic = [sentence]
        else:
            current_topic.append(sentence)
    
    if current_topic:
        chunks.append(" ".join(current_topic))
    
    return chunks

def main():
    sample_text = (
        "Apple released its quarterly earnings report today. Revenue exceeded expectations driven by iPhone sales. "
        "The stock price jumped 5% in after-hours trading.\n\n"
        "Meanwhile, Microsoft unveiled a new AI Copilot feature for Windows. "
        "This tool integrates deeply with the OS to automate tasks. "
        "Analysts believe this will drive Azure adoption."
    )

    print("--- 1. Recursive Chunking (Size=100) ---")
    splitter = RecursiveSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split_text(sample_text)
    for i, c in enumerate(chunks):
        print(f"Chunk {i+1}: {c!r}")

    print("\n--- 2. Semantic Chunking (Simulated) ---")
    sem_chunks = semantic_chunking_simulation(sample_text)
    for i, c in enumerate(sem_chunks):
        print(f"Chunk {i+1}: {c!r}")

if __name__ == "__main__":
    main()
