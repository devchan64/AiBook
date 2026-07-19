# P3-5.5 How Do We Handle Samples with Missing Values or Empty Segments

> Section ID: `P3-5.5`
> Version: `v2026.07.20`

By the time we reach the stage of turning raw logs into a summary table, questions such as `what if the action existed but some sensor values are empty?` and `if the middle segment is missing, should we discard this sample or use part of it?` appear immediately. At that point, what we should look at first is not how to fill the values, but how much the missing values disturb the sample boundary and the meaning of the features.

The fact that values are missing is not just a cleaning problem. It is a data-modeling signal that asks again `can this sample still be treated as the same kind of case?`

## How Missingness Shakes the Sample Structure

If we look only at the empty values and immediately think `we can just fill NaN`, it becomes easy to miss whether the sample boundary has already collapsed and which features have already lost their meaning. In practice, questions like the following have to be settled much earlier.

| What we currently see | The question Part 3 should ask first |
| --- | --- |
| The whole late sensor segment is empty | Can this sample still be used as one action-level comparison unit? |
| Only a few time points are missing | Can the same structural comparison still be made after building summary values? |
| Only one specific sensor is often missing | Is the missingness itself an operational signal? |

So a sample with missing values is not just `a table with values to fill`. It is `a case where the sample boundary and the meaning of the features have to be checked again`. For a reader first looking at the table, understanding is usually faster when we separate `partial missingness`, `segment missingness`, and `sample-boundary collapse` first.

## Three Distinctions That Must Come First

When values are empty, it is better to distinguish the following three cases before talking about complicated techniques.

| What to distinguish first | Turned into a question |
| --- | --- |
| Are only some values missing? | Is only part of one segment average or one sensor missing? |
| Is one whole segment missing? | Is one entire block among early, middle, and late gone? |
| Has the meaning of the sample itself broken? | Is it hard to treat the whole action as the same kind of case at all? |

This distinction matters because the next judgment changes completely depending on `what we count as being missing`. `Only some values are missing` and `the end of the action is gone` both look like blanks, but the decisions they require later are not the same at all.

## The Same-Looking Missingness Can Be Different Problems

For example, the three situations below all look like `there is no value`, but their actual meaning differs.

| Visible problem | Closer interpretation |
| --- | --- |
| One or two time points are missing | Partial measurement missingness |
| The whole last 20% range is missing | Segment missingness that disturbs structural comparison |
| There is no `event_end`, so the end time itself is unknown | Sample-boundary collapse |

The first case may still be a case where only some information is missing inside the same sample structure. The second directly shakes the meaning of features such as late-phase decline rate. The third may require us to revisit the sample itself, because the start and end of the whole action are not closed at all.

## So What Must Be Decided First at This Stage

Before complicated missing-value imputation techniques, it is more important to write down the following four judgments.

| Judgment to write down first | Why it is necessary |
| --- | --- |
| Will this sample be kept? | To see whether it is still comparable as the same kind of case |
| Which features should not be built? | To block features whose meaning is broken by a missing segment |
| Should the missingness itself remain as a flag column? | Because missingness itself can be an operational signal |
| Does the raw log need to be checked again? | Because this may be not just a blank value but a sample-boundary problem |

So the concern here is closer to `how should we classify the current state of this sample?` than to `how should we fill it?` The usual order of judgment is `whether to keep the sample -> what features must not be built -> whether the missingness itself should remain as a flag column`.

## Looking Through a Small Diagram

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-5-mermaid-01-en.mmd"
```

This diagram shows that we do not treat `being empty` as one single state. The judgment branches according to the location of the missingness and the state of the sample boundary. So the example in this section aims less to reveal values themselves and more to reveal first the judgment structure that branches into `keep`, `exclude features`, and `structural collapse`.

## Why Can the Missingness Itself Remain as a Column

People often think only `blanks should be removed`. But in practice, the missingness itself can have meaning.

| Missing state | Why it can remain as a flag column |
| --- | --- |
| A certain sensor is often missing only under certain conditions | It may signal the operating mode or communication state |
| The range right before the end is often missing | It may be connected to failure in detecting event termination |
| Values are missing only in a certain period | It may be connected to system changes or maintenance state |

So in Part 3, it is also worth checking whether flag columns such as `missing_sensor_flag` or `late_segment_missing` should remain. This does not mean they are already fixed as model inputs. It means we judge whether missingness should remain as structural information instead of being erased immediately.

Once this judgment is made first, we stop mixing together `values that can be filled` and `missingness that has already broken the sample structure`. The key point comes before the name of any processing technique: first separate whether the current sample is still the same comparison unit and whether the missingness itself should remain as structural information.

## Small Code Example

Problem situation: check that not all samples with missing values are in the same state; some only require avoiding certain features, while others have their sample structure itself broken.

Input: the [`p3_5_5_missing_segments.csv`](/AiBook/assets/part-03/chapter-05/p3_5_5_missing_segments.csv){: target="_blank" rel="noopener noreferrer" } file. One row is one action-summary row, and an empty value means that the segment average could not be produced. The policy for keeping partially missing samples is controlled by `keep_partial_samples`.

Expected output: output that organizes `late_segment_missing`, `sample_structure_broken`, `keep_sample`, and `avoid_features` together. If `keep_partial_samples` changes, the keep/drop decision for rows with only partial segment missingness changes.

Concept to check: before filling missing values, we should first classify them as `keep sample`, `exclude features`, or `structural collapse`. Whether partial missingness is allowed should remain as an explicit policy.

```python
import csv
from collections import Counter
from pathlib import Path

keep_partial_samples = True
preview_count = 9

