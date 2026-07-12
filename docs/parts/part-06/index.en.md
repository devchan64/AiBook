# Part 6. LLMs And Generative AI

> Section ID: `P6-index`
> Version: `v2026.07.12`

Part 6 is the Part where LLMs and generative AI are `actually explained from here on`. If Part 1 through Part 5 established position and prepared the foundation, Part 6 no longer postpones the explanation. From here, the main text must explain `what structure an LLM operates on`, `why next-token prediction can still produce long answers and instruction following`, and `why retrieval, tools, and agents get attached`.

This Part should be read with the rule that the detailed explanation of a major concept appears in the same Part only once in the main text, and later chapters leave only the minimum explanation needed for the current context. So the safest way to hold the baseline is to use `P6-1.1` as the representative explanation for `tokens`, `P6-2.1` for `embeddings`, `P6-3.1` for `how to reread the Transformer from the LLM point of view`, `P6-10.1` for `RAG`, `P6-13.1` for `agents`, `P6-14.1` for `MCP`, and `P6-15.1` for `evaluation`, and then reconnect later sections back to the concept glossary and the representative Section.

The core purpose of this Part is to make it possible to explain `why generative AI services have the structure they do now`. Many readers already have user experience with chatbots, document summarization, retrieval augmentation, code generation, and agents. But that experience alone still makes it difficult to hold in one line how tokens, Transformers, GPT, pretraining, instruction tuning, RAG, tool use, and MCP connect. The responsibility of Part 6 is to fulfill exactly that promise through real main-text explanation.

So Part 6 establishes the main current first.

1. Tokens and tokenization
2. Embeddings and representation
3. Rereading the Transformer from the LLM point of view
4. The GPT family and next-token prediction
5. Pretraining, fine-tuning, instruction tuning, and alignment
6. Prompts, RAG, and vector retrieval
7. Tool use, agents, MCP, and harnesses
8. Evaluation, operations, and a small integrated practice

In this process, the BERT family and the history of LLM development are treated as a `background map` for reading the main current. In other words, background explanation is needed, but the central axis of this Part is `how generative AI works and how it connects to service structure`.

It is more stable not to read every chapter in this Part as the same kind of explanation. The level being read right now can be held as follows.

| Level being read now | The question to ask first here | Representative topics |
| --- | --- | --- |
| Internal model principle | How does the model read input and choose the next output? | Tokens, embeddings, Transformer, GPT |
| Adjustment and user experience | Why does the same structure appear as different response behavior? | Pretraining, fine-tuning, instruction tuning, alignment |
| Service connection | What has to be added outside the model to become a real function? | Prompts, RAG, vector retrieval, tool use, agents, MCP |
| Operational judgment | Why is a well-generated answer different from an operable service? | Evaluation, latency, cost, failure handling |
| Background axis | Where did the main current come from, and what is it different from? | LLM history, BERT-family comparison |

Part 6 currently keeps the existing chapter order and instead makes the main current and the background axis more explicit within that order. Therefore, the more stable reading is to treat Chapter 1 through Chapter 17 as the main current first, and then treat Chapter 18 `History of LLM Development` and Chapter 19 `The BERT Family` as a comparison/background axis attached afterward.

And this Part does not stop at explaining concepts, but also makes the reader see together `what should be checked first and what judgment it should lead to`, such as:

- tokenization -> how was the input split, and how does it affect context length?
- RAG -> what evidence was found, and why was that evidence selected?
- agent -> through what steps did execution proceed, and at what point is review needed?
- evaluation/operations -> how should answer quality, failure cases, and next actions be organized?

## The Order For Reading This Part

Part 6 holds its flow best when read in the following order.

1. First, look at what the model actually reads as input through tokens, tokenization, and embeddings.
2. Next, read the core generation structure through the Transformer, GPT, and next-token prediction.
3. Then, use pretraining, instruction tuning, and alignment to see why the same structure leads to different user experiences.
4. Finally, read the service-connection structure through RAG, tool use, agents, MCP, evaluation, and operations.
5. After reading the full main current, attach the history of LLM development and the BERT family to reorganize the `direct lineage` and the `comparison standard`.

