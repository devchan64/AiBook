# Part 6 Wrap-up. LLM And Generative AI Review

> Section ID: `P6-summary`
> Version: `v2026.07.12`

Part 6 was the section that moved one step beyond consuming generative AI as `an impressive answer machine` and regrouped, through real explanation, what input units an LLM reads, what structure it is trained on, and inside what service structure it actually works.

The core of this Part is not to stop at seeing an LLM merely as `a model that talks well`. Only when the flow from tokens, embeddings, the Transformer, pretraining, fine-tuning, RAG, tool use, agents, evaluation, and operational constraints is seen together does the real structure of generative AI become visible.

In other words, Part 6 was the Part that had to actually explain GPT, next-token prediction, instruction tuning, RAG, tool use, and agents that Part 1 through Part 4 had left behind with `this will be explained later`.

When reopening this Part, the safest way is to distinguish what level the current explanation belongs to first.

| Level to recover again | The question to check here | Representative topics |
| --- | --- | --- |
| Internal model principle | How does the model read input and choose the next output? | Tokens, embeddings, Transformer, GPT |
| Adjustment and user experience | Why does the same structure lead to differences in instruction following and conversational quality? | Pretraining, fine-tuning, instruction tuning, alignment |
| Service connection | What must be attached outside the model for it to become a real function? | Prompts, RAG, vector retrieval, tool use, agents, MCP |
| Operational judgment | How do we separate answer quality from service quality? | Evaluation, cost, latency, failure handling |
| Background axis | Against what lineage and comparison should the main current be reread? | LLM history, the BERT family |

## The Core Flow Covered In This Part

The flow of Part 6 can be organized as follows.

| Flow stage | The question to hold onto at this stage |
| --- | --- |
| Tokens and tokenization | In what input units does the model read a sentence? |
| Embeddings and semantic space | How are symbols turned into comparable representations? |
| The Transformer, the GPT family, and next-token prediction | Why does next-token prediction lead into long-form generation and instruction following? |
| Pretraining, fine-tuning, instruction tuning, alignment | How is the same structure adjusted into different user experiences? |
| Prompts, RAG, vector databases | When the model's internal memory is not enough, what is attached from outside? |
| Tool use, function calling, agents | How does the flow continue beyond answering into retrieval and execution? |
| MCP and harnesses | From what perspective should tool-connection and execution-record environments be organized? |
| Evaluation, automatic evaluation, human evaluation | What should be checked automatically, and what should remain for human judgment? |
| Service constraints, failure response, operations | Why are a good answer and an operable service different things? |
| Regrouping as a small generative-AI feature flow | How does one question close through retrieval, answering, evaluation, and recording? |
| Reorganizing the history and the BERT family as a background axis | How should direct lineage and comparison background be separated? |

The outcome to confirm in this flow is that you can read `the model itself` separately from `the system around the model`. After Part 6, it should become clear that writing a good prompt, attaching retrieval, calling tools, and recording failures in operations are problems on different levels. In particular, it is important not to lose the sequence `internal model principle -> adjustment layer -> service connection -> operational judgment`.

Under the current table of contents, this Part reads more naturally as `input and representation -> LLM core structure -> learning and adjustment -> prompts and evidence connection -> execution structure -> evaluation, operations, and integrated practice -> background axis`. In other words, it is most stable to first read Chapter 1 through Chapter 17 as the main current and then read Chapter 18 `History of LLM Development` and Chapter 19 `The BERT Family` as a background axis attached afterward.

If you fix the representative Sections again in the current Part 6, `P6-10.1` carries RAG, `P6-14.2` carries harnesses, `P6-15.1` carries evaluation, `P6-15.2` carries automatic and human evaluation, `P6-17.2` carries request execution records, `P6-18.2` carries direct lineage and surrounding evidence, and `P6-19.1` carries the BERT comparison axis. When reviewing, fixing these baselines first also makes it easier to follow the connection between the concept glossary and the main text.

At the first review, it is enough to hold the following three lines first.

