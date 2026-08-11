# P6-19.2 A Minimal Implementation that Records Evidence, State, and Review Before the Response

> Section ID: `P6-19.2`
> Version: `v2026.07.31`

The minimum implementation record starts by leaving `request_id`, `selected_policy`, `evidence_state`, `answer_state`, `review_status`, and `retrospective_note`. With this record, the feature reads as a small function where evidence, state, and retrospective notes remain before the response sentence itself.

In P6-19.1, we tied a small generative AI feature into the flow `request interpretation -> retrieval or tool selection -> response generation -> state judgment -> record`. Here, we redraw that flow with a very small piece of code.

The point of the minimal implementation is not to complete a high-performance service. It is to see with your own eyes `which input goes through which path and remains as which output and record`. More precisely, it makes `what ran` and `where to fix first next` visible in the same request record.

## What Request Execution Records Leave Behind

The core questions are:

- What minimal implementation can be made before attaching a real commercial API?
- What execution record should keep retrieval, response generation, and review-needed state together?
- How can the remaining records show the next improvement point?

This implementation is a `reduced baseline implementation`. It ties a RAG flow, tool-use structure, evaluation, and record-keeping viewpoint into small code so we can check what output and execution record a request leaves behind. The goal is not to finish product-level automation or deployment. It is to make the same record show patch priorities such as `should retrieval be fixed first?`, `should the insufficient-evidence gate be fixed first?`, or `should the human-review boundary be reset?`.

The important shift is from `designing a request flow` to `leaving that flow as an actual request execution record`. The distinction between `it runs` and `it was designed to be recordable` also becomes visible here. This record should not be simple result storage. It should be an input that helps decide what to fix first among retrieval quality, state classification, and human-review handoff.

It is safer to watch when the same question changes inside the code flow into states such as `answer draft generated`, `insufficient evidence`, `document not retrieved`, and `human review needed`. The core of the minimal implementation is not merely printing strings. It is leaving, in the same record, the operating state in which one request ended.

| State that splits first inside the code flow | Common situation | Why this state must be recorded separately |
| --- | --- | --- |
| Answer draft can be generated | Two or more relevant evidence items are found and conflict is not large | To pass the request to the next evaluation while keeping `an answer can be drafted` separate from `it is ready to deploy` |
| Insufficient evidence | A related document is found, but direct evidence is weak or only one document exists | To avoid reading retrieval success and answer-finalization readiness as the same thing |
| Document not retrieved | No document that can settle the question is found | To avoid covering the gap with general advice and to leave search expansion as a separate issue |
| Human review needed | Exception clauses or approval boundaries make automatic certainty risky | Even a minimal implementation must keep operating boundaries and handoff points so the next improvement is possible |

## Separating Response Generation from Execution Records

- You can read the minimal implementation flow of a small generative AI feature.
- You can explain why retrieval results, response, evidence, and failure records should be output together.
- You can distinguish the fact that a feature runs from the judgment that the feature is well designed.
- You can explain the minimum record structure to check before the next improvement.

## Five Execution Steps in the Minimal Implementation

The minimal implementation in this section has five steps.

1. Receive a question.
2. Find related documents with simple rules.
3. Create an answer from the found documents.
4. Decide whether the answer can be finalized, whether evidence is insufficient, or whether human review is needed.
5. Record which documents were used and leave answer-quality notes.

Even without attaching a real LLM API call, checking these five steps first makes it easier to see later where the model call enters and where retrieval-quality problems arise.

## Execution State Left by Policy Documents and Questions

Input: 12 policy fragments in a policy document CSV, and 36 user questions that induce different failure types.

Output:

Retrieval score by document, selected evidence documents, generated answer draft, whether human review is needed, and evaluation notes.

The goal of this example is not `accuracy`, but checking a flow that includes `operating state classification`. Even in the same minimal feature, `multiple evidence items found`, `insufficient evidence`, and `retrieval failed` must be read separately to decide the next improvement priority. The `requires_review` column in the question CSV is not an answer key. It is an observation signal showing whether the question itself touches a human-review boundary such as approval, exception, or security.

## Cases and Examples

