# Part 6. LLMs and Generative AI

> Section ID: `P6-index`
> Version: `v2026.07.26`

Part 6 moves the deep-learning structures covered in Part 5 into the actual experience of using generative AI. The starting point here is not tokens or the implementation details of Transformers. It is the generative-AI artifact that a person actually receives. First, this Part asks what generative AI creates, why an LLM (large language model) is useful as the representative path, and why generation should be read not as pulling out one finished answer but as repeated candidate distributions and selection.

Then it follows how text becomes a computable input through tokens, token IDs, and embeddings. Transformer and GPT-family structures are read as flows that create the next candidate from that input. After that, pretraining, fine-tuning, instruction tuning, and alignment show how response habits are formed.

In the middle and later sections, the discussion expands from inside-the-model explanations into actual usage structures. Prompts, RAG (retrieval-augmented generation), vector databases, tool use, agents, MCP (Model Context Protocol), and harnesses are not treated as separate buzzwords. They are reinforcement structures that make generated results easier to review. Finally, LLM evaluation, automatic and human evaluation, service operation constraints, failure response, and the run records of a small generative-AI feature separate a natural answer from a reviewable service result. Development history and the BERT family are placed after the main current as a background map and comparison axis so the GPT-centered explanation does not become overgeneralized.

## Part 6 Generative AI Understanding Standards

- How are the artifacts created by generative AI different from classification or numeric prediction?
- Why read LLMs as the central example rather than as all of generative AI?
- Why should LLM generation be read as repeated candidate distributions and selection?
- In what order do tokens, embeddings, Transformers, GPT, and next-token prediction connect?
- What differs between tasks that can be handled by prompts alone and tasks that need RAG, vector databases, tool use, or agents?
- Why are MCP and harnesses closer to questions of connection format, execution records, and reproducibility than to model capability itself?
- Why is a natural generated result different from a result that can be evaluated, operated, and recovered from failure?

## Part Scope

This Part does not equate LLMs with all of generative AI. Instead, it uses LLMs as the central case for explaining the generative-AI flows that readers most often encounter: text generation, chat interfaces, RAG, tool use, and AI agents.

This Part is also not an implementation guide for training large models directly. Instead, it asks how a request becomes an input unit, how the model creates candidates, when external evidence and tools become necessary, and how results should be evaluated and recorded. Part 7 handles the implementation details of actual projects. Part 6 prepares the judgment standards needed to understand those projects.

## Module Reading Axes

| Range | Central question | Sense to retain |
| --- | --- | --- |
| Module 1. Generative AI And The Position Of LLMs | Why should a generative-AI artifact first be treated as something to review? | An LLM is a representative path for reading generative AI, not the same thing as all of it. |
| Module 2. Input Units And Representations For Text Generation | How does text become a computable input and a comparable representation? | Tokens, token IDs, and embeddings are values at different levels. |
| Module 3. LLM Structures That Create The Next Candidate | How should Transformers and GPT-family models be read as creating the next candidate? | Even a long answer is the accumulated result of next-candidate selections. |
| Module 4. Learning And Adjustment That Form Response Habits | What do pretraining, fine-tuning, instruction tuning, and alignment change differently? | Learning a lot and answering in the desired way are different. |
| Module 5. Prompts And Evidence Reinforcement | What must be attached from outside when prompts are not enough? | Freshness, grounding, and retrieval failure are not solved by prompt wording alone. |
| Module 6. Tool And Agent Execution Structures | How are outside-model execution and multistep work connected? | Tools, agents, MCP, and harnesses reveal problems of connection and observation. |
| Module 7. Reviewable Service State | What differs between a good sentence and a serviceable answer? | Evaluation, cost, latency, failure response, and execution records must remain together. |
| Module 8. Background Map And Comparison | How can we read the GPT-centered main current without overgeneralizing it? | Development history and the BERT family help separate direct lineage from comparison axes. |

## Generative AI Reading Flow

```text
generative-AI artifacts
-> LLM as a representative path
-> candidate distributions and repeated selection
-> tokens and embeddings
-> LLM structures that create the next candidate
-> learning and adjustment that shape response habits
-> prompts and evidence reinforcement
-> tool and AI agent execution structure
-> reviewable service state
-> background map and comparison
```

After Part 6, generative AI should no longer look only like `a model that produces plausible answers`. It should be readable as `a system that combines requests, input representations, candidate generation, evidence reinforcement, tool execution, evaluation, and operation records`. This standard becomes the starting point for deciding what to build and what to record in the small project of Part 7.
