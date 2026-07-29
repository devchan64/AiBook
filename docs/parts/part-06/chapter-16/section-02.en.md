# P6-16.2 Division of Work Between Automatic Evaluation and Human Evaluation

> Section ID: `P6-16.2`
> Version: `v2026.07.26`

_Subtitle: How are repeated checks and contextual judgment divided between automatic evaluation and human evaluation?_

Once LLM evaluation axes are set, the next standard is deciding not to handle every evaluation in the same way. Items that can be checked mechanically and repeatedly, such as format errors, are easy to send first to automatic evaluation. Items that need contextual judgment, such as interpretation, nuance, and actual helpfulness, still need human evaluation.

Automatic evaluation is fast and repeatable, while human evaluation is better at context and quality sense. In real operations, the two are often used together. The evaluated target here is not the internal LLM algorithm, but the actual output produced by the model, such as answers, summaries, and guidance messages.

This also connects back to why we covered harnesses and MCP earlier. Output candidates, inputs, evidence documents, and tool-call records must remain so automatic evaluation can repeatedly check the same conditions and humans can later reread the same run. In other words, evaluation division of work is an operational structure for treating LLM outputs as reviewable service records.

## Division of work between automatic and human evaluation

The core questions are:

- What is automatic evaluation strong at?
- What still requires human evaluation?
- Why do structures that mix both often appear?

The core is not `is automatic evaluation better, or are people better`. Even for the same output, some items are first marked for correction by an automatic grader, while other items move to a human review queue. Evaluation division of work moves away from one person reading the whole quality judgment end to end. It automates repeatable checks and leaves ambiguous judgments as review packets that people can read.

| Evaluation item | Easier for automatic evaluation | What human evaluation must still leave |
| --- | --- | --- |
| Format compliance | JSON format, required fields, length limit, source presence | Whether the reading order is actually natural even though the format is valid |
| Groundedness | Source link, citation location, banned unsupported-expression detection | Whether the cited sentence actually supports the answer's conclusion |
| Helpfulness | Required item presence, next-action wording | Whether the user can actually understand the next action |
| Safety | Banned expressions, risky keywords, policy-violation candidates | Whether contextual misunderstanding or overconfidence remains |

So the central question is `how should the same evaluation axes be divided between automatic graders and human review`.

## Separating repeated checks from contextual judgment

You should be able to explain the difference between automatic evaluation and human evaluation, distinguish repeatability from contextual judgment, explain why operations mix the two, and split evaluation results into candidates that need automatic fixing and candidates that need human review.

Rather than memorizing long definitions, it is safer to use the standard of why the same answer branches into `stopped first by an automatic grader`, `sent to a human review queue`, or `left as a review packet`.

| First visible answer state | Following evaluation route | Why the route splits this way |
| --- | --- | --- |
| Format error, missing required field, basic criterion failure | Automatic fix needed | This is a mechanical failure to fix before a person reads the full answer. |
| Format is valid, but interpretation, nuance, or risk judgment is ambiguous | Human review queue | Automatic checks alone cannot fully read misunderstanding risk and helpfulness. |
| Automatic criteria pass, but contextual judgment remains | Human review packet | The output candidate and review questions must be bundled so a person can reread it in context. |

This table makes evaluation division easier to understand as a branching structure of `where should this candidate stop and where should it go`, not as a comparison of who is better.

## What automatic evaluation is strong at

Automatic evaluation is usually strong at:

- fast repetition
- comparing many samples
- detecting regressions
- checking format
- checking items with clear criteria

For example, it is good for checking:

- whether JSON format is valid
- whether required fields exist
- whether retrieved document sources are attached
- whether a certain score became worse than the previous version

`Automatic evaluation is strong at repetition and comparison.`

## What human evaluation is strong at

Human evaluation is usually strong at:

- understanding context
- judging subtle quality differences
- noticing awkward expressions
- judging real work fit
- judging social risk and misunderstanding potential

For example:

- the answer is formally valid but actually creates misunderstanding
- the explanation is fluent but does not fit the reader level
- evidence exists, but the wording is too categorical

These are easy to miss with automatic evaluation alone.

