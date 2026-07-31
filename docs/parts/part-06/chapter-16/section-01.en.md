# P6-16.1 LLM Evaluation That Separates Natural Answers from Quality Criteria

> Section ID: `P6-16.1`
> Version: `v2026.07.31`

Separate LLM evaluation records into `answer_text`, `task_success`, `evidence_quality`, `format_quality`, `safety_issue`, and `revision_need`. This prevents a natural-looking answer and the actual quality criteria from being covered by a single score.

Even if a harness leaves execution records such as traces, tool-call logs, and replay information, those records alone do not guarantee quality. An LLM-based system needs evaluation criteria that separate `what counts as a pass`, `which axis failed first`, and `what must be fixed before trying again`.

LLM evaluation is not merely checking whether an answer sounds plausible. It checks the answer against criteria such as correctness, helpfulness, safety, groundedness, and format compliance. In other words, it is more similar to checking item by item what is good and what is still risky, rather than asking whether the answer looks good.

## Axes for evaluating LLM answers separately

The core questions are:

- Why is LLM evaluation difficult?
- What should be evaluated?
- Why should model evaluation and system evaluation be separated?

If evaluation is reduced to `one accuracy number`, failures in generative AI outputs become hard to separate. A sentence can sound natural while being factually wrong. It can cite a document while making a conclusion outside that document. It can match the requested format while still being unusable for the user's actual work. So the core change at this stage is from `did we leave a record` to `by what quality axes should we judge that record and answer`.

Evaluation rereads the records left by a harness and judges the final answer, input request, evidence documents, and output format through different questions. The same execution record produces different questions depending on why it is being read.

| Same record | Question in the P6-15 harness layer | Question in the P6-16 evaluation layer | Question read again in P6-17 operations |
| --- | --- | --- | --- |
| User request and output candidate | What was entered, and what answer came back? | Does the answer actually solve the requested task? | Which request types show unstable quality? |
| Retrieved documents and evidence paragraphs | What did the system read before answering? | Do the answer's claims match the evidence text? | Where should search range and document selection be adjusted? |
| Output format and constraints | What format was required? | Did the output follow the requested format and required items? | Where should service response rules be reinforced? |

So even for the same trace, the question changes: in the harness layer, `was it recorded`; in evaluation, `which quality axes did it satisfy`; and in operations, `which request types keep shaking`.

The first record to keep at this stage is the per-axis judgment that shows which axes passed and failed, plus the first fix axis that shows what should be corrected first.

## Separating natural answers from quality criteria

At an introductory level, you should be able to explain LLM evaluation, distinguish evaluation axes such as correctness, helpfulness, safety, and groundedness, and separate model evaluation from system evaluation. You should also be able to distinguish an answer that looks well written from quality criteria that can actually be checked.

The first scenes to separate are:

| First visible blockage | First question to ask | Why this question is needed first |
| --- | --- | --- |
| The answer reads naturally but still feels unreliable | Are the core facts and calculations actually correct? | Fluent sentences can hide weak correctness, so facts come before tone. |
| The sentence seems right, but it is hard to use immediately | Is it useful enough to finish the user's job? | A true statement and a usable answer are not always the same. |
| The answer says it used sources, but it is still hard to trust | Does the answer actually connect to the evidence text? | Groundedness can fail even when retrieval or citation exists. |
| The format is polite and correct, but the answer feels risky to release | Which axis should stop first: safety, format compliance, or helpfulness? | One answer can fail several axes at once, so format pass and safety pass must not be treated as identical. |

This table makes evaluation easier to read not as `a list of evaluation terms`, but as a standard for deciding where an answer that looks good fails first.

## Why LLM evaluation is difficult

In traditional classification problems, the correct label is often clear. In generative AI, there may not be only one correct answer, and we must look at naturalness, factuality, format, and evidence together.

- There may be more than one acceptable answer.
- A sentence can be natural while the facts are wrong.
- The content can be right while the format is inappropriate.
- The answer can look good while the evidence is weak.

So LLM evaluation often does not end with one line saying `right` or `wrong`.

This is an important difference from traditional machine-learning evaluation. In a classification problem, `was it correct` is central. In generative AI, we also need to ask `how was it correct`, and `what was correct while what was still weak`.

## What should be evaluated

The following evaluation axes should be separated first.

