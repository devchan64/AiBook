# P6-10.3 Supplement: Observing and Comparing Response Paths

> Section ID: `P6-10.3`
> Version: `v2026.07.24`

_Subtitle: How CoT and self-consistency make us view one path and many paths differently_

In P6-10.1, we saw prompt engineering as the first control point of input design, and in P6-10.2, we saw the standard for passing problems that do not close with prompts alone to system structure. But inside the prompt layer, there is one more strategy distinction. The difference is whether we ask for an answer directly, observe intermediate judgment paths, or compare several candidate paths.

Chain-of-thought (CoT) and self-consistency are both prompt strategies for seeing or comparing response paths better. CoT tries to make intermediate reasoning more visible inside one answer, while self-consistency tries to see where several reasoning candidates converge.

The question to close in this Section is the following.

`When looking at only one answer feels unstable, how can we observe response paths more carefully at the prompt layer?`

## Scenes Where the Path Matters More Than the Answer

Some tasks are fine with only the final answer. But in classification with several mixed conditions, judgment across multiple paragraphs, or work with rule priorities, an answer that looks right and an answer that actually applied the standards correctly can be different.

Suppose a customer inquiry is classified into one of `refund`, `shipping`, `account`, and `error`. Even if the model answers `refund`, it is hard to read from that one answer whether it first checked shipment-start conditions, weighed payment-cancel conditions more heavily, or ignored operating rules. What is needed here is not a more impressive sentence, but better observation of `which standard led to that answer`.

If we separate problems reducible by prompt strategies from problems that must move to system structure, it looks as follows.

| Stuck point | Prompt strategy to check first | What it still does not replace |
| --- | --- | --- |
| The answer appears, but the order of applying standards is invisible | CoT | Latest-document retrieval, calculation verification, execution logs |
| The conclusion sometimes drifts | self-consistency | Errors from a shared wrong premise, missing external evidence |
| The response path becomes long and hard to review | Output format and path-summary adjustment | Evaluation system, approval flow |

The key of this table is that both CoT and self-consistency are strategies that help `observe response paths`. By contrast, system-external guarantees such as latest documents, calculation tools, and save success are not the role of these strategies.

## Chain-of-Thought Is a Strategy for Revealing Intermediate Standards

Chain-of-thought is a strategy that does not make the model state only the answer right away, but asks it to reveal intermediate reasoning more clearly.

A simple request may look like this.

> Classify this inquiry into one of refund, shipping, account, and error.

A CoT-style request changes it as follows.

> First divide the key conditions in the inquiry,<br>
> briefly write why each label candidate is excluded or kept,<br>
> then write one final label at the end.

The expected change is not `the answer becomes longer`. It is that people can review which conditions the model checked first and which candidates it excluded, instead of seeing only the final label.

Here, `seeing the path` does not mean directly looking inside the model. It is closer to receiving judgment traces structured in a form that users can review. At the beginner stage, it is enough to hold the following four slots.

| Slot to check | Question asked | Example |
| --- | --- | --- |
| Conditions captured from the input | What did the model use as evidence? | `payment cancellation`, `shipment started`, `refund inquiry` |
| Candidate labels | What possible answers were separated? | `refund`, `shipping` |
| Reasons for exclusion | Why was a candidate discarded? | It includes a direct refund request, so it is not only a shipping inquiry |
| Final answer | What is the final choice? | `refund` |

Without these four slots, even if there is a CoT request, the reviewer must reread a long sentence. With the four slots, the human can compare it with the actual work rule. If the operating rule says `check shipment-start status first`, we can see whether that item appears first in the model's intermediate standards too.

However, CoT also has limits.

- Long intermediate steps do not guarantee correct reasoning.
- If latest documents are missing, the model can explain an old premise at greater length.
- If calculation is needed, a separate verification structure is still needed even with intermediate explanation.

Therefore, CoT is an `input strategy that makes intermediate standards visible`, not a truth guarantee.

## Self-Consistency Looks at Agreement Among Several Paths

Self-consistency is a strategy that does not trust only one reasoning path, but looks at the conclusion reached more often among several generated paths.

At this stage, it is enough to understand it as follows.

| Strategy | What it sees | Expected effect |
| --- | --- | --- |
| CoT | Intermediate reasoning inside one answer | The order of applying standards becomes more visible |
| self-consistency | Conclusion distribution across several reasoning candidates | Reduces accidental drift from one generation |