`Human evaluation is better at context and nuance.`

## Why automatic evaluation alone is not enough

Automatic evaluation is strong when criteria are clearly defined, but it is hard for it to replace all quality judgment.

For example, automatic evaluation can often check:

- whether a specific keyword exists in a document
- whether a format constraint was followed
- whether a score crossed a threshold

But it has limits in judging:

- whether the answer is actually trustworthy and usable
- whether the wording can mislead the user
- whether it fits the organization's real purpose

## Why human evaluation alone is also not enough

If evaluation relies only on people, other problems appear.

- It is slow.
- It is costly.
- Standards can differ across reviewers.
- It is hard to repeat frequently.

Human evaluation has depth, but as operations scale, it is hard to sustain without automation.

## Why both are used together

In practice, the two are usually mixed like this.

- Automatic evaluation first catches large-scale regressions and format errors.
- Human evaluation checks important samples and subtle quality issues.
- Automatic criteria are reinforced again when needed.

Automatic evaluation and human evaluation are therefore closer to a division of work than to replacements for each other.

In operational flow, this division can be read more briefly like this.

| Evaluation route checked first | What it catches best | Where it goes next |
| --- | --- | --- |
| Automatic grader based on a fixed evaluation set | Regressions, format errors, basic groundedness signals | Human review or automatic-fix-needed state |
| Human review | Ambiguous interpretation, nuance, actual helpfulness, high-risk samples | Fix, hold, or approve decision |

Automatic evaluation is strong at `repeated comparison`, and human evaluation is strong at `interpreting ambiguous candidates and high-risk samples`. This is why practical external curricula often keep automatic evaluation sets and human review together.

Before and after deployment, the same questions can be run through an automatic evaluation set to find regressions and format errors first, while human evaluation checks whether those changes matter to real user experience. Automatic evaluation is a broad filter, and human evaluation interprets the meaning of the remaining candidates.

Simplified once more:

```mermaid
--8<-- "assets/part-06/chapter-16/p6-c16-s02-auto-human-routing-en.mmd"
```

The key point in this figure is that automatic evaluation does not finish all judgment first. It reduces the candidates that need human review and helps decide final action faster.

## Drawn very simply

```mermaid
--8<-- "assets/part-06/chapter-16/p6-c16-s02-eval-decision-flow-en.mmd"
```

The key point of this diagram is that actual quality judgment does not end through only one path.

Another important point is that automatic and human evaluation results become inputs to operational judgment. The end of evaluation division is not simply `quality judgment complete`; it is closer to a state where candidates have been sorted into continue or stop paths.

| Judgment left by evaluation division | Question read again in operations |
| --- | --- |
| Whether the automatic grader passed | Can this candidate move to full human reading? |
| Whether human review is needed | Which path should it move to: fix, hold, or approval? |
| Human review packet | What questions should a person use when rereading it? |
| Failure or review reason | Which cause should failure handling trace first? |

Automatic and human evaluation are not procedures that simply say `good` or `bad`. They are baselines for splitting candidates into operational routes.

## Cases and examples

The focus of these cases is not `what is correct`, but `which failures are filtered automatically and which failures must be read by people to the end`.

### Case 1. Evaluating RAG answers

Suppose a RAG answer includes both a source link and a cited span. If links and format are attached well, it is easy to feel first that `there is evidence`. Automatic checks can quickly confirm `is there a source` and `is the format valid`, but a link does not mean the answer actually reflects the document's meaning. For example, the document may contain an exception clause while the answer reads only one main sentence and states `always possible`.

In that case, automatic checks may pass while the actual user guidance is wrong. This interpretation error appears only when a person reads the document and answer together. Automatic evaluation checks `is evidence attached`, while human evaluation checks `was the evidence read correctly`. The criterion changes from `is there a source link` to `does the source actually support the interpretation`.

This matters in real operations because passing automatic checks can create too much comfort. If links and citation formatting are present, many teams first feel that the answer is grounded. But what automatic checks see well and what people must read to the end are different. Automatic checks filter surface structure quickly, while exception interpretation and contextual overstatement require reading the source and answer together.

