# P1-13.3 The Flow That Leads into RAG

> Section ID: `P1-13.3`
> Version: `v2026.07.07`

P1-13.1 introduced embeddings, which turn text into vectors. P1-13.2 introduced similarity search, which finds document vectors close to a query vector.

Now the next question appears:

> how do retrieved document candidates get connected to the LLM’s answer?

`RAG`, or retrieval-augmented generation, is one representative answer.

> RAG is a structure that first retrieves external material,  
> then places that retrieved material into the generation input so the model can answer with it as context

The important point is that RAG is not an `answer guarantee device`. It is a structure for adding more context that the LLM can refer to. If the retrieved result is wrong or incomplete, the answer can still fail.

Part 1 introduces the basic distinctions among `RAG`, `retrieval`, `augmentation`, `generation`, `parametric memory`, `non-parametric memory`, and `provenance` here. Section 13.1 explained embeddings. Section 13.2 explained similarity search. This section connects those two steps into:

> adding retrieval results into LLM input context

Implementation details and service architecture return later in P1-13.4 and Chapter 14.

## Scope of This Section

This section gives a conceptual view of the full RAG flow. It does not explain vector databases, indexes, ANN methods, or graph-based retrieval structures in detail. Those return in P1-13.4.

These terms refer to different stages and different memory resources. Their roles can first be separated like this:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| RAG | a structure that attaches retrieval results to generation input | the connection stage of Chapter 13 |
| retrieval | the stage that finds related document candidates | the preparation of external material |
| augmentation | the stage that adds retrieved documents to the input context | the construction of reference context |
| generation | the stage where the LLM makes an answer from the augmented input | the final response step |
| parametric memory | knowledge compressed inside model parameters | the intuition of the model’s internal memory |
| non-parametric memory | searchable external material such as document stores | the external knowledge RAG adds |
| provenance | information that tracks what sources were used | the element that connects to evidence review |

The baseline distinctions are:

- RAG connects retrieval and generation
- external documents are evidence outside the model
- source tracking is a separate review element

Later sections in P1-14 place RAG inside broader service architecture and tool-use flow. This section focuses only on how retrieval results enter the LLM input.

This section also does not describe RAG as `a hallucination removal mechanism`. Its safer role is:

> a structure for attaching candidate evidence into input context

with review responsibility still remaining afterward.

| Topic | Question in this section |
| --- | --- |
| retrieval | what outside material should be brought in? |
| augmentation | how should the retrieved material be attached to the input context? |
| generation | what does the LLM generate from the augmented input? |
| limit | why does RAG still not guarantee factual verification automatically? |

## Goal of This Section

- Understand RAG as a structure that combines retrieval and generation.
- Explain the flow in which retrieved results become part of the LLM’s context.
- Distinguish model-internal knowledge and external searchable material at an intuitive level.
- Understand that RAG can help with recency, evidence, and source tracking, but cannot automatically guarantee them.
- Prepare to move into the AI service structures of P1-14.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| RAG is a structure that connects retrieval and generation | This shows the difference between an answer from the model alone and an answer supported by retrieved material. | It is enough to understand that documents are first found, then used as a basis for the answer. |
| external documents can supplement evidence and newer information outside model parameters | This helps separate model memory from document evidence. | It is enough to understand that documents can provide newer or more specific material than the model alone. |
| even with RAG, outputs still need review | This prevents the misunderstanding that adding retrieval makes the output automatically correct. | It is enough to understand that wrong retrieval or wrong reading can still produce wrong answers. |

## RAG Retrieves First, Then Generates

At the simplest level, the RAG flow looks like this:

> user question  
> -> create a question embedding  
> -> retrieve related candidates from a document store  
> -> add those retrieved chunks into the prompt context  
> -> let the LLM generate an answer

Suppose the user asks:

> why can prompts not guarantee factuality?

The retrieval system may find candidates such as:

| Retrieved candidate | Role |
| --- | --- |
| P1-12.3 The limits and evaluation of prompts | provides factuality, evidence, and evaluation criteria |
| P1-10.3 The quality and risk of generated outputs | explains hallucination and missing evidence |
| P1-13.2 The intuition of similarity search | explains why retrieval results are only candidates |

The system can then place those chunks into the LLM input:

> question:  
> why can prompts not guarantee factuality?
>
> reference material:  
> - relevant passage from P1-12.3  
> - relevant passage from P1-10.3  
> - relevant passage from P1-13.2
>
> instruction:  
> answer based on the reference material

The final answer is now generated not only from model-internal knowledge, but also from retrieved external material.

## Retrieval Works Like Attaching External Memory

The RAG paper describes a problem setting where pretrained models store knowledge in their parameters, but have limits in precise access and in updating that knowledge. RAG addresses that by combining the model with an external `non-parametric memory`.

At this level, the intuition is:

| Distinction | Intuition |
| --- | --- |
| model-internal knowledge (parametric memory) | knowledge compressed into model parameters during training |
| external searchable material (non-parametric memory) | document stores or indexes that can later be added, updated, or searched |

Internal model knowledge can be fast to use, but it does not automatically know newly added organizational documents, updated policies, or later-written project notes.

External searchable material can be updated:

- documents can be added
- documents can be edited
- older versions can be replaced

That is why RAG can help with issues such as:

| Problem | How RAG can help |
| --- | --- |
| recency | newer documents can be added to the retrieval target |
| evidence | supporting passages can be attached to the answer process |
| provenance | the system can record which source passages were used |
| domain knowledge | organization-specific or project-specific documents can be connected |

But `can help` is not the same thing as `guarantees`. If the retrieved document is wrong, irrelevant, or misunderstood by the LLM, the answer can still be wrong.

