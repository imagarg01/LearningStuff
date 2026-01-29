# LoRA Adapter Guide (Deep Dive)

**LoRA (Low-Rank Adaptation)** is the engine behind modern fine-tuning. It allows us to adapt massive models (like Llama 3 70B) on consumer hardware.

---

## 1. The Math Intuition

Standard fine-tuning updates the entire weight matrix $W$ of the model.

$$W_{updated} = W + \Delta W$$

If $W$ is $4096 \times 4096$, then $\Delta W$ is also $4096 \times 4096$ (16 million parameters just for one layer!).

**LoRA Insight**: The changes needed for a specific task ($\Delta W$) have a "low intrinsic rank". We don't need to change all 16 million numbers independently.

LoRA decomposes $\Delta W$ into two tiny matrices, $A$ and $B$:

$$\Delta W = B \times A$$

- $A$ is dimensions $r \times 4096$.
- $B$ is dimensions $4096 \times r$.
- $r$ (rank) is tiny (e.g., 8 or 16).

If $r=8$:

- Matrix $A$ = $8 \times 4096 = 32,768$ params.
- Matrix $B$ = $4096 \times 8 = 32,768$ params.
- Total = ~65,000 params (vs 16 million!). **99.6% reduction**.

---

## 2. Key Hyperparameters within PEFT

When using HuggingFace `peft`, you will configure `LoraConfig`.

### A. Rank (`r`)

- **What**: The dimension of the LoRA matrices.
- **Recommendation**: start with **8**.
  - **8**: Good for simple instruction following.
  - **64**: Needed for complex reasoning or hard domain shifts (e.g., teaching a model a completely new language).
  - **Warning**: increasing $r$ increases VRAM usage slightly and training file size linearly.

### B. Alpha (`lora_alpha`)

- **What**: Scaling factor. The update is scaled by $\frac{\alpha}{r}$.
- **Recommendation**: Set $\alpha = 2 \times r$ (e.g., if $r=8$, $\alpha=16$). This has become a standard heuristic.

### C. Dropout (`lora_dropout`)

- **What**: Randomly zeros out neuron connections to prevent overfitting.
- **Recommendation**: **0.05** or **0.1**.

### D. Target Modules (`target_modules`)

- **What**: Which layers of the Transformer to apply LoRA to.
- **Recommendation**: Apply to **all linear layers** (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`).
  - Early LoRA papers only targeted `q_proj` and `v_proj`.
  - QLoRA paper showed targeting *all* layers improves performance significantly with minimal cost.

---

## 3. Storage Efficiency

Because we only train A and B, we save only A and B.

- **Base Model**: 15GB (Llama-2-7b-fp16).
- **LoRA Adapter**: ~100MB.

This means you can have **one base model** and **50 different adapters** (one for coding, one for poetry, one for SQL) loaded and hot-swapped at runtime. This is called **Multi-LoRA serving** (supported by vLLM and LoRAX).
