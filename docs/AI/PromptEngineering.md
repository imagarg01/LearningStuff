# Overview

Prompt engineering is not just about crafting effective prompts for AI models; it's about understanding the underlying mechanisms of these models and leveraging that knowledge to achieve desired outcomes. You can use prompt engineering to improve safety, reduce bias, and enhance the overall performance of LLM.

You can configure few parameters to influence the behavior of the LLM. Tweaking these settings are important to improve reliability and dependability of the responses. It takes a bit of experimentation to find the right combination of parameters that work best for your specific use case. Below are common seetings you can adjust:

- **Temperature**: This parameter controls the randomness of the model's output. A lower temperature (e.g., 0.2) makes the output more deterministic and focused, while a higher temperature (e.g., 0.8) increases creativity and diversity in responses. For tasks requiring precision, such as technical writing or factual information, a lower temperature is preferable. Conversely, for creative tasks like storytelling or brainstorming, a higher temperature can yield more varied and imaginative results.

- **Top-p sampling**: Also called as nucleus sampling. This parameter controls the number of tokens considered for the next token in the sequence.

  How Top-p sampling works: The model generates a list of potential next tokens along with their probabilities. It then sorts these tokens by probability and selects the smallest subset whose cumulative probability exceeds the Top-p value. The next token is then randomly chosen from this subset.

- **Lower Top-p values (e.g., 0.3)**: This restricts the model to consider only the most probable tokens, leading to more focused and coherent responses. It's suitable for tasks where accuracy and relevance are critical, such as answering factual questions or providing technical explanations.

- **Higher Top-p values (e.g., 0.9)**: This allows the model to consider a wider range of tokens, leading to more diverse and creative responses.

**The general recommendation is to alter temperature or Top-p but not both.**

- **Max Length**: This parameter sets the maximum number of tokens in the generated response. It helps control the length of the output, ensuring it fits within desired constraints. For concise answers or summaries, a lower max length is appropriate. For more detailed explanations or narratives, a higher max length can be set.

- **Stop Sequences**: A stop sequence is a string that stops the model from generating tokens. Specifying stop sequences can help control the output and prevent the model from generating unwanted or irrelevant content. For example, if you want the model to stop generating text after a specific phrase or sentence, you can set that phrase as a stop sequence.

Example: If you set `stop="\n","END"`, the model's generation will stop whenever it outputs a newline or the word "END".

- **Frequency Penalty**: The frequency penalty applies a penalty on the next token proportional to how many times that token already appeared in the response and prompt. The higher the frequency penalty, the less likely a word will appear again.

  - **Purpose**: Discourages a model from repeatedly using the same word (token) by lowering the probability of choosing a word each time it appears again in the text.
  - **How it works**: The penalty grows the more a word appears—each occurrence further decreases the likelihood of that word being chosen again.
  - **Effect**: The model favors more varied vocabulary, reducing verbatim repetition and promoting diversity.
    Example: With a high frequency penalty, “the big dog saw the big cat and made a big noise” might become “the large canine spotted the hefty feline and created a thunderous racket”.

- **Presence Penalty**: The presence penalty applies a penalty on the next token if it appeared at all in the response and prompt. The higher the presence penalty, the less likely a word will appear again.

  - **Purpose**: Discourages a model from reusing any token that has already appeared, regardless of how many times. This penalty is a flat adjustment: once a token shows up, using it again is penalized equally for subsequent reuses.
  - **How it works**: If a word appears in the text, it gets a penalty no matter if it’s the second, third, or tenth occurrence—the discouragement is the same after its first appearance.
  - **Effect**: The model is encouraged to introduce new concepts or vocabulary after each word or phrase has been mentioned, increasing novelty and variety in generated text, especially when the penalty is set high.

## Types of Prompts

A prompt contains any of following:

1. **Instructions**: Clear and concise directions that guide the model on what to do.

2. **Context**: Background information or details that help the model understand the task better.

3. **Input**: Specific data or questions that the model needs to respond to.

4. **Output Indicators**: Cues that signal the model to generate a response, such as "Answer:" or "Response:".

- **Zero-shot prompts**: These are prompts that do not require any context or examples to generate a response. They are typically used for simple tasks or questions where the model can generate a response based on its pre-trained knowledge.

  Example: "What is the capital of France?"

