# P4-17.1 Intuition For Clustering

> Section ID: `P4-17.1`
> Version: `v2026.07.26`

Up through gradient boosting in P4-16, we followed how models improve predictive performance on problems where answer labels already exist. If we shift the viewpoint slightly here, the next question appears.

If there is no answer label at all, how can we find structure inside the data?

That question is the starting point of clustering.

Clustering is an unsupervised learning problem that tries to find what groups of similar data points form clusters without answer labels.

In other words, clustering is closer to `discovering structure` than to `solving a problem by getting the answer right`.

This Section explains [clustering](/AiBook/en/reference/concept-glossary-alpha/c/#clustering), [cluster](/AiBook/en/reference/concept-glossary-alpha/c/#cluster), and the difference between [answer labels](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) and clusters. In the next Section, we continue the current line of judgment from this handle, and the basic sense of reading grouping proposals as structure exploration is connected again through [unsupervised learning](/AiBook/en/reference/concept-glossary-alpha/u/#unsupervised-learning), [similarity](/AiBook/en/reference/concept-glossary-alpha/s/#similarity), and [cluster label](/AiBook/en/reference/concept-glossary-alpha/c/#cluster-label).

## Questions Closed By Clustering

This Section answers the following questions.

- How is clustering different from supervised learning?
- Why is the phrase `similar` so important?
- Why is a cluster different from a class label?
- What different intuitions do [k-means](/AiBook/en/reference/concept-glossary-alpha/k/#k-means) and [DBSCAN](/AiBook/en/reference/concept-glossary-alpha/d/#dbscan) show?
- With what attitude should clustering results be read?

This Section first closes the question `what question clustering answers in structure exploration without labels`. Cautions for interpreting results continue in P4-17.2, hierarchical clustering and spectral clustering continue in P4-17.3 supplementary learning, cluster quality metrics continue in P4-6.4 supplementary learning, and cautions for reading structure together with dimensionality reduction continue in P4-18.1 and P4-18.2.

## Judgments To Keep From Clustering

- You can explain clustering as `finding structure without labels`.
- You can explain that a cluster is not a human-assigned correct answer, but a group found from the data.
- You can describe that k-means and DBSCAN have different clustering intuitions.
- You can get an initial sense of why it is risky to immediately treat clustering results as facts or causes.

## Why This Section Is Needed

When first learning machine learning, people usually start by asking whether a problem is classification or regression. But in real work, unlabeled data are often even more common.

For example:

- You want to group customers by a few usage patterns
- You want to see what topic bundles news articles gather into
- You want to see whether sensor data separate into a few states
- You want to see whether outliers stick out on their own

These questions ask not `what is the correct answer?` but `what structure is hidden here?` Clustering is the first tool that enters exactly that kind of question.

So P4-17.1 is the Section where the viewpoint shifts from `prediction models` to `exploring data structure`.

### When Does It Make Sense To Think Of Clustering First?

Clustering does not appear when the goal is getting the answer right. It appears naturally when the criterion is `do I want to see the structure first without labels?`

| Current question | Why clustering comes to mind first | What to check first |
| --- | --- | --- |
| I want to group usage patterns without labels | Because it fits proposing groups of similar data | Which features will define similarity |
| Exploratory structure matters more than prediction | Because the goal is discovering structure, not forecasting | Whether clusters are being read as correct answers |
| I want to see outliers or groups that stand apart | Because density- or distance-based clustering can show structure | Whether k-means or DBSCAN fits better |
| I want to break customers, documents, or sensor states into a few lumps | Because it becomes a starting point for segment hypotheses | Sensitivity to cluster count or density criteria |
| I want to make follow-up labeling or domain-review questions | Because clusters can suggest candidates for interpretation | Whether the cluster result is being sent directly into policy |

The core of this table is to place clustering not as `a substitute for a predictive model`, but as `a tool for structure exploration and hypothesis generation`.

## What Is Clustering Trying To Do?

The scikit-learn user guide describes clustering as a task performed on unlabeled data. That means it is not about predicting after the correct answer has already been given. It is about letting the algorithm search for a basis on which the data can be grouped.

`Look at unlabeled points and try grouping together the ones that are close or show similar patterns.`

The important thing here is [similarity](/AiBook/en/reference/concept-glossary-alpha/s/#similarity). Clustering is ultimately connected to the question `what counts as similar?`

## How Is It Different From Supervised Learning?

In classification, people usually ask questions like these.

- Is this email spam or not?
- Will this customer churn or not?

These already have answer labels.

Clustering asks questions like these instead.

- How do these customers appear to separate by usage pattern?
- What topic bundles do these documents appear to form?

In other words, clustering is not `a problem of predicting labels`, but `a problem of proposing groups when labels are absent`.

| Question | Supervised learning | Clustering |
| --- | --- | --- |
| Is there an answer label? | Yes | No |
| Goal | Predict the correct answer | Explore structure |
| Output | class, score, value | cluster label, grouping |
| Key question | What should be predicted? | What gets grouped together as similar? |

The cluster label here is not meaning given in advance by humans. It is only a number attached for convenience by the algorithm.

If we view this difference once through a diagram, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-1-mermaid-01-en.mmd"
```

This diagram shows at a glance where supervised learning and clustering diverge at the starting point. Supervised learning learns a mapping with answer labels, but clustering first finds the structure of similarity without labels, and then humans must interpret those groups again.

## Why Does The Word `Similar` Matter So Much?

Clustering ultimately works on ideas such as [distance](/AiBook/en/reference/concept-glossary-alpha/d/#distance), [density](/AiBook/en/reference/concept-glossary-alpha/d/#density), connectivity, and center between data points.

That means clusters do not just appear on their own. They change depending on `what standard was used to define similarity`.

Consider customer data, for example.

- Number of monthly visits
- Average purchase amount
- Days since the last login

If we look at customers through these three [features](/AiBook/en/reference/concept-glossary-alpha/f/#feature), similarity can mean that their positions are close along these three axes.

But for text documents, similarity may change into closeness in word distributions or embedding space.

So in clustering, the word `similar` is not an emotional expression. It is a definition of relationships inside [feature space](/AiBook/en/reference/concept-glossary-alpha/f/#feature-space).

If this is compressed into a data flow, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-1-mermaid-02-en.mmd"
```

This diagram shows that clustering is not a process that pulls an answer directly out of raw data. Only after choosing features and deciding what similarity rule to use do clusters form, so the result is always affected by representation and similarity definition.

The final stage of the diagram right above is important. Clustering is not `an answer generator`, but `a structure proposer`. Once the result comes out, humans still need to interpret what those groups actually mean.

## Why Is A Cluster Different From A Class?

The most common misunderstanding is this.

`Now that clusters came out, this must already be the true category.`

But clusters and classes are different.

- Class: a correct category whose meaning was defined by humans
- Cluster: a group found by the algorithm inside the data

For example, even if customer segments are divided into three clusters, that does not automatically mean they are official categories such as `VIP / regular / churn risk`. That interpretation is attached later by humans.

So clustering does not `automatically finalize meaning`. It is closer to `proposing interpretation candidates`.

If we picture this point, it looks like the following.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-1-mermaid-03-en.mmd"
```

This diagram separates cluster numbers from business meaning. Outputs such as `cluster 0` and `cluster 1` are still only temporary IDs, and interpreting them as `VIP customer`, `light user`, or `risk group` happens later in the human review step.

## What Intuition Does k-means Show?

The scikit-learn user guide explains K-means as an algorithm that divides samples into `n groups of equal variance` and tries to reduce inertia, or the within-cluster sum of squares. It also describes the process of assigning each sample to the nearest cluster based on [centroids](/AiBook/en/reference/concept-glossary-alpha/c/#centroid).

k-means creates clusters by placing a few centers and attaching each point to the nearest center.

In other words, k-means is a center-based intuition.

So it tends to fit the following situations.

- When the number of clusters can be decided in advance
- When clusters look round and relatively even in size
- When you want a quick first look at the basic structure

But as the scikit-learn documentation also points out, it may not fit elongated or complex cluster shapes well.

## What Intuition Does DBSCAN Show?

The scikit-learn clustering overview table describes DBSCAN as useful for `non-flat geometry`, `uneven cluster sizes`, and `outlier removal`.

`DBSCAN builds clusters by looking at how densely points gather, without deciding centers first.`

In other words, DBSCAN is a density-based intuition.

So it comes to mind in the following situations.

- When cluster shapes are not round
- When some points should be left separately as noise or outliers
- When cluster sizes may not be even

On the other hand, if density differences are very large or the parameters do not fit, clusters may be hard to capture well.

## Putting k-means And DBSCAN Side By Side

| Question | k-means | DBSCAN |
| --- | --- | --- |
| Cluster intuition | center | density |
| Is the number of clusters fixed in advance? | Usually yes | Usually no |
| Outlier handling | Weak | Relatively better at exposing them |
| Cluster shape | Better for round and even shapes | Can handle more complex shapes |

This comparison is not about `which one is better`. It is about `what kind of structure you expect`.

If we compare only the intuition, it is often easier to read the two algorithms as starting from entirely different questions.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-1-mermaid-04-en.mmd"
```

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-1-mermaid-05-en.mmd"
```

The first diagram shows that k-means is `a way of placing centers first and then attaching points`. The second shows that DBSCAN is `a way of expanding dense connected regions while leaving sparse points behind`. When the comparison is split instead of forced into one panel, readers can understand more quickly that `center-based` and `density-based` are different clustering questions.

## Cases And Examples

### Case 1. When You Want To Regroup Shopping-Mall Customers By Usage Pattern Rather Than Sales Rank

When an online shopping team looks at customers, it is easy to separate them only by a single criterion such as `how large was this month's purchase amount?` But in reality, patterns are mixed: customers who visit often but buy small amounts, customers who visit rarely but spend a lot at once, customers whose recent visits stopped, and so on. If you look only at amount, they can be forced into the same category. Clustering proposes similar customer groups by looking together at features such as visit count, purchase amount, and recency. As a result, the team can discover `behavior-pattern-centered` groups that were not visible in a simple sales ranking table, and then continue with interpretation and marketing-strategy review.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-1-mermaid-06-en.mmd"
```

If this case is compressed into a review memo, it can be written like this.

| Candidate group | Representative case | What not to decide immediately | Next question to check |
| --- | --- | --- | --- |
| Group of customers who visit often but purchase in small amounts | Sample customers with high visit count and mid-to-low spend | Do not call them VIPs or loyal customers right away | Does this also connect with revisit rate, lifetime value, and churn rate? |
| Group of customers who visit rarely but spend heavily at once | Sample customers with low visit count and high spend | Do not immediately pass this to a special high-price customer policy | Is this seasonal buying or a repeated pattern? |

### Case 2. When There Are No Article Classification Labels Yet And You Want To Build Topic Groups For Editorial Review First

Suppose a news-service team wants to organize incoming articles, but there are not yet enough labels such as `politics`, `economy`, or `sports`. If humans try to classify articles one by one just by skimming titles, documents with fuzzy boundaries, such as technology pieces and industry pieces, repeatedly shake the judgment about where they belong. In that situation, clustering gives a starting point for `first grouping similar articles together` based on article embeddings or word distributions.

The important point here is that clusters do not immediately replace the correct categories. For example, if one group gathers articles about `semiconductor investment`, `AI chips`, and `data centers`, that group could be read as a `technology` cluster or as an `industry` cluster. In other words, clustering suggests `sets of documents the editorial team should review together first`, but the final topic names and operational classification system still have to be attached later by humans.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-1-mermaid-07-en.mmd"
```

If this case is compressed into a work memo, it can be written like this.

| Candidate group | Representative case | What not to decide immediately | Next question to check |
| --- | --- | --- | --- |
| Group where semiconductor investment and AI infrastructure articles gather together | Data-center investment article, AI-chip demand article | Do not immediately finalize it as a `technology` cluster | Where exactly does the boundary between industry and technology articles fall? |
| Group where player results and club-management stories gather together | Match-summary article, coach-replacement article | Do not fix it only as one `sports` cluster immediately | Do result articles and operations articles also need to be separated again? |

## Practice And Example

This example is a tiny exercise that uses only two coordinates to see whether points look like they form two groups. It does not stop after one run. It also looks at how the cluster hypothesis becomes less stable when one point changes.

- Problem situation: inspect whether unlabeled points naturally look like a few groups
- Input: two-dimensional coordinates
- Expected output: an intuition for nearby point groups
- Concepts to check:
  - Clusters begin from spatial relationships
  - Even without labels, a sense of grouping can appear

First, look at the coordinates below and write down for yourself how many groups the points seem to form.

| Point ID | Coordinate |
| --- | --- |
| A | (1.0, 1.2) |
| B | (1.1, 0.9) |
| C | (0.8, 1.0) |
| D | (5.0, 5.1) |
| E | (5.2, 4.9) |
| F | (4.8, 5.0) |

At this stage, readers usually make a judgment like the following.

| Grouping hypothesis that appears first | Why it is easy to read it this way |
| --- | --- |
| A, B, and C look like one group | They are close together in the lower-left area |
| D, E, and F look like another group | They are close together in the upper-right area |
| The whole set looks like two groups | The gap between the two point sets is relatively large |

What should be read first here is the following.

1. Even without labels, point positions can suggest a sense of groups.
2. Clusters are ultimately connected to the question of which points gather closely in some space.
3. Real algorithms try to generalize this kind of grouping criterion and find it automatically.

### Change One Value: How Should We Read It When A Point Appears In The Middle?

This time, add point G in the middle and read the scene again.

| Point ID | Coordinate |
| --- | --- |
| A | (1.0, 1.2) |
| B | (1.1, 0.9) |
| C | (0.8, 1.0) |
| G | (3.0, 3.1) |
| D | (5.0, 5.1) |
| E | (5.2, 4.9) |
| F | (4.8, 5.0) |

First answer these questions for yourself.

- Can you still immediately say that there are `two groups`?
- Is G closer to the left group, the right group, or a boundary case?
- What is needed right now: `the correct cluster number` or a note about where ambiguity appears?

Then compare with the explanation below.

| What changed in the scene | What should be rechecked first | Why it matters |
| --- | --- | --- |
| Boundary point G was added | Whether the boundary between the two groups is still clear | A single boundary case can shake the structure hypothesis |
| The simple `left three, right three` grouping no longer holds | Whether G is assigned automatically to one side | This reveals that a cluster is an interpretation candidate, not an answer |
| The counts changed from 3 vs 3 to 3 vs 4 | Whether boundary interpretation now matters more than group size | In practice, ambiguous points should be recorded before cluster numbers |

Even adding one point makes the interpretation of `two groups` less clear. What the reader should feel here is that clustering is not `a device that gives the answer`, but `a device for seeing how the structure hypothesis changes once a standard of similarity is chosen`. Since interpretation changes depending on how points near the boundary are read, in practice you should record `what remained ambiguous` before you record cluster numbers.

### Apply k-means and DBSCAN to the same point set

This time, apply `k-means` and `DBSCAN` side by side to the same toy data and check how the `center-based` and `density-based` viewpoints produce different outputs.

- Problem situation: when there are two dense groups and one faraway point, examine how `k-means` and `DBSCAN` read that point differently
- Input: two dense groups plus one faraway point
- Expected output: confirm that `k-means` still places the faraway point into one of its clusters, while `DBSCAN` can leave it as noise
- Concepts to check:
  - `k-means` assigns every point inside a pre-decided number of clusters
  - `DBSCAN` can leave low-density points outside the clusters
- Values to change before running:
  - Change `n_clusters` from 2 to 3 and check whether G starts to look like its own cluster
  - Make `eps` smaller or larger than 0.6 and check how DBSCAN's noise decision changes
  - Move G from `[8.5, 1.0]` to `[6.0, 4.0]` and check whether the difference between the two algorithms becomes smaller

```python
# This example compares how k-means and DBSCAN assign the outlier-like point G on the same point set.
import numpy as np
from sklearn.cluster import DBSCAN, KMeans

names = ["A", "B", "C", "D", "E", "F", "G"]
X = np.array([
    [1.0, 1.1],
    [1.2, 0.9],
    [0.9, 1.0],
    [5.0, 5.1],
    [5.2, 4.8],
    [4.9, 5.0],
    [8.5, 1.0],
])

kmeans = KMeans(n_clusters=2, random_state=0, n_init=10)
km_labels = kmeans.fit_predict(X)

left_km = int(np.argmin(kmeans.cluster_centers_[:, 0]))
right_km = int(np.argmax(kmeans.cluster_centers_[:, 0]))
km_groups = {
    "left-centered group": [name for name, label in zip(names, km_labels) if label == left_km],
    "right-centered group": [name for name, label in zip(names, km_labels) if label == right_km],
}

dbscan = DBSCAN(eps=0.6, min_samples=2)
db_labels = dbscan.fit_predict(X)

dense_labels = sorted(label for label in set(db_labels) if label != -1)
db_groups = {}
for order, label in enumerate(dense_labels, start=1):
    db_groups[f"dense group {order}"] = [
        name for name, current in zip(names, db_labels) if current == label
    ]
db_groups["noise"] = [name for name, current in zip(names, db_labels) if current == -1]

print("k-means :", km_groups)
print("DBSCAN  :", db_groups)
```

An example output is as follows.

```text
k-means : {'left-centered group': ['A', 'B', 'C'], 'right-centered group': ['D', 'E', 'F', 'G']}
DBSCAN  : {'dense group 1': ['A', 'B', 'C'], 'dense group 2': ['D', 'E', 'F'], 'noise': ['G']}
```

What should be read first from this result is the following.

| Comparison point | What appeared in k-means | What appeared in DBSCAN | Why it matters |
| --- | --- | --- | --- |
| Cluster-count handling | It placed every point into the two pre-decided clusters | It formed two dense groups and left G as noise | This is where `forcing a cluster count` and `leaving points outside clusters` diverge |
| Faraway point G | It was assigned together with the right-side group | It was not placed into any cluster | The difference in handling outlier-like points becomes directly visible |
| Interpretation style | It leans toward `every point belongs to one of the clusters` | It leans toward `only dense regions become clusters and the rest can remain outside` | It lets the reader verify the difference between center-based and density-based intuition at the output level |

So, even on the same input, `k-means` reads the problem as `assignment by center inside a pre-decided number of clusters`, while `DBSCAN` reads it as `forming clusters from dense regions and leaving sparse points outside`. That is why `DBSCAN` feels more natural when you want to leave outlier-like points aside, while `k-means` feels more natural when you want a quick baseline grouping into `a few clusters`.

### What Should Be Read Together In This Example?

The goal of Part 4 is not to list model names, but to build criteria for how problems should be defined and how results should be read. This exercise checks all at once the problem definition `a structure exploration problem without answer labels`, the evaluation viewpoint `one point in the middle can shake the cluster hypothesis`, the comparison viewpoint `k-means and DBSCAN can read the same point differently`, and the application principle `the grouping hypothesis and representative cases should be recorded together`. In other words, if you ran a clustering example but still did not feel the goal of the Part, the problem usually was not too few runs. It was that the sentences for `interpreting the difference in results and passing it to the next question` were missing.

| Shared recording language | What to record immediately in this example |
| --- | --- |
| What structure appeared | A set of points that looked like two groups could be shaken by only one boundary point |
| Interpretation boundary | A cluster is not an automatic answer, but an interpretation candidate built on a similarity criterion |
| Next question | How do groups change if the distance rule, scaling, or outlier handling changes? |

| What should be looked at together | The question read first in this Section | Where it goes immediately next |
| --- | --- | --- |
| Grouping hypothesis | Under what feature criteria did what groups appear? | P4-17.2 cautions for cluster interpretation |
| Representative cases | How should each group be described at the sample level? | Cluster summaries and domain interpretation |
| Next verification question | By what should we recheck whether this structure is really meaningful? | Scaling, parameters, and follow-up outcome comparison |

## Checklist

- Have you made it clear that the need here is not answer prediction but structure exploration?
- Can you explain that clustering is unsupervised learning that finds structure in unlabeled data?
- Can you explain that a cluster is not a correct class but an interpretation candidate?
- Do you understand that similarity is defined on criteria such as distance, density, and connectivity?
- When comparing k-means and DBSCAN, can you first explain the intuition difference between center-based and density-based clustering?
- Can you speak separately about what similarity criterion is being used and what clustering intuition, such as k-means or DBSCAN, is being used?
- Do you know that clustering results are the starting point of interpretation, not truth that becomes fixed automatically?

## Sources And References

- scikit-learn developers, `2.3. Clustering`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/clustering.html](https://scikit-learn.org/stable/modules/clustering.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `KMeans`, scikit-learn API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `DBSCAN`, scikit-learn API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html){: target="_blank" rel="noopener noreferrer" }
