# P6-10.3 LLM Failures Divided into Format, Evidence, and Execution Gaps

> Section ID: `P6-10.3`
> Version: `v2026.07.26`

By P6-10.2, we can read `which answer looks more assistant-like` and `which answer is more acceptable and safe`. But when we move into actual feature improvement, the question changes one more time. We cannot stop at knowing the standard for a good answer. We need to diagnose what was missing first in the failed answer.

When a model behaves differently from expectation, what shortage caused the failure first?

When improving a generative AI feature, it is safer to first divide whether the failure cause is closer to `format`, `evidence`, `execution`, or `persistent adaptation`, instead of choosing a technique name first.

## A Diagnostic Map That Divides Failure Causes First

Failure-cause diagnosis starts from the following questions.

- Is the current failure a problem where the answer format is unstable?
- Is the current evidence document or latest information missing?
- Does the task require execution such as calculation, lookup, or state change?
- Does the model need to match repeated domain style or task responses for longer?

Prompt revision, RAG, tool use, and fine-tuning are support paths considered after this diagnosis. Prompt adjustment modifies input instructions and output format. RAG connects external documents and sources as evidence. Tool use delegates calculation, lookup, and state changes to functions outside the model. Fine-tuning is closer to moving repeated domain patterns or style adaptation into the model-adjustment layer.

The point to be careful about is that these four paths can look lumped together under the name `ways to improve performance`. In reality, they touch different locations. Prompt revision changes the input sentence and output form while keeping the same model. RAG finds documents before the model answers and attaches them to the input side. Tool use lets the model call outside functions and receive results instead of calculating or looking things up directly. Fine-tuning reflects repeatedly needed response habits in the model-adjustment process. So even the same phrase `the answer is wrong` can require different repair points.

This Section does not replace the detailed techniques in later chapters. The problem to close here is `what should be fixed first, and where?` Prompt design itself is handled in P6-10, RAG and vector search in P6-11 and P6-12, and tool use and AI agent structure in later Modules. P6-10.4 and P6-10.5 are supplementary studies on efficient adjustment when this diagnosis points toward the fine-tuning axis.

## Why Read a Diagnostic Map Right After Alignment?

After instruction tuning and alignment, it can feel as if most model-quality problems have been explained. But in real products, that is where the work starts. If every strange answer is collapsed into `the model is not good`, the response can easily go wrong: a format problem can be mistaken for a retrieval problem, a freshness problem can be handled by only writing longer prompts, or a calculation problem can be pushed into fine-tuning.

The diagnostic map therefore acts as a bridge that translates the previous ideas of `response-habit adjustment` and `acceptable behavior standards` into actual improvement work. We do not stop at evaluating which response looks more assistant-like or which answer is more acceptable and safe. We first divide whether the current failure is a format problem, an evidence problem, an execution problem, or a persistent-adaptation problem.

In other words, the closing point of this Section is not `knowing four technique names`, but `being less wrong when classifying the cause of a failure from symptoms`. Here we only hold which failure type prompt revision, fine-tuning, RAG, and tool use first target, and whether the current problem is closer to format, evidence, execution, or persistent adaptation. The actual design, implementation, cost comparison tables, and organization-specific operating processes for each support path are developed later.

The key standard is not `fix every problem with one method`, but `diagnose by separating format, evidence, execution, and persistent adaptation according to the failure cause`. Once this standard is in place, later techniques can be read not as `new technology introductions`, but as `support paths for different failure causes`.

## Separating Format, Evidence, Execution, and Adaptation Problems

- You can explain the role differences among prompts, fine-tuning, RAG, and tool use.
- You can say which axis should be checked first for each problem type.
- You can read the prompt, RAG, tool-use, and AI agent chapters inside one diagnostic map.
- You can more easily understand why several devices are combined in the integrated mini-practice.

## Shortest Separation of Four Shortages

| First shortage | Support path to suspect first |
| --- | --- |
| Input instruction and output format | prompt revision |
| Latest information, internal documents, evidence connection | RAG |
| External functions such as calculation, lookup, and execution | tool use |
| Repeated tone, domain pattern, task response | fine-tuning |

