# P3-6.1 What Features Should We Keep to Represent a Structure for Comparison

> Section ID: `P3-6.1`
> Version: `v2026.07.24`

When people first learn about features, they often take them to mean `wouldn't more columns always be better?` But a feature is not just the act of inserting many values. A feature is a value that rewrites the structure of a sample so it can be used for comparison and prediction. So a good feature is less about being numerous and more about making `what it is trying to show` clear. If the raw log was turned into a summary table in the previous chapter, we now have to decide what structure should remain inside that summary table.

To say that we design features means not that we use the numbers already sitting in the summary table as they are, but that we choose again how to express the structure we want to compare in numerical form. So only after we first decide what structure to preserve do candidate features such as averages, slopes, and variability gain meaning. At this point, one more judgment splits in two. Turning the same structure into different expressions such as an average, a difference, a slope, a token, or a ratio is variable transformation, while choosing which of those transformed expressions should actually remain is feature selection.

| Viewpoint | The question being asked now | Representative examples |
| --- | --- | --- |
| Variable transformation | Into what expression should the same structure be converted? | Average, segment difference, slope, ratio, token |
| Feature selection | Which of the converted expressions should actually remain? | Features for overall level, features for late-stage collapse detection, variability features |

Suppose we treat one automatically executed action as one sample. In that case, we cannot place the entire time-point sensor sequence into one row as-is. Instead, we need to create summary values that reveal important aspects of the action. For example, the following values are often good starting points.

- mean
- slope
- variability
- maximum or minimum value
- rate of change in a specific segment

Why do values like these appear so often? First, they are easy to convert into comparable numbers without throwing away the raw curve too roughly. Second, even when a person reads them, they are easier to explain in sentences such as `this action has a similar average but a steeper decline in the late phase`. Third, even when the average is the same, a different variability or slope can reveal a real structural difference.

So a good feature is closer to `an appropriate question` than to `many values`. An average shows the overall level, a slope shows direction and speed of change, and variability shows the size of the fluctuation. The reason different features are needed is that each value reveals a different part of the structure. The judgment about what transformations to create first from the same summary table, and which of them to keep, is exactly the core of variable transformation and feature selection.

| Action | Average | Slope | Variability | Structure we can read |
| --- | --- | --- | --- | --- |
| A | similar | gentle | low | relatively stable |
| B | similar | steep | high | unstable or changing a lot |

Problem situation: check what features should remain when the overall level of two actions is similar but the size of their rise and the degree of their fluctuation differ.

Input: an action-summary table where only segment averages remain, and the structure to inspect first, `feature_focus`

Expected output: a feature table that calculates level, segment difference, slope, and variability from the same summary table. If `feature_focus` changes, the features selected first also change.

Concept to check: a feature is not a simple listing of existing columns, but an added expression that computes the structure we want to compare. Feature selection changes with the question focus.

```python
# This example creates and selects features from segment summaries according to the comparison goal.
from statistics import mean, stdev

feature_focus = "change"

segment_summary = [
    {"event_id": "A", "early_flow_mean": 1.8, "mid_flow_mean": 2.2, "late_flow_mean": 2.6},
    {"event_id": "B", "early_flow_mean": 2.1, "mid_flow_mean": 2.2, "late_flow_mean": 2.3},
]

feature_table = []
for row in segment_summary:
    segment_values = [row["early_flow_mean"], row["mid_flow_mean"], row["late_flow_mean"]]
    late_minus_early = row["late_flow_mean"] - row["early_flow_mean"]
    feature_table.append(
        {
            **row,
            "overall_mean": mean(segment_values),
            "late_minus_early": late_minus_early,
            "early_to_late_slope": late_minus_early / 2,
            "segment_variability": stdev(segment_values),
        }
    )

focus_map = {
    "level": ["overall_mean"],
    "change": ["late_minus_early", "early_to_late_slope"],
    "stability": ["segment_variability"],
}
focus_columns = focus_map[feature_focus]

print("1) segment means before feature design")
print("  event_id  early_flow_mean  mid_flow_mean  late_flow_mean")
for index, row in enumerate(segment_summary):
    print(
        f"{index}        {row['event_id']}              {row['early_flow_mean']:.1f}"
        f"            {row['mid_flow_mean']:.1f}             {row['late_flow_mean']:.1f}"
    )
print()
print("2) designed features for comparison")
print(
    "  event_id  overall_mean  late_minus_early  early_to_late_slope"
    "  segment_variability"
)
for index, row in enumerate(feature_table):
    print(
        f"{index}        {row['event_id']}           {row['overall_mean']:.1f}"
        f"               {row['late_minus_early']:.1f}"
        f"                  {row['early_to_late_slope']:.1f}"
        f"                  {row['segment_variability']:.1f}"
    )
print()
print(f"3) selected features when feature_focus = {feature_focus}")
if focus_columns == ["overall_mean"]:
    print("  event_id  overall_mean")
    for index, row in enumerate(feature_table):
        print(f"{index}        {row['event_id']}           {row['overall_mean']:.1f}")
elif focus_columns == ["late_minus_early", "early_to_late_slope"]:
    print("  event_id  late_minus_early  early_to_late_slope")
    for index, row in enumerate(feature_table):
        print(
            f"{index}        {row['event_id']}               {row['late_minus_early']:.1f}"
            f"                  {row['early_to_late_slope']:.1f}"
        )
else:
    print("  event_id  segment_variability")
    for index, row in enumerate(feature_table):
        print(f"{index}        {row['event_id']}                  {row['segment_variability']:.1f}")
print()
print("4) feature_focus comparison")
for focus_name, columns in focus_map.items():
    print(f"- {focus_name}: {columns}")
```