For example, if the same classification problem is solved several times and three answers are `refund` while one is `shipping`, `refund` can look like the more stable candidate. But this is still only looking at agreement among candidate paths. If several candidates share the same wrong premise, the agreement can also be wrong together.

Even if a latest refund policy question returns the same answer several times, if the model did not see the latest document, the result may be `stable repetition of old memory`, not `verification of the current policy`. This is where the boundary between self-consistency and RAG splits.

When reading self-consistency in practice, do not look only at `how many times out of how many the same conclusion appeared`. Also look at why the conclusions diverged.

| Candidate path | Intermediate judgment summary | Final label | Review point |
| --- | --- | --- | --- |
| 1 | Looked first at payment cancellation and refund inquiry | refund | Uses the direct refund request as evidence |
| 2 | Looked first at shipment-start status | shipping | Captures a condition that operating rules may check first |
| 3 | Treated the refund inquiry as customer intent | refund | Judges by customer intent |
| 4 | Connects payment cancellation quickly to refund processing | refund | Somewhat quickly connects cancellation and refund |

From this result, we should not confirm `refund` by majority vote alone. We should also ask why the `shipping` candidate appeared. If the real work rule prioritizes shipment-start status, the second path may be a more important warning than the 3-to-1 majority. Self-consistency shows the conclusion distribution, but deciding which path fits the work standard still belongs to a human standard table or evaluation structure.

## Agreement Is Not Evidence

The most common reason CoT and self-consistency are overtrusted is that the output looks more diligent. If the intermediate explanation is long and similar conclusions appear across several tries, people want to trust it more. But what prompt strategies change is how the response path is observed, not the starting point of the answer itself.

It is safe to hold the following comparison.

| Good-looking signal | Bad judgment if trusted as-is | What to check again |
| --- | --- | --- |
| Intermediate steps are long and detailed | Believing facts are correct because reasoning is long | Does the order of applying standards match the work rule? |
| Several candidates reach the same conclusion | Believing latest facts were checked because they agreed | Does the shared premise match the current document? |
| The conclusion repeats stably | Believing execution or calculation is also stable | Are there calculation logs, tool execution results, and evidence document IDs? |

CoT and self-consistency are useful when the problem is one where `the path needs to be read more`. For problems that require checking freshness, grounding, and execution success, we must move to another structure, as seen in P6-10.2.

## Cases and Examples

### Case 1. Why Add CoT to a Classification Problem with Many Conditions?

Suppose a customer inquiry contains several conditions at once, such as `The payment was canceled, shipment already started, and when will the refund happen?` If only the final label `refund` appears, it can look correct, but the actual operating rule may first check shipment-start status before deciding refund possibility.

In this case, CoT lets the model reveal what it checked first among `payment cancellation`, `shipment started`, and `refund request`. The human can review whether the label-selection standard was applied in the same order as the work rule, rather than only seeing the final label.

Comparing the same input in two output styles makes the difference clearer.

| Output style | What the human can immediately see | Remaining uncertainty |
| --- | --- | --- |
| `refund` | Final label | Whether shipment-start status was considered is unknown |
| `Conditions: payment cancellation, shipment started, refund inquiry`<br>`Excluded: not only a shipping inquiry`<br>`Final: refund` | Which conditions were captured and which candidates were excluded | The human still needs to compare the order with operating rules |

The result to check is not `did the explanation become longer?`, but `did the standard for choosing the label become more readable, and does that standard match the actual classification rule?`

### Case 2. Latest Policy Problems Remain Even with Self-Consistency

Suppose we ask a latest refund policy question several times and adopt the most frequent answer. If the same answer appears several times, it can look stable. But if the model has not seen the latest policy document, the repeated answer may simply be repetition of an old policy.

The standard that must change in this case is not `how many times did the answer repeat?`, but `did that repetition happen on top of current document evidence?` Self-consistency can reduce one-time drift, but it does not solve missing latest-document connection.

## Exercise and Example

The goal of this example is not just to distinguish CoT and self-consistency in words, but to read conclusion distribution and check signals together from several response-path logs. Even if the same conclusion repeats several times, it cannot be adopted as-is if evidence is missing or calculation is wrong. Conversely, even a minority path can contain an important warning under work rules.

