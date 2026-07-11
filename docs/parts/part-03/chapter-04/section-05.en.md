# P3-4.5 How Well Does the Sample Set We Collected Represent the Overall Operating Situation

> Section ID: `P3-4.5`
> Version: `v2026.07.11`

Once the sample unit has been fixed as something like one full action or one recent segment, one more question remains that is easy to miss. `How well does the sample set we collected represent the overall operating situation?` Even if the table itself is well organized, if the cases in it were gathered only from a specific process mode, a specific time period, or a specific equipment state, then the table may fail to describe the overall operating scene evenly. Choosing the sample unit correctly and having a sample bundle that evenly represents the whole situation are not the same thing.

## What Must the Representativeness of the Sample Bundle Be Distinguished From

The problem of representativeness asks, separately from whether the definition of one sample is correct, what operating range the sample bundle actually covers.

| What the situation looks like on the surface | The question that should be asked first in Part 3 |
| --- | --- |
| The sample unit is well organized | Under what operating conditions were the samples gathered? |
| Feature and label candidates also exist | Are they concentrated only in one specific period or one specific mode? |
| The number of rows also looks sufficient | Does the bundle evenly cover the whole operating scene? |

In other words, `the definition of one sample` and `the representativeness of the sample bundle` are different problems.

## Representative Scenes Where Representativeness Becomes Weak

Even if all samples are the same unit of `one full action`, representativeness can still differ depending on from which range they were gathered.

| Current state of the collected samples | Why representativeness may be weak |
| --- | --- |
| Mostly normal operation during the daytime | We barely see night shifts, high-load conditions, or transition intervals |
| Mostly after-maintenance periods | The usual long-run operating state is represented less |
| Mostly gathered from one specific machine | Differences among machines may be missed |
| Concentrated in only one week of the month | Seasonal patterns, periodic changes, or policy shifts may be missed |

So even if the number of samples is large, representativeness can still be weak when the covered conditions are narrow.

## Four Things Worth Writing Down First

In Part 3, what matters more than formal sampling theory at this stage is to write down the following four things first.

| What to write down first | Turned into a question |
| --- | --- |
| Time range | From what period were the samples collected? |
| Operating-mode range | Under what conditions and states were the samples collected? |
| Equipment / entity range | From which facilities or entities were the samples collected? |
| Missing ranges | What conditions or modes were barely seen? |

These notes are not for proving generalization later. They are for first making visible what the current table does represent and what it still does not represent.

## A Small Diagram

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-5-mermaid-01-en.mmd"
```

This diagram shows that even if every sample unit is consistently `one full action`, the operating range it covers can still be tilted to one side. In other words, the point of this section's example is not to read many raw table values, but to identify first `which conditions are overrepresented and which conditions are nearly empty`.

## Why This Problem Has to Come After the Sample Unit

The problem of representativeness can only be read after the sample unit has first been fixed. If it is still unclear whether one row means a time-point record or one full action, then questions such as `how many night-shift actions are there?` or `how many high-load-condition samples are there?` cannot even be counted properly.

So the order is as follows.

1. First decide what will count as one sample.
2. Then check what condition range those samples actually cover.

Only after these notes are left behind can we later read results together with `from what condition range was this sample bundle obtained?`, and avoid missing `what operating conditions were barely seen?` In that sense, the problem of representativeness is close to the problem of first writing down what the current sample bundle covers and what it misses.

## Small Code Example

Problem situation: even if all sample units are correctly aligned as `one full action`, check which conditions the actual sample bundle is tilted toward.

Input: an action-sample table containing `shift`, `load_mode`, `machine_id`, and `maintenance_phase`

Expected output: a `coverage summary` showing which conditions were seen a lot and which were barely present

Concept to check: the correctness of one sample definition and the even representativeness of the sample bundle over the whole operating range are different problems

```python
import pandas as pd

samples = pd.DataFrame(
    [
        {"event_id": "A", "shift": "day", "load_mode": "normal", "machine_id": "M1", "maintenance_phase": "stable"},
        {"event_id": "B", "shift": "day", "load_mode": "normal", "machine_id": "M1", "maintenance_phase": "stable"},
        {"event_id": "C", "shift": "day", "load_mode": "high", "machine_id": "M1", "maintenance_phase": "stable"},
        {"event_id": "D", "shift": "day", "load_mode": "normal", "machine_id": "M2", "maintenance_phase": "stable"},
        {"event_id": "E", "shift": "night", "load_mode": "normal", "machine_id": "M1", "maintenance_phase": "stable"},
        {"event_id": "F", "shift": "day", "load_mode": "normal", "machine_id": "M1", "maintenance_phase": "after-maintenance"},
    ]
)

coverage = pd.DataFrame(
    [
        {"scope": "shift", "most_seen": samples["shift"].value_counts().idxmax(), "count": samples["shift"].value_counts().max(), "least_seen": samples["shift"].value_counts().idxmin()},
        {"scope": "load_mode", "most_seen": samples["load_mode"].value_counts().idxmax(), "count": samples["load_mode"].value_counts().max(), "least_seen": samples["load_mode"].value_counts().idxmin()},
        {"scope": "machine_id", "most_seen": samples["machine_id"].value_counts().idxmax(), "count": samples["machine_id"].value_counts().max(), "least_seen": samples["machine_id"].value_counts().idxmin()},
        {"scope": "maintenance_phase", "most_seen": samples["maintenance_phase"].value_counts().idxmax(), "count": samples["maintenance_phase"].value_counts().max(), "least_seen": samples["maintenance_phase"].value_counts().idxmin()},
    ]
)

print("1) raw sample coverage table")
print(samples)
print()
print("2) coverage summary")
print(coverage)
```

Expected output:

```text
1) raw sample coverage table
  event_id  shift load_mode machine_id  maintenance_phase
0        A    day    normal         M1             stable
1        B    day    normal         M1             stable
2        C    day      high         M1             stable
3        D    day    normal         M2             stable
4        E  night    normal         M1             stable
5        F    day    normal         M1  after-maintenance

2) coverage summary
               scope most_seen  count         least_seen
0              shift       day      5              night
1          load_mode    normal      5               high
2         machine_id        M1      5                 M2
3  maintenance_phase    stable      5  after-maintenance
```

What matters in this example is not a classification technique, but making visible at a glance `what the current table sees a lot of` and `what it barely sees`. In step 1, we see which condition combinations actually came in. In step 2, we immediately read what is overrepresented and what is barely visible in each scope. Only then can we explain with both numbers and table why `the sample count is 6, but representativeness is still weak`.

When reading this table, three things should be checked together. Can this table explain the time, mode, and equipment range from which it collected samples? Can we write down the conditions that were barely seen? And later, when reading evaluation scores, can we also bring back to mind this range of representativeness? Only when notes like these are attached does the sample table become not just `an organized table`, but `a table that also records what operating range it represents`.

Fixing the sample unit correctly does not automatically mean that the sample bundle represents the whole operating situation. That is why, in Part 3, the time range, mode range, equipment range, and remaining gaps should all be written down together.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because the example unit has to be fixed before we can ask what set of examples represents the current problem, it strengthens this section's starting point that the definition of one sample and the representativeness of the sample bundle should be read separately. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because it explains that provenance and activity context should be preserved together, it provides the higher-level frame that to explain the range of representativeness, we must be able to trace from what time period, what machine, and what operating mode the current sample bundle came. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. Because it explains that when current performance is compared with past performance, the samples should come from the same essential conditions, it provides a general basis for the claim that before sample count, the operating conditions covered by the data must first be organized. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
