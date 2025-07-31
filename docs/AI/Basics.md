## Language Models

A language model is a statistical model that is trained on a large corpus of text data in one or more languages. It learns the patterns and structures of the language, allowing it to generate text that is coherent and contextually relevant.

Basic unit of langyage model is a token. A token can be character, a word or a part of word, depending on the model. For example, in the case of GPT-4 it breaks the phrase "I can't wait to build AI applications" into nine tokens.

The process of breaking the original text into tokens is called tokenization. For GPT-4, an average token is approximately 3/4 lenght of a word, so 1000 tokens is approximately 750 words.

The set of all tokens that a language model can understand is called its vocabulary. The vocabulary size can vary depending on the model, but it typically ranges from tens of thousands to hundreds of thousands of tokens. For GPT-4, the vocabulary size is around 100,256 tokens.

There are two main types of language models: **masked language models** (MLMs) and **autoregressive language models** (ARLMs).

- Masked language models (MLMs) are trained to predict missing tokens anywhere in a sequence, using the context from both before and after the missing token. This allows them to learn bidirectional context, making them effective for tasks like text classification and named entity recognition. Examples of MLMs include BERT and RoBERTa. Commonly used for non-generative tasks such as text classification, sentiment analysis, and named entity recognition.

- Autoregressive language models (ARLMs) are trained to predict the next token in a sequence, using only the context from the tokens that come before it. This makes them suitable for tasks like text generation and completion. Examples of ARLMs include GPT-3 and GPT-4. Commonly used for generative tasks such as text generation, summarization, and translation.

![Language Models](images/LanguageModels.png)
