# P6-10.2 Limits That Move Freshness, Grounding, and Execution Outside Prompts

> Section ID: `P6-10.2`
> Version: `v2026.07.26`

In P6-10.1, we saw that prompt engineering is the first practical tool for observing and adjusting model behavior through input design. Now we need to look more directly at what remains even when prompts are written well.

A prompt is a strong tool for guiding model responses, but it is not a tool that solves freshness, factuality, evidence guarantees, and long-term consistency by itself.

## Problems That Do Not Close with Input Adjustment Alone

- What problems are difficult to solve with prompts alone?
- Why can prompts that look good still be insufficient in real services?
- At what point do RAG, fine-tuning, tool use, and evaluation systems become necessary?

The core of prompt limits is the standard that separates `input adjustment` from `problems that require changing the system structure`. Freshness and evidence problems belong to RAG, which changes the starting point of the answer to external documents. Execution problems belong to tool use and function calling. Repeated judgment belongs to evaluation structures.

To avoid overvaluing prompt engineering, the question needs to move from `how should we ask?` to `what problem remains even if we ask well?`

The impression that must change first is not `write the prompt more strongly and it will be solved`, but the understanding that `input adjustment and system-structure guarantees are different layers`.

When reading prompt limits, it is more stable to also ask `what should be attached next?`

| Remaining problem | Is revising the prompt enough? | Structure to attach next first | Why the structure changes |
| --- | --- | --- | --- |
| Answer format and length often drift | Sometimes yes | Prompt improvement or instruction-format adjustment | It may still be solvable at the input-design layer. |
| Latest policies or current-version documents are needed | No | RAG, latest-document connection | The starting point of the answer must move to external documents. |
| Real actions such as calculation, saving, or lookup are needed | No | tool use, function calling | Real execution results are needed, not only words. |
| The same failures must be checked repeatedly and passing criteria set | No | evaluation, harness | Execution records and judgment structures are needed more than response sentences. |

In short, writing a stronger prompt is `input adjustment`, while moving to RAG, tool use, and evaluation is `a choice to change the system structure`.

What should be kept first here is failure-type notes, format-drift statistics, and reproducibility failure records that show which problem is an input-adjustment limit and which problem is missing evidence connection.

This record is needed so that the move to P6-11.1 RAG necessity judgment does not become shaky, and so that problems reducible by prompt improvement can be separated from problems that require changing system structure.

Later, this record is read again as evaluation standards in P6-16 and as review memos, improvement plans, and project records for Part 6.

## Separating Input Adjustment from System-Structure Guarantees

- You can explain prompt limits at an introductory level.
- You can say why freshness, factuality, consistency, and executability problems remain.
- You can distinguish problems to solve with prompts from problems that require changing structure.
- You can read the need for RAG not as `writing a longer prompt`, but as an `evidence-connection structure`.

The scenes to separate first are cases where format is roughly right but latest facts are unstable, cases where the answer is plausible but sources are hard to trust, cases where actions such as calculation, saving, or lookup are needed but only the answer sentence improves, and cases where the same failure repeats but the cause is hard to compare.

At that point, the question should not be `should we write the prompt more strongly?`

It should be `what is missing among latest-document connection, actual evidence, execution structure, and evaluation records?`

With this distinction, prompt limits can be read more directly as `the standard for separating problems reducible by input adjustment from problems that require changing structure`, rather than as `stronger wording tips`.

## Why Prompts Are Powerful but Incomplete

A prompt is a tool for designing input. It can therefore draw out the model's existing abilities better or make a format more stable. But input design alone cannot solve every problem outside the model.

For example, prompts can be strong for:

- adjusting answer length
- controlling format
- inducing patterns from examples
- adjusting tone

By contrast, prompts alone do not automatically solve the following.

- reflecting latest information
- guaranteeing evidence from external documents
- querying a database
- verifying calculation results
- reproducibility of long workflows

## Freshness Problems

A model does not automatically know information that appeared after training. Even if a prompt is written more carefully, it cannot reliably guarantee latest facts that the model has never seen.

Therefore, the prompt `Answer based on the latest information` is only a request. It does not replace a connection to external latest data.

This is where RAG or tool use becomes necessary.

## Factuality and Evidence Problems

Even if the prompt says `explain with evidence`, the model may not have actually retrieved an evidence document. It can generate a plausible explanation, but there is no guarantee that the answer is connected to a real source.

In other words:

- a prompt asking for evidence
- a system connected to actual evidence documents

