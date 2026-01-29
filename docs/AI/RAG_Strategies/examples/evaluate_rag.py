# evaluate_rag.py
import os
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevance,
    context_precision,
    context_recall,
)
from datasets import Dataset

# NOTE: You need an OpenAI API Key for Ragas to work as a judge.
# os.environ["OPENAI_API_KEY"] = "sk-..."

def run_evaluation():
    print("Preparing Evaluation Dataset...")
    
    # 1. Prepare Data
    # In a real scenario, these would come from your RAG pipeline logs.
    data_samples = {
        'question': [
            'What is the capital of France?', 
            'Who is the CEO of Tesla?'
        ],
        'answer': [
            'Paris is the capital of France.', 
            'Elon Musk is the CEO of Tesla.'
        ],
        'contexts': [
            ['Paris is the capital and most populous city of France. It is situated on the Seine River.'], 
            ['Elon Musk is the CEO of Tesla, SpaceX, and several other companies.']
        ],
        'ground_truth': [
            'Paris', 
            'Elon Musk'
        ]
    }
    
    dataset = Dataset.from_dict(data_samples)

    print("Running Ragas Evaluation (this requires OpenAI API Key)...")
    try:
        # 2. Run Evaluation
        results = evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevance,
                context_precision,
                context_recall,
            ],
        )

        print("\n--- Evaluation Results ---")
        print(results)
        
        # 3. Export to Pandas for analysis
        df = results.to_pandas()
        print("\n--- Detailed Scores ---")
        print(df[['question', 'faithfulness', 'answer_relevance']])
        
    except Exception as e:
        print(f"\nError running evaluation: {e}")
        print("Tip: Make sure OPENAI_API_KEY is set in your environment variables.")

if __name__ == "__main__":
    run_evaluation()
