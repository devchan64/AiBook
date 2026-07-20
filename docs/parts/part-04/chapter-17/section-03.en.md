# P4-17.3 Supplementary Learning: How To Distinguish Hierarchical Clustering And Spectral Clustering For The First Time

> Section ID: `P4-17.3`
> Version: `v2026.07.20`

After looking at k-means and DBSCAN in P4-17.1, this question naturally remains.

Why are there so many clustering algorithm names, and how are they different from one another?

Two names that come up repeatedly when organizing that question for the first time are hierarchical clustering and spectral clustering.

Rather than going long on implementation details, this supplementary Section distinguishes the two methods from the perspective of `what criterion they use to form groups`.

## Scope Of This Section

This Section answers the following questions.

- What does hierarchical clustering show step by step?
- Why is spectral clustering said to look at connectivity before distance?
- Compared with k-means and DBSCAN, in what scenes do these two methods come to mind?
- When distinguishing the four methods for the first time, what is the first thing worth recording?

This Section focuses on distinguishing `the perspective of merging like a tree` from `the perspective of cutting and grouping a graph`.

## Goals Of This Section

- You can explain hierarchical clustering as `clustering that shows the order in which things merge`.
- You can explain spectral clustering as `clustering that regroupes data by rereading connectivity structure`.
- You can describe that k-means, DBSCAN, hierarchical clustering, and spectral clustering start from different questions.

## Why This Section Is Needed

When first learning clustering, the growing list of algorithm names can make things more confusing rather than less.

- k-means looks at centers
- DBSCAN looks at density
- But then some methods are described as tree-like, while others are described as graph-like

The important thing here is not memorizing more names. It is to first grasp `what each algorithm is trying to use to read clusters`.

So P4-17.3 reorganizes the clustering family through four intuitions: `center`, `density`, `merge order`, and `connectivity`.

## What Does Hierarchical Clustering Show?

Hierarchical clustering does not begin by cutting points into a fixed number of clusters from the start. Instead, it tries to show step by step `what becomes close first and what merges later`.

At an introductory level, one sentence is enough.

`Hierarchical clustering shows not only one clustering result, but also the order in which groups grow.`

Suppose there are four customers.

- A and B are very similar
- C and D are also fairly similar
- The A/B group and the C/D group are somewhat farther from each other

In that case, hierarchical clustering can show the order in which `A and B merge first, C and D merge next, and then the two groups merge into a larger group at the end`.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-3-mermaid-01-en.mmd"
```

The key point in this diagram is the `merge order`, not the `final number of clusters`. So hierarchical clustering naturally comes to mind when `you have not decided yet how many groups to cut into, but you want to see the structure of what becomes close first`.

This difference can be stated more briefly like this.

| What you want to know first | Why hierarchical clustering fits better |
| --- | --- |
| It is still unclear whether to read the data as 2 groups or 4 groups | Because you can look at the merge order and decide the cut point later |
| You want to see which samples become similar to each other first | Because it shows the stages of becoming close, not only the final number of clusters |
| You want to adjust the grouping level together with domain review | Because it lets you inspect multiple grouping levels instead of only one fixed answer |

So hierarchical clustering is closer to `first looking at how groups grow, then deciding later at what height to cut and read them` than to `finding the correct number of clusters in one shot`. That is why it is especially useful in early exploration, when domain interpretation is not settled yet.

## What Is Spectral Clustering Trying To See?

Spectral clustering does not try to read points only through coordinate distance. It tries to reread them through a graph structure that asks `who is connected to whom`.

For an introduction, the following is enough.

`Spectral clustering tries to read breaks in connectivity better than the shape of nearby points alone.`

Suppose there are two curved groups shaped like crescents. In a scene like this, center-based k-means may cut the boundary too straight, but if you look at connectivity structure, it can be more natural to read points on the same curve as one group.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-3-mermaid-02-en.mmd"
```

The key here is not `do we cut the original coordinates directly?` but `do we build a new expression of the connectivity relation first, then split that structure?` So spectral clustering comes to mind in scenes where `the shape is complex, but the connectivity is still clear`.

This can be compared more directly as follows.

| The first problem you hit | Why spectral clustering comes to mind |
| --- | --- |
| A center-based cut breaks a curved structure in the middle | Because it is more natural to read connectivity before geometric centers |
| Some points look far apart, but still continue along the same curve | Because a graph of neighborhood relations can reveal connectivity inside the same structure more clearly |
| The cluster shape does not look like round blobs | Because rebuilding the graph structure may fit better than relying on one distance alone |

Still, spectral clustering is not always the right answer just because `the shape is complex`. The core question is whether `building a graph from neighborhood relations reveals the connectivity inside the same structure more clearly`. In other words, it is more accurate to understand spectral clustering as `a way of rerepresenting connectivity and then reading that structure`, rather than directly cutting coordinates.

## Putting The Four Intuitions Side By Side

If we place the representative intuitions from Chapter 17 into one table, they organize like this.

| Method | What it looks at first | Scene where it naturally comes to mind | What to be careful about first |
| --- | --- | --- | --- |
| k-means | center | When you want to quickly see round and relatively even groups | It is sensitive to the assumed number and shape of clusters |
| DBSCAN | density | When you want to separate noise and inspect irregular groups | It is sensitive to `eps` and `min_samples` |
| Hierarchical clustering | merge order | When you want to see how groups grow step by step | You still need to interpret where to cut |
| Spectral clustering | connectivity | When the shape is complex but the connectivity structure is clear | It is sensitive to how the similarity graph is built |

The purpose of this table is not ranking the methods. The first thing is to hold on to the fact that `they read clusters through different handles`.

If this comparison is turned into concrete selection questions, it looks like this.

