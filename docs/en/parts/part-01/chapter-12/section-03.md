# P1-12.3 The Limits and Evaluation of Prompts

> Section ID: `P1-12.3`
> Version: `v2026.07.09`

Section 12.1 explained what prompts specify. Section 12.2 separated `instructions`, `context`, and `examples`.

One important question now remains:

> is writing a good prompt enough?

The answer here is clear:

> prompts can guide the model’s output,  
> but they do not automatically guarantee factuality, evidence, safety, or consistency

Part 1 introduces the basic distinctions among `prompt limits`, `evaluation`, `factuality`, `evidence`, `recency`, `hallucination`, and `reproducibility` here. Section 12.1 explained what prompts specify. Section 12.2 separated instruction, context, and example. This section separates one more distinction:

> writing a better input  
> and  
> reviewing a better result  
> are different kinds of work

So when dealing with prompts, it is necessary to learn not only `how to ask better`, but also `what must be reviewed afterward`.

## Scope of This Section

This section deals with the limits of prompts and the criteria for reviewing outputs. It does not explain `RAG`, `vector search`, `tool use`, `agents`, or `harnesses` in detail. Those structures return in the next chapter and later sections such as P1-13.3, P1-13.4, and P1-14.2 through P1-14.5.

These terms can all sound like similar review categories at first. A quick distinction helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| prompt limit | a problem that does not disappear automatically even if the prompt is written well | the standard that prevents overtrust in prompts |
| evaluation | the procedure for checking whether the output fits its purpose | the step of judging by criteria rather than by intuition alone |
| factuality | whether the sentence matches the real facts | a core accuracy criterion |
| evidence | whether the claim is supported by checkable sources | the criterion of verifiability |
| recency | whether the information is still current | the criterion needed for changing information |
| hallucination | plausible but wrong generation | the representative generative-AI error |
| reproducibility | whether we can later confirm what changed and what result followed | the basis for recording prompt experiments |

The minimum distinction to keep is:

- prompts are not guarantees
- evaluation is separate work
- factuality, evidence, and recency are not the same
- reproducibility requires records

This section focuses on three questions:

| Question | Focus in this section |
| --- | --- |
| what can prompts not guarantee? | factuality, evidence, recency, safety, consistency |
| why is evaluation needed? | because plausible output can still be wrong |
| by what criteria should results be reviewed? | purpose fit, evidence, reproducibility, risk, revisability |

This section also does not expand the list of prompt-writing tricks. Its focus is narrower:

> why are prompts not enough by themselves,  
> and why do later structures such as RAG, tool use, agents, and harnesses become necessary?

## Goal of This Section

- Explain that prompts can guide results but do not guarantee them.
- Distinguish factuality, evidence, safety, and consistency.
- Shift output review away from `do I like this?` and toward `does this fit the purpose?`
- Organize the minimum evaluation criteria needed when writing a learning-oriented book.
- Preview why RAG, tool use, agents, and harnesses become the next topic.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| changing the prompt does not erase model limits | This helps separate input design from model capability. | It is enough to understand that better wording does not remove every type of error. |
| prompt results should be compared by evaluation criteria | This prevents us from stopping at `it looks good`. | It is enough to know that accuracy, consistency, and evidence should be checked together. |
| prompt revisions without records are hard to reproduce | This connects naturally to later harness, evaluation, and experiment-recording flows. | It is enough to understand that we should keep track of what changed and what happened. |

## A Prompt Is a Condition, Not a Guarantee

A clearer prompt can increase the chance of getting a better output. But a prompt is not a warranty card.

> good prompt:  
> write only claims that are supported by verified evidence  
> if the evidence is weak, mark it as `needs verification`
>
> possible problem:  
> the model may still write as if evidence exists even when it has not actually checked any source

This does not happen only because the prompt is bad. LLMs generate plausible output from the input context. Whether that output actually matches the real world still requires separate review.

That is why this book keeps the following rule:

> a prompt sets request conditions  
> evidence review is a separate task done by people and tools  
> the output is a draft, and factual claims remain subject to verification

## Factuality, Evidence, and Recency Are Different

The first important split in evaluating prompt results is among `factuality`, `evidence`, and `recency`.

| Criterion | Question | Example |
| --- | --- | --- |
| factuality | does the sentence match reality? | paper year, concept definition, event description |
| evidence | is there a source that supports the sentence? | paper, official document, standard, reliable reporting |
| recency | is the information still current now? | product feature, price, policy, law, model specification |

These are related, but they are not the same thing.

> something may be true but have no cited source  
> something may have a source but be outdated  
> something may be recent but come from a weak source

For example, `GPT-family models are Transformer-based` is a historical and structural statement. By contrast, `which API model is currently cheapest` can change with pricing and product policy. They require different review methods.

The working rule here is:

- stable concepts should be checked first against textbooks, papers, and official documentation
- changing information should be rechecked against dated official or otherwise reliable current material

## Hallucination Is a Plausible Error

In the context of generative AI, `hallucination` refers to output that is plausible but wrong. The NIST Generative AI Profile explains `confabulation` as the generation of content that is confidently presented but incorrect or false, and notes that this is also called hallucination or fabrication.

The important point here is not to treat hallucination as a rare exception where the model `misbehaves strangely`. LLMs are good at generating contextually fitting language, but that does not automatically guarantee that the language is factually grounded.

> risky prompt:  
> write this claim so it sounds persuasive
>
> safer prompt:  
> review this claim  
> separate what is supported from what needs verification  
> do not state unsupported content as fact

The second prompt is safer, but it is still not sufficient by itself. The actual sources must still be opened, and the sentence must still be checked against those sources.