The purpose of this table is not to explain the four techniques in detail. It leaves the point that even the same symptom, `the LLM is wrong`, can require a different first support path if the missing layer is different.

Suppose a user asks, `Summarize the vacation policy in three lines`, and the answer is unsatisfactory. In one sentence, all of the following could be called `a bad answer`, but the actual diagnosis splits as follows.

| Observed failure | First shortage to check | Why this is a different problem |
| --- | --- | --- |
| It answers in a long paragraph, not a three-line summary | Format | Adding more current policy information may still leave the output format unstable |
| It uses three lines, but answers from last month's policy | Evidence | The problem is missing current documents, not sentence shape |
| It must calculate remaining vacation days, but the number is wrong | Execution | Even with policy documents, the calculation result needs a separate check |
| The tone changes every time, even when asked to use the same brand voice | Persistent adaptation | Stabilizing a repeated pattern matters more than one instruction |

Read this way, `wrong answer` is not one cause. We need to first divide whether the format broke, evidence is missing, execution results are needed, or repeated habits are needed. Only then does the next support path become less misaligned.

## Problems That Each Support Path Does Not Close Well

The important point is to see not only `what fits`, but also `what this path does not close well`.

| Means | Problems it first fits well | Problems this alone does not close well |
| --- | --- | --- |
| Prompt revision | Format drift, explanation order, tone adjustment | Missing latest information, external execution, guaranteed calculation accuracy |
| Fine-tuning | Repeated domain style, persistent task adaptation | Frequently changing latest documents, immediate lookup tasks |
| RAG | Freshness, internal-document evidence, source connection | Calculation execution, state change, external system action |
| Tool use | Calculation, lookup, real execution | Tone consistency, long-term domain style adaptation |

So the diagnostic map is less about `choosing one of four` and more about first separating which layer the current failure belongs to.

## When Format Signals Are Missing

The following problems should first be checked as missing input-instruction and output-format signals.

- The answer format often drifts.
- The model follows the instruction order incorrectly.
- The same information needs a more summarized or more structured output.

In this case, the model may not lack knowledge. The current input design may not reveal the target clearly enough.

## When Persistent Adaptation Signals Repeat

When the following conditions repeat, we can check whether this is not a one-time input revision problem but a persistent-adaptation problem.

- A specific domain style is continuously needed.
- The same pattern of work must be processed reliably at scale.
- Consistency does not improve enough with prompts alone.

Fine-tuning is close to a choice that moves part of `designing a long input every time` into the learning layer.

## When Evidence Signals Are Missing

The following problems should first be checked as missing current evidence and source connection, rather than answer style.

- Freshness of the answer matters.
- Internal-document evidence is needed.
- Letting the model answer only from internal memory is risky.

In this case, the core problem is less `how do we make it speak better?` and more `what should it speak from?`

## When Execution Signals Are Missing

The following problems do not close with document evidence alone. We should check whether execution or lookup outside the model is needed.

- It must calculate directly.
- It must look up current state.
- It must cause an actual action in an external system.

For example, creating a calendar event, checking remaining vacation days, reading a file, and checking order status do not end with document evidence alone. This is where we should consider tool use that performs the real execution or lookup.

## If It Does Not Split Cleanly, Break the Failure Log Down

Real problems often do not divide cleanly into only one of the four categories above. So before attaching a technique name, we need to divide the failure log into smaller observations. A good diagnosis does not jump straight to a conclusion such as `we need RAG`. It asks in this order.

| Diagnostic order | Question to ask | Record to check |
| --- | --- | --- |
| 1. What was required? | What output format, fact standard, or execution result did the user expect? | Original request, system instruction, expected output |
| 2. Where did the actual answer deviate? | Which signal appears among format, evidence, execution, and persistent adaptation? | Model answer, missing sources, wrong numbers, repeated failure pattern |
| 3. Where would the first fix have the largest effect? | Is the largest failure closer to input design, document connection, tool execution, or adjustment layer? | Failure frequency, risk level, reproducibility |
| 4. What problem will still remain? | Is there a second-priority signal after the first support path? | Rerun result, remaining error type |

