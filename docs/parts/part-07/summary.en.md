# Part 7 Wrap-up. Project Review

> Section ID: `P7-summary`
> Version: `v2026.07.31`

The review plan for this summary page is to check whether `problem definition`, `comparison standard`, `evidence and execution records`, `failure records`, and `next improvement plan` remain in the actual artifact. The learning effect of Part 7 grows not when code has run once, but when records remain so the same project can be explained and improved again.

Part 7 is where earlier material is practiced through actual project execution and interpretation. The core of this Part is not completing a large service, but tying question setting, comparison, structure interpretation, execution records, and operational judgment together inside one project and becoming able to explain `why this result appeared`.

This project Part especially makes two things be checked together.

- Can you explain the concept?
- Can you confirm the concept through real input and output changes?

In other words, this Part changes the feeling of `I know it` into the state of `I ran it myself, compared it, and also read the failures`.

## Repeatable Project Record

The purpose of Part 7 is to bind the concepts learned across the whole book into actual project execution and review results so that the next stage of learning becomes repeatable by the learner alone.

- Question setup, baselines, comparison tables, and error cases should remain together inside one document.
- Input structure, learning-result interpretation, evidence checking, and execution logs should connect as one chain of judgment.
- Deployment and operational judgment should also remain as project records rather than being treated as an appendix at the end.

## Explanation Ability to Keep

After finishing this Part, you should be able to explain the flow of leaving a problem definition, a baseline, a result, a failure record, and the next improvement plan behind as actual execution and comparison results.

## Core Structure Covered in This Part

The overall structure of Part 7 is organized around `which judgment elements must remain together inside one project`.

| Structure to read together | Why it should stay one bundle |
| --- | --- |
| Question, sample unit, baseline, and comparison experiments | Because what was compared and why it counts as improvement must settle in one place. |
| Input structure, learning curves, and error cases | Because the reason for a structural choice and the reason for failure belong to the same interpretation bundle. |
| Retrieval evidence, execution logs, and approval policy | Because RAG and AI agent quality appears only when the answer, evidence, and execution path are read together. |
| Deployment, logs, failure response, and retrospective documents | Because operational records are not an appendix outside the project interpretation but part of its judgment standard. |

If this flow is regrouped by the standard of `execution and review`, it becomes the following.

| Project axis | Core execution and review element that must remain | Why this element is needed |
| --- | --- | --- |
| Analysis start | Input-unit definition, summary table, comparison table | The next exploration continues only when what counted as one unit and what difference was read are both left behind. |
| Baseline comparison | Execution summary, sample-by-sample comparison table, list of wrong cases | Improvement can be interpreted only when execution results and wrong cases remain together. |
| Structure choice and learning review | Learning curves, evaluation records, error samples | Because you must reread why this structure shook, not only read a score table. |
| RAG | Retrieval records, selection grounds, evidence-answer records | Because retrieval evidence and the connection method must be checked before the answer itself. |
| Agent | Plan list, execution records, approval state, blocked state | Because blocked points can be traced only when the plan and the real execution path are separated. |
| Deployment and operations | Incident records, status checks, improvement plans | Because operational review accumulates only when failures remain and the next action is separated. |

If this table is reduced again to the smallest level, the records that must not disappear first in each axis are the following.

| Project axis | Execution evidence that must not disappear first |
| --- | --- |
| Analysis start | One question sentence and input-unit definition |
| Baseline comparison | The simplest baseline result |
| Structure choice and learning review | Representative error samples and learning or evaluation records |
| RAG | Evidence documents and answer state |
| Agent | Tool order and approval state |
| Deployment and operations | Failure category and next action |

Even if project themes differ, the questions that must remain are the same.

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
| Data | Comparison and interpretation require a clear input, output, and split standard. |
| Evaluation | Project results should be read through both numbers and cases. |
| Retrospective | Leaving behind failure, omission, and ambiguity is core to project documents. |
| Reproducibility | Input, code, and output records are needed so the project can be run again. |
| Service perspective | In LLM projects, not only answer quality but also retrieval failure, permissions, latency, and logs must be examined together. |

If this perspective is turned one step more practical, there are many times when `what input was used, what comparison was made, and where the failure happened` matters more than `the final score number`.

- In a baseline-comparison project, not only `accuracy` but also `what samples were wrong` must remain. That is, records such as a wrong-case list are needed so that the next comparison stays alive.
- In a text project, not only `correct` or `incorrect` but also token lists, token coverage, and out-of-vocabulary tokens must remain. You must see what input was split and what word was missed to find preprocessing problems again.
- In a RAG project, not only the `answer` but also retrieval candidates, answer state, and selected evidence documents must remain. The starting point of quality review is not the answer itself but the evidence-selection process.
- In an AI agent project, not only `success` or `failure` but also permissions, approval state, and next actions must remain. You must know what approvals and blocks existed to redesign the execution path.
- In a deployment project, not only `deployment completed` but also incident records, priority, and next actions must remain. In operational records, the next-action order matters more than the declaration of completion.

These example axes are already sufficiently recovered across Part 7 itself. What matters more is that the main-text examples of each section directly show the flow `question -> execution -> comparison -> interpretation -> retrospective`.

## Easy Misunderstanding Points

The misunderstandings that need special caution in this Part are the following.

- It is easy to think a project only needs to leave behind `successful cases`.
- It is easy to misunderstand that one high result number means the project ended well.
- Running an example once does not mean the real structure has already been understood.
- Code having executed and the problem definition being sound are not the same thing.
- In an LLM project, a few good-looking answers do not mean evaluation is finished.
- If operational failures are not recorded, the next improvement becomes difficult.