If this order is lost, Part 6 can easily look like a `list of terms`. If the order is maintained, it reads as a single flow of `input units -> generative structure -> user-experience adjustment -> service connection`.

### Current Recommended Reading Route

| Reading bundle | Relevant chapters | Why read it this way |
| --- | --- | --- |
| Main current 1. Input and representation | Chapters 1-2 | The later structure becomes less blurry only when tokens, tokenization, and embeddings are fixed first. |
| Main current 2. Generative structure | Chapters 3-5 | Transformer, GPT, and next-token prediction are the most important structural axis of Part 6. |
| Main current 3. Learning and adjustment | Chapters 6-8 | Pretraining, fine-tuning, instruction tuning, and alignment are read as a single adjustment axis. |
| Main current 4. Service connection | Chapters 9-14 | Prompts, RAG, vector retrieval, tool use, agents, and MCP are bundled as service structure. |
| Main current 5. Evaluation and integration | Chapters 15-17 | Evaluation, operations, and a small integrated practice distinguish `a good model` from `a good service`. |
| Background axis | Chapters 18-19 | History and BERT-family comparison are attached afterward to reread the main current more accurately. |

Within this bundle, Chapter 4, 6, 8, and 10 are not pulled forward again. Chapter 4 closes GPT's generative position immediately after the Transformer; Chapter 6 is the first chapter that opens `what learning acquires first` right after next-token prediction; Chapter 8 closes `the adjustment layer that makes the model follow user instructions` after pretraining and fine-tuning; and Chapter 10 reads as `the structure that attaches external evidence` only after you first confirm where prompts alone are insufficient. For that reason, the current order best matches the flow of the main current.

If the main current is shortened further, it can be summarized into the following stages.

| Main-current stage | Core question | Chapters bundled here |
| --- | --- | --- |
| Tokens and input representation | What does the model read as input? | Chapters 1-2 |
| Transformer and the GPT generative structure | Why does next-token prediction lead into generation? | Chapters 3-5 |
| Learning and adjustment | Why does the same structure change into different user experiences? | Chapters 6-8 |
| Retrieval and execution connection | When are prompts alone insufficient, and when are RAG, tools, and agents needed? | Chapters 9-14 |
| Evaluation and operations | Why is a good answer different from an operable service? | Chapters 15-17 |
| Background axis | Through what history and comparison perspective should this main current be reread? | Chapters 18-19 |

The key of this table is to make Chapter 18 and Chapter 19 read not as `front matter that blocks the main current`, but as a background axis attached after the full main current is read.

From the perspective of service experience, the main current of one request can be reduced to the following four stages.

| The main-current flow of one request | What to look at first here |
| --- | --- |
| Read the input | Tokens, embeddings, context representation |
| Generate or adjust the answer | Transformer, GPT, pretraining, instruction tuning |
| Supplement from outside if needed | RAG, tool use, agents, MCP |
| Check the result | Evaluation, operations, failure causes, next actions |

## The Earlier Previews That This Part Must Actually Recover

Part 6 must actually fill in the LLM and generative-AI explanations postponed in the earlier Parts. In particular, the following items must be explained here in the main text, not merely introduced by name.

| Topic postponed in earlier Parts | What this Part must actually explain |
| --- | --- |
| Tokens and tokenization | Why input is split into tokens rather than whole words, and how that connects to cost and length |
| The Transformer and next-token prediction | Why this structure leads into long generation and instruction following |
| GPT and BERT | Why the structure and the strong task orientation diverged |
| Pretraining and instruction tuning | At what level the model learns general language patterns and instruction following |
| RAG and vector retrieval | Why evidence outside the model must be pulled in |
| Tool use, agents, and MCP | Why generation alone is insufficient and why an execution environment is attached |
| Evaluation and operations | Why a good answer and a good service are not the same thing |

If this standard is missing, Part 6 weakens back into a `map of generative-AI terms`.

