# P4-18.1 Dimensionality Reduction

> Section ID: `P4-18.1`
> Version: `v2026.07.11`

In P4-17, we looked at the viewpoint of finding data structure without labels through clustering. Within the same unsupervised-learning flow, another question appears here.

When there are too many features, can we reduce that information into fewer axes and still look at it?

That question is the starting point of dimensionality reduction.

Dimensionality reduction is a method that changes many features into a smaller number of axes or components so that the structure becomes simpler to inspect and the computation becomes easier to handle.

Dimensionality reduction is both `removing some information` and `making structure easier to see`.

This Section explains the basic meaning of `dimensionality reduction`, `dimension`, and `PCA (principal component analysis)`. In the next Section, we continue the current line of judgment from this handle, and the basic sense of reexpressing many features through fewer axes reconnects through this Section and the [concept glossary](../../../reference/concept-glossary.md).

## Scope Of This Section

This Section answers the following questions.

- What does dimension mean in machine learning?
- Why can learning and interpretation become harder when the number of features grows?
- What problems is dimensionality reduction trying to ease?
- What representative intuition does PCA show?
- What does dimensionality reduction preserve, and what does it discard?
- Why do eigenvalue and eigenvector appear in PCA?
- How are kernel PCA and Truncated SVD different from PCA?

This Section focuses on grasping, at an introductory level, `why we want to reduce dimensions` and `how to read PCA first through intuition and a minimum amount of mathematics`. So this Section directly covers why PCA's new axes are read as eigenvectors and how PCA, kernel PCA, and Truncated SVD split into different branches. By contrast, visualization-oriented methods and interpretation of reconstruction error are closed in the next Section, P4-18.2.

## Goals Of This Section

- You can explain dimensionality reduction as `reexpressing feature space through fewer axes`.
- You can describe why interpretation and computation become harder when there are many features.
- You can explain PCA at an introductory level as `a method for finding orthogonal axes that explain a large amount of variance`.
- You can understand that dimensionality reduction brings both convenience and information loss.

## Why This Section Is Needed

As you keep studying machine learning, the number of features keeps growing.

- Customer data can contain dozens of numerical indicators.
- Document data can contain thousands of word features.
- Image data creates as many features as there are pixels.

At that point, readers easily feel the following.

- If there are more features, shouldn't the description become more detailed?
- Then why does understanding become harder instead?

That is exactly where dimensionality reduction becomes necessary.

So P4-18.1 is the Section for learning `why simplification becomes necessary again as information increases`.

If we place it beside the clustering from the previous Chapter, the first thing that should appear is that even inside unsupervised learning, the central questions differ.

| Question | Clustering | Dimensionality reduction |
| --- | --- | --- |
| What is asked first | What groups are hidden? | Through what axes can this be reexpressed more clearly? |
| What is wanted immediately | Cluster structure, outlier candidates | Fewer components, a more readable representation |
| What is often done next | Interpret cluster meaning, review segments | Visualization, noise reduction, cleanup for downstream model input |

If clustering is closer to `finding groups`, dimensionality reduction is closer to `rebuilding the representation`. That distinction must be visible first so that PCA is read not as just another algorithm name, but as a representative answer to the question `how can high-dimensional representation be changed into easier axes for reading?`

### When Should Dimensionality Reduction Come To Mind First?

Dimensionality reduction is not simply a technique for throwing information away. It is a tool that first asks `has the current representation become too large to see the structure clearly?`

| Current problem state | Why dimensionality reduction comes to mind first | What to check first |
| --- | --- | --- |
| There are too many features to imagine the structure clearly | Because the overall flow can be viewed again through fewer axes | What will be preserved and what will be reduced |
| Many features seem to overlap with one another | Because overlapping variation may be grouped into a few components | Whether there is actually a lot of redundant information |
| Visualization or a follow-up clustering hypothesis is needed | Because the large structure can be viewed at a 2D or 3D level | Whether the visualization is being read as the answer itself |
| You want to reduce computation or simplify downstream model input | Because a smaller representation can make later steps easier to handle | Whether the information loss is worth accepting |
| You want to interpret representative axes such as PCA | Because the direction with large spread can be summarized | Whether the axis with large variance should be treated as meaningful by itself |

The core of this table is to position dimensionality reduction not as `magical simplification`, but as `a tool for building easier axes when representation complexity has become too large`.

## What Does Dimension Mean?

In machine learning, dimension usually connects to the number of axes used to describe one data sample, in other words, the number of features.

For example, if one customer is expressed through the following three numbers:

- Monthly visit count
- Average purchase amount
- Days since last login

that customer can be viewed as one point in a three-dimensional feature space.

Dimension is both an abstract mathematical concept and something that can be understood as `the number of coordinate axes used to describe the data`.

Whenever one feature is added, one more axis for viewing the data is added.

