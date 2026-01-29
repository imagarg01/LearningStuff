# Edge AI & SLMs: Intelligence Everywhere

The future of AI is not just massive models in the cloud. It's **Small Language Models (SLMs)** running locally on your phone, laptop, or browser.

---

## 1. Why Edge AI? (The "Why")

1. **Privacy**: Data never leaves the device. (Critical for Healthcare/Finance).
2. **Latency**: No network round-trip. Instant response.
3. **Cost**: Zero inference cost after deployment. No GPU cloud bills.
4. **Offline**: Works without internet.

---

## 2. Strong Contenders (The "Who")

| Model | Size | Best For |
| :--- | :--- | :--- |
| **Phi-3 (Microsoft)** | 3.8B | Reasoning & Coding. Beats Llama-2-7b. |
| **Gemma-2 (Google)** | 2B / 9B | General chatbot. Open weights. |
| **Llama-3.2 (Meta)** | 1B / 3B | Specifically optimized for edge devices (Snapdragon). |
| **Qwen-2-0.5B** | 0.5B | Extremely lightweight (IoT devices). |

---

## 3. The Stack (The "How")

### A. WebLLM (In-Browser)

- **Tech**: WebGPU + WASM.
- **Workflow**:
  1. User visits website.
  2. Browser downloads 2GB quantized model (cached).
  3. Inference happens on user's Laptop GPU.
- **Library**: `mlc-llm`.

### B. Mobile (iOS/Android)

- **Tech**: CoreML (Apple Neural Engine) / TFLite.
- **Library**: `executorch` (PyTorch for Edge).

### C. Local Desktop

- **Tech**: Ollama / Llama.cpp.
- **Workflow**: Background service exposes `localhost:11434` API.

---

## 4. Implementation Strategy

1. **Quantize heavily**: Use 4-bit (q4_k_m) or even 3-bit.
2. **Speculative Decoding**: Use a tiny draft model (100M) to speed up the main SLM (3B).
3. **Hybrid RAG**: Run retrieval locally (SQLite + Vector Extension) and Generation locally.
