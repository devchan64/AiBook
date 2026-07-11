# P4-11.2 Decision Boundary

> Section ID: `P4-11.2`
> Version: `v2026.07.11`

In P4-11.1, logistic regression was read as `a linear model that creates scores that can be read like probabilities`. Now the question changes by one step.

Why does that score divide some inputs into class 0 and others into class 1?

To answer that, it is not enough to ask only `what is the probability?` The reader also has to see `up to where is it read as class 0, and from where is it read as class 1?` The perspective that reads that criterion inside the input space is the decision boundary.

So the phrase `where does the model draw a line in the input space?` is closer to a result than the deepest idea. The more essential question is the following.

By what rule does the model read inputs as two different sides?

If P4-11.1 was the Section of reading the output, P4-11.2 is the Section of looking back at the input.

`A decision boundary is the criterion line or criterion surface that separates class 0 and class 1.`

This Section does not repeat the basic definition of logistic regression at length. The core intuition, `a linear classifier that makes a score that can be read like a probability`, reconnects through P4-11.1 and the [concept glossary](../../../reference/concept-glossary.md). Here the focus stays on how that score divides the input space.

## Scope Of This Section

This Section answers the following questions.

- What is a decision boundary?
- How does the boundary look in a one-dimensional input?
- Why does it look like a line in a two-dimensional input?
- How do coefficients relate to the direction of the boundary?
- How can the boundary change when the threshold changes?

This Section does not treat the following topics deeply.

- rigorous hyperplane geometry in high-dimensional spaces
- boundary partitioning in multiclass classification
- mathematical development of kernel methods and nonlinear boundaries
- implementation details of plotting the boundary

The hyperplane intuition reconnects again in P4-1.2, and kernel methods and nonlinear boundaries return in P4-13.1 and P4-13.2. Settings such as `C`, `gamma`, and threshold adjustment reconnect again in P4-9.1 and P4-9.2. Detailed multiclass boundary partitioning and plot implementation stay outside the current main scope of this book.

## Goals Of This Section

- You can explain a decision boundary not as `an output score` but as `a criterion that divides the input space`.
- You can understand that in one dimension the boundary looks like `one point`, and in two dimensions it usually looks like `one line`.
- You can explain that the coefficients of logistic regression participate in changing the direction of the boundary.
- You can explain that when the threshold changes, the boundary interpretation can move too.
- You can connect the probability-output view of 11.1 and the boundary view of 11.2 as two descriptions of the same model.

## Learning Background

### Why Read The Decision Boundary Separately?

In 11.1, the reader saw scores such as `0.58` and `0.73`. But in practice and in learning, the following questions often matter more.

- Why did one input become class 0?
- Why did another input become class 1?
- Where is the criterion that separates the two classes?

Those questions cannot be answered sufficiently from an output table alone. The output table shows `the result`, but not enough of `why that result appeared`.

This is why the decision boundary is needed.

- to explain why an input became class 0
- to explain why an input became class 1
- to say where the criterion that separates the two classes lies
- to identify near-boundary cases that should be treated as ambiguous

So the decision boundary is not merely a visualization device. It is an `interpretation tool for reading why classification happened`.

The perspective that appears when we need to ask `where did the model divide the space into two sides?` is the decision boundary.

It should also be read together with the following four items.

| What to read together | Why it is needed |
| --- | --- |
| baseline classification result | because we still need to know whether the linear boundary is actually better than a simple rule |
| threshold position | because the criterion that changes the class must be visible even with the same score |
| problem cells in the confusion matrix | because we need to see what kind of misclassification the boundary is creating |
| representative near-boundary examples | because we need to explain why ambiguous inputs crossed to the opposite side |

So this is not a Section about drawing a line prettily. It is a Section about reading together `what improved compared with what`, `where the class changes`, and `what type of error appears as a result`.

If one more point is added, the decision boundary becomes even more directly connected to operational interpretation. Near-boundary cases are not just `ambiguous points`. They are cases that should be left first as priority review targets. In that sense, the decision boundary can also be read as a comparison frame for deciding `which inputs should be checked by a human again`. The fact that a case lies near the boundary shows a change signal and review priority. It does not automatically complete the causal explanation of why the case crossed.

The same comparison frame should be kept here too. The same baseline, the same score ranges, and the same representative failure cases should be used before and after the boundary so that `model score change`, `threshold policy change`, and `lack of feature representation` are not mixed together too easily.

| What to keep when reading the boundary | Why it is needed |
| --- | --- |
| IDs of near-boundary examples | to find review targets again |
| changed classifications relative to the baseline | to see which cases were newly separated compared with a simple rule |
| cases that moved after a threshold change | to see which inputs crossed because of a policy change |
| next review question | to decide whether to add features or adjust the threshold |