Expected output:

```text
1) segment means before feature design
  event_id  early_flow_mean  mid_flow_mean  late_flow_mean
0        A              1.8            2.2             2.6
1        B              2.1            2.2             2.3

2) designed features for comparison
  event_id  overall_mean  late_minus_early  early_to_late_slope  segment_variability
0        A           2.2               0.8                  0.4                  0.4
1        B           2.2               0.2                  0.1                  0.1

3) selected features when feature_focus = change
  event_id  late_minus_early  early_to_late_slope
0        A               0.8                  0.4
1        B               0.2                  0.1

4) feature_focus comparison
- level: ['overall_mean']
- change: ['late_minus_early', 'early_to_late_slope']
- stability: ['segment_variability']
```

Stage 1 of the output is still only a summary table with segment averages. Only in stage 2 do `overall_mean`, `late_minus_early`, `early_to_late_slope`, and `segment_variability` get added. `overall_mean` shows the overall level, `late_minus_early` shows the late-versus-early difference, `early_to_late_slope` shows a simple slope expression that divides that difference by segment distance, and `segment_variability` shows the degree of fluctuation across segments. The value to manipulate here is `feature_focus`. If it is set to `"change"`, change features are kept first. If it is changed to `"level"`, the overall-level feature is kept first. If it is changed to `"stability"`, the variability feature is kept first. Stage 4 shows that even with the same feature table, the actual group of columns kept changes when the question focus changes. In other words, a feature is not something that merely re-shows what was already written down. It is the result of computing and attaching the structure we want to compare from the same summary table and choosing it for the current question.

The same difference appears in actual model input. The next example compares a model that keeps only the overall mean with a model that also keeps change and variability features. Both models use the same decision-tree classifier, but the test predictions change depending on which features are given as input.

Problem situation: We want to compare predictions when actions with similar averages but different segment changes are read through only mean features versus through structure features.

Input: A small action table with `early`, `mid`, `late` segment means and the label `review_needed`.

Expected output: Accuracy and test predictions for the `mean_only` feature set and the `structure_features` feature set.

Concept to check: Feature selection decides which structure the model can see, and if we keep only the mean, we can miss change or variability structure.

```python
# This example compares predictions from a mean-only model and a model with change/variability features.
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

events = pd.DataFrame(
    [
        {"event_id": "A", "early": 1.8, "mid": 2.2, "late": 2.6, "review_needed": 1},
        {"event_id": "B", "early": 2.1, "mid": 2.2, "late": 2.3, "review_needed": 0},
        {"event_id": "C", "early": 2.5, "mid": 2.2, "late": 1.9, "review_needed": 1},
        {"event_id": "D", "early": 2.0, "mid": 2.2, "late": 2.4, "review_needed": 0},
        {"event_id": "E", "early": 1.7, "mid": 2.2, "late": 2.7, "review_needed": 1},
        {"event_id": "F", "early": 2.2, "mid": 2.2, "late": 2.2, "review_needed": 0},
        {"event_id": "G", "early": 2.6, "mid": 2.2, "late": 1.8, "review_needed": 1},
        {"event_id": "H", "early": 2.0, "mid": 2.1, "late": 2.3, "review_needed": 0},
    ]
)

segment_values = events[["early", "mid", "late"]]
events["overall_mean"] = segment_values.mean(axis=1)
events["late_minus_early"] = events["late"] - events["early"]
events["segment_variability"] = segment_values.std(axis=1)

train = events[events["event_id"].isin(["A", "B", "C", "D", "E", "F"])]
test = events[events["event_id"].isin(["G", "H"])]
feature_sets = {
    "mean_only": ["overall_mean"],
    "structure_features": ["overall_mean", "late_minus_early", "segment_variability"],
}

for name, columns in feature_sets.items():
    model = DecisionTreeClassifier(random_state=0, max_depth=2)
    model.fit(train[columns], train["review_needed"])
    predicted = model.predict(test[columns])
    comparison = [
        (event_id, int(prediction), int(actual))
        for event_id, prediction, actual in zip(test["event_id"], predicted, test["review_needed"])
    ]
    print(name, "accuracy:", accuracy_score(test["review_needed"], predicted))
    print(name, "predictions:", comparison)
```