are not the same thing.

Without this distinction, users can mistake an `answer that looks like it has a source` for a `verified answer`.

## Consistency and Reproducibility Problems

If a prompt changes slightly, temperature changes, or context order changes, the output can change. So prompts alone make very strict reproducibility hard to guarantee.

In practice, this appears as follows.

- The same request produces drifting expressions.
- Classification labels differ subtly.
- Table format sometimes breaks.
- Standards change front to back in a long task.

Prompt improvement can reduce these problems, but it is hard to remove them completely.

## Execution and Action Problems

A prompt is basically text input. Therefore, actions such as:

- real database lookup
- external API calls
- file modification
- saving calculation results

do not happen with prompts alone. These stages require tool use, function calling, and AI agent structures.

In short, a prompt can express an `action request`, but it is not the action-execution structure itself.

This transition becomes clearer when connected directly to the next structural choices. If latest information is missing, RAG or latest-document connection is needed. If real actions such as calculation and saving are needed, tool use or function calling is needed. If the same failure must be compared and filtered repeatedly, repeated judgment structures such as evaluation and harness are needed.

So prompt limits do not close only by `writing a stronger prompt`. From the viewpoint of external comparison standards, this is where the work changes from `input adjustment` to choosing which of `evidence connection`, `execution connection`, and `repeated evaluation` should be attached first.

The same transition can be diagnosed more briefly as follows.

| First question | If yes, check first | If no, check first |
| --- | --- | --- |
| Is the shortage about speaking style and format? | Readjust prompt instructions, context, and examples. | Check what is missing among latest evidence, execution, and evaluation structure. |
| Is the shortage about latest documents and current evidence? | Check RAG and latest-document connection first. | Check whether execution or repeated evaluation is more important. |
| Is the shortage about actual lookup, calculation, or saving? | Check tool use, function calling, and execution-log structure first. | Check whether repeated judgment and regression detection are larger problems. |
| Is the shortage about repeated judgment and regression detection? | Check evaluation, harness, and fixed evaluation sets first. | Check again whether the drift can be reduced at the prompt layer. |

## Drawn Very Simply

```mermaid
--8<-- "assets/part-06/chapter-10/p6-c10-s02-prompt-limit-flow-en.mmd"
```

The key of this diagram is that prompt improvement matters, but it does not solve every structural problem by itself.

## Cases and Examples

### Case 1. Latest Policy Guidance

Imagine a user asking, `How many days is the refund period from today?` It is easy to expect that a more elaborate prompt such as `answer accurately and carefully` will reduce the freshness problem. But if the latest policy source is not included in the input, the model can state an old standard. People are more likely to trust an answer if it sounds careful and confident, but the core that is easy to miss in this scene is not the answer attitude. It is `did the system access the current document?`

Without latest-document connection, a polite wrong answer can go out as operating guidance. The change here is a move from checking `is the tone careful?` to checking `is the latest document evidence actually attached?`

In this case, the problem is not that the prompt is weak. It is that the structure connecting latest information is missing.

The result to check in this case is not tone, but whether the latest document evidence is actually attached, and whether the document ID alone lets us recheck that it is the current version.

This case is a real operating scene because policy guidance requires `the currently effective answer`, not `the most plausible answer`.

Customer support, internal HR rules, shipping policies, and refund conditions do not end just because the sentence is natural.

The user asks about clauses that apply today, and the operator must be able to trace which document version the answer came from. So no matter how carefully the prompt sentence is refined, if latest-document connection is missing, the system remains only `an assistant that speaks old patterns well`.

The difference becomes clearer when the same question is compared as follows.

| Same question scene | What is easy to miss when checking only prompts | What to check after attaching structure |
| --- | --- | --- |
| `How many days is the refund period from today?` | Whether the answer sentence is careful and natural | Whether the latest policy document was actually retrieved |
| `I heard the rule changed this week. Is that right?` | Whether the model carefully says `it may have changed` | Which notice document version supports the answer |
| `Tell me the exception clauses too` | Whether the answer is long and kind | Whether the main clause and exception clause are attached in the same evidence bundle |

The core of this comparison is that `an answer that speaks more carefully` and `an answer bound to the current document` are different layers.

The misunderstanding corrected here is the expectation that `careful wording also solves the freshness problem somewhat`.

In reality, the first work that reduces freshness problems is not prompt micro-adjustment, but attaching current-document retrieval and evidence-marking structure.

