# P4-17.2 Cautions When Interpreting Clustering Results

> Section ID: `P4-17.2`
> Version: `v2026.07.26`

In P4-17.1, clustering was introduced as an unsupervised learning problem that finds structure in unlabeled data. The more important stage now is interpretation.

If the algorithm proposes groups, how far can we trust those groups?

A clustering result is a proposal about data structure, not an automatically finalized correct answer or causal explanation.

The risk of clustering usually arises less from the calculation itself than from `humans overinterpreting the result`.

This Section does not repeat the basic definition of [clustering](/AiBook/en/reference/concept-glossary-alpha/c/#clustering) at length. The core intuition `exploring structure without labels` reconnects through P4-17.1, [unsupervised learning](/AiBook/en/reference/concept-glossary-alpha/u/#unsupervised-learning), and [cluster](/AiBook/en/reference/concept-glossary-alpha/c/#cluster), and here the focus is only on how to read the result without overtrusting it.

## Questions Closed By Cluster Interpretation

This Section answers the following questions.

- Why should a clustering result not be read immediately like a correct [supervised learning label](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label)?
- Why can the same data produce different clusters depending on representation and parameters?
- Why do cluster numbers carry no meaning?
- Why is it risky to connect clustering results directly to business policy or human evaluation?
- How should clustering results be read conservatively?

This Section first closes the question `why clustering results should not be read immediately as correct answers or causal explanations`. Cluster evaluation metrics continue in P4-6.4, visualization and embedding-space distortion continue in P4-18.2, and the connection to semi-supervised learning continues in P4-17.4 supplementary learning.

## Judgments To Keep From Cluster Interpretation

- You can explain that a clustering result differs from a correct class label.
- You can describe that the same data can yield different clusters depending on feature choice and parameter settings.
- You can explain that cluster numbers themselves have no fixed meaning.
- You can understand why extra review is needed before connecting cluster results to business decisions.

## Why This Section Is Needed

At first glance, clustering can look very persuasive.

- The data split into a few groups
- Each group looks fairly plausible
- Then the grouping starts to feel like a true category

That is exactly where the misunderstanding begins.

Clustering has not `predicted the correct answer`. It has `proposed a structure`. People want to attach meaning to that proposal, but if that happens too quickly, it can lead to wrong conclusions.

So P4-17.2 is the Section for learning `the brake on interpretation` more than the computation of clustering itself.

### When Should We Stop And Recheck A Cluster Interpretation?

The more plausible a clustering result looks, the faster we need to check `am I already mixing up a structure proposal with an assigned meaning?`

| What appears on the surface | Why you should stop first | What to check together |
| --- | --- | --- |
| You want to attach grade-like meaning directly to cluster numbers | Because numbers are only identifiers | Do not assign meaning before human review |
| Clusters change when you change features, scaling, or parameters | Because the result may depend on the lens rather than on one truth | Record under what settings the result changes |
| You want to use clusters directly as risk-group or premium-group policy | Because structure proposals and policy decisions can be mixed up too easily | Verify with actual labels and follow-up outcomes |
| One cluster looks so plausible that confidence grows quickly | Because interpretation candidates can easily be overread as true categories | Review representative cases and alternative interpretations |
| Numbers or groupings shift slightly between runs | Because result stability may not be sufficient | Compare reruns and re-representations |

The purpose of this table is not to make clustering untrustworthy, but to stop first at the point `where an exploratory result starts being treated like a fact`.

This risky flow looks like the following.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-2-mermaid-01-en.mmd"
```

This diagram shows the dangerous interpretation path in which a clustering result is accepted too quickly as fact. The key point is that if a grouping looks plausible and is immediately treated like a true category, it can race all the way to risky policy decisions.

## A Cluster Is Not A Correct Label

As seen in P4-17.1, a [cluster](/AiBook/en/reference/concept-glossary-alpha/c/#cluster) is a grouping the algorithm found in the data. By contrast, a [supervised learning label](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) is a category predefined by people according to the problem definition.

The two can look similar on the surface, but their roles are different.

| Item | Correct label | Cluster |
| --- | --- | --- |
| Who defined it? | People, domain rules, data collection process | Algorithm |
| Purpose | Define the prediction target | Explore structure |
| Meaning | Usually defined in advance | Attached later through interpretation |
| Stability | Fairly stable unless the definition changes | Can change with representation, distance rule, and parameters |

The most important sentence is this.

`A cluster is an interpretation candidate, not a correct category.`

## Why Do Cluster Numbers Have No Meaning?

Clustering results often look like the following.

- cluster 0
- cluster 1
- cluster 2

Many readers then unconsciously read them like this.

- 0 means a lower grade
- 2 means a higher grade

But that interpretation is usually wrong.

A cluster number is only a temporary identifier assigned by the algorithm. In the next run, the same grouping may receive different numbers.

Interpretations such as `cluster 2 is larger or better than cluster 1` usually mean nothing.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-2-mermaid-02-en.mmd"
```

This diagram visually fixes the point that cluster numbers do not indicate ranks or levels. `cluster 0`, `cluster 1`, and `cluster 2` are only IDs, so attaching value judgments from the size of the number immediately leads to a wrong reading.

## Why Can The Same Data Produce Different Clusters?

As seen in P4-17.1, clustering depends heavily on `what counts as similar`. So even with the same raw data, the result can change when the following change.

- What [features](/AiBook/en/reference/concept-glossary-alpha/f/#feature) were included
- Whether [feature scale](/AiBook/en/reference/concept-glossary-alpha/s/#standardization) was adjusted
- How [distance](/AiBook/en/reference/concept-glossary-alpha/d/#distance) was measured
- What value was chosen for the number of clusters `k`
- How DBSCAN's `eps` and `min_samples` were set

A clustering result is usually not `the one truth inside the data itself`. It is `one interpretation obtained on top of a chosen representation and criterion`.

If this point is drawn all at once, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-2-mermaid-03-en.mmd"
```

This diagram shows all at once that even the same raw data can lead to different clustering results when feature choice, scaling, distance criteria, or parameters change. In other words, the algorithm is not pulling out `the one truth`. It can propose different groupings depending on the lens and criterion used to read the data.

The meaning of this picture is simple.

`Even with the same data, the grouping can change if the reading lens changes.`

## Why Do Feature Choice And Scaling Matter So Much?

Suppose we are clustering customer data.

- Monthly visit counts range from 1 to 20
- Average purchase amounts range from 10,000 won to 1,000,000 won

If these two features are used together as they are, the amount axis is much larger in scale, so the clustering can be pulled more by amount than by visit count.

Also, a completely different structure can appear depending on which features are removed or added.

Clustering often needs to be read like this.

`Before saying the cluster changed, check what was used as the basis for clustering.`

## What Does It Mean To Say That Parameters Make The Cluster?

In k-means, the result changes depending on what value is chosen for `k`. In DBSCAN, the definition of a dense region changes depending on `eps` and `min_samples`.

What matters here is not the formula, but the following sense.

- There is a part where the algorithm `discovers` clusters
- At the same time, there is also a part where people `induce` clusters

Parameters are less like a password that opens the hidden truth and more like a handle for deciding how the structure will be read.

As the previous diagram showed, even the same data can be grouped differently when values such as `k`, `eps`, or `min_samples` change. So when recording a clustering result, you should leave together `under what parameters was this result obtained?`

## Clusters Do Not Explain Causes

A dangerous interpretation that often appears after looking at clustering results is the following.

- This cluster is the loyal-customer group
- This cluster is the problematic-customer group
- This cluster is the risk group

Statements like these may be possible later, but they do not follow automatically.

That is because clustering usually tells us only this much.

`These points look similar to one another.`

Why that similarity appears, what cause lies behind it, and what policy should be applied are all questions that require separate analysis.

Clusters may suggest correlated patterns, but they do not automatically provide [causality](/AiBook/en/reference/concept-glossary-alpha/c/#causal-inference).

## How Does This Connect To Semi-Supervised Learning?

After learning clustering, a natural thought appears.

`If only a small amount of labels exist, could we build clusters first and use those groups as support for label learning?`

That question continues into [semi-supervised learning](/AiBook/en/reference/concept-glossary-alpha/s/#semi-supervised-learning). Semi-supervised learning is usually a problem setting that tries to use `a small amount of labeled data` together with `a large amount of unlabeled data`.

In that context, clustering can connect in the following way.

| Connection that appears first | Why it should not be used directly as the answer |
| --- | --- |
| If similar points gather in one cluster, they may seem likely to share the same label | Because clusters reflect similarity structure, not necessarily the true label boundary |
| When labels are scarce, clusters can suggest label candidates | Because if labels are spread through a wrongly formed cluster, the error spreads as well |
| Clusters can help decide the order of follow-up labeling | Because cluster numbers themselves carry no meaning, so sending them directly into automatic labeling without human review is risky |

So a cluster can become an auxiliary starting signal for semi-supervised learning, but it is not a device that replaces the correct label itself.

Restated through this Section's central question, it becomes this.

`Even if a cluster looks plausible, that group must not be treated immediately like the true answer.`

So even when connecting to semi-supervised learning, the first required attitude stays the same. Clusters should not be read as `automatic label generators`, but more conservatively as `tools that propose label hypotheses and review priority`.

## Why Is It Risky To Connect Clusters Directly To Business Policy?

Clustering is useful in exploratory analysis, but problems can arise when it is moved directly into decision rules.

For example:

- `cluster 2 is the churn-risk group, so let's send discount coupons automatically`
- `cluster 1 is the loyal-customer group, so let's reduce the screening process`
- `cluster 0 is the abnormal-user group, so let's mark it as a blocking candidate`

These judgments can all be too fast if they rely on the cluster result alone.

That is because:

- clusters can change with parameters and representation
- verification against the actual business target label may not exist
- noise or data bias may have created some of the groups

In other words, a cluster is closer to `a signal that starts further review` than to `a start button for policy automation`. Even when cluster results appear repeatedly, the safer reading is conservative until they are compared with real labels or follow-up outcome metrics.

The same principle applies when moving toward business use. The appearance of clusters is not the signal to use them immediately in policy. Each group must first be described, compared with domain data, and verified through later outcomes before real use is considered.

## Then How Should We Overcome This Risk?

Reducing the risk of clustering does not mean throwing clustering away. It means having `a reading procedure that prevents the cluster result from being used immediately as the conclusion`.

At an introductory level, it helps to fix the following four steps first.

1. Summarize the representative features of each cluster before looking at the cluster number.
2. Check whether a similar structure remains even after making small changes to scaling, features, or parameters.
3. Re-read representative cases for each cluster at the sample level.
4. Before moving to policy or meaning interpretation, compare the result against real labels or follow-up outcome metrics.

The core of these four steps is not to move straight from `cluster output -> immediate interpretation`, but to insert `summary`, `sensitivity check`, `representative cases`, and `follow-up verification` in the middle.

| Reading that becomes risky immediately | Safer reading |
| --- | --- |
| `This is cluster 2, so it is the premium-customer group` | `What common pattern do members of cluster 2 show?` |
| `This group appeared, so it should be usable in policy` | `Does this grouping remain under different settings and over different time ranges?` |
| `One cluster looks plausible, so the cause must be explained too` | `Separate the fact that points were grouped similarly from any explanation of cause` |

## What Should Be Done Immediately After Seeing A Cluster Result?

In practice, if you remember only the cautions, your hands can stop moving. So right after seeing a cluster result, it is better to organize it in the following order.

| Order | Immediate action | Why it is needed |
| --- | --- | --- |
| 1 | Write cluster size, average values, and representative samples | To read by actual pattern rather than by number |
| 2 | Recheck after small changes to scaling, feature choice, or parameters | To see whether the result depends only on one lucky setup |
| 3 | Write only one or two interpretation candidates for each cluster from a domain perspective | To separate interpretation candidates from finalized meaning |
| 4 | Write a plan for comparing with real labels, follow-up reactions, or operating metrics | To move the exploratory result into the verification phase |

Compressed into one line, this becomes:

`We saw clusters -> summarize them -> perturb them -> read representative cases -> leave verification questions.`

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-2-mermaid-04-en.mmd"
```

This diagram shows `a flow that delays interpretation and inserts review steps one by one` after a cluster result appears. The key is not to pass the algorithm output straight into policy, but to place human review and rechecking steps in the middle without fail.

### If You Leave It As A Small Review Memo

After first seeing a cluster result, the following short memo is often more useful than a long report.

| Item | Example memo |
| --- | --- |
| Cluster summary | `cluster 0: low visits, low spend`, `cluster 1: high visits, medium spend` |
| Sensitivity check | `With standardization applied, part of the boundary between cluster 1 and 2 is rearranged` |
| Representative cases | `A and C visit often but do not spend much` |
| Next verification | `Compare again with next month's revisit rate and long-term value` |

Even this level of memo greatly reduces `the mistake of attaching meaning from the number alone` and `the mistake of fixing one result as the truth`.

## Cases And Examples

### Case 1. Why Is It Risky To Use A Cluster Number Directly As A Customer Grade And Build A Coupon Policy?

Suppose a marketing team clusters customer data and then tries to send large discount coupons automatically only to `cluster 2`. But this number is only an identifier attached by the algorithm, and if the analysis is run again with a different feature choice or a different value of `k`, the same customers may receive different numbers. On top of that, if the current cluster has not yet been verified against actual churn risk or long-term value, the result may simply increase coupon cost while missing the truly important customers. So rather than using cluster results directly as policy rules, the safer path is to summarize each cluster's characteristics and compare them with follow-up outcome metrics through an explicit review step.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-2-mermaid-05-en.mmd"
```

If this case is compressed into a project memo, it can be written like this.

| Current cluster interpretation | Why it is risky to use immediately | Review items to write first | Next question |
| --- | --- | --- | --- |
| We want to read `cluster 2` as a premium-customer group | The number itself has no fixed meaning and can be rearranged under different settings | Cluster feature summary, scaling/parameter sensitivity, actual retention rate | Does this grouping remain in other data ranges too? |

### Case 2. Why Is It Risky To Spread A Cluster Directly Like The Correct Label In Article Classification With Few Labels?

Suppose a news-service team has not attached enough article labels yet, sees that similar articles gathered into one cluster, and decides `let's automatically label this whole cluster as economy articles`. At first glance it sounds efficient, but one cluster may still mix boundary documents such as `industry investment`, `semiconductor policy`, and `company earnings`. If the cluster is spread directly as if it were the correct label, a small interpretation error at the start can turn into a much larger label error.

In other words, a cluster can become `a tool that helps review label hypotheses faster`, but it is not a device that replaces the correct label itself without human review. A safer flow is to read representative articles and boundary documents first, narrow the possible label candidates, and only then reflect the result partially through an actual review process.

| What appeared first | What should not be done immediately | Safer next step |
| --- | --- | --- |
| Similar articles gathered into one cluster | Spread one correct label across the whole cluster | Review representative articles and boundary documents first |
| One cluster looks like economy articles | Finalize the cluster number immediately as the topic label | Also write alternative interpretations such as industry, policy, or earnings |

## Practice And Example

### Check With A Library: Clusters Can Change When Scale Changes

This example clusters the same customer data into two groups with `AgglomerativeClustering`, then compares the result before and after standardization.

- Values to change before running:
  - Change `n_clusters` from 2 to 3 and check which customer separates
  - Increase or decrease the `spend` values and check how much the raw-feature result changes
  - Remove and restore `StandardScaler` and compare the mean summary for each cluster

```python
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

customers = pd.DataFrame(
    [
        {"id": "A", "visits": 2, "spend": 20, "support": 1},
        {"id": "B", "visits": 3, "spend": 22, "support": 0},
        {"id": "C", "visits": 8, "spend": 85, "support": 4},
        {"id": "D", "visits": 9, "spend": 88, "support": 5},
        {"id": "E", "visits": 9, "spend": 28, "support": 6},
        {"id": "F", "visits": 10, "spend": 30, "support": 7},
    ]
)

features = customers[["visits", "spend", "support"]]


def summarize(labels):
    table = customers.assign(cluster=labels)
    summary = table.groupby("cluster")[["visits", "spend", "support"]].mean().round(1)
    members = table.groupby("cluster")["id"].apply(list)
    for cluster_id in sorted(summary.index):
        print(
            "cluster",
            int(cluster_id),
            "members=",
            members.loc[cluster_id],
            "mean=",
            summary.loc[cluster_id].to_dict(),
        )


raw_labels = AgglomerativeClustering(n_clusters=2).fit_predict(features)
scaled_labels = AgglomerativeClustering(n_clusters=2).fit_predict(
    StandardScaler().fit_transform(features)
)

print("raw features")
summarize(raw_labels)
print("scaled features")
summarize(scaled_labels)
```

The output is as follows.

```text
raw features
cluster 0 members= ['A', 'B', 'E', 'F'] mean= {'visits': 6.0, 'spend': 25.0, 'support': 3.5}
cluster 1 members= ['C', 'D'] mean= {'visits': 8.5, 'spend': 86.5, 'support': 4.5}
scaled features
cluster 0 members= ['C', 'D', 'E', 'F'] mean= {'visits': 9.0, 'spend': 57.8, 'support': 5.5}
cluster 1 members= ['A', 'B'] mean= {'visits': 2.5, 'spend': 21.0, 'support': 0.5}
```

With raw features, the `spend` axis dominates and C/D form their own group. After standardization, visits and support tickets are reflected more strongly, so C/D/E/F are grouped together. The point is not `which result is the truth`. The point is that clustering is sensitive to representation, so readers should record feature summaries and sensitivity checks before attaching meaning to cluster numbers.

### Why Is It Risky To Attach Meaning From The Number Alone?

This example is a small exercise showing that even if customers are divided into two clusters, the number itself does not automatically carry meaning. It directly checks the point that even if only the number changes, the interpretation sentence should remain the same.

- Problem situation: the algorithm created two groups, but meaning should not be attached from the number alone
- Input: customer-wise cluster IDs and observed values
- Expected output: a sense of separating numbers from meaning
- Concepts to check:
  - cluster IDs are identifiers, not grades
  - meaning is attached later through human review

First, look at the table below and write down for yourself what can be said only from the cluster numbers.

| Customer | cluster ID | Visits | Spend |
| --- | --- | --- | --- |
| A | 0 | 3 | 20 |
| B | 0 | 2 | 18 |
| C | 1 | 10 | 95 |
| D | 1 | 11 | 88 |

Then compare with the explanation below.

| What can be said immediately | What still cannot be said immediately | Why |
| --- | --- | --- |
| A and B were proposed as one group | `cluster 0 is a low grade` | The number itself has no grade meaning |
| C and D were proposed as another group | `cluster 1 is a premium customer group` | Meaning still needs feature summaries and business review |
| The two groups seem to differ in visits and spending | This difference directly becomes a policy rule | It is risky to move straight into policy without follow-up checks |

What should be read first from this example is the following.

1. The numbers 0 and 1 are only identifiers that distinguish groups.
2. Interpretations such as `cluster 1 is better` cannot be made until the actual meaning of the data is reviewed separately.
3. To attach meaning to clusters, feature summaries, business context, and additional verification are needed.

### Change One Value: The Interpretation Should Stay The Same Even If The Numbers Are Reversed

Now keep the same customer groups, but reverse only the cluster numbers.

| Customer | cluster ID | Visits | Spend |
| --- | --- | --- | --- |
| A | 1 | 3 | 20 |
| B | 1 | 2 | 18 |
| C | 0 | 10 | 95 |
| D | 0 | 11 | 88 |

First answer these questions for yourself.

- Does customer meaning change just because the numbers were reversed?
- What changed here: behavior or the identifier name?
- If you had to write a policy sentence, would you start with `cluster 0` or with an actual pattern such as `high-visit, high-spend group`?

Then compare with the explanation below.

| What changed | What did not change | Why this distinction matters |
| --- | --- | --- |
| The names of cluster IDs 0 and 1 | The actual behavior patterns of A/B and C/D | A cluster number is only an identifier, not the interpretation itself |
| The surface label notation | Which customers were grouped together | If the members stay the same, the number alone does not create a new meaning |
| The cluster number written in a document | The need to summarize the features of each group | Policy and explanation must start from pattern summaries, not from numbers |

Even though the numbers were reversed, the customer behavior did not change at all. This comparison lets you feel that when reading clustering results, you must not go directly from `number -> meaning`, but must go in the order `members -> feature summary -> business interpretation`. So even if a clustering result looks plausible, before turning it into a policy rule you should rewrite the actual pattern in words rather than relying on the number.

### What Should Be Read Together In This Example?

The goal of Part 4 is to build the judgment to separate what a model result means from what it does not yet mean, rather than consuming model results as if they were facts. This exercise lets the reader directly confirm that judgment through the smallest possible change: `a cluster number is only an identifier`. So the learner should train here to separate `what can be said immediately` from `what still needs follow-up verification` after seeing a clustering result. If that separation is missing, the whole text quickly collapses back into an overview.

| Shared recording language | What to record immediately in this example |
| --- | --- |
| What structure appeared | Even when cluster numbers changed, the actual customer behavior pattern stayed the same |
| Interpretation boundary | Numbers such as `cluster 0` and `cluster 1` do not carry rank or meaning on their own |
| Next question | If representative feature summaries and follow-up metrics are attached, what interpretation remains stable? |

## How Should Cluster Results Be Read Conservatively?

Cluster results should be read in the following question order.

1. Under what feature criteria was this cluster created?
2. Does a similar structure remain under different scaling or parameter choices?
3. What actual differences appear when each cluster is summarized?
4. Are those differences interpretable in the business context?
5. Before using it in policy, was it checked again with separate labels or follow-up analysis?

If we view this flow as a diagram, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-17/p4-17-2-mermaid-06-en.mmd"
```

The core is the last sentence.

`Use cluster results as hypotheses, not as final truths.`

When recording cluster results in a review memo, write them separately as `needs review`, `interpretation candidate`, and `next verification question`. The key is not to fix them immediately as a policy name or a cause name.

| Cluster result that first appeared | Interpretation boundary to attach immediately | Review question to check again |
| --- | --- | --- |
| A few clusters seem to divide plausibly | The visible grouping right now is not a correct category, but a proposal on top of a chosen representation and parameter setting | Does something similar remain under different features, scaling, and parameters? |
| A certain cluster looks like a risk group | Do not finalize policy meaning from the number and shape of the cluster alone | Does the same interpretation remain when connected to actual performance metrics or labels? |

| What should be read together | The question read first in this Section | Where it goes next |
| --- | --- | --- |
| Interpretation boundary | How far can the visible cluster be trusted, and where should judgment stop? | Part 4 summary, Part 6 retrospective notes |
| Representative review items | What cluster summaries, parameter sensitivity checks, and follow-up metrics should be viewed first? | Hypothesis review together with dimensionality reduction |
| Next verification question | What more is needed before moving to policy or meaning interpretation? | Label comparison and follow-up outcome analysis |

## Looking At 17.1 And 17.2 Together

If P4-17.1 explained `what kinds of groups can be found`, then P4-17.2 explains `how far those groups should be trusted`.

| Section | Central question |
| --- | --- |
| P4-17.1 | What kinds of structure can we try to find when labels do not exist? |
| P4-17.2 | How can we read the structure we found without overtrusting it? |

Both Sections must be understood together to use clustering safely in practice.

## Checklist

- Can you explain that clusters are not correct labels, but groupings proposed by the algorithm?
- Are you reading cluster IDs as if they were grades or fixed categories?
- Can you explain that cluster ID numbers themselves have no fixed meaning?
- Do you understand that clusters can change when feature choice, scaling, distance rule, or parameters change?
- Are you starting from the premise that results can also change when representation and parameters change?
- Do you understand the possibility of cluster instability, where clusters can be rearranged after changing feature representation or parameters?
- Do you know that clusters do not automatically explain causes?
- Do you understand that cluster results should be used as the starting point of further analysis, not as the final basis for policy?
- Before turning cluster results into policy, are you leaving human-review and follow-up verification steps in place?
- Do you know that follow-up metrics and label comparison are still needed before moving cluster results into causal explanations or automatic policy?

## Sources And References

- scikit-learn developers, `2.3. Clustering`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/clustering.html](https://scikit-learn.org/stable/modules/clustering.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Common pitfalls and recommended practices`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/common_pitfalls.html](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }
