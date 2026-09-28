# P3-6.1 What Features Should We Keep to Represent a Structure for Comparison

> Section ID: `P3-6.1`
> Version: `v2026.09.19`

When people first learn about [features](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature), they often take them to mean `wouldn't more columns always be better?` But a feature is not just the act of inserting many values. A feature is a value that rewrites the structure of a sample so it can be used for comparison and prediction. So a good feature is less about being numerous and more about making `what it is trying to show` clear. If the raw log was turned into a [summary table](/AiBook/en/reference/concept-glossary-alpha/d/#data-modeling) in the previous chapter, we now have to decide what structure should remain inside that summary table.

To say that we design features means not that we use the numbers already sitting in the summary table as they are, but that we choose again how to express the structure we want to compare in numerical form. So only after we first decide what structure to preserve do candidate features such as averages, slopes, and variability gain meaning. At this point, one more judgment splits in two. Turning the same structure into different expressions such as an average, a difference, a slope, a token, or a ratio is [variable transformation](/AiBook/en/reference/concept-glossary-alpha/v/#glossary-variable-transformation), while choosing which of those transformed expressions should actually remain is [feature selection](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature-selection).


Raw measurements can also serve directly as features. Here we focus on selecting and expressing comparison information from summaries.

## What These Features Measure, and in Which Units

These are segment means for fictional events A and B, in L/min. **The calculation uses three means—early, middle, and late—not all raw measurements.** If segment observation counts or durations differ, the unweighted mean of these three means can differ from the overall observation mean or time average.

| Event | Early mean | Middle mean | Late mean |
| --- | ---: | ---: | ---: |
| A | 1.8 | 2.2 | 2.6 |
| B | 2.1 | 2.2 | 2.3 |

Assign indices 0, 1, and 2 to the early, middle, and late segments. The early-to-late index gap is `2−0=2`. Dividing A's difference, `2.6−1.8=0.8 L/min`, by 2 gives **0.4 L/min per index interval**, not a per-second change. If the representative times were 20 seconds apart, the time slope would be `0.8/20=0.04 L/min/s`. Without timestamps, we cannot assume 20 seconds.

| Event | Mean of three segment means: L/min | Late−early: L/min | Slope per index interval | Standard deviation of three segment means: L/min |
| --- | ---: | ---: | ---: | ---: |
| A | 2.2 | 0.8 | 0.4 | 0.4 |
| B | 2.2 | 0.2 | 0.1 | 0.1 |

Standard deviation summarizes how far values lie from their mean. Here we use the sample-standard-deviation convention: divide the sum of squared deviations by `3−1=2`, then take its square root. A's deviations from 2.2 are −0.4, 0, and 0.4, so `sqrt((0.16+0+0.16)/2)=0.4`. The same calculation gives 0.1 for B. Using this convention does not establish statistical independence of the three means.

## Spread Between Segment Means Differs from Variation Within a Segment

Suppose every segment contains measurements `[2, 2]` for X and `[0, 4]` for Y. Both events have segment means `[2, 2, 2]`, and **the standard deviation of those three means is zero**. Yet the within-segment maximum minus minimum is 0 for X and 4 for Y. Segment means alone cannot recover this difference.

A's larger standard deviation in the table means its segment means are further apart. It does not diagnose greater sensor noise or operational instability. Reversing early and late also leaves standard deviation unchanged, so read a signed difference to distinguish rising from falling.

Choose a mean for “Are the levels of the three segments similar?” and late−early for “How much changed from early to late?” The answers are 2.2 for both A and B in the first case, and 0.8 for A versus 0.2 for B in the second. With a fixed index gap of 2, slope is half the difference, so keeping both columns adds no independent new information. A question about within-segment variation requires raw values or an additional within-segment spread measure.

## A Small Prediction Experiment with Different Features

Give the same decision-tree algorithm different feature sets derived from events A–H. Here `overall_mean` is the unweighted mean of three segment means, and `segment_variability` is their sample standard deviation calculated above. Run in Python with pandas and scikit-learn installed.

This is an eight-event fictional experiment designed to illustrate input information loss. `review_needed` contains assigned example values, not validated inspection criteria. All six training events A–F have a mean of segment means of 2.2, so that mean alone cannot readily distinguish their different labels. The test contains only G and H: accuracies 0.5 and 1.0 mean one of two and two of two correct. This is not evidence that adding features generally improves performance.

Run the experiment with just `overall_mean` and `late_minus_early` as inputs. This setting also predicts both test events correctly, but performance on more data requires separate evaluation. Distinguishing within-segment variation still requires raw information that none of these features can restore.

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

```text
mean_only accuracy: 0.5
mean_only predictions: [('G', 0, 1), ('H', 0, 0)]
structure_features accuracy: 1.0
structure_features predictions: [('G', 1, 1), ('H', 0, 0)]
```

## Retaining Features for the Comparison Question {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-06/p3-6-1-mermaid-01-en.mmd"
```

## Checklist

- Can you distinguish the slope denominator 2 from elapsed time?
- Can you name the three values used for standard deviation and their units?
- Can you explain why means [2, 2, 2] cannot recover within-segment variation?
- Can you avoid generalizing accuracy on two test events to overall performance?

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `feature`. Because it explains a feature as an input variable used to make predictions, it supports the point that we should first decide what structure we want to show and then turn that structure into input variables. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
- Google for Developers, `Machine Learning Glossary`: `feature engineering`. Because it explains feature engineering as the process of deciding transformations that are helpful for model training, it reinforces the point that feature design is not leaving raw values untouched but converting structure into comparable numerical expressions. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Location`. Because it describes the mean, median, and mode as representative measures of location and shows that skewed or heavy-tailed distributions can make the mean and median carry different information, it reinforces this section's point that even an overall-level feature should be chosen according to the structure we want to inspect. [https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Scale`. Because it explains several numerical measures of variability or spread and says the choice of a scale estimator depends on which part of spread we want to emphasize, it supports this section's point that stability features should remain as a structure separate from the average. [https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
