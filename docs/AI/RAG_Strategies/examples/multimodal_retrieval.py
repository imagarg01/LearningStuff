from sentence_transformers import SentenceTransformer, util
from PIL import Image
import torch
import os

# NOTE: In a real scenario, you would have distinct image files
# like 'dog.jpg', 'cat.jpg', 'beach.jpg' in your directory.
# This script simulates the embedding part.

def main():
    print("--- Multimodal Retrieval (Text-to-Image with CLIP) ---")
    
    # 1. Load CLIP model
    # This model can embed both Images and Text into the SAME vector space
    model_name = "sentence-transformers/clip-ViT-B-32"
    print(f"Loading CLIP model: {model_name}...")
    model = SentenceTransformer(model_name)
    
    # 2. Mock Images
    # We will create dummy images just for the data structure, 
    # but in reality you load: Image.open("path/to/image.jpg")
    print("Creating mock images...")
    img_descriptions = [
        "Two dogs running in the snow",
        "A red sports car driving on a highway",
        "A plate of sushi on a wooden table",
        "A corporate meeting in a glass office",
        "A galaxy with spiral arms in deep space"
    ]
    
    # Since we don't have actual files, we will use the text capability of CLIP
    # to simulate "image embeddings" by embedding their descriptions.
    # In production: image_embeddings = model.encode([Image.open(f) for f in files])
    image_embeddings = model.encode(img_descriptions)
    
    print(f"Indexed {len(img_descriptions)} 'images'.")
    
    # 3. Text Query
    user_query = "Automobile moving fast"
    print(f"\nUser Query: '{user_query}'")
    
    # 4. Retrieval
    # Embed the text query
    query_embedding = model.encode(user_query)
    
    # Compute Cosine Similarity
    hits = util.semantic_search(query_embedding, image_embeddings, top_k=2)
    
    # 5. Results
    print("\nTop Matches:")
    for hit in hits[0]:
        idx = hit['corpus_id']
        score = hit['score']
        print(f"- [Score: {score:.4f}] {img_descriptions[idx]}")
        
    print("\n(Note: In a real app, this would return the actual image file path)")

if __name__ == "__main__":
    main()
