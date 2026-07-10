# P4-7.4 Supplementary Learning: How To First Distinguish Filter, Wrapper, And Dimensionality Reduction

> Section ID: `P4-7.4`
> Version: `v2026.07.10`

From P4-7.1 to P4-7.3, the discussion chose features, separated input-representation problems, and established the basic judgment for preprocessing. In practice, however, the reader soon meets names such as the following.

- statistical-test-based feature selection
- recursive feature elimination (RFE)
- dimensionality reduction

All of these can look similar in that they `reduce the input or represent it again`, but they differ in what criterion is used to reduce and in what is left behind.

## Scope Of This Supplementary Learning

This Section answers the following questions.

- What is different among filter, wrapper, and embedded feature selection?
- On what idea does statistical-test-based feature selection operate?
- What does recursive feature elimination (RFE) repeat?
- How is dimensionality reduction different from feature selection?

This Section does not treat the following topics deeply.

- derivation of formulas for individual statistical tests
- the calculation procedures of PCA, t-SNE, and UMAP
- large-scale automated feature-selection systems

The intuition and limits of individual dimensionality-reduction algorithms are revisited in P4-18.1 and P4-18.2.

## Goals Of This Supplementary Learning

- You can distinguish feature selection and dimensionality reduction without mixing them as the same task.
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
flowchart TD
  A["customer behavior columns"]
  B["quick first pass"]
  C["model-based repeat check"]
  D["new compressed axes"]
  E["filter keeps original columns"]
  F["wrapper or RFE keeps best subset"]
  G["dimensionality reduction rewrites representation"]

  A --> B --> E
  A --> C --> F
  A --> D --> G
```

The distinction needed here is the following. The filter approach is closer to quickly inspecting the original features and reducing first-round candidates, while RFE, which is a wrapper approach, repeatedly reduces features based on current model performance. Dimensionality reduction is closer not to choosing some of the original columns, but to mixing several features and re-expressing them as new axes.

The confirmable results must also be read differently. With filter and RFE, readers can view a list of which original columns remained, but dimensionality reduction changes the data into new axes such as `component_1` and `component_2`, so the interpretation method itself changes. So even when the same phrase `reduce input` is used, readers must first decide whether they want to preserve interpretability or compress into a new representation.

## Perspective To Remember In This Section

- Statistical-test-based feature selection is usually understood as a filter approach.
- RFE is understood as a wrapper approach that reduces features while repeatedly training a model.
- Dimensionality reduction looks similar to feature selection, but it is a separate problem that re-expresses the original features into new axes.

## Short Check

- Have you distinguished whether the current task is choosing original columns or rebuilding them as new axes?
- Are you speaking of quick first-pass reduction and model-based repeated comparison as if they were the same method?
- Can you explain why feature selection can be better than dimensionality reduction when interpretability matters?

## When Should This Perspective Come To Mind First

- Bring up this Section first when readers need to distinguish choosing original columns from re-expressing them as new axes.
- Return to this Section when checking whether filter, wrapper, embedded, and dimensionality reduction are being mixed together as if they were the same kind of solution.
- This Section becomes the standard when organizing which method should be used first while considering interpretability and computational cost together.

## Sources And References

- scikit-learn developers, [Feature selection](https://scikit-learn.org/stable/modules/feature_selection.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-01.
- scikit-learn developers, [Unsupervised dimensionality reduction](https://scikit-learn.org/stable/modules/unsupervised_reduction.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-01.
- Trevor Hastie, Robert Tibshirani, Jerome Friedman, [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-01.
