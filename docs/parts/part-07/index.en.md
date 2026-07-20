# Part 7. Projects

> Section ID: `P7-index`
> Version: `v2026.07.20`

Part 7 is the part where earlier material is practiced through real inputs, code execution, output comparison, and error interpretation. Instead of adding a long stretch of new theory, this Part executes and interprets already learned judgment standards around question setting, comparison, structure choice, and execution records inside one project.

This Part matters especially for the following readers.

- Readers who can follow AI explanations but have had few chances to change inputs and compare results themselves
- Readers who followed example code but still find `why this output appeared` and `what should be checked first` unclear
- Readers who know about LLMs, RAG, and agents but want a clearer way to read execution logs and quality reviews

## What A Project Must Leave As Evidence

The purpose of Part 7 is not to finish a massive service. It is also not a Part that stops at formal imitation. Instead, it makes the goal of `stabilizing understanding by actually running and rereading examples` explicit.

- Close the question in one sentence and define the input unit clearly
- Run a baseline first so there is a floor line for comparison
- Execute the code and read output tables, predictions, and error cases together
- Reinterpret results instead of leaving them at `correct` or `incorrect`
- Turn failures and limits into concrete revision items for the next experiment
- Review execution records, evaluation notes, and operational logs when they matter

In other words, the core of Part 7 is `turning understood ideas into executable practice and readable review records`.

What matters here is not replacing `I did a project` with a single code file or a short success screen. In Part 7, the following execution evidence and review records should be kept together inside the actual project document whenever possible.

| Execution and review element | Why it is needed |
| --- | --- |
| Question and input definition | They are needed to fix what is being solved and what counts as one unit before execution starts. |
| Baseline result | It is needed to create the floor line for interpreting any claim that something improved. |
| Comparison tables and error cases | They are needed to reread the failure structure that a single score cannot show. |
| Retrieval evidence and selection grounds | They are needed to verify what evidence was used before the answer itself. |
| Execution records and permission state | They are needed to trace what order the agent moved through and where it stopped. |
| Incident records and next actions | They are needed to separate post-deployment failures from the next revision step. |

In other words, Part 7 asks more strictly not `did you build a model`, but `what did you actually run, what did you verify, and what should be revised next`.

## The Integrated Practice Structure Of Part 7

Part 7 rereads one project through several judgment axes: `question`, `baseline`, `comparison`, `structure`, `evidence`, `execution records`, and `operational review`. The sections reveal, from different angles, what must remain together inside the same project document.

| Integrated practice axis | What should be read together here |
| --- | --- |
| Question and input definition | What counts as one unit, how the baseline is set, and where the first line of the retrospective changes |
| Comparison and error interpretation | How comparison tables, error cases, and the next question remain as one bundle |
| Structure and learning interpretation | How input structure, learning curves, and failure decomposition connect |
| Evidence and execution records | How retrieval evidence, tool calls, approval state, and blocked state are read together |
| Operations and iterative improvement | How deployment checks, incident records, and next actions return to the next experiment |

Once this structure is fixed first, Part 7 is organized less as `a Part with many scattered examples` and more as `a Part that rereads the same project through several judgment axes`.

| Axes that destabilize the project if missing | Why they matter |
| --- | --- |
| Question and input unit | Because later comparisons also drift if what counts as one unit is unstable. |
| Baseline and comparison table | Because claims of improvement can be interpreted only on top of an explicit comparison. |
| Execution records and failure records | Because it prevents LLM, agent, and deployment practice from ending with answer examples or success screens alone. |

## Practice Axes And Representative Sections

| Practice axis | The intuition to recover here | Representative place to run it directly in Part 7 |
| --- | --- | --- |
| Question and comparison practice | Question setup, baseline, preprocessing, comparison experiments | `P7-1.1` to `P7-2.3` |
| Structure and learning interpretation | Input-structure choice, learning-result interpretation, error reading | `P7-3.1` to `P7-4.3` |
| RAG and agent practice | Evidence, permissions, execution records | `P7-5.1` to `P7-6.3` |
| Deployment and operational checks | Deployment checks, incident records, next-action priority | `P7-7.1` to `P7-7.3` |

This mapping matters because Part 7 is not a Part that adds a long separate block of new theory. It is a Part that binds `question setup -> comparison -> structure interpretation -> execution records -> operational retrospective` into one flow. If the current problem is separated into a comparison-design issue, a structure or learning-interpretation issue, or an evidence, tool, or operational issue, the project record itself becomes much easier to narrow down.

## The Shared Elements Of Practice Records

Even if the code blocks differ by section, the execution records in Part 7 tend to preserve the same elements.

