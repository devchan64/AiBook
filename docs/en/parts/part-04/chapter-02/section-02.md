# P4-2.2 Unsupervised Learning

> Section ID: `P4-2.2`
> Version: `v2026.07.11`

P4-2.1 looked at supervised learning, where a model is trained using examples that already have labels. This time we look at unsupervised learning, which looks for structure in data without labels.

Unsupervised learning does not mean `it learns freely without answers` in some vague way. It means an approach that looks for similarity, grouping, axes, density, or unusual points inside data without labels attached beforehand by people. In many cases, the model is not trying to match an answer. It is building structure candidates so that people can understand the data better or prepare the next task.

This Section explains the broad distinction among `unsupervised learning`, `reading structure without labels`, `clustering`, and `dimensionality reduction`. Later Sections continue the current context with this handle, and the basic meaning of structure exploration is connected again through this Section and the [concept glossary](../../../reference/concept-glossary.md).

## Scope Of This Section

This Section explains the basic intuition of unsupervised learning. It does not go deeply into the formulas or implementation of individual algorithms such as k-means, PCA, t-SNE, or DBSCAN. k-means and DBSCAN return in P4-17 on clustering, while PCA and t-SNE return in P4-18 on dimensionality reduction.

- What does it mean that labels are absent?
- What does unsupervised learning learn?
- What kinds of problems are clustering, dimensionality reduction, and outlier detection?
- Why must the results of unsupervised learning be interpreted carefully?
- How can supervised and unsupervised learning connect in real work?

## Goals Of This Section

- You can explain unsupervised learning as an approach that finds structure in unlabeled data.
- You can distinguish clustering, dimensionality reduction, and outlier detection through examples.
- You can explain why `similar data are grouped together` does not automatically guarantee a meaningful correct answer.
- You can understand that people still need to interpret and review the result of unsupervised learning.
- You can explain that unsupervised learning can be used as preparation for later supervised learning or data analysis.

## Understanding It First Through One Scene

Think about customer data from an online shopping mall. Suppose you have information like the following, but there is not yet any label such as `good customer`, `churn risk`, or `regular customer`.

| Customer | Visits in the last 30 days | Purchase count | Average purchase amount | Coupon use |
| --- | ---: | ---: | ---: | --- |
| Customer A | 20 | 8 | high | frequent |
| Customer B | 3 | 0 | low | almost never |
| Customer C | 18 | 7 | high | frequent |
| Customer D | 5 | 1 | medium | occasional |

In supervised learning, each customer might already have a label such as `good customer`, `churn risk`, or `general customer`. In unsupervised learning, you start without such labels. Instead, you inspect whether similar customers group together naturally, what axes create differences, or whether there are unusually different customers.

The important point here is that the model does not automatically understand the meaning of customer types. It can find similar patterns. But whether that group means `high-value customers`, `coupon-sensitive customers`, or `temporary event participants` must be interpreted by people using the data and the business context.

Even with the same customer table, unsupervised learning treats it not as `a table for matching answer labels`, but as `a table for reading structure candidates`. The following diagram shows how the same input table can split into cluster candidates, an axis summary, and an outlier candidate.

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-2-mermaid-01-en.mmd"
```

## Comparing It With Supervised Learning

Supervised and unsupervised learning look different from the shape of the data onward.

| Category | Supervised learning | Unsupervised learning |
| --- | --- | --- |
| Data | Input `X` and label `y` exist together | Only input `X` exists, without explicit label `y` |
| Question | What is the correct output for this input? | What structure exists inside these data? |
| Representative problems | classification, regression | clustering, dimensionality reduction, outlier detection |
| Result interpretation | It is easier to evaluate performance against actual labels | People must interpret and validate the meaning of the result |
| Example | Predict whether an email is spam or normal | Group similar kinds of email together |

Because there are no labels in unsupervised learning, it is hard to say simply `it was correct by this percentage` by comparing against an answer. Instead, you need to ask whether the grouping is meaningful for the business, whether the visualization helps understanding, and whether an outlier candidate is actually worth checking.

## Looking At It As A Flow

The basic flow of unsupervised learning can be seen as follows.

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-2-mermaid-02-en.mmd"
```

