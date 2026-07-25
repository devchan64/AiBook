# P3-2.2 What Structures Go Inside a Dataset Candidate

> Section ID: `P3-2.2`
> Version: `v2026.07.20`

As the previous section showed, stored records may not yet be a dataset. The next question therefore follows immediately: if we rebuild a dataset candidate, what structure should go inside it? To answer that question, Part 3 looks at [sample](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-sample), [feature](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-feature), [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline), and [output structure](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure) together. These terms are more accurate when read not as a list to memorize separately, but as one dataset-design structure. We have to decide what counts as one sample before features can be made; features are needed before we can decide what should be compared with a baseline; and only after that comparison is in place can we decide what output structure to make.

What matters especially in this section is reading `output structure`, before it hardens directly into a [target](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target), as a problem-design axis that separates review-oriented results from prediction-oriented target candidates. This is also why a dataset candidate should be read not as the name of one table, but as several connected structures. Only when what counts as the sample, which features are kept, what is compared against the baseline, and what output structure closes the process are all decided together does the meaning of the dataset candidate become clear.

Take one automatically executed action as an example. The sample might be `the whole current action treated as one case`. Features might be values calculated and kept from that action, such as `total time`, `mid-stage mean`, `late-stage drop rate`, or `tracking error`. The baseline might be a representative value from the usual range or a comparison group outside the recent cases. The output structure is the result format that a person or a model will finally read, for example something like `needs review`, `caution`, `normal range`, or `candidate prediction label`.

The relationship can first be organized in the following table.

| Component | What it means here | The question asked at this stage |
| --- | --- | --- |
| Sample | one case that becomes the basic unit for comparison or learning | What will count as one row? |
| Feature | a value calculated and kept in order to describe the sample | Which values should remain to make comparison easier? |
| Baseline | the usual structure or reference group against which the recent state is compared | Compared with what does change become visible? |
| Output structure | the result format that a person reads or a model receives next | What final judgment are we trying to produce? |

Seeing these four together reveals why data modeling is more than simple organization. For example, if we have not yet decided whether the sample is `one time-point measurement` or `one full action`, we cannot set features stably either, because features suited to a time-point table differ from features suited to an action-level table. Likewise, if the baseline is not fixed, changes in the recent segment are hard to read. And if the output structure is not fixed as either `creating review candidates` or `emitting prediction labels`, then even the needed comparison remains vague.

So these four elements are not a vocabulary list to memorize separately. They are a design sequence that runs from the front to the back when building a dataset candidate. If the sample drifts, the features drift too. If the features drift, baseline comparison drifts as well. If the comparison drifts, the output structure also drifts. That is why this section first fixes how they connect through a question order.

In practice, the questions connect in the following order.

1. Is what we are comparing one time point, one full action, or a recent segment?
2. Which numbers should remain to describe that object?
3. Compared with what do those numbers gain meaning?
4. Should the final result be emitted as a sentence that a person reads, or as a candidate label that a model will receive?

These four questions correspond respectively to sample, feature, baseline, and output structure. So even when the terms themselves feel blurry, following the question order makes it easier to recover which stage of dataset design we are currently in.

The table below shows more concretely how the four elements connect inside one row. Even for the same one action, we first establish the sample as one case, then write features on top of it, compare those features with the usual baseline, and finally close with an output that a person will read.

| sample_id | mean_flow | late_drop_rate | baseline_mean_flow | baseline_late_drop_rate | baseline_gap | output |
| --- | --- | --- | --- | --- | --- | --- |
| A | 0.74 | -0.32 | 0.92 | -0.05 | -0.27 | `needs review` |
| B | 0.89 | -0.08 | 0.92 | -0.05 | -0.03 | `normal range` |

The order for reading this table proceeds naturally from left to right. `sample_id` fixes what was counted as one sample. `mean_flow` and `late_drop_rate` are features that describe that sample. `baseline_mean_flow` and `baseline_late_drop_rate` are the usual baseline. `baseline_gap` records the comparison result, showing how much more the late-stage drop rate of the current sample fell relative to the baseline. And if that comparison result is large enough, the `output` column creates an operational judgment such as `needs review`.

In other words, an output such as `needs review` is not a phrase that gets attached suddenly at the far end of the table. The earlier columns must already have organized `what is being compared` and `what differs from the usual state`, or the final output column cannot be explained either. For that reason, sample, feature, baseline, and output structure are not independent lists even when they live in the same table. They are one design flow that runs from front to back.