The CSV below is a snapshot log of 40 response paths made by actually calling an Ollama local model for four tasks. The generation script does not inject predefined answer candidates into the prompt. It calls the same task several times, separating CoT-style single-path observation and self-consistency-style repeated-candidate observation. Then it reduces raw model responses into observation columns: final answer, short path summary, evidence mention, calculation error, missing current policy, rule warning, and minority conclusion. If the actual model, prompt, or sampling setting changes, the conclusion and check signals for each path can also change.

First, the code that creates the stored log is as follows. The prompts sent to the model are written in English to keep the same execution standard in translations, and the manuscript example reads the CSV snapshot produced by this script.

```python
--8<-- "assets/part-06/chapter-10/p6_10_3_generate_response_path_log.py"
```

If Ollama is installed and a local model is available, `.venv/bin/python docs/assets/part-06/chapter-10/p6_10_3_generate_response_path_log.py` can be run to create a new log with the same format. The numbers included in the manuscript are a snapshot obtained by running `llama3.2:latest` with a specific setting. If it is run again, conclusion distributions and check-signal counts can change, and that difference itself shows why self-consistency and log observation are needed.

- Response path log: [p6-10-3-response-path-log.csv](/AiBook/assets/part-06/chapter-10/p6-10-3-response-path-log.csv){ .csv-preview }

One row is one response path. The core columns are `task_name`, `path_type`, `log_source`, `model_name`, `temperature`, `final_answer`, `evidence_mentioned`, `calculation_correct`, `policy_current`, `rule_warning`, and `minority_answer`. `path_type` distinguishes whether this is CoT-style single-path observation or a self-consistency-style repeated candidate. What should be checked here is not only conclusion majority vote, but whether missing evidence, calculation error, missing current policy, work-rule warning signals, and minority conclusions outside the majority remain together. In particular, `path_summary` is not model-internal reasoning itself. It is a path summary reduced to a reviewable level.

```python
# Read response-path logs and compare conclusion distribution
# together with check signals.
import csv
from pathlib import Path

log_path = Path("docs/assets/part-06/chapter-10/p6-10-3-response-path-log.csv")


def to_bool(value):
    return value.lower() == "true"


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    for row in rows:
        for column in [
            "evidence_mentioned",
            "calculation_correct",
            "policy_current",
            "rule_warning",
            "minority_answer",
        ]:
            row[column] = to_bool(row[column])
    return rows


def summarize_task(rows, task_name):
    group = [row for row in rows if row["task_name"] == task_name]
    answer_counts = {}
    for row in group:
        answer_counts[row["final_answer"]] = answer_counts.get(row["final_answer"], 0) + 1
    majority_answer, majority_count = max(answer_counts.items(), key=lambda item: item[1])
    return {
        "answer_counts": answer_counts,
        "majority_answer": majority_answer,
        "majority_ratio": round(majority_count / len(group), 2),
        "missing_evidence": sum(not row["evidence_mentioned"] for row in group),
        "calculation_error": sum(not row["calculation_correct"] for row in group),
        "stale_policy": sum(not row["policy_current"] for row in group),
        "rule_warning": sum(row["rule_warning"] for row in group),
        "minority_answer": sum(row["minority_answer"] for row in group),
    }


rows = read_rows(log_path)
tasks = sorted({row["task_name"] for row in rows})

print("[dataset]")
print("run_count =", len(rows))
print("task_count =", len(tasks))
print("log_sources =", sorted({row["log_source"] for row in rows}))
print("models =", sorted({row["model_name"] for row in rows}))
print("temperatures =", sorted({row["temperature"] for row in rows}))
print()

for task_name in tasks:
    print(f"[{task_name}]")
    summary = summarize_task(rows, task_name)
    for key, value in summary.items():
        print(key, "=", value)
```

The example output can be read as follows.

```text
[dataset]
run_count = 40
task_count = 4
log_sources = ['ollama_generated']
models = ['llama3.2:latest']
temperatures = ['0.7']

[current_refund_policy]
answer_counts = {'check_current_policy': 7, 'refund_7_days': 2, 'refund_14_days': 1}
majority_answer = check_current_policy
majority_ratio = 0.7
missing_evidence = 1
calculation_error = 0
stale_policy = 3
rule_warning = 8
minority_answer = 3
[discount_total]
answer_counts = {'apply_discount': 10}
majority_answer = apply_discount
majority_ratio = 1.0
missing_evidence = 7
calculation_error = 6
stale_policy = 0
rule_warning = 10
minority_answer = 0
[mixed_refund_label]
answer_counts = {'error': 10}
majority_answer = error
majority_ratio = 1.0
missing_evidence = 0
calculation_error = 0
stale_policy = 0
rule_warning = 10
minority_answer = 0
[security_escalation]
answer_counts = {'escalate_security': 10}
majority_answer = escalate_security
majority_ratio = 1.0
missing_evidence = 5
calculation_error = 0
stale_policy = 0
rule_warning = 10
minority_answer = 0
```

