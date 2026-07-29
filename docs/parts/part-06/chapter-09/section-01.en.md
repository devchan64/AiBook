# P6-9.1 Instruction Tuning That Builds Response Habits Matching Request Formats

> Section ID: `P6-9.1`
> Version: `v2026.07.26`

In P6-8.2, we saw why efficient adjustment methods such as LoRA matter in practice. But being able to adjust a model a little more cheaply does not immediately create answers that follow human instructions well.

What is the process that makes a model go beyond simply continuing sentences and follow user instructions better?

Instruction tuning is the process of additionally adjusting a model so it understands natural-language instructions better and responds in the requested format.

If we say the same thing more simply, it is as follows.

Instruction tuning is the stage that strengthens the habit of answering according to the way people make requests, beyond simply continuing text.

## Layer Adjusting Response Habits

Response-habit adjustment begins with the following questions.

- What does instruction tuning try to change?
- How do pretraining, fine-tuning, and instruction tuning connect?
- Why does instruction tuning feel important in the conversational LLM experience?

Instruction tuning is an `instruction-following adjustment layer`. This layer is closer to changing response habits so that existing language ability is brought out according to the user's request format, rather than storing more new facts. Alignment is the next problem that separately asks `is an answer that follows so well acceptable?`

The user experience of conversational LLMs changes greatly at this instruction-following ability. Pretraining creates a broad language base and expression sense, fine-tuning narrows domain expressions and task criteria, and instruction tuning fits request formats and answer structures more closely to user responses. Latest-information connection, external-document evidence, and actual execution are separate service connections added later through RAG and tool use.

Therefore, what we first need to see here is not `does it put in more new knowledge?`, but `what response habit does the same generation structure acquire?` How to handle alignment more precisely, and how to attach external-document evidence and tool execution to actual responses, are separated again in later sections and service-connection chapters.

The impression that `conversational LLMs naturally follow human requests well from the start` should be reread as `the result of additionally adjusting response format and response habits`.

In other words, the center of this section is `how to make it respond more like an assistant`. From there, we move to questions such as `is that answer acceptable?`, `what should it use as evidence?`, and `what should it actually execute?`

## Distinguishing New Knowledge Addition and Response-Habit Adjustment

- You can explain instruction tuning at an introductory level.
- You can reorganize the difference between pretraining, fine-tuning, and instruction tuning.
- You can explain why conversational LLMs feel different from ordinary language models.
- You can read alignment as an acceptability problem different from `does it follow instructions well?`

This distinction matters for the following reasons.

- because it moves beyond seeing generative AI only as simple autocomplete
- because it separates assistant behavior as its own layer
- because it connects the alignment problem in P6-9.2 to the question `why is it needed?`

## Judgment Criteria for Instruction Tuning

Instruction tuning is not a stage that adds new knowledge, but a response-habit adjustment that brings out the same language ability according to user request formats.

| Judgment Criterion | Question to Check |
| --- | --- |
| Adjustment target | Is the problem changing response format and response habit rather than new facts? |
| Stage distinction | Can pretraining, fine-tuning, and instruction tuning be separated by what each changes? |
| User experience | Why does the same generation structure start to look like a conversational assistant? |
| Observable scene | Do response habits such as summary, steps, tables, and limitation notices actually change? |

## What Does Instruction Tuning Try to Change?

A pretrained model learns broad language patterns. But that alone does not always make it respond in the way users expect.

It is easier to read this through the following short questions.

| Question | Short Answer |
| --- | --- |
| Why is this adjustment needed again? | because knowing language and following instructions well are not the same |
| What are we trying to make it better at? | request-format understanding, answer structure, limitation notices |
| Where does it change? | response habits and format fit, more than next-token prediction itself |

For example, users expect the following.

- answer the question
- organize as a table when a table is requested
- explain in order when step-by-step explanation is requested
- clearly state limits for impossible requests

These expectations are not sufficiently guaranteed only by predicting the next token well. Instruction tuning can be seen as the process of strengthening response habits that fit these `user instruction formats`.

In other words, the core of this section is separating `the ability to continue words` from `the ability to answer according to a request`.

## Difference from Pretraining

It is good to separate this difference again.

| Stage | Core Question |
| --- | --- |
| pretraining | Does it first learn general language patterns? |
| fine-tuning | Does it adjust for a specific task or domain? |
| instruction tuning | Does it adjust to follow natural-language instructions better? |

Instruction tuning can usually be explained as fitting `the user's request format` and `the desirable answer format` better.