## Main Learning Content

### What Is A Decision Boundary?

A classification model usually computes an internal score and divides classes based on that score. The decision boundary is `the location where that score becomes equal to the criterion value`.

If logistic regression is simplified at an introductory level, it can be imagined as follows.

\[
z = w_1x_1 + w_2x_2 + \cdots + w_nx_n + b
\]

If this linear score \(z\) is passed through sigmoid, a value between 0 and 1 appears. When threshold 0.5 is used, the place where the sigmoid output becomes 0.5 becomes the class boundary.

Sigmoid output 0.5 corresponds to the linear score \(z = 0\). So the decision boundary of logistic regression can usually be understood as `the place where the linear score becomes 0`.

`The decision boundary is the place where the probability becomes ambiguous and the place where the class splits.`

### In One Dimension, The Boundary Looks Like One Point

If there is only one input, the boundary appears not as a line but as `one point`.

Suppose the input is just `study_hours`. The model can separate fail and pass using some time value as the criterion.

| Study hours | Class 1 score | Prediction |
| ---: | ---: | --- |
| 3 | 0.17 | fail |
| 4 | 0.31 | fail |
| 5 | 0.55 | pass |
| 6 | 0.76 | pass |

In this case, the boundary can be read as lying `somewhere between 4 and 5 hours`. So a one-dimensional decision boundary is close to `one cutoff point`.

The idea can be drawn as follows.

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-01-en.mmd"
```

The key in this diagram is that as the input value increases, the score rises, and around the `score 0.50` boundary point the model splits the axis into the class 0 side and the class 1 side.

This becomes especially important when threshold is inspected. What looked like a score table in 11.1 starts to reappear in 11.2 as `a boundary point on the input axis`.

### In Two Dimensions, The Boundary Looks Like A Line

Now suppose there are two inputs, such as `exam_1` and `exam_2`, and the task is to classify pass or fail. Then the input space is easier to imagine as a plane rather than as a single table.

- one axis is `exam_1`
- the other axis is `exam_2`
- each student becomes one point on that plane

In this setting, logistic regression tries to find the criterion line that separates those points into two sides. So in two dimensions the decision boundary usually appears like `a line`.

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-02-en.mmd"
```

This diagram shows the decision boundary of logistic regression as the trace left in the input space by a rule that compares the score \(z\) with zero. What matters is not that the line exists first. Rather, because the linear score changes sign across the plane, the class changes too.

`When one more input dimension is added, the boundary changes from one point to one line.`

The important point here is not `there is a line first and then the class splits`, but `because the rule compares z with 0, a boundary line appears as a result on the plane`.

### How Do Coefficients Relate To The Direction Of The Boundary?

The coefficients of logistic regression are not used only to compute the score. When viewed in the input space, they also influence the direction in which the boundary is placed.

If there are two features,

\[
z = w_1x_1 + w_2x_2 + b
\]

then the relative size and sign of \(w_1\) and \(w_2\) change the slope and direction of the boundary line.

The following intuition is more important than a formal derivation.

- If the coefficient of one feature becomes larger, the influence of that axis can become stronger.
- If the combination of the two coefficients changes, the tilt of the class-separating boundary changes too.
- The intercept shifts the boundary in parallel.

So in 11.1 the coefficients were `numbers that make a score`, while in 11.2 they also become `numbers that define a boundary`.

### The Boundary Can Move If The Threshold Changes

In 11.1, the reader saw that the final behavior changes when the threshold changes. In 11.2 that statement has to be reread from the spatial perspective.

The boundary under threshold 0.5 and the boundary under threshold 0.7 do not need to sit at the same place. The reason is simple.

- threshold 0.5: choose class 1 from the place where the score crosses this level
- threshold 0.7: require a higher score before class 1 is chosen

So when the threshold rises, the region classified as class 1 can shrink, and the boundary can move in a more conservative direction.

`The coefficients of the model create the direction of the boundary, and the threshold can readjust where that boundary is applied.`

