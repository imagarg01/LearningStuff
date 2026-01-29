# Fine-Tuning LLMs: From Basics to Advanced

Fine-tuning is the process of adapting a pre-trained Large Language Model (LLM) to a specific domain or task. Unlike RAG, which adds context to the prompt, fine-tuning modifies the model's internal weights.

---

## 1. The Fine-Tuning Spectrum

### Level 1: Full Fine-Tuning (The Old Way)

- **Concept**: Retrain *all* parameters of the model.
- **Cost**: Extremely expensive. Requires enough GPU memory to hold the model states, gradients, and optimizer states (approx 4-8x model size).
- **When to use**: Almost never for modern LLMs (7B+), unless you are OpenAI/Meta level.

### Level 2: Parameter-Efficient Fine-Tuning (PEFT)

- **Concept**: Freeze the massive base model. Train only a tiny set of new parameters (adapters) added on top.
- **Techniques**:
  - **LoRA (Low-Rank Adaptation)**: The industry standard.
  - **QLoRA (Quantized LoRA)**: Doing LoRA on a 4-bit quantized base model. Allows fine-tuning a 70B model on a single consumer GPU (24GB VRAM).
- **Benefit**: Retains base model knowledge while adapting behavior.

### Level 3: Alignment (RLHF & DPO)

- **Concept**: Teaching the model *preferences* (e.g., "Be helpful and safe") rather than just next-token prediction.
- **Techniques**:
  - **RLHF (Reinforcement Learning from Human Feedback)**: Train a Reward Model, then use PPO to optimize the LLM. Complex/Unstable.
  - **DPO (Direct Preference Optimization)**: A stable, mathematical equivalent to RLHF that skips the Reward Model step. You just need pairs of `(chosen, rejected)` answers.

---

## 2. Key Research & Papers

If you want to master fine-tuning, you must read these foundational papers:

| Technique | Paper & Link | Key Insight |
| :--- | :--- | :--- |
| **LoRA** | [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) | Decomposes weight updates into low-rank matrices. $W = W_0 + BA$. |
| **QLoRA** | [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) | Introduced 4-bit NormalFloat (NF4) and Double Quantization. Enabled 65B training on 48GB VRAM. |
| **NEFTune** | [NEFTune: Noisy Embeddings Improve Instruction Finetuning](https://arxiv.org/abs/2310.05914) | Adding noise to embedding vectors during training prevents overfitting and boosts conversational quality. |
| **DPO** | [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) | Solves the RLHF alignment objective analytically without reinforcement learning loops. |

---

## 3. How to Measure Success (Evaluation)

How do you know if your fine-tuned model is better?

### A. Training Metrics (During Training)

- **Training Loss**: Should go down.
- **Validation Loss**: Should go down. If it starts going up while Training Loss goes down, you are **overfitting**.
- **Perplexity**: A measure of how "surprised" the model is by the text. Lower is better.

### B. Generic Benchmarks (The "Vibes" check)

- **MMLU / ARC / HellaSwag**: Use tools like `lm-evaluation-harness` to ensure you haven't caused "Catastrophic Forgetting" (making the model stupid at general reasoning while teaching it your niche).

### C. Domain-Specific Evaluation (The Real Test)

- **Golden Set**: reserve 100 high-quality `(Prompt, Ideal Answer)` pairs.
- **LLM-as-a-Judge**: Use GPT-4 to blindly grade your Fine-Tuned Model vs Base Model on the Golden Set.
  - "Win Rate": % of times Fine-Tuned Model beats Base Model.

---

## 4. The Fine-Tuning Workflow

1. **Data Prep**:
    - **Instruction Tuning**: Format data as `{"instruction": "...", "input": "...", "output": "..."}`.
    - **Quantity**: 1,000 high-quality examples > 100,000 messy ones (See *LIMA* paper).
2. **Base Model Selection**:
    - Llama 3 8B, Mistral 7B, Qwen 2.
3. **Config**:
    - Rank ($r$): 8, 16, 64 (Higher = more parameters to learn).
    - Alpha: Usually $2 \times r$.
4. **Training**: Run via `SFTTrainer` (HuggingFace TRL).
5. **Merge**: Merge adapters back into base model for deployment (or load dynamically at runtime).
