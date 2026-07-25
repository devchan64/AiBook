# P5-13.3 Supplementary Reading: QKV and Multi-Head Attention

> Section ID: `P5-13.3`
> Version: `v2026.07.23`

In P5-13.1 and P5-13.2, we first fixed the intuition of attention and self-attention. Once we have read this far, the next question appears naturally.

Then why, in the actual computation, is attention explained through query, key, and value, and why does multi-head attention get its own name?

When the terms start to scatter again, reread together the glossary entries on [query-key-value (QKV)](/AiBook/en/reference/concept-glossary-alpha/q/#-query-key-value-qkv) and [multi-head attention](/AiBook/en/reference/concept-glossary-alpha/m/#multi-head-attention).

## Questions That Need QKV And Multi-Head Attention

- What do query, key, and value mean?
- Why is self-attention explained by dividing the computation into these three names?
- What does multi-head attention mean by looking several times?
- When reading the Transformer, how much understanding of these concepts is enough?

This supplementary reading focuses on `why are these names used` and `how should we read intuitively the difference between one head and several heads`. The core here is not `do we memorize more formulas`, but `can we reread the intuition of attention we already hold through the repeated names QKV and multi-head`.

## Distinguishing Role Names From Multiple Viewpoints

- You can explain query, key, and value at an introductory level.
- You can read self-attention as `a computation that asks a question, finds the matching position, and brings back the information`.
- You can explain multi-head attention as meaning `relationships are not seen from only one type, but split into several viewpoints`.
- When rereading the Transformer section, you can recall where QKV and multi-head belong.

## If We First Look Through A Very Short Analogy

Query, key, and value can be compared as follows.

| Name | Introductory intuition |
| --- | --- |
| query | what do I want to find right now? |
| key | what label is attached to each position? |
| value | what content will actually be brought back? |

If we rewrite it through a library analogy:

- query: `I want to find a history book right now`
- key: `each book card has a label such as history, science, or novel`
- value: `the actual content of the book that will be read and brought back`

That is, attention is a computation that, according to `the question needed right now (query)`, finds positions that have a matching `label (key)` and then brings back more of the `actual content (value)` from there.

If we read it immediately in the context of an operation memo, it becomes clearer.

| The same operation-memo scene | What is read like a query | What is read like a key | What is read like a value |
| --- | --- | --- | --- |
| `Release of shutdown was requested. However, pressure recovery has not yet been completed.` | the question the current representation asks again: `what is still incomplete?` | the labels that reveal what kind of information each position holds, such as `shutdown release`, `pressure recovery`, and `not yet completed` | the actual meaning content of `release requested` and `recovery incomplete` that must be mixed back into the current representation |
| shift handoff summary | the question of whether the current summary expression is `a final decision, a basis, or a condition` | labels showing whether each sentence is closer to `conclusion`, `abnormal sign`, or `safety condition` | the contents of the decision, basis, and condition that must actually remain in the final summary |
| reading maintenance code | the question `where did this value come from?` that the current line asks again | the labels showing the role of variable definitions, conditions, and function calls | the definition-use relationship and call context that must actually be mixed back into the current line interpretation |

That is, the reason QKV is given separate names is to read separately `what is being searched for now`, `what kind of information each position is`, and `what will actually be brought back and used to change the representation`. This section is the place to hold why these role names are needed, not the place to deal with matrix dimensions and implementation optimization.

## What Changes Inside Self-Attention

In P5-13.2, we explained self-attention as `a method in which tokens inside the same sequence refer to one another and recalculate their representations`. When we attach QKV to that description, we rewrite the same idea in a slightly more computation-friendly form.

- the current token sends out a query meaning `what do I need right now?`
- every token has a key meaning `what kind of information am I?`
- every token has a value meaning `what is the actual content I can provide?`

That is, the current token compares its own query with the keys of the other tokens to decide `whom should I refer to more`, and then creates a new representation by taking a weighted average of the values of those tokens.

If we draw this flow very simply, it becomes the following.

```mermaid
--8<-- "assets/part-05/chapter-13/qkv-flow-en.mmd"
```

This diagram compresses the following sequence of computation.

1. The current token asks a question.
2. It compares which token labels match that question better.
3. It gives larger weights to the better-matching positions.
4. It mixes in more of the actual content (value) from those positions and forms a new representation.

## Why Separate Key And Value At All

At the introductory level, the natural question here is, `it is one token anyway, so why call key and value separately?`

The core reason is that `the criterion used to search` and `the content to be brought back` can play different roles.

For example, suppose we want to find `the final decision of this shift` in a shift-handoff record.

- words such as `decision`, `approved`, and `hold` are closer to labels used as the search criterion
- what the model actually needs to bring back is the meaning representation contained in the sentence as a whole

That is, the key is closer to `the label used to decide how much to refer to this position`, while the value is closer to `the content that is actually mixed in to form a new representation`.

If we reduce this distinction to one sentence, it becomes the following.

`The key is closer to deciding where to look, and the value is closer to deciding what to actually bring back.`

## If We Look Again Through A Small Sentence

```text
Release of shutdown was requested. However, pressure recovery has not yet been completed.
```

If the current token is trying to understand the context after `however`, the query can act like a question asking `what forms the contrast here right now?` At that time, the two expressions `release of shutdown requested` and `pressure recovery incomplete` provide different keys, and the position that matches the current query better receives a larger weight. Then more of the value at that position is mixed in and the current representation is updated.

That is, in self-attention, one token works by `scanning the whole sentence again and selecting and mixing the cues needed for my interpretation right now`.

## What Does Multi-Head Attention Mean By Looking Several Times

Now the next question appears.

If one round of attention is enough, why do we need `multi-head`?

The core point is that the model does not look at only one kind of relationship, but instead splits token relationships across different viewpoints.

`Instead of looking at only one kind of relationship, let us read the relationships several times from different viewpoints.`

For example, in a sentence, even the same token can participate in multiple important relationships at once.

- one head may see subject-verb relationships better
- one head may see modifier-target or referring-expression relationships better
- one head may see nearby token combinations better, while another may see more distant token connections better

That is, multi-head attention is `a device that, instead of seeing only one correct relationship, splits and reads several kinds of relatedness`.

The table below compares directly the difference in relationship information left by single-head and multi-head in the same scene.

| The same scene | What tends to remain first when read only once like a single head | What tends to remain first when read from several viewpoints like multi-head |
| --- | --- | --- |
| procedure-document transformation | only one most noticeable relationship remains, so modifier scope or exception conditions can weaken | subject-action, modifier scope, and contrast relationships can be seen separately together |
| shift-handoff summary | one line of conclusion may remain, but the basis or the condition can weaken together | conclusion, basis, and condition are easier to preserve by splitting them into different relatedness patterns |
| maintenance-code understanding | it can become biased toward one kind of signal such as repeated variable names | definition-use, condition-result, and call flow are easier to read together from different viewpoints |

## If We Look Through A Diagram

```mermaid
--8<-- "assets/part-05/chapter-13/multihead-flow-en.mmd"
```

The key point in this diagram is not `the input is split into several pieces`, but `the same input is read from several viewpoints and then the results are combined again`.

If we place the same judgment sentence side by side in the feel of single-head and multi-head, it can be seen briefly as follows.

```mermaid
--8<-- "assets/part-05/chapter-13/single-vs-multihead-baseline-en.mmd"
```

The first points to hold from this comparison diagram are the following.

- single-head tends to fold `decision`, `basis`, and `condition` into one compromise context
- multi-head can leave the same input split into different relatedness patterns such as `decision-side relationship` and `condition-side relationship`
- only when this feel is fixed can multi-head be read not as `attention repeated several times`, but as `a structure that preserves different kinds of relationships separately`

## Cases And Examples

In the cases of this section, what must be read first is not only `looking again at a distant position`, but `what kinds of relationships have to be carried separately`. That is, even when reading the same sentence, we need to distinguish whether `decision`, `basis`, `condition`, and `definition-use` are folded into one average context, or carried separately across different viewpoints.

### Representative Case. Procedure-Document Transformation

When turning a long procedure document into a work instruction, people often feel that it is enough to match the meaning of each word one by one. But in reality, subject-action relationships, modifier scope, negation, and exception conditions can all matter at the same time. For example, there are scenes where, to build the instruction correctly, we must look at both `what modifies what` and `what stands in contrast to what`. If only one round of attention reads all relationships as one single type, important distinctions can mix together. Multi-head attention gives the intuition of reading different relationships separately, so it is useful for explaining scenes where several grammatical cues in a procedure document must all be reflected together.
So the result to confirm in this case is whether the current instruction phrase does not follow only one relationship, but keeps both the subject-action relationship and the scope of exception conditions as different viewpoints so the actual work order is less distorted.

The same viewpoint extends directly to organizing shift-judgment sentences and reading maintenance code. But the core point to hold in this section is not the domain name, but `whether relationships that are easy to compromise into one context are instead preserved separately across different heads`.

```mermaid
--8<-- "assets/part-05/chapter-13/multihead-decision-condition-case-flow-en.mmd"
```

This diagram compresses the difference between a scene where the same judgment sentence is compromised under single-head and a scene where it is split again under multi-head into decision, basis, and condition relationships.

| Standard that is easy for a person to see first | Standard to reread from the single-head viewpoint | Standard to reread from the multi-head viewpoint |
| --- | --- | --- |
| it feels as if a procedure document is fine as long as a few key words are matched | one strongest relationship remains, and modifier scope or exception conditions can be compromised into one context | different heads can split and hold subject-action, modifier scope, and contrast relationships separately |
| it feels as if a shift-judgment sentence is fine as long as the conclusion word is caught | one conclusion-centered signal can pull the average context while the basis and condition weaken | conclusion, basis, and condition can be split into different relatedness patterns and preserved longer |
| it feels as if code is readable as long as variable names continue | definition-use, condition-result, and call flow can be mixed into one compromise representation | different heads read different connection patterns separately so the model is not pulled toward only one kind of signal |

Across the three cases, the common result to confirm is that relationships are not read as only one line, but are seen separately from several viewpoints. In procedure-document transformation, it is enough to check whether the subject-action relationship and the exception condition remain together; in shift-judgment sentences, whether the conclusion, basis, and condition all remain; and in code, whether the definition-use and condition-result relationships both continue.

The final result to confirm across these cases is also clear. The difference of multi-head lies not in `attention runs several times`, but in the fact that different relationships that would easily be folded into one context in a single head are divided across different heads and preserved for longer.

## Practice And Example

The goal of this example is to experiment directly, even with the same token sequence, how different heads read different relationships and how that difference grows or shrinks depending on changes in head weights.

This time, we separate short operating-report fragments into a CSV and read them from there. When fragments such as `shutdown decision`, `pressure anomaly`, and `return condition` appear, the core point is whether single-head tends to fold them into one compromise context, while multi-head can keep viewpoints such as `decision side` and `condition side` separated.

Input:

- [`qkv-multihead-report-scenarios.csv`](/AiBook/assets/part-05/chapter-13/qkv-multihead-report-scenarios.csv){ .csv-preview }
- 4 operating reports, 3 head scenarios, 36 token rows
- token-level meaning axes `decision_axis`, `evidence_axis`, `condition_axis`
- comparison baseline `single_weight` and the two heads' `head1_weight`, `head2_weight`

Output:

- the single-head context for each scenario
- the head 1 and head 2 contexts for each scenario
- the difference from the single-head baseline for each head
- a separation measure showing how differently the two heads read relationships

Problem situation:

- because multi-head attention can sound abstract if explained only in words, it helps to compare directly how much the relationship split actually grows when the heads are made more different

Concepts to confirm:

- different heads can emphasize different relationships even over the same token sequence
- if the head weights are similar, multi-head also becomes closer to compromise, and if they are farther apart, relationship separation grows
- by combining the results of several heads, a richer representation than single-head can be formed

A CSV row means `how much one token fragment is reflected in single-head and two heads in one scenario for one operating report`. The code below selects only the `ops_pressure_return` report and compares its three scenarios.

First look at part of the CSV.

| report_id | scenario | token | relation_role | decision_axis | evidence_axis | condition_axis | single_weight | head1_weight | head2_weight |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ops_pressure_return | balanced_heads | 정지결정 | decision | 1.0 | 0.0 | 0.0 | 0.4 | 0.45 | 0.30 |
| ops_pressure_return | balanced_heads | 압력이상 | evidence | 0.0 | 2.0 | 0.0 | 0.3 | 0.30 | 0.30 |
| ops_pressure_return | balanced_heads | 복귀조건 | condition | 3.0 | 0.0 | 1.0 | 0.3 | 0.25 | 0.40 |
| ops_pressure_return | decision_vs_condition_split | 정지결정 | decision | 1.0 | 0.0 | 0.0 | 0.4 | 0.70 | 0.10 |
| ops_pressure_return | decision_vs_condition_split | 복귀조건 | condition | 3.0 | 0.0 | 1.0 | 0.3 | 0.10 | 0.60 |
| ops_pressure_return | condition_heavy_both_heads | 복귀조건 | condition | 3.0 | 0.0 | 1.0 | 0.3 | 0.55 | 0.65 |

Input:

Read the CSV above and compare the three head-weight scenarios of the `ops_pressure_return` report.

Before looking at the code, it helps to predict first how much relationship separation each scenario will leave. That makes the difference between `one compromised context` and `several separated relationships` clearer.

| Comparison item | Output to predict first | Why that is the prediction |
| --- | --- | --- |
| `balanced_heads` | the difference between `head1_context` and `head2_context` is likely to stay relatively small | because both heads mix `shutdown decision`, `pressure-anomaly basis`, and `restart condition` in similar proportions |
| `decision_vs_condition_split` | the difference between `head1_context` and `head2_context` is likely to become the largest | because one head pushes the decision side and the other pushes the condition side, reopening strongly the difference that a single head would fold together |
| `condition_heavy_both_heads` | both heads are likely to lean toward the back side, so the difference from single-head may be smaller | because the two heads both emphasize the same condition-side relationship rather than different viewpoints |
| `head_separation` | `decision_vs_condition_split` is likely to be the largest | because when different heads truly read different kinds of relationships, the separation becomes larger |

The purpose of this table is not to calculate the exact vector values in advance. It is to help hold before the code that multi-head is not simple repetition, and that depending on how the heads are designed, `relationship separation` can grow or return toward compromise.

```python
from pathlib import Path
import csv
import math

DATA_PATH = Path("docs/assets/part-05/chapter-13/qkv-multihead-report-scenarios.csv")
FOCUS_REPORT_ID = "ops_pressure_return"
CONTEXT_AXES = [
    ("decision_axis", ["decision_axis"]),
    ("evidence_condition_axis", ["evidence_axis", "condition_axis"]),
]

with DATA_PATH.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

focus_rows = [row for row in rows if row["report_id"] == FOCUS_REPORT_ID]
scenario_names = []
for row in focus_rows:
    if row["scenario"] not in scenario_names:
        scenario_names.append(row["scenario"])


def weighted_context(scenario_rows, weight_column):
    return [
        sum(
            float(row[weight_column]) * sum(float(row[column]) for column in source_columns)
            for row in scenario_rows
        )
        for _, source_columns in CONTEXT_AXES
    ]


def vector_diff(left, right):
    return [left_value - right_value for left_value, right_value in zip(left, right)]


def l2_distance(left, right):
    return math.sqrt(sum((l - r) ** 2 for l, r in zip(left, right)))


def summarize_scenario(name):
    scenario_rows = [row for row in focus_rows if row["scenario"] == name]
    single_head_context = weighted_context(scenario_rows, "single_weight")
    head1_context = weighted_context(scenario_rows, "head1_weight")
    head2_context = weighted_context(scenario_rows, "head2_weight")
    difference_from_single = vector_diff(head1_context, single_head_context) + vector_diff(
        head2_context, single_head_context
    )
    head_separation = l2_distance(head1_context, head2_context)

    print(f"[{name}]")
    print("tokens =", [row["token"] for row in scenario_rows])
    print("single_head_context =", [round(value, 3) for value in single_head_context])
    print("head1_context       =", [round(value, 3) for value in head1_context])
    print("head2_context       =", [round(value, 3) for value in head2_context])
    print("difference_from_single =", [round(value, 3) for value in difference_from_single])
    print("head_separation =", round(head_separation, 3))
    print()


print("csv_rows =", len(rows))
print("focus_report_rows =", len(focus_rows))
print("context_axes =", [name for name, _ in CONTEXT_AXES])
print()

for scenario_name in scenario_names:
    summarize_scenario(scenario_name)
```

In the output, start by looking at how `head_separation` and `difference_from_single` change across scenarios.

```text
csv_rows = 36
focus_report_rows = 9
context_axes = ['decision_axis', 'evidence_condition_axis']

[balanced_heads]
tokens = ['정지결정', '압력이상', '복귀조건']
single_head_context = [1.3, 0.9]
head1_context       = [1.2, 0.85]
head2_context       = [1.5, 1.0]
difference_from_single = [-0.1, -0.05, 0.2, 0.1]
head_separation = 0.335

[decision_vs_condition_split]
tokens = ['정지결정', '압력이상', '복귀조건']
single_head_context = [1.3, 0.9]
head1_context       = [1.0, 0.5]
head2_context       = [1.9, 1.2]
difference_from_single = [-0.3, -0.4, 0.6, 0.3]
head_separation = 1.14

[condition_heavy_both_heads]
tokens = ['정지결정', '압력이상', '복귀조건']
single_head_context = [1.3, 0.9]
head1_context       = [1.85, 1.05]
head2_context       = [2.1, 1.05]
difference_from_single = [0.55, 0.15, 0.8, 0.15]
head_separation = 0.25
```

The first result to look at in this example is `head_separation` by scenario. In `decision_vs_condition_split`, the two heads truly split toward the decision side and the condition side, so the separation is the largest. In `condition_heavy_both_heads`, even though there are two heads, they both look toward the same condition side, so the degree of separation is small.

![Head separation by scenario](/AiBook/assets/part-05/chapter-13/qkv-head-separation-en.png)

The second result is where the single-head context and the head 1 and head 2 contexts separate on the coordinate space. The gray point is the same single-head baseline, and the greater the distance between the blue triangle and the orange square, the more we can see that the two heads are reading different relationships.

![Context positions of the single head and the two heads](/AiBook/assets/part-05/chapter-13/qkv-head-context-space-en.png)

| Output to look at first | What this output means | What changes if you vary it |
| --- | --- | --- |
| `head_separation` is large | it means the two heads are truly reading different relationships | if the head weights are made more similar, the degree of separation decreases; if they are made more different, it increases |
| `difference_from_single` spreads in two directions | it means the difference that was folded into the average in a single head is split again in multi-head | if the single-head baseline weights change, we can compare what differences are already absorbed into the `compromise result` |
| both heads grow in the same direction | even with two heads, they may still be redundantly looking at the same relationship | if both heads are pushed toward the same side as in `condition_heavy_both_heads`, the separation advantage of multi-head decreases |

| Reading standard | Easy judgment if we only look at the single-head output | Judgment that changes after comparing scenarios |
| --- | --- | --- |
| operating-report summarization | `shutdown decision`, `pressure anomaly`, and `restart condition` can remain only as one average lump, weakening what is conclusion and what is condition | if the heads are separated as in `decision_vs_condition_split`, conclusion and condition can be carried as different contexts for longer |
| interpreting a procedure document | it is easy to feel that if there are several heads, the relationships will automatically diversify | `condition_heavy_both_heads` shows that even with two heads, if both emphasize the same condition side, the relationship split may still be small |
| experiment design | it is easy to feel that multi-head is understood once one value is seen | only by placing `balanced_heads`, `decision_vs_condition_split`, and `condition_heavy_both_heads` side by side does it become clear that the core is `how differently the heads are set` |

That is, if single-head folds several relationships into one compromise representation, multi-head keeps the results of different relationship readings side by side so differences that disappear in a single average can survive for longer. But that effect depends more on `how differently the heads actually read relationships` than on `the number of heads itself`.

If we translate these numbers into operating-report reading, `balanced_heads` is still close to a compromise summary, while `decision_vs_condition_split` is closer to a reading that keeps `the decision-side context` and `the condition-side context` separated. In contrast, `condition_heavy_both_heads` is a scene where, even with two heads, both are pulled toward the condition side, so the advantage of multi-head is reduced. What matters is not the vector values themselves, but `what kinds of judgments different heads leave separately`.

Real multi-head attention later includes more precise combinations including linear transformations, but at the introductory stage it is enough to hold the feel that `different relationship-reading results are kept side by side`, and that `how the heads are separated matters`.

This example is better treated not as something to run once and stop, but as something to tweak through the following three manipulations and check when `relationship separation` grows and when it shrinks.

| Value to change right now | Output to observe | Question to interpret |
| --- | --- | --- |
| make the CSV `head1_weight` and `head2_weight` more similar | `head_separation` | if different heads end up reading almost the same relationship, how much does the advantage of multi-head decrease? |
| tilt the CSV `single_weight` more toward `head1_weight` or toward `head2_weight` | `difference_from_single` | if single-head already reflects one specific relationship strongly, how much does the difference from multi-head shrink? |
| make `condition_axis` larger or smaller in the CSV row for `복귀조건` | `head2_context`, `head_separation` | if the strength of the token's own meaning changes, which head pulls that change in more sensitively? |

The numbers above do not implement all of real large-scale multi-head attention, but they clearly show the comparison standard that single-head tends to average several relationships at once into one compromised context, while multi-head keeps the results of different relationship readings side by side and then uses them together, and the experimental standard that head design can magnify or reduce this difference. That is, multi-head attention is not simply `attention repeated several times`, but is closer to `a structure that divides heads so that different patterns of relatedness can be carried simultaneously without being lost`.

What the reader should finally hold in this section is the same. QKV is a set of names that helps us read separately `what is being searched for`, `what label matches it`, and `what is actually brought back`, and multi-head is a structure that, instead of averaging those found relationships at once, keeps different viewpoints such as `decision`, `basis`, and `condition` alive for longer.

## Why Is This Important In The Flow Of Part 5

This supplementary reading is not a detailed implementation memo squeezed in between the attention section and the Transformer section. Rather, it is the place where the intuition already fixed in the main text is connected to `why do these names and structures appear`. The core intuition of attention and self-attention has already been closed in the main text, but because the names QKV and multi-head are repeatedly used in the Transformer chapter, this section is better kept not as a formula memo, but as `an introductory recovery point that rereads the names`. In the next chapter, P5-14.1, we explain where these names sit inside the Transformer block.

## Checklist

- Can you explain that QKV is a set of names used to describe attention computation?
- Can you explain why multi-head attention is read as reference computation from several viewpoints?
- Can you explain query, key, and value as the different roles of `question`, `label`, and `content to bring back`?
- Can you say that multi-head attention is a method that reads several kinds of relatedness together instead of only one kind of relationship?
- Can you explain the difference between single-head and multi-head as `one compromised relationship` versus `simultaneous preservation of several relationship viewpoints`?
- When the names query, key, and value suddenly feel disconnected from the intuition of attention, can you first recall the QKV recovery viewpoint?
- When you need to explain why there are several heads, can you return to the difference between single-head compromise and multi-head multi-view preservation?
- When reading the next Transformer section, are you ready first to ask `why do these names keep repeating as key parts inside the block`?

## Sources And References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Jay Alammar, `The Illustrated Transformer`, checked on 2026-06-30. [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-30. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
