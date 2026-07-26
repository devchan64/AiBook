# P6-18.1 A Small Generative AI Feature that Connects Question, Evidence, Answer, and Record

> Section ID: `P6-18.1`
> Version: `v2026.07.26`

Even if you can explain LLMs, RAG, tool use, agents, evaluation, and failure handling separately, the actual feature design is not finished yet. The question now gathers around how these concepts move together inside one real request.

A small generative AI feature is safer to understand as a flow: `interpret request -> retrieve needed evidence or choose a tool -> generate model response -> judge state -> record`. Here, `judge state` also includes which state values are left inside the actual request for decisions such as automatic gate, human review, retry, fallback, stop, and approval.

## Reconnecting Everything Through One Request

The core questions are:

- How can the concepts from Part 6 be reconnected as one request flow?
- When is a prompt alone enough, and when should retrieval or a tool be attached?
- What is the minimum record a small feature should keep?

We have already studied retrieval and evidence connection, tool selection and execution connection, execution records and reproducibility, operating constraints, and failure handling separately. Here, those pieces are reconnected as `the structure by which one request actually closes`.

The important shift is from `choosing a failure route` to `tying together the structure of one request, including that judgment`. You need a criterion for grouping question, evidence, execution, evaluation, and record at request level. Only then can the request result remain as a state value such as `answer draft possible`, `evidence reinforcement needed`, `state lookup needed`, or `human review needed`.

The judgments made in evaluation and operation come down into the request structure as follows.

| Judgment already made | What must enter the request flow | What to keep as a request execution record |
| --- | --- | --- |
| Automatic gate and human review result | Whether to accept this answer immediately or route it to additional checking | Answer state, whether human review is needed, review summary |
| Retry, fallback, stop, and approval judgment | Which route was taken when failure occurred | Next action, incident record, execution note |
| Retrieval, tool, and state-acquisition result | Which evidence and execution the answer was based on | Evidence document list, selection rationale, execution record |

It is safer to watch when the same question becomes `answer draft`, `human review`, `state lookup needed`, or `insufficient evidence` inside the request. The core of request-flow integration is not attaching many component names. It is making visible when evaluation and operation judgments become actual request state values.

For example, even in the same HR assistant, requests split as follows.

| State that splits first in the same request flow | Common question type | Why this state should remain |
| --- | --- | --- |
| Answer draft possible immediately | Polishing a sentence or changing format that closes with the current input | To avoid making the flow heavy with unnecessary retrieval or tools |
| Evidence document check needed | Questions about current rules, policies, or procedures | To separate `an answer can be written` from `the evidence is sufficient` |
| Current state lookup needed | Remaining leave, approval status, actual schedule lookup | To avoid mixing policy explanation and current-value response in the same step |
| Human review or insufficient evidence state | Questions with many exception clauses or insufficient documents | To avoid covering the issue with a natural-sounding general answer and to keep the operating route |

So tying together a request flow does not simply mean drawing `question -> answer`. It means keeping `how far this request has closed so far` inside the same structure. With this criterion, the request execution record becomes not just a log, but an operating note that distinguishes `answerable`, `evidence reinforcement needed`, `state lookup needed`, and `human review needed`.

## Distinguishing Prompt, Retrieval, and Tool-Use Request Flows

- You can explain a small generative AI feature as a request flow.
- You can distinguish work that can be handled by prompt alone from work that needs retrieval or tools.
- You can connect input, evidence, output, evaluation, and record in one design sentence.
- You can read the request execution records needed in a minimal implementation more easily.

The first split can be organized as follows.

| First visible request state | First question to ask | Why this question comes first |
| --- | --- | --- |
| It seems possible to draft an answer from the input alone | Does this request close around the prompt? | If the needed information is already present, unnecessary retrieval or execution should not make the flow heavier. |
| An answer can be written, but current rules or documentary evidence feel uncertain | Should evidence documents be checked first? | Natural general advice and evidence-based answers should not be mixed as the same state. |
| A rule explanation is not enough; a current value or actual state is needed | Is state lookup or tool use needed before retrieval? | Document-evidence questions and current-state questions must be separated to see where the request flow changes. |
| A definite answer is risky because there are many exceptions | Should this remain as human review, follow-up question, or insufficient-evidence state? | If answer generation and request closure are treated as the same thing, requests that should remain pending are easy to force into completion. |