This minimal implementation section is needed because it separates `it ran once` from `it left operational judgment behind`. The three scenes below show that even when all of them look like the same policy assistant, without request execution records we cannot reread where the failure happened.

### Case 1. When an Answer Appears but Its Reason Is Not Recorded

If the answer string looks natural, people easily feel that the feature worked at least once. For example, if the question `Can an employee who joined this month use summer vacation right away?` receives a plausible one-sentence answer, it is tempting to pass it immediately.

But in this case, what is actually needed is a record of whether the `one month after joining` rule and the `summer vacation approval` rule were read together, whether the two pieces of evidence conflicted, and which documents the answer used. If only the answer remains and the evidence documents and execution state are not recorded, later you cannot distinguish whether a wrong answer came from bad retrieval or bad interpretation.

So even a minimal implementation should keep document scores, selected documents, and execution state next to the answer string. The result to confirm in this case is not `an answer appeared`, but `can we reread why that answer appeared from the same request execution record?`

This scene matters because, when a problem happens in operation, the first question people ask is less `what answer did it give?` and more `why did it answer that way?` Without evidence documents and execution state, even if the same failure appears the next day, you cannot immediately separate retrieval-quality problems from prompt-interpretation problems. Fixes become guesswork. In contrast, if even the minimal implementation leaves a request execution record, you can retrace which document scored too highly, which rule was not selected together, and where the judgment began to drift.

The information an operator can see changes greatly depending on whether the same request left records.

| Request execution result | How it looks on the surface | What the operator can actually reread |
| --- | --- | --- |
| Only the answer string remains | It looks as if the response was completed | Almost nothing. Retrieval failure and interpretation failure are hard to separate |
| Answer + selected document list remain | It looks as if evidence exists | Which documents were seen is visible, but why they were chosen is unclear |
| Answer + document scores + selected documents + execution state remain | It looks like a small baseline implementation | It is possible to trace whether retrieval, selection, or interpretation should be fixed first |

The criterion to hold from this table is not `more records make things complex`, but `without records, the next improvement is blocked`. The focus of the minimal implementation is not building a polished dashboard. It is leaving the minimum clues needed to reread failure.

### Case 2. When the Answer Is Finalized Despite Insufficient Evidence

A question such as `Can new benefit points be used starting this week?` is riskier. If the system finalizes the answer just because one document was retrieved, it may actually have answered from a general sentence such as `new benefit programs require HR confirmation until notice`, not from a direct benefit-point rule.

In this scene, it is easy to feel that `since at least one related document appeared, an answer is possible`. But the more important thing is to record whether there is only one piece of evidence, whether exception clauses may be missing, and whether human review is needed. In other words, `retrieval success` and `answer can be finalized` are not the same step.

So even in the minimal implementation, `insufficient evidence state` and `human review needed state` must remain separately. Then the retrospective can distinguish whether the next issue is search expansion or approval-gate design. The result to confirm in this case is not `an answer was generated`, but `was the insufficient-evidence state kept as an operating route instead of being hidden?`

This is more dangerous in practice because `one document was found` gives people too much comfort. Once a related document title appears in a search screen, it is easy to treat that almost as `evidence secured`. But operational judgment must separate `a related document exists` from `there is enough evidence to settle the question`. Especially when exception clauses or approval procedures are involved, finalizing an automatic answer from a single evidence document can distribute the wrong answer with more confidence.

The difference can be written as an operating note.

| State | Interpretation that comes to mind first | Operating judgment that should actually remain |
| --- | --- | --- |
| 1 related document retrieved | `It was found, so we can answer.` | Distinguish direct evidence from surrounding explanatory material |
| Exception clause unchecked | `We can answer first and reinforce later.` | Raise the request to human-review-needed state |
| Automatic response completed from single evidence | `The minimal feature worked.` | Operating risk increased because insufficient evidence was hidden |

The misunderstanding to get past here is `retrieval success = automatic response allowed`. What the minimal implementation should show is not the impressiveness of automation, but whether the boundary line `this must still go to human review` can be kept as a state value.

### Case 3. When No Document Is Found but the Gap Is Covered by General Advice

