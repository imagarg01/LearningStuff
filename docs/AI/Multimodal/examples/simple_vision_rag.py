import torch
import torch.nn.functional as F

# Multimodal RAG Simulation
# Real CLIP requires downloading ~500MB weights. 
# We simulate the "Shared Embedding Space" concept math.

class MockCLIP:
    """Simulates a model that embeds both Text and Images into the same 512d space."""
    def __init__(self):
        self.dim = 512
        
    def encode_text(self, texts):
        # In reality, this runs a Transformer
        # Simulation: Deterministic random vectors for demo
        torch.manual_seed(42) 
        return F.normalize(torch.randn(len(texts), self.dim), p=2, dim=1)

    def encode_image(self, image_names):
        # In reality, this runs a ViT
        # Simulation: Make "dog.jpg" vector similar to "photo of a dog" text
        torch.manual_seed(42) 
        # Add slight noise to simulate "almost same"
        base = F.normalize(torch.randn(len(image_names), self.dim), p=2, dim=1)
        noise = torch.randn_like(base) * 0.1
        return F.normalize(base + noise, p=2, dim=1)

def main():
    print("--- Multimodal RAG (CLIP Simulation) ---")
    model = MockCLIP()
    
    # Database of Images
    images = ["dog.jpg", "chart_of_sales.png", "cat.jpg"]
    print(f"Indexing Images: {images}...")
    img_embeddings = model.encode_image(images)
    
    # User Query
    query = "A photo of a golden retriever"
    print(f"\nUser Query: '{query}'")
    text_embedding = model.encode_text([query]) # In simulation, seed 42 makes this close to img[0]
    
    # Retrieval (Cosine Similarity)
    # text @ img.T
    scores = text_embedding @ img_embeddings.T
    
    print("\nRetrieval Scores:")
    probs = scores.softmax(dim=1)
    for i, img in enumerate(images):
        print(f"{img}: Similarity = {scores[0][i]:.4f} (Prob: {probs[0][i]:.2%})")
        
    best_idx = scores.argmax()
    print(f"\nRetrieved: {images[best_idx]}")
    
    if images[best_idx] == "dog.jpg":
        print("Success! The text query retrieved the semantically similar image.")
    else:
        print("Simulation artifact: Match failed (expected in random simulation).")

if __name__ == "__main__":
    main()