In other words, it can be summarized as follows.

`Pretraining is the stage that broadly learns language, and instruction tuning is the stage that adjusts answer habits so the model responds better to human request styles.`

If we place fine-tuning together with these, it reads as follows.

- pretraining: broad base of language
- fine-tuning: adaptation to a specific task and domain
- instruction tuning: response adaptation to user request formats

## Why Does It Feel Important in Conversational LLMs?

In conversational LLMs, users make requests directly in natural language. Therefore, users expect the model to show the following.

- a response that seems to understand my question
- an answer that matches the requested format
- an answer that is not too verbose, or is sufficiently detailed when needed
- structured steps, summaries, examples, and cautions

This experience is closer to `a conversational assistant-like response` than to a simple language model. Instruction tuning is an important layer that explains this change.

Readers feel this point most strongly. Even within the same model family, some models feel like they `continue plausible sentences`, while others feel like they `structurally follow my request`. Instruction tuning is needed to explain this difference.

## Instruction Tuning Is Not Universal

But instruction tuning should not be exaggerated either.

Even when instruction tuning is done, it does not automatically:

- guarantee factuality
- remove bias
- fully handle dangerous requests by itself
- automatically reflect latest external information

A safer explanation is as follows.

`Instruction tuning strengthens responses that match user request formats, but it does not solve factual verification, recency, and safety as a whole by itself.`

We need to hold this boundary first so we do not mix the fact that `answer format improved` with the judgment that `factual verification, recency, and safety were solved together`.

## Response Habits Changed by Instruction Tuning

If we summarize this so far in the shortest form, it is as follows.

- Pretraining is the `stage that broadly learns language`.
- Fine-tuning is the `stage that fits a specific task and domain better`.
- Instruction tuning is the `stage that adjusts response habits so the model responds better to human request formats`.

We need to distinguish these three so we do not mix `what the model knows` and `how the model answers` as the same problem.

## Flow Where Response-Format Adjustment Is Added

```mermaid
--8<-- "assets/part-06/chapter-09/p6-c09-s01-instruction-tuning-flow-en.mmd"
```

This diagram makes us read instruction tuning as a flow where `response-format adjustment` is added on top of the `language model body`. So the result to check in this diagram is whether the base model's general language ability and the response-format adjustment added later are actually distinguished as different layers.

The core to read in this figure is as follows.

- the base model already knows language
- additional examples show `how to answer`
- the result becomes closer to `assistant-like responses`

## Cases and Examples

### Case 1. Summary Request

Suppose a user asks, `Summarize the key points in three lines`, when summarizing a team document. At first, it is easy to think `it is enough if the content is correct`. If the model does not miss key facts, it already feels fairly good. But actual users expect length and format together. A model with weak instruction adjustment may only continue a long explanatory paragraph and fail to match the three-line format. For example, even if all key facts are included, if it writes one long paragraph, users may feel it is hard to paste directly into a messenger or report.

What changes here is a shift from checking `are the key facts included?` to checking `does it also match the requested length and format?` Instruction tuning helps match not only `what to say`, but also `in what length and structure to answer`, turning the same content into a response users can reuse immediately. The misunderstanding to correct here is the expectation that `if the facts are right, request satisfaction automatically follows`. So the result to check in this case is not only whether key facts are right, but whether the three-line summary format is actually matched and whether that format makes the answer directly reusable.

| Comparison Point | Response That Looks Before Adjustment | Response Reflecting Instruction Format |
| --- | --- | --- |
| three-line summary | contains the core but expands into one paragraph or more than three lines | separates the core into a three-line structure |

### Case 2. Step-by-Step Explanation

When creating internal training material, a user may ask, `Explain it in 3 steps so a new employee can follow it`. In this scene, it is easy to feel that if the model knows the content, the structure will naturally fit too. But even people do not automatically fit `3 steps` and `an easy-to-follow order` just because they know information. A general language model may mix the explanation order or fail to match the requested number of steps. For example, if it discusses exception handling before the preparation step, the content may be correct but harder to follow in practice. In other words, `having information` and `speaking in an easy-to-teach structure` are different abilities.

What changes here is a shift from checking `does it know the content?` to checking `does it also keep the requested number of steps and development order?` An instruction-tuned model is adjusted toward reflecting requirements such as `number of steps`, `explanation order`, and `development matched to the reader level` more naturally. The misunderstanding to correct here is the thought that `if the content is right, the educational structure follows automatically`. So the result to check in this case is not only whether the explanation content is right, but whether the 3-step order and easy-to-follow development are maintained, and whether the dependency order between steps also stays intact.