With this table in mind, the rest of the section becomes easier to read not as a `list of steps`, but as a criterion for deciding which request state the same question enters first.

## Which Feature Should We Use as the Example?

Take an `internal-document-based vacation policy assistant`. When a user asks, `Can an employee who joined this month use summer vacation right away?`, it may look like a simple Q&A task. In reality, the assistant must retrieve the current policy document, and the request may later expand into a system lookup such as `How many vacation days do I have left?` The assistant must also record which document was used as evidence, or that no document was found, so the feature can be fixed later. That makes this example useful for tying prompting, retrieval, tool use, evaluation, and records together inside one request.

This case was chosen because `questions closed by prompt alone`, `questions requiring retrieval`, and `questions requiring current-state lookup` can be compared side by side in one flow. It also naturally reveals operational judgments such as evidence-document selection, failure records, and human-review routing. The point is not to explain the HR domain in detail, but to show what structure a small generative AI feature needs.

## Drawing It as One Request Flow

The simplest flow for the question above is:

1. Read what kind of question it is.
2. Judge whether it needs current policy.
3. Retrieve related documents if needed.
4. Create an answer and attach the evidence.
5. If something is ambiguous or missing, route to human confirmation or a follow-up question.

Even these five steps already form a structure different from a simple prompt example.

But to read the request flow as an operable structure, one more step is needed.

6. Record whether the answer should be accepted immediately or routed to evidence reinforcement or human review.

In other words, saying that one request has closed does not only mean that an answer sentence was created. It also means the state in which the answer remains has been decided.

The flow can be simplified once more as follows.

```mermaid
--8<-- "assets/part-06/chapter-18/p6-c18-s01-request-flow-en.mmd"
```

The key point in this figure is that even a small feature should be read as a flow of `question classification`, `evidence or state acquisition`, `answer`, and `record`.

The main line of the back half of Part 6 closes here by tying `good-answer judgment` and `choosing an operational path on failure` into `one request flow that connects question, evidence/state, answer, evaluation, and record`.

## When Prompt Alone Is Enough

A prompt alone is usually enough in cases such as:

- Polishing a sentence
- Changing summary format
- Answering within already provided material
- Writing a creative draft

In these cases, the model can perform the task using only `information inside the current input`.

For example:

- Making an email sentence more polite
- Summarizing the already pasted meeting notes in three sentences

These tasks can start without retrieval or tool calls.

## When Retrieval Is Needed

Retrieval becomes necessary when conditions such as these appear:

- Current rules matter.
- Evidence documents must be shown with the answer.
- Long internal documents cannot all be placed directly into the prompt.
- Current repository documents are more reliable than the model's internal memory.

The vacation policy assistant belongs here. The actual current company policy matters more than `a general answer that sounds correct`.

In these cases, the problem should be read not as `writing in a better tone`, but as `finding the current document accurately and answering with evidence`.

`The model's ability to write a good answer` and `the system's ability to bring the right evidence` are not the same problem.

## When Tool Use Is Needed

Retrieval alone is not always enough.

For example, if the user asks for:

- remaining vacation days,
- approval status, or
- creating an application form,

document retrieval is no longer sufficient.

In these cases, the system needs a tool that reads a value from the real system or performs an action.

Retrieval is closer to checking `what the rule is`, while tool use is closer to handling `what should be executed or looked up in the current state`.

## Even Small Features Need Minimal Evaluation

Even for a small feature, looking only at one answer makes improvement difficult.

At minimum, it is useful to keep these four records.

| Record item | Why it is needed |
| --- | --- |
| User question | To keep what request was handled |
| Whether retrieval or tool use was used | To distinguish failure causes later |
| Final answer | To revisit output quality |
| Evidence or failure reason | To distinguish wrong answers from system issues |

These four items are the minimum device that brings the evaluation and failure-handling explanations from the back half of Part 6 into actual design.