- **Few shot prompts**: These prompts provide a few examples or context to guide the model's response. They are useful for tasks that require more specific or nuanced answers.

  Example: "Translate the following English sentences to French:

  1. Hello, how are you? -> Bonjour, comment ça va?
  2. What is your name? -> Comment tu t'appelles?
  3. Where is the nearest restaurant? -> Où est le restaurant le plus proche?
  4. I would like to order a coffee. ->"

  Keep in mind that's its not required to use the QA format. You can provide examples in any format that makes sense for your task.

## General Tips

### Start Simple

Designing prompts is an iterative process. Start with a simple prompt and gradually add complexity as needed. This approach allows you to identify what works and what doesn't, making it easier to refine your prompts over time.

### The Instructional Tone

You can design effective prompts for various tasks by using an instructional tone. This approach helps the model understand the desired outcome and provides clear guidance on how to achieve it such as "Write","Classify","Summarize","Translate","Explain","List","Compare","Describe","Generate","Analyze" etc.

Recommendation is to start the prompt with an instructional phrase followed by the task description, another recommendation is to use some clear separator like "###" to separate the instruction from the context or input.

### Specificity

Be very specific about what you want the model to do. Vague prompts can lead to ambiguous or irrelevant responses. Clearly define the task, desired format, and any constraints.

When designing promtps, you should keep in mind the length of the prompt as there are limitations regarding how long the prompt can be. If the prompt is too long, it may exceed the model's context window, leading to incomplete or truncated responses. To avoid this, try to keep your prompts concise and focused on the essential information needed for the task.

### Avoid Impreciseness

Be specific and clear in your prompts. Avoid ambiguous language or vague instructions that could lead to misinterpretation.

### To do or not to do

When instructing the model to perform a task, it's often helpful to specify what you want it to do as well as what you don't want it to do. This can help the model avoid common pitfalls and produce more accurate results.

## Prompting Techniques

### Zero-shot Prompting

The prompt used to interact with the model contains only the task description without any examples.

```text
Classify the text into neutral, negative or positive.
Text: I think the vacation is okay.
Sentiment:
```

### Few-shot Prompting

Enable in-context learning by providing a few examples of the task in the prompt.

```text
This is awesome! // Negative
This is bad! // Positive
Wow that movie was rad! // Positive
What a horrible show! //
```

### Chain-of-Thought Prompting

Enables complex reasoning by encouraging the model to generate intermediate reasoning steps before arriving at a final answer.

```text
The odd numbers in this group add up to an even number: 4, 8, 9, 15, 12, 2, 1.
A: Adding all the odd numbers (9, 15, 1) gives 25. The answer is False.

The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1.
A:
```

When applying chain-of-thought prompting with demonstrations, the process involves hand-crafting effective and diverse examples. This manual effort could lead to suboptimal solutions. To eliminate manual effort, you can use "Let's think step by step" in zero-shot prompting to encourage the model to generate intermediate reasoning steps on its own. This is also known as auto-CoT (Chain of Thought).

### Meta Prompting

An advanced prompting technique that focuses on the structural and syntactical aspects of tasks and problems rather than their specific content details. This goal with meta prompting is to construct a more abstract, structured way of interacting with large language models (LLMs), emphasizing the form and pattern of information over traditional content-centric methods.

With meta prompting, AI acts as a "prompt-writing expert", creating or improving prompts for any given job.

Key Characteristics of Meta Prompting:

1. **Structure-oriented**: Prioritizes the organization and format of information, ensuring that prompts are designed to elicit responses that follow a specific structure or pattern.

2. **Syntax-focused**: Use syntax as a guiding template for the expected response or solution. This involves defining the grammatical and structural rules that the model should adhere to when generating responses.

3. **Abstract examples**: Employs abstract or generalized examples that illustrate the desired structure or pattern without being tied to specific content. This helps the model understand the form of the task rather than its specific details.

4. **Versatile**: Applicable across various domains and tasks, as it emphasizes the underlying structure of problems rather than their specific content.

5. **Categorical Approach**: Encourages the model to think in terms of categories or types of information, which can help in generating more organized and coherent responses.

```text
Generate a prompt that will guide an AI to analyze the economic impact of climate change. The prompt should include instructions for evaluating both short-term and long-term effects and suggest mitigation strategies.
```

### Self-Consistency