| Comparison Point | Response That Looks Before Adjustment | Response Reflecting Instruction Format |
| --- | --- | --- |
| 3-step explanation | content exists, but the number or order of steps shakes | keeps a followable order such as preparation, execution, and review |

### Case 3. Refusal and Limitation Notice

A user may ask to show a document without internal permission, or demand an assertive answer without evidence. In this scene, it is easy to feel that a model that kindly keeps answering is always a good response. So if the answer continues, service quality may seem higher. But if it only keeps answering here, it can lead to wrong information or permission violations. For example, if it guesses and summarizes the content of a file it cannot access, it fails to follow actual document access control and can spread incorrect content. What is needed here is not `the diligence to answer to the end`, but `a response habit that knows where to stop`.

What changes here is a shift from checking `does it keep answering to the end?` to checking `does it structurally present the refusal reason and safe next action?` Instruction tuning is also used to strengthen response habits that structurally state `why it cannot do something`, `verifiable alternatives`, and `information needed next`. So the result to check in this case is whether, instead of unconditionally continuing the answer, the refusal reason and safe next action are presented together, and whether the next input or approval condition needed by the user is also shown.

| Comparison Point | Response That Looks Before Adjustment | Response Reflecting Instruction Format |
| --- | --- | --- |
| limitation notice | guesses inaccessible content and keeps answering | separates why it cannot do it and what safe next action is possible |

If we group the three cases again from the perspective of response habits, we get the following.

| Situation | What Can Shake With Only the Base Model | What Instruction Tuning Tries to Hold More Strongly |
| --- | --- | --- |
| Summary request | format constraints such as length and line count | requested structure and amount |
| Step-by-step explanation | number of steps and development order | guide flow and step structure for readers |
| Refusal and limitation notice | habit of unconditionally continuing an answer | refusal reason and safe next action |

## Scenes Where Instruction-Format Adjustment Is Needed

After reading this section, even if you do not yet know the details of alignment or RLHF, you can first practice distinguishing whether the current blocker is a `content shortage problem` or an `instruction-format adjustment problem`. If the format is right but latest rules or evidence facts are often wrong, you should check whether new knowledge or evidence connection is lacking rather than focusing on the fact that it answers like an assistant. If the key facts are right but it often violates requested formats such as `in three lines`, the problem may be weak instruction-format-following habit rather than factuality. If explanation content is right but step count and development order shake, a response habit that matches the request structure may be needed more than more knowledge. If it keeps answering even impossible requests and limitation notice is weak, what appears first is refusal and limitation-notice habit adjustment, not content generation.

What matters here is not seeing `instruction tuning adds new knowledge`, but first reading `what to say` and `how to answer` as different problems.

The things often mixed here are as follows.

- It is easy to feel that factual knowledge and request-format following are the same ability.
- It is easy to think that if the content is right, format and limitation notices naturally follow too.
- It is easy to exaggerate instruction tuning as solving recency, factuality, and safety all at once.

So the closing point of this section is to turn the sentence `instruction tuning is a layer that adjusts response habits and format` into an actual judgment criterion.

## Exercise and Example

The goal of this example is not to reproduce actual instruction-tuning training as a whole, but to check through evaluation logs how response habits differ even with the `same bundle of facts`. Instead of directly comparing only four requests, we aggregate 36 request-evaluation records and check how often `three-line summary`, `3-step explanation`, `table organization`, and `limitation notice when evidence is insufficient` are satisfied.

The code below uses the instruction-following evaluation CSV [p6_9_1_instruction_following_eval-en.csv](/AiBook/assets/part-06/chapter-09/p6_9_1_instruction_following_eval-en.csv){ .csv-preview }. Representative raw response logs are stored separately in [p6-9-1-instruction-response-log-en.csv](/AiBook/assets/part-06/chapter-09/p6-9-1-instruction-response-log-en.csv){ .csv-preview }. One row in the evaluation CSV is one user-instruction evaluation case, and one row in the response-log CSV is a base response or instruction-format-reflecting response observed for the same case.

The core columns are `request_type`, `requested_signal`, `base_*`, and `tuned_*`. `requested_signal` tells us which instruction-following signal to check, such as line count, numbered steps, table rows, or uncertainty marking.

