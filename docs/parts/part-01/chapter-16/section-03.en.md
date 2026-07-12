# P1-16.3 How to Validate with a Project

> Section ID: `P1-16.3`
> Version: `v2026.07.12`

P1-16.2 looked at work automation and search from the viewpoint of workflow. This section organizes how to validate learning and practical use through a small `project`.

It is easy to feel that AI has been understood. But whether it has actually been understood becomes much clearer only after making a small deliverable.

This section summarizes how to turn the earlier flows of learning documentation and work automation into a `small, testable project` through `project`, `success criteria`, `evaluation`, `record`, and `failure type`.

## Scope of This Section

This section focuses on how to design and validate a small project after finishing Part 1. Specific algorithm implementation and large-scale service development are left to later parts.

| Topic | Question in this section |
| --- | --- |
| project scope | how should a goal that is too large be reduced? |
| success criteria | what conditions count as success? |
| evaluation | how should correctness be checked? |
| record | how should failures and revisions be preserved? |

## Goal of This Section

- Explain why a small project should begin from one concrete question.
- Explain the habit of writing down success criteria and evaluation criteria first.
- Explain why failure records become learning material in project retrospection.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| a small project should start from one question rather than from a technology name | This reduces the mistake of making the starting scope too large. | It is enough to understand that "can I find relevant sections in my document set?" is safer than "let's build RAG." |
| success criteria should be written first | This keeps evaluation from remaining only a feeling. | It is enough to understand that the threshold for success and the meaning of failure should be set before building. |
| failure records become learning material | This prevents the project from being seen only as a simple success or failure. | It is enough to understand that repeated failure types should be named and preserved. |

## A Small Project Starts from One Question

A good beginner project does not begin with the name of a technology. It begins with one question.

> weak start:  
> let's build RAG
>
> better start:  
> can the system find a relevant section inside the set of learning documents I wrote?

When the question is concrete, the required technology also becomes narrower naturally.

| Question | Likely components |
| --- | --- |
| can it find a relevant section in my documents? | embeddings, vector search |
| can it answer with retrieved evidence? | RAG, source citation |
| can answer errors be reduced? | evaluation questions, original-source checking |
| can repeated writing steps be reduced? | templates, automation scripts |

## Write the Success Criteria First

One common reason projects fail is that no real `success criteria` were defined.

> goal:  
> build document-based question answering
>
> weak success criterion:  
> it answers well
>
> better success criterion:  
> on at least 16 of 20 questions, it includes a relevant section link  
> it does not produce unsupported assertive claims  
> when asked about missing content, it says it does not know

Success criteria in an AI project should include more than raw accuracy. They should also consider grounding, security, cost, latency, and whether a person can review the result.

## Failure Records Become Learning Material

Failure happens often in AI projects. The important point is not hiding failure, but turning it into categories.

| Failure type | What to record |
| --- | --- |
| retrieval failure | why the relevant document was not found |
| hallucination | where nonexistent content was invented |
| missing grounding | where an unsupported claim appeared |
| permission problem | where disallowed material was mixed in |
| cost problem | call count, token use, latency |

Failure records then become requirements for the next improvement cycle.

> record the failure  
> classify repeated failures  
> adjust the validation standard  
> make a small fix and test again

## Checklist

- You can explain why an AI project should start from a central question rather than from a technology name.
- You can explain why success criteria should be written first.
- You can include grounding, cost, latency, and security conditions in evaluation.
- You can explain why failure records become the next requirements.
- You can explain an AI project as a testable learning unit by separating `central question`, `success criteria`, `evaluation method`, and `failure record`.

## Sources and Further Reading

- NIST, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- OWASP, [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- U.S. Department of Education, [Artificial Intelligence and the Future of Teaching and Learning](https://www.ed.gov/sites/ed/files/documents/ai-report/ai-report.pdf){: target="_blank" rel="noopener noreferrer" }, 2023, accessed 2026-06-23.