| Evaluation axis | Core question |
| --- | --- |
| Correctness | Are the facts and calculations right? |
| Helpfulness | Does the answer actually help the user's task? |
| Safety | Does it reduce harmful outcomes? |
| Groundedness | Is the answer connected to the given documents or evidence? |
| Format compliance | Does it follow the requested format and constraints? |

Without separating these axes, it is easy to mistake a fluent answer for an accurate and safe answer.

You can also remember the table in one line:

- Correctness asks `is it right`.
- Helpfulness asks `is it useful`.
- Safety asks `does it reduce risk`.
- Groundedness asks `where did it come from`.
- Format compliance asks `did it follow the requested shape`.

## Why model evaluation and system evaluation differ

This distinction must be set first so that when an answer fails, we can separate whether the model failed to generate a good sentence or the system path failed in search and evidence use.

LLM-based systems are usually not made only of a model. In a RAG system, for example, we need to check separately:

- whether retrieval worked
- whether the retrieved documents were read correctly
- whether the answer reflected the evidence well

In a tool-using system, we also need to check:

- whether the appropriate tool was selected
- whether the call arguments were correct
- whether the execution result was read correctly

So:

- Model evaluation is more similar to evaluating sentence generation.
- System evaluation is more similar to evaluating the whole flow, including retrieval, tools, execution, and output.

This distinction lets us diagnose whether an LLM service problem comes from sentence generation itself or from a system-path issue such as retrieval quality, tool calls, or postprocessing.

| Evaluation target | Mainly checked |
| --- | --- |
| Model | Sentence generation, format, reasoning result |
| System | Retrieval, tools, execution, full response path |

## Why one score is not enough

The immediate question is: `Can we just summarize everything with one score?` In practice, one score hides many problems.

For example:

- helpfulness can be high while factuality is low
- safety can be high while the answer is too conservative
- retrieval can be good while the final summary is wrong

So LLM evaluation is safer when it reads which axis is unstable among correctness, safety, groundedness, and format compliance, instead of covering everything with `one absolute score`.

## Why repeated comparison is needed

Evaluation is not only for academic benchmarks. It is also needed when comparing the same question set repeatedly.

- Did this deployment version improve over the previous one?
- Which question type has more failures?
- Did retrieval quality fall, or did generation quality fall?
- Did a format change affect helpfulness or groundedness?

In other words, evaluation is not a number for showing off a model. It is a standard for comparing outputs before and after a change by the same criteria.

Pulled more similar to service operation, evaluation is less like praising `one good answer` and more like repeatedly checking `what improved and what regressed on the same fixed question set`.

| Why the same evaluation set is repeated | What operation actually wants to know |
| --- | --- |
| To compare quality before and after deployment | Did this change really improve the system? |
| To see whether the same failure returns | Did a regression occur? |
| To see whether retrieval, generation, or format is unstable | Can the weak axis be narrowed down to model output or system composition? |

Evaluation is therefore both a process for choosing good-looking answers and a process for tracking regressions with a fixed question set.

Placed in the service-structure flow:

- prompts, RAG, tools, and agents are designed
- actual outputs are produced
- evaluation decides by what criteria those results will be kept and compared

Simplified once more:

```mermaid
--8<-- "assets/part-06/chapter-16/p6-c16-s01-eval-axis-flow-en.mmd"
```

The core of this figure is that evaluation does not simply say `good` or `bad` once. It finds which axis is weak and decides the next fix.

## Drawn very simply

```mermaid
--8<-- "assets/part-06/chapter-16/p6-c16-s01-eval-system-flow-en.mmd"
```

The key point of this diagram is that after an output appears, the system still needs criteria for judging whether it is acceptable.

## Cases and examples

The focus of these cases is not `does the result look good`, but `which evaluation axis fails first`.

### Case 1. Evaluating a document summary

Suppose a meeting-note summary is written in smooth sentences. At first glance, it is easy to judge it as good because it is easy to read and neatly formatted. But if key conclusions such as `deployment postponed to August 2`, `legal review required`, and `owner changed to Mina` are missing, the summary cannot be used directly in work. A good-looking sentence and preservation of important information are different evaluation axes.

For example, even if the tone is natural, a report summary is similar to failure if it omits the reason for postponement. If that summary is sent upward, the reader may know only that the schedule changed and still need to reopen the original document to learn why. The criterion changes from `is the sentence natural and readable` to `are the core conclusions and decisions preserved`. So evaluation must check `is the key information still there`, separately from naturalness.

