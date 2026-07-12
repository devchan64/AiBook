# Part 7. Projects

> Section ID: `P7-index`
> Version: `v2026.07.12`

Part 7 is the section where the concepts organized earlier are checked again as `small project documents`. Here, rather than stretching out more new theory, the point is to confirm how concepts already learned reappear inside actual project organization.

This Part matters especially for the following readers.

- Readers who can read AI explanations but have not yet left behind even a small result of their own
- Readers who followed example code but still find it unclear `why a project should be organized in this order`
- Readers who have heard about LLMs, RAG, and agents but want to organize what must actually be recorded and verified

## The Purpose Of This Part

The purpose of Part 7 is not to complete a massive service. Instead, it makes the following smaller goals explicit.

- Write the question in one sentence
- State the data or input clearly
- Set a baseline
- Leave behind code and output results
- Organize failure and limits into a review document
- If needed, also organize execution records, evaluation notes, and operational logs

In other words, the core of Part 7 is `leaving what you understood behind again in executable form`.

What matters here is not to let the phrase `I did a project` be replaced by a single code file. In Part 7, the following kinds of records should be organized together inside the actual project document whenever possible.

| Record type | Why it is needed |
| --- | --- |
| Project notes and review notes | They are needed to leave behind what was being checked and what is still unstable. |
| Execution results and comparison tables | They are needed to compare the baseline and the improved result on the same scale. |
| Test records and evaluation records | They are needed to reread sample-level errors and evaluation grounds. |
| Retrieval evidence and selection grounds | They are needed to verify what evidence was used before the answer itself. |
| Execution logs and review summaries | They are needed to trace what order the agent moved through and where it stopped. |
| Failure records and improvement plans | They are needed to leave behind post-deployment failures and next actions separately. |

In other words, Part 7 asks more strictly not `did you build the model`, but `what will you record and pass to the next iteration`.

## The Goals Of This Part

- Where should a project start?
- Can a small data-analysis task also be called a project?
- How should baselines and improvements be compared?
- What minimum units should be confirmed in deep-learning and text-classification projects?
- In RAG and agent projects, what should be treated as quality standards?
- In deployment and operations, what kinds of failure records are needed?

If these goals are moved into the standard of actual project documents, they become the following.

| Project stage | Minimum document element |
| --- | --- |
| Question setup | One-sentence goal, standards to check |
| Input organization | Data, documents, tools, constraints |
| Baseline | The simplest comparison standard and its result |
| Execution | Code, output, intermediate observations |
| Evaluation | Automatic checks, human review, comparison notes |
| Operational review | Failure records, next improvement order |

If these minimum document elements are rewritten again as the actual project axes of Part 7, they can be read as follows.

| Project axis | Representative artifact example | What to grasp when seeing this name for the first time |
| --- | --- | --- |
| Analysis start | Project note, review note | The note explaining why the project started and the review note left after it ended |
| Baseline comparison | Execution result, baseline error-case list | The result of one run and the list of cases the baseline frequently got wrong |
| Image/text classification | Test record, evaluation grounds | Sample-level test records and the grounds of evaluation judgment |
| RAG | Retrieval record, evidence-answer record | The record of what documents were found and on what evidence the answer was written |
| Agent | Planned steps, execution record, final summary document | The planned order, the actual execution log, and the final summary document |
| Deployment/operations | Review summary, failure record, improvement plan | The review summary, the failure record, and the next improvement order |

When writing the first project, the flow becomes much clearer even if you first leave only the following one line for each axis.

| Project axis | The minimum record to leave first | Why that one line is needed |
| --- | --- | --- |
| Analysis start | One sentence for `what is being checked` | Because a summary without a question does not lead to the next iteration |
| Baseline comparison | One line for `the simplest baseline result` | Because a floor is needed to interpret the claim that something improved |
| Image/text classification | A few `samples that were most often wrong` | Because a score table alone does not show the error structure |
| RAG | `What document was used as evidence` | Because evidence must remain before the answer to enable later verification |
| Agent | `What tools were used in what order` | Because the execution path must appear before success/failure can be interpreted |
| Deployment/operations | `What failure occurred and what will be changed next` | Because in operations, the next action matters more than the completion report |

## What This Part Explains And Does Not Explain

This Part covers the following scope.

- How to set a small project goal
- Input and output definition
- Baseline and comparison
- Result and limit recording
- The basic document structure of RAG, agent, and deployment projects

This Part does not treat the following topics in depth.

- Building large-scale training infrastructure
- Automating complex MLOps pipelines
- Deep analysis of long-term operating-cost optimization
- The entirety of production-grade security-policy design

Among these omitted items, the big picture of cost, operations, permissions, and failure response is still recovered again inside the main text through `P7-6.2` on permissions and logs, `P7-7.1` on deployment and monitoring goals, and `P7-7.2` on failure records and improvement plans. By contrast, large-scale training infrastructure and the full security design of production services remain outside the current book's entry-level project scope.

In other words, this Part covers not `the whole of real practice`, but `the minimum project intuition for crossing into practice`.