## A Small Diagram

The four structures inside a dataset candidate can be read in one pass when they are compressed into the sequence `sample -> feature -> baseline comparison -> output structure`.

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-2-mermaid-01-en.mmd"
```

Problem situation: check the flow in which one action is treated as one sample, features are written down, the result is compared with the usual baseline, and a final operational output is produced.

Input: the time-step flow log [p3_2_2_event_flow_log.csv](/AiBook/assets/part-03/chapter-02/p3_2_2_event_flow_log.csv), which contains both `baseline` and `recent` periods, and candidate review thresholds `review_gap_thresholds`

One input-file row is the measured flow (`flow`) at a specific second (`second`) of one sample. `sample_id` points to one action, and `period` separates whether that sample belongs to the `baseline` period used to build the usual reference or the `recent` period to be compared.

Expected output: the raw log becomes `sample rows -> feature table -> baseline creation -> recent-sample comparison table -> operational output`, and the number of review candidates changes when different `review_gap_thresholds` are applied

Concept to check: output structure and baseline are not result columns written in advance. They are generated after raw logs are grouped by sample unit, features are calculated, and period roles are separated. Comparing several output criteria reveals how sensitive the operational judgment is to the threshold.

```python
# This example checks the roles of sample, feature, label, and baseline columns in a dataset candidate.
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

event_log_path = "docs/assets/part-03/chapter-02/p3_2_2_event_flow_log.csv"
selected_review_gap_threshold = -0.20
review_gap_thresholds = [-0.36, selected_review_gap_threshold, 0.0]

event_log = pd.read_csv(event_log_path)

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
        lambda gap: "needs review" if gap <= threshold else "normal range"
    )
    if threshold == selected_review_gap_threshold:
        selected_output_table = output_table.copy()
    threshold_results.append(
        {
            "review_gap_threshold": threshold,
            "review_count": int((output_table["output"] == "needs review").sum()),
            "review_samples": ",".join(
                output_table.loc[output_table["output"] == "needs review", "sample_id"]
            )
            or "none",
        }
    )

print("6) final output structure when review_gap_threshold = -0.20")
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
  sample_id  period  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap        output
3        R1  recent       0.83           -0.32                0.94                    -0.05         -0.27  needs review
4        R2  recent       0.90           -0.08                0.94                    -0.05         -0.03  normal range
5        R3  recent       0.94           -0.40                0.94                    -0.05         -0.35  needs review

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

One more important distinction needs to be fixed here. Output structure does not necessarily mean `training data where the correct label has already been fixed`. Outputs such as `needs review` or `normal range` may look similar to supervised-learning labels such as `yes/no`, but in practice they can differ.

| What the output structure means | How to read it at this stage |
| --- | --- |
| `needs review`, `caution`, `normal range` | operational results that a person checks first |
| fixed labels such as `normal/abnormal` | target-label candidates that may later be passed into a prediction problem |

If this distinction is established first, then later references to `output structure` will not be misunderstood as meaning that `the label is already complete`.

This flow can be remembered more briefly in the following order.

1. Decide what will count as one sample.
2. Keep features that describe that sample.
3. Build a baseline that compares the recent state with the usual state.
4. Decide the output structure that a person reads or a model inherits.

These four stages unfold later into different Chapters, but in practice they are one continuous judgment. So whichever Chapter we are reading, it helps not to lose direction if we also ask `which stage does this explanation belong to: sample, feature, baseline, or output structure?` Once we hold onto the relation that `the sample has to be fixed before features exist, features have to be fixed before comparison structure exists, and comparison structure has to exist before output structure is organized`, it becomes much clearer that a dataset candidate is not the name of one file, but a table designed so that these four structures interlock. More broadly, this section establishes the minimum contract that organizes how `the example unit`, `descriptive variables`, `comparison reference`, and `result format` lock together inside one data problem. So a dataset candidate should be read not as `a table with many columns`, but as a structure in which descriptive values, comparison references, and result formats divide their roles inside one example.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `example`, `labeled example`, `feature`, `label`. Because it explains separately the roles that features and labels play inside an example, it supports this section's framing of sample, feature, baseline, and output structure as divided roles inside one table. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general concept of a reference period for comparison, it strengthens this section's explanation that the current sample's values gain meaning only when compared with a baseline. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it explains that derivation and activity context should remain visible together, it strengthens this section's higher-level frame that output structure is the result of earlier sample definition, feature calculation, and baseline comparison. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