The key in this diagram is `human interpretation`. The result of unsupervised learning is a structure candidate inside the data. The grouping or axis produced by the model must still be named by people and checked for actual usefulness.

## Three Problems Often Met In Unsupervised Learning

Unsupervised learning is used in many ways. The first important step is to distinguish the following three problem types.

| Problem | Question | Easy example |
| --- | --- | --- |
| clustering | Do similar cases group together? | Group customers with similar purchase patterns |
| dimensionality reduction | Can many features be summarized into fewer axes? | Reduce 100 features into a 2D plot |
| outlier detection | Are there cases that are unusually different? | Find unusual payment patterns as review candidates |

The unsupervised-learning documentation in scikit-learn also covers several categories such as clustering, manifold learning, matrix factorization, outlier detection, and density estimation. This Section centers on clustering, dimensionality reduction, and outlier detection.

## Clustering: Grouping Similar Things

Clustering is an approach that groups unlabeled data into similar cases.

If you look at customer data through visit count and purchase count, you may see groups like the following.

| Candidate group | Pattern visible in the data | Interpretation a person may attach |
| --- | --- | --- |
| Group A | many visits and many purchases | active customers |
| Group B | many visits but few purchases | browsing customers or price-comparison customers |
| Group C | few visits and few purchases | dormant-customer candidates |

But these names are not told by the model. They are interpretations attached by a person after looking at the data. A clustering result is a starting point that says `a grouping like this is visible`, not an immediate conclusion that `this customer must be this type of person`.

Google's clustering explanation also describes clustering as grouping unlabeled examples according to similarity. In actual use, you must make clear what similarity criterion is being used, and comparison becomes more complicated as the number of features grows.

The point to be especially careful about is not to misunderstand `a cluster ID was assigned` as `the correct answer label now exists`.

| What is visible | What it means | What it is not yet |
| --- | --- | --- |
| Cluster 0, Cluster 1, Cluster 2 | A temporary grouping of similar cases made by the model | A confirmed real-world customer-type label |
| Points that look close in a 2D plot | They look close inside a particular representation space | They do not automatically share the same cause or business group |
| Outlier candidate | A signal that a case looks different from most others | An immediate confirmed error or risk judgment |

In other words, the output of unsupervised learning is closer to `structure candidate` than to `answer`. Once that point is accepted first, later clustering or dimensionality-reduction results are less likely to be exaggerated.

## Dimensionality Reduction: Drawing What Looks Large In A Smaller View

Dimensionality reduction is an approach that reduces many features into a smaller number of axes.

For example, if 50 features describe one customer, it is hard for a person to inspect them all at once. Dimensionality reduction can compress that information into 2 or 3 axes so that it becomes easier to visualize or to see the main directions of change.

Dimensionality reduction can be an operation that throws away some information. So if two points look close in a 2D plot, that alone is not enough to conclude they must mean the same thing in the original data as well. You still need to check what information was preserved and what was reduced away.

## Outlier Detection: Reading Different Points As Review Candidates

Outlier detection is an approach that finds data that look different from most other cases.

For example, in a payment service, a payment that appears at an unusual time, with an unusual amount, or from an unusual region can become an outlier candidate. But an outlier does not automatically mean fraud. It may be a purchase made while traveling or a legitimate high-value purchase.

So the result of unsupervised learning usually needs to be read as `a review candidate`. You inspect why the model marked it as unusual, then judge it by combining that signal with actual business criteria.

## Points To Be Careful About In Interpretation

Because unsupervised learning has no labels, interpretation becomes especially important.

- A grouping made by the model is not automatically a meaningful real-world group.
- Points that are close are not always close for the same cause.
- A dimensionality-reduction plot may not preserve all information from the original data.
- An outlier candidate may differ from an actual error, risk, or fraudulent case.
- The moment a result is given a name, human interpretation has entered.

So unsupervised learning should be read as `we found a candidate structure for understanding the data`, not `we found the correct answer`.

## Places Where It Can Connect To Supervised Learning

Unsupervised learning is not a world completely separate from supervised learning. In real work, the two can connect.

