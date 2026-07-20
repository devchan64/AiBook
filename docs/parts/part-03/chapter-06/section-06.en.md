# P3-6.6 Why the Same Column Name May Still Not Mean the Same Feature When the Measurement Rule or Unit Changes

> Section ID: `P3-6.6`
> Version: `v2026.07.20`

There is one more trap that is easy to miss while designing features. It appears the moment we think `if the column name is the same, it must be the same feature`. But in real data, even under the same name `flow_mean`, the sensor version may have changed, the unit may have changed, or the calculation rule may have changed. Once such changes happen, the numbers may still exist, yet it becomes difficult to say that it is still the same feature.

A feature should be judged as the same feature not by column name alone, but by including `what quantity was measured under what rule and in what unit`.

## Cases Where the Same Column Name Does Not Mean the Same Feature

If we look only at the same column name and move on as if it were the same feature, we can easily place rows on the same comparison table and the same baseline even when the meaning of the feature has already changed.

| What it looks like on the surface | The question Part 3 should ask first |
| --- | --- |
| The column name stayed the same | Did the calculation rule and unit also stay the same? |
| The value distribution suddenly changed | Is it a real change, or a change in measurement method? |
| Values changed after maintenance | Is it a process-state change, or a change in sensor definition? |

So the mere fact that the feature name stayed the same does not mean the same comparison structure is still in place.

## What Has to Change Before It Stops Being the Same Feature

Even with the same column name, if one of the following changes, Part 3 should first ask again `is this still the same feature?`

| What changed | Why it matters |
| --- | --- |
| Measurement unit | Because the numerical comparison itself changes |
| Sensor location or sensor version | Because the same name can become closer to a different physical quantity |
| Segment calculation rule | Because even the same average may now be an average over a different range |
| Operational definition | Because even the same `normal range` may now follow a different criterion |

All four of these are not primarily model-technique issues. They are issues of `what the feature we kept actually means`.

## Looking Through a Small Diagram

| event_id | flow_mean | flow_unit | sensor_version | segment_rule | ops_definition |
| --- | ---: | --- | --- | --- | --- |
| A | 2.4 | L/min | v1 | early-mid-late | normal-band-v1 |
| B | 2.5 | L/min | v1 | early-mid-late | normal-band-v1 |
| C | 41.0 | mL/s | v2 | early-mid-late | normal-band-v1 |
| D | 39.5 | mL/s | v2 | quartile-4bin | normal-band-v2 |

If we look at this table, every row uses the same name `flow_mean`, but more than one thing changed at the same time.

1. `A`, `B` and `C`, `D` differ in unit.
2. `C`, `D` also differ in sensor version.
3. `D` also differs in segment calculation rule.
4. `D` also differs in operational definition, so it is hard to tie it immediately to the same baseline note.

So if we read these four rows as one unchanged feature column, the meaning of the feature itself becomes unstable even before we talk about whether the numbers are similar. That is why the conclusion we should hold first here is simple. `The same column name` does not guarantee `the same feature definition`.

```mermaid
--8<-- "assets/part-03/chapter-06/p3-6-6-mermaid-01-en.mmd"
```

## So What Should Be Written Down First at This Stage

In Part 3, it matters more to leave feature-definition notes first than to move immediately into complicated correction techniques.

| Note to write down first | Why it is needed |
| --- | --- |
| Unit | Because we need it to judge whether absolute-magnitude comparison is even possible |
| Generation rule | Because we have to check whether it was built from the same range and the same calculation method |
| Collection version | Because we have to distinguish sensor or pipeline changes |
| Whether direct comparison is allowed | Because we have to decide whether it can be placed on the same baseline right away |

These notes are not here to make the explanation longer. They are the minimum structural information needed to block the illusion of `the same column name`.

## Why Baseline Comparison Also Becomes Unstable

Once it is no longer the same feature, the baseline comparison in Chapter 7 also becomes unstable immediately.

| What we currently see | What may actually be unstable |
| --- | --- |
| A recent value became higher than usual | It may be a unit or sensor change rather than a process change |
| The difference stayed large after maintenance | The baseline group and the measurement definition may have changed |
| Variability grew from a certain point onward | The segment-calculation rule may have changed |

So a baseline is not only a same-group comparison. It should also be a `same feature-definition` comparison. Leaving this note behind lets us check first `did different feature definitions get mixed together?` before jumping to the conclusion that `the model is strange`.

## Small Code Example

Problem situation: check that even when the same column name `flow_mean` is used, it may not be the same feature if unit, sensor version, segment rule, and operational definition differ.

Input: a feature-catalog table where `feature_name`, `unit`, `sensor_version`, `segment_rule`, and `ops_definition` are written together, plus the field bundle `definition_fields_to_check` to use when deciding whether rows share the same definition

Expected output: output where the rows look like one group if we look only at the column name, but split into several `same_definition_group` values when `definition_fields_to_check` includes unit, sensor version, segment rule, and operational definition

Concept to check: feature identity should be judged not at the column-name level alone, but at the definition level that includes measurement unit and generation rule. Which rows can be placed on the same baseline also changes depending on which fields are included in the definition.