| Record element | What should remain |
| --- | --- |
| Question | Fix what the run is checking in one sentence. |
| Input | Leave which CSV, document, log, or tool state was read. |
| Execution | Leave what was actually run, such as a Python example, comparison table, retrieval step, or tool call. |
| Output | Leave the object to interpret, such as an execution summary, prediction result, error case, or failure record. |
| Interpretation | Explain what judgment the output supports. |
| Recheck | Leave the next value to change, sample to revisit, or pending/failure state to track. |

The key is not to stop at `the code ran`. Part 7 cares more about `where to read the result and what to recheck next` than execution by itself.

Reduced to the repository level, the start can be as short as the following.

```bash
.venv/bin/python
```

The CSV files and record files used by the code blocks in each section are grouped under `docs/assets/part-07/`, so even checking which file is being read first makes the practice context much clearer.

## Questions That Open The Project

- Where should a project start?
- How should a real input be cut into one sample unit?
- How should a baseline and an improvement be compared?
- What should be checked visually in a deep-learning project?
- What should count as a quality standard in RAG and agent projects?
- What kinds of failure records are needed in deployment and operations?

Moved into the standard of actual project documents, these questions become the following.

| Project stage | Minimum document element |
| --- | --- |
| Question setup | One-sentence goal, standards to check |
| Input organization | Data, documents, tools, constraints |
| Baseline | The simplest comparison standard and its result |
| Execution | Code, outputs, intermediate artifacts |
| Evaluation | Automatic checks, human review, comparison notes |
| Operational review | Failure records, next improvement order |

If these minimum elements are rewritten again as the actual project axes of Part 7, they can be read as follows.

| Project axis | Representative execution scene | What must be checked at this stage |
| --- | --- | --- |
| Analysis start | Table inspection, summary calculation, baseline comparison | How the input unit is grouped and what difference appears first |
| Baseline comparison | Baseline-model run, comparison table, error-case review | Whether the claim that something improved really holds in the comparison |
| Structure choice | Input-structure comparison, model-structure choice, learning-curve review | Why this structure was chosen and where it shakes |
| RAG | Retrieval-candidate comparison, evidence selection, answer review | Whether retrieval evidence and failure are readable before the answer |
| Agent | Plan, tool calls, approval, blocked-state review | Whether the execution path and failure-handling rules are visible |
| Deployment and operations | Deployment check, status inspection, incident review | Whether the service is actually holding and what the next action is |

Written as the first question to hold in each axis, the practice can be reduced as follows.

| Project axis | The first question to check | Why this question is needed |
| --- | --- | --- |
| Analysis start | `What was grouped as one unit?` | Because later comparisons also shake if the sample unit shakes. |
| Baseline comparison | `How far does the simplest standard work?` | Because a floor line is needed to interpret the claim that something improved. |
| Structure choice | `Why was this structure chosen for this input?` | Because the reason for the choice must appear before the model name. |
| RAG | `What document was used as evidence?` | Because evidence must remain before the answer so it can be verified again later. |
| Agent | `What tools were used in what order?` | Because the execution path must appear before success or failure is interpreted. |
| Deployment and operations | `What failure happened and what will be changed next?` | Because the next action matters more than the completion report in operations. |

## Execution Boundaries A Small Project Must Close

This Part covers the following scope.

- How to set a project goal
- Input and output definition
- Baseline and comparison
- Result and limit recording
- The basic document structure of RAG, agent, and deployment projects

This Part does not finish `the whole of practice`, but it clearly covers `the scenes that must be run and reread directly before entering practice`. The main-text axis of this Part is `question and input definition`, `baseline and comparison`, `error cases and review`, `RAG and agent execution records`, and `deployment and failure review`. The larger picture of permissions, operations, and failure response continues inside the main text through `P7-6.2` on permission and log review, `P7-7.1` on deployment checks and status inspection, and `P7-7.2` on incident records and the next iteration plan.

In particular, this Part keeps the following distinctions throughout.

- `Analysis project`: questions, input units, summary values, and comparison tables are central
- `Model project`: baselines, prediction results, error cases, and revision priority are central
- `RAG and agent project`: evidence documents, tool results, execution records, and failure logs are central

This distinction is not only a genre label. It is also the standard for deciding what record should be organized first.

- In an analysis project, `the question and input unit` come before summary values.
- In a model project, `comparison rows` and `error samples` come before accuracy.
- In a RAG project, `retrieval evidence` and `answer state` come before the answer itself.
- In an agent project, `approval state` and `next actions` come before success or failure.
- In a deployment project, `incident records` and `next actions` come before deployment completion.

