# LLM Inference Strategies: From Laptop to Production

Running an LLM efficiently is a completely different skill from training one. In production, **Latency** (time to first token) and **Throughput** (requests per second) are king.

---

## 1. The Inference Landscape

| Engine | Best For | Key Features | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **vLLM** | **Production (GPU)** | PagedAttention, Continuous Batching | State-of-the-art throughput. Industry standard for high-scale. | Requires NVIDIA GPUs (mostly). |
| **TGI** (HuggingFace) | **Production (Docker)** | Tensor Parallelism, Rust backend | Very easy deployment (Docker container). Robust. | Slightly slower than vLLM in some benchmarks. restrictively licensed for very large use. |
| **Ollama** | **Local / Dev (CPU/Mac)** | GGUF support, Modelfiles | Easiest UX. "Docker for LLMs". Runs on specific hardware (Apple Silicon). | Not optimized for massive concurrent batching like vLLM. |
| **Llama.cpp** | **Edge / CPU / Mac** | GGUF format | Runs on *anything* (Raspberry Pi, Android, Mac). | Lower throughput than vLLM. |
| **CTranslate2** | **CPU Production** | C++ backend, INT8 quantization | Extremely fast on CPU. Good for non-generative tasks (Embeddings/Translation). | Complex API. |

---

## 2. Key Concepts in High-Performance Inference

### A. PagedAttention (The vLLM Breakthrough)

Standard attention algorithms reserve contiguous memory for the KV (Key-Value) cache. This leads to massive memory fragmentation (waste).

- **PagedAttention** breaks the KV cache into non-contiguous blocks (like OS virtual memory).
- **Result**: Near 0% memory waste, allowing much larger batch sizes.

### B. Continuous Batching

- **Old Way (Static Batching)**: Group 10 requests. Wait for *all* to finish generation before sending the batch back. If one request generates 1000 tokens and others generate 10, the GPU is idle for the small ones.
- **New Way (Continuous/Iteration Batching)**: As soon as request A finishes, eject it and insert request B *mid-stream*. The GPU is always 100% utilized.

### C. Speculative Decoding

- **Idea**: Use a small "Draft Model" (e.g., Llama-7B) to guess the next 5 tokens cheaply. Then, use the Main Model (e.g., Llama-70B) to verify them in one parallel pass.
- **Gain**: Can speed up inference by 2-3x if the prompts are predictable.

---

## 3. Hardware Selection Guide

| Model Size | Quantization | VRAM Needed | Recommended GPU |
| :--- | :--- | :--- | :--- |
| **7B** | FP16 | ~16 GB | RTX 3090 / 4090 / A10G |
| **7B** | 4-bit (GGUF) | ~6 GB | RTX 3060 / Laptop GPU |
| **70B** | FP16 | ~140 GB | 2x A100 (80GB) |
| **70B** | 4-bit (AWQ) | ~35 GB | 1x A6000 Ada / 2x RTX 3090 (NVLink) |
| **Mixtral 8x7B**| 4-bit | ~26 GB | 1x RTX 3090 / A100 |

> **Rule of Thumb**: For FP16 loading, you need `2GB VRAM` per `1 Billion Params`. For 4-bit, you need `0.7GB` per `1B`.
