# P1-8.2 Unsupervised Learning: Structure and Representation

> Section ID: `P1-8.2`
> Version: `v2026.07.17`

Section 8.1 explained a `label` as a distinguishing marker attached to data. Supervised learning tries to match the relationship between inputs and outputs using examples where inputs and labels are given together.

This section starts from the opposite side. `Unsupervised learning` is a learning method that tries to find structure, clusters, or representations inside data without labels attached in advance by people.

The central question is:

> when there are no labels,  
> what is the model trying to find inside the data?

> unsupervised learning is not learning without any standard at all; it is learning to find structure inside data without human-provided labels

This section organizes `unsupervised learning`, `structure`, `clustering`, `dimensionality reduction`, and `cluster labels` under one viewpoint: learning from unlabeled data by finding structure. The baseline sense of `label` and supervised learning was fixed in 8.1, and the baseline sense of `representation` was introduced earlier in 3.3 and 4.3.

## Scope of This Section

This section does not calculate specific unsupervised-learning algorithms. K-means, hierarchical clustering, PCA, t-SNE, and autoencoders pass by only as names and roles.

It also does not go deeply into distance functions, the curse of dimensionality, cluster-evaluation metrics, or manifold learning. Those return later in Part 4, and some details remain outside the main scope of this book.

This section also does not redefine labels at length. Their basic distinction was already fixed in 8.1. Here the focus is narrower:

> if there are no labels,  
> what becomes the standard of learning?

The working definition here is:

> unsupervised learning is a method that finds structure, clusters, or representations inside data without labels attached by people

## Goal of This Section

- Explain unsupervised learning as learning that finds structure in unlabeled data.
- Understand that `no labels` does not mean `no goal` or `no standard`.
- Distinguish clustering from dimensionality reduction at an introductory level.
- Avoid confusing `cluster labels` with human-attached labels.
- Avoid mixing unsupervised learning with supervised learning, reinforcement learning, or deep learning as if they were one category.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| unsupervised learning tries to find structure inside data without labels | This is the most basic distinction from supervised learning. | It is enough to understand that the model looks for similarity, grouping, or hidden axes without human answer tags. |
| the result does not come with automatic meaning; people still have to interpret it | This reduces the mistake of reading clusters or reduced dimensions as truth by themselves. | Even if the model makes groups, people still have to decide what those groups mean. |
| clustering, dimensionality reduction, and similar tasks ask different questions | This prevents `unsupervised learning` from being treated as one single technique. | It is enough to distinguish `what is similar?`, `how can we reduce dimensions?`, and `where is structure dense?` |

A short role separation is useful:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| unsupervised learning | learning without labels by finding structure | the second baseline of Chapter 8 |
| structure | relationships and patterns inside data | the central concept of what is being sought |
| clustering | grouping similar things together | one representative unsupervised-learning problem |
| dimensionality reduction | looking at many dimensions through fewer ones | another representative problem that makes structure easier to see |
| representation | the form in which data appears inside the model | the angle through which structure becomes visible |
| cluster label | a group number or marker produced by the algorithm | something that must be kept separate from human-provided supervised labels |

## No Labels Does Not Mean No Goal

When people hear `unsupervised`, they sometimes imagine that no guidance exists at all. The more accurate point is narrower: there are no labels attached in advance by people.

> there are no human-provided labels in advance  
> but there is still a goal: find structure in the data

Google’s Machine Learning Glossary explains unsupervised learning as training a model to find patterns in unlabeled examples. If supervised learning fits outputs to given labels, unsupervised learning looks at the arrangement and relationships of the data itself without such labels.

Suppose we have customer-support sentences like these:

| Support sentence | Human-provided label |
| --- | --- |
| `I want a refund.` | none |
| `When will the delivery arrive?` | none |
| `The item arrived broken.` | none |
| `Can I cancel the order?` | none |
| `I want to change the address.` | none |

No labels such as `delivery`, `refund`, or `exchange` are attached. But similarities may still exist among the sentences. Unsupervised learning tries to find that kind of similarity, repeated pattern, or hidden axis.

