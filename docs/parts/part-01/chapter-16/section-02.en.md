# P1-16.2 Work Automation and Search

> Section ID: `P1-16.2`
> Version: `v2026.07.19`

P1-16.1 treated an AI relearning documentation project as a case of personal learning and documentation. This section widens the view toward workplace use.

When AI is applied in real work, one of the first things people imagine is `work automation` and `search`. But the useful question is not "AI will do it all by itself." The better question is:

> which parts of a human workflow can be delegated, and which parts should remain under human responsibility?

This section organizes where AI can be used as a support tool inside work flow through `work automation`, `search`, `summary`, `review`, and `productivity`.

This section focuses on how AI can be used as a support tool in repetitive work and document search. Project-based validation is covered in P1-16.3.

| Topic | Question in this section |
| --- | --- |
| automation | which repeated steps can be delegated? |
| search | how should needed evidence be found inside many documents? |
| summary | what may be lost when long material is compressed? |
| review | how should a person check the AI result? |

## Goal of This Section

- Explain work automation through step decomposition rather than as replacement of the whole job.
- Explain why search results should be read as `evidence candidates`, not as final answers.
- Explain why productivity must include review cost.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| automation means dividing a workflow into stages, not replacing the whole job | This makes the realistic scope of AI use easier to see. | It is enough to understand that classification, drafting, and retrieval can be separated as different kinds of delegation. |
| search results are evidence candidates rather than the answer itself | This prevents overconfidence in RAG and vector retrieval. | It is enough to understand that people still need to check the original material. |
| productivity has to include review cost | This separates "fast" from "actually usable." | It is enough to understand that a fast draft may still lower overall productivity if revision cost is high. |

## Automation Means Dividing the Workflow into Stages

In workplace automation, the important first step is dividing the work into smaller stages.

> collect materials  
> -> classify  
> -> draft  
> -> check evidence  
> -> revise  
> -> approve  
> -> publish

AI does not perform every stage equally well. It may help find candidates or generate first drafts, but legal judgment, security approval, and final accountability should remain with people and organizational process.

| Workflow stage | Where AI may help | Caution |
| --- | --- | --- |
| document classification | useful if the criteria repeat clearly | a person still has to define the labeling standard |
| summary | useful for scanning long documents quickly | important exceptions and evidence may disappear |
| draft writing | useful for repeated formats | factual errors and exaggerated language still need review |
| retrieval support | useful for finding related documents | retrieval output is not the final answer |
| final approval | should not be delegated to AI | responsibility should remain with a person |

## Search Narrows Evidence Candidates Rather Than Finding the Answer

After learning RAG and vector search, it can feel as if AI is now able to "find the answer" in documents. In real work, however, retrieval output should be treated as an `evidence candidate`, not as the answer itself.

> weak usage:  
> AI summarized it, so it must be true
>
> better usage:  
> AI found candidate documents  
> a person opens the original and checks whether the actual claim matches

Search-based AI becomes more useful as document volume grows, but it still carries risks:

| Risk | Description |
| --- | --- |
| stale documents | the result may differ from current policy or pricing |
| permission issues | documents the user should not see may be retrieved |
| context loss | only part of a document may be retrieved, leaving out limiting conditions |
| source confusion | the answer may mix claims from several documents |

## Productivity Has to Include Review Cost

AI tools can produce first drafts quickly. But faster drafting does not automatically mean the whole job became faster.

> time saved:  
> first-draft writing time
>
> time added:  
> evidence review  
> security review  
> wording revision  
> approval by the responsible person  
> error correction

The productivity of AI use should not be judged only by generation speed. It also has to consider `review cost`, `failure cost`, and `operational cost`.

## Checklist

- You can explain work automation through workflow decomposition rather than total replacement.
- You can explain why search and RAG results should be treated as evidence candidates.
- You can explain why summary cannot replace checking the original.
- You can evaluate AI productivity by looking at both draft speed and review cost.
- You can explain workplace AI use by separating `workflow-stage decomposition`, `evidence-candidate search`, `original-source review`, and `review cost`.

## Sources and Further Reading

- NIST, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19.
- U.S. Department of Education, [Artificial Intelligence and the Future of Teaching and Learning](https://www.ed.gov/sites/ed/files/documents/ai-report/ai-report.pdf){: target="_blank" rel="noopener noreferrer" }, 2023, accessed 2026-07-19.
- World Economic Forum, [The Future of Jobs Report 2025](https://www.weforum.org/publications/the-future-of-jobs-report-2025/){: target="_blank" rel="noopener noreferrer" }, 2025-01-07, accessed 2026-07-19.
