# P3-2.2 What Structures Go Inside a Dataset Candidate

> Section ID: `P3-2.2`
> Version: `v2026.09.19`

As the preceding section showed, even a stored dataset may need restructuring for the current question. The next question follows directly: what structures belong inside a rebuilt [dataset candidate](/AiBook/en/reference/concept-glossary-alpha/d/#dataset)? To answer it, Part 3 considers [samples](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample), [features](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature), [baselines](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline), and [output structures](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) together. These terms are better understood as a connected dataset design than as separate items to memorize. Defining one sample lets us construct features; those features determine what to compare with a baseline; and the comparison helps determine the output structure.

What matters especially in this section is reading `output structure`, before it hardens directly into a [target](/AiBook/en/reference/concept-glossary-alpha/t/#target), as a problem-design axis that separates review-oriented results from prediction-oriented target candidates. This is also why a dataset candidate should be read not as the name of one table, but as several connected structures. Only when what counts as the sample, which features are kept, what is compared against the baseline, and what output structure closes the process are all decided together does the meaning of the dataset candidate become clear.

The four elements below form a design framework for this book's state-comparison example. They do not mean every dataset must contain baseline and output columns. An unlabeled image collection is also called a dataset, for example. Features can be directly measured values or categories; they need not always be produced by summary calculations.

With one action as a sample, measured flow or operating mode can come directly from the records, while a mean or slope can be calculated. Here we use mean flow and final-interval slope as features, with past actions under the same conditions as a baseline. The output is `review` or `no_flag` under a specified rule, not a label confirming an actual fault.

The relationship can first be organized in the following table.

| Component | What it means here | The question asked at this stage |
| --- | --- | --- |
| Sample | one case that becomes the basic unit for comparison or learning | What will count as one row? |
| Feature | an observed value, category, or calculated value representing the sample | Which values should remain to make comparison easier? |
| Baseline | the usual structure or reference group against which the recent state is compared | Compared with what does change become visible? |
| Output structure | the result format that a person reads or a model receives next | What final judgment are we trying to produce? |

Seeing these four together reveals why data modeling is more than simple organization. For example, if we have not yet decided whether the sample is `one time-point measurement` or `one full action`, we cannot set features stably either, because features suited to a time-point table differ from features suited to an action-level table. Likewise, if the baseline is not fixed, changes in the recent segment are hard to read. And if the output structure is not fixed as either `creating review candidates` or `emitting prediction labels`, then even the needed comparison remains vague.

So these four elements are not a vocabulary list to memorize separately. They are a design sequence that runs from the front to the back when building a dataset candidate. If the sample drifts, the features drift too. If the features drift, baseline comparison drifts as well. If the comparison drifts, the output structure also drifts. That is why this section first fixes how they connect through a question order.

In practice, the questions connect in the following order.

1. Is what we are comparing one time point, one full action, or a recent segment?
2. Which values or categories should remain to describe that object?
3. What reference should we compare those values with to read changes in this example?
4. Should the final result be emitted as a sentence that a person reads, or as a candidate label that a model will receive?

These four questions correspond respectively to sample, feature, baseline, and output structure. So even when the terms themselves feel blurry, following the question order makes it easier to recover which stage of dataset design we are currently in.

The table below uses recent actions R1, R2, and R3 calculated from the same fictional CSV as the Python example. Each action has six flow records at 0–5 seconds; the final interval is always 4–5 seconds. Flow and means are in L/min; slopes and slope differences are in L/min/s. Values are displayed to two decimal places, while calculations and rules use unrounded values.

| sample_id | mean_flow | late_drop_rate | baseline_mean_flow | baseline_late_drop_rate | baseline_gap | output |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| R1 | 0.83 | -0.32 | 0.94 | -0.05 | -0.27 | `review` |
| R2 | 0.90 | -0.08 | 0.94 | -0.05 | -0.03 | `no_flag` |
| R3 | 0.94 | -0.40 | 0.94 | -0.05 | -0.35 | `review` |

The final slopes of baseline actions B1, B2, and B3 are −0.04, −0.06, and −0.04 L/min/s. Assuming these are usual actions under matching conditions, their mean is `(-0.04−0.06−0.04)/3 = −0.046666… L/min/s`, displayed as −0.05. Baseline mean flow is likewise the mean of the three action-level flow means, displayed as 0.94 L/min.

R1 changes from 0.92 L/min at 4 seconds to 0.60 at 5 seconds. Its slope is therefore `(0.60−0.92)/(5−4) = −0.32 L/min/s`. The baseline difference is **the current slope minus the baseline slope**.

- Reading the displayed values: `−0.32−(−0.05) = −0.27 L/min/s`.
- Before rounding: `−0.32−(−0.046666…) = −0.273333… L/min/s`.
- Interpretation: both slopes indicate decline, but R1 falls about 0.27 L/min/s more steeply than the usual reference. This does not mean flow itself is negative.

Applying the fictional review rule `baseline_gap <= −0.20 L/min/s` assigns `review` to R1 and R3 and `no_flag` to R2. Exactly −0.20 is included: of −0.21, −0.20, and −0.19, only the first two qualify. `no_flag` means this rule did not trigger; it is not confirmation of normal operation or a no-fault label.

`sample_id` identifies the object; `mean_flow` and `late_drop_rate` are its features; `baseline_gap` is a comparison result; and `output` is a review-rule result. Changing the threshold does not change observations, slopes, or baseline differences. It changes the policy deciding what people inspect first from the same numbers. Here we use role tables and calculations to distinguish them; the preceding section's charts explain the slopes on a time axis.

## Connecting Samples, Features, Baselines, and Outputs {#a-small-diagram}

The four structures inside a dataset candidate can be read in one pass when they are compressed into the sequence `sample -> feature -> baseline comparison -> output structure`.

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-2-mermaid-01-en.mmd"
```

Problem situation: check the flow in which one action is treated as one sample, features are written down, the result is compared with the usual baseline, and a final operational output is produced.

Input: the time-step flow log [p3_2_2_event_flow_log.csv](/AiBook/assets/part-03/chapter-02/p3_2_2_event_flow_log.csv), which contains both `baseline` and `recent` periods, and candidate review thresholds `review_gap_thresholds`

One input-file row is the measured flow (`flow`) at a specific second (`second`) of one sample. `sample_id` points to one action, and `period` separates whether that sample belongs to the `baseline` period used to build the usual reference or the `recent` period to be compared.

Expected output: the raw log becomes `sample rows -> feature table -> baseline creation -> recent-sample comparison table -> operational output`, and the number of review candidates changes when different `review_gap_thresholds` are applied

Concept to check: output structure and baseline are not result columns written in advance. They are generated after raw logs are grouped by sample unit, features are calculated, and period roles are separated. Comparing several output criteria reveals how sensitive the operational judgment is to the threshold.

Each action in this CSV is measured at 1-second intervals without missing values, and baseline and recent actions are assumed to share operating conditions. The code checks time intervals before using the last two flow values’ difference as a per-second slope. The CSV does not itself verify matching operating conditions; real data requires a separate check.

```python
# Separate sample features, baseline differences, and review-rule results; no actual fault labels are present.
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

event_log_path = "docs/assets/part-03/chapter-02/p3_2_2_event_flow_log.csv"
selected_review_gap_threshold = -0.20
review_gap_thresholds = [-0.36, selected_review_gap_threshold, 0.0]

event_log = pd.read_csv(event_log_path)
event_log = event_log.sort_values(["sample_id", "second"])
intervals = event_log.groupby("sample_id")["second"].diff().dropna()
if not intervals.eq(1).all():
    raise ValueError("This example requires 1-second observation intervals.")

print("1) raw input shape and first rows")
print("shape:", event_log.shape)
print(event_log.head())
print()

sample_rows = event_log[["sample_id", "period"]].drop_duplicates().reset_index(drop=True)
print("2) sample rows")
print(sample_rows)
print()

feature_table = (
    event_log.sort_values(["sample_id", "second"])
    .groupby(["sample_id", "period"], as_index=False)
    .agg(
        mean_flow=("flow", "mean"),
        late_drop_rate=("flow", lambda values: values.iloc[-1] - values.iloc[-2]),
    )
)
print("3) add features")
print(feature_table.round(2))
print()

baseline = (
    pd.DataFrame(
        [
            {
                "baseline_mean_flow": feature_table.loc[
                    feature_table["period"] == "baseline", "mean_flow"
                ].mean(),
                "baseline_late_drop_rate": feature_table.loc[
                    feature_table["period"] == "baseline", "late_drop_rate"
                ].mean(),
            }
        ]
    )
)
print("4) build baseline from baseline samples")
print(baseline.round(2))
print()

comparison_table = feature_table[feature_table["period"] == "recent"].copy()
comparison_table["baseline_mean_flow"] = baseline.loc[0, "baseline_mean_flow"]
comparison_table["baseline_late_drop_rate"] = baseline.loc[0, "baseline_late_drop_rate"]
comparison_table["baseline_gap"] = (
    comparison_table["late_drop_rate"] - comparison_table["baseline_late_drop_rate"]
)
print("5) compare recent samples with baseline")
print(comparison_table.round(2))
print()

selected_output_table = None
threshold_results = []
for threshold in review_gap_thresholds:
    output_table = comparison_table.copy()
    output_table["output"] = output_table["baseline_gap"].apply(
        lambda gap: "review" if gap <= threshold else "no_flag"
    )
    if threshold == selected_review_gap_threshold:
        selected_output_table = output_table.copy()
    threshold_results.append(
        {
            "review_gap_threshold": threshold,
            "review_count": int((output_table["output"] == "review").sum()),
            "review_samples": ",".join(
                output_table.loc[output_table["output"] == "review", "sample_id"]
            )
            or "none",
        }
    )

print(f"6) final output structure when review_gap_threshold = {selected_review_gap_threshold:.2f}")
print(selected_output_table.round(2))
print()
print("7) threshold sensitivity")
print(pd.DataFrame(threshold_results))
```

Expected output:

```text
1) raw input shape and first rows
shape: (36, 4)
  sample_id    period  second  flow
0        B1  baseline       0  0.80
1        B1  baseline       1  0.92
2        B1  baseline       2  1.02
3        B1  baseline       3  1.04
4        B1  baseline       4  1.00

2) sample rows
  sample_id    period
