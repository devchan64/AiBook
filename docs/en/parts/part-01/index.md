# Part 1. Introduction to AI and the Landscape

> Section ID: `P1-index`
> Version: `v2026.07.07`

Part 1 is the section where we rebuild the overall landscape before studying AI again in depth. It does not begin by implementing specific algorithms. Instead, it first clarifies how later work on mathematical recovery, machine learning, deep learning, LLMs, generative AI, service architecture, and project practice fits into one connected map.

Within the same Part, detailed explanation of a major concept should stay in one main section whenever possible. Later sections only reconnect what is needed for the current question. If a term becomes unstable again while reading, return to the [Concept Glossary](../../reference/concept-glossary.md), check the `Core Section` first, and then trace the `Appears In` list to see where the concept returns in later context.

The central purpose of this Part is to rebuild what should come to mind when someone says “AI.” AI is not just the name of one technology. It is a broad field that includes rule-based approaches, search, probabilistic judgment, data-driven learning, deep learning, generative models, agent-style tools, and social responsibility. If that range is treated as one undifferentiated mass from the beginning, the learning flow breaks quickly.

Part 1 is also the starting point where personal intuition and scattered experience are connected back to reusable standard concepts. Instead of leaving private impressions as isolated fragments, it reorganizes them into generalized knowledge that can be checked and reused across later study.

So Part 1 begins by drawing the map first.

1. It clarifies the scope of the word AI.
2. It reviews the history and shifts in paradigm.
3. It shows the movement from rules to learning.
4. It establishes the basic language of models, data, learning, and execution.
5. It connects the rise of deep learning and generative AI.
6. It places LLMs, prompts, embeddings, RAG, and agents on the same large map.
7. It keeps service architecture, ethics, copyright, security, and forecasting in view.

## Purpose of This Part

This Part is the starting point for reconnecting older introductory AI knowledge to the current AI landscape.

When many readers first studied AI, rule-based systems, search, knowledge representation, heuristics, probabilistic reasoning, data mining, and machine learning may have appeared as separate topics. Today those topics sit alongside deep learning, LLMs, prompts, embeddings, vector search, RAG, agents, tool use, service operations, copyright, and security issues.

Part 1 does not explain all of that deeply at once. Instead, it prepares the reader to answer questions such as these:

1. How are AI, machine learning, deep learning, and generative AI different?
2. What is different between rule-based and learning-based approaches?
3. What relationship do data and models have?
4. Why must learning and model execution be separated?
5. Is an LLM the same thing as AI as a whole, or only one stream inside it?
6. Is an AI service built from only one model?
7. Why must risk and responsibility be discussed together with technical explanation?

## Goals of This Part

After reading Part 1, the goal is not to know every formula or implementation detail. The goal is to keep a working understanding like this:

- You can explain how wide the term AI can be.
- You can distinguish the broad relationship among AI, machine learning, deep learning, generative AI, and LLMs.
- You can explain that rule-based approaches, search, heuristics, probabilistic judgment, and learning-based approaches play different roles.
- You can become comfortable with the basic language of data, features, representations, models, parameters, learning, and inference.
- You can distinguish prompts, embeddings, vector search, RAG, and agents inside modern LLM usage.
- You can look at an AI service through the lenses of model, app, data, tools, operational constraints, and responsibility.
- You can maintain the habit of separating personal working hypotheses from standard explanations.

## What This Part Covers and Does Not Cover

Part 1 is for establishing the overall terrain of AI. It therefore covers:

- the broad relationship among AI, machine learning, deep learning, generative AI, and LLMs
- the place of rule-based approaches, search, probabilistic judgment, and learning-based approaches
- the basic language of data, models, learning, inference, and service structure
- the large map needed to read prompts, embeddings, RAG, agents, and operational constraints

It does not try to finish the following here:

- detailed formulas and implementations of individual algorithms
- internal computational procedures of deep learning architectures
- detailed service design for LLMs, RAG, and agents

That omission is not an evasion. It is scope control. Part 1 is responsible for first making clear what belongs where. The deeper explanations are recovered in later Parts.

## The Reading Standard This Part Establishes

Because this is the first main Part of the book, it first establishes the reading standard on which later Parts depend.

- how to connect private working hypotheses to standard concepts
- the habit of reading terms in both Korean and English
- the habit of looking not only at a model but also at the service and responsibility around it

If those standards are established first, later study of mathematics, code, data, and model structure is less likely to lose its place on the overall map.

## How to Read Part 1

This Part contains many terms and a wide scope. At first, it is more important to ask what conceptual level a term belongs to, what its input and output are, and where its result has impact than to memorize individual technical names.