## Structure Means Relationships Inside Data

In unsupervised learning, `structure` means that data is not just scattered randomly. It has some relationship or pattern inside it.

Examples:

| Data | Structure that might be found |
| --- | --- |
| customer purchase history | groups of customers with similar buying tendencies |
| product browsing records | products frequently viewed together |
| support sentences | groups of sentences with similar intent |
| server logs | request patterns that differ from normal behavior |
| image features | groups of visually similar shapes or textures |

The key point is that nobody labeled these in advance as `group A` or `delivery inquiry`. The algorithm tries to find structure through distances, similarities, densities, or variances in the data.

> supervised learning fits to labels  
> unsupervised learning looks for structure without labels

## Clustering Groups Similar Things Together

`Clustering` is one of the most representative examples of unsupervised learning. scikit-learn explains that unlabeled data can be clustered through `sklearn.cluster`.

Clustering in the AI sense is not just a person manually sorting items by intuition. A person can, of course, create groups manually in statistics or business work. But in machine learning, clustering is closer to a procedure that represents data numerically through features and then groups it using calculable criteria such as distance, similarity, density, or variance.

| Distinction | Human manual grouping | Algorithm-based clustering |
| --- | --- | --- |
| basis | human reading, business experience, prior knowledge | chosen features, distance, similarity, density, variance |
| result | a human-assigned business group or category name | cluster number, centroid, or grouping structure |
| strength | easy to reflect context and intention directly | easier to inspect large data with a consistent calculable standard |
| caution | standards may differ between people | the grouping may not match business meaning directly |

So clustering is not `the machine automatically understands the true categories`. It is closer to `the system groups things that look similar under the chosen representation and criteria`.

For example, K-means divides data into a chosen number of clusters and repeatedly assigns each point to the nearest centroid. Stanford CS229 notes describe it as creating cohesive clusters from unlabeled data.

| Input data | What clustering tries to find |
| --- | --- |
| customer purchase history | groups of customers with similar patterns |
| news articles | groups of articles with similar themes |
| sentence embeddings | groups of sentences with similar meaning |
| image features | groups of visually similar images |
| sensor records | groups of similar operating states |

The important question is always:

> by what notion of similarity are we saying these belong together?

The answer can change with the chosen features. Even with the same data, the grouping may change depending on what we compare.

| Situation | Features we might compare | Possible clusters | Caution |
| --- | --- | --- | --- |
| shopping-mall customers | purchase frequency, average order amount, revisit interval | frequent buyers, occasional high spenders, window shoppers | names such as `VIP` or `churn risk` are later human interpretations |
| support messages | sentence embeddings, frequent terms, message length | delivery-like messages, refund-like messages, defect-like messages | clusters may not match business departments exactly |
| news articles | title and body embeddings, named people, places, topic terms | political articles, economic articles, sports articles | articles about the same event may mix with articles about the same topic |
| product images | color, shape, texture, feature vectors | products with similar color tone, form, or shooting angle | the result may differ from the category people expect |
| server logs | request time, status code, latency, route path | normal request patterns, slow request patterns, error-heavy patterns | these are anomaly candidates, not the root-cause analysis itself |

Using support-message embeddings as an example:

| Cluster | Possible included sentences |
| --- | --- |
| cluster 1 | `When will delivery happen?`, `My order still has not arrived.` |
| cluster 2 | `I want a refund.`, `Can I cancel the payment?` |
| cluster 3 | `The item arrived broken.`, `Can I exchange it?` |

The algorithm did not start with the labels `delivery`, `refund`, or `exchange`. It grouped the sentences first by similarity. A human may then look at the group and say, `this cluster seems close to delivery inquiries`.

That is why a `cluster label` such as `cluster 1` is not the same thing as the label discussed in supervised learning.

> a cluster label is a grouping marker created by the algorithm  
> it is not the same as a human-attached supervised-learning label

## Dimensionality Reduction Views Complex Data Through Fewer Axes