Consider the question `How much is the night-shift allowance starting this month?` Even if the current document set has no night allowance policy, the model can combine generic HR guidance and produce a plausible sentence such as `It is paid according to company policy`. If no document is retrieved but the answer sentence sounds natural, it is easy to think, `Since it responded anyway, maybe we can reinforce it later.` Operationally, this is one of the most dangerous cases. The fact that no related document was found is itself the key signal. If that is hidden under a general answer, questions that need human review and questions that require search-index expansion get buried together.

So the minimal implementation should leave `document not found` as an explicit state, not as a mere exception. With this state, a later retrospective can distinguish `there was no source document`, `there was a document but keywords or embeddings missed it`, and `the question expression should be expanded`. The misunderstanding to leave behind is `if no answer was found, quietly fill the gap with general advice`. The result to confirm in this case is not `did it cover the blank naturally?`, but `did it clearly leave the failure of not finding documents as an operating state?`

The three cases can be reduced through the lens of request execution records.

| Scene | What is missed if only the answer remains | Record to keep together |
| --- | --- | --- |
| Question requiring multiple evidence items | Which documents were read together and whether conflict was possible | Document scores, selected documents, execution state, answer draft |
| Question with only one evidence item | Whether the answer can be finalized or needs human review | Insufficient-evidence state, whether human review is needed, retrospective note |
| Question where no document was found | Whether this was retrieval failure or interpretation failure, and whether general advice covered the gap | Document-not-retrieved state, failure note, next action |

## Rereading Failure Through Records

A common misjudgment when first reading a minimal implementation is to feel that the implementation is already enough because `an answer appears`. But the first thing to check is not whether the answer appeared. It is whether `what remains for the next improvement` can be reread from the same request record.

| If this scene appears | First thing to check | Why this check comes first |
| --- | --- | --- |
| The answer appears, but why it answered that way cannot be explained | Are document scores and selection rationale left together? | To separate retrieval failure from interpretation failure, the selection path behind the answer must be visible. |
| Evidence is weak but the request ends as an automatic response | Is human-review-needed state left separately? | Retrieval success and answer-finalization readiness are not the same thing. |
| No document is found, but a general answer covers it | Are document-not-retrieved state and next action explicit? | If failure is hidden, search expansion issues and answer-policy issues cannot be separated in the next retrospective. |

The same criterion can be shortened into practical questions.

| If this suspicion appears | First question to ask |
| --- | --- |
| `There is an answer, but I do not know what to fix.` | Which document was selected with which score? |
| `Isn't this an answer a person should review again?` | Did human-review-needed state remain as a state value? |
| `Why did it answer even though retrieval failed?` | Were document-not-retrieved state and next action recorded without being hidden? |

The first criterion to learn is simple. A minimal implementation is not a toy that ends at `a response appears`. It is a baseline implementation that keeps `evidence documents`, `execution state`, `whether human review is needed`, and `next action` together so the next improvement can be read.

## Exercise and Example

The example checks `question -> retrieval -> answer draft -> evaluation -> record` all at once. Instead of looking at only two questions, it includes `multiple evidence found`, `only one evidence found`, and `retrieval failure` so that even a small baseline implementation splits into several failure types. In particular, each question ends as one request execution record, making it possible to reread what should be fixed in retrospectives or operational judgment.

The example input is a policy document CSV and a user question CSV. The result includes retrieval scores by document, selected evidence documents, an answer draft, whether human review is needed, retrospective notes, request execution records by question, and summary statistics over the whole question set.

The key to check is that even a minimal implementation must tie retrieval, answer, evaluation, and record into one flow. Request execution records must remain by question so recurring failure types can be reread. From an operational viewpoint, how evidence gaps and retrieval failures are separated matters more than raw accuracy.

Before reading the code, it is useful to write down what execution state should remain for the representative questions below.

| Question | Execution state to expect first | Why this is expected |
| --- | --- | --- |
| `Can an employee who joined this month use summer vacation right away?` | Multiple evidence check state | The request settles only after reading both the joining rule and vacation rule. |
| `Can new benefit points be used starting this week?` | Insufficient evidence + human review state | Direct evidence is likely weak, so there is risk of missing exception clauses. |
| `How much is the night-shift allowance starting this month?` | Document not retrieved + human review state | The current document set is likely unable to find a related rule. |