In other words, a project should not be a document that proves only `it worked once`, but a document that proves `the next iteration is possible`.

## Project Review Execution Boundaries

Part 7 focused on explaining the entry-level structure of projects. Therefore, it covers goal setting, implementation, evaluation, retrospective, and operational records, but it does not finish the entire structure of large-scale infrastructure and long-term operation here.

## Expansion Tasks This Part Does Not Settle Directly

Part 7 does not settle the following tasks directly.

- What topic should be expanded into the next actual project?
- How should evaluation and failure records grow into team-level documents?
- To what point should operations and deployment be automated, and where should human review remain?

In other words, Part 7 corresponds less to the destination of the book than to the starting point of later self-directed projects.

These questions were already previewed in small form inside Part 7 itself.

- Baseline comparison can grow into a larger experiment-tracking system.
- Token-coverage and OOV records can lead into more precise tokenizer experiments.
- The recording of evidence-shortage states in RAG can grow into a stricter evaluation pipeline.
- Agent records about operational deferral and approval-required tools can expand into real operational policy documents.
- Deployment failure records become the seeds of team-level incident-retrospective documents.

## Questions Before the Next Learning Stage

- Can you explain the problem definition and the output standard of each project in one sentence?
- Did you separate and record the baseline and the improvement?
- Can the data-preparation and split process be executed again?
- Did you read the result through numbers, comparison tables, and cases together?
- Did you leave behind failure cases and an improvement plan?
- If it is an LLM project, did you also inspect retrieval, tool calls, permissions, logs, and failure handling?

When the project documents are checked again in practice, the following artifact checks should also be confirmed.

- Is there an execution summary or a review summary?
- Do sample-level records remain, such as comparison tables, test records, and evaluation records?
- Do evidence records remain, such as selection grounds and retrieval candidates?
- Do operational-flow records remain, such as execution records and incident records?

Read more briefly again, this check becomes the following.

| What to check first | Why it is important |
| --- | --- |
| Does the question remain? | To recover what the project was trying to verify |
| Does the baseline remain? | To recover the floor line for interpreting improvement |
| Do errors or failures remain? | To create the starting point of the next iteration |
| Do evidence and execution path remain? | To verify RAG and AI agent results again |
| Does the next action remain? | To prevent the retrospective from ending as a memo |

## Minimum Procedure in Project Documents

The practice repeated in Part 7 tends to reappear in nearly the same minimum procedure in the next real project as well.

1. Write the question in one sentence.
2. Fix the input file or the input unit first.
3. Run the baseline first.
4. Compare the improvement or the follow-up structure on the same input.
5. Check what remains among the execution summary, comparison table, error cases, and failure records.
6. Leave a retrospective in the form `fact -> interpretation -> next question` or `failure category -> next action`.

Even these six lines recover most of the core of Part 7.

Linked back to representative places in Part 7, the same procedure can be read as follows.

| Execution stage | Representative Section |
| --- | --- |
| Fix the question and input unit | `P7-1.1` |
| Read the baseline and comparison table together | `P7-1.2`, `P7-2.2` |
| Interpret structure and failure causes together | `P7-3.2`, `P7-4.2` |
| Leave evidence and execution logs together | `P7-5.2`, `P7-6.2` |
| Return operational failure to the next experiment | `P7-7.2` |

In other words, the current blocked stage can be compared directly with the representative section that plays the same role. If the practice sections are included as well, it becomes possible to return not only to rereading explanations, but to changing values and rewriting results.

## Wrapping Up

The purpose of the project Part is not to produce a massive artifact. Instead, it is to reveal through actual execution and comparison `what I understood and what is still unstable`.

After this Part, the reader should be able to design the next step independently.

- Expand to a larger dataset
- Attach more appropriate evaluation metrics
- Run comparison experiments on RAG quality
- Refine AI agent permissions and log policies more precisely
- Separate operational cost and failure response into independent documents

In other words, Part 7 is not the end, but the starting point of `now building projects yourself and learning again through them`.

At the shortest level, the conclusion of Part 7 can be grouped into the following sentence.

`A good project document leaves behind comparison and records that make it possible to reread why the result happened before it leaves behind code that merely ran once.`

## Recheck Standards in This Summary

When one project has finished and you start to lose track of what should have remained, it is enough to look again at whether the following standards remain as actual records.

- Implementation happened, but you are no longer sure whether the question, baseline, and failure records remained together
- You want to regroup again the shared record elements across RAG, AI agent, and deployment projects
- Before moving to the next real project, you want to organize what kind of retrospective sentence should remain

At that point, before scattering again into detailed sections, first confirm `what was being solved`, `what was recorded`, and `what will be changed next`.

Reduced to three lines, the first standards to confirm in this summary are the following.

- Does my current project still have a one-sentence question and input unit?
- Do the baseline and the comparison result remain on the same input?
- Do error cases or failure records remain together with the next action?

## Checklist

- Can you rewrite in one line the records that should remain first in each project axis?
- Can you explain why the baseline, comparison table, and failure record are shared standards across all of Part 7?
- Can you say again why operational-perspective records are needed in RAG, AI agent, and deployment work?
- Can you organize the retrospective format that will be carried directly into the next real project?

## Sources and References

This document is an internal summary of all of Part 7. It does not directly cite external sources.