Part 7 keeps these examples inside the main text of each axis instead of separating them away from execution scenes. What matters is that `how to read the actual execution result` remains visible where the record is produced. Practice where the input changes and the output and interpretation change together matters more than examples that end at copying commands.

## Expansion Tasks This Part Does Not Close Directly

Because Part 7 focuses on project entry and integrated practice, it does not close the following tasks directly.

- How should team-level collaboration documents and experiment-tracking systems be designed?
- By what standards should larger datasets and longer operational logs be managed?
- To what stage should deployment automation and permission review be documented?

In other words, Part 7 closes `the minimum structure for starting and reviewing a project`, not every practical system in full.

## Understanding That Should Remain After This Part

After reading Part 7, the reader should carry roughly the following intuition.

- A project should define the question and the baseline before implementation.
- If the input unit and the floor line shake, later result interpretation also shakes.
- A model result without baseline comparison and improvement comparison is weakly interpreted.
- In an LLM project, not only answer examples but also retrieval failure, tool failure, permissions, and logs must be read together.
- A project retrospective is not a document that hides failure, but a document that prepares the next iteration.

Compressed to the shortest form, these five lines become the following.

`A project is not the act of running code once, but the act of leaving records that make it possible to reread why the result happened.`

## The Common Standard For Project Records

Each project in Part 7 is organized, whenever possible, in the following flow.

- Problem definition
- Data or input
- Approach
- Implementation
- Result
- Limitations and improvements
- Sources and references

This format is less a mechanical template than the minimum shared structure that makes a project runnable again and readable again. In the actual main text, however, `the execution scene` should appear before the label of the format. For example, in a result section, a comparison table and error cases should appear before a single score line. In an implementation section, how the input and output change should appear before a long code block.

In generative-AI-related projects, the following items are often added.

- Evidence documents or retrieval results
- Tool-call results or execution logs
- Automatic-evaluation results
- Human-review notes
- Execution records or fallback-action records when failure occurs

Read again as actual records, this common standard becomes the following.

| Document question | The record to check | Why this record is examined |
| --- | --- | --- |
| What was being attempted? | Goal sentence, planning steps, project notes | Because without the question and the plan, only execution logs remain and the purpose disappears. |
| What was put in? | Data tables, document snippets, tool lists | Because the same project cannot be rerun if the input is missing. |
| How was comparison made? | Baseline, comparison tables, evaluation records | Because claims of improvement must be interpreted through the same standard. |
| What was the evidence? | Selection grounds, retrieval candidates | Because RAG and agent results must be verifiable again later. |
| Where did it stop? | Blocked state, evidence-shortage state, failure state | Because a starting point for the next iteration appears only when the failure point remains. |
| What will change next time? | Review summary, improvement plan | Because a retrospective must lead to the next action rather than end as a memo. |

Reduced further into a practical check, the same questions can be inspected as follows.

| Project axis | What weak practice tends to omit | What strong practice leaves first |
| --- | --- | --- |
| Analysis | Only the result number | Question, input unit, comparison table |
| Model | Only accuracy | Baseline, error samples, reason for comparison |
| RAG | Only the answer | Evidence documents, answer state, missing grounds |
| Agent | Only success or failure | Tool order, approval state, blocked point |
| Deployment | Only that an incident happened | Incident category, priority, next action |

## Completion Criteria

- You can organize a project in the flow of question, input, implementation, result, and retrospective.
- You can explain the difference between a baseline and an improved model through actual comparison results.
- You can read quality and operational perspectives together in RAG and agent projects.
- You can leave failure records and the next improvement plan inside the project result.

At the shortest level, the completion standard of Part 7 can be grouped into the following sentence.

`You should be able to leave records that let a project you actually ran be executed again and interpreted again.`

## The Judgment Standards That Should Remain From This Part

If the following standards do not remain as records even after reading Part 7, the practice axis of this Part is not yet closed enough.

- Result numbers remain, but the baseline, error cases, and retrospective notes are missing
- RAG or agent work is being described, but evidence records, execution records, and permission records do not remain together
- The standard for what to check after deployment and what to leave as an incident record starts to shake

In that case, it is better to fix again the structure of `question -> execution -> evaluation -> retrospective` before attaching more new functionality.

## Checklist

- Can you rewrite the project goal again in one sentence?
- Can you immediately say which of the following is missing: baseline, comparison table, error case, failure record?
- Can you read evidence, tool, and permission records separately in RAG and agent work?
- Can you leave a retrospective sentence for the next iteration in each project axis?

## Sources And References

This document is an internal overview of Part 7. It does not directly cite external sources.
