# Quantization Guide: Squeezing Giants onto Laptops

Quantization allows us to run massive models on smaller hardware by reducing the precision of the weights. We trade a tiny bit of accuracy for massive gains in speed and memory efficiency.

---

## 1. The Formats: From 32-bit to 1-bit

| Precision | Name | Size (Per Param) | Use Case | Accuracy Loss |
| :--- | :--- | :--- | :--- | :--- |
| **FP32** | "Full Precision" | 4 bytes | Training (Golden Master) | 0% |
| **FP16 / BF16** | "Half Precision" | 2 bytes | Fine-Tuning / High-end Inference | <1% (Negligible) |
| **INT8** | 8-bit Integer | 1 byte | CPU Inference | Low |
| **INT4** | 4-bit Integer | 0.5 bytes | **The Standard** for Deployment | Noticeable but acceptable |
| **1.58-bit** | Ternary (BitNet) | ~0.2 bytes | Research / Future | Varies |

---

## 2. The Techniques: GGUF vs AWQ vs GPTQ

When you download a model from HuggingFace (TheBloke or MaziyarPanahi), you see these acronyms. Which one do you pick?

### A. GGUF (GPT-Generated Unified Format)

- **Engine**: **Llama.cpp**, **Ollama**, **LM Studio**.
- **Hardware**: **Apple Silicon (Mac M1/M2/M3)**, CPUs, Older GPUs.
- **Why**: It is designed for CPU+GPU split (offloading). If the model doesn't fit in VRAM, it seamlessly overflows to System RAM.
- **Best for**: Usage on simple Macbooks or consumer PCs.

### B. AWQ (Activation-aware Weight Quantization)

- **Engine**: **vLLM**, **TGI**.
- **Hardware**: **NVIDIA GPUs**.
- **Why**: Faster than GPTQ for inference. It protects the "salient" weights (important ones) based on activation data.
- **Best for**: Production API servers running vLLM.

### C. GPTQ (Generalized Post-Training Quantization)

- **Engine**: Older AutoGPTQ, ExLlamaV2.
- **Hardware**: NVIDIA GPUs.
- **Status**: Slowly being replaced by AWQ and EXL2.

---

## 3. How to Quantize?

You generally don't quantize yourself; you download pre-quantized models. But if you must:

### Using `llama.cpp` (to make GGUF)

```bash
python convert.py models/my-fine-tuned-llama --outtype f16
./quantize models/my-fine-tuned-llama/ggml-model-f16.gguf q4_k_m
```

### Using `AutoAWQ` (to make AWQ for vLLM)

```python
from awq import AutoAWQForCausalLM
model = AutoAWQForCausalLM.from_pretrained("my-model")
model.quantize(tokenizer, quant_config={"w_bit": 4})
```

---

## 4. Summary Recommendation

- **Running on Mac?** -> Download **GGUF** (Q4_K_M or Q5_K_M). Use Ollama.
- **Running a Production API?** -> Download **AWQ**. Use vLLM.
- **Fine-Tuning?** -> Use **QLoRA** (bitsandbytes NF4).