| Handle to recover first | What to check immediately here |
| --- | --- |
| The main current of Chapters 1-17 | How input, generation, retrieval/execution, and evaluation/operations close as one request flow |
| The background axis of Chapters 18-19 | Against what history and comparison standard that main current stands |
| The transition into Part 6 outputs | Into what run records and review documents this structure should be rewritten |

The same flow can be compressed at the request level into the following one line.

`Read the question as tokens -> attach documents or tools if needed -> generate the answer -> confirm it again through evaluation and recording.`

If this main current and background axis are separated again, the most stable reading becomes the following.

| Main current read first | What to confirm here |
| --- | --- |
| Tokens and embeddings | Input units and representation |
| Transformer, GPT, next-token prediction | The core of generative structure |
| Pretraining, fine-tuning, instruction tuning, alignment | The adjustment layer that changes user experience |
| Prompts, RAG, vector retrieval, tool use, agents | Retrieval and execution connection outside the model |
| Evaluation, operations, integrated mini practice | Quality judgment and recording structure |

| Background axis attached later | What gets reread here |
| --- | --- |
| History of LLM development | On what lineage the current main current stands |
| Comparison with the BERT family | How to distinguish the generation-centered GPT family from the reading-centered family |

In other words, Part 6 is safest when read in the order `how it works first`, then `where it came from and what it differs from`.

If this main current is reread once more as the shortest flow of a service request, it compresses into the following four stages.

| The main-current flow of one request | What to check first here |
| --- | --- |
| Read the input | Tokens, embeddings, context representation |
| Generate or adjust the answer | Transformer, GPT, pretraining, instruction tuning |
| Supplement from outside if needed | RAG, tool use, agents, MCP |
| Check and leave the result | Evaluation, operations, records, next actions |

At the first review, the following two lines are enough to quickly reorganize the main current and the background axis.

| Standard to recover again | One-line summary |
| --- | --- |
| Chapters 1-17 | The chapters that explain the main current of generative AI |
| Chapters 18-19 | The history and comparison background that let that main current be read more precisely afterward |

If this flow is rewritten from the perspective of the `artifacts` that Part 6 passes forward, it becomes the following.

| Structure understood in Part 6 | The actual artifact to leave in Part 6 |
| --- | --- |
| Tokens and input representation | Token-length notes, context-limit checklists, input-comparison records |
| Generation and next-token prediction | Generated-result comparison tables, decoding-setting notes, output-quality observations |
| RAG and retrieval integration | Retrieval-candidate lists, selected-evidence notes, answer-to-evidence connection records |
| Agent execution loops | Step plans, execution-result records, final review summaries |
| Evaluation and operations | Review summaries, failure-case records, next-improvement actions |

## Concepts That Must Be Remembered

The concepts that especially need to remain after Part 6 are the following.

| Distinction | Perspective to remember |
| --- | --- |
| Token | The model reads input and output in token units, not as whole sentences the way a person sees them. |
| Embedding | An embedding turns a symbol into a vector representation whose meaning can be compared. |
| Transformer | The central structure of today's LLMs stands on self-attention and parallel computation. |
| Pretraining | LLMs first learn language patterns from large-scale data through next-token prediction. |
| Fine-tuning and alignment | There is a separate stage that adjusts the model more closely toward a specific task or instruction. |
| Prompt | A prompt is a way of structuring input, not a process that newly trains the model's knowledge itself. |
| RAG | RAG does not increase the model's internal memory; it retrieves external evidence and connects it as input context. |
| Vector retrieval | It retrieves documents that are semantically close, but retrieval quality depends jointly on embedding quality and index structure. |
| Agent | An agent is an execution structure that connects a goal into multiple steps of planning, action, and observation. |
| MCP and harnesses | MCP organizes the tool-connection interface, while a harness organizes the execution, evaluation, and recording environment. |
| Evaluation and operations | Good answer examples and good service operations are not the same thing. Quality, cost, latency, and failure handling must be examined together. |

After reading this table, the following distinction should remain at the end.

- `Model structure`: tokens, embeddings, the Transformer, pretraining
- `Service connection`: prompts, RAG, vector retrieval, tool use, agents
- `Operational judgment`: evaluation, automatic/human review, cost, latency, failure handling

