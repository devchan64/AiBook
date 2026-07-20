# P4-12.2 Distance And Scale

> Section ID: `P4-12.2`
> Version: `v2026.07.17`

P4-12.1 explained k-NN as `a model that judges by looking at nearby cases`. But the most important word there is really `near`.

What exactly does near mean?

If this question is skipped, the reader has not really understood the model, only the result. In k-NN, `what rule is used to compute nearness` is part of the model itself.

## Scope Of This Section

This Section answers the following questions.

- What role does distance play in k-NN?
- If the distance function changes, can the neighbor order and prediction change?
- Why can scale distort distance calculation?
- What does standardization change in the interpretation of k-NN?

This Section first closes `why distance and scale change neighbors and predictions in k-NN`. The purpose and types of preprocessing stay centered in `P4-7.2 Preprocessing`; here the focus stays on the scenes where distance and scale change the judgment.

## Goals Of This Section

- You can explain that a distance function is not `an outside setting`, but `part of the judgment rule`.
- You can explain that when the distance function changes, the neighbor order and prediction can change too.
- You can explain that when feature scales differ, one large axis can dominate the distance.
- You can explain that standardization is not `making numbers look neat`, but `realigning the comparison criterion`.

## Main Learning Content

### Distance Is Part Of The Judgment Rule

k-NN computes distances between a new input and the existing data, then finds the nearest neighbors. So the distance function is not just a calculation tool. It is the rule that decides `who gets selected as a neighbor`.

- Euclidean distance: a way of reading closeness like straight-line distance
- Manhattan distance: a way of summing movement along axes

Even for the same query, if the distance rule changes, the neighbor order can change, and the prediction can change as well.

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-2-mermaid-01-en.mmd"
```

The key sentence is this.

`The distance function is part of the perspective used to interpret the input.`

### If The Distance Function Changes, The Neighbor Order Can Change

Suppose the query and two candidate points are the following.

| Target | Coordinate |
| --- | --- |
| query | (0, 0) |
| point A | (3, 0) |
| point B | (2, 2) |

Under Euclidean distance:

- distance between query and A = 3
- distance between query and B = about 2.83

So B is closer.

But under Manhattan distance:

- distance between query and A = 3
- distance between query and B = 4

Now A is closer.

This example shows the flow `distance rule change -> neighbor order change`. In actual k-NN, once the neighbor order changes, the labels entering the majority vote can change too, and then the final prediction can change.

### Why Can Scale Distort Distance Calculation?

Scale is as important as the distance function itself. Just because two features are both numbers does not mean the distance calculation reads them with equal weight.

Suppose there are two features like the following.

- annual income: numbers in the millions or tens of millions
- late payments: counts such as 0, 1, 2, or 7

Both can be important. But if the raw ranges are left as they are, the annual-income axis looks much larger numerically. Then the distance starts asking more strongly `whose income is numerically similar?` than `whose late-payment pattern is similar?`

Two things should be separated here.

- unit difference: the number systems are already different, such as currency, seconds, or count
- variance difference: even among numeric features, one axis can spread much more widely than another

Both can ultimately lead to a similar problem: `a large axis dominates the distance`.

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-2-mermaid-02-en.mmd"
```

### What Does Standardization Change?

Standardization is not decoration that makes numbers prettier. More accurately, it is `the act of rebalancing how much influence each feature has inside the distance calculation`.

At an introductory level, the following order is enough.

- subtract the mean from each feature
- divide each feature by its standard deviation
- move large-unit and small-unit axes into a more comparable range

So standardization can be read as `bringing back into the comparison features that were previously being drowned out`.

That does not mean it `always improves performance`. A feature that gets brought back may contain useful information, but it may also contain noise.

## Cases And Examples

### Case 1. Loan-Risk Classification Where Large Income Numbers Hide Late-Payment History

A loan-screening support model wants to separate a new applicant into `safe` and `risky`. A person would first look at signals such as `annual income`, `late-payment count`, `existing loan size`, and `repayment history`.