0        B1  baseline
1        B2  baseline
2        B3  baseline
3        R1    recent
4        R2    recent
5        R3    recent

3) add features
  sample_id    period  mean_flow  late_drop_rate
0        B1  baseline       0.96           -0.04
1        B2  baseline       0.94           -0.06
2        B3  baseline       0.92           -0.04
3        R1    recent       0.83           -0.32
4        R2    recent       0.90           -0.08
5        R3    recent       0.94           -0.40

4) build baseline from baseline samples
   baseline_mean_flow  baseline_late_drop_rate
0                0.94                    -0.05

5) compare recent samples with baseline
  sample_id  period  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap
3        R1  recent       0.83           -0.32                0.94                    -0.05         -0.27
4        R2  recent       0.90           -0.08                0.94                    -0.05         -0.03
5        R3  recent       0.94           -0.40                0.94                    -0.05         -0.35

6) final output structure when review_gap_threshold = -0.20
  sample_id  period  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap   output
3        R1  recent       0.83           -0.32                0.94                    -0.05         -0.27   review
4        R2  recent       0.90           -0.08                0.94                    -0.05         -0.03  no_flag
5        R3  recent       0.94           -0.40                0.94                    -0.05         -0.35   review

7) threshold sensitivity
   review_gap_threshold  review_count review_samples