```python
# This example checks whether features with the same column name changed measurement rules or units.
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 180)

definition_fields_to_check = [
    "feature_name",
    "unit",
    "sensor_version",
    "segment_rule",
    "ops_definition",
]

feature_catalog = pd.DataFrame(
    [
        {
            "event_id": "A",
            "feature_name": "flow_mean",
            "unit": "L/min",
            "sensor_version": "v1",
            "segment_rule": "early-mid-late",
            "ops_definition": "normal-band-v1",
        },
        {
            "event_id": "B",
            "feature_name": "flow_mean",
            "unit": "L/min",
            "sensor_version": "v1",
            "segment_rule": "early-mid-late",
            "ops_definition": "normal-band-v1",
        },
        {
            "event_id": "C",
            "feature_name": "flow_mean",
            "unit": "mL/s",
            "sensor_version": "v2",
            "segment_rule": "early-mid-late",
            "ops_definition": "normal-band-v1",
        },
        {
            "event_id": "D",
            "feature_name": "flow_mean",
            "unit": "mL/s",
            "sensor_version": "v2",
            "segment_rule": "quartile-4bin",
            "ops_definition": "normal-band-v2",
        },
    ]
)

def summarize_groups(fields):
    grouped = (
        feature_catalog.groupby(fields, as_index=False)
        .agg(
            event_count=("event_id", "count"),
            event_ids=("event_id", lambda values: ",".join(values)),
        )
        .copy()
    )
    grouped["same_definition_group"] = grouped[fields].astype(str).agg("|".join, axis=1)
    return grouped[["same_definition_group", "event_count", "event_ids"]]

name_only_groups = summarize_groups(["feature_name"])
definition_groups = summarize_groups(definition_fields_to_check)
group_comparison = pd.DataFrame(
    [
        {
            "grouping_rule": "feature_name only",
            "group_count": len(name_only_groups),
            "grouped_event_ids": " / ".join(name_only_groups["event_ids"]),
        },
        {
            "grouping_rule": "selected definition fields",
            "group_count": len(definition_groups),
            "grouped_event_ids": " / ".join(definition_groups["event_ids"]),
        },
    ]
)

print("1) same column name, different definition notes")
print(
    feature_catalog[
        [
            "event_id",
            "feature_name",
            "unit",
            "sensor_version",
            "segment_rule",
            "ops_definition",
        ]
    ]
)
print()
print("2) grouping changes when definition fields are included")
print(group_comparison)
print()
print("3) rows that can be treated as the same definition group")
print(definition_groups)
```

Expected output:

```text
1) same column name, different definition notes
  event_id feature_name   unit sensor_version    segment_rule ops_definition
0        A    flow_mean  L/min             v1  early-mid-late  normal-band-v1
1        B    flow_mean  L/min             v1  early-mid-late  normal-band-v1
2        C    flow_mean   mL/s             v2  early-mid-late  normal-band-v1
3        D    flow_mean   mL/s             v2   quartile-4bin  normal-band-v2

2) grouping changes when definition fields are included
                grouping_rule  group_count grouped_event_ids
0           feature_name only            1           A,B,C,D
1  selected definition fields            3       A,B / C / D

3) rows that can be treated as the same definition group
                              same_definition_group  event_count event_ids
0  flow_mean|L/min|v1|early-mid-late|normal-band-v1            2       A,B
1   flow_mean|mL/s|v2|early-mid-late|normal-band-v1            1         C
2    flow_mean|mL/s|v2|quartile-4bin|normal-band-v2            1         D
```

The purpose of this example is not to calculate a new feature. It is to check first `up to what point can rows really be grouped under the same definition even when the column name is the same?` The value to manipulate here is `definition_fields_to_check`. In stage 1, we see that all four rows use `flow_mean` but that the definition notes differ. In stage 2, we see that if we look only at `feature_name`, `A,B,C,D` all look like one group, but if we include unit, sensor version, segment rule, and operational definition, they split into three groups: `A,B`, `C`, and `D`. Stage 3 shows that only `A,B` actually remain in the same definition group, while `C` and `D` each stay separate. So what matters in this section is not the internal key string itself, but first separating which rows are allowed onto the same baseline and into the same comparison table.

The last three things to check here are the following. Are the unit and calculation rule written down? Did we distinguish version changes or sensor changes? Did we mark definition differences that must not be mixed into the same baseline and partition? Only when these three conditions stand together does a feature table remain not as a simple bundle of numbers, but as a structure with comparable definitions attached. Checking whether the current feature table compares only columns that still mean the same thing is exactly the center of this section.

If the measurement unit, sensor version, or calculation rule changes, then the same column name may no longer mean the same feature, so Part 3 should check feature-definition sameness before looking at the numbers. This section can be read not as a trick for managing column names, but as the problem of `feature-definition identity`.


So feature identity should be read not as one line of column name, but as a definition bundle that includes what was built under what rule and version.

## Sources and Further Reading

- W3C, `PROV-Overview`. Because it provides a general framework for tracing through provenance information what process and version generated the data, it reinforces the explanation that to preserve comparability, a feature should keep not only its name but also its generation rule and version. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `feature engineering`. Because it explains that a feature is not a raw value left untouched but the result of a chosen transformation, it supports the core point of this section that once the unit or calculation rule changes, the same column name is no longer easily the same feature definition. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