For example, if the request `Summarize the latest vacation policy in three lines` produces a four-line answer and also has the wrong policy number, both format and evidence appear. If we fix only the format, we get a three-line wrong answer. If we fix only the evidence, the model may produce a correct policy in a long paragraph. So we need to reduce the higher-risk evidence error first, then stabilize the output format as the second priority.

Conversely, if the total amount is wrong but we start by editing the prompt because the sentence is verbose, we may get a shorter and prettier wrong answer. The purpose of diagnosis is not to create a pretty answer first. It is to find which shortage must be reduced first for the failure to actually shrink.

## A Flow That Moves Missing Signals into Support Paths

```mermaid
--8<-- "assets/part-06/chapter-09/p6-c09-s03-solution-map-en.mmd"
```

This diagram is not meant to automate every choice mechanically. It gives an order of judgment for reading the following chapters. In real problems, two signals can appear together, so we should read it as catching the largest shortage first and leaving the second signal as a secondary response.

## Cases and Examples

### Case 1. Answer Format Often Drifts

Suppose the user asks, `Always answer as a three-line summary`, but some answers are long and others are short. When answers drift, people may first feel that the model is not smart. But in this case, the model is not failing because it lacks the latest document or because it lacks a calculation tool. The core problem is instability in `what form should the answer take`, so it is natural to check prompt structure and examples before moving to evidence gaps or execution gaps.

For example, if the content is correct but the bullets grow into four lines, solving freshness or calculation problems will still not fit the usage purpose. The change here is a move from vaguely asking `is the model smart?` to asking `does the output-format requirement actually stabilize?` The result to check in this case is whether answer-format drift actually decreases after revising the prompt structure, before considering evidence connection or tool execution.

| Current symptom | What is effectively missing first | Response that is too heavy to check first |
| --- | --- | --- |
| Bullet count changes every time | Format instruction and example structure | RAG, calculation tool connection |
| Title/summary order often changes | Output-order constraint | Fine-tuning review |
| Content is correct, but shape is inconsistent | Prompt design | Adding latest documents |

### Case 2. Model Often Gets Internal Policy Wrong

Suppose internal vacation rules change often, but the model answers from last quarter's standard. If the sentence is natural, people may first pass over it as correct. But in this case, no matter how much we refine the answer form, internal model memory alone cannot easily reflect the latest policy. The core problem is that `current document evidence is missing`, so we should first check whether the latest policy document is retrieved and connected as answer evidence, rather than making the prompt longer.

For example, even if we make the sentence more polite or adjust the answer length, the problem remains if the latest standard number is wrong. The change here is a move from asking `is the answer natural?` to asking `was the current evidence document actually connected?` The result to check in this case is whether freshness errors that were not fixed by prompt revision alone actually decrease when the latest document evidence is connected.

| Current symptom | What is effectively missing first | Why prompts alone do not close it |
| --- | --- | --- |
| Numbers and policy dates are often wrong | Latest evidence document | Writing a longer input does not update internal memory |
| Sentences are natural, but the standard is old | Current version reference | Tone edits cannot fix factual errors |
| The answer drifts when asked for a source | Document connection and citation evidence | The core issue is missing evidence, not explanation style |

### Case 3. Model Often Gets Numbers Wrong

Suppose the model often gets discount calculations or total sums wrong. It can feel as if a longer prompt such as `think slowly` will solve the problem, but that does not guarantee calculation accuracy. If the core issue is execution accuracy, connecting a calculation tool may be a more direct solution than a longer prompt.

For example, even if the explanation becomes longer and more plausible, the business failure remains if the final number is wrong. The change here is a move from asking `does the explanation sound plausible?` to asking `is the actual calculation result correct?` The result to check in this case is whether final-number accuracy becomes more stable when a calculation tool checks the value, rather than merely increasing explanation length.

### Case 4. We Want the Same Domain Style to Stay Consistent

Consider legal guidance, medical consultation drafts, or brand announcements where the same domain style must stay consistent over time. It can feel sufficient to put long tone rules into the prompt, but as request volume grows, expressions can drift little by little. This is not a one-time revision problem but a persistent style-adjustment problem, so fine-tuning or a more structured adjustment layer can be considered.

