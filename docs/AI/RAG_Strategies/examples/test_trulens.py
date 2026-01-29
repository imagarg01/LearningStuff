# test_trulens.py
import os

# NOTE: TruLens requires a DB setup and keys. This is a skeleton to demonstrate intent.
# pip install trulens-eval

try:
    from trulens_eval import Tru, Feedback, TruLlama
    from trulens_eval.feedback import Groundedness
    from trulens_eval.feedback.provider.openai import OpenAI
except ImportError:
    print("TruLens not installed or dependencies missing.")
    print("Run: pip install trulens-eval")
    exit(0)

def main():
    print("Initializing TruLens...")
    tru = Tru()
    # Reset dashboard database for demo
    tru.reset_database()

    # 1. Define Feedback Functions
    # Uses OpenAI as the judge
    openai = OpenAI()
    
    # Faithfulness / Groundedness
    grounded = Groundedness(groundedness_provider=openai)
    f_groundedness = (
        Feedback(grounded.groundedness_measure_with_cot_reasons)
        .on_input()
        .on_output()
        .aggregate(grounded.grounded_statements_aggregator)
    )

    # Answer Relevance
    f_answer_relevance = (
        Feedback(openai.relevance)
        .on_input()
        .on_output()
    )

    # 2. Wrap your App
    # Assuming 'rag_app' is your LlamaIndex or LangChain app
    # recorder = TruLlama(rag_app, feedbacks=[f_groundedness, f_answer_relevance])

    print("Success! In a real app, you would now use 'with recorder:' context manager.")
    print("Then run: tru.run_dashboard()")

if __name__ == "__main__":
    main()