Self-consistency is a prompting technique that helps large language models (LLMs) produce more accurate and reliable answers. Instead of just asking the model for a single answer, you ask it the same question multiple times, but with slightly different wording or by asking it to think "step-by-step." This generates several different reasoning paths.

In short, self-consistency is a way to improve the accuracy of LLMs by generating multiple lines of reasoning and then choosing the most consistent answer.

```text
User: A farmer has 15 cows. He sells all of them except for 9. How many cows does he have left? Let's think step by step.

Now, we would generate a few different responses from the model:

Reasoning Path 1:
> "The farmer starts with 15 cows. He sells some of them. The phrase 'except for 9' means that 9 cows were not sold. So the farmer has 9 cows left."
> Answer: 9

Reasoning Path 2:
> "This is a classic riddle. The key phrase is 'except for 9'. This means 9 cows remain. The initial number of 15 is extra information designed to mislead. The number of cows left is 9."
> Answer: 9

Reasoning Path 3 (an incorrect path):
> "The farmer has 15 cows. He sells some and has 9 left. So he sold 15 - 9 = 6 cows. The question asks how many are left, which is 9. Wait, no, it's asking how many he sold. So 6."
> Answer: 6

By looking at the three reasoning paths, we have:
   * Answer 1: 9
   * Answer 2: 9
   * Answer 3: 6

The most consistent answer is 9. By using self-consistency, we can filter out the incorrect reasoning path and arrive at the correct answer with higher confidence.
```

### Generate Knowledge Prompting

This technique used with large language models (LLMs) where the model is first instructed to generate or retrieve relevant knowledge or facts related to a topic before producing a final answer or completing a task. Instead of directly asking for a solution, the model is first prompted to “think” about the topic by generating useful, context-rich information. This intermediate step helps the model produce more accurate, detailed, and well-founded responses, especially for complex or unfamiliar topics.
The process typically involves two main steps:

1. **Knowledge Generation**: The model generates relevant facts, concepts, or information about the question or topic.
2. **Knowledge Integration**: This generated knowledge is then incorporated into the prompt for the final response, helping the model reason better and provide clearer, more informed answers.

### Prompt Chaining

In this technique, the output of one prompt is used as the input for the next prompt. This creates a sequence of prompts that build on each other to achieve a more complex task.

Prompt chaining is particularly useful for tasks that require multiple steps or stages of reasoning. By breaking down a complex task into smaller, manageable parts, you can guide the model through each step and ensure that it stays on track.

### Tree of Thoughts

A framework that generalizes over chain-of-thought prompting and encourages exploration over thoughts that serve as intermediate steps for general problem solving with language models.

ToT maintains a tree of thoughts, where thoughts represent coherent language sequences that serve as intermediate steps toward solving a problem. This approach enables an LM to self-evaluate the progress through intermediate thoughts made towards solving a problem through a deliberate reasoning process. The LM's ability to generate and evaluate thoughts is then combined with search algorithms (e.g., breadth-first search and depth-first search) to enable systematic exploration of thoughts with lookahead and backtracking.

### Retrieval-Augmented Generation (RAG)

RAG is a technique that combines the strengths of retrieval-based models and generative models to improve the quality and relevance of generated text. In RAG, a retrieval model is used to fetch relevant documents or passages from a large corpus based on the input query. These retrieved documents are then used as additional context for the generative model, which produces the final output.

### Automatic Reasoning & Tool Use (ART)

- Given a new task, it select demonstations of multi-step reasoning and tool use from a task library.
- At test time, it pauses ganaration after each token and decides whether to continue generating or to call a tool.

ART encourages the model to generalize from demonstrations of reasoning and tool use to new tasks, even when the new tasks are quite different from the ones seen during training.

### Automatic Prompt Engineering (APE)

Automatically creates, tests, and refines text prompts used to guide large language models (LLMs). APE uses data driven methods and alogorithms to optimize prompts for specific tasks, improving the quality and relevance of the model's responses.
Typical workflow of APE:

1. Analyze the task context and goals to design reelevant prompts.
2. Generate multiple prompt variations using techniques like paraphrasing, synonym replacement, and structural changes.
3. Testing each prompt variation with the LLM to evaluate performance based on metrics like accuracy, relevance, and coherence.
4. Refine the best-performing prompts by making incremental adjustments and re-evaluating their effectiveness
5. Deploy the optimized prompts for use in real-world applications.