### Case 2. A Report Where Numerical Calculation Matters

Suppose we automatically write a weekly sales report. It is easy to expect that adding `calculate the numbers accurately and organize them in a table` to the prompt will improve calculation accuracy. But if actual totals and growth rates are trusted without a calculation tool, small arithmetic errors can enter the report. People can easily feel that the report is `accurate-looking` if the table format is right and the sentences are smooth.

What this scene needs is not a stronger sentence, but a structure that checks the numbers again, such as a calculator or post-processing verification.

If even one calculation cell is wrong, the following interpretation sentence and decision can be wrong together.

The change here is a move from checking `does the table look plausible?` to checking `do the original numbers, totals, and growth rates actually match?`

This reveals that the prompt `be accurate` and a `structure that guarantees accuracy` are different problems. The result to check in this case is whether totals, growth rates, and original numbers match each other more than whether the table sentence is smooth, and whether that match can be inspected again through calculation logs or verification records.

In actual report automation, one wrong number does not end at one wrong sentence. It can disturb judgments and actions in the next meeting. Especially for connected metrics such as sales, inventory, ad spend, and conversion rate, if one item is wrong, the later interpretation chain can be wrong as a whole. So operators should check `where did this number come from, what calculation did it pass through, and is it the same if recalculated?` before asking whether the table looks nice.

For example, if weekly sales report automation is divided as follows, the difference between prompt and structure becomes clearer.

| Report stage | Risk often remaining with prompts alone | What to check after attaching structure |
| --- | --- | --- |
| Reading source numbers | A sentence may look plausible even if the wrong CSV or table column was interpreted | Which source row and column were read |
| Calculating totals and growth rates | Small arithmetic errors can propagate into tables and explanation sentences | Whether calculation logs and recalculation results match |
| Generating interpretation sentences | A natural conclusion can be written from wrong numbers | Whether interpretation sentences reference only verified numbers |

The important standard in this case is that the instruction `calculate accurately` does not mean `accuracy is guaranteed`. Calculation problems split by whether a verification structure exists, not by how strongly the instruction is written. So in practice, before refining the prompt at length, we should first check whether a calculator is attached, whether intermediate totals remain in logs, and whether source and result numbers can be matched again.

### Case 3. Repeated Work Automation

Suppose an operations team wants automation that `reads uploaded files, classifies them, and saves them into folders`. If the request sentence is specific enough, execution can feel almost solved. But with a prompt, we can write reading, classification, and saving in one sentence, while in the actual system, file access permission, classification standards, save location, and retry on failure are separate stages.

In the real world, permissions and tool connections matter more than words. If there is no permission or the save path is wrong, the task can break at the final save stage even if classification itself is correct. In other words, a human can say it in one line, but the execution world requires several tools and applications to be attached. The change here is a move from checking `is the request sentence specific?` to checking `are actual save success, failure handling, and retry structure present?` What is missing in this scene is therefore not a longer prompt, but the execution structure itself. The result to check in this case is not classification sentence generation, but whether there is actual save success, failure handling, and retry path, and whether logs let us reread which stage failed.

The three cases can be grouped again from the perspective of structural limits.

| Situation | What stronger prompting does not fill | Structure that must actually be attached |
| --- | --- | --- |
| Latest policy guidance | Access to latest information | RAG or latest-document connection |
| Numerical calculation report | Guaranteed arithmetic accuracy | Calculation tool, post-processing verification |
| Repeated work automation | File access, saving, retry | tool use, permission handling, execution flow |

The same content can be read again by system boundary as follows.

```mermaid
--8<-- "assets/part-06/chapter-10/p6-c10-s02-system-boundary-en.mmd"
```

The key is that `stronger sentences` and `stronger system guarantees` are different layers.

The conclusion up to this point is that `writing prompts better` and `binding answer evidence to actual documents` are different. From P6-11, we follow exactly this difference and read `where the answer should start`, not only adjustment of speaking style.

## Scenes That Need Structure Outside Prompts

The most common reason real failure scenes get stuck is that several causes are mixed together inside one sentence, `the answer is strange`. After reading this Section, we need the habit of first writing down `what was missing and caused this failure`.

| Problem first observed | Question to attach first | What to fix first |
| --- | --- | --- |
| Answer tone and format drift often | Does the way of answering drift with the same material? | Prompt structure, examples, output format |
| Today's-policy answer remains unstable | Did the system actually read the current document? | RAG, latest-document connection |
| We are not sure the calculation is correct | Can the calculation process be checked again? | Calculation tool, verification log |
| We do not know whether save, lookup, or send actually finished | Are there execution records, not only words? | tool use, function calling, execution log |

