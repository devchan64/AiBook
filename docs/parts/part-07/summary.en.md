# Part 7 Wrap-up. Project Review

> Section ID: `P7-summary`
> Version: `v2026.07.12`

Part 7 is the section where the concepts restored and organized through the earlier six Parts are checked again as `small artifacts`. The core of this Part is not completing a large service, but directly walking once through the shared flow of problem definition, data preparation, implementation, evaluation, and review.

This project Part makes two things be checked together in particular.

- Can you explain the concept?
- Can you confirm the concept again through small code and results?

In other words, this Part changes the feeling of `I know it` into the state of `I tried it and left a record`.

## The Purpose Of This Part

The purpose of Part 7 is to regroup the concepts learned across the whole book into small project documents and execution results, so that the next stage of learning becomes repeatable by the learner alone.

When reopening Part 7, the quickest route is to grab the representative Sections as handles. The start of analysis is `P7-1.1`, the review structure of `fact -> interpretation -> next question` is `P7-1.2`, baseline comparison is `P7-2.2`, text-evaluation records are `P7-4.2`, RAG verification is `P7-5.2`, agent permissions and logs are `P7-6.2`, and deployment-failure review is `P7-7.2`.

## The Goals Of This Part

After finishing this Part, you should be able to explain the flow of leaving behind a problem definition, a baseline, a result, a failure record, and the next improvement plan as small artifacts.

## The Core Flow Covered In This Part

The overall flow of Part 7 can be organized as follows.

1. Read small data and summarize the question and the exploration result.
2. Compare a baseline model and an improved model.
3. Compress deep-learning and text-classification flows into small examples.
4. Connect RAG and agent structures into small service projects.
5. Leave behind deployment, logs, failure response, and review documents.

If this flow is regrouped from the standpoint of `artifacts`, it becomes the following.

| Project axis | The core record that must remain | Why this record is needed |
| --- | --- | --- |
| Analysis start | Project notes, review notes | The next exploration continues only when what was being examined and what will be checked again are both left behind. |
| Baseline comparison | Execution summaries, sample-by-sample comparison tables, lists of wrong cases | Improvement can be interpreted only when execution results and wrong cases are left together. |
| Image/text classification | Test records, evaluation records, error-sample IDs | It is necessary to reread sample-level judgment grounds, not only a score table. |
| RAG | Retrieval records, selection grounds, evidence-answer records | Retrieval grounds and connection method must be checked before the answer itself. |
| Agent | Plan lists, execution records, review summaries | Blocked points can be traced only when the plan and the actual execution path are seen separately. |
| Deployment and operations | Failure records, improvement plans | Operational review accumulates only when failures are left behind and next actions are separated. |

If this table is reduced again to the smallest level, the records that must not disappear first on each axis are the following.

| Project axis | The record that must not disappear first |
| --- | --- |
| Analysis start | One question sentence and observation notes |
| Baseline comparison | The simplest baseline result |
| Image/text classification | Representative error samples and evaluation records |
| RAG | Evidence documents and answer state |
| Agent | Tool order and approval state |
| Deployment and operations | Failure category and next action |

Even though each project has a different theme, the questions that must remain are the same.

1. What is being solved?
2. What are the inputs and outputs?
3. How was the data prepared?
4. What is the baseline?
5. How was the result checked?
6. What were the failures and limits?
7. Where should the next improvement start?

## Concepts That Must Be Remembered

The perspectives that must be carried out of Part 7 are the following.

| Distinction | Perspective to remember |
| --- | --- |
| Problem definition | A project should make the question explicit before implementation. |
| Baseline | Without a baseline, even the claim that something improved becomes weak. |
| Data | Even with toy data, the input, output, and split standard must be explicit. |
| Evaluation | Project results should be read through both numbers and cases. |
| Review | Leaving behind failure, omission, and ambiguity is core to project documents. |
| Reproducibility | Input, code, and output records are needed so the project can be run again. |
| Service perspective | In LLM projects, not only answer quality but also retrieval failure, permissions, latency, and logs must be examined together. |

If this perspective is turned one step more practical, there are many times when `what records were left behind` matters more than `the final result number`.

- In a baseline-comparison project, not only `accuracy` but also `what samples were wrong` must remain. That is, records such as a list of wrong cases are needed so that the next comparison stays alive.
- In a text project, not only `right/wrong` but also token lists, token coverage, and out-of-vocabulary tokens must remain. You must see what input was split and what words were missed to find preprocessing problems again.
- In a RAG project, not only the `answer` but also retrieval candidates, answer state, and selected evidence documents must remain. The quality review begins from the evidence-selection process, not from the answer itself.
- In an agent project, not only `success/failure` but also permissions, approval status, and next actions must remain. You must know what approvals and blocks existed to redesign the execution path.
- In a deployment project, not only `deployment completed` but also failure records, priorities, and next actions must remain. In operations, the order of the next action matters more than the declaration of completion.