In particular, this Part keeps the following distinctions throughout.

- `Analysis project`: questions, tables, summary values, and observation notes are central
- `Model project`: baselines, prediction results, and error cases are central
- `RAG/agent project`: evidence documents, tool results, execution records, and failure logs are central

This distinction is not merely a genre classification, but also the standard for deciding what record must be organized first.

- In an analysis project, `the question and observation notes` come before summary values.
- In a model project, `comparison rows` and `error samples` come before accuracy alone.
- In a RAG project, `retrieval evidence` and `answer state` come before the answer itself.
- In an agent project, `approval status` and `next actions` come before success/failure.
- In a deployment project, `failure records` and `next actions` come before deployment completion.

Part 7 does not pull these examples back out again as separate `supplementary study`. It is a better fit for the current entry-level project flow to let the core examples of each axis be followed directly inside the main text.

## Questions This Part Does Not Close

Because Part 7 is the Part that treats the entry-level flow of projects, the following questions are passed to the reader's later real projects.

- How should team-level collaboration documents and experiment-tracking systems be designed?
- By what standards should larger datasets and longer operation logs be managed?
- To what degree should deployment automation and permission review be documented?

In other words, Part 7 is the Part that closes `the minimum structure for starting and reviewing a project`, not the Part that finishes every practical system here.

## Understanding That Should Remain After This Part

After reading Part 7, the reader should have roughly the following intuition.

- A project should define the question and the baseline before implementation.
- Even a small data analysis can be a valid project unit.
- A model result without baseline comparison and improvement comparison is weakly interpreted.
- In an LLM project, retrieval failure, tool failure, permissions, and logs must be recorded together, not just answer examples.
- A project review is not a document that hides failure, but a document that prepares the next iteration.

If these five lines are compressed at the shortest level, they become the following.

`A project is not the act of making one result, but the act of leaving records that can be used again in the next iteration.`

## The Common Format Of Project Documents

Each project in Part 7 is written, whenever possible, in the following flow.

- Problem definition
- Data or input
- Approach
- Implementation
- Result
- Limitations and improvements
- Sources and references

This format is not a mechanical template, but the minimum common structure that makes the project executable again and readable again.

In projects related to generative AI, the following items are often added.

- Evidence documents or retrieval results
- Tool-call results or execution logs
- Automatic-evaluation results
- Human-review notes
- Execution records or fallback-action records when failure occurs

When the reader checks this common format again, it is also fine to read it through the following questions.

| Document question | The record to check | Why this record is examined |
| --- | --- | --- |
| What was being attempted? | Goal sentence, planning steps, project notes | Without question and plan, only execution logs remain and the purpose disappears. |
| What was put in? | Data tables, document snippets, tool lists | If the input is missing, the same project cannot be rerun. |
| How was comparison made? | Baseline, comparison tables, evaluation records | Claims of improvement must be interpreted through the same standard. |
| What was the evidence? | Selection grounds, retrieval candidates | RAG and agent results must be verifiable again later. |
| Where did it stop? | Blocked state, evidence-shortage state, failure state | A starting point for the next iteration only appears when the failure point is left behind. |
| What will change next time? | Review summary, improvement plan | A review must lead into the next action rather than end as a memo. |

These questions can also be reduced more practically as follows.

| Project axis | What a weak record tends to omit | What a good record leaves first |
| --- | --- | --- |
| Analysis | Only the result number | Question, observation, next question |
| Model | Only accuracy | Baseline, error samples, reason for comparison |
| RAG | Only the answer | Evidence documents, answer state, missing grounds |
| Agent | Only success/failure | Tool order, approval status, blocked points |
| Deployment | Only that an incident happened | Failure category, priority, next action |

## Completion Criteria

- You can organize a small project in the flow of question, input, implementation, result, and review.
- You can explain the difference between a baseline and an improved model in document form.
- You can write quality and operational perspectives together in RAG and agent projects.
- You can leave failure records and the next improvement plan inside the project result.

At the shortest level, the completion standard of Part 7 can be grouped into the following one sentence.

`Even in a small project, you should be able to leave records that make it executable again and a review that prepares the next iteration.`

## When To Open Part 7 Again

It is useful to open Part 7 again when the conceptual content has been read, but the sense of regrouping it into the form of project artifacts has become blurry, such as:

- when result numbers are left behind, but you are no longer sure whether baselines, error cases, and review notes remained together
- when you are describing RAG or agents, but the evidence records, execution records, and permission records are not being left together
- when the standards for what to check after deployment and what to leave as failure records have started to shake

At that point, before attaching more new functionality, it is better to follow the representative Sections of Part 7 and fix again the structure of `question -> execution -> evaluation -> review`.

## Checklist

- Can you rewrite in one line the records that must be left first on each project axis?
- Can you explain why baselines and failure records are the common standards across all of Part 7?
- Can you say again why operational-perspective records are needed in RAG, agent, and deployment work?
- Can you organize the review format that will be carried directly into the next real project?

## Sources And References

This document is an internal overview that organizes the purpose and learning path of Part 7. It does not directly cite external sources.
