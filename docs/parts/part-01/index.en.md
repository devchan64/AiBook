# Part 1. Introduction to AI and the Landscape

> Section ID: `P1-index`
> Version: `v2026.07.26`

Part 1 is the section where we rebuild the overall landscape before studying AI again in depth. It does not begin by implementing one specific algorithm in detail. Instead, it first clarifies how later work on mathematical recovery, machine learning, deep learning, LLMs, generative AI, service architecture, and project practice fits into one connected map.

Within the same Part, detailed explanation of a major concept should stay in one main section whenever possible. Later sections only reconnect what is needed for the current question. If a term becomes unstable again while reading, return to representative glossary entries such as [AI](/AiBook/en/reference/concept-glossary-alpha/a/#ai-artificial-intelligence), [machine learning](/AiBook/en/reference/concept-glossary-alpha/m/#machine-learning), and [LLM](/AiBook/en/reference/concept-glossary-alpha/l/#llm), check the `Core Section` first, and then trace the `Appears In` list to see where the concept returns in later context.

The central purpose of this Part is to rebuild what should come to mind when someone says “AI.” AI is not just the name of one technology. It is a broad field that includes rule-based approaches, search, probabilistic judgment, data-driven learning, deep learning, generative models, AI-agent-style tools, and social responsibility. If that range is treated as one undifferentiated mass from the beginning, the learning flow breaks quickly.

Part 1 is also the starting point where personal intuition and scattered experience are connected back to reusable standard concepts. Instead of leaving private impressions as isolated fragments, it reorganizes them into generalized knowledge that can be checked and reused across later study.

So Part 1 begins by drawing the map first.

1. It clarifies the scope of the word AI.
2. It reviews history and shifts in paradigm.
3. It shows the movement from rules to learning.
4. It establishes the basic language of models, data, learning, and execution.
5. It connects the rise of deep learning and generative AI.
6. It places LLMs, prompts, embeddings, RAG, and agents on the same large map.
7. It keeps service architecture, ethics, copyright, security, and forecasting in view.

## Why Start by Building the Whole AI Map

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

## How to Distinguish AI, Machine Learning, and LLMs

After reading Part 1, the goal is not to know every formula or implementation detail. The goal is to keep a working understanding like this:

- You can explain how wide the term AI can be.
- You can distinguish the broad relationship among AI, machine learning, deep learning, generative AI, and LLMs.
- You can explain that rule-based approaches, search, heuristics, probabilistic judgment, and learning-based approaches play different roles.
- You can become comfortable with the basic language of data, features, representations, models, parameters, learning, and inference.
- You can distinguish prompts, embeddings, vector search, RAG, and agents inside modern LLM usage.
- You can look at an AI service through the lenses of model, app, data, tools, operational constraints, and responsibility.
- You can maintain the habit of separating personal working hypotheses from standard explanations.

## Boundary Between AI Landscape and Later Study

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

## Working Hypotheses, Terms, and Service Responsibility

Because this is the first main Part of the book, it first establishes the common reading standard on which later Parts depend.

- how to connect private working hypotheses to standard concepts
- the habit of reading terms in both Korean and English
- the habit of looking not only at a model but also at the service and responsibility around it

If those standards are established first, later study of mathematics, code, data, and model structure is less likely to lose its place on the overall map.

## Reading AI Terms by Level

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

This Part does not repeat every concept at the same density in every chapter. For example, core terms such as `model`, `input`, `output`, `feature`, `representation`, and `parameter` are first fixed in earlier sections, and later sections only reconnect what is needed for the current problem scene. So when the same term appears again, the reader should ask whether a new definition is being added or whether the term is only being placed into a different context.

The role of Part 1 becomes clearest when the following five standards remain in place:

| Standard to keep first | Where it returns later |
| --- | --- |
| AI is a broad field, and LLMs are one stream inside it. | Part 6 |
| Learning and inference are not the same thing. | Part 2, Part 3 |
| Rules, search, probability, and learning are different problem-solving styles. | Part 3 |
| Deep learning is the stream that learns representations, and Transformers are one structure within it. | Part 5 |
| In services, data, tools, and operational judgment outside the model also matter. | Part 6, Part 7 |

## 17 Flows Making Up the AI Introduction

Part 1 is organized into 17 chapters.

It begins by clarifying the scope of AI and the relationship among AI, machine learning, deep learning, and generative AI. It then follows the large flow from symbolic AI, rule-based approaches, search, knowledge representation, probabilistic reasoning, machine learning, and deep learning to generative AI.

In the middle, it deals with what it means to turn a problem into a model, with inputs and outputs, with data, features, representations, parameters, learning, and inference. That language is necessary before later Parts can be read in mathematics, code, and model documentation.

It then reviews uncertainty, probability, stochasticity, search space, heuristics, supervised learning, unsupervised learning, and reinforcement learning. In particular, Chapters 6 and 7 deliberately separate boundaries that are often mixed together. Uncertainty, probability, and stochastic processes are not the same thing. A heuristic is also not the same thing as a probabilistic model. Part 1 closes those distinctions first, and later Parts recover them in statistics, evaluation, and generation. How to read a score like `0.80`, how much to trust calibration and confidence, and how to discuss uncertainty estimation more precisely are only placed on the map here, then recovered in Part 2 on probability and statistics and in Part 4 on evaluation and threshold decisions.

Later chapters move into the spread of the deep learning paradigm, generative AI, the lineage of LLMs, prompts, embeddings, vector search, RAG, AI service architecture, agents, MCP, harnesses, and operational constraints. One distinction to keep early is that generative AI is the broader category grouped by `what is generated` such as text, image, audio, or code, while LLMs are the representative model family for language data inside that category. That distinction returns in Part 6 when tokens, Transformers, the GPT line, and comparisons with BERT are handled in depth. The final chapters keep ethics, copyright, security, practical use, and future forecasting tied to technical explanation.

Chapter 9 is also handled carefully. Examples such as CNNs, GPUs, YOLO, and WaveNet are placed as background for the expansion of the deep-learning paradigm, while the direct lineage of LLMs is placed on the language-modeling side through Seq2Seq, Attention, and Transformers. That boundary needs to be fixed early so that later learning of CNNs, Transformers, GPT, and BERT in Part 5 and Part 6 does not mix up time order and direct lineage.

The same principle applies to early AI examples. Names such as Logic Theorist, GPS, MYCIN, and DENDRAL are used here only as reference points that help the reader recall representative cases of early symbolic AI and rule-based systems. The text does not expand them into long historical catalogs.

## Why the Same Term Changes Across Contexts

The hard part of studying AI again is often not the difficulty of any one concept by itself. The harder part is that the same word can mean different things in different contexts. For that reason, current explanations of AI are not stabilized by endlessly comparing dictionary definitions across languages, but by using core references such as OECD, English-language dictionaries, SEP, and NIST that support the whole structure of the book.

For example, `inference` can refer to model execution, reasoning, prediction, or generation depending on context. `model` can mean a mathematical abstraction, a trained machine-learning model, an API-delivered LLM, or even the broader service structure. `parameter` can also refer either to internal model weights, training settings, or generation settings in an LLM service.

Part 1 cuts through that `inference` confusion early. It first separates inference as `the process of running a trained model to produce output`, reasoning as `a thought process that reaches a conclusion by following grounds`, prediction as `the output the model produced`, generation as `the process of making a result such as text or image`, and statistical inference as a separate statistical context. That boundary is first closed in Chapter 5, and Part 6 returns to it again when reading next-token prediction, reasoning-like generated text, and evaluation contexts.

Part 1 builds a common language that reduces this kind of confusion. When the terms and distinctions are fixed first, later Parts on mathematics, data modeling, machine learning, deep learning, and LLMs become less scattered. For the same reason, examples such as recommendation, ranking, control, search services, and autonomous driving are only used here as short learning scenes for reading problem types, not expanded into long domain-specific explanations.

## Concepts That Return After Part 2

Part 1 is not where each technology is completed. It is the starting point that prevents later explanations from losing track of where they connect.

- Part 2 revisits the language from Part 1 in formulas, arrays, code, and runtime terms.
- Part 3 uses that basis to rebuild raw data into samples, features, baselines, and comparison structures.
- Part 4 builds on that structure to teach problem formulation, training, and evaluation in machine learning.
- Part 5 and Part 6 recover the full explanations for deep learning, LLMs, and generative AI.

Inside Part 1, every chapter is not closed as though it were a complete body of knowledge by itself. Instead, the text keeps connecting `what is introduced now` to `where the full explanation returns later`.

| What Part 1 fixes first | What level of understanding is fixed here | Where the full explanation returns later |
| --- | --- | --- |
| model, data, parameter, learning, inference | enough to know that a model takes input, produces output, and learning changes internal values | Part 2 formulas and Python basics, Part 3 data modeling, Part 4 learning and evaluation |
| supervised, unsupervised, and reinforcement learning | enough to know that their learning signals differ as labels, structure, and reward | Part 4 machine learning |
| representation learning, CNN, RNN, Attention, Transformer | enough to know that they appeared to answer different data-structure problems | Part 5 deep learning |
| generative AI, LLM, token, prompt, RAG, agent | enough to know that a generative service does not end with one model alone | Part 6 LLMs and generative AI |
| service operations, evaluation, and responsibility | enough to know that humans, policy, cost, and safety remain after model output | Part 6 evaluation and operations, Part 7 project review |

## Calculation and Implementation Questions for Later Parts

Because Part 1 is about the map, it intentionally defers some questions:

- How are loss and gradients actually calculated?
- Why do deep learning architectures branch into CNNs, RNNs, and Transformers?
- Why do LLM services need layers such as RAG, tool use, agents, and MCP?

Those questions are recovered in later Parts.

## Seeing AI as a Broad Landscape

When Part 1 is done, AI should no longer look like a single buzzword. It should look like a broad terrain built from many layers of approaches and technical streams.

1. There were attempts to solve problems through rules.
2. There were attempts to reduce computational limits through search and heuristics.
3. There were growing attempts to learn patterns from data.
4. There were expanding attempts to learn representations through deep learning.
5. There were stronger attempts to generate outputs through generative AI and LLMs.
6. There is now a need to see those outputs together with tools, retrieval, services, and responsibility.

If that understanding remains, later detailed study can keep asking where a concept sits on the larger map. Part 2 is the first step in translating that map into the language of computation, and the later Parts recover the distinctions built here with more precise explanation.

## Checks That Should Remain

- You can explain the broad relationship among AI, machine learning, deep learning, generative AI, and LLMs.
- You can explain the difference between rule-based and learning-based approaches.
- You can state the basic relationship among data, features, representations, models, parameters, learning, and inference.
- You can explain why uncertainty, probability, search, and heuristics keep reappearing in AI explanation.
- You can explain the large flow connecting prompts, embeddings, vector search, RAG, and agents.
- You can view an AI service not as one model alone but as a structure that also includes apps, data, tools, operational constraints, and responsibility.
- You are ready to separate personal working hypotheses from standard explanations.

## Sources and References

This document is an original overview that organizes the purpose and study path of Part 1. It does not directly quote external sources.
