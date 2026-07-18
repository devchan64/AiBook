# P3-2.2 What Structures Go Inside a Dataset Candidate

> Section ID: `P3-2.2`
> Version: `v2026.07.17`

As the previous section showed, stored records may not yet be a dataset. The next question therefore follows immediately: if we rebuild a dataset candidate, what structure should go inside it? To answer that question, Part 3 looks at [sample](/AiBook/reference/concept-glossary/#glossary-sample), [feature](/AiBook/reference/concept-glossary/#glossary-feature), [baseline](/AiBook/reference/concept-glossary/#glossary-baseline), and [output structure](/AiBook/reference/concept-glossary/#glossary-output-structure) together. These terms are more accurate when read not as a list to memorize separately, but as one dataset-design structure. We have to decide what counts as one sample before features can be made; features are needed before we can decide what should be compared with a baseline; and only after that comparison is in place can we decide what output structure to make.

What matters especially in this section is reading `output structure`, before it hardens directly into a [target](/AiBook/reference/concept-glossary/#glossary-target), as a problem-design axis that separates review-oriented results from prediction-oriented target candidates. This is also why a dataset candidate should be read not as the name of one table, but as several connected structures. Only when what counts as the sample, which features are kept, what is compared against the baseline, and what output structure closes the process are all decided together does the meaning of the dataset candidate become clear.

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

Problem situation: check, in one table, the flow in which one action is treated as one sample, features are written down, the result is compared with the usual baseline, and a final operational output is produced.

Input: feature values by sample and the corresponding baseline values

Expected output: a process in which the same sample row expands in the order `feature -> baseline comparison -> operational output`

Concept to check: output structure is created as a result of the earlier sample, feature, and baseline comparison

```python
import pandas as pd

samples = pd.DataFrame(
    [
        {
            "sample_id": "A",
            "mean_flow": 0.74,
            "late_drop_rate": -0.32,
            "baseline_mean_flow": 0.92,
            "baseline_late_drop_rate": -0.05,
        },
        {
            "sample_id": "B",
            "mean_flow": 0.89,
            "late_drop_rate": -0.08,
            "baseline_mean_flow": 0.92,
            "baseline_late_drop_rate": -0.05,
        },
    ]
)

print("1) sample rows")
print(samples[["sample_id"]])
print()

feature_table = samples[["sample_id", "mean_flow", "late_drop_rate"]].copy()
print("2) add features")
print(feature_table)
print()

comparison_table = samples[
    [
        "sample_id",
        "mean_flow",
        "late_drop_rate",
        "baseline_mean_flow",
        "baseline_late_drop_rate",
    ]
].copy()
comparison_table["baseline_gap"] = (
    comparison_table["late_drop_rate"] - comparison_table["baseline_late_drop_rate"]
)
print("3) compare with baseline")
print(comparison_table)
print()

output_table = comparison_table.copy()
output_table["output"] = output_table["baseline_gap"].apply(
    lambda gap: "needs review" if gap <= -0.20 else "normal range"
)
print("4) final output structure")
print(output_table)
```

Expected output:

```text
1) sample rows
  sample_id
0         A
1         B

2) add features
  sample_id  mean_flow  late_drop_rate
0         A       0.74           -0.32
1         B       0.89           -0.08

3) compare with baseline
  sample_id  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap
0         A       0.74           -0.32                0.92                    -0.05         -0.27
1         B       0.89           -0.08                0.92                    -0.05         -0.03

4) final output structure
  sample_id  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap        output
0         A       0.74           -0.32                0.92                    -0.05         -0.27  needs review
1         B       0.89           -0.08                0.92                    -0.05         -0.03   normal range
```

This example shows the same row expanding across four passes. At first, there is only the sample identifier. Next, feature columns are attached. Then the difference from the baseline is calculated. Finally, an operational output column is added. So the output column does not exist by itself. It is built by inheriting the result of the earlier stages, `sample definition -> feature calculation -> baseline comparison -> operational judgment`.

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

- Google for Developers, `Machine Learning Glossary`: `example`, `labeled example`, `feature`, `label`. Because it explains separately the roles that features and labels play inside an example, it supports this section's framing of sample, feature, baseline, and output structure as divided roles inside one table. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general concept of a reference period for comparison, it strengthens this section's explanation that the current sample's values gain meaning only when compared with a baseline. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because it explains that derivation and activity context should remain visible together, it strengthens this section's higher-level frame that output structure is the result of earlier sample definition, feature calculation, and baseline comparison. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