This case matters because whether a summary `looks good` and whether it is `usable for work` often differ. Readability does not mean all information needed for decision-making remains. When the sentence is very natural, people may notice omissions even later. So evaluation should not pass an answer only by fluency; it should check the decisions and risk items that must remain from the original.

| Visible state | Easy first judgment | What evaluation must check separately |
| --- | --- | --- |
| Sentences are natural and short | `It summarized well` | Were core decisions and owner changes preserved? |
| The format is clean and numbered | `It is enough for reporting` | Are postponement reason and legal review still present? |
| It is easy to read and not repetitive | `Quality is high` | Does important-information preservation pass the minimum criterion? |

The standard to hold here is not treating `a good-looking sentence` and `a sufficient work summary` as the same thing.

### Case 2. RAG-based question answering

Suppose a RAG answer is very fluent, but adds a number or condition not found in the retrieved document. If the sentence is smooth, people tend to trust it unless they compare it line by line with the source. For example, if the document says only `basic 14 days`, but the answer adds `opened products are also eligible for 30 days`, the sentence is natural but groundedness has failed. Even if there is a citation link, groundedness fails if the cited paragraph does not actually say the condition.

If this answer is used for customer guidance, the tone may be smooth while the answer violates policy. The criterion changes from `is the answer fluent and plausible` to `does each answer condition actually align with the evidence document`. In RAG, what matters more than plausibility is whether the attached evidence really supports the answer. Evaluation should therefore check document-answer match and citation accuracy separately from the answer sentence itself.

This scene is risky because many users feel that RAG is safer once a source is attached. But groundedness is not automatically secured just because a retrieved document exists. If the answer sentence moves even a little outside the evidence document, the source link can make users trust it more, not less. So evaluation should first ask whether each claim and cited sentence actually touch.

| Answer state | How it looks from outside | What evaluation checks first |
| --- | --- | --- |
| Source link is attached | Evidence looks solid | Does the linked paragraph actually state the number and condition? |
| Sentence is natural and polite | It seems ready for customer guidance | Did it add conditions outside the document? |
| Citation format is correct | It looks grounded | Do citation accuracy and document-answer alignment pass the threshold? |

The misunderstanding to pass here is `if a source exists, groundedness exists`.

### Case 3. Evaluating format and helpfulness

Suppose a customer-guidance answer is polite and grammatical. If the tone is good, it is easy to feel that it passed. But if it omits the user's next required action, it does not finish the job. For example, in an account-lock notice, if `identity verification`, `password reset link`, and `request number to send if the problem continues` are missing, the customer must ask again even if the sentence is natural.

The criterion changes from `is the tone friendly` to `can the user take the next action`. If the format is correct but the next action is empty, format compliance may pass while helpfulness fails. So the result to check in this case is not whether the answer is polite, but whether it actually includes the required action and conditions the user can follow immediately.

The three cases can be grouped by evaluation axis like this.

| Situation | Easy-to-miss issue even when it looks good | Evaluation axis to check separately |
| --- | --- | --- |
| Document summary | Smooth sentences can omit key decisions | Key-information preservation and omission |
| RAG Q&A | A source can exist while conditions outside the document are added | Groundedness and citation accuracy |
| Customer guidance | Polite sentences can omit the next action | Format compliance and helpfulness |

## Scenes to separate first by evaluation axis

The easiest thing to miss when first reading evaluation is passing an answer immediately just because `it looks good`. Real evaluation is more similar to separating `which axis failed first` than to trusting one impression. Practical check questions look like this.

| If you suspect this | First question to ask |
| --- | --- |
| `It reads well, so is it not okay?` | Are the required information and decisions actually preserved? |
| `A source is attached, so why is it still unsettling?` | Does each claim actually match the cited sentence? |
| `The content seems right, but it is hard to use immediately.` | Are the requested format and required action instructions actually present? |
| `The tone is friendly, but is it safe to follow?` | Does it need to filter risky instructions or overconfident claims? |
| `The content is right, but the user does not know what to do next.` | Does it include an executable next action or check criterion? |

If we move directly to `which axis failed first`, the answer can be read more briefly like this.

| Judgment to leave first | Criterion for leaving it there |
| --- | --- |
| `correctness needs review` | Any number, fact, or condition conflicts with evidence |
| `groundedness needs review` | Sources exist, but the answer's claims do not actually match cited sentences |
| `format/helpfulness needs reinforcement` | The content is right, but requested format, required items, or next action are missing |
| `safety needs review` | A friendly answer still contains risky instructions or overconfident claims |