This distinction is also the standard for deciding what should be recorded first in Part 6.

- If model structure was explained, then `input and output records` should remain next.
- If service connection was explained, then `evidence and tool-result records` should remain next.
- If operational judgment was explained, then `evaluation state and failure records` should remain next.

## Points That Are Easy To Misunderstand

In Part 6, the following misunderstandings require particular caution.

- You should not treat LLMs as the whole of AI.
- You should not read prompts and fine-tuning as the same thing.
- You should not misunderstand RAG as `the model has fully understood external facts`.
- The fact that tool use is attached does not automatically mean the system is an agent.
- You should not read MCP as if it were a single product name or a feature limited to a particular vendor.
- You should not fix a harness as the name of one single tool.
- A high automatic-evaluation score alone does not mean the real user experience is immediately good.
- Even if generated quality looks good, service completion still requires cost, latency, permissions, and failure handling.
- Understanding retrieval, tool use, and evaluation separately does not mean you can immediately implement them as one request flow.
- You should not read every famous event in the history of deep learning as part of the direct lineage of LLMs.

The misunderstandings that especially need to be checked again in the later part of Part 6 are the following.

| A scene that is easy to confuse | The more accurate distinction |
| --- | --- |
| Since there is a source link, groundedness must also be sufficient | The existence of a link and the actual correctness of interpretation are different things. |
| Since automatic evaluation passed, service quality must also be sufficient | Automatic checks and human review catch different kinds of failure. |
| A larger model means a better service | Quality, latency, cost, and throughput must be examined together. |
| Timeout and hallucination are both just failures | System failure and model failure require different response paths. |

## Questions This Part Does Not Close

Part 6 focused on explaining the structure and service connection of generative AI. Therefore, the following questions are intentionally passed into the project context of Part 7.

- With real data and logs, what minimum feature should be built first?
- Through what documents and artifacts should baselines, improvement experiments, and failure records be left behind?
- In what order should deployment and operations review be reflected in project documents?

In other words, Part 6 is the Part that explains `why this structure is needed`, while Part 7 is the Part that verifies that structure again through actual project artifacts.

The most important transition passed forward at this point is the following.

- In Part 6, you understand `the names of the concepts`.
- In Part 7, you confirm `what record items those names must become`.

For example:

- tokenization should remain as records of input length and context usage
- RAG should remain as notes about selected evidence and answer-to-evidence connection
- agents should remain as records of execution steps and approval status
- operational failure should remain as records of failure causes and next actions

The practical questions especially passed forward here are the following.

- Which questions close with prompts alone, and which require retrieval or tools?
- In what run record should retrieval failure, lack of evidence, and execution failure be left?
- In what order should automatic evaluation and human review be placed in actual project documents?

## Questions To Check Before Moving To The Next Part

Before moving to Part 7, you should be able to answer the following questions.

- Can you explain why tokens and tokenization affect model cost and output length?
- Can you explain embeddings and vector retrieval in the context of RAG?
- Can you describe in broad flow why the Transformer became the basic structure of LLMs?
- Can you distinguish pretraining, fine-tuning, instruction tuning, and alignment?
- Can you say what level of problem prompts, RAG, tool use, and agents each belong to?
- Can you explain MCP and harnesses from the standpoint of `organizing the execution environment`?
- Can you explain that model quality and service quality are not always the same thing?
- Can you regroup a small generative-AI feature again as a flow of request, evidence, output, and recording?
- Can you explain history while distinguishing direct lineage from surrounding evidence?

## Closing Part 6

Once Part 6 is complete, you should be able to distinguish, whenever you hear an explanation of generative AI, what is a matter of internal model structure, what is a matter of service design, and what is a matter of operations and evaluation.

Once that distinction appears, it becomes clear that the single sentence `the LLM is smart` is not enough. In reality, input units, representations, learning method, retrieval connection, tool calling, execution environment, evaluation standards, and operational constraints all work together.

Part 6 is the final place to organize that structure before it is passed into the actual project unit of Part 7.

## Sources And References

This document is an internal summary of all of Part 6. It does not directly cite external sources.