Expected output:

```text
mean_only accuracy: 0.5
mean_only predictions: [('G', 0, 1), ('H', 0, 0)]
structure_features accuracy: 1.0
structure_features predictions: [('G', 1, 1), ('H', 0, 0)]
```

If we look only at the overall mean, `G` is hard to distinguish from a stable action. But if we also look at `late_minus_early` and `segment_variability`, the downward late-section structure and segment fluctuation become visible. So even with the same model, `G` is missed when only the mean is visible, and correctly predicted when structure features are visible. This output shows that a feature is not just another column. It is a choice about which structure the model can see.

If these features are read in smaller layers, the role of each value becomes clearer.

| Feature type | Representative examples | What it mainly shows |
| --- | --- | --- |
| Level features | Average, maximum value | Overall size |
| Change features | Segment difference, slope | Direction and speed |
| Stability features | Standard deviation, variability | Degree of fluctuation |

This table brings back the two-way split mentioned earlier. The stage that turns the structure into an average, difference, slope, or variability is variable transformation. The stage that chooses which of those values should remain for the current question is feature selection. Numerical features are the first step of summarizing structure, while tokenized expressions are the next step of turning that structure into an intermediate representation that is easier for people to read.

When designing features, the following questions should keep being checked.

- What aspect of the action does this value show?
- Does it complement structure that the average alone misses?
- Can a person also explain it when reading it?
- Does it fit the sample unit well?

If these questions are shortened into a more practical form, the link between a structure we want to see first and the feature that should come first can be chosen like this.

| The structure we want to inspect first | The feature that should come to mind first |
| --- | --- |
| Is the overall level similar? | Average, maximum value |
| How different did the early and late phases become? | Segment difference, slope |
| How much did it fluctuate? | Standard deviation, variability |
| Did it change sharply at a certain point? | Time of maximum value, rate of change |

The point of this table is not `let's memorize more feature names`. The point is that after first deciding what structure we want to see, we should attach the feature that reveals that structure most directly.

One more place where people get stuck is that even the sentence `look at the structure and choose a feature` can still sound abstract. So if we write once more, more briefly, the process of moving from a real question to feature design, it becomes the following.

| The question that first arises in practice | The feature to build first | Why that feature is needed first |
| --- | --- | --- |
| Was the overall level of this action lower than usual? | Average, median | Because it lets us first check the overall scale difference |
| Was the early part acceptable but the late part collapsed? | `late_minus_early`, segment-wise slope | Because it reveals directly in which segment the structure changed |
| Did the process fluctuate more even though the result looked similar? | Standard deviation, segment-wise variability | Because it lets us inspect instability hidden by the average |
| Did the peak arrive too late or fade too early? | Time of maximum value, time the decline begins | Because timing differences can greatly change operational meaning |

So a feature is not chosen from `a list of column candidates`. It is the act of translating `what are we asking right now?` into numerical form. If the question is about the `overall level`, level features should come first. If the question is about `shape change`, change features such as segment differences and slopes should come first. Only when this connection is fixed can we later explain again in baseline comparison `why did we keep this feature in particular?`

This section can be read not as an introduction to a list of features, but as the problem of what question should guide `the numeric representation of structure`.

## A Small Diagram

The flow of this section is to decide `the structure to compare` first, convert that structure into expressions such as average, difference, slope, and variability, and then choose which features should actually remain. A feature is not the act of growing columns, but the process of rewriting structure into numerical form.

--8<-- "assets/part-03/chapter-06/p3-6-1-mermaid-01-en.mmd"


So a feature is not `adding more columns`, but translating the structure we want to compare into numerical forms such as level, change, and stability.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `feature`. Because it explains a feature as an input variable used to make predictions, it supports the point that we should first decide what structure we want to show and then turn that structure into input variables. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `feature engineering`. Because it explains feature engineering as the process of deciding transformations that are helpful for model training, it reinforces the point that feature design is not leaving raw values untouched but converting structure into comparable numerical expressions. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it explains a reference period as the basis for comparison with other periods, it offers a general basis for choosing level/change/stability features in a way that leaves behind structures that are easy to read in baseline comparison. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Location`. Because it describes the mean, median, and mode as representative measures of location and shows that skewed or heavy-tailed distributions can make the mean and median carry different information, it reinforces this section's point that even an overall-level feature should be chosen according to the structure we want to inspect. [https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Scale`. Because it explains several numerical measures of variability or spread and says the choice of a scale estimator depends on which part of spread we want to emphasize, it supports this section's point that stability features should remain as a structure separate from the average. [https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