| Criterion in the design sentence | Minimum record to keep | Larger artifact it can grow into |
| --- | --- | --- |
| Question and retrieval path | Request execution record by question, evidence document list, score by document | Search log, selection rationale, execution record |
| Whether the answer is accepted and whether human review is needed | Human-review-needed flag, execution state | Review summary, answer state, incident record |
| Retrospective after several questions | Overall summary | Improvement plan, Part 7 project retrospective |

The key is not to draw a generative AI feature as `one model call`. The request must be read, needed evidence or state must be acquired, and the answer and record must be seen as one structure.

## Cases and Examples

The distinction among `prompt-centered`, `retrieval combined`, and `tool use combined` can be reconnected to feature scenes as follows.

The focus of these cases is not `using generative AI`, but `which structure must be attached for this question to close`.

### Case 1. Polishing a Sentence

Imagine a feature that makes an entered notice sentence more polite. It is easy to think that a generative AI feature should always include retrieval or tools, but in this case the first thing to check is `the current sentence itself`, and external documents or real-time system values may not be needed. For example, making `Submit the documents again` sound softer is not a problem of finding the latest policy. It is a problem of how to express a sentence that is already given.

If retrieval is attached here, unrelated policy phrases may be mixed in, producing a longer and stiffer answer than the original. The core structure is therefore closer to a prompt with good instructions and examples. If the target to be changed is already inside the input, a prompt-centered structure may be enough. The shift here is from asking `does generative AI require retrieval too?` to asking `does the work close with the current input alone?` Therefore, the result to confirm in this case is whether the desired expression change closes sufficiently from the input sentence itself without retrieval.

In this scene, it is important to first ask whether the needed information is already present. Adding retrieval to a request that only needs expression change can make the answer scattered while trying to find evidence that is not needed. So when designing a small generative AI feature, it is more important to first remove unnecessary components than to attach more components.

| What is already present to close the question | What does not need to be attached | Problem if attached unnecessarily |
| --- | --- | --- |
| Original sentence to revise | retrieval, tool use | Unrelated rules or background mix in and lengthen the answer |
| Desired tone or format instruction | External state lookup | Search-result organization becomes larger than expression conversion |
| One or two examples | System execution step | A simple sentence edit becomes an excessive workflow |

### Case 2. Internal Policy Guidance

Consider an internal policy-guidance chatbot. When people see questions such as `How many days in advance should I request vacation?` or `What is the order for applying for parental leave?`, they may feel that the model can simply write the answer. But for these questions, accurately bringing the latest policy document comes before tone. For example, last quarter's policy may have said `3 days in advance`, while the latest policy changed to `5 business days in advance`. Even with a well-written prompt, the model's internal memory cannot guarantee the current standard.

Because policies can change, finding the latest document and attaching evidence sentences is more important than a natural-sounding answer. The core structure in this case is closer to retrieving the latest passage and organizing the answer based on that evidence. The shift here is from asking `can it write the answer well right away?` to asking `does it actually bring the latest policy evidence?` Therefore, the result to confirm in this case is whether the answer becomes more stable in evidence accuracy, rather than tone, when the latest passage is attached.

In this case, you need to quickly read the signal that `input alone is not enough`. For a policy question, `is this correct by current standards?` matters more than whether the sentence sounds natural. Even if you improve only the model's ability to write well without attaching current documents, the core failure remains. Retrieval is therefore not optional decoration. It is a required structure for closing the question.

| What the question requires | Limit that remains with prompt alone | Why retrieval is needed first |
| --- | --- | --- |
| Current policy numbers and conditions | Internal memory may be outdated | Latest passage and evidence sentence must actually be attached |
| Explanation with source | The answer may sound natural but lack evidence | Selected document and evidence sentence can remain together |
| Guidance on frequently changing policy | Tone adjustment alone cannot reduce the error | Document updates can be reflected directly in the answer flow |

### Case 3. Remaining Vacation Lookup

Remaining vacation lookup is one step further. Policy documents can explain `how annual leave is calculated`, but they cannot answer `how many days are actually left in my account`. It is easy to feel that once the policy is found, the answer is complete. But to close this request, you must immediately distinguish that not only the rule, but also the HR system value, is needed.