For example, if the honorific level is strong one day and the explanation order changes another day, the brand or domain tone can easily drift even when the content is correct. The change here is a move from asking `did we write a long rule once?` to asking `does the same style hold across repeated requests?` The result to check in this case is whether a model-adjustment layer leads to more consistent style than input-sentence revision when the same style problem repeatedly remains.

The four cases can be grouped again from the perspective of missing-signal diagnosis.

| Symptom | Missing signal to suspect first | Support path to check first |
| --- | --- | --- |
| Answer-format drift | Insufficient reflection of format requirements | prompt revision |
| Latest policy error | Missing evidence document | RAG |
| Calculation error | Insufficient execution accuracy | tool use |
| Lack of style consistency | Insufficient persistent style adaptation | fine-tuning |

The same content can be read again by asking `what is missing?`

```mermaid
--8<-- "assets/part-06/chapter-09/p6-c09-s03-missing-piece-map-en.mmd"
```

The key is not to choose a technique name first, but to first divide which shortage explains the current failure.

## Scenes Where Missing-Signal Diagnosis Is Needed

After reading this Section, even without knowing the detailed implementation of each later chapter, you can practice first separating whether the current problem is a `format problem`, a `latest-evidence problem`, an `execution problem`, or a `persistent-style problem`. If the answer format often drifts, you should check whether this is about input structure and format guidance before thinking about large adjustment. If policy numbers and dates use old standards, the core issue may be missing latest document evidence, not tone. If calculation results or current-state lookups are often wrong, you need to check execution and lookup signals rather than text improvement. If the same domain style is not maintained across repeated requests, the scene may need persistent style adaptation more than latest evidence.

The important point is not choosing `which technique looks better`. It is first reading `what is missing` as `format`, `evidence`, `execution`, or `persistent adaptation`.

Common confusions here include the following.

- It is easy to view missing latest information and format drift as the same problem.
- It is easy to mistake execution-accuracy problems for tone or explanation-length problems.
- It is easy to feel that repeated style problems can be solved with latest-document connection.

Therefore, the standard `failure-cause classification comes before technique names` must become an actual selection habit.

If we first mark the signals briefly by hand as follows, it becomes clearer what the Python example is trying to compute.

| Failure scene | Format | Evidence | Execution | Persistent adaptation | First reading direction |
| --- | --- | --- | --- | --- | --- |
| Summary format changes every time | Large | Small | Small | Some | First look at input instructions and output examples |
| Latest policy number is wrong | Small | Large | Some | Small | First look at document retrieval and source connection |
| Total calculation is wrong | Small | Some | Large | Small | First look at calculation tools or connected lookup results |
| The same domain style repeatedly drifts | Some | Small | Small | Large | Check whether repeated style adjustment is needed |

This table is not an answer key. It is observation practice. Even in the same scene, the marks can change depending on company risk, user requirement, and data-access permission. But if the marks change, the priority of support paths seen later should also change.

The next three scenes intentionally do not show only one signal. First mark the `first-priority shortage` and `second-priority shortage` yourself, then compare with the explanation.

| Scene | First-priority shortage | Second-priority shortage |
| --- | --- | --- |
| A customer-support answer gets the latest refund deadline in company policy wrong, and its tone also differs from the brand voice |  |  |
| A sales-summary answer uses the correct table format, but the total is wrong and the file used for calculation is unclear |  |  |
| A contract summary cites the latest clauses well, but the summary order changes every time and the reviewer must reorganize it |  |  |

Explanation:

| Scene | Shortage to check first | Shortage to check next | Reason |
| --- | --- | --- | --- |
| Refund-deadline error and brand-tone drift | Evidence | Persistent adaptation | The latest-policy error is a factual failure that must be reduced first, and brand tone is the next problem for stabilizing repeated response quality |
| Table is correct, but total and source file are unclear | Execution | Evidence | The total is a calculation-execution problem, and which file was used is an evidence-connection problem |
| Latest clauses are correct, but summary order drifts | Format | Persistent adaptation | The current failure is output-structure instability first, and if it repeats across many contracts, persistent adaptation comes next |

The point of this exercise is not `attach one technique to one scene`. If we split failures and separate first and second priorities, it becomes easier to understand why the Python example looks at both `first_action` and `second_action`.

## Exercise and Example