For example, after clustering customers, you can analyze the behavior of each group and set different marketing strategies. Or you can use a cluster ID as a new feature and feed it into a supervised model. After reducing dimensions for visualization, you can inspect whether label errors exist.

The caution is the same even then. The result of unsupervised learning can become material for the next task, but it does not guarantee the correct answer about reality by itself.

The result of unsupervised learning should be interpreted in the following order.

1. First look at what groupings or axes are visible in the data.
2. Then look at what interpretation a person can attach to those groupings.
3. Only after that decide whether to use them for the next analysis or for supervised-learning preparation.

If you pass through this order, you are less likely to freeze an unsupervised-learning result into a `correct answer` too quickly.

In practice, you often need to judge first whether `the current problem should be read through unsupervised learning`.

| Current state | Read it as unsupervised learning? | Why |
| --- | --- | --- |
| You want to inspect groups, axes, or unusual points before any labels exist | yes | Because understanding structure matters more than predicting an answer right now |
| There are no labels yet, but you need candidate structure for the next analysis | yes | Because clusters, axes, and outlier candidates can become material for the next step |
| Stable labels already exist and you want to match outputs for new cases | usually no | Because a supervised-learning problem is more direct than structure exploration |

## Perspective To Remember In This Section

- Unsupervised learning is an approach for finding structure candidates in unlabeled data.
- Clustering groups similar cases, dimensionality reduction compresses many features into fewer axes, and outlier detection finds unusually different cases as review candidates.
- The result of unsupervised learning still needs human interpretation.
- Because labels do not exist, it is difficult to evaluate it directly against correct answers the way supervised learning can.
- Unsupervised learning can be used for data understanding, visualization, review-candidate discovery, and preparation for later supervised learning.

## Short Check

- Can you explain when the goal of unsupervised learning is not `matching the correct answer` but `building structure candidates`?
- Can you explain why a cluster ID, closeness in a 2D plot, or an outlier candidate is not immediately a correct answer label?
- Can you explain how the result of unsupervised learning can be connected to the next analysis or supervised-learning preparation?

## Cases And Examples

### Case 1. When Customer-Type Names Do Not Exist Yet, But You Want To See Whether Similar Patterns Appear First

Suppose a shopping mall has collected a lot of customer-behavior data, but labels such as `loyal customer`, `churn-risk customer`, or `discount-sensitive customer` still do not exist. Even so, people naturally want to see first whether some grouping already appears inside the data.

In this scene, the problem is not to match correct labels the way supervised learning does. Instead, the first step is to look only at values such as visit count, purchase amount, and coupon use and inspect whether similar customers group together or whether unusually different customers exist.

That is why unsupervised learning is explained as `an approach that finds structure candidates in unlabeled data`. The model does not tell you the name `this group is VIP` by itself. It first exposes patterns to which people may later attach interpretations.

The checkable result can be judged by whether the groupings and axes actually create a review question. For example, if customers with similar purchase patterns separate into several groups and a person can explain the differences among them, then the result of unsupervised learning becomes a useful starting point for the next analysis step.

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-2-mermaid-03-en.mmd"
```

## When This Perspective Should Come To Mind First

- Recall the unsupervised-learning perspective first when labels do not exist yet and structure candidates must be found before anything else.
- Return to this Section when checking whether a cluster ID, 2D closeness, or an outlier candidate is being read too quickly as if it were already the answer.
- This Section becomes the reference point when reorganizing how an unsupervised-learning result will connect to the next analysis or to supervised-learning preparation.

## Sources And References

- scikit-learn developers, `Unsupervised learning`, scikit-learn User Guide, accessed 2026-06-25. [https://scikit-learn.org/stable/unsupervised_learning.html](https://scikit-learn.org/stable/unsupervised_learning.html){: target="_blank" rel="noopener noreferrer" }
- Google for Developers, `What is clustering?`, Machine Learning, accessed 2026-06-25. [https://developers.google.com/machine-learning/clustering/overview](https://developers.google.com/machine-learning/clustering/overview){: target="_blank" rel="noopener noreferrer" }