For example, even if the annual leave formula is known, the current balance that reflects already used days and pending vacation approvals can only be known by querying the system. This feature is not closed by retrieval alone. Tool use that reads the real state must be attached. The shift here is from asking `can the rule be explained?` to asking `can the current state value be actually looked up and used to close the answer?` Therefore, the result to confirm in this case is whether a question that cannot close with policy explanation alone closes as a current-state answer only after a real system lookup is attached.

The three cases can be reduced to design judgment as follows.

| Question form | What to check first | Problem if the wrong structure is attached |
| --- | --- | --- |
| Sentence expression revision | Is the needed information already inside the input? | Unnecessary retrieval scatters the answer |
| Rule explanation | Is a current evidence document needed? | The answer relies on outdated standards or generalities |
| Current state lookup | Is a system value needed instead of a document? | Explains the rule but cannot answer the actual state |

The same idea can be drawn again as a design-choice flow.

```mermaid
--8<-- "assets/part-06/chapter-18/p6-c18-s01-request-routing-en.mmd"
```

The key point in this diagram is that the feature structure is chosen not by model type, but by the evidence and state needed to close the question. Also, whatever structure is chosen, the final step must recheck the risk of overconfident answers or insufficient evidence so the request can be routed to human review or a follow-up question.

## Scenes Where Request State Should Be Recorded First

A common misunderstanding when first reading small generative AI feature design is to think, `Since this is an AI feature, I should attach lots of retrieval and tools first.` In reality, it is more important to distinguish `what is first missing to close the current question`.

Turned into practical questions, this criterion reads as follows.

| If this suspicion appears | First question to ask |
| --- | --- |
| `Isn't this just a matter of writing it well?` | Is the needed information already inside the input? |
| `An answer can be written, but the evidence feels uncertain.` | Should the latest document and evidence sentence be attached first? |
| `The rule was explained, but the user did not get the actual value they wanted.` | Is a current-state lookup tool needed? |
| `An answer can be made, but a definite answer feels risky now.` | Should this remain as human review, follow-up question, or insufficient-evidence state? |

If the same request is brought down to `which state should remain?`, it can be read more briefly as follows.

| State to record immediately after reading the request | First criterion |
| --- | --- |
| `answer draft possible` | Does the needed information already exist in the input, and can the request close without additional evidence or state lookup? |
| `evidence reinforcement needed` | Can an answer be written, but is the latest document or evidence sentence still missing? |
| `state lookup needed` | Does the request need a real value, such as current balance, approval status, or schedule state, rather than a rule explanation? |
| `human review or insufficient evidence` | Are there many exception clauses or insufficient documents, making a definite answer risky now? |

The key in this table is to go one level below `which structure should be attached?` and record immediately `how far this request has closed so far`. That way, even after retrieval or tool use is attached, the final state can still be separated into `answerable`, `evidence reinforcement needed`, `state lookup needed`, and `human review needed`.

The first criterion to learn is simple. Designing a small generative AI feature is closer to distinguishing what is first missing among `current input`, `current evidence`, `current state`, and `whether a definite answer is possible`, then attaching the right structure and state value, than to choosing a model-call method.

## Exercise and Example

The focus of this exercise is not `attach a generative AI feature`, but judging directly `which structure is needed to close the question`. Even after reading the cases above, prompt, retrieval, and tool use can look mixed again when you see an actual request sentence. So read the question, write down `which structure is needed`, `what record must remain`, and `where failure appears if the wrong choice is made`, then compare with the explanation below.

The exercise below uses four request sentences. Even though they look like the same HR assistant, some requests close with `prompt-centered`, some first need `prompt + retrieval`, and some first need `prompt + tool use`.

The key is to first distinguish whether the question needs `current input`, `current evidence`, or `current state` to close. If the structure is chosen incorrectly, missing evidence, missing state, or unnecessary retrieval appears before answer quality becomes the main problem.

First, cover the `structure to attach first` column in the table below and write what each request needs first. Then compare the answer, reason, and record item.

