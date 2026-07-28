# P4-12.1 Intuition For k-NN

> Section ID: `P4-12.1`
> Version: `v2026.07.26`

P4-11.2 showed [logistic regression](/AiBook/en/reference/concept-glossary-alpha/l/#logistic-regression) as `a model that draws a boundary in the input space and separates classes`. Now the question changes.

Can we make a judgment without drawing a line first, by looking instead at nearby similar examples?

That question is the starting point of k-NN (k-nearest neighbors). It is more accurate to read k-NN not as `a model that first builds a formula`, but as `a model that first looks for similar cases around a new input`.

## Questions Closed By k-NN Intuition

This Section answers the following questions.

- What basic idea does k-NN use to make a judgment?
- What roles do `query`, `neighbor`, `label`, and `k` each play?
- How does the character of the judgment change when `k` changes?
- What should training mean in k-NN?

This Section first closes `what basic idea k-NN uses to judge from nearby cases`. Why distance functions and scale change the result continues in `P4-12.2 Distance And Scale`, and the practical guidance continues in `P4-12.3 What Should Be Checked First When Using k-NN?`

## Judgments To Keep From k-NN Intuition

- You can explain k-NN as `a method that gathers nearby cases and makes a judgment by majority vote or average`.
- You can explain what `query`, `training data`, `neighbor`, and `label` each do inside the judgment.
- You can explain the difference between cases where `k` is too small and where it is too large.
- You can explain that training in k-NN is closer to `preparing reference cases for comparison` than to `building a complex formula`.

## Main Learning Content

### How Does k-NN Make A Judgment?

k-NN first looks at a new input, called the [query](/AiBook/en/reference/concept-glossary-alpha/q/#query). Then it finds cases in the [training data](/AiBook/en/reference/concept-glossary-alpha/t/#training-data) whose [labels](/AiBook/en/reference/concept-glossary-alpha/l/#label) are already known and are close to that query. Finally, it gathers the labels of those [neighbors](/AiBook/en/reference/concept-glossary-alpha/n/#nearest-neighbor) and creates a result by majority vote or average.

In short, the order is the following.

1. A new input (query) arrives.
2. Close cases are found in the existing training data.
3. The labels of those close cases are collected.
4. The result is made by majority vote or average.

So k-NN can be read as `a method that does not interpret a new point alone, but compares it with already known nearby cases`.

### What Does Each Term Do Inside The Judgment?

| Term | Role inside the judgment |
| --- | --- |
| query | the new input that we want to predict now |
| training data | the collection of reference cases where inputs and labels are already known |
| neighbor | a case selected because it is close to the query |
| label | the answer or category already attached to each reference case |
| `k` | the number that decides how many neighbors will be used |

This table matters because k-NN is closer to `how reference cases are read` than to `how an internal formula is computed`.

### Why Use Nearby Cases As Evidence?

The core assumption of k-NN is that `similar inputs are likely to have similar outputs`. This assumption is not always right, but it becomes a strong starting point in problems where local similarity really carries meaning.

Examples include the following.

- customers with similar purchase patterns may show similar responses
- users with similar click flows may belong to similar product-interest groups
- students with similar score patterns may fall into similar result categories

If this intuition is compressed into one calculation flow, it becomes the following.

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-1-mermaid-01-en.mmd"
```

But `close` does not automatically mean `correct`. If the criterion used to compute closeness changes, the neighbors themselves can change. That exact point is the topic of the next Section.

### What Does `k` Change?

`k` decides how many neighbors will be used.

- if `k = 1`, only the single closest case is used
- if `k = 3`, the three closest cases are used
- if `k = 5`, the judgment is made with a wider local neighborhood

Even for the same query, the character of the judgment changes when `k` changes.

| `k` value | Character that appears |
| --- | --- |
| too small | becomes sensitive to one or two nearby exceptions |
| moderate | can keep local patterns while reducing instability |
| too large | can mix in faraway cases and blur the boundary |

A tiny toy example makes that clearer.

| Labels around the query | `k = 1` | `k = 3` | `k = 5` |
| --- | --- | --- | --- |
| `1, 0, 0, 0, 0` | `1` | `0` | `0` |

This example shows that if only the single closest case is used, the answer is `1`, but if the neighborhood expands to three or five, the larger local majority can move the result to `0`. So `k` is not just a number. It is the handle that decides `how narrowly` or `how broadly` the model looks.

### What Does Training Mean In k-NN?

In linear regression or logistic regression, the usual explanation is that the model `learns coefficients`. k-NN feels different.

At an introductory level, training in k-NN is close to the following.

- store the inputs and labels
- prepare them so a new input can be compared later
- if needed, use an internal structure that makes distance calculation faster

So k-NN should be read not as `learning that builds a sophisticated formula in advance`, but as `learning that prepares reference cases to compare later`.

That is why two traits come together in k-NN.

- how the data are organized and represented matters
- the comparison cost can become large at prediction time

For example, if there are 100 training cases, one query needs 100 comparisons. If there are 100,000 training cases, the same query may need far more comparison work. Saying that `training is simple` does not mean that preparation is unimportant. It means that the cost of judgment can show up more clearly at prediction time than at training time.

### How Is It Different From A Linear-Boundary Model?

Logistic regression asks first `what single formula or boundary divides the whole space well?` In contrast, k-NN asks first `what kinds of cases are gathered around this point?`

| Model perspective | Central question |
| --- | --- |
| logistic regression | what boundary would separate the classes well? |
| k-NN | what class do similar cases around this new point have? |

Because of this difference, k-NN puts `local neighbors` ahead of a `global rule`.

## Cases And Examples

### Case 1. When A Team Wants To Judge A New Customer Through Similar Existing Customers First

A subscription-service team wants to estimate the churn risk of a new customer. A person would first look at signals such as `recent visits`, `complaint frequency`, `payment amount`, and `login time range`.

But the team has not yet found a simple rule strong enough to say `customers who churn always follow this pattern`. Instead, the existing records show that customers with similar behavior often end up with similar results. In that case, k-NN does not interpret the new customer alone. It first finds several similar existing customers nearby and uses their labels as evidence.

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-1-mermaid-02-en.mmd"
```

This case shows three key points.

- k-NN is closer to `a model that first refers to nearby cases` than to `a model that first writes a rule`.
- If `k=1`, the judgment can become sensitive to one exceptional person. If `k=5`, it can become more stable, but the boundary can blur.
- If the composition of neighbors splits, that is first a signal telling the reader `this query needs review`.

## Practice And Example

### Python Example: A Small k-NN

- problem situation: inspect which group a new point is closer to
- input: two features that can be read like 2D coordinates
- label: class 0 / class 1
- concept to check:
  - the prediction is made by reading neighbor labels
  - even for the same query, the result can actually change when `k` changes
  - a query near the boundary can shake interpretation easily

Values to change:

- Change `query` to `(4.3, 4.1)` or `(3.9, 4.0)` to see how the nearest-neighbor order changes.
- Change the `k` list to something like `[1, 2, 3, 5]` to check whether an even `k` can create a tie.

```python
# This example calculates distances between a new query and existing samples to choose k-NN neighbors and a predicted label.
from math import dist
from collections import Counter

train = [
    ((4.1, 4.1), 1),
    ((3.7, 4.0), 0),
    ((3.8, 4.3), 0),
    ((4.2, 3.8), 0),
    ((4.4, 4.0), 1),
]

query = (4.0, 4.2)

def knn_predict(train, query, k):
    ranked = sorted(
        [(dist(point, query), point, label) for point, label in train],
        key=lambda x: x[0],
    )
    neighbors = ranked[:k]
    labels = [label for _, _, label in neighbors]
    prediction = Counter(labels).most_common(1)[0][0]
    return prediction, neighbors

for k in [1, 3, 5]:
    prediction, neighbors = knn_predict(train, query, k)
    print(f"k={k}, prediction={prediction}")
    for d, point, label in neighbors:
        print(" ", point, "label=", label, "distance=", round(d, 3))
    print()
```

An example output is as follows.

```text
k=1, prediction=1
  (4.1, 4.1) label= 1 distance= 0.141

k=3, prediction=0
  (4.1, 4.1) label= 1 distance= 0.141
  (3.8, 4.3) label= 0 distance= 0.224
  (3.7, 4.0) label= 0 distance= 0.361

k=5, prediction=0
  (4.1, 4.1) label= 1 distance= 0.141
  (3.8, 4.3) label= 0 distance= 0.224
  (3.7, 4.0) label= 0 distance= 0.361
  (4.4, 4.0) label= 1 distance= 0.447
  (4.2, 3.8) label= 0 distance= 0.447
```

This output shows directly that `k` is not just a number. It is the handle that changes the range of the judgment.

- Under `k=1`, the single closest point is class 1, so the prediction is `1`.
- Once it widens to `k=3`, two of the three closest points are class 0, so the prediction changes to `0`.
- Under `k=5`, class 0 still remains the majority, so the prediction stays `0`.

In other words, this example closes the point that `one exceptional nearest point` and `a slightly wider local majority` can say different things. The first thing to read here is not the score but `which neighbors were included` and `how the majority changed because of that`.

## Checklist

- Can you explain k-NN as `a method that gathers nearby cases and makes a judgment`?
- Do you understand that `query`, `neighbor`, `label`, and `k` play different roles inside the judgment?
- Can you explain that `k` is not just a number, but the handle that controls the range of the judgment?
- Can you explain the difference between when `k` is too small and when it is too large?
- Do you understand that training in k-NN is closer to `preparing reference cases for comparison` than to `building a formula`?
- Do you know that the comparison cost can become large at prediction time in k-NN?

## Sources And References

- scikit-learn, *Nearest Neighbors*, scikit-learn User Guide, checked on 2026-07-26. <https://scikit-learn.org/stable/modules/neighbors.html>{: target="_blank" rel="noopener noreferrer" }