The `base_*` columns are format signals observed in ordinary responses, and the `tuned_*` columns are format signals observed in instruction-format-reflecting responses. The `reader_hint` and `base_observation` columns do not give the answer instead; they are helper explanations that show what format difference to observe when opening the CSV. The response-log CSV is supporting material for checking which raw responses produced these signals. Some `tuned_*` rows are intentionally left failing. This lets us read instruction tuning not as a perfect-answer device, but as adjustment that raises request-format-following rates.

This code does not directly grade raw response text with natural-language understanding. A human first observed structural signals such as line count, numbered step count, table row count, and limitation-notice marking from raw responses and recorded them in the CSV; the code then aggregates those observed signals using the same criteria. Therefore, the learning point of this example is not `implementing an automatic grader`, but what output signals to observe separately when looking at instruction tuning.

The key point to confirm is that instruction tuning is not adding new facts, but can be read as a change that more stably matches requested output formats and instruction-following rates even with the same content.

```python
# This example reads CSV evaluation cases and compares how often base and instruction-tuned responses satisfy requested format and structure signals.
import csv
from collections import defaultdict
from pathlib import Path

eval_path = Path("docs/assets/part-06/chapter-09/p6_9_1_instruction_following_eval-en.csv")

def to_bool(value):
    return value.lower() == "true"

def read_cases(path):
    rows = []
    with path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            rows.append(row)
    return rows

def check_case(row, prefix):
    request_type = row["request_type"]
    lines = int(row[f"{prefix}_lines"])
    numbered_steps = int(row[f"{prefix}_numbered_steps"])
    table_rows = int(row[f"{prefix}_table_rows"])
    uncertainty_marker = to_bool(row[f"{prefix}_uncertainty_marker"])
    bullets = int(row[f"{prefix}_bullets"])

    if request_type == "three_line_summary":
        return lines == 3
    if request_type == "three_steps":
        return lines == 3 and numbered_steps == 3
    if request_type == "table":
        return table_rows >= 4
    if request_type == "limitations":
        return uncertainty_marker and bullets >= 2
    return False

cases = read_cases(eval_path)
preview_count = 6

evaluated = []
for row in cases:
    base_ok = check_case(row, "base")
    tuned_ok = check_case(row, "tuned")
    evaluated.append(
        {
            "case_id": row["case_id"],
            "request_type": row["request_type"],
            "base_ok": base_ok,
            "tuned_ok": tuned_ok,
            "improved": (not base_ok) and tuned_ok,
        }
    )

by_type = defaultdict(lambda: {"count": 0, "base_ok": 0, "tuned_ok": 0, "improved": 0})
for item in evaluated:
    group = by_type[item["request_type"]]
    group["count"] += 1
    group["base_ok"] += int(item["base_ok"])
    group["tuned_ok"] += int(item["tuned_ok"])
    group["improved"] += int(item["improved"])

total = len(evaluated)
base_total = sum(item["base_ok"] for item in evaluated)
tuned_total = sum(item["tuned_ok"] for item in evaluated)
improved_total = sum(item["improved"] for item in evaluated)

print("[dataset]")
print("case_count =", total)
print("request_types =", sorted(by_type))
print()
print("[preview]")
for item in evaluated[:preview_count]:
    print(item)
print(f"... {total - preview_count} more cases")
print()
print("[summary]")
print("base_meets_request_count =", base_total)
print("tuned_meets_request_count =", tuned_total)
print("improved_case_count =", improved_total)
print("base_meets_request_rate =", round(base_total / total, 2))
print("tuned_meets_request_rate =", round(tuned_total / total, 2))
print()
print("[by request type]")
for request_type, values in sorted(by_type.items()):
    print(
        request_type,
        {
            "count": values["count"],
            "base_ok": values["base_ok"],
            "tuned_ok": values["tuned_ok"],
            "improved": values["improved"],
        },
    )
```

The execution result example can be read as follows.