The key of this table is not to treat `write the prompt more strongly` and `attach another structure to the system` as the same improvement. Format drift can be reduced at the prompt layer, but missing latest documents or missing execution records do not close by refining the input sentence.

If we hold this standard and move to P6-11, we will not misunderstand RAG as an `expanded prompt`. The feeling that `making the model speak better` and `binding the answer's starting point to external evidence` are different layers must be fixed here first. Then the retrieval-evidence combination in P6-11 can be read with much less compression.

## Exercise and Example

The goal of this exercise is to judge directly that a `strong prompt` and `actual structural guarantee` are different problems. In real services, we should not read only the answer sentence. We should also check verification items such as `was the latest document attached?`, `is there a calculation log?`, and `was an execution log left?`

Users can expect latest policy, accurate calculation, and actual save execution all at once. In the prompt, we can strongly write `based on the latest document`, `calculate accurately`, and `complete saving`, but if there is no latest-document connection, calculation tool, or saving tool, the answer can still end as a word-only instruction.

First, the verification items to compare can be summarized in a table.

| Task | What the user expects | What prompts alone often miss | Structure to attach |
| --- | --- | --- | --- |
| Policy guidance | Answer based on latest documents | Latest-version document ID | Document retrieval, latest-version connection |
| Numerical report | Accurate calculation values | Calculation log, recalculation evidence | Calculation tool, post-processing verification |
| File automation | Actual save completion | Save log, retry information | File tool, execution log |

In the three scenes below, the first work is not calculating an answer, but marking which slot is empty and needs structure outside prompts.

| Scene | What prompts can reduce first | What needs system structure | Record to check |
| --- | --- | --- | --- |
| The model politely answered 7 days when asked `Tell me today's refund period` | Answer length, tone, caution phrase | Currently effective policy document connection | Document ID, document version, retrieval time |
| The table looks nice but the total is wrong when asked `Tell me the total and average sales for three branches` | Table format, explanation order | Calculation tool and verification structure | Source rows, calculation log, recalculation result |
| The model said it saved the contract to the legal folder when asked `Save the contract to the legal folder` | Report sentence format | Actual file-save tool and permission handling | Save path, save log, retry record on failure |

Now make the same scenes a little more ambiguous and judge them directly. In the blanks, write the first structure to check among `prompt`, `RAG`, `tool use`, and `evaluation/log`.

| Failure scene | Structure to check first | Reason |
| --- | --- | --- |
| The answer comes from the latest document, but the summary format differs every time |  |  |
| The total number is correct, but there is no record of which source rows were calculated |  |  |
| File saving succeeded, but we do not know whether retry would happen on failure |  |  |
| The answer is natural and the table is correct, but the policy document version is from last month |  |  |

Explanation:

| Failure scene | Structure to check first | Reason |
| --- | --- | --- |
| Latest document is attached, but summary format drifts | prompt | Evidence connection exists, so first fix output format and examples |
| Total is correct, but source-row record is missing | evaluation/log | Even if the calculation result is correct, operation verification is hard without reproducibility records |
| Save succeeds, but retry is unknown | tool use | Execution structure includes not only success but also failure handling and retry paths |
| Table and sentences are good, but document version is old | RAG | The problem is not tone or format, but that the answer's starting point is not bound to the current document |

What this exercise should confirm is that `write a strong prompt` and `attach structure` are not the same judgment. Prompts are strong at changing answer shape, but latest document version, calculation reproducibility, save success, and failure-handling records can only be checked with separate structures.

## Failure Types That Remain at the System Boundary

This exercise prevents the misunderstanding that every problem is solved as prompts become stronger. In real services, outside structures such as latest-information access, calculation verification, tool calls, and execution logs are separately needed, so prompts should be read as only one layer of the whole system.

What matters in the judgment table above is that structural support is not one universal device. Freshness moves to evidence connection, calculation moves to verification structure, saving moves to execution tools and logs, and repeated failure detection moves to evaluation records. Therefore, prompt limits should be read not as `tone problems`, but as `what is missing among evidence, calculation, execution, and evaluation structures`.

## Boundary That Moves Outside Prompts

Prompts are strong at changing response shape, but system guarantees such as latest-document access, calculation verification, and real execution success can only be secured with separate structures.
