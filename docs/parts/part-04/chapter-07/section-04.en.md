# P4-7.4 Supplementary Learning: Distinguishing Feature Selection Methods

> Section ID: `P4-7.4`
> Version: `v2026.07.26`

From P4-7.1 to P4-7.3, the discussion chose [features](/AiBook/en/reference/concept-glossary-alpha/f/#feature), separated input-representation problems, and established the basic judgment for preprocessing. In practice, however, the reader soon meets names such as the following.

- statistical-test-based feature selection
- recursive feature elimination (RFE)
- [dimensionality reduction](/AiBook/en/reference/concept-glossary-alpha/d/#dimensionality-reduction)

All of these can look similar in that they `reduce the input or represent it again`, but they differ in what criterion is used to reduce and in what is left behind.

## Where Reduction Methods Split

This Section answers the following questions.

- What is different among filter, wrapper, and embedded feature selection?
- On what idea does statistical-test-based feature selection operate?
- What does recursive feature elimination (RFE) repeat?
- How is dimensionality reduction different from feature selection?

This Section first closes `how to distinguish names that reduce input or re-express it`. The intuition and limits of individual dimensionality-reduction algorithms continue in P4-18.1 and P4-18.2.

## Judgments To Keep When Distinguishing Method Names

- You can distinguish [feature selection](/AiBook/en/reference/concept-glossary-alpha/f/#feature-selection) and dimensionality reduction without mixing them as the same task.
- You can explain what criterion filter, wrapper, and embedded approaches use to reduce features.
- You can say that RFE is `a method that repeatedly runs a model and reduces less important features`.

## First Grasp The Big Picture

Start with the following table.

| Method | What is kept or changed | Judgment criterion |
| --- | --- | --- |
| filter | chooses some of the original features | statistics, correlation, univariate scores |
| wrapper | repeatedly compares subsets of the original features | model performance |
| embedded | creates importance together within the learning process | internal model rules |
| dimensionality reduction | re-expresses the original features into new axes | variance, distance, structure preservation, and so on |

The core point is this.

`Feature selection is mainly the work of deciding which original features should remain, while dimensionality reduction is the work of re-expressing several features into fewer new axes.`

## Where Does Statistical-Test-Based Feature Selection Belong?

Statistical-test-based feature selection usually belongs to the filter approach. In other words, it scores or tests the relationship between each feature and the answer, then reduces feature candidates based on that result.

This approach is intuitive in the following scenes.

- when there are many features and a quick first-pass reduction is needed
- when readers want to reduce candidates before repeatedly training a complex model
- when readers want to inspect each feature individually first

In return, this approach may not fully reflect `the effect created when feature combinations work together`. So in this Section, it is treated as an approach closer to `a quick first-pass arrangement`.

## What Does Recursive Feature Elimination (RFE) Repeat?

RFE can be viewed as a representative example of the wrapper approach. Put very simply, it repeats the following sequence.

1. Train a model on the current feature set.
2. Remove some of the features with low importance.
3. Train again with the remaining features.
4. Repeat until the number is reduced to the desired count.

That means RFE is a method that repeatedly checks `which features are less helpful inside the current model`.

It can cost more computation than the filter approach, but it more easily reflects `usefulness when viewed together with the current model`.

## Why Should Dimensionality Reduction Be Viewed As A Separate Category?

Dimensionality reduction can look like the work of discarding features, but in reality it is more often `the work of creating new axes`.

For example:

- feature selection can leave only two out of `age`, `income`, and `visits`
- dimensionality reduction can mix these three features and change them into new axes such as `component_1` and `component_2`

So dimensionality reduction needs to be read differently from `the work of reducing while keeping the original column names`.

| Question | Feature selection | Dimensionality reduction |
| --- | --- | --- |
| Do the original feature names remain? | often yes | usually no, they become new axes |
| Is interpretation easy? | relatively easier | it can become harder |
| Purpose | reduce unnecessary features | compress representation, summarize structure, visualize |

The goals and limits of dimensionality reduction itself are revisited in much more detail in P4-18.1 and P4-18.2.

## Cases And Examples

### What Kind Of Reduction Method Should Come To Mind First?

When method names are mixed together, organizing first around `will the original columns remain`, `will reduction be based on model performance`, or `will the data be re-expressed into new axes` makes the situation clearer much faster.

| Judgment needed right now | Method to bring to mind first | Reason |
| --- | --- | --- |
| I want to do a quick first-pass reduction of many columns | filter | because candidates can be reduced quickly with statistics or univariate scores |
| I want to reduce features that help little under the current model | wrapper, for example RFE | because feature subsets are compared repeatedly together with model performance |
| I want to obtain importance during the learning process itself | embedded | because selection happens together through internal model rules |
| Compression and structure summary matter more than interpretation | dimensionality reduction | because the representation is rebuilt into new axes instead of the original columns |

This distinction must come first so that readers do not mix different kinds of work under the one sentence `reduce dimensions`.

### Case 1. When The Names Of Reduction Methods Look Mixed Before Customer Segmentation

A marketing team is preparing customer segmentation and wants to reduce the input columns. The criteria people first used were behavioral signals such as `recent visits`, `purchase amount`, `discount response`, and `inquiry patterns`.

But in the meeting, different method names appear all at once. One person suggests removing columns with low correlation first, another suggests repeatedly running a model and reducing columns with low importance, and another suggests reducing axes with PCA. All of them are grouped under the phrase `reduce dimensions`, but in reality what is kept and what is changed are different.

```mermaid
--8<-- "assets/part-04/chapter-07/p4-7-4-mermaid-01-en.mmd"
```

The distinction needed here is the following. The filter approach is closer to quickly inspecting the original features and reducing first-round candidates, while RFE, which is a wrapper approach, repeatedly reduces features based on current model performance. Dimensionality reduction is closer not to choosing some of the original columns, but to mixing several features and re-expressing them as new axes.

The confirmable results must also be read differently. With filter and RFE, readers can view a list of which original columns remained, but dimensionality reduction changes the data into new axes such as `component_1` and `component_2`, so the interpretation method itself changes. So even when the same phrase `reduce input` is used, readers must first decide whether they want to preserve interpretability or compress into a new representation.

## Practice And Example

This example compares what a filter method, RFE, and PCA leave behind on the same data.

- Problem situation: reduce six customer-behavior features to three retained features or three axes
- Input: a small classification dataset generated by scikit-learn
- Expected output: retained original feature names, new component names, cross-validation score, and input shape
- Concepts to check:
  - filter and RFE choose some of the original features
  - PCA re-expresses the data into new axes instead of preserving original feature names
  - similar-looking scores do not mean the same level of interpretability

Values to change:

- Change the `3` in `SelectKBest(..., k=3)`, `RFE(..., n_features_to_select=3)`, and `PCA(n_components=3)` to `2` or `4`; the number of retained features, the number of new axes, and the scores will change together.
- Change `class_sep=1.1` or `random_state=7`; the selected feature lists and score gaps may change.

```python
from sklearn.datasets import make_classification
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE, SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

feature_names = [
    "visit_count",
    "avg_order",
    "discount_click",
    "support_calls",
    "days_since_login",
    "newsletter_open",
]

X, y = make_classification(
    n_samples=180,
    n_features=6,
    n_informative=3,
    n_redundant=1,
    class_sep=1.1,
    random_state=7,
    shuffle=False,
)

filter_selector = SelectKBest(score_func=f_classif, k=3).fit(X, y)
filter_features = [
    name for name, keep in zip(feature_names, filter_selector.get_support()) if keep
]

base_model = LogisticRegression(max_iter=1000)
rfe_selector = RFE(base_model, n_features_to_select=3).fit(
    StandardScaler().fit_transform(X),
    y,
)
rfe_features = [
    name for name, keep in zip(feature_names, rfe_selector.support_) if keep
]

models = {
    "filter_selected": X[:, filter_selector.get_support()],
    "rfe_selected": X[:, rfe_selector.support_],
}

print("filter keeps:", filter_features)
print("rfe keeps   :", rfe_features)
print("pca output  :", ["component_1", "component_2", "component_3"])

for name, selected_X in models.items():
    score = cross_val_score(base_model, selected_X, y, cv=5).mean()
    print(name, "cv=", round(score, 3), "shape=", selected_X.shape)

pca_score = cross_val_score(
    make_pipeline(StandardScaler(), PCA(n_components=3), base_model),
    X,
    y,
    cv=5,
).mean()
print("pca_reduced cv=", round(pca_score, 3), "shape=", (X.shape[0], 3))
```

The output is as follows.

```text
filter keeps: ['visit_count', 'discount_click', 'support_calls']
rfe keeps   : ['visit_count', 'avg_order', 'support_calls']
pca output  : ['component_1', 'component_2', 'component_3']
filter_selected cv= 0.817 shape= (180, 3)
rfe_selected cv= 0.828 shape= (180, 3)
pca_reduced cv= 0.617 shape= (180, 3)
```

The first thing to read here is not the score ranking. The filter method and RFE retained different original feature lists, while PCA reduced the input to the same three columns but removed the original column names. So `reduced to three` is not enough. Readers also need to tell whether it was feature selection that preserved original features or dimensionality reduction that compressed them into a new representation.

## Checklist

- Have you distinguished whether the current task is choosing original columns or rebuilding them as new axes?
- Are you speaking of quick first-pass reduction and model-based repeated comparison as if they were the same method?
- Can you explain why feature selection can be better than dimensionality reduction when interpretability matters?
- Can you understand statistical-test-based feature selection usually as a filter approach, and RFE as a wrapper approach that repeatedly trains a model while reducing features?
- Can you explain that dimensionality reduction may look similar to feature selection but is a separate problem that re-expresses the original features into new axes?
- Can you distinguish filter, wrapper, embedded, and dimensionality reduction without mixing them as if they were solutions of the same kind?

## Sources And References

- scikit-learn developers, [Feature selection](https://scikit-learn.org/stable/modules/feature_selection.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-26.
- scikit-learn developers, [Unsupervised dimensionality reduction](https://scikit-learn.org/stable/modules/unsupervised_reduction.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-26.
- Trevor Hastie, Robert Tibshirani, Jerome Friedman, [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-26.