If this is drawn in a very simple way, it looks like the following.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-01-en.mmd"
```

This diagram shows that as dimensions increase, it becomes harder to picture the data directly as if it were a simple drawing. Once the reader grasps the sense that one feature creates one axis, it becomes easier to understand why summary axes are needed again for high-dimensional data.

## Why Does It Become Harder When Features Increase?

Having many features can increase expressive power, but at the same time it creates three kinds of difficulty.

1. It becomes harder for people to imagine the structure.
2. Computational cost can increase.
3. There may be a lot of unnecessary or overlapping information.

For example, a two-dimensional point can be seen directly in a picture. But 50-dimensional, 500-dimensional, or 5000-dimensional data cannot be viewed directly. In the end, they need to be summarized in some other way.

Also, when there are many features, they often store similar information repeatedly. For example:

- Monthly purchase amount
- Yearly purchase amount
- Number of purchases
- Average order amount

These values may not be fully independent of one another.

Dimensionality reduction often becomes a process of asking again `how much genuinely new information is really present?`

## What Is Dimensionality Reduction Trying To Ease?

The scikit-learn user guide explains PCA as a method that decomposes a multivariate dataset into successive orthogonal components and finds directions that explain the largest amount of variance.

At an introductory level, dimensionality reduction can be read as an attempt to ease the following problems.

| Difficulty | What help dimensionality reduction tries to provide |
| --- | --- |
| There are too many features to inspect structure easily | Summarize through fewer axes |
| Features overlap with each other | Group overlapping variation into a few components |
| Visualization is hard | Lower it to 2D or 3D and look at the rough structure |
| Computation is heavy | Change it into a smaller representation so downstream models are easier to handle |

So dimensionality reduction is better understood as `a tool for building a more readable representation` than as `something that completely replaces the original data`.

## Looking At One Scene

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-02-en.mmd"
```

The core of this diagram is that dimensionality reduction is not simple deletion, but `reexpression through newly built axes`. When there are too many features to inspect directly and overlapping information may exist, fewer axes are created to reinterpret the structure or pass it into downstream models.

The key point of this figure is that dimensionality reduction is not a matter of blindly throwing away original features. It is `a matter of looking again through new axes`.

## What Representative Intuition Does PCA Show?

The scikit-learn documentation explains PCA as a method for finding `successive orthogonal components that explain the most variance`.

`Take the direction in which the data spread the most as the first axis, then among the directions orthogonal to it, take the next direction with a large spread as the second axis.`

PCA is closer to the sense of not using the original axes such as x, y, and z 그대로, but instead rotating the axes again toward the directions in which the data actually vary a lot.

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

The moment you look just a little deeper into PCA, the words eigenvalue and eigenvector of the covariance matrix appear immediately. The reason is simple.

`To find the directions in which the data spread most strongly in formulas, you need to find the direction vectors that best explain that spread.`

At an introductory level, the following flow is enough.

1. Center the data around the mean
2. Build a covariance matrix that captures how much the axes move together
3. Find the directions that `explain the most variance` in that matrix
4. Read those directions as eigenvectors, and the size of variance along them as eigenvalues

The formula is usually written like this.

\[
\Sigma v = \lambda v
\]

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

In other words, dimensionality reduction is convenient, but it is not free.

## Where Is It Used Often?

Dimensionality reduction often appears in the following scenes.

| Work scene | What dimensionality reduction does there |
| --- | --- |
| Preparing visualization | Reduce high-dimensional data into 2D or 3D and inspect the rough structure |
| Preprocessing | Change downstream model input into a more compressed representation |
| Trying to reduce noise | Preserve large variation first and place less emphasis on small fluctuations |
| Summarizing text or images | Reduce very many features into a smaller number of components |

So dimensionality reduction is often used first not as `the final model` itself, but as `a lens for rereading the data`.

Even then, it is not enough to write only that the representation changed. You should also leave together which cases were rearranged in the new axes and how. Structures seen in the new axes should first be read as signals for review and hypothesis candidates. Before looking back at the original features, causes or categories should not be finalized.

| What to record together | What is written in this Section | Why it is needed |
| --- | --- | --- |
| Representation change | Into how many components was the original feature space reduced | To make clear what expression was changed |
| Rearrangement of cases | Where the same customer or document moved in the new axes | To see whether the new representation really made the structure easier to read |
| Next question | Is this new axis sufficient for clustering, visualization, or downstream model input? | To check whether simplification really helps the next step |

## How Are Clustering And Dimensionality Reduction Connected?

Chapter 17 examined clustering, and Chapter 18 examines dimensionality reduction. These two often appear together.

- People reduce the data into two dimensions and inspect the cluster structure with their eyes.
- Conversely, they sometimes compress the representation first because they want clusters to become easier to see.

The scikit-learn documentation also explains that PCA can be useful for downstream models such as K-means.

In other words, dimensionality reduction is an independent technique, while also becoming `a preparation stage for later clustering or visualization`.