In other words, the standard that Part 6 must keep is `whether the topics previewed earlier are actually recovered here`. If the names reappear but the explanation is empty, this Part does not fulfill its responsibility.

## The Purpose Of This Part

This Part is the section for understanding LLMs and generative AI again across three levels: `model structure`, `generation mechanism`, and `service-connection structure`.

Generative AI is often remembered only as `a chatbot that answers well`. But in reality, the following questions come with it.

- How does an LLM read data and choose the next output?
- What is different between GPT and BERT, and why do their use cases diverge?
- What kinds of tasks are handled by prompts alone, and what kinds of tasks need RAG or tools?
- Why are agents and MCP not simply prompt-expansion problems, but execution-environment problems?
- Why does a generative-AI service not end with a single model?

Part 6 prepares the ability to answer those questions. It does not go deep into paper implementation details or large-scale distributed learning systems. Instead, its purpose is to let the reader distinguish, when reading LLM-related documents, product descriptions, and practical structures, whether `what is being explained now is an internal model principle, an adjustment layer, a service component, or an operational judgment`.

## What This Part Explains And Does Not Explain

Part 6 is the Part that explains the main current of LLMs and generative AI. Therefore, the following content is explained within the scope of the main text.

- The basic structure of tokens, embeddings, the Transformer, GPT, and next-token prediction
- The role distinction among pretraining, fine-tuning, instruction tuning, and alignment
- The connection structure of prompts, RAG, vector search, tool use, agents, MCP, and harnesses
- Evaluation, operations, failure handling, and a small integrated feature flow

By contrast, the following topics are not treated in full depth in this Part.

- Rapidly changing product comparisons and metric races among the latest commercial models
- Large-scale distributed-learning infrastructure and paper-implementation details
- Detailed usage of every agent framework and vendor tool

This omission is not avoidance of the core, but scope control. The responsibility of Part 6 is to explain `why generative AI services have this structure`, while the race among current products and framework-specific usage details remain outside the scope of the current edition's main text.

## The Goals Of This Part

After reading Part 6, the goal is to reach roughly the following level of understanding.

- You can explain why the Transformer is the core structure of LLMs.
- You can explain that the GPT family performs generative tasks through `next-token prediction`.
- You can explain in broad flow what roles temperature, decoding, and instruction tuning play in generation.
- You can distinguish why the BERT family and the GPT family were each stronger in `read-and-judge tasks` and `generate tasks`, respectively.
- You can explain when RAG is needed and what its limits are.
- You can explain what problems embeddings, vector search, tool use, agents, MCP, and harnesses are attached to solve.
- You can read the failure modes of generative-AI services from the perspective of evaluation and operations.
- You can explain in what flow a small generative-AI feature should be implemented and reviewed.

If these goals are rewritten from the standpoint of preparing for Part 6, they can also be organized as follows.

| Structure to understand in Part 6 | Representative judgment standard to check together in Part 6 |
| --- | --- |
| Tokens and input representation | Token length, context limits, input-design judgment |
| Generation and next-token prediction | Comparison of generated results, decoding-setting checks, observation of output quality |
| RAG and retrieval integration | Retrieval candidates, selected evidence, and judgment about how evidence connects to the answer |
| Agent and tool execution | Step planning, execution results, and points needing human review |
| Evaluation and operations | Interpretation of failure cases, operational constraints, and the next improvement action |

## Reading Standards For Entry-Level Readers

In this Part, familiar service experience and unfamiliar structural terms appear mixed together. Rather than trying to hold every implementation detail at once, you first need to separate levels with the following three questions.

| Question to hold first | Why this question is needed | What is enough to hold in this Part |
| --- | --- | --- |
| Is what is being explained now `an internal model principle`, or `a service-connection method`? | In LLM contexts, tokens, attention, RAG, and agents may appear in one document together, but they are not concepts on the same level. | First fix the distinction that Transformer and next-token prediction are model principles, while RAG and tool use are service-connection methods. |
| What does this system `generate directly`, and what does it `retrieve or execute from outside`? | To understand generative AI, you must distinguish cases where the model answers only from internal knowledge from cases where external documents or tools are attached. | First distinguish tasks handled by prompts alone from tasks that require RAG or tools. |
| Does making the result better mean `improving model performance`, or `improving service design`? | Generation-quality problems are not always solved only by retraining the model. Retrieval, prompts, tool connection, and evaluation design act together. | You need to separate the model itself from the service components. |