In this result, `mixed_refund_label`, `discount_total`, and `security_escalation` all have a majority conclusion ratio of 1.0. But `security_escalation` still has 5 cases with missing evidence, so the fact that every conclusion is the same does not mean enough reviewable standards remain. `discount_total` also converges entirely to `apply_discount`, but many paths do not leave enough calculation evidence. `current_refund_policy` mostly converges to `check_current_policy`, but minority conclusions that chose old refund periods and missing current-policy signals still remain. Here, `rule_warning` separately shows whether the response retained a signal that should be reviewed under work rules, and `minority_answer` shows whether a conclusion different from the majority existed.

When the same log is shown as a chart, it becomes clearer that conclusion agreement and observed check signals are different axes. Even if the upper bar is high, if the lower check signals are also high, the answer should not be adopted only because it repeated often. The lower bars are not response counts, but the sum of several check columns. If one response has both missing evidence and a rule warning, both signals are added together, so the bar height should be read not as `how many answers failed`, but as `how many signals remain for reviewers to revisit`.

![Majority Conclusion Ratio and Check Signals in Response-Path Logs](/AiBook/assets/part-06/chapter-10/response-path-consistency-en.png)

Values readers can directly change in this example are the log rows themselves and the check-signal standards. For example, if `rule_warning` is made stricter, only warnings that are important under real work rules can remain among response paths. If paths where `policy_current` is `False` are all excluded, we can also check how the self-consistency majority changes. Through this manipulation, we confirm that CoT and self-consistency are not answer-guaranteeing technologies. They are strategies that help observe and compare response paths better.

Now mark whether the first thing to check in each scene is CoT, self-consistency, or system structure rather than a prompt strategy. The key is first choosing `why the output is unstable`.

| Scene | Why it is unstable | What to check first | Reason |
| --- | --- | --- | --- |
| A classification label appears, but the reviewer cannot understand why that label was chosen |  |  |  |
| The conclusion sometimes changes for the same numerical comparison question. The source numbers are already in the input |  |  |  |
| The same refund period appears across several tries, but the document version is not shown |  |  |  |
| The calculation process is explained at length, but totals are often wrong |  |  |  |
| Three paths give the same label, but a different label that appeared once looks important under work rules |  |  |  |

Explanation:

| Scene | Why it is unstable | What to check first | Reason |
| --- | --- | --- | --- |
| Label-selection standard is unreadable | The judgment path is invisible | CoT | Revealing intermediate standards and candidate-exclusion reasons comes first |
| Source numbers exist and only the conclusion drifts | One generation is unstable | self-consistency | Comparing conclusion distribution across several candidate paths can reduce one-time drift |
| Document version is not shown | Current evidence is missing | RAG or evidence-connection structure | Even if several answers agree, freshness does not close without current document evidence |
| Explanation is long but calculation is wrong | Actual calculation verification is missing | tool use or verification structure | Actual calculation verification is needed before reasoning explanation |
| A minority candidate matters under work rules | Majority vote and work priority conflict | Interpret self-consistency results + compare rules | Check candidate distribution, but do not close by majority vote alone |

The point of this exercise is not to bundle CoT and self-consistency as `stronger prompts`. CoT makes one path more readable, while self-consistency compares several paths. But evidence and execution guarantees are still separate structural problems.

## Checklist

- Can you explain CoT as a strategy that makes intermediate reasoning paths more visible?
- Can you explain self-consistency as a strategy that looks at agreement among several reasoning candidates?
- Can you distinguish the fact that an intermediate explanation is long or a conclusion repeats from guarantees of latest evidence, calculation verification, and tool execution?
- Are you ready to read automatic prompt optimization in P6-10.4 as a prompt experiment-loop strategy, not a response-path strategy?

## Sources and References

- Jason Wei et al., [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, accessed 2026-07-19.
- Xuezhi Wang et al., [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, accessed 2026-07-19.
- Pranab Sahoo et al., [A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications](https://arxiv.org/abs/2402.07927){: target="_blank" rel="noopener noreferrer" }, arXiv, 2024, accessed 2026-07-19.
