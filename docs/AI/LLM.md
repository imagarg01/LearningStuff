# LLM

- RNN (Recurrent Neural Networks) and CNN (Convolutional Neural Networks) were the dominant architectures for many years, especially in natural language processing (NLP) and computer vision tasks.

- LSTMs (Long Short-Term Memory networks) and GRUs (Gated Recurrent Units) were developed to address some of the limitations of traditional RNNs, particularly in capturing long-range dependencies in sequential data.

## Transformers

Transformers, introduced in the paper "Attention is All You Need" by Vaswani et al. in 2017, revolutionized the field of NLP and beyond. The key innovation of transformers is the self-attention mechanism, which allows the model to weigh the importance of different words in a sentence relative to each other, regardless of their position. This enables transformers to capture long-range dependencies more effectively than RNNs or LSTMs.

## Core Characteristics of an AI Agent

AI Agents are widerly conceptualized as instantiated operational instances of artificial intelligence system.These agents are different from traditional LLM
in the sense that they exhibit structured intialization, bounded autonomy, and presistent task orientation. While LLMs priamary function as reactive prompt
followers, AI agents operate automatically within explicitly defined scopes, engaging dynamically with inputs and producting actionable outputs in real-time.

1. **Autonomy**: Ability to function with minimal or no human intervention after deployment. Once initialized, these agents are capable of perceiving environmental
   inputs, reasoning over contextual data, and executing predefined or adaptive action in realtime.
2. **Task-Specificity**: Purpose-built for narrow and well-defined tasks. They are optimized to execute repetable operations within a fixed domain.
3. **Reactivity and Adaptation**: Often include basic mechanisms for interacting with dynamic inputs, allowing them to respond to real-time stimuli such as user queries or environmental changes.

WithIn AI Agent architectures, LLMs serve as primary decision making engine, allowing the agent to parse user queries, plan muilti-step solutions, and generate human-like responses.

## Key Characteristics of Generative AI

- **Reactivity**: As non-autonomous systems, generative models are exclusively input-driven. Their operation are triggered by user-specified prompts and they lack internal states,
  persistent memory, or goal-following mechanisms.
- **Multi-modal Capability**: Modern generative systems can produce a diverse array of outputs, including coherent narratives, executable code, realistic images and even speech transcripts.
- **Prompt Dependency and Statelessness**: They do not retail context across interactions unless explicitly prompoted, lacks intrinsic feedback loops, state management,
  or multi-step planning a requirement for autonomous decision making and interative goal refinement.

AI agents overcome these limitations by integrating LLMs with additional components such as memory systems, task planners, and execution modules. LLMs works as core reasoning engine,
within the dynamic agentic system.

## Agentic AI

- Refers to AI systems that

  - Act autonomously and independently
  - Pursue goals and tasks
  - Make decisions with minimal human intervention
  - Reason, plan and adapt to achieve complex, open-ended objectives
  - It's goal oriented, not just rule-based or data-driven

Agentic AI indpendently research, schedule tasks, or optimize a workflow to meet a user's goal. Workflows are not agentic AI.
There are different kind of workflows:

1. Prompt chaining: A sequence of prompts that build on each other to achieve a complex task. It should be used when the task can be easiliy decomposed into fixed subtasks.
   It is not agentic AI, but it can be used as a building block for agentic AI. A trade off of latency for higher accuracy, for making each LLM call an easier task.
2. Routing:
3. Parllelization:
4. Orchestrator-workers:
5. Evaluator-optimizer:

## Types of AI Agents

There are different types of AI agents, each with its own characteristics and capabilities. Some common types include:

1. Simple Reflex Agents: These agents respond to specific stimuli with pre-defined actions. They are not capable of learning or adapting to new situations.
2. Model based Reflex Agents: These agents maintain an internal model of the world and use it to make decisions. They can adapt to changes in the environment but are still limited in their capabilities.
3. Goal-based Agents: These agents have specific goals and can plan and execute actions to achieve them. They can adapt their behavior based on the current state of the environment.
4. Utility-based Agents: These agents evaluate the utility of different actions and choose the one that maximizes their expected utility. They can adapt their behavior based on the current state of the environment and their goals.
5. Learning Agents: These agents can learn from their experiences and improve their performance over time. They can adapt their behavior based on the current state of the environment and their goals.

## LLM (Large Language Model)

A LLM is an AI model trained on massive amounts of text data to understand and generate human-like language, recognize pattern in language, and perform a wide variety of tasks.
LLM are characterized by:

1. **Scale**: They contain millions or billions of parameters, allowing them to capture complex language patterns and relationships.
2. **General Capability**: They can perform a wide range of tasks without task-specific training, including text generation, language translation, question answering, summarization, and more.
3. **In-context Learning**: They can learn from examples provided in the prompt.
4. **Emergent ablities**: As these model grows in size, they demonstrate capabilities that weren't explicitly programmed or anticipated.

LLMs also have important limitations:

- **Hallucinations**: They can generate incorrect information confidently, leading to misinformation.
- **Lack on true understanding**: They lack true understanding of the world and operate purely on statistical patterns.
- Bias: They can reflect and amplify biases present in the training data.
- **Context windows**: They have limited context windows, meaning they can only consider a certain amount of text at a time, which can lead to loss of information in longer conversations.(though this is improving with newer models)
- **Resource Intensive**: They require significant computational resources for training and inference, making them less accessible for smaller applications or devices.