The problem is that these columns use very different units. Annual income can be a large number, while late-payment count may range only from 0 to a few cases. If k-NN distance is computed in that state, late-payment count can be important in reality and still be buried under the income axis.

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-2-mermaid-03-en.mmd"
```

This case shows the following key points.

- distance and scale are not small choices outside preprocessing, but part of the judgment rule
- even when the data stay the same, changing the representation can change `who counts as a nearby person`
- so before and after scale adjustment, the reader should first inspect `which neighbors entered and left`, rather than only a final score

## Practice And Example

### Python Example: Compare Raw Distances With Distances After Scale Adjustment

- problem situation: inspect whether a new customer is closer to `safe` or `risky`
- input: annual income and late-payment count
- label: `safe` / `risky`
- concept to check:
  - under raw numbers, the large-unit income axis can dominate the distance
  - after standardization, information from the smaller axis can come back into the comparison
  - so the order of the nearest neighbors can change even for the same query

The reading order can be kept as follows.

1. inspect which group looks closer under raw distances
2. inspect which neighbors became newly closer after standardization
3. if a difference appears, first interpret whether `the rule used to compute nearness changed`, not `the model itself changed`

```python
# This example checks how feature scale differences change distance calculations and k-NN neighbor selection.
from math import sqrt
from collections import Counter

train = [
    ((1800000, 1), "safe"),
    ((2200000, 0), "safe"),
    ((9000000, 7), "risky"),
    ((9500000, 8), "risky"),
]

query = (6000000, 0)

