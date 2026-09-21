# P3-6.6 Same Column Name, Different Feature

> Section ID: `P3-6.6`
> Version: `v2026.09.20`

_Subtitle: Why can a column with the same name become a different feature when its measurement rule or unit changes?_

There is one more trap that is easy to miss while designing [features](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature). It appears the moment we think `if the column name is the same, it must be the same feature`. But in real data, even under the same name `flow_mean`, the sensor version may have changed, the unit may have changed, or the calculation rule may have changed. Once such changes happen, the numbers may still exist, yet it becomes difficult to say that it is still the same feature.

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

## Comparing Measurement Definitions Beyond Column Names {#looking-through-a-small-diagram}

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

If only units differ, conversion can restore comparability. Since `41 mL/s = 41×60/1000 = 2.46 L/min`, C's value is not about 17 times A's. This does not establish that sensor location, calibration, or calculation intervals match, so check those conditions even after standardizing units. If only an operational judgment rule changed, the original physical feature may be unchanged while the output label's meaning differs.


## Separate Matching Strings from Physical Comparability {#small-code-example}

The four rows are fictional. Matching notes for A and B do not verify sensor locations, calibration history, or missing-data handling. The name `early-mid-late` also does not fully specify which observations were averaged and how. Matching metadata gathers candidates for review; it does not certify comparability.

| Level checked | What this example establishes | What still needs checking |
| --- | --- | --- |
| Selected definition strings match | A and B have the same recorded fields | Omitted locations, calibration, and averaging rules |
| Units converted | C=2.46 and D=2.37 L/min | Correspondence of measurement targets and calibration for v1/v2 sensors |
| Segment-definition difference found | D uses the different rule name quartile-4bin | Whether raw data can be aggregated over the same scope |
| Operational-rule version differs | D uses normal-band-v2 | Whether measurement changed or only decision thresholds changed |

D converts as `39.5×60/1000=2.37 L/min`. Its closeness to A's 2.4 does not establish identical measurement definitions. Unit conversion restores numeric comparability when units alone differ and the measurement target, location, calibration, and aggregation rules are confirmed equivalent. Sensor changes require corresponding measurements or calibration records; segment changes require exact boundaries and a check on whether reaggregation is possible.

## Record Operational Decisions Separately from Measurement Definitions

Consider a fictional change from a decision threshold of “at least 2.50 L/min” to “at least 2.40 L/min,” with physical measurement rules unchanged. A measured 2.46 L/min stays the same, while its decision changes from below to above threshold. That is a rule change, not a measurement change. The actual normal-band-v1/v2 thresholds are absent from the table, so these numbers do not define those versions.

| Record category | Examples of items to retain |
| --- | --- |
| Measurement and aggregation | Quantity, sensor location/version, calibration history, segment boundaries, averaging method, missing-data handling |
| Unit conversion | Original value/unit, conversion formula, converted value/unit |
| Operational decision | Rule version, effective time, outcome label |

For C, retain the original 41.0 mL/s, formula `×60/1000`, and converted 2.46 L/min. Merely changing the unit label to L/min while leaving 41.0 creates incorrect data. Changing a sensor-version string to v1 also does not perform calibration.

## Fewer Groups Do Not Mean Matched Definitions

Grouping by name alone puts A, B, C, and D together. Comparing unit, sensor version, segment rule, and operational-rule strings produces three groups: A,B / C / D. Removing the operational-rule field still leaves three because D has a different segment rule. Removing both operational and segment rules leaves two groups: A,B / C,D.

Can C and D now share a baseline? Not yet: hiding a segment field did not change how the values were aggregated. Conversely, when evidence shows that only decision rules changed and measurement definitions match, physical-feature comparisons and outcome-label comparisons can be handled separately.

List what is needed to compare C with A. Unit conversion is insufficient: sensor location, calibration, actual segment scope, and averaging rules must correspond. Including D also requires checking whether quartile-4bin and early-mid-late represent the same measurement scope. If raw data is unavailable and definitions cannot be reconciled, hold the comparison or retain separate groups.

## Checklist

- Can you convert C and D to L/min while preserving original values and units?
- Can you distinguish matching metadata strings from actual comparability?
- Can you separate decision-only changes from measurement or aggregation changes?
- Can you explain why reducing group count cannot replace calibration or reaggregation?

## Sources and Further Reading

- W3C, `PROV-Overview`. Because it provides a general framework for tracing through provenance information what process and version generated the data, it reinforces the explanation that to preserve comparability, a feature should keep not only its name but also its generation rule and version. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `feature engineering`. Because it explains that a feature is not a raw value left untouched but the result of a chosen transformation, it supports the core point of this section that once the unit or calculation rule changes, the same column name is no longer easily the same feature definition. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
