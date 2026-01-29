import random

# DSPy Educational Simulator
# ------------------------------------------------------------------
# This script simulates the DSPy library structure to teach the concepts:
# 1. Signatures (Interface)
# 2. Modules (Architecture)
# 3. Teleprompters (Optimizers/Compilers)
#
# Note: Real DSPy requires PyTorch and an LLM connection. 
# This simulator allows you to "run" the code to see the logical flow.
# ------------------------------------------------------------------

class Field:
    def __init__(self, desc):
        self.desc = desc

class Signature:
    """Base class for DSPy Signatures. Defines Input/Output schema."""
    def __init__(self):
        self.fields = {k: v for k, v in self.__class__.__dict__.items() if isinstance(v, Field)}
    
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(self.fields.keys())})"

class Module:
    """Base class for DSPy Modules (like PyTorch nn.Module)."""
    def forward(self, **kwargs):
        raise NotImplementedError

class Predict(Module):
    """The basic atomic unit. Calls the LLM."""
    def __init__(self, signature):
        self.signature = signature
        self.demos = [] # Few-shot examples

    def forward(self, **kwargs):
        # Simulation of prompt construction
        prompt = f"System: You are an expert. Follow format {self.signature}.\n"
        
        # Inject Optimized Demos (This is what the Compiler adds!)
        if self.demos:
            prompt += "--- Optimized Few-Shot Examples ---\n"
            for demo in self.demos:
                prompt += f"Input: {demo['input']} | Output: {demo['output']}\n"
            prompt += "-----------------------------------\n"
            
        # Current Task
        prompt += f"Task Input: {kwargs}\nOutput:"
        
        # Simulate LLM Response
        print(f"\n[LLM Call] Prompt:\n{prompt}")
        return "Simulated Answer"

class BootstrapFewShot:
    """The Optimizer (Compiler). It 'trains' the prompt."""
    def __init__(self, metric):
        self.metric = metric

    def compile(self, student, trainset):
        print(f"\n[Compiler] Starting Optimization using Metric: {self.metric.__name__}...")
        print(f"[Compiler] Training on {len(trainset)} examples...")
        
        # Simulation: The compiler runs the student model, generates traces,
        # checks against the metric, and saves the successful traces as "demos".
        
        best_demos = []
        for example in trainset:
            # Fake a validation pass
            score = random.random()
            if score > 0.7:
                print(f"  -> Example '{example['input']}' passed metric! Adding to prompting set.")
                best_demos.append(example)
        
        # Inject the best demos into the student
        student.demos = best_demos
        print(f"[Compiler] Optimization Complete. Selected {len(best_demos)} robust examples.")
        return student

# --- User Code Starts Here ---

# 1. Define Signature
class RAGSignature(Signature):
    """Answer questions based on context."""
    context = Field(desc="Reference documents")
    question = Field(desc="User query")
    answer = Field(desc="Fact-based answer")

# 2. Define Architecture
class RAGPipeline(Module):
    def __init__(self):
        self.generate_answer = Predict(RAGSignature)

    def forward(self, context, question):
        return self.generate_answer.forward(context=context, question=question)

# 3. Define Metric
def correct_answer_metric(example, pred):
    return example['output'] == pred

def main():
    print("=== DSPy Workflow Simulation ===\n")

    # A. Data Setup
    trainset = [
        {"input": "What is the capital of France?", "output": "Paris"},
        {"input": "Who wrote Hamlet?", "output": "Shakespeare"},
        {"input": "What is 2+2?", "output": "4"},
    ]
    
    # B. Define Pipeline
    print("1. Defining Pipeline...")
    my_rag = RAGPipeline()
    
    # C. Compile (Optimize)
    print("2. Compiling (Optimizing Prompts)...")
    optimizer = BootstrapFewShot(metric=correct_answer_metric)
    compiled_rag = optimizer.compile(student=my_rag.generate_answer, trainset=trainset)
    
    # D. Inference
    print("\n3. Running Inference (Compiled vs Uncompiled)...")
    
    print("\n--- Running Optimized Program ---")
    compiled_rag.forward(context="History book", question="Who won WWII?")
    
    print("\n=== Takeaway ===")
    print("Notice that the [LLM Call] included 'Optimized Few-Shot Examples'.")
    print("You did not write those. The Compiler selected them from your data.")

if __name__ == "__main__":
    main()