The goal of this example is to check that even when all problems look like `the LLM is not doing well`, classifying the failure cause changes the first shortage to inspect and the response to postpone. We take five representative failures, read the `format`, `latest evidence`, `execution`, and `persistent style` signals separately, and compare by score which support path should be checked first and which response should be pushed down the priority list.

Input:

The code below uses five representative failure types and observations for format, latest evidence, execution, and persistent style signals in each failure type. The result shows a means score table by problem type, the first support path and second support path to check, the response that should not be first, and a failure-cause classification summary.

Here, the scores are not answer keys produced automatically by a real operating system. They are diagnostic-practice weights for separating `observed failure signals` from `the problem targeted by each support path`. So what matters is not the number itself, but how the first and second support paths change when a signal is raised or lowered.

The key result to check is that prompt revision, fine-tuning, RAG, and tool use are not selected first as technique names. Their support priority changes according to whether the failure cause lies in format, evidence, execution, or persistent adaptation.

```python
# Compare which support path should be checked first by adding scores for each failure signal.
cases = [
    {
        "issue": "format drift",
        "symptom": "answer format often drifts",
        "signals": {
            "format": 3,
            "evidence": 0,
            "execution": 0,
            "persistent_style": 1,
        },
    },
    {
        "issue": "missing latest policy",
        "symptom": "latest policy is often wrong",
        "signals": {
            "format": 0,
            "evidence": 3,
            "execution": 0,
            "persistent_style": 1,
        },
    },
    {
        "issue": "needs calculator",
        "symptom": "calculation result is often wrong",
        "signals": {
            "format": 0,
            "evidence": 1,
            "execution": 3,
            "persistent_style": 0,
        },
    },
    {
        "issue": "persistent domain style",
        "symptom": "style is inconsistent across repeated requests",
        "signals": {
            "format": 1,
            "evidence": 0,
            "execution": 0,
            "persistent_style": 3,
        },
    },
    {
        "issue": "mixed format and policy evidence",
        "symptom": "summary format drifts and latest policy evidence is missing",
        "signals": {
            "format": 2,
            "evidence": 3,
            "execution": 0,
            "persistent_style": 1,
        },
    },
]

weights = {
    "prompt revision": {
        "format": 3,
        "evidence": 0,
        "execution": 0,
        "persistent_style": 1,
    },
    "RAG": {
        "format": 0,
        "evidence": 3,
        "execution": 0,
        "persistent_style": 0,
    },
    "tool use": {
        "format": 0,
        "evidence": 1,
        "execution": 3,
        "persistent_style": 0,
    },
    "fine-tuning": {
        "format": 1,
        "evidence": 0,
        "execution": 0,
        "persistent_style": 3,
    },
}

def score_action(signals, action_name):
    action_weights = weights[action_name]
    return sum(signals[key] * action_weights[key] for key in signals)

action_counter = {}

for case in cases:
    scores = {
        action_name: score_action(case["signals"], action_name)
        for action_name in weights
    }
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best_action, best_score = ranked[0]
    second_action, second_score = ranked[1]
    last_action, last_score = ranked[-1]
    action_counter[best_action] = action_counter.get(best_action, 0) + 1

    print("=" * 70)
    print("issue =", case["issue"])
    print("symptom =", case["symptom"])
    print("signals =", case["signals"])
    print("scores =", scores)
    print("first_action =", best_action, best_score)
    print("second_action =", second_action, second_score)
    print("not_first =", last_action, last_score)

print("[action summary]", action_counter)
```

I ran this example with the local `.venv` Python and confirmed that the output matches the manuscript.

The example output can be read as follows.