If you write your answer first and compare it with the code result, it becomes clearer that this is not a simple output check, but a practice in `operational state classification by question`.

The integrated record criteria for this example are:

| Check item | Why it is needed |
| --- | --- |
| Evidence document list | To leave which evidence was actually used |
| Whether human review is needed | To separate answers that can be used immediately from answers needing human confirmation |
| Execution state | To distinguish multiple evidence, insufficient evidence, and retrieval failure at a glance |
| Overall summary | To read which failures are common in the whole flow, not only one question at a time |

The example below uses the policy document CSV [p6_18_2_policy_documents_en.csv](/AiBook/assets/part-06/chapter-18/p6_18_2_policy_documents_en.csv){ .csv-preview } and the question CSV [p6_18_2_policy_questions_en.csv](/AiBook/assets/part-06/chapter-18/p6_18_2_policy_questions_en.csv){ .csv-preview }. One row in the document file is one policy fragment. One row in the question file contains a user question, interpreted keyword groups, and a human-review-needed signal. `requires_review` is not an answer-key column for whether the model was correct. It is an input signal for observing question types where an automatic definite answer is risky. This example does not attach a real LLM or real search engine. It is a baseline implementation for checking which evidence and state should remain in the request execution record.

Retrieval does not directly understand natural-language questions. It uses the overlap between `query_groups` in the question CSV and `keyword_groups` in the document CSV as a simple score. So the important point here is not to exaggerate retrieval quality. It is to record which documents this loose retrieval pulled in and what its limits are.

```python
--8<-- "assets/part-06/chapter-18/p6_18_2_generate_run_records_en.py"
```

Read the output in three layers. `[summary]` shows the state distribution over 36 questions. `[selected_records]` shows whether representative questions split into different execution states. `[detailed_record]` checks whether document scores, selected evidence, answer draft, and evaluation state remain together in one request.