| Request scene | Structure to attach first | Why this structure fits | Minimum record to keep |
| --- | --- | --- | --- |
| `Please make the notice sentence below softer.` | prompt-centered | The target to revise is already entirely inside the input | Original sentence, revised sentence, revision intent |
| `What is the parental leave application order this quarter?` | prompt + retrieval | Current policy documents and evidence sentences are needed first | Question, selected document, evidence sentence, answer |
| `How many vacation days do I have left?` | prompt + tool use | A current account-state lookup is needed, not a rule explanation | Question, called lookup tool, lookup result, answer |
| `Do welfare points expire immediately this year?` | prompt + retrieval, human review if needed | Current notice documents are needed first, and the answer should not be definite if the documents are insufficient | Question, selected document, whether evidence is insufficient, whether human review is needed |

![Structures needed first by request](/AiBook/assets/part-06/chapter-18/request-structure-matrix-en.png)

When reading this table, what matters more than the `correct feature name` is `what is missing first if the answer is to close`. For example, if retrieval alone is attached to a remaining-vacation lookup, the rule sentence may be retrieved, but the current balance remains unanswered. If retrieval is attached to sentence polishing, the answer can become scattered instead.

The same idea can be shortened into a practical review note.

| Wrongly chosen structure | Problem that appears first | Safer next judgment |
| --- | --- | --- |
| Attaching retrieval to sentence polishing | Unrelated rule phrases mix in and make the answer long and stiff | First check whether the work closes with the current input |
| Handling policy guidance with prompt alone | Relies on generalities or outdated memory instead of current policy | Attach current document retrieval and evidence display first |
| Handling state lookup with retrieval alone | Explains the rule but cannot answer the current value | Attach the actual state-lookup tool |
| Giving a definite answer when evidence is insufficient | The answer sounds natural but evidence-missing risk increases | Route to human review and keep a failure record |

## Reconnecting as a Design Sentence

Instead of writing a long design document, it is enough if you can summarize one feature in a sentence like this:

`The vacation policy assistant reads the user's question, retrieves relevant policy documents, creates an answer with evidence sentences, and records retrieval failure or missing evidence.`

If the feature requires current-state lookup, the sentence must change too. For example: `The remaining-vacation guidance feature reads the user's question, checks vacation rules if needed, retrieves the current remaining days through an HR-system lookup tool, and records the lookup result together with the answer.` This sentence includes tool call and lookup-result recording.

Such a design sentence already contains:

- input,
- retrieval or tool call,
- output,
- evidence or lookup result, and
- failure record.

In other words, the whole of Part 6 has been compressed into one small service sentence.

If we separate once more at this point, what the request-flow design directly decides and what the minimal implementation checks become clearer.

| Situation | What design decides directly | What the minimal implementation checks |
| --- | --- | --- |
| Question types differ | Which of prompt-centered, retrieval combined, and tool-use combined is needed | Whether that choice remains as actual output and execution record |
| Evidence and state look mixed | Whether this is an evidence-acquisition problem or a current-state lookup problem | Whether evidence document list and lookup result actually remain separately |
| Failure must not be hidden | Human-review routing, follow-up question, failure-record path | Whether human-review-needed flag, execution state, and retrospective note are actually recorded |
| Part 6 concepts feel scattered | Tie question, evidence/state, output, evaluation, and record into one request sentence | Whether that request sentence appears as actual steps in a reduced implementation |

The key in this table is that you should first decide `which request structure should be attached`, rather than `what was implemented`. The minimal implementation then checks which output and request execution record that structure actually leaves behind.

Condensed into one line, designing a small generative AI feature is not `calling a model once`. It is `choosing the structure that fits the question type, answering with evidence and state, and recording that path`.

## Checklist

- Can you explain a small generative AI feature not as `one model call`, but as a request flow of `question, evidence/state acquisition, output, evaluation, and record`?
- Can you distinguish work where a prompt alone is enough from work that needs retrieval or tools?
- Can you explain that retrieval is about evidence acquisition, while tool use is about state lookup and execution?

## Sources and References

- OpenAI, [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Retrieval](https://developers.openai.com/api/docs/guides/retrieval){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