## RAG Does Not Replace Prompting

RAG does not remove the need for prompts. It is better understood as a way of preparing the `context` that the prompt will contain.

| Element | Role |
| --- | --- |
| prompt | gives the LLM the task instruction, format, and constraints |
| retrieval | finds relevant external material |
| augmentation | inserts that material into the input context |
| generation | lets the LLM answer from the augmented input |

Without RAG, a person must gather and paste the reference material manually. With RAG, the system can retrieve related material first and then attach it automatically to the prompt context.

> prompt only:  
> the human manually prepares the question and supporting material
>
> prompt with RAG:  
> the system retrieves relevant supporting material and attaches it into the input context

So RAG is not the opposite of prompt engineering. It is a more systematic way of preparing the context that goes into the prompt.

## The Quality of RAG Depends on Several Stages

RAG is not a magical single-step feature. It is closer to a pipeline:

> document preparation  
> -> chunking  
> -> embedding generation  
> -> retrieval  
> -> reranking or filtering  
> -> prompt construction  
> -> answer generation  
> -> source display and review

Each stage can create problems:

| Stage | Possible problem |
| --- | --- |
| document preparation | old, wrong, or duplicated documents may be mixed in |
| chunking | needed context may be split across several chunks |
| embedding | the question and documents may not be represented well in the same semantic space |
| retrieval | irrelevant candidates may rank too high |
| prompt construction | too much material may blur the core point |
| generation | the LLM may mix in unsupported content or summarize badly |
| source display | the displayed source may not fully match the actual basis of the answer |

That is why the safer perspective is not:

> once retrieval is added, the system is safe

but:

> retrieval, input construction, generation, and review all have to be designed together

## RAG Is Not a Fact-Verification Device

One of the most common early misunderstandings is:

> misunderstanding:  
> if we use RAG, hallucinations disappear
>
> safer explanation:  
> RAG can increase the chance of grounded answers by attaching outside material,  
> but it does not automatically remove retrieval errors or generation errors

The following situations are all possible:

| Situation | Result |
| --- | --- |
| the wrong document is retrieved | the LLM may answer from false evidence |
| the relevant document is not retrieved | the LLM may fall back on general knowledge or guesses |
| only part of the needed document is retrieved | the answer may lose crucial context |
| conflicting sources are retrieved | someone still needs to judge which source is more reliable |
| a source is displayed | source display alone does not prove the answer is correct |

This connects directly to the writing principles of the book. AI-generated explanations are drafts, and factual claims still require evidence review. RAG can help find candidate evidence, but the final judgment remains part of the review process.

## A Small Example of the RAG Flow

Suppose a study-oriented document collection is the retrieval target.

> question:  
> is an embedding the same thing as meaning itself?

The retrieval stage may produce candidates such as:

| Candidate | Why it appears |
| --- | --- |
| P1-13.1 an embedding is not meaning itself | directly connected to the question |
| P1-13.2 a nearby vector is not always a good answer | connected to the limits of search results |
| P1-11.1 statistical language models and embeddings | connected to historical background |

The RAG input may then look like:

> question:  
> is an embedding the same thing as meaning itself?
>
> reference material:  
> [retrieved passage from P1-13.1]  
> [retrieved passage from P1-13.2]
>
> answer instruction:  
> explain this for a beginner based on the reference material  
> do not state unsupported content as certain

A good answer should preserve points like:

> an embedding is not meaning itself, but a learned vector representation  
> retrieved results are relevant candidates, not answer guarantees  
> if needed, the source passage should be checked again directly

This shows that RAG is not a machine that `discovers the answer`. It is a mechanism that connects candidate evidence into the LLM’s input.

## What to Remember from This Section

RAG is the structure that connects embeddings and similarity search to the generation process of the LLM. Retrieval finds external candidates, augmentation places them into input context, and generation produces an answer from that augmented input.

> embeddings turn text into vectors  
> similarity search finds nearby candidates  
> RAG attaches those candidates into the LLM’s input context  
> the LLM generates an answer from the augmented input  
> the answer still requires review

With this perspective, RAG becomes easier to understand later in P1-14 not as a single feature, but as a flow connecting data, retrieval, prompts, models, and review.

## Short Check

- I can explain RAG as a structure that combines retrieval and generation.
- I can distinguish the roles of retrieval, augmentation, and generation.
- I can explain the intuitive difference between model-internal knowledge and externally searchable material.
- I can explain that RAG does not replace prompts, but prepares context for them.
- I can explain that RAG can help with recency, evidence, and provenance.
- I can explain that RAG does not automatically guarantee fact verification or eliminate hallucinations.
- I can explain that RAG quality depends on document preparation, chunking, retrieval, prompt construction, and generation.

## When to Recall This View First

This section is useful when RAG is being understood only as `a hallucination removal feature`, and the connection structure between retrieval and generation needs to be re-established.

- when explaining that RAG is not the opposite of prompting, but a way of preparing context
- when distinguishing model-internal knowledge from outside searchable material
- when restating that review responsibility still remains even after retrieval is added

In those moments, it helps to separate:

> retrieval  
> augmentation  
> generation  
> review

That makes it easier to explain RAG not as an answer-guarantee mechanism, but as a structure that connects external evidence candidates into the LLM input.

## Sources and Further Reading

- Patrick Lewis et al., [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-06-23.
- Vladimir Karpukhin et al., [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-06-23.
- Kelvin Guu et al., [REALM: Retrieval-Augmented Language Model Pre-Training](https://arxiv.org/abs/2002.08909){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-06-23.