```text
[dataset]
case_count = 36
request_types = ['limitations', 'table', 'three_line_summary', 'three_steps']

[preview]
{'case_id': 'S01', 'request_type': 'three_line_summary', 'base_ok': False, 'tuned_ok': True, 'improved': True}
{'case_id': 'S02', 'request_type': 'three_line_summary', 'base_ok': False, 'tuned_ok': True, 'improved': True}
{'case_id': 'S03', 'request_type': 'three_line_summary', 'base_ok': False, 'tuned_ok': True, 'improved': True}
{'case_id': 'S04', 'request_type': 'three_line_summary', 'base_ok': False, 'tuned_ok': True, 'improved': True}
{'case_id': 'S05', 'request_type': 'three_line_summary', 'base_ok': False, 'tuned_ok': True, 'improved': True}
{'case_id': 'S06', 'request_type': 'three_line_summary', 'base_ok': False, 'tuned_ok': True, 'improved': True}
... 30 more cases

[summary]
base_meets_request_count = 1
tuned_meets_request_count = 32
improved_case_count = 31
base_meets_request_rate = 0.03
tuned_meets_request_rate = 0.89

[by request type]
limitations {'count': 9, 'base_ok': 0, 'tuned_ok': 8, 'improved': 8}
table {'count': 9, 'base_ok': 0, 'tuned_ok': 8, 'improved': 8}
three_line_summary {'count': 9, 'base_ok': 1, 'tuned_ok': 8, 'improved': 7}
three_steps {'count': 9, 'base_ok': 0, 'tuned_ok': 8, 'improved': 8}
```

So the result to check in this example is not one or two success cases, but how the pass pattern changes between base responses and instruction-format-reflecting responses across several request types. Base responses can accidentally match the format in some requests, but when 36 cases are grouped, the request-format-following rate changes from `0.03` to `0.89`. At the same time, instruction-format-reflecting responses still fail the criterion in 4 cases. This difference lets us read instruction tuning not as `new knowledge addition` or `automatic perfection`, but as `response-habit adjustment`.

When the summary statistics are shown as a chart, the difference between base responses and instruction-tuned responses becomes simpler to see. Here, `0.03 -> 0.89` is not a general performance score, but an observed value from counting 36 cases in this example evaluation log by the criteria above. Even with the same bundle of facts, instruction-tuned responses change output rules in the direction of stably increasing satisfaction across several request formats. At the same time, 4 unmet cases remain, so this graph makes us read instruction tuning not as a perfect-answer device, but as adjustment that raises request-format-following rates.

![Request-met and unmet counts for base and instruction-tuned responses](/AiBook/assets/part-06/chapter-09/instruction-tuning-request-match-en.png)

Readers can directly try the following adjustments in this example.

- add new request types such as `two_sentence_summary` or `pros_cons_table` to the CSV
- check how results change if the pass criterion for `three_line_summary` is changed from `lines == 3` to `lines <= 3`
- make the `limitations` criterion stricter by requiring both limitation wording and additional-information items
- open the `tuned_*` rows intentionally left as failures and check which request formats still miss the criterion

The core to read in this example is as follows.

- even with the same question, response-format requirements can differ
- base responses may continue content successfully but often miss format requirements
- instruction-tuned responses more stably reflect user-requested structures as actual output signals, but do not automatically solve every case
- especially for different response habits such as `summary`, `steps`, `table`, and `limitation notice`, instruction tuning helps bring them out more stably within one model, but remaining failures must be checked again in evaluation and alignment stages

In other words, it is often better to understand instruction tuning as a layer that changes `how to answer` rather than `what is known`.

## Format Changes Caused by Response-Method Adjustment

This compressed comparison shows that instruction tuning is less a task that injects new knowledge and more a layer that makes existing base ability come out better in the user's requested format. In particular, it shows that even with the same bundle of facts, when request habits differ, such as `three lines`, `3 steps`, `table`, and `limitation notice`, output rules must also change together. However, as the remaining failure cases show, a higher format-following rate does not mean factuality, recency, and safety have also been solved. So in the next section, we separate `an answer that follows well` from `an acceptable answer` again.

## Checklist
- Can you explain instruction tuning as a layer that adjusts `how to answer` rather than `what is known`?
- Can you distinguish again what pretraining, fine-tuning, and instruction tuning each change?
- Are you ready to read P6-9.2 as a problem that separates `following well` from `acceptable behavior`?

## Sources and References

- Long Ouyang et al., `Training language models to follow instructions with human feedback`, arXiv, 2022, accessed 2026-07-19. [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155){: target="_blank" rel="noopener noreferrer" }
- Victor Sanh et al., `Multitask Prompted Training Enables Zero-Shot Task Generalization`, arXiv, 2021, accessed 2026-07-19. [https://arxiv.org/abs/2110.08207](https://arxiv.org/abs/2110.08207){: target="_blank" rel="noopener noreferrer" }
- OpenAI, `Aligning language models to follow instructions`, 2022, accessed 2026-07-19. [https://openai.com/index/instruction-following/](https://openai.com/index/instruction-following/){: target="_blank" rel="noopener noreferrer" }