This movement can be drawn conceptually as follows.

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-03-en.mmd"
```

The key is that even without retraining the model, a stricter threshold pushes the effective boundary to the right on the same score axis and reads a smaller class 1 region. So a boundary shift should be read as a policy change that changes which cases cross the line, not as a complete causal explanation of the features.

The following three lines should be kept together in decision-boundary notes.

- Near-boundary cases are signals to raise review priority, not automatic confirmation.
- If the threshold changes, the same input can move to a different action.
- A boundary shift can be observed, but the shift itself does not finish the causal explanation.

### When Is The Decision-Boundary Perspective Especially Important?

The decision boundary is not just a pretty picture. It becomes especially important when the reader must ask `why did this input cross into the other class?`

| What the reader wants to inspect now | Why the decision-boundary perspective is needed | What to check together |
| --- | --- | --- |
| ambiguous cases near the boundary | because the score alone does not explain well why they split | threshold and the review zone |
| repeated misclassification of one type | because the reader must see how the boundary is tilted | the problem cells of the confusion matrix |
| deciding whether to change the threshold | because the effect of the policy change must be read in the input space | changes in cases before and after the threshold |
| suspecting that more features are needed | because the current boundary may be too simple | cases newly separated compared with the baseline |
| selecting human-review targets | because near-boundary cases define review priority | case IDs and score ranges |

The point of this table is not to admire the picture of the boundary, but to track `where the classification rule really splits and what it misses`.

## Cases And Examples

Before the cases, the common comparison frame of this Section can be organized as follows.

| Scene | Easy rule a person might use first | Limit of that rule | What the decision-boundary perspective changes | Result to check |
| --- | --- | --- | --- | --- |
| exam-pass prediction | use one cutoff on one score | weak when several features act together | read it as a combined criterion | the boundary becomes a line or plane rather than one point |
| customer churn | judge risk from one variable | misses combined patterns | check whether a combination of features creates a risk region | explain which combinations lie beyond the boundary |
| medical risk | judge risk from one number | misses ambiguous combinations | separate near-boundary cases for review | identify review-priority targets |
| loan / spam | explain approval or blocking with one simple rule | misses mixed features and the limit of a linear boundary | inspect which combinations the boundary separates | read both the strength and the limit of a linear boundary |

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-04-en.mmd"
```

## Practice And Example

### Python Example: Read The Same Scores Under Two Thresholds

```python
import numpy as np

proba_class_1 = np.array([0.48, 0.62, 0.81])

pred_05 = (proba_class_1 >= 0.5).astype(int)
pred_07 = (proba_class_1 >= 0.7).astype(int)

print("class 1 scores  :", proba_class_1)
print("threshold 0.5   :", pred_05)
print("threshold 0.7   :", pred_07)
```

An example output is as follows.

```text
class 1 scores  : [0.48 0.62 0.81]
threshold 0.5   : [0 1 1]
threshold 0.7   : [0 0 1]
```

This result shows that a score like `0.62` can already look fairly positive from the model's perspective, but under a stricter threshold it can still remain outside the class 1 region.

### Change One More Value: What Stays The Same And What Changes If The Threshold Becomes Even Higher?

Now keep the same score array and raise the threshold again to `0.9`.

```python
import numpy as np

proba_class_1 = np.array([0.48, 0.62, 0.81])

pred_07 = (proba_class_1 >= 0.7).astype(int)
pred_09 = (proba_class_1 >= 0.9).astype(int)

print("class 1 scores  :", proba_class_1)
print("threshold 0.7   :", pred_07)
print("threshold 0.9   :", pred_09)
```

An example output is as follows.

```text
class 1 scores  : [0.48 0.62 0.81]
threshold 0.7   : [0 0 1]
threshold 0.9   : [0 0 0]
```

### What Stayed The Same And What Changed?

- What stayed the same: the relative order of the scores is unchanged. `0.81` is still closest to class 1, and `0.48` is still the farthest.
- What changed: once the threshold rose again, even `0.81`, which used to look like an automatic candidate, no longer became class 1 automatically.
- Judgment to leave first: the score itself and the final behavior are not the same stage. Not only near-boundary cases, but even cases that once looked certain can return to the review pool when the operating criterion changes.

### How This Exercise Recovers The Goal Of Part 4

This exercise makes the classification model readable not as `a probability calculator` but as `a device whose operating boundary can be adjusted`. What matters in Part 4 is not merely raising one score. It is reading which cases move from automatic handling to review when the threshold changes, and how error costs move with them. Repeating the same score array while changing only the boundary trains the reader to separate `model output` from `applied judgment`.

| Common record language | What to record immediately from this exercise |
| --- | --- |
| structure observed | with the same score array, a higher threshold shrank the class 1 region and returned former automatic cases to review |
| interpretation boundary | a more conservative threshold does not always mean a better policy; false-negative cost still has to be checked together |
| next question | is the reduced false-positive risk more important than the increased false-negative and review cost in the current setting? |

## Supplementary Reading Points

### Where Do The Main Discussion Points Arise?

Even though the decision boundary can look simple as a picture, there are several places where readers often misunderstand it.

### 1. Is The Boundary A Wall?