| The question you ask first right now | The method that comes to mind first |
| --- | --- |
| Do you want to see the merge order more than fix the number of clusters immediately? | Hierarchical clustering |
| Do you want to keep noise separate and inspect irregular groups? | DBSCAN |
| Do you want a quick baseline for round and relatively even groups? | k-means |
| Do you want to cut a curved or complex connectivity structure? | Spectral clustering |

If we write the difference between hierarchical clustering and spectral clustering more directly, it looks like this.

| The question you hit first | The more natural starting point |
| --- | --- |
| Are you more interested in `what merges first` than in `how many groups to cut into` | Hierarchical clustering |
| Is the order of getting closer itself a clue for interpretation | Hierarchical clustering |
| Is there a curved structure that center points fail to capture well | Spectral clustering |
| Does `who is connected to whom` seem more important than coordinate distance | Spectral clustering |

## Cases And Examples

### Case 1. When You Have Not Yet Decided At What Level To Group Customer Segments

Suppose a subscription service team wants to group customers, but it is difficult to fix the analysis from the start as `3 clusters` or `4 clusters`. In that case, hierarchical clustering can be a useful starting point. By seeing which customers become close first and at what stage they merge into larger groups, the team can read `is it more natural to see this as 2 groups right now, or as 4 groups` together with domain review.

So in this scene, the important thing is not automatically finding the correct number of clusters. It is to look at `the order in which groups grow` and build interpretation candidates more carefully.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-3-mermaid-03-en.mmd"
```

### Case 2. When Curved Movement Paths Are Hard To Cut Well With Centers

When data take a long curved shape, such as location logs or movement trajectories, k-means may cut them too straight based on centers. In such a scene, there are cases where you want to care more about `points connected along the same curve`, and that is when spectral clustering can come to mind. In other words, it is a problem scene where `does this stay connected inside the same structure` matters more than `what is the nearest center`.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-3-mermaid-04-en.mmd"
```

Looking at the two cases together makes the difference clearer.

| The question read first in the case | The method that fits better | Why |
| --- | --- | --- |
| Is it still unclear at what grouping level customer segments should be read | Hierarchical clustering | Because you can compare multiple cut levels while looking at the merge order |
| Do you want to see whether curved movement paths stay inside the same structure | Spectral clustering | Because it is more natural to read connectivity before centers |

In short, hierarchical clustering is closer to interpreting `the order in which groups grow`, while spectral clustering is closer to inspecting `whether connectivity structure is preserved`.

## Practice And Example

This practice block is a verification exercise: choose first `what clustering intuition should come to mind` and then compare your choice with the explanation right below.

- Problem situation: distinguish, scene by scene, whether round groups, irregular groups, merge order, or connectivity structure matters first
- Input: four short problem scenes
- Expected output: for each scene, the method that should come to mind first and the reason
- Concepts to check:
  - There are questions that must be read before algorithm names
  - Even with the same data, the starting point changes depending on `what structure you want to inspect`

First cover the `Method to think of first` column, write down your own choice for each scene, and then compare it with the table.

| Scene | Method to think of first | Why this method fits first |
| --- | --- | --- |
| You want a quick baseline for round and fairly even groups | k-means | Because the question starts with putting centers down and grouping quickly |
| You want to leave noise aside and inspect irregular groups | DBSCAN | Because density and noise separation matter first in this scene |
| You want to see what merges first before fixing the number of clusters | Hierarchical clustering | Because merge order itself is the interpretation clue here |
| You want to preserve a curved structure, and a center-based cut looks awkward | Spectral clustering | Because reading connectivity first is more natural than reading centers first |

The point of this practice is not memorizing algorithm names. It is to ask first `what structure do I want to inspect?` More important than getting the label right is being able to explain why that question comes first in the scene.

## What Is Worth Recording In A First Comparison?

At the beginning, it is more practical to record the following questions than to focus on implementation details.

| Question to record | Why it is needed |
| --- | --- |
| Do we need to fix the number of clusters from the start | Because this becomes the first criterion for separating k-means from other methods |
| Do we need to keep noise separate | Because this becomes the criterion for whether DBSCAN-like intuition is needed |
| Does the merge order itself matter | Because this is a reason to think of hierarchical clustering |
| Is the shape complex, but does connectivity seem more important | Because this is a reason to think of spectral clustering |

If you record these questions first, you will read more easily `what clustering intuition the current data scene is asking for`, instead of trying to memorize algorithm names.

## Checklist

- Can you explain that hierarchical clustering shows `what merges first` more than `how many groups there are`?
- Do you understand that spectral clustering is closer to rereading `connectivity structure` than to rereading `distance itself`?
- Is this a scene where you want to see what becomes close first, rather than fixing the number of clusters immediately?
- Is this a scene where connectivity structure must be read first, not merely one with an irregular shape?
- Instead of reading the clustering result as one final answer, can you explain from what question this method came to mind?
- Can you distinguish k-means, DBSCAN, hierarchical clustering, and spectral clustering again through the four axes of `center`, `density`, `order`, and `connectivity`?

## Sources And References

- scikit-learn developers, `2.3. Clustering`, scikit-learn User Guide. Consulted for the basic descriptions and comparison axes of hierarchical clustering, spectral clustering, k-means, and DBSCAN. Accessed 2026-07-19. [https://scikit-learn.org/stable/modules/clustering.html](https://scikit-learn.org/stable/modules/clustering.html){: target="_blank" rel="noopener noreferrer" }
- Ulrike von Luxburg, `A Tutorial on Spectral Clustering`, Statistics and Computing, 2007. Consulted for the background connecting spectral clustering to graph Laplacians and connectivity structure. Accessed 2026-07-19. [https://doi.org/10.1007/s11222-007-9033-z](https://doi.org/10.1007/s11222-007-9033-z){: target="_blank" rel="noopener noreferrer" }
