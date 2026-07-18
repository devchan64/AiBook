# P3-3.1 Why Source Data Should Not Be Read as a Learning Problem Right Away

> Section ID: `P3-3.1`
> Version: `v2026.07.17`

When source data first arrives, many people almost reflexively think, `what can we predict with this?` first. Because there is a table, many values, and records measured over time, it feels as if the data could be turned immediately into some learning problem. But that reaction is usually too fast. The table in front of us is more likely not yet `a training dataset`, but merely `recorded source data`, or at best a `dataset candidate`.

Here the first point to fix is that `problem structure` comes before `the learning-problem frame`. We have to make clear the warning that this is not yet the stage for choosing a learning-problem frame such as a prediction problem, a classification problem, or an anomaly-detection problem.

At the entry to this Chapter, the `dataset candidate` viewpoint built in Chapter 2 is narrowed one step further.

| What the previous Chapter left behind | What this Chapter adds | The structure passed to the next Chapter |
| --- | --- | --- |
| the difference between storage structure and a dataset candidate, and the first checks for a new table | the reason source data should not yet be promoted into a learning problem | the judgment that actually fixes the sample unit and table structure |

Consider a situation where, for each automatically executed action, a control-parameter time series and a sensor time series are recorded. When seeing such a table, thoughts like the following arise first.

- Since there are sensor values, this could be turned into an anomaly-detection problem.
- Since action results differ slightly, it could be turned into a classification problem.
- If the time series is long, maybe it can be sent directly into a time-series prediction problem.

These thoughts are not themselves wrong. The problem is that the learning-problem frame appears first while `what counts as one case`, `what we are trying to predict`, and `whether a label actually exists` have not yet been fixed. In that state, the data problem has not been defined yet. The learning-problem frame has merely been imagined before the data itself.

The reason this happens so often is clear. First, when a table is visible, people often accept it immediately as `already organized data`. Second, if prior AI-learning experience has been remembered mostly through learning-problem types, prediction style appears before problem representation. Third, the longer and more complex the raw time series is, the more likely the expectation comes first that `maybe this can be passed directly into a learning problem as it is`.

But if source data is read immediately as if it were already a dataset, important questions are skipped.

| The question that easily comes to mind first | The question that is actually needed first |
| --- | --- |
| Into what learning problem should this be read? | What should count as one sample? |
| What should the label be? | Does a stable label truly exist right now? |
| How should accuracy be improved? | Into what table must this be regrouped so comparison becomes possible? |

This difference is not merely about order. What is needed when source data is first seen is not choosing a learning problem, but `asking again what kind of table this really is`. Depending on whether what we are looking at is time-point measurement records, a summary of one action, or an aggregate of a recent segment, every later explanation of feature, baseline, and target changes.

For example, even after seeing only part of the source data below, the learning-problem frame may jump out too early.

| event_id | second | pressure | flow |
| --- | --- | --- | --- |
| A | 0 | 1.0 | 0.0 |
| A | 1 | 2.0 | 1.4 |
| A | 2 | 2.4 | 1.6 |

Looking only at this table, it is easy to think of words such as `classification problem`, `prediction problem`, or `time-series learning problem`. But we still have not decided whether this table is `a time-point record` or `a one-action table`. So if we choose a learning-problem frame here right away, the format of the problem gets ahead of the problem itself.

## A Small Diagram

It becomes clearer which questions stay empty when source data is escalated too early into a learning problem if the flow is reread as `source records -> empty questions -> sample/label candidate cleanup`.

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-1-mermaid-01-en.mmd"
```

Problem situation: when a time-point log table arrives, check which core questions remain empty if we read it immediately as a learning problem.

Input: a raw log table where multiple time-point measurements are mixed under each `event_id`

Expected output: it becomes visible that `read it as a classification problem right now` and `fill in the missing questions first` produce different results

Concept to check: before source data is read as a learning problem, we first have to decide what `one sample`, `a label candidate`, and `a comparison table` are

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "pressure": 1.0, "flow": 0.0},
        {"event_id": "A", "second": 1, "pressure": 2.0, "flow": 1.4},
        {"event_id": "A", "second": 2, "pressure": 2.4, "flow": 1.6},
        {"event_id": "B", "second": 0, "pressure": 1.1, "flow": 0.1},
        {"event_id": "B", "second": 1, "pressure": 1.7, "flow": 1.0},
        {"event_id": "B", "second": 2, "pressure": 1.9, "flow": 1.1},
    ]
)

print("1) raw log")
print(raw)
print()

print("2) too-early reading")
print("- maybe this is a classification problem")
print("- label column: not found yet")
print("- one training sample: not decided yet")
print()

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        max_pressure=("pressure", "max"),
        mean_flow=("flow", "mean"),
    )
)
print("3) questions that must be settled first")
print("- one sample: one event")
print("- candidate comparison table: one row per event")
print("- label candidate: still not decided")
print()

print("4) event-level table after defining the sample")
print(event_summary)
```

Expected output:

```text
1) raw log
  event_id  second  pressure  flow
0        A       0       1.0   0.0
1        A       1       2.0   1.4
2        A       2       2.4   1.6
3        B       0       1.1   0.1
4        B       1       1.7   1.0
5        B       2       1.9   1.1

2) too-early reading
- maybe this is a classification problem
- label column: not found yet
- one training sample: not decided yet

3) questions that must be settled first
- one sample: one event
- candidate comparison table: one row per event
- label candidate: still not decided

4) event-level table after defining the sample
  event_id  max_pressure  mean_flow
0        A           2.4   1.000000
1        B           1.9   0.733333
```

The core of this example is the difference between steps 2 and 3. In step 2, only the sentence `maybe this is a classification problem` appears first, but in reality there is neither a label column nor even one decided training sample. By contrast, step 3 first fixes the structure `one sample is one action` and `the comparison table is one row per action`. Only after that does a comparable table appear, as in step 4. In other words, if source data is read too quickly as a learning problem, the format of the problem gets fixed first while the still-empty questions remain covered over.

If we place side by side the empty questions left behind when the learning-problem frame jumps out first, the issue becomes clearer.

| The phrase that jumps out first | The question that is still empty |
| --- | --- |
| `anomaly-detection problem` | What exactly will count as an anomaly? |
| `classification problem` | Does a stable label truly exist? |
| `time-series learning problem` | Is one sample one time-point bundle, or one full action? |

The core of this table is not that the name of the learning problem is wrong. The problem is that the questions that have to be answered before that frame are still empty. Data modeling is the front-end design that fills those blanks.

So the most common mistake when source data first arrives is to mistake `record structure` for `learning structure`. The mere existence of time-point logs does not mean a prediction problem has already been defined. Only after we decide how to group those logs, what to keep, and what to compare them against can we accurately use the word dataset. Once the learning-problem frame appears first, that front-end design is easily skipped, and later the sample unit and table structure have to be taken apart and rebuilt. If this section is reread as a problem of managing the moment of `problem escalation`, it becomes even clearer that the key is not `let model names come to mind later`, but the judgment not to escalate prematurely into a learning problem before the sample unit and label candidate are organized.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because it explains that a labeled example consists of features and a label, it supports the claim that source data where neither one sample nor a label has yet been fixed should not be read immediately as a learning problem. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Google for Developers, `Machine Learning Glossary`: `label leakage`. Because it explains a design flaw where a feature becomes a proxy for the label, it strengthens the warning that choosing the problem frame first risks reading not-yet-organized source columns into a bad learning structure. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because the provenance framework explains that it should support identifying an object and representing derivation, it strengthens the higher-level frame that we must first decide what counts as one object and through what transformation a dataset candidate was made. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