No. The decision boundary is not a physical wall in the real world. It is `a separating criterion drawn by the model for convenience`. Samples near the boundary can cross into the other class with a small change.

### 2. Does Farther From The Boundary Always Mean More Certain?

In logistic regression, points farther from the boundary usually tilt the score more strongly toward one class. But that does not guarantee perfect certainty in the real world. Data quality and data distribution still matter.

### 3. Is A Linear Boundary Always Enough?

No. If the data are mixed in a curved shape, or if the class structure is very complex, one line may not be enough. That limitation is why more complex models appear later.

### 4. Does The Boundary Stay Fixed Even If The Data Change?

No. If the training data change, the coefficients and intercept can change, and then the position and direction of the boundary can change as well. So a decision boundary is closer to `a learning result produced by the current data and model` than to `a line discovered from nature`.

This point connects directly with why train/test split, sample bias, and dataset updates matter.

### 5. Why Should Near-Boundary Samples Be Treated Carefully?

Samples far from the boundary are usually classified more stably. Samples near the boundary can switch class with a small change.

Because of that, real services often attach policies such as the following.

- if the point is far from the boundary, handle it automatically
- if it is near the boundary, send it to human review
- gather near-boundary cases separately for quality inspection

So the decision boundary can be used not only to split classes, but also to find `which cases are ambiguous and operationally risky`.

### 6. Are A Good Boundary And A Good Service Always The Same Thing?

Not necessarily. A boundary may look clean from the model perspective but still be inappropriate from the service perspective. If the cost of misclassification differs across classes, the safest operating boundary may differ from the mathematically neatest one.

This point connects to the threshold of 11.1, the evaluation metrics in the early part of Part 4, and model selection later.

## Perspectives To Remember In This Section

- A decision boundary is the criterion line or surface that divides classes.
- In one dimension it looks like one point, and in two dimensions it usually looks like one line.
- The coefficients and intercept of logistic regression participate in the direction and position of the boundary.
- If the threshold changes, the class regions and the boundary interpretation can change too.
- The boundary is a way of rereading the model's computation inside the input space.

This is not a Section about learning how to draw lines. It is a Section about reading boundaries inside the evaluation flow.

| What should be read together | First question to read in this Section | Where it reconnects later |
| --- | --- | --- |
| threshold position | where does the class split, and how conservative is the boundary | P4-6 classification metrics, P4-15.3 threshold adjustment |
| problem cells of the confusion matrix | what kind of FP or FN is this boundary creating more often | P4-6 evaluation metrics |
| representative near-boundary examples and baseline comparison | why did ambiguous inputs cross, and is this really better than a simple rule | P4-8 baseline, later classification-model comparison |

## Checklist

- Are you looking not only at output scores but also at where the split occurs in the input space?
- Are you separating cases that crossed because of threshold change from cases that failed because the feature representation was too weak?
- Are you leaving near-boundary cases not as automatic confirmations but as review-priority signals?

## When To Recall This Perspective First

- When classification scores are visible but the explanation of where the input space splits is blurry, draw the decision boundary first.
- When you need to interpret which samples crossed to the opposite side after a threshold change, read the boundary position and the change in class regions together.
- When a linear model feels unsatisfying in a vague way, return to this Section as the starting point for asking whether the limit comes from the straight boundary itself or from weak representation.

## Connection To The Next Sections

P4-11.2 showed where logistic regression `draws the line`. The next questions change again.

- Is a straight boundary enough?
- What other classification algorithms explain the data better?
- How do evaluation metrics and model selection compare these boundaries?

So 11.2 is the Section where the reader begins to read a classification model as `a device that divides space`. That perspective continues directly into trees, SVMs, and more complex classifiers.

## Sources And References

- Ronald A. Fisher, `The Use of Multiple Measurements in Taxonomic Problems`, *Annals of Eugenics*, 1936, DOI: [https://doi.org/10.1111/j.1469-1809.1936.tb02137.x](https://doi.org/10.1111/j.1469-1809.1936.tb02137.x){: target="_blank" rel="noopener noreferrer" }, checked on 2026-06-29.
- Benyamin Ghojogh, Mark Crowley, `Linear and Quadratic Discriminant Analysis: Tutorial`, arXiv, 2019, [https://arxiv.org/abs/1906.02590](https://arxiv.org/abs/1906.02590){: target="_blank" rel="noopener noreferrer" }, checked on 2026-06-29.
- scikit-learn, `1.1.11. Logistic regression`, scikit-learn User Guide, checked on 2026-06-26. [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `LogisticRegression`, scikit-learn API Reference, checked on 2026-06-26. [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }
