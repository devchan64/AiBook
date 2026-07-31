# Part 6 Wrap-up

> Section ID: `P6-summary`
> Version: `v2026.07.31`

The review plan for this summary page is to separate `computation inside the model`, `prompt and retrieval`, `tool connection`, `quality evaluation`, and `service operation records` again. This distinction must remain so that, in Part 7, you do not mix the result sentence of a small project with a reviewable execution record.

Part 6 read generative AI through LLMs as the central case. The point was not to equate LLMs with all of generative AI, but to use them as a representative path for seeing generative-AI artifacts, input representations, candidate generation, evidence reinforcement, tool execution, evaluation, and operation records in one flow.

This Part did not begin with `whether the model answers well`. It first treated the artifact a person receives as something to review, then followed how that artifact is produced from computable input through tokens and embeddings and accumulates through next-candidate selection inside Transformer and GPT-family structures. After that, prompts, RAG, vector databases, tool use, agents, MCP, harnesses, evaluation, and operation constraints showed why these are not separate topics, but devices that make generative-AI use more reviewable.

## Core Sense to Keep

- Generative-AI output is an artifact that must be reviewed.
- LLM generation is not retrieving a finished answer at once, but repeatedly selecting from candidate distributions.
- Text generation becomes a computable representation through tokens and embeddings.
- Transformer and GPT structures should be read as flows that reflect context and create the next candidate.
- Pretraining, fine-tuning, instruction tuning, and alignment each learn or adjust something different.
- Prompts adjust input instructions, but they do not solve every problem of freshness, grounding, or execution.
- RAG and vector databases attach external evidence candidates before the answer and expose the original text and metadata of those candidates.
- Tool use and agents connect outside-model lookup, calculation, and execution, and they change the next action based on intermediate observations.
- MCP and harnesses are not about model capability itself. They are perspectives on tool connection format, execution records, reproducibility, and reviewability.
- A good sentence and a serviceable answer are different. Evaluation, cost, latency, failure response, and execution records must be checked together.
- Development history and the BERT family are background maps that keep the GPT-centered main current from being exaggerated.

## Easy Misunderstandings

| Misunderstanding | Standard to recover |
| --- | --- |
| LLM means the same thing as all of generative AI. | In this Part, an LLM is the central case used to explain generative AI. Do not assume image, speech, and video generation all have the same structure. |
| A larger token ID means a more important meaning. | A token ID is more similar to an index number in a vocabulary. Meaning comparison belongs to embedding vectors and similarity. |
| A nearby vector is the answer. | A nearby vector is a signal for narrowing candidates. The final answer still requires checking original text, metadata, freshness, and work conditions. |
| A better prompt solves most things. | Fresh document lookup, outside retrieval, calculation execution, permission approval, and failure records require structures outside the prompt. |
| A natural answer is ready for service. | A serviceable answer must also pass quality standards, automatic evaluation, human review, cost, latency, failure response, and execution records. |
| An AI agent is an automatic executor that handles everything to the end. | An agent must be read with planning, action, observation, stopping conditions, and human-review standards. |

## Part 6 Integrated Flows

| Flow | Standard organized |
| --- | --- |
| Starting from artifacts | Generative-AI output is an artifact, so it must be reviewed not only for right or wrong but also for evidence, format, risk, and usability. |
| Moving down into input representation | A sentence written by a person becomes tokens, token IDs, and embeddings, and these distinctions change cost, context length, retrieval, and candidate comparison. |
| Reading generation structure | A long GPT-family answer is the result of repeated next-token candidate selection, and output settings change the balance between stability and diversity. |
| Distinguishing response habits | Pretraining builds a broad language base, while fine-tuning, instruction tuning, and alignment adjust response habits for goals and allowed standards. |
| Attaching evidence and execution | Once prompt limits are crossed, RAG, vector databases, tool use, and AI agent structures become necessary. |
| Leaving connections and records | MCP helps connect tools and resources in a consistent format, and a harness wraps runs so causes and results can be inspected again. |
| Reviewing service state | LLM evaluation does not look only at answer sentences. It also includes automatic evaluation, human evaluation, operation constraints, and failure response. |
| Balancing with background and comparison | Development history and the BERT family provide comparison axes that prevent GPT-centered explanations from covering every language-model explanation. |

## Question for the Next Part

Part 7 confirms this flow through actual project artifacts. The important question is not first `what generative-AI feature should be built`, but `how requests, inputs, evidence, outputs, evaluation, failure response, and records should be left behind`.

Before moving to Part 7, keep these questions.

- Is the request fixed as a one-sentence goal and an input unit?
- Are you saying something improved without a baseline?
- If RAG is used, are retrieval evidence and failed candidates left before the answer?
- If tools or agents are used, which tools were called in what order, and where did the flow stop?
- What does automatic evaluation repeatedly check, and what contextual judgment does human evaluation handle?
- Are cost, latency, usage limits, and failure records left in a way that can guide the next revision?

These questions are what let the Part 7 project settle not as a code execution alone, but as a learning record that can be reviewed and improved again.