| Question to ask first | Why it matters | What should be fixed first in this Part |
| --- | --- | --- |
| Is the term a `technology name`, a `problem type`, or a `service component`? | In AI, terms that look similar can belong to different conceptual levels. | First separate AI, machine learning, deep learning, and LLMs as terms that do not live on exactly the same level. |
| What does the system take as `input`, and what does it produce as `output`? | Problem type becomes easier to read when input and output are visible before the algorithm name. | If classification, prediction, generation, recommendation, and search look different by input-output structure, the flow is working. |
| Where does the result have `impact`? | AI does not end at calculation. It connects to human judgment, system behavior, cost, and safety. | Build the habit of seeing not only the model but also the surrounding service and responsibility. |

Compressed into four short lines, the standard is this:

1. AI is a broad field.
2. It contains multiple problem types and multiple implementation styles.
3. Recent LLMs are one stream inside that larger map.
4. In services, model outputs affect real people and systems.

## What the Part Explains

Part 1 is organized into 17 chapters.

It begins by clarifying the scope of AI and the relationship among AI, machine learning, deep learning, and generative AI. It then follows the large flow from symbolic AI, rule-based approaches, search, knowledge representation, probabilistic reasoning, machine learning, and deep learning to generative AI.

In the middle, it deals with what it means to turn a problem into a model, with inputs and outputs, with data, features, representations, parameters, learning, and inference. That language is necessary before later Parts can be read in mathematics, code, and model documentation.

Later it reviews uncertainty, probability, stochasticity, search space, heuristics, supervised learning, unsupervised learning, and reinforcement learning. It then moves into the spread of the deep learning paradigm, generative AI, the lineage of LLMs, prompts, embeddings, vector search, RAG, AI service architecture, agents, MCP, harnesses, and operational constraints. The final chapters keep ethics, copyright, security, real-world application, and AI forecasting tied to technical explanation.

## Why This Order Matters

The hard part of studying AI again is often not the difficulty of any one concept by itself. The harder part is that the same word can mean different things in different contexts.

For example, `inference` can refer to model execution, reasoning, prediction, generation, or statistical inference depending on context. `model` can mean a mathematical abstraction, a trained machine-learning model, an API-delivered LLM, or even the broader service structure. `parameter` can also refer either to internal model weights, training settings, or generation settings in an LLM service.

Part 1 builds a common language that reduces this kind of confusion. When the terms and distinctions are fixed first, later Parts on mathematics, data modeling, machine learning, deep learning, and LLMs become less scattered.

## How It Connects to Later Parts

Part 1 is not where each technology is completed. It is the starting point that prevents later explanations from losing track of where they connect.

- Part 2 revisits the language from Part 1 in formulas, arrays, code, and runtime terms.
- Part 3 uses that basis to rebuild raw data into samples, features, baselines, and comparison structures.
- Part 4 builds on that structure to teach problem formulation, training, and evaluation in machine learning.
- Part 5 and Part 6 recover the full explanations for deep learning, LLMs, and generative AI.

## Questions This Part Intentionally Leaves Open

Because Part 1 is about the map, it intentionally defers some questions:

- How are loss and gradients actually calculated?
- Why do deep learning architectures branch into CNNs, RNNs, and Transformers?
- Why do LLM services need layers such as RAG, tool use, agents, and MCP?

Those questions are recovered in later Parts.

## What Should Remain After Finishing This Part

When Part 1 is done, AI should no longer look like a single buzzword. It should look like a broad terrain built from many layers of approaches and technical streams.

1. There were attempts to solve problems through rules.
2. There were attempts to reduce computational limits through search and heuristics.
3. There were growing attempts to learn patterns from data.
4. There were expanding attempts to learn representations through deep learning.
5. There were stronger attempts to generate outputs through generative AI and LLMs.
6. There is now a need to see those outputs together with tools, retrieval, services, and responsibility.

That understanding is what allows later detailed study to keep asking where a concept sits on the larger map.

## Completion Criteria

- You can explain the broad relationship among AI, machine learning, deep learning, generative AI, and LLMs.
- You can explain the difference between rule-based and learning-based approaches.
- You can state the basic relationship among data, features, representations, models, parameters, learning, and inference.
- You can explain why uncertainty, probability, search, and heuristics keep reappearing in AI explanation.
- You can explain the large flow connecting prompts, embeddings, vector search, RAG, and agents.
- You can view an AI service not as one model alone but as a structure that also includes apps, data, tools, operational constraints, and responsibility.
- You are ready to separate personal working hypotheses from standard explanations.

## Sources and References

This document is an original overview that organizes the purpose and study path of Part 1. It does not directly quote external sources.