## Consistency Is Hard to Judge from One Answer

LLM outputs can change depending on the input, model, settings, and conversation history. Even the same request repeated later can yield different wording or slightly different judgments.

So `evaluation` is not the same thing as getting one answer that looks nice.

> one output:  
> it looks readable
>
> evaluation:  
> does the model keep the same standard across similar inputs?  
> does it distinguish between wrong claims and unknown claims?  
> does it stay within section boundaries?  
> do the cited sources actually support the claims?

For a learning-oriented manuscript, `section boundaries` matter especially. If 12.3 starts explaining the detailed structure of RAG at length, it intrudes into the domain of P1-13. Even an output that looks good should be revised if it no longer answers the current section’s central question.

## Evaluation Must Fit the Purpose

Evaluation criteria depend on the purpose of the task. It is difficult to reduce every output to one single score.

| Task | Important evaluation criteria |
| --- | --- |
| concept explanation | accuracy, simple wording, bilingual terminology, no exaggeration |
| evidence review | source reliability, match between claim and source, access date |
| table-of-contents design | section boundaries, learning order, duplication |
| example writing | beginner readability, risk of misunderstanding, reusability |
| forecasting | dated evidence, comparison of viewpoints, separation of fact and speculation |

The InstructGPT paper by Ouyang and colleagues uses human evaluation along with multiple criteria such as helpfulness, truthfulness, and harmlessness. This book does not need to replicate that exact procedure, but it is still useful as a reminder:

> LLM output evaluation does not end with one criterion

For this project, the following review table is practical:

| Review item | Question |
| --- | --- |
| fit to purpose | does this output answer the current section question? |
| factuality | are there errors in the main factual claims? |
| evidence | do important claims have sources? |
| terminology | are core terms used clearly and, where needed, with Korean-English pairing? |
| boundary | does the output avoid prematurely invading another section or chapter? |
| risk | does it avoid making unsupported legal, copyright, security, or safety conclusions? |

## Risks That Prompts Can Reduce and Risks They Cannot

Prompts can reduce some kinds of risk.

> risks that prompts can help reduce:  
> - messy output format  
> - mismatch with the target reader level  
> - crossing section boundaries  
> - failing to distinguish unsupported content

But some problems remain difficult to solve with prompting alone.

> risks that prompting alone struggles to solve:  
> - factual claims whose original sources were never actually checked  
> - changes in current policy or pricing  
> - copyright questions that require legal judgment  
> - maintaining consistency across a long document  
> - mismatches between tool results and written explanation

Those problems require the next layer of structure:

| Need | Topic that follows later |
| --- | --- |
| bring external material into the response | RAG, vector search |
| verify calculations or files | tool use |
| manage multi-step work | agents |
| repeat evaluation and track logs | harnesses |

This is only a preview. The core of 12.3 is not to explain those structures in detail, but to clarify why they become necessary.

## The Minimum Review Procedure for This Book

When writing a learning-oriented manuscript with AI tools, the minimum procedure should look like this:

> 1. confirm the central question of the section  
> 2. check whether the draft actually answers that question  
> 3. separate factual claims from personal interpretation  
> 4. check whether factual claims have sources  
> 5. check whether the sources actually support the written claims  
> 6. check whether later sections are being explained too early  
> 7. record unresolved items as `needs verification`

This is not full quality assurance. But it reduces one of the biggest risks in an introductory book:

> unsupported explanation hardens into polished prose and starts to look trustworthy

## What to Remember from This Section

Prompts are tools for organizing output conditions. `Evaluation` is separate work that checks whether the result fits its purpose, has support, and does not create unnecessary risk.

> prompts clarify the request  
> evaluation reviews the result  
> evidence review checks factual claims  
> human judgment carries the final responsibility

This also summarizes the whole flow of Chapter 12:

> 12.1 what does a prompt specify?  
> 12.2 how do instruction, context, and example work differently?  
> 12.3 what can prompts not guarantee, and what must still be evaluated?

From here, the discussion moves to how LLMs meet external material. That begins with embeddings, vector search, and RAG.

## Checklist

- I can explain that prompts specify output conditions but do not guarantee factuality.
- I can distinguish factuality, evidence, and recency.
- I can explain hallucination as a plausible error.
- I can explain that evaluation is not the same as picking one answer that looks good.
- I can explain that evaluation criteria depend on the purpose of the task.
- I can distinguish risks that prompting can reduce from risks it cannot easily solve.
- I can explain why RAG, tool use, agents, and harnesses become the next topic.

## When to Recall This View First

This section is useful when it starts to feel as if fixing the prompt a little more will solve everything, and evaluation and review need to be re-established as separate work.

- when factuality, evidence, and recency need to be checked separately even if the output looks plausible
- when prompt revision and model limits are being mixed together
- when explaining why later structures such as RAG, tool use, agents, and harnesses are needed

In those moments, it helps to separate:

> input conditions  
> output evaluation  
> evidence checking  
> reproducibility records

That makes it easier to say both of the following at once:

- prompt improvement matters
- prompt improvement alone is not enough

## Sources and Further Reading

- Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, accessed 2026-06-23.
- Pranab Sahoo et al., [A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications](https://arxiv.org/abs/2402.07927){: target="_blank" rel="noopener noreferrer" }, arXiv, 2024, accessed 2026-06-23.
- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://doi.org/10.6028/NIST.AI.600-1){: target="_blank" rel="noopener noreferrer" }, NIST AI 600-1, 2024, accessed 2026-06-23.
- OpenAI, [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering){: target="_blank" rel="noopener noreferrer" }, OpenAI API documentation, accessed 2026-06-23.