Unsupervised learning is not only about grouping. It is also used to look at complex data through fewer axes. This is called `dimensionality reduction`.

Here, a `dimension` can be thought of as one descriptive axis of the data. An image may have many pixel-related dimensions, a document may have many token or embedding dimensions, and customer data may have many behavioral variables.

Dimensionality reduction tries to view that high-dimensional data through fewer dimensions while preserving important structure as much as possible.

| Data | What dimensionality reduction can help with |
| --- | --- |
| high-dimensional image features | seeing whether similar images lie near each other |
| sentence embeddings | observing groups of semantically similar sentences |
| customer behavior data | finding major behavioral axes for visualization |
| sensor data | inspecting normal patterns versus unusual ones |

scikit-learn’s explanation of PCA describes it as decomposing multivariate data into orthogonal components that explain variance. At the introductory level, the key point is simpler:

> dimensionality reduction means viewing complex data again through fewer axes  
> while trying to preserve important structure

## Representation Is the Form in Which Data Appears to the Model

The word `representation` also matters here. Representation is the form into which original data is transformed so that the model or algorithm can handle it more easily.

For example, sentences are difficult to compute over as raw language. When turned into numeric vectors, distances or similarities between sentences can be calculated. Images are arrays of pixels, but inside models they may appear through features related to shape, color, boundary, or texture.

In unsupervised learning, the model may be used not to fit labels, but to find or build representations that make data structure visible.

| Original data | Example representation |
| --- | --- |
| support sentences | sentence embeddings |
| product images | image feature vectors |
| customer behavior logs | behavioral-pattern vectors |
| document collections | lower-dimensional topic-related representations |

Unsupervised learning can also connect to making structure visible by changing the representation without labels. Later chapters connect that more directly to deep learning and embeddings.

## Unsupervised-Learning Results Need Interpretation

Because no labels are attached in advance, it is risky to read unsupervised-learning results directly as business truth.

Suppose a clustering result looks like this:

| Cluster | Included customers |
| --- | --- |
| cluster 1 | high purchase amount, high visit frequency |
| cluster 2 | many visits but low purchasing |
| cluster 3 | purchases only in a particular season |

It would be too quick to declare these immediately as `VIP`, `churn-risk`, or `seasonal customer`. Those names are interpretation added later by people. Unsupervised learning can reveal candidate structure, but the business meaning of that structure still has to be examined.

Useful questions include:

> by what criteria was this structure created?  
> would a different distance function or variable choice change it?  
> is the result interpretable in business terms?  
> is the human name attached to it an over-interpretation?

## The Boundary from Other Learning Types

Chapter 8 separates three basic learning types. Summarized again:

| Learning type | Data and signal | Central question | Place in this chapter |
| --- | --- | --- | --- |
| supervised learning | inputs and labels | what label should be predicted from this input? | 8.1 |
| unsupervised learning | unlabeled data | what structure exists inside the data? | 8.2 |
| reinforcement learning | states, actions, rewards | which actions increase reward over time? | 8.3 |

`Deep learning` is not on the same axis as this table. It can be used inside unsupervised learning, but it is not identical to unsupervised learning itself.

## Checklist

- Explain unsupervised learning as a way of finding structure in unlabeled data.
- Explain why `no labels` does not mean `no goal`.
- Explain clustering as a way of grouping similar things together.
- Explain dimensionality reduction as a way of looking again at complex data through fewer axes.
- Distinguish a cluster label from a human-attached supervised label.
- Explain why unsupervised-learning results still require human interpretation and review.
- Explain that `what counts as similar`, `what structure we are trying to find`, and `who interprets the result` should be separated.
- Explain why cluster numbers or reduced coordinates should not be read directly as business meaning or truth.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- scikit-learn, [Clustering](https://scikit-learn.org/stable/modules/clustering.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- scikit-learn, [PCA](https://scikit-learn.org/stable/modules/decomposition.html#pca){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- Stanford CS229, [Unsupervised Learning](https://cs229.stanford.edu/notes2022fall/cs229-notes7a.pdf){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
