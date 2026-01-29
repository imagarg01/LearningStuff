import torch
import torch.nn as nn

# Simulation of LoRA logic to demonstrate the parameter savings without needing a GPU/HuggingFace download
# This script runs on any local Python environment (CPU).

class SimpleLinear(nn.Module):
    """A standard heavy Linear layer representing a slice of an LLM."""
    def __init__(self, in_features, out_features):
        super().__init__()
        # In a real 7B model, these dimensions are ~4096
        self.weight = nn.Parameter(torch.randn(out_features, in_features))
        
    def forward(self, x):
        return x @ self.weight.T

class LoraLayer(nn.Module):
    """A LoRA adapter wrapping the standard linear layer."""
    def __init__(self, original_layer, rank=8, alpha=16):
        super().__init__()
        self.original_layer = original_layer
        self.rank = rank
        self.scaling = alpha / rank
        
        in_features = original_layer.weight.shape[1]
        out_features = original_layer.weight.shape[0]
        
        # Matrix A: r x in
        self.lora_A = nn.Parameter(torch.zeros(rank, in_features))
        # Matrix B: out x r
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
        
        # Initialize A with Neural Gaussian, B with Zeros (Identity start)
        nn.init.kaiming_uniform_(self.lora_A, a=5**0.5)
        nn.init.zeros_(self.lora_B)
        
        # Freeze original weights!
        self.original_layer.weight.requires_grad = False

    def forward(self, x):
        # Result = Wx + (BA)x * scaling
        original_out = self.original_layer(x)
        lora_out = (x @ self.lora_A.T @ self.lora_B.T) * self.scaling
        return original_out + lora_out

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def main():
    print("--- LoRA Parameter Efficiency Demo ---\n")
    
    # simulate a layer in Llama-2-7b (dim=4096)
    d_model = 4096
    
    # 1. Standard Layer
    base_layer = SimpleLinear(d_model, d_model)
    total_params = base_layer.weight.numel()
    print(f"Base Layer (4096 x 4096)")
    print(f"Total Parameters: {total_params:,}")
    print(f"Trainable Parameters (Full FT): {total_params:,}\n")
    
    # 2. Apply LoRA
    rank = 8
    print(f"Applying LoRA (Rank r={rank})...")
    lora_layer = LoraLayer(base_layer, rank=rank)
    
    trainable_params = count_parameters(lora_layer)
    
    print(f"Total Parameters (Base + LoRA): {total_params + trainable_params:,}")
    print(f"Trainable Parameters (LoRA only): {trainable_params:,}")
    
    reduction = 100 * (1 - (trainable_params / total_params))
    print(f"\nParameter Reduction: {reduction:.4f}%")
    print("\nThis explains why LoRA allows fine-tuning on consumer GPUs!")

if __name__ == "__main__":
    main()
