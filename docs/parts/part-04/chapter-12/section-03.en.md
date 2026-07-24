# P4-12.3 What Should Be Checked First When Using k-NN?

> Section ID: `P4-12.3`
> Version: `v2026.07.24`

P4-12.1 introduced the intuition of k-NN, and P4-12.2 showed why distance and scale can change the result. The remaining question is the following.

When the judgment of k-NN shakes, what should be checked first?

The purpose of this Section is not to explain preprocessing in general again. It is to organize `what should be inspected first` when reading k-NN.

## Scope Of This Section

This Section answers the following questions.

- In what kind of problem is k-NN a good first candidate?
- What signals suggest that distance or scale should be suspected first?
- Among `distance rule`, `k`, and `data representation`, what should be rechecked first?
- How should a query that needs review be read?

## Goals Of This Section

- You can explain what kinds of problems make k-NN worth raising as a first candidate.
- You can explain the signals that suggest a distance or scale issue.
- When the result shakes, you can set an order for what should be rechecked first.

## Main Learning Content

### When Is k-NN A Good First Candidate?

k-NN is not the default answer for every classification problem. But when `explaining by nearby similar cases` is a natural reading of the problem, it can be a good first comparison candidate.

| Current problem state | Why think of k-NN first |
| --- | --- |
| similar cases tend to show similar results | because it is easy to explain the prediction by nearby neighbors |
| local pattern matters more than one global rule | because the query can be compared directly with nearby cases |
| the team wants an example-based judgment before a formula-based one | because the neighbors themselves become the explanation |
| the dataset is not too large and the comparison cost is manageable | because prediction-time comparison is still realistic |

The key point is not `use k-NN because no formula can be written`. It is that `when local similarity is naturally meaningful, k-NN can be a good starting point`.

### What Signals Suggest A Distance Or Scale Problem First?

In a distance-based model, when performance looks strange, it is often better to suspect first `which axis is deciding almost the whole distance by itself` rather than jumping immediately to the model structure.

| Signal that appears | What to suspect first | Why |
| --- | --- | --- |
| one column has a much larger numeric range than the others | scale domination | because one large axis may monopolize the distance |
| neighbors change heavily before and after scale adjustment | representation dependence | because the definition of nearness is sensitive to representation change |
| a small-range column is important but barely appears in the prediction | burial under a large axis | because useful information may be hidden inside the distance |
| the same kind of query keeps gathering near the boundary | distance rule or `k` setting | because the neighbor order may be unstable |

The goal of this table is not to make scale adjustment a magic solution. It is to make the reader check first whether `the definition of nearness is already shaking`.

### What Should Be Rechecked First?

When the result shakes, it is usually helpful to inspect in the following order.

1. Is this really a problem that should be read through `comparison with nearby cases`?
2. Does the current distance rule fit the problem?
3. Is `k` too small or too large?
4. Is scale or data representation pushing one axis too strongly?
5. Is the prediction-time comparison cost actually manageable?

This order matters because each question points to a different kind of issue.

- item 1 is a `model family` question
- items 2 and 3 are `judgment rule` questions
- item 4 is a `representation` question
- item 5 is an `operational cost` question

So even the single sentence `the result looks strange` can hide causes from several different layers.

Especially once scale or representation becomes suspicious at item 4, the general theory of preprocessing itself should not be re-explained at length here. It is more appropriate to return to `P4-7.2 Preprocessing` and recheck the criteria there.

### If The Same Query From P4-12.1 Is Read Again

If the query `(4.0, 4.2)` from the previous Section is brought back, the inspection order becomes more concrete.

| Question to recheck | What is actually seen in `(4.0, 4.2)` | Judgment to make now |
| --- | --- | --- |
| is `k` too sensitive? | under `k=1` the class is 1, under `k=3` it becomes 0 | recheck `k`, because one exceptional point may be shaking the result |
| is the neighbor composition mixed? | nearby labels are mixed, such as `1, 0, 0, 1, 0` | the query is likely near the boundary |
| would the result change if the distance rule changed? | even with the same coordinates, neighbor order can change under a different distance rule | continue into the distance-rule comparison of `P4-12.2` |
| should scale be suspected too? | in this toy coordinate example, scale is not the main issue | in real data with different numeric ranges, return to `P4-7.2` and `P4-12.2` |

The point of this table is not to make the reader memorize a checklist. It is to show, for one concrete query, `where suspicion should be reopened first`.

### A Small Flow For Rechecking One Query All The Way Through

If the previous table is compressed again into an actual judgment order, the sentence `the result is ambiguous` becomes not a vague feeling, but a process of finding `which step is shaking`.

1. First inspect whether the neighbors are clearly biased to one side.
2. If the split comes from only one or two points, inspect whether the interpretation stays the same when `k` changes.
3. If it still shakes after a small `k` change, inspect whether the distance rule itself fits the current problem.
4. If there are features with very different numeric ranges, inspect scale and data representation last.