| Answer state | What automatic evaluation can see first | What human evaluation must read to the end |
| --- | --- | --- |
| Link and citation format both exist | Source presence, format pass | Is there no categorical claim that omits an exception clause? |
| Cited paragraph exists | Paragraph reference is not empty | Does the paragraph actually support the answer condition? |
| Answer is natural and short | Length and format are fine | Did shortening remove a key limitation? |

The misunderstanding this table corrects is expecting that if a source link exists, the interpretation is also mostly correct.

### Case 2. Evaluating AI agent execution records

Even if an AI agent produced a final answer, the execution record may contain signals such as repeated search, failed tool calls, or repeated reads of the same document. Automatic evaluation can quickly mark whether these signals exist. But whether the signal is actually a problem or a necessary confirmation step requires a person to read the record together.

For example, if similar searches are repeated several times even after enough documents were found in the first search, automatic evaluation can leave a `repeated call` signal. But whether that repetition was an unnecessary detour or a needed recheck of ambiguous evidence depends on the execution flow. The criterion changes from `did a final answer appear` to `does the automatic signal become a human-review question`.

The result to check in this case is not cost calculation or operation optimization itself. That judgment is handled more directly in P6-17's operational constraints. Here, we only need to hold the division of work: automatic evaluation first gathers abnormal signals from the execution record, and human evaluation rereads those signals in context.

| Execution record state | Signal automatic evaluation catches well | Question human evaluation should ask next |
| --- | --- | --- |
| Similar searches are repeated | Repeated-call signal | Was it necessary evidence checking or an unnecessary detour? |
| Failed tool call remains | Failure signal | Did it repeat the same failure or recover through another path? |
| Final answer exists | Success flag | Did success hide intermediate risk signals? |

The important standard is not closing evaluation with only `success/failure`. Automatic evaluation gathers abnormal signals, and human evaluation interprets whether those signals are actual quality problems.

### Case 3. Customer-support answer

Suppose a customer-support answer is fast, has no banned terms, and follows format. It is easy to feel that if automatic evaluation passed everything, it is almost enough. But if the actual sentence sounds too cold or shifts responsibility to the customer, service quality can still be poor. Conversely, even if the sentence is polite, the customer can still be confused if the action order is awkward.

For example, if the answer explains the document-submission route for a long time before saying whether a refund is available, the facts may be right but the customer may still not understand the answer. This does not show up well in format checks; people need to read it. In customer-support scenes, automatic evaluation is a basic guardrail, while human evaluation checks misunderstanding risk and tone quality.

| Situation | Good target for automatic evaluation first | What human evaluation must read to the end |
| --- | --- | --- |
| RAG answer evaluation | Source presence, format match, citation notation | Was the exception clause interpreted correctly? |
| Agent execution record | Repeated-call signal, failure signal, success flag | Is the signal a real quality issue or a necessary contextual check? |
| Customer-support answer | Banned terms, format, length, response speed | Tone, misunderstanding risk, next-action clarity |

## Scenes where automatic and human evaluation should split

A common misunderstanding is leaning to one side: `automatic is better because it is faster`, or `humans are more accurate, so automation matters less`. In real operations, the core is separating `what should be filtered automatically first` from `what must be left to people to the end`.

| If you suspect this | First question to ask |
| --- | --- |
| `Does a person really need to see this?` | Can it be repeatedly checked by an automatic grader, like format, length, or source presence? |
| `Automatic checks passed, so why is it still unsettling?` | Did a person reread nuance, misunderstanding risk, and actual helpfulness? |
| `Why do some answers get fixed immediately while others go to people?` | Is the boundary between automatic-fix-needed and human-review-queue defined? |

The standard to learn first is simple. Automatic evaluation is stronger at quickly filtering `repeatable surface criteria`; human evaluation is stronger at judging `ambiguous interpretation and actual helpfulness` to the end. In operation, they should be read as division of work, not competition.

## Practice and example

The goal of the example is to see that automatic evaluation and human evaluation have different roles through different check items. Instead of looking at one answer, we compare several LLM output candidates and ask `what does automatic evaluation stop first through repeated checks` and `what moves to a review packet for a person to read`.