0                 -0.36             0           none
1                 -0.20             2          R1,R3
2                  0.00             3       R1,R2,R3
```

This example shows how the same raw-log rows gradually become a dataset-candidate structure. First, `event_log` uses `sample_id` and `period` to establish sample rows, and then calculates `mean_flow` and `late_drop_rate` from time-step flow values. Next, only the `baseline` period samples are used to build the baseline, and `recent` period samples are compared against it. The final operational output is not a column that was already present. It is generated from `baseline_gap` and `review_gap_thresholds`. If the threshold is `-0.36`, there are no review candidates. If it is `-0.20`, R1 and R3 become review candidates. If it is `0.0`, all three recent samples become review candidates. In other words, the output column is created by inheriting the preceding stages: `sample definition -> feature calculation -> baseline creation -> baseline comparison -> operational judgment criterion`.

If we dissect the same table a little further, it becomes clearer which of the four structures sits in which cells.

| Column name | Role it plays here | Why it should be read in that role |
| --- | --- | --- |
| `sample_id` | sample identifier | because it points to what was counted as one case |
| `mean_flow`, `late_drop_rate` | features | because they describe the state of the sample |
| `baseline_mean_flow`, `baseline_late_drop_rate` | baseline columns | because they separately record representative values from the usual range |
| `baseline_gap` | baseline-comparison column | because it directly records the difference between the current sample and the usual baseline |
| `output` | output structure | because it is the result format that a person reads or the next stage inherits |

This table shows that a `dataset candidate` does not simply mean a table with many columns. It means a structure in which `sample`, `descriptive values`, `comparison result`, and `result format` all sit in the same row while dividing their roles.

`review` and `no_flag` are results produced by this example’s rule. Using them as ground-truth fault labels would require separate evidence, such as inspection records and fault criteria. This CSV contains no such evidence.

| Distinction | What can be established in this example |
| --- | --- |
| Rule result | Whether the chosen threshold selected the sample for review |
| Actual fault label | Whether a separate inspection confirmed a fault; this CSV alone cannot tell us |

A column’s role can also change with its purpose. For example, a later model could use `baseline_gap` as an input feature. Here, we distinguish the original features, the baseline-comparison result, and the review-rule result to understand the calculation process. Numeric columns do not all play the same role simply because they contain numbers.

After defining the sample, selecting descriptive values, and setting the comparison reference and output rule, trace one row back to its original records. If you can calculate the slope from R1’s two measurements, then use the baseline slope derived from B1, B2, and B3 and the review threshold to reproduce the gap and `review` result, you can read the structure of this example.

## Checklist

- Can you explain how original measurements or categories such as operating mode can be features?
- Can you find R1’s 4- and 5-second values in the CSV, calculate its slope of −0.32, and subtract the baseline slope to reproduce the difference?
- Can you explain why −0.32−(−0.05) is negative and what its unit means?
- Did you check which of −0.21, −0.20, and −0.19 are included by the review rule?
- Can you distinguish columns that change when only the threshold changes from those that stay fixed, without treating `review` as an actual fault label?

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `example`, `labeled example`, `feature`, `label`. Because it explains separately the roles that features and labels play inside an example, it supports this section's framing of sample, feature, baseline, and output structure as divided roles inside one table. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general concept of a reference period for comparison, it supports the role of reference values when reading changes from usual behavior in this example. This does not mean that every feature requires a baseline comparison to be meaningful. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it explains that derivation and activity context should remain visible together, it strengthens this section's higher-level frame that output structure is the result of earlier sample definition, feature calculation, and baseline comparison. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