If this connection is compressed into a diagram, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-1-mermaid-04-en.mmd"
```

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

This small exercise shows how several features can be compressed into one simple summary score. It is intentionally simplified, but it lets the reader feel the difference between `the representation became easier` and `some details were lost`.

- Problem situation: inspect what becomes easier and what disappears when multiple features are compressed into one axis-like value
- Input: samples expressed through three features
- Expected output: one summary value
- Concepts to check:
  - Dimensionality reduction simplifies representation
  - In return, some per-axis detail becomes weaker

```python
samples = [
    {"f1": 2.0, "f2": 2.1, "f3": 2.2},
    {"f1": 4.0, "f2": 4.1, "f3": 3.9},
    {"f1": 6.0, "f2": 5.8, "f3": 6.2},
]

reduced = [
    round((row["f1"] + row["f2"] + row["f3"]) / 3, 2)
    for row in samples
]

print("original samples:", samples)
print("1D summary      :", reduced)
```

The result is as follows.

```text
original samples: [{'f1': 2.0, 'f2': 2.1, 'f3': 2.2}, {'f1': 4.0, 'f2': 4.1, 'f3': 3.9}, {'f1': 6.0, 'f2': 5.8, 'f3': 6.2}]
1D summary      : [2.1, 4.0, 6.0]
```

What the reader should take from this example is:

1. Once three axes are reduced to one, the overall flow becomes easier to inspect.
2. But the detailed differences among `f1`, `f2`, and `f3` are compressed into the summary value.
3. In other words, simplification and information loss come together.

### Change One Value: The Summary Can Stay Similar Even When The Original Pattern Changes

Now change the arrangement of the third sample so that the average remains similar while the shape across axes changes.

```python
samples = [
    {"f1": 2.0, "f2": 2.1, "f3": 2.2},
    {"f1": 4.0, "f2": 4.1, "f3": 3.9},
    {"f1": 7.0, "f2": 6.8, "f3": 4.2},
]

reduced = [
    round((row["f1"] + row["f2"] + row["f3"]) / 3, 2)
    for row in samples
]

print("original samples:", samples)
print("1D summary      :", reduced)
```

```text
original samples: [{'f1': 2.0, 'f2': 2.1, 'f3': 2.2}, {'f1': 4.0, 'f2': 4.1, 'f3': 3.9}, {'f1': 7.0, 'f2': 6.8, 'f3': 4.2}]
1D summary      : [2.1, 4.0, 6.0]
```

The summary value of the third sample is still `6.0`, but now the three axes are not uniformly large because `f3` is relatively lower. If you look only at the summary, it looks like the same conclusion as the previous example, but if you go back to the original features, it is not actually the same sample pattern. That difference is exactly why you must move back and forth between `the visible structure` and `the original features` when reading a dimensionality-reduced visualization or summary axis.

### What Should Be Read Together In This Exercise?

Part 4 is not only about how to view one model output. It is also about learning how to judge what becomes visible and what gets hidden when a representation changes. This exercise forces the reader to keep together `the structure that became easier to inspect after compression` and `the per-axis differences that disappeared because of compression`, so dimensionality reduction is read as an interpretation tool rather than only as a visualization trick. If the learner does not feel the goal here, the missing part is usually not the PCA formula but the practical scene `even with the same summary value, the original pattern can differ`.

| Shared recording language | What to record immediately in this exercise |
| --- | --- |
| What structure appeared | In a one-dimensional summary, different samples could appear to sit in the same place |
| Interpretation boundary | A reduced plot or summary axis does not preserve every difference in the original features |
| Next question | Does the same separation remain in the original feature space or with other projection methods? |

## What To Remember From This Section

- Dimensionality reduction is unsupervised reexpression of many features through fewer axes.
- As the number of features grows, interpretation and computation both become harder.
- PCA can be read first as a method for finding orthogonal axes that explain large variance.
- Eigenvectors are read as directions of new axes, and eigenvalues as the amount of explained variance on those axes.
- Dimensionality reduction makes representations easier to handle, but information loss comes with that convenience.

| What should be viewed together | The question read first in this Section | Where it goes next |
| --- | --- | --- |
| Reexpression hypothesis | Through what new axes did the structure become more readable? | P4-18.2 visualization and information loss |
| Representative cases | What business pattern seems to appear through the new components? | Feature interpretation and downstream model review |
| Next verification question | What was preserved, and what may already have become weaker? | Reconstruction error and visualization caution |

## Short Check

- When there are too many features to read the structure clearly, do you first think of dimensionality reduction as a reexpression tool?
- Can you explain PCA not only as `rotation`, but also as `finding directions that explain variance strongly`?
- Can you distinguish PCA, kernel PCA, and Truncated SVD through the handles of linear axes, nonlinear unfolding, and matrix factorization?

## Sources And References

- scikit-learn developers, `2.5. Decomposing signals in components (matrix factorization problems)`, scikit-learn User Guide, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/decomposition.html](https://scikit-learn.org/stable/modules/decomposition.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `PCA`, scikit-learn API Reference, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html){: target="_blank" rel="noopener noreferrer" }