Because these example axes are already sufficiently recovered in distributed form within Part 7, the current edition does not need additional project `supplementary study` sections. Instead, it is more important that the main-text examples of each section directly show the flow of `question -> record -> review`.

## Points That Are Easy To Misunderstand

The misunderstandings that need special caution in this Part are the following.

- It is easy to think a project only needs to leave behind `successful cases`.
- It is easy to misunderstand that one high number means the project ended well.
- Building a small example does not mean you immediately understood a production-style service structure.
- Code having executed and the problem definition being sound are not the same thing.
- In an LLM project, a few good-looking answers do not mean evaluation is finished.
- If operational failures are not recorded, the next improvement becomes difficult.

In other words, a project document should not prove only `it worked once`, but `the next iteration is possible`.

## What This Part Explains And Does Not Explain

Part 7 focused on explaining the entry-level structure of projects. Therefore, it covers small goal-setting, implementation, evaluation, review, and operational records, but it does not finish the entire structure of large-scale infrastructure and long-term operation here.

## Questions This Part Does Not Close

Part 7 passes the following questions to the reader's later real projects.

- What topic will be expanded into the next actual project?
- How will evaluation and failure records be grown into team-level documents?
- To what point will operations and deployment be automated, and where will human review remain?

In other words, Part 7 is less the destination of the book than the starting point of later self-directed projects.

These questions were already previewed in small form inside Part 7 itself.

- Baseline comparison can grow into a larger experiment-tracking system.
- Token coverage and OOV records can lead into more precise tokenizer experiments.
- The recording of evidence-shortage states in RAG can grow into a stricter evaluation pipeline.
- Agent records about operational deferral and approval-required tools can expand into actual operational policy documents.
- Deployment failure records become the seeds of team-level incident review documents.

## Questions To Check Before Moving To The Next Stage Of Learning

- Can you explain the problem definition and output standard of each project in one sentence?
- Did you separate and record the baseline and the improvement?
- Can the data preparation and splitting process be executed again?
- Did you read the result through both numbers and cases?
- Did you leave behind failure cases and an improvement plan?
- If it is an LLM project, did you also check retrieval, tool calls, permissions, logs, and failure handling?

When actually opening the project documents again, the following artifact checks should also be confirmed.

- Is there an execution summary or a review summary?
- Are there sample-level records such as comparison tables, test logs, or evaluation records?
- Are there evidence records such as selection grounds or retrieval candidates?
- Is there an operational flow such as execution records and failure records?

If this check is reduced more briefly again, it becomes the following.

| What to check first | Why it is important |
| --- | --- |
| Does the question remain? | To recover what the project was trying to verify |
| Does the baseline remain? | To recover the floor line for interpreting improvement |
| Do error or failure remain? | To create the starting point of the next iteration |
| Do evidence and execution path remain? | To verify RAG/agent results again |
| Does the next action remain? | To prevent the review from ending as a memo |

## Closing Part 7

The purpose of the project Part is not to produce a massive artifact. Rather, it is to reveal through a small artifact `what I understood and what is still unstable`.

After this Part, the reader should be able to design the next steps independently.

- Expand to a larger dataset
- Attach more appropriate evaluation metrics
- Run comparison experiments on RAG quality
- Refine agent permissions and log policies more precisely
- Separate operating cost and failure response into independent documents

In other words, Part 7 is not the end, but the starting point of `now building projects yourself and learning again through them`.

At the shortest level, the conclusion of Part 7 can be grouped into the following one sentence.

`A good project document leaves behind records that can be reread and rerun before it leaves behind the model or the code itself.`

## When To Open The Part 7 Summary Again

It is useful to open this summary page again when one project has been finished, but you want to compress once more what should have remained, such as:

- when implementation happened, but you are not sure whether the question, baseline, and failure records remained together
- when you want to regroup again what the shared record elements were across RAG, agent, and deployment projects
- when you want to organize what kind of review sentence should remain before moving to the next real project

At that point, before scattering again into the detailed sections, it is better to come back to this summary page and first confirm `what was being solved`, `what was recorded`, and `what will be changed next`.

## Checklist

- Can you rewrite once more in one line the records that must remain first on each project axis?
- Can you explain why baselines and failure records are the shared standards of all Part 7 work?
- Can you say again why operational-perspective records are needed in RAG, agent, and deployment work?
- Can you organize the review format that will be carried immediately into the next actual project?

## Sources And References

This document is an internal summary of all of Part 7. It does not directly cite external sources.