The example uses the English evaluation-routing candidate CSV [p6_16_2_eval_routing_cases_en.csv](/AiBook/assets/part-06/chapter-16/p6_16_2_eval_routing_cases_en.csv){ .csv-preview }. One row is one LLM output candidate that can appear in operation. `model_output` is the candidate answer, and `source_marker`, `required_action`, `format_marker`, `max_length`, and `banned_terms` are criteria the automatic grader checks repeatedly. The CSV does not contain prewritten human risk labels or answer labels.

The automatic grader names continue from P6-16.1's evaluation axes. `source_marker_grader` maps to groundedness, `required_action_grader` maps to helpfulness, `format_grader` and `length_grader` map to format compliance, and `banned_terms_grader` maps to safety. This mapping also appears in the code's `GRADER_AXIS_MAP`.

The output shows code-grader results for each candidate, optional LLM-as-a-judge results, human review packets, and a routing summary. The key point in the code is that it does not let code replace human evaluation. The code first checks repeatable surface criteria and then creates candidate sentences plus review questions for candidates that pass.

The local LLM judge is attached only to sample candidates when Ollama is running. Ollama is not used here to teach a specific product workflow; it is only a local way to show that an LLM can also be attached as one type of automatic grader. The prompt passed to the LLM judge stays in English and includes code-grader signals such as `required action exists` and `banned expression absent`. This keeps the LLM judge from looking like a replacement for human evaluation. It should be read as a supporting automatic grader that refers to repeatable check results.

The operational judgment criteria to read together are:

| Check item | Why it is needed |
| --- | --- |
| Automatic grader pass status | To see whether basic guardrails such as format, length, evidence hint, and banned terms pass first |
| Automatic grader fix note | To separate mechanical fixes needed before human review |
| Human review packet | To let people read evidence interpretation, helpfulness, tone, and omissions even after automatic pass |
| Automatic-fix-needed status | To separate mechanical failures before people read the answer |
| Routing summary | To clearly record how automatic-fix-needed and human-review queues split |

```python
--8<-- "assets/part-06/chapter-16/p6_16_2_eval_routing_cases_en.py"
```

The example output can be read like this when the optional local LLM judge is disabled or unavailable.

```text
[summary]
{'auto_fail_count': 20,
 'auto_pass_count': 16,
 'automatic_fix_first_count': 20,
 'case_count': 36,
 'human_review_queue_count': 16,
 'route_count': {'fix_with_automatic_grader_first': 20,
                 'human_review_queue': 16}}
[llm_grader]
{'available': False,
 'enabled': False,
 'model': 'llama3.2:latest',
 'note': 'Only sample cases call the optional local LLM judge to keep the '
         'example short.'}

================================================================================
case_001 / refund
automatic_grade = 1.0
auto_pass = True
grader_scores =
{'banned_terms_grader': 1.0,
 'format_grader': 1.0,
 'length_grader': 1.0,
 'required_action_grader': 1.0,
 'source_marker_grader': 1.0}
grader_fix_note = -
llm_grader =
{'available': False,
 'model': 'llama3.2:latest',
 'reason': 'Local LLM judge is disabled or not running, so this optional '
           'grader was skipped.',
 'score': None}
llm_grader_alignment = The LLM judge was not used in this run.
human_review_packet =
{'automatic_grade': 1.0,
 'candidate': 'The refund request handling time is 14 days. Based on the '
              'notice please send the order number so we can help with intake.',
 'first_focus': 'The automatic graders passed. A person now reads context, '
                'usefulness, and tone to the end.',
 'rubric': ["Does the source signal actually support the answer's conclusion?",
            'Can the user immediately understand the next action?',
            'Is the tone or overconfidence risky in context?',
            'Did the answer omit an important condition or exception while '
            'shortening?']}
route = human_review_queue
```

The first thing to notice is that the code does not imitate human judgment. A candidate such as `case_002`, which is missing the required next action, and a candidate such as `case_007`, which includes a banned expression, stop at the automatic grader before human review. By contrast, a candidate such as `case_001`, which passes repeated check criteria, is not approved immediately. It moves to the human review queue with a packet that a person can read.