```text
======================================================================
issue = format drift
symptom = answer format often drifts
signals = {'format': 3, 'evidence': 0, 'execution': 0, 'persistent_style': 1}
scores = {'prompt revision': 10, 'RAG': 0, 'tool use': 0, 'fine-tuning': 6}
first_action = prompt revision 10
second_action = fine-tuning 6
not_first = tool use 0
======================================================================
issue = missing latest policy
symptom = latest policy is often wrong
signals = {'format': 0, 'evidence': 3, 'execution': 0, 'persistent_style': 1}
scores = {'prompt revision': 1, 'RAG': 9, 'tool use': 3, 'fine-tuning': 3}
first_action = RAG 9
second_action = tool use 3
not_first = prompt revision 1
======================================================================
issue = needs calculator
symptom = calculation result is often wrong
signals = {'format': 0, 'evidence': 1, 'execution': 3, 'persistent_style': 0}
scores = {'prompt revision': 0, 'RAG': 3, 'tool use': 10, 'fine-tuning': 0}
first_action = tool use 10
second_action = RAG 3
not_first = fine-tuning 0
======================================================================
issue = persistent domain style
symptom = style is inconsistent across repeated requests
signals = {'format': 1, 'evidence': 0, 'execution': 0, 'persistent_style': 3}
scores = {'prompt revision': 6, 'RAG': 0, 'tool use': 0, 'fine-tuning': 10}
first_action = fine-tuning 10
second_action = prompt revision 6
not_first = tool use 0
======================================================================
issue = mixed format and policy evidence
symptom = summary format drifts and latest policy evidence is missing
signals = {'format': 2, 'evidence': 3, 'execution': 0, 'persistent_style': 1}
scores = {'prompt revision': 7, 'RAG': 9, 'tool use': 3, 'fine-tuning': 5}
first_action = RAG 9
second_action = prompt revision 7
not_first = tool use 3
[action summary] {'prompt revision': 1, 'RAG': 2, 'tool use': 1, 'fine-tuning': 1}
```

The result to check in this example is that even similar-looking LLM problems produce different first support paths and different paths that do not close well right away when we first separate `what is missing`. In particular, format drift and lack of style consistency can look similar, but one scores higher on input design and the other scores higher on persistent adaptation. Latest-policy errors and calculation errors can both look like `wrong answers`, but one is an evidence-connection shortage and the other is an execution shortage. In a mixed failure, first and second priorities appear together. If missing latest policy evidence is the larger problem, we check RAG first and then clean up format drift with prompt revision.

Readers can directly adjust the example in the following ways.

- Change the `signals` values and check under which conditions the recommended means changes.
- Make the `weights` more conservative and experiment with which failures the organization treats as more serious.
- Add a new scene to `issue`, such as customer support, financial reporting, or internal approval automation.
- Read not only `first_action` but also the second-place score, and check why some problems need a combined response.

When the score table is shown as a graph, the reason each failure type splits toward a different support path becomes clearer. The darkest cell is the path to check first, and the next darkest cell is the second-priority support candidate to keep. Even similar-looking failures change priority depending on which signal is larger among format, evidence, execution, and persistent style.

![Support Path Scores by Missing Signal](/AiBook/assets/part-06/chapter-09/solution-selection-score-map-en.png)

## Support Paths Split by the Diagnostic Map

This example shows that reading failures again as `format`, `evidence`, `execution`, and `persistent adaptation` matters more than memorizing and choosing among four paths. In real systems too, we should not classify a problem directly by technique name. We should first collect observation signals about what was missing. Only then can we avoid mixing problems that require longer prompts, document evidence, calculation tools, or a stronger long-term adjustment layer.

## Support Paths by Failure Type

Prompts, fine-tuning, RAG, and tool use are not competing universal solutions. They are different means that should be pulled out first depending on `which shortage caused the failure`.

## Checklist

- Can you divide a failure again into `format`, `evidence`, `execution`, and `persistent adaptation`?
- Can you explain that prompts, fine-tuning, RAG, and tool use are not competing solutions but target different shortages?
- Are you ready to read the following chapters as detailed chapters inside a diagnostic map, rather than as a list of techniques?

## Sources and References

- OpenAI Academy, `Prompting fundamentals`, accessed 2026-07-19. [https://openai.com/academy/prompting/](https://openai.com/academy/prompting/){: target="_blank" rel="noopener noreferrer" }
- Patrick Lewis et al., `Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks`, NeurIPS, 2020, accessed 2026-07-19. [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401){: target="_blank" rel="noopener noreferrer" }
- Jason Wei et al., `Finetuned Language Models Are Zero-Shot Learners`, arXiv, 2021, accessed 2026-07-19. [https://arxiv.org/abs/2109.01652](https://arxiv.org/abs/2109.01652){: target="_blank" rel="noopener noreferrer" }