At the shortest level, it can be summarized as follows. An LLM is a structure that predicts the next token, and that structure leads into long-form generation and instruction following. RAG and tools are attached to compensate for knowledge limits and execution limits, and in real services you must also look at agents, MCP, evaluation, and operations together.

## What It Explains

Part 6 can largely be read in five bundles: `input and representation`, `the LLM core structure`, `learning and adjustment`, `service connection and operations`, and `the background axis`.

First, the early part treats tokenization and embeddings. This section explains what units the model actually reads as input and through what representation it begins computation.

Next, the main current treats the Transformer, the GPT family, next-token prediction, the generative process, pretraining, fine-tuning, instruction tuning, and alignment. This bundle is the core section that explains both `why an LLM can generate` and `how the user experience is adjusted`.

After that, it treats prompts, RAG, vector databases, tool use, agents, MCP, harnesses, evaluation, operations, and a small integrated practice. Here the explanation stops being only about a model and instead shows through what connection structure a generative-AI service actually works, before regrouping that structure into a very small feature flow at the end.

On the final background axis, it rereads the history of LLM development and the BERT family. The purpose of this section is not to delay the main current, but to reorganize the GPT-centered explanation read earlier through a historical and comparative perspective.

What matters in this section is not to mix the background axis with the main-current axis. History and comparison are necessary, but the main question of this Part remains `why generative AI operates in this structure`.

## Why It Is Needed

When relearning generative AI, the most common confusion is that `what the model does` and `what the service additionally attaches` get mixed together.

For example, if you cannot distinguish whether an answer improved because:

- a larger model was used
- the prompt changed
- external documents were attached
- a calculator was called
- the task was split into several steps of execution

then instead of understanding generative AI, you end up memorizing a feature list.

Part 6 builds a common structure for reducing this confusion. Starting from internal principles such as tokens and the Transformer, and continuing to why RAG and tool use are attached and why agents and MCP are needed, lets you reinterpret later product documents and practical system designs through the same structure.

At the same time, understanding this structure also lets you distinguish more clearly later what is an input-design problem, what is an evidence-connection problem, and what is an execution-stage problem.

## Understanding That Should Remain After This Part

After this Part, you should be able to see generative AI not as a simple chatbot feature, but as a structure where several levels are connected. The process that turns tokens into representations, the process by which the Transformer reflects context, the process by which next-token prediction leads into generation, the process by which instruction tuning and decoding change user experience, the process by which RAG and tool use compensate for the model's limits, and the process by which agents, MCP, evaluation, and operations determine service quality should all be visible in one flow.

Once this understanding forms, you can move beyond the oversimplification that `LLMs are the whole of AI`, and you can also reduce the misunderstanding that `if only the model gets better, every service problem is solved`. Part 6 is the Part that creates the baseline for reading LLMs and generative AI not as a buzzword, but as a technical system with structure and constraints.

Therefore, the final outcome to check on this index page is whether Part 6 can be read not as `a collection of chatbot features`, but as the main-current Part that explains both internal model principles and service-connection structure.

## Completion Criteria

- You can explain why the Transformer is the core structure of LLMs.
- You can explain that the GPT family is a generative model based on next-token prediction.
- You can explain the difference between the BERT family and the GPT family as the difference between reading-centered tasks and generation-centered tasks.
- You can explain what limitations prompts, RAG, vector retrieval, and tool use each compensate for.
- You can explain that agents, MCP, and harnesses belong to the topic of execution environment rather than the topic of prompts.
- You can describe the major failure types of generative-AI systems from the standpoint of evaluation and operations.
- You can explain how to design and review a small generative-AI feature as a request flow.

## Sources And References

This document is an internal overview that organizes the purpose and learning path of Part 6. It does not directly cite external sources.