```text
[summary]
{'multi_evidence_count': 26,
 'needs_human_review_count': 24,
 'next_patch_counts': {'expand_index_or_add_policy_documents': 8,
                       'expand_retrieval_or_add_review_gate': 2,
                       'improve_grounded_answer_rules': 26},
 'retrieval_failed_count': 8,
 'run_count': 36,
 'single_evidence_count': 2}
[selected_records]
{'needs_human_review': False,
 'next_patch': 'improve_grounded_answer_rules',
 'notes': ['Multiple evidence check: read several documents together to '
           'inspect possible condition conflicts'],
 'query_id': 'query_001',
 'question': 'Can an employee who joined this month use summer vacation right '
             'away',
 'retrieved_doc_ids': ['policy_001', 'policy_002', 'policy_003'],
 'run_status': 'multi_evidence'}
{'needs_human_review': True,
 'next_patch': 'expand_retrieval_or_add_review_gate',
 'notes': ['Possible evidence gap: only one document was found, so missing '
           'exceptions should be checked',
           'Because of the question type, keep human review state instead of '
           'an automatic final answer'],
 'query_id': 'query_002',
 'question': 'Can new benefit points be used starting this week',
 'retrieved_doc_ids': ['policy_004'],
 'run_status': 'single_evidence'}
{'needs_human_review': True,
 'next_patch': 'expand_index_or_add_policy_documents',
 'notes': ['Retrieval failed: no related document was found, so human review '
           'is needed',
           'Because of the question type, keep human review state instead of '
           'an automatic final answer'],
 'query_id': 'query_003',
 'question': 'How much is the night-shift allowance starting this month',
 'retrieved_doc_ids': [],
 'run_status': 'retrieval_failed'}
{'needs_human_review': True,
 'next_patch': 'improve_grounded_answer_rules',
 'notes': ['Multiple evidence check: read several documents together to '
           'inspect possible condition conflicts',
           'Because of the question type, keep human review state instead of '
           'an automatic final answer'],
 'query_id': 'query_007',
 'question': 'Can I share a file containing personal data outside the company',
 'retrieved_doc_ids': ['policy_010', 'policy_002', 'policy_004'],
 'run_status': 'multi_evidence'}
{'needs_human_review': True,
 'next_patch': 'improve_grounded_answer_rules',
 'notes': ['Multiple evidence check: read several documents together to '
           'inspect possible condition conflicts',
           'Because of the question type, keep human review state instead of '
           'an automatic final answer'],
 'query_id': 'query_026',
 'question': 'Do I request access in the asset management system',
 'retrieved_doc_ids': ['policy_006', 'policy_003', 'policy_007'],
 'run_status': 'multi_evidence'}
{'needs_human_review': True,
 'next_patch': 'expand_index_or_add_policy_documents',
 'notes': ['Retrieval failed: no related document was found, so human review '
           'is needed',
           'Because of the question type, keep human review state instead of '
           'an automatic final answer'],
 'query_id': 'query_030',
 'question': 'Where is the night-shift meal allowance policy',
 'retrieved_doc_ids': [],
 'run_status': 'retrieval_failed'}
[detailed_record]
{'draft_answer': 'Question: Can an employee who joined this month use summer '
                 'vacation right away\n'
                 'Evidence found:\n'
                 '- policy_001: New employees can use monthly leave after one '
                 'month from their start date\n'
                 '- policy_002: Summer vacation can be used within the '
                 'announced period after team approval\n'
                 '- policy_003: Remaining leave days are checked in the HR '
                 'system\n'
                 'Draft judgment: multiple evidence documents should be read '
                 'together to check condition conflicts and application order.',
 'evaluation': {'needs_human_review': False,
                'next_patch': 'improve_grounded_answer_rules',
                'notes': ['Multiple evidence check: read several documents '
                          'together to inspect possible condition conflicts'],
                'run_status': 'multi_evidence'},
 'query_id': 'query_001',
 'question': 'Can an employee who joined this month use summer vacation right '
             'away',
 'retrieved_doc_ids': ['policy_001', 'policy_002', 'policy_003'],
 'top_document_scores': [{'doc_id': 'policy_001',
                          'matched_groups': ['leave', 'onboarding'],
                          'score': 2},
                         {'doc_id': 'policy_002',
                          'matched_groups': ['leave'],
                          'score': 1},
                         {'doc_id': 'policy_003',
                          'matched_groups': ['leave'],
                          'score': 1},
                         {'doc_id': 'policy_004',
                          'matched_groups': [],
                          'score': 0},
                         {'doc_id': 'policy_005',
                          'matched_groups': [],
                          'score': 0}]}
```

![Request execution status and human-review distribution](/AiBook/assets/part-06/chapter-18/run-record-status-summary-en.png)

## Reading Retrieval Scores and Operating State Together

This example does not call a real LLM or real search engine. What we look at first is not performance, but the skeleton of request execution records that must remain even after LLM, RAG, and tool use are attached later. Even this small baseline can clearly reveal five things.

- A question enters.
- The retrieval step exists separately with scores.
- The answer depends not on one document, but on a selected evidence bundle.
- Multiple evidence, insufficient evidence, and retrieval failure are recorded as different notes and execution states.
- Per-question execution results are grouped again into an overall summary at the end.

So the result to confirm in this example is not one line, `the model answered`. It is whether retrieval score, evidence documents, answer draft, human-review flag, retrospective note, and request execution record by question actually remain separately. In particular, even inside the same minimal feature, `multiple evidence secured`, `insufficient evidence`, and `retrieval failed` must remain as different operating states.

In the representative detailed record, it is intentional that the `remaining leave days lookup` document is also retrieved. This document shares the same `leave` keyword group, but it is hard to read as direct evidence that settles `whether summer vacation can be used right after joining`. Therefore, this result should not be read as complete retrieval success. Instead, because simple keyword-group retrieval can pull in nearby documents, the execution record must keep document scores and selected documents so reranking, evidence-citation rules, and groundedness checks can be attached in the next step.

The same result can be rewritten as a practical review note.

| Question | Review note to leave now | Next patch priority |
| --- | --- | --- |
| Question involving both joining and vacation rules | Two or more evidence items were found, but an interpretation rule for condition conflicts is needed | Interpretation rule and groundedness check |
| Question with weak direct evidence, such as benefit points | An answer can be drafted, but finalizing immediately is risky | Search expansion or approval gate |
| Question where no document was found | It is good that failure was exposed instead of decorating the answer, but the retrieval range is insufficient | Index expansion, document addition, human-review flow |