def euclidean(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def zscore_from_train(train_points):
    cols = list(zip(*train_points))
    means = [sum(col) / len(col) for col in cols]
    stds = []
    for i, col in enumerate(cols):
        m = means[i]
        var = sum((x - m) ** 2 for x in col) / len(col)
        stds.append(var ** 0.5)
    return means, stds

def scale(point, means, stds):
    return tuple((x - m) / s for x, m, s in zip(point, means, stds))

def ranked_neighbors(points_with_labels, query_point):
    ranked = []
    for point, label in points_with_labels:
        ranked.append((euclidean(point, query_point), point, label))
    return sorted(ranked, key=lambda x: x[0])

def majority_vote(labels):
    return Counter(labels).most_common(1)[0][0]

train_points = [point for point, _ in train]
means, stds = zscore_from_train(train_points)

print("raw distances")
raw_ranked = ranked_neighbors(train, query)
for distance, point, label in raw_ranked:
    print(point, label, round(distance, 3))

print()

scaled_query = scale(query, means, stds)
print("scaled distances")
scaled_ranked = []
for point, label in train:
    scaled_point = scale(point, means, stds)
    scaled_ranked.append((euclidean(scaled_point, scaled_query), point, label, scaled_point))
scaled_ranked.sort(key=lambda x: x[0])

for distance, point, label, scaled_point in scaled_ranked:
    print(
        point,
        label,
        "scaled =", tuple(round(v, 3) for v in scaled_point),
        "distance =", round(distance, 3),
    )

print()
print("top-2 neighbors before scaling =", [(point, label) for _, point, label in raw_ranked[:2]])
print("top-2 neighbors after scaling =", [(point, label) for _, point, label, _ in scaled_ranked[:2]])
raw_top3_labels = [label for _, _, label in raw_ranked[:3]]
scaled_top3_labels = [label for _, _, label, _ in scaled_ranked[:3]]
print("k=3 labels before scaling =", raw_top3_labels)
print("k=3 labels after scaling =", scaled_top3_labels)
print("k=3 prediction before scaling =", majority_vote(raw_top3_labels))
print("k=3 prediction after scaling =", majority_vote(scaled_top3_labels))
```

An example output is as follows.

```text
raw distances
(9000000, 7) risky 3000000.0
(9500000, 8) risky 3500000.0
(2200000, 0) safe 3800000.0
(1800000, 1) safe 4200000.0

scaled distances
(2200000, 0) safe scaled = (-0.943, -1.131) distance = 1.046
(1800000, 1) safe scaled = (-1.053, -0.849) distance = 1.305
(9000000, 7) risky scaled = (0.929, 0.849) distance = 1.897
(9500000, 8) risky scaled = (1.067, 1.131) distance = 2.179

top-2 neighbors before scaling = [((9000000, 7), 'risky'), ((9500000, 8), 'risky')]
top-2 neighbors after scaling = [((2200000, 0), 'safe'), ((1800000, 1), 'safe')]
k=3 labels before scaling = ['risky', 'risky', 'safe']
k=3 labels after scaling = ['safe', 'safe', 'risky']
k=3 prediction before scaling = risky
k=3 prediction after scaling = safe
```

The first sentence to hold in this output is the following.

`The result of k-NN depends not only on the data, but also on how the data are represented.`

Under raw distance, the `risky` group appears first. After standardization, the `safe` group appears first. If the reader checks `k=3`, the raw-distance reading becomes `risky, risky, safe`, so the final prediction is `risky`, while the standardized reading becomes `safe, safe, risky`, so the final prediction changes to `safe`. So the first thing this example should make visible is not only that a score changed, but that `the neighbor order itself changed, and that change reached all the way to the k-NN judgment`.

### Change One More Value: If Only The Late-Payment Count Increases Under The Same Scale, How Does The Neighbor Order Mix Again?

Now keep the same standardization scheme, but change only the query's late-payment count from `0` to `2`.

```python
# This example checks how feature scale differences change distance calculations and k-NN neighbor selection.
from math import sqrt

train = [
    ((1800000, 1), "safe"),
    ((2200000, 0), "safe"),
    ((9000000, 7), "risky"),
    ((9500000, 8), "risky"),
]

def euclidean(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def zscore_from_train(train_points):
    cols = list(zip(*train_points))
    means = [sum(col) / len(col) for col in cols]
    stds = []
    for i, col in enumerate(cols):
        m = means[i]
        var = sum((x - m) ** 2 for x in col) / len(col)
        stds.append(var ** 0.5)
    return means, stds

def scale(point, means, stds):
    return tuple((x - m) / s for x, m, s in zip(point, means, stds))

def ranked_neighbors(points_with_labels, query_point):
    ranked = []
    for point, label in points_with_labels:
        ranked.append((euclidean(point, query_point), point, label))
    return sorted(ranked, key=lambda x: x[0])

train_points = [point for point, _ in train]
means, stds = zscore_from_train(train_points)

scaled_query_0 = scale((6000000, 0), means, stds)
scaled_query_2 = scale((6000000, 2), means, stds)

ranked_0 = ranked_neighbors([(scale(point, means, stds), label) for point, label in train], scaled_query_0)
ranked_2 = ranked_neighbors([(scale(point, means, stds), label) for point, label in train], scaled_query_2)

print("top-2 after scaling, late_payment=0 :", [(label, round(distance, 3)) for distance, _, label in ranked_0[:2]])
print("top-2 after scaling, late_payment=2 :", [(label, round(distance, 3)) for distance, _, label in ranked_2[:2]])
```

An example output is as follows.

```text
top-2 after scaling, late_payment=0 : [('safe', 1.046), ('safe', 1.305)]
top-2 after scaling, late_payment=2 : [('safe', 0.975), ('risky', 1.184)]
```

### What Stayed The Same And What Changed?

- What stayed the same: after scale adjustment, distance still uses not only income but the late-payment axis as a real part of the comparison.
- What changed: with only a small increase in late-payment count, the second neighbor starts changing from `safe` to `risky`.
- Judgment to leave first: standardization is not a one-time technical check. It is also the starting point for seeing `how sensitive the neighbor composition and the prediction become` when one feature changes.

This comparison makes k-NN readable not as `a model that simply retrieves nearby cases`, but as `a comparison rule that is sensitive to representation and input changes`. What matters is not memorizing the value of `k`, but being able to explain which neighbors enter and leave when the representation or the feature values shift even for the same query. The learning effect of this repeated-change exercise appears when the reader can say not only `the prediction changed`, but also `what part of the comparison criterion was mixed again when one value changed`.

| Common record language | What to record immediately from this exercise |
| --- | --- |
| structure observed | after scaling was aligned, even a small feature change could mix the neighbor composition and the final judgment again |
| interpretation boundary | the fact that neighbors changed in one query alone does not prove that one feature is always more important |
| next question | if `k` changes, does the neighbor switch continue all the way to the final majority vote, and does the same sensitivity repeat for other queries? |

## Checklist

- Can you explain why a distance function is part of the judgment rule?
- Do you understand that if the distance function changes, the neighbor order and the prediction can change too?
- Do you understand that when a large axis dominates the distance, important information on a small axis can be buried?
- Can you explain standardization as rebalancing the comparison criterion?
- Are you comparing which neighbors entered and left before and after scale adjustment using the same query?
- Even when a difference appears after standardization, are you avoiding treating that alone as a complete causal explanation?

## Sources And References

- scikit-learn, *Nearest Neighbors*, scikit-learn User Guide, checked on 2026-06-27. <https://scikit-learn.org/stable/modules/neighbors.html>{: target="_blank" rel="noopener noreferrer" }
- scikit-learn, *Importance of Feature Scaling*, scikit-learn Examples, checked on 2026-06-27. <https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html>{: target="_blank" rel="noopener noreferrer" }