So a review query is better read not as `one wrong prediction`, but as `an observation point that shows which layer of the judgment rule is shaking`.

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-3-mermaid-01-en.mmd"
```

### How Should A Query That Needs Review Be Read?

A query that needs review is usually one where `the neighbor composition does not lean clearly to one side`.

Examples include the following.

| query | nearest labels | reading now |
| --- | --- | --- |
| `(4.0, 4.2)` | `[1, 0, 1]` | leaning toward class 1, but likely near the boundary |
| `(4.0, 4.2)` with `k=5` | `[1, 0, 1, 0, 0]` | the interpretation may change when the neighborhood widens |

What matters here is that `the neighbors split` does not finish the explanation of the cause. It is first a signal that tells the reader `what needs to be rechecked`.

In other words, a review query is usually read in the following order.

1. how much the neighbor composition is split
2. whether the interpretation stays the same when `k` changes
3. whether the neighbors change when the distance rule changes
4. which neighbors enter and leave before and after scale adjustment

These four questions matter because each one aims at a different cause.

- item 1 asks `is this query near the boundary now?`
- item 2 asks `is the result too sensitive to one or two exceptional neighbors?`
- item 3 asks `does the current definition of nearness fit the problem?`
- item 4 asks `is the representation distorting the judgment?`

## Cases And Examples

### Case 1. When Prediction Exists But The Explanation Keeps Shaking

A subscription-service team is using k-NN to inspect churn risk. The prediction itself works to some degree, but two customers who look similar keep receiving different predictions.

At that point, the team should not jump immediately to `should we switch models?` First it should recheck the following.

- does this problem really read naturally through local similarity?
- does the current distance rule fit the features?
- is the configuration too sensitive, such as `k=1`?
- is a large axis such as payment amount crushing the other features?

This order helps the reader separate `failure of the model family` from `instability of the judgment criterion`.

So the goal of this Section is not the vague conclusion `k-NN must be used carefully`. More precisely, it is to let the reader explain for themselves `what should be reopened first when the prediction starts to shake`.

## Practice And Example

This example keeps the same query and checks how `k` and scaling change the neighbor list and prediction.

- Problem situation: predict churn with k-NN from monthly spending and support-ticket count
- Input: each customer's `monthly_spend`, `support_tickets`, and `churn`
- Expected output: prediction by `k`, nearby-neighbor IDs, and the changed neighbors after scaling
- Concepts to check:
  - `k=1` can be pulled strongly by one nearest case
  - increasing `k` can change the local majority vote
  - features with different numeric ranges can change neighbor order before and after scaling

```python
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

customers = pd.DataFrame(
    [
        {"id": "A", "monthly_spend": 30, "support_tickets": 0, "churn": 0},
        {"id": "B", "monthly_spend": 58, "support_tickets": 0, "churn": 0},
        {"id": "C", "monthly_spend": 61, "support_tickets": 0, "churn": 0},
        {"id": "D", "monthly_spend": 65, "support_tickets": 0, "churn": 0},
        {"id": "E", "monthly_spend": 40, "support_tickets": 8, "churn": 1},
        {"id": "F", "monthly_spend": 62, "support_tickets": 8, "churn": 1},
        {"id": "G", "monthly_spend": 90, "support_tickets": 9, "churn": 1},
    ]
)

X = customers[["monthly_spend", "support_tickets"]]
y = customers["churn"]
query = pd.DataFrame([{"monthly_spend": 63, "support_tickets": 7}])

for k in [1, 3, 5]:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X, y)
    distances, indices = model.kneighbors(query, n_neighbors=k)
    neighbor_ids = customers.iloc[indices[0]]["id"].tolist()
    print("raw k=", k, "prediction=", int(model.predict(query)[0]), "neighbors=", neighbor_ids)

scaled_model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
scaled_model.fit(X, y)
knn = scaled_model.named_steps["kneighborsclassifier"]
scaled_query = scaled_model.named_steps["standardscaler"].transform(query)
distances, indices = knn.kneighbors(scaled_query, n_neighbors=3)
neighbor_ids = customers.iloc[indices[0]]["id"].tolist()
print("scaled k= 3 prediction=", int(scaled_model.predict(query)[0]), "neighbors=", neighbor_ids)
```

The output is as follows.

```text
raw k= 1 prediction= 1 neighbors= ['F']
raw k= 3 prediction= 0 neighbors= ['F', 'C', 'D']
raw k= 5 prediction= 0 neighbors= ['F', 'C', 'D', 'B', 'E']
scaled k= 3 prediction= 1 neighbors= ['F', 'E', 'G']
```

This output does not mean readers should immediately say `k-NN is wrong`. With the same query, `k=1` is pulled by the single nearest case F, while `k=3` changes the prediction once C and D enter the neighborhood. After scaling, support-ticket count is reflected more clearly in the distance calculation, so E and G enter the nearby-neighbor set. Therefore, when a query shakes, readers should reopen `k`, neighbor composition, and scale in order.

## Checklist

- Can you explain that k-NN can be a good first comparison candidate in problems where local similarity matters?
- Can you distinguish problems where k-NN should be raised first from problems where it should not?
- Did you understand that when the result shakes, it is usually better to reopen `distance rule`, `k`, and `data representation` before the model name itself?
- Can you explain in what order to inspect `distance rule`, `k`, and `scale` when the result shakes?
- Are you reading a review query not as `cause confirmed`, but as `reinspection signal`?

## Sources And References

- scikit-learn, *Nearest Neighbors*, scikit-learn User Guide, checked on 2026-06-27. <https://scikit-learn.org/stable/modules/neighbors.html>{: target="_blank" rel="noopener noreferrer" }
- scikit-learn, *Importance of Feature Scaling*, scikit-learn Examples, checked on 2026-06-27. <https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html>{: target="_blank" rel="noopener noreferrer" }