Another value to watch is `reason_source` when the optional LLM judge is available. If `reason_source` is `llm`, the local LLM judge produced the reason directly. If it is `code_grader_fallback`, the LLM judge's reason was empty or weak, so code-grader observations reinforced the reason. This distinction matters because the LLM judge itself is also something to review. Automatic grading does not end with one LLM judgment; it records code-check signals and LLM-judge signals together and leaves room for conflict.

![automatic and human evaluation routing](/AiBook/assets/part-06/chapter-16/auto-human-eval-routing-en.png)

This chart shows that the first row splits candidates into automatic-grader pass and fail, while the second row sends failed candidates to automatic fix and passed candidates to the human review queue. An `automatic pass` is therefore not an approval result. It is an intermediate state organized so a person can read further.

The same result can be grouped briefly by operational route.

| Candidate | First visible state | Why it goes this route | Follow-up action |
| --- | --- | --- | --- |
| `case_001` | Human review queue | It passed automatic graders, but evidence interpretation, usefulness, and tone still need human reading. | Bundle into a review packet and send to a person |
| `case_002` | Automatic fix needed | It has the notice signal, but the next action, order number request, is missing. | Fix the output candidate and rerun automatic grading |
| `case_007` | Automatic fix needed | It has required signals, but includes a banned expression such as `always possible`. | Revise the categorical expression and rerun automatic grading |

The result to check in this example is that automatic evaluation quickly checks repeatable conditions such as format, length, evidence hint, and banned terms, while human evaluation separately checks actual helpfulness, misunderstanding risk, tone quality, and interpretation of policy exceptions. In operation, automatic graders do not replace the final human judgment. They make the set of candidates humans read smaller and more reproducible.

Readers can try these adjustments in the example.

- Remove or add next-action guidance in the CSV's `model_output` and see how `required_action_grader` changes.
- Change `banned_terms` or candidate wording and see how `banned_terms_grader` changes.
- Change `AIBOOK_OLLAMA_MODEL` and see how the optional LLM judge's score, reason, and `reason_source` change.
- Adjust `max_length` and see how the length limit works at the automatic-grader stage before human review.
- Change `HUMAN_REVIEW_RUBRIC` and see how the review packet attached to automatically passed candidates changes.

## Human review remaining after automatic grading

The previous example is not a complete implementation that imitates human evaluation in code. It shows that `the same output becomes a different work state after passing through automatic graders and human review packets`. The core point is that increasing automatic checks and reducing human review are not the same goal. They are a division of work for catching different failures.

In one line, automatic evaluation and human evaluation are not a relationship of `which is superior`; they are `an operational division of work that separates which candidates should be mechanically fixed first and which candidates should be read in context by people`.

The more important point is that `filter many cases quickly` and `check important errors to the end` cannot be solved through the same review path. Automatic and human evaluation should therefore be read as an operational division that decides where a candidate stops and how far it moves up.

This division matters because it:

- extends P6-16.1's evaluation axes from `what to check` to `how to check`
- turns evaluation from a score table into a reviewable operational process
- connects the same output candidates to records and failure handling that can be reviewed repeatedly
- sets criteria for later verification procedures

## Checklist

- You should be able to explain that automatic evaluation is strong at `repetition and comparison`, while human evaluation is strong at `context and subtle quality judgment`.
- You should be able to say that operations can shake with automatic evaluation alone or human evaluation alone, so the two should be used together.
- You should know that quality judgment does not stop here, but continues into how candidates are left as records and review routes.

## Sources and Further Reading

- OpenAI, [Getting started with datasets](https://developers.openai.com/api/docs/guides/evaluation-getting-started){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-24.
- OpenAI, [Graders](https://developers.openai.com/api/docs/guides/graders){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-24.
- OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed 2026-07-24.
- Yupeng Chang et al., [A Survey on Evaluation of Large Language Models](https://arxiv.org/abs/2307.03109){: target="_blank" rel="noopener noreferrer" }, arXiv, 2023, accessed 2026-07-24.