The key point is separating `looks good` from `which axis must be fixed first`. That makes it possible to label the same answer as a content error, evidence mismatch, format miss, usefulness gap, or safety problem.

The criterion to learn first is simple. Evaluation is not `choosing a good-looking answer`. It is the work of separating correctness, helpfulness, safety, groundedness, and format compliance, then deciding which axis to fix first. Execution-path cost, retries, and fallback paths are operational constraints and are handled later in P6-17.

## Practice and example

The goal of the example is to see that LLM evaluation is not one item but several axes, and to read from those results `which candidate should be accepted` and `what should be fixed first`. Looking at only one answer can easily end as `right` or `wrong`, so we place output candidates from several local LLMs side by side and check which axis separates them.

The example first sends the same small task set to lightweight local Ollama models such as `qwen2.5:1.5b`, `llama3.2:1b`, and `llama3.2:latest`, then stores the outputs in the English CSV [p6_16_1_llm_eval_outputs_en.csv](/AiBook/assets/part-06/chapter-16/p6_16_1_llm_eval_outputs_en.csv){ .csv-preview }. One row is `one model's answer to one task`. `source_excerpt` is the evidence to compare against, `required_claim_terms` are core expressions that must move from evidence into the answer, `unsupported_claim_terms` are expressions outside the evidence, `safety_risk_terms` and `safety_required_terms` are for safety judgment, `format_terms` and `helpful_terms` are observations for format and usefulness, and `model_output` is the actual model output.

The output shows a model-level evaluation report, summary values for correctness, groundedness, safety, format compliance, and helpfulness, and the first fix axis. The core thing to check in the code is that per-axis inspection does not look only at one correct-or-wrong result. It applies several criteria together: groundedness, safe guidance, format compliance, and usefulness. This rubric is a simple string-based check, so it does not replace real semantic evaluation. Its purpose is to show that even under the same input and evidence, different models can fail different axes, and those differences can be left as CSV rows and evaluation axes.

The evaluation criteria to read together are:

| Check item | Why it is needed |
| --- | --- |
| `correctness` | To check whether core claims in the evidence remain in the answer |
| `groundedness` | To check whether the answer adds conditions outside the evidence |
| `safety` | To avoid risky expressions and require protective guidance in safety tasks |
| `format_compliance` | To check whether requested format and ending conditions are followed |
| `helpfulness` | To check whether the answer includes next actions or usage information |
| `next_fix` | To decide which axis should be fixed first for a failed candidate |

The script that creates the English CSV is:

```python
--8<-- "assets/part-06/chapter-16/p6_16_1_generate_llm_eval_outputs_en.py"
```

If this script is run, it creates `p6_16_1_llm_eval_outputs_en.csv`. If Ollama and the listed models are not ready locally, this step can be skipped and the stored English output CSV provided in the repository can be used as is.

After the CSV exists, the following separate script evaluates each row. This second script does not call a local model. It reads only the existing CSV, so it runs independently from `p6_16_1_generate_llm_eval_outputs_en.py`.

```python
--8<-- "assets/part-06/chapter-16/p6_16_1_evaluate_llm_outputs_en.py"
```

The example output can be read like this.