data_path = Path("docs/assets/part-03/chapter-05/p3_5_5_missing_segments.csv")

def parse_optional_float(value):
    return None if value == "" else float(value)

with data_path.open(newline="", encoding="utf-8") as file:
    summary = []
    for row in csv.DictReader(file):
        early = parse_optional_float(row["early_flow_mean"])
        mid = parse_optional_float(row["mid_flow_mean"])
        late = parse_optional_float(row["late_flow_mean"])
        end_detected = int(row["end_detected"])
        late_segment_missing = int(late is None)
        sample_structure_broken = int(end_detected == 0)

        if sample_structure_broken:
            keep_sample = "no"
            avoid_features = "all event-level features"
        elif late_segment_missing and not keep_partial_samples:
            keep_sample = "no"
            avoid_features = "late_drop features"
        elif late_segment_missing:
            keep_sample = "yes"
            avoid_features = "late_drop features"
        else:
            keep_sample = "yes"
            avoid_features = "none"

        summary.append(
            {
                "event_id": row["event_id"],
                "early_flow_mean": early,
                "mid_flow_mean": mid,
                "late_flow_mean": late,
                "late_segment_missing": late_segment_missing,
                "sample_structure_broken": sample_structure_broken,
                "keep_sample": keep_sample,
                "avoid_features": avoid_features,
            }
        )

def fmt(value):
    return "missing" if value is None else f"{value:.2f}"

print("1) missingness flags")
for row in summary[:preview_count]:
    print(
        f'{row["event_id"]}: '
        f'late={fmt(row["late_flow_mean"]):<7} '
        f'late_missing={row["late_segment_missing"]} '
        f'boundary_broken={row["sample_structure_broken"]}'
    )
print(f"... {len(summary) - preview_count} more event summaries")
print()
print("2) sample decision")
for row in summary[:preview_count]:
    print(
        f'{row["event_id"]}: keep={row["keep_sample"]:<3} '
        f'avoid={row["avoid_features"]}'
    )
print()
print("3) decision counts")
for decision, count in sorted(Counter(row["keep_sample"] for row in summary).items()):
    print(f"keep_sample={decision}: {count}")
for feature_group, count in sorted(Counter(row["avoid_features"] for row in summary).items()):
    print(f"avoid={feature_group}: {count}")
```

Expected output:

```text
1) missingness flags
E01: late=1.80    late_missing=0 boundary_broken=0
E02: late=missing late_missing=1 boundary_broken=0
E03: late=missing late_missing=1 boundary_broken=1
E04: late=1.75    late_missing=0 boundary_broken=0
E05: late=missing late_missing=1 boundary_broken=0
E06: late=missing late_missing=1 boundary_broken=1
E07: late=1.82    late_missing=0 boundary_broken=0
E08: late=missing late_missing=1 boundary_broken=0
E09: late=missing late_missing=1 boundary_broken=1
... 27 more event summaries

2) sample decision
E01: keep=yes avoid=none
E02: keep=yes avoid=late_drop features
E03: keep=no  avoid=all event-level features
E04: keep=yes avoid=none
E05: keep=yes avoid=late_drop features
E06: keep=no  avoid=all event-level features
E07: keep=yes avoid=none
E08: keep=yes avoid=late_drop features
E09: keep=no  avoid=all event-level features

3) decision counts
keep_sample=no: 12
keep_sample=yes: 24
avoid=all event-level features: 12
avoid=late_drop features: 12
avoid=none: 12
```

The core of this example is not code that fills values. It is the point that `partial segment missingness` and `sample-structure collapse` are not treated as the same blank. The value to manipulate is `keep_partial_samples`. If it is `True`, rows such as `E02` are kept as samples, but late-drop features are excluded conservatively. If it is changed to `False`, the 12 rows with partial segment missingness are also removed from comparison candidates. Rows such as `E03`, however, have unstable sample boundaries and are hard to use immediately as action-level comparison samples regardless of the policy. In stage 1, we distinguish the location of the missingness. In stage 2, that distinction leads directly to the judgment about `whether to keep the sample` and `what features should not be built`.

The last thing to check here is threefold. Is this sample still the same comparison unit? Have we separated the features that should not be built because of the missingness? Have we decided whether the missingness itself should remain as a flag column? Only when these three conditions stand together does a blank become readable not as a simple cleaning target but as a data-modeling item mixed with judgment about sample structure.

The fact that values are missing is not only a preprocessing problem. It is a data-modeling signal that asks again whether the sample is still the same comparison unit and whether the missingness itself should remain as structural information. So to say that we handle missingness means, before filling blanks, redrawing the boundary that says which samples remain comparable and which should be pulled back from comparison.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example assumes the same unit where features and labels attach, it supports the point that when missingness shakes the sample boundary, we should check first whether the sample is still the same comparison unit before filling values. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `feature engineering`. Because feature engineering is the process of turning raw data into a form more useful for learning and comparison, it reinforces the judgment in this section that features whose meaning is broken by segment missingness should not be built. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because the provenance framework says derivation and processing steps should remain explainable, it provides the higher-level frame that the location of missingness and whether sample structure has collapsed should remain as separate information so that quality and reproducibility can be judged again later. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- scikit-learn developers, `Imputation of missing values`. Because it explains that dropping rows or columns with missing values can lose valuable data and that `MissingIndicator` can preserve information about which values were missing, it supports this section's explanation that we should first decide whether missingness itself should remain as a flag column. [https://scikit-learn.org/stable/modules/impute.html#marking-imputed-values](https://scikit-learn.org/stable/modules/impute.html#marking-imputed-values){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
