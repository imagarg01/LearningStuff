# Multimodal AI: Seeing Beyond Text

Multimodal AI processes multiple types of data (Text, Image, Audio) simultaneously. The most critical component for modern RAG is the **Vision Transformer (ViT)** and embedding models like **CLIP**.

---

## 1. Core Concepts

### A. Vision Transformers (ViT)

- **Old Way (CNNs)**: Convolutions look at local pixels (edges -> shapes -> objects) like sliding a window.
- **New Way (ViT)**:
  1. Break image into $16 \times 16$ patches (like tokens in text).
  2. Flatten patches into vectors.
  3. Feed vectors into a standard Transformer Encoder.
  - **Result**: Global attention across the entire image instantly.

### B. CLIP (Contrastive Language-Image Pre-training)

- **Problem**: How do you make an image of a dog "mathematically similar" to the text "a photo of a dog"?
- **Solution**: OpenAi trained two encoders (One for Image, One for Text).
- **Training**: Maximizing cosine similarity between correct `(Image, Text)` pairs and minimizing it for incorrect ones.
- **Magic**: You can now search your image database using text queries. `query_embedding("dog")` matches `image_embedding(dog_pic)`.

---

## 2. Multimodal RAG Strategies

How do you RAG with PDFs containing charts?

### Strategy A: Image-to-Text (Captioning)

1. Use an **LMM (Large Multimodal Model)** like GPT-4o, LLaVA, or BLIP.
2. Ask it to "Describe this chart in detail."
3. Save the text description into your Vector DB.
4. Retrieve using standard text search.

- **Pros**: Easy.
- **Cons**: You lose visual nuances.

### Strategy B: Multi-Vector Retrieval (ColPali)

1. Embed the Image (using CLIP/SigLIP).
2. Embed the User Query (Text).
3. Search in the joint embedding space.
4. Feed the raw image + text to the LMM for the final answer.

- **Pros**: Highest fidelity.
- **Cons**: Requires specialized Vector DBs (Weaviate, Qdrant) and embedding models.

---

## 3. Libraries to Know

- **Transformers (HuggingFace)**: `CLIPProcessor`, `ViTForImageClassification`.
- **Llava**: Open source equivalent of GPT-4 Vision.
- **Timm (PyTorch Image Models)**: Massive collection of pre-trained vision backbones.