## What to Review from Request Execution Records

This minimal implementation does not stop at checking whether the code runs once. The request execution record left by each question must be reread to distinguish whether the failure occurred in retrieval, interpretation, or a state that should be routed to human review.

For example, if a document was found but the answer failed to fully reflect a condition such as `one month after joining`, that is an interpretation failure after retrieval success. In that case, evidence-citation style and answer-review rules should be checked before adding more keywords. Conversely, if no related document was found, the system should not decorate an answer. It should leave `human review needed state` and first check keyword expansion, embedding search, or index improvement. If the answer was given but actual remaining days or approval status were missing, the direct cause may be the absence of a lookup API or tool call, not a document-search problem.

Reading this way makes it clear what should be fixed first when the same failure appears again.

One step further, it is useful to separate what the minimal implementation directly shows from what remains for the next improvement.

| Situation | What this minimal implementation directly shows | What remains for the next improvement |
| --- | --- | --- |
| Questions produce different results | Multiple evidence, insufficient evidence, and retrieval failure remain as different execution states | Real embedding search, reranking, more precise groundedness judgment |
| An answer appears but needs review | Human-review-needed state, retrospective note, request execution record | Approval gate, real human-review queue, retry policy |
| Evidence is insufficient or missing | Retrieval and interpretation are reviewed separately | Better search infrastructure and tool-call connection |
| The code runs once | Request path and record structure appear separately | Service work that includes cost, latency, and operating limits |

The key in this table is that the minimal implementation is more than a `working example`. It is a `baseline that shows where to fix next`. Real embedding search, tool use, AI agent loops, and operating controls are then added on top of this baseline.

The retrospective questions can be this simple.

| Scene | Retrospective question to leave immediately | Likely first area to fix next |
| --- | --- | --- |
| A document was found but the answer drifted | Did the answer read the evidence all the way through? | Interpretation rule, groundedness check |
| No document was found and the request went to human review | Was lack of evidence left visible instead of hidden? | Search expansion, human-review flow |
| Choosing the next expansion point | Is the failure a retrieval problem or absence of a tool? | Vector search, tool use, agent branch |

## What This Minimal Implementation Still Cannot Do

This minimal implementation clearly has limits: retrieval quality depends on simple keyword rules, answer generation is essentially template-level, priority among conflicting documents is not handled, and real tool calls or permission checks are not included.

But writing down these limits is exactly how we separate `the code ran once` from `it can be used repeatedly under real work conditions`.

Another important point is that this list of limits becomes the design priority.

- If retrieval failures are common, fix retrieval quality first.
- If documents are found but answers often drift, fix answer-generation rules and evidence display first.
- If current-state questions increase, attach tool use.

The retrospective of a minimal implementation should therefore not be an impression. It should be an input for deciding the `next patch order`.

## When to Expand to Vector Search and Tool Use

This mini-practice becomes an expansion target when situations like these appear:

- There are enough documents that keyword rules begin to show limits.
- Similar expressions need to be found more reliably.
- Current-state lookup or execution is needed.

This section is therefore not a `finished implementation`, but a `baseline for the next improvement`.

It is enough to connect it as follows.

- If better evidence connection is needed, return to the RAG flow in P6-11 and the vector database structure in P6-13.
- If real state lookup or calculation is needed, move to tool use in P6-14.
- If multi-step judgment is needed, move to the AI agent structure in P6-15.
- Failure records and safety devices should be reread through the evaluation viewpoint in P6-16 and the operation viewpoint in P6-18.

## Checklist

- Can you explain that a minimal implementation is not a finished product, but a baseline for structure checking?
- Can you explain that retrieval, response, and records should be output together rather than separately?
- Can you distinguish the fact that a feature runs from the judgment that it is actually usable?

## Sources and References

- OpenAI, [Retrieval](https://developers.openai.com/api/docs/guides/retrieval){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Working with evals](https://developers.openai.com/api/docs/guides/evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
