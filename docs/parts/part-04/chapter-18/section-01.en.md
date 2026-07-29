# P4-18.1 Dimensionality Reduction

> Section ID: `P4-18.1`
> Version: `v2026.07.26`

In P4-17, [clustering](/AiBook/en/reference/concept-glossary-alpha/c/#clustering) asked `what hidden groups are present?` Here, we hold a different question.

If there are too many [features](/AiBook/en/reference/concept-glossary-alpha/f/#feature) to read the structure easily, can we rebuild the representation itself with fewer axes?

That question is the starting point of [dimensionality reduction](/AiBook/en/reference/concept-glossary-alpha/d/#dimensionality-reduction). Dimensionality reduction is not just a technique for discarding many features. It is closer to `reexpressing the original representation through axes that are easier to read when the original representation has become too complex`.

This Section explains [dimension](/AiBook/en/reference/concept-glossary-alpha/d/#dimension), [PCA](/AiBook/en/reference/concept-glossary-alpha/p/#principal-component-analysis-pca) (principal component analysis), and `why [eigenvalues](/AiBook/en/reference/concept-glossary-alpha/e/#eigenvalue) and [eigenvectors](/AiBook/en/reference/concept-glossary-alpha/e/#eigenvector) appear here` through the same toy-data scene. In the next Section, P4-18.2, we continue by asking how far we should trust the resulting picture and how to read information loss.

## Questions Closed By Dimensionality Reduction

This Section answers the following questions.

- What does dimension mean in machine learning?
- Why can learning and interpretation become harder when the number of features grows?
- What problems is dimensionality reduction trying to ease?
- What representative intuition does PCA show?
- Why do [variance](/AiBook/en/reference/concept-glossary-alpha/v/#variance), [orthogonal](/AiBook/en/reference/concept-glossary-alpha/o/#orthogonal), eigenvalue, and eigenvector appear together in PCA explanations?
- How should we distinguish [kernel PCA](/AiBook/en/reference/concept-glossary-alpha/k/#kernel-pca) and [Truncated SVD](/AiBook/en/reference/concept-glossary-alpha/t/#truncated-svd) from PCA at the level of intuition?

This Section focuses on grasping, at an introductory level, `why we want to reduce dimensions` and `what kind of calculation PCA performs`. How to interpret visualization results, t-SNE and UMAP, [reconstruction error](/AiBook/en/reference/concept-glossary-alpha/r/#reconstruction-error), and trustworthiness continue in the next Section, P4-18.2.

## Judgments To Keep From Dimensionality Reduction

- You can explain dimensionality reduction as `reexpressing feature space through fewer axes`.
- You can explain PCA as `a method that resets new axes in the directions where data vary strongly`.
- You can explain why the first component and second component should be orthogonal to one another.
- You can read eigenvectors as directions of new axes and eigenvalues as the amount of variation explained by those axes.

## Why This Section Is Needed

As you keep studying machine learning, the number of features keeps growing.

- Customer data can contain dozens of numerical indicators.
- Document data can contain thousands of word features.
- Image data creates as many features as there are pixels.

At that point, readers easily feel the following.

- If there are more features, shouldn't the description become more detailed?
- Then why does understanding become harder instead?

That is exactly where dimensionality reduction becomes necessary. As the number of features grows, there may be more information, but humans find it harder to hold the structure at once. So dimensionality reduction first checks `is this representation too complex right now?`, then creates axes for reading the large flow again.

## Looking At One Scene

This Section keeps returning to a small dataset where two features move almost together.

| Sample | Monthly visits `x1` | Average purchase amount `x2` |
| --- | ---: | ---: |
| A | 2.0 | 2.1 |
| B | 3.0 | 3.2 |
| C | 4.0 | 3.9 |
| D | 5.0 | 5.1 |

This table has a flow where `customers with more visits also tend to have higher average purchase amounts`. There are only two axes, so we can still read it by eye, but the core reason PCA becomes useful already appears here.

1. The two features move almost in the same direction.
2. Then a single new axis may be enough to summarize the large flow.
3. But small differences where the two axes do not perfectly match may become weaker.

In other words, dimensionality reduction is not `squeezing a complicated table into a few axes`. It is `deciding what to treat as the large flow and what to leave as fine detail`.

## What Does Dimension Mean?

In machine learning, dimension usually connects to the number of axes used to describe one data sample, in other words, the number of features.

In the table above, one customer is represented with two values, `monthly visit count` and `average purchase amount`, so the data are two-dimensional. If we add `days since last login`, it becomes three-dimensional. If we add `return rate`, it becomes four-dimensional.

If we draw this very simply, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-01-en.mmd"
```

For now, it is enough to hold dimension less as a mathematical symbol and more as `the number of coordinate axes through which the data are viewed`. Whenever one feature is added, one more axis for describing the data is added.

## Why Does It Become Harder When Features Increase?

Having many features can increase expressive power, but at the same time it creates three kinds of difficulty.

1. It becomes harder for people to imagine the structure.
2. Computational cost can increase.
3. There may be a lot of unnecessary or overlapping information.

For example, the following values may not be fully independent.

- Monthly purchase amount
- Yearly purchase amount
- Number of purchases
- Average order amount

Here, the problem is less `there are many features` and more `how much genuinely new information is present?` If many features move almost in the same direction, the original table may be long while the main flows to read are few.

So dimensionality reduction becomes a step that asks again `has the current representation become unnecessarily bulky?`

## What Is Dimensionality Reduction Trying To Ease?

The scikit-learn user guide explains PCA as a method that decomposes a multivariate dataset into successive orthogonal [components](/AiBook/en/reference/concept-glossary-alpha/c/#component) and finds directions that explain the largest amount of variance.

At an introductory level, dimensionality reduction can be read as an attempt to ease the following problems.

| Difficulty | What help dimensionality reduction tries to provide |
| --- | --- |
| There are too many features to inspect structure easily | Summarize through fewer axes |
| Features overlap with each other | Group overlapping variation into a few components |
| Visualization is hard | Lower it to 2D or 3D and look at the rough structure |
| Computation is heavy | Change it into a smaller representation so downstream models are easier to handle |

So dimensionality reduction is better understood as `a tool for building a more readable representation` than as `something that completely replaces the original data`.

## How Does PCA Reexpress This Scene?

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-02-en.mmd"
```

PCA tries to reset new axes in `the directions where the data are actually spread out a lot`. In the toy data above, `x1` and `x2` grow almost together, so one diagonal direction looks more important than reading the two axes separately.

## What Representative Intuition Does PCA Show?

The scikit-learn documentation explains PCA as a method for finding `successive orthogonal components that explain the most variance`.

`Take the direction in which the data spread the most as the first axis, then among the directions orthogonal to it, take the next direction with a large spread as the second axis.`

PCA is closer to the sense of not using the original axes such as x, y, and z as they are, but instead rotating the axes again toward the directions in which the data actually vary a lot.

## A Simpler Analogy For PCA

Imagine many points spread in the shape of a tilted ellipse.

- If they are viewed with the original x-axis and y-axis, the spread is divided awkwardly.
- But if the long direction of the ellipse is taken as new axis 1, the large flow of data variation becomes easier to see.
- If the short direction of the ellipse is taken as new axis 2, smaller fluctuations can be separated out.

PCA is an attempt to find `a coordinate system that matches the data flow better than the original one`.

If this is compressed into a small diagram, it looks like the following.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-03-en.mmd"
```

This diagram helps the reader interpret PCA as `a process of rotating the axes again in the directions where the data actually spread a lot`. Once axes better aligned with the data flow are found, the first component can explain the major variation more efficiently than the original coordinate axes.

## Why Look At Variance?

As seen earlier in Part 2 and early Part 3, variance is a basic way of feeling how widely values are spread. PCA tries to capture first the major direction of that spread.

- Direction with large variance: a direction where the data vary a lot
- Direction with small variance: a direction that may hold relatively less important fluctuation

Of course, small variance does not always mean no meaning. But when reducing dimensions, the question usually becomes `can the large variation be preserved first while the smaller variation is discarded later?`

In summary, PCA chooses its summarization priority based on `what changes more strongly`.

If the priority is stated more briefly, PCA does not preserve all variation at once. It keeps first the component that explains the largest overall variation. Then the next component explains the remaining variation in a direction that does not overlap with the previous one.

## Why Does The Word Orthogonal Appear?

The scikit-learn documentation describes PCA components as orthogonal components. Here, orthogonal can be understood as meaning the new axes are chosen so they do not overlap with one another, in other words, so repeated explanation is reduced.

Put briefly:

`The idea is that the second component should not simply explain again the same variation already explained by the first component.`

So PCA creates new axes while trying to separate information across different directions.

## Why Do Eigenvalue And Eigenvector Appear In PCA?

The moment you look just a little deeper into PCA, the words eigenvalue and eigenvector of the [covariance matrix](/AiBook/en/reference/concept-glossary-alpha/c/#covariance-matrix) appear immediately. The reason is simple.

`To find the directions in which the data spread most strongly in formulas, you need to find the direction vectors that best explain that spread.`

At an introductory level, the following flow is enough.

1. Center the data around the mean
2. Build a covariance matrix that captures how much the axes move together
3. Find the directions that `explain the most variance` in that matrix
4. Read those directions as eigenvectors, and the size of variance along them as eigenvalues

The formula is usually written like this.

\[ \Sigma v = \lambda v \]

Here:

- \(\Sigma\): covariance matrix
- \(v\): direction vector, or candidate new axis
- \(\lambda\): the amount of variance along that direction

If this equation is read in words, it becomes the following.

- When the data are viewed along some direction \(v\)
- if the covariance structure stretches that direction again in the same direction
- then that direction becomes a candidate axis for explaining the spread of the data

So in PCA, the eigenvector can be read as `the direction of a new axis`, and the eigenvalue as `how much variation that new axis explains`.

| What we want to see in PCA | Mathematical counterpart |
| --- | --- |
| The most important new axis first | The eigenvector corresponding to the largest eigenvalue |
| The next most important new axis | The eigenvector corresponding to the next largest eigenvalue |
| How much information each axis explains | The size of each eigenvalue |

Even without following the full derivation, it is important to secure the connection `why does the eigenvector become the axis and the eigenvalue become the explained variance` here. Otherwise PCA stops as only a rotation metaphor instead of becoming `a calculation for finding directions that explain variance best`.

## How Are kernel PCA And Truncated SVD Different?

PCA is not the only standard in dimensionality reduction. Even inside the same flow of `rebuilding the representation`, different names appear depending on what someone wants to handle better.

| Method | Introductory core to hold | When it comes up more naturally |
| --- | --- | --- |
| PCA | Rebuild linear axes and keep directions with large variance | When you want to summarize the large overall variation in numerical features |
| kernel PCA | Try to see structure that is not easy to read linearly in the original space by using a kernel space | When you want to unfold curved or nonlinear structure better |
| Truncated SVD | Keep only a few major components through matrix factorization | When handling sparse matrices or text-word matrices |

If the difference is written very briefly, it looks like this.

- PCA: `look again through straight-line axes`
- kernel PCA: `try to unfold nonlinear structure as well`
- Truncated SVD: `keep only a few important components in a large matrix`

Mathematically, they also look at slightly different objects.

| Comparison item | PCA | kernel PCA | Truncated SVD |
| --- | --- | --- | --- |
| Basic starting point | Covariance structure | Similarity structure built by kernels | Factorization of the original data matrix itself |
| What it fits well | Linear reexpression | Nonlinear reexpression | Low-rank approximation of a large matrix |
| The difference a beginner should remember first | `Rotate axes and capture large variance` | `View structure that is hard to see with straight axes inside another space` | `Compress a matrix into a few components` |

In other words, kernel PCA and Truncated SVD are not just minor variations of PCA. They are branches that differ slightly in `what they regard as the central structure of the data`. In this Section, instead of memorizing names, it is better to distinguish them through the three feelings `linear-axis reexpression`, `unfolding nonlinear structure`, and `matrix compression`.

## What Improves And What Disappears When Dimensions Are Reduced?

Dimensionality reduction always creates a trade-off.

| What is gained | What can be lost |
| --- | --- |
| A simpler representation | Per-feature detail from the original data |
| Easier visualization | Some fine differences |
| Faster computation | Directness of interpretation |
| Compressed overlapping information | Business meaning tied to one specific axis |

So after seeing a reduced representation, the question should always be:

`Is this simpler representation sufficient for the problem I am trying to inspect?`

That question matters because dimensionality reduction always changes the expression first, then asks whether the changed expression is still enough for the actual task.

Sometimes the simplified axes are sufficient for seeing the large flow.

Sometimes an important per-feature distinction becomes weaker during compression.

So dimensionality reduction is convenient, but it is not free.

What matters is not only `did the picture become easier to read?`

It is also `did any difference important for the current problem disappear while the picture became easier to read?`

## Cases And Examples

### Case 1. When There Are Dozens Of Customer Indicators And You Want To Reduce Them To A Few Axes First

Suppose a business team has many customer indicators at once, such as visit count, purchase amount, recent activity, session time, category diversity, and discount response. Looking at the full table directly makes it hard to grasp the large flow. In that case, dimensionality reduction can compress the information into a few components such as `activity-like axis`, `spend-size axis`, or `recency-like axis`, and make it easier to inspect the structure again. The important point here is not that the original features become unnecessary, but that `a new representation is first built to make the broad structure readable`.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-05-en.mmd"
```

This case can be compressed into a review memo like this.

| What you want to summarize first | What not to decide immediately | What to check next |
| --- | --- | --- |
| Whether customer behavior can be re-read through a few broad axes | Do not assume that one compressed axis directly matches one business meaning | Check which original features contribute strongly to that axis |
| Whether the large flow is visible before downstream clustering or modeling | Do not treat the reduced representation as a complete replacement of the original table | Compare with the original features and inspect information loss |

## Practice And Example

This exercise keeps using the same four samples from above and turns them into a small hands-on check of `what remains and what disappears when 2D data are reduced to 1D with actual PCA`.

- Problem situation: when two features move almost together, check whether the large flow is still preserved even if only one principal component remains
- Input: two features, visit count and average purchase amount
- Expected output: 1D principal-component scores, explained variance ratio, restored values
- Concepts to check: PCA can project the original features onto one new axis, and even if only one component remains, large variation can be preserved while restored values do not have to be exactly the same as the original

```python
# This example reduces 2D features to one PCA component and restores them to see what remains.
import numpy as np
from sklearn.decomposition import PCA

sample_ids = np.array(["A", "B", "C", "D"])
X = np.array([
    [2.0, 2.1],
    [3.0, 3.2],
    [4.0, 3.9],
    [5.0, 5.1],
])

pca = PCA(n_components=1)
X_reduced = pca.fit_transform(X)
X_restored = pca.inverse_transform(X_reduced)

print("principal axis:", np.round(pca.components_, 3))
print("explained variance ratio:", np.round(pca.explained_variance_ratio_, 3))

for idx, reduced, restored in zip(sample_ids, X_reduced, X_restored):
    print(
        idx,
        "reduced =", np.round(reduced, 3),
        "restored =", np.round(restored, 3),
    )
```

The execution result is as follows.

```text
principal axis: [[0.707 0.707]]
explained variance ratio: [0.996]
A reduced = [-2.112] restored = [2.007 2.086]
B reduced = [-0.662] restored = [3.032 3.111]
C reduced = [0.52] restored = [3.868 3.947]
D reduced = [2.254] restored = [5.093 5.172]
```

What matters in this result is the following.

1. Since `principal axis` is almost `[0.707, 0.707]`, the direction where the two features move together with similar weight is captured as the first principal component.
2. Since `explained variance ratio` is `0.996`, one component alone preserves most of the total variation.
3. The `restored` values are very close to the originals but not completely identical, which shows that dimension reduction can preserve the large flow while still losing some fine detail.

### Change One Value: If They Stop Moving Together, Reconstruction Error Grows

This time, deliberately lower only the second feature of the last sample, so the two features no longer move in the same flow.

```python
# This example adds a sample whose two features do not move together to see how PCA reconstruction error grows.
import numpy as np
from sklearn.decomposition import PCA

sample_ids = np.array(["A", "B", "C", "D"])
X = np.array([
    [2.0, 2.1],
    [3.0, 3.2],
    [4.0, 3.9],
    [5.0, 2.5],
])

pca = PCA(n_components=1)
X_reduced = pca.fit_transform(X)
X_restored = pca.inverse_transform(X_reduced)

row_errors = np.sum((X - X_restored) ** 2, axis=1)

print("principal axis:", np.round(pca.components_, 3))
print("explained variance ratio:", np.round(pca.explained_variance_ratio_, 3))

for idx, reduced, restored, err in zip(sample_ids, X_reduced, X_restored, row_errors):
    print(
        idx,
        "reduced =", np.round(reduced, 3),
        "restored =", np.round(restored, 3),
        "row_error =", round(float(err), 3),
    )
```

```text
principal axis: [[0.894 0.449]]
explained variance ratio: [0.904]
A reduced = [-1.937] restored = [2.075 1.959] row_error = 0.027
B reduced = [-0.555] restored = [3.311 2.578] row_error = 0.413
C reduced = [0.54] restored = [4.29  3.067] row_error = 0.736
D reduced = [1.952] restored = [5.554 3.698] row_error = 1.727
```

This time, D has the largest `row_error`. In other words, one principal component alone cannot restore D's crossed pattern well. This scene shows directly through a Python example that `dimensionality reduction can preserve the large flow, but it does not preserve every sample's fine detail equally well`.

## Checklist

- Can you explain that dimension is connected to the number of axes that describe the data, in other words the number of features?
- Is what you need right now closer to rebuilding the representation than to finding groups?
- Can you explain dimensionality reduction as something closer to `rebuilding the representation` than to `deleting features`?
- Can you explain that the first component captures the large flow and the second component captures the remaining difference?
- Can you connect eigenvectors to `the direction of a new axis` and eigenvalues to `how much variation that axis explains`?
- Do you understand that reducing dimensions makes the representation easier to read, but some fine differences can become weaker?
- Even if the reduced representation looks convenient, are you prepared to go back and check whether important differences disappeared from the original features?

## Sources And References

- scikit-learn developers, `2.5. Decomposing signals in components (matrix factorization problems)`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/decomposition.html](https://scikit-learn.org/stable/modules/decomposition.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `PCA`, scikit-learn API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html){: target="_blank" rel="noopener noreferrer" }