```text
[summary]
{'all_pass_count': 9,
 'average_axis_score': 4.11,
 'axis_pass_count': {'correctness': 16,
                     'format_compliance': 10,
                     'groundedness': 17,
                     'helpfulness': 13,
                     'safety': 18},
 'case_count': 18,
 'highest_axis_score_run': 'qwen2.5_1.5b_meeting_summary',
 'model_count': 3}

================================================================================
[case]
qwen2.5_1.5b_refund_policy / qwen2.5:1.5b / policy_answer
[model_output]
Refund request handling now follows the latest policy and takes 14 days.
[evaluation]
{'axis_score': 3,
 'correctness': True,
 'failed_axes': ['format_compliance', 'helpfulness'],
 'format_compliance': False,
 'groundedness': True,
 'helpfulness': False,
 'matched_claims': ['14 days', 'latest policy'],
 'missing_safety_terms': [],
 'next_fix': 'rewrite_to_required_format',
 'passes_all': False,
 'safety': True,
 'safety_risk_hits': [],
 'unsupported_hits': []}

================================================================================
[case]
qwen2.5_1.5b_meeting_summary / qwen2.5:1.5b / summary
[model_output]
Deployment was postponed to August 2 because legal review remains. Mina will handle the follow-up check.
[evaluation]
{'axis_score': 5,
 'correctness': True,
 'failed_axes': [],
 'format_compliance': True,
 'groundedness': True,
 'helpfulness': True,
 'matched_claims': ['August 2', 'legal review', 'Mina'],
 'missing_safety_terms': [],
 'next_fix': 'accept_candidate',
 'passes_all': True,
 'safety': True,
 'safety_risk_hits': [],
 'unsupported_hits': []}

================================================================================
[case]
qwen2.5_1.5b_rag_plan_limit / qwen2.5:1.5b / rag_answer
[model_output]
Basic plan supports up to 5 projects and SSO is available on Enterprise plans or higher.
[evaluation]
{'axis_score': 4,
 'correctness': True,
 'failed_axes': ['groundedness'],
 'format_compliance': True,
 'groundedness': False,
 'helpfulness': True,
 'matched_claims': ['5 projects', 'Enterprise', 'SSO'],
 'missing_safety_terms': [],
 'next_fix': 'remove_claim_not_supported_by_source',
 'passes_all': False,
 'safety': True,
 'safety_risk_hits': [],
 'unsupported_hits': ['or higher']}
```

The first thing to notice is that the pass counts inside `axis_pass_count` differ by axis. Three models received the same evidence and the same requests, but some outputs miss part of a core claim, some add a condition wider than the source, and some fail format or helpfulness. If evaluation were only one score, these differences would quickly disappear.

![LLM evaluation axis pass check](/AiBook/assets/part-06/chapter-16/llm-eval-axis-check-en.png)

This chart shows that the number of candidates passing all criteria and the number passing each axis are different. The fact that the bars are not all the same height matters. LLM outputs do not split once into `good` and `bad`; one output can pass correctness but fail format, or stay within evidence while still lacking helpful next-action guidance.

The result to check in this example is that several LLM output candidates can be judged separately by axes such as correctness, groundedness, safety, format compliance, and helpfulness. Evaluation does not end with one score.

Readers can try these adjustments in the example.

- Run `p6_16_1_generate_llm_eval_outputs_en.py` to regenerate the same tasks with the currently installed Ollama models.
- Change the `MODELS` list in the generation script and see how smaller and larger models fail different axes.
- Adjust `required_claim_terms`, `unsupported_claim_terms`, `safety_risk_terms`, `safety_required_terms`, `format_terms`, and `helpful_terms` to see how correctness, groundedness, safety, format compliance, and helpfulness judgments split.

## Fix directions separated by evaluation axis

The previous example is not code for creating a score table. It is a small scene that shows `several output candidates for the same question must be read differently by axis`. The important point is not adding another case, but learning to read evaluation as several check axes and batch comparisons instead of one score.

The core points are:

- even if the output sentence is one sentence
- review questions can be several questions
- so evaluation is more similar to an itemized checklist than to one-line judgment

In one sentence, LLM evaluation is not `assigning one score`; it is `a comparison standard for deciding which candidate to accept and which axis to fix first`.

In the service stage, we must distinguish more directly `which criteria are satisfied`, not just `does it speak well`. Evaluation is therefore better read as a comparison standard for deciding which candidate to accept and which axis to repair first, rather than as an impression of the output.

This evaluation standard matters because it:

- checks whether tool connections and execution structures are actually producing good answers by quality axis
- makes evaluation a standard for fix priority, not a boast about model performance
- prepares the next section to divide the same evaluation axes between automatic checks and human review
- creates criteria that will later be used to verify results

## Checklist

- You should be able to explain evaluation not as `checking one accuracy rate`, but as `separating pass and failure across several quality axes`.
- You should be able to say that separating model evaluation from system evaluation helps narrow down the cause of the same failure more accurately.
- You should not treat a natural answer and checkable quality criteria as the same thing.

## Sources and Further Reading

- OpenAI, [Working with evals](https://developers.openai.com/api/docs/guides/evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-19.
- Yuzheng Chang et al., [A Survey on Evaluation of Large Language Models](https://arxiv.org/abs/2307.03109){: target="_blank" rel="noopener noreferrer" }, arXiv, 2023, accessed 2026-07-19.
