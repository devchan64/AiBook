# P4-18.2 Visualization And Information Loss

> Section ID: `P4-18.2`
> Version: `v2026.07.26`

In P4-18.1, we saw that [dimensionality reduction](/AiBook/en/reference/concept-glossary-alpha/d/#dimensionality-reduction) reexpresses many [features](/AiBook/en/reference/concept-glossary-alpha/f/#feature) through fewer axes. The next step is to ask how far the resulting picture should be trusted.

If reducing dimensions makes the data easier to view as a picture, how far can that picture be trusted?

A two-dimensional or three-dimensional plot built through dimensionality reduction is useful for inspecting structure, but it does not preserve every relationship in the original high-dimensional data exactly as it was.

Visualization is a very strong tool, but it can also create very strong illusions.

This Section does not repeat the basic definition of dimensionality reduction at length. The core intuition `many features are reexpressed through fewer axes` reconnects through P4-18.1, and here the focus is on what kinds of [information loss](/AiBook/en/reference/concept-glossary-alpha/i/#information-loss) and interpretation risk that picture creates.

## Questions Closed By Visualization And Information Loss

This Section answers the following questions.

- Why is a dimensionality-reduction result easy to see but not a complete copy?
- What kinds of information are relatively well preserved, and what kinds may disappear?
- Why can two points that look close in 2D fail to be close in the original space?
- How should dimensionality-reduction results be used safely in exploratory analysis?
- When interpreting [t-SNE](/AiBook/en/reference/concept-glossary-alpha/t/#t-sne), [UMAP](/AiBook/en/reference/concept-glossary-alpha/u/#umap), [reconstruction error](/AiBook/en/reference/concept-glossary-alpha/r/#reconstruction-error), and [trustworthiness](/AiBook/en/reference/concept-glossary-alpha/t/#trustworthiness), what minimum ideas should be understood?

This Section focuses at an introductory level on `how far the reduced picture can be trusted` and `how information loss should be read`. So this Section directly covers what kinds of structure t-SNE and UMAP try to preserve more strongly, and how reconstruction error and trustworthiness should be read as minimum criteria. By contrast, implementation optimization, detailed tuning, and extended metric comparisons are not developed here at length.

## Judgments To Keep From Visualization And Information Loss

- You can explain that dimensionality-reduction [visualization](/AiBook/en/reference/concept-glossary-alpha/v/#visualization) is a tool for structure exploration.
- You can describe that reducing dimensions creates some information loss.
- You can understand that distances in a 2D picture can differ from distances in the original high-dimensional space.
- You can hold the attitude that visualization results should be read as the starting point of follow-up review rather than as a final conclusion.

## Judgment Flow For Visualization And Information Loss

This Section moves quickly because visualization interpretation, method comparison, and quality metrics appear together. On a first read, it helps to hold only the following four questions in order.

1. Why is a dimensionality-reduced picture easy to view but not a complete copy?
2. What do [PCA](/AiBook/en/reference/concept-glossary-alpha/p/#principal-component-analysis-pca), t-SNE, and UMAP each try to preserve more strongly?
3. How far should `points that look close` and `lumps that seem separate` be trusted?
4. In what direction do reconstruction error and trustworthiness recheck those risks?

Once this order is fixed first, interpretation questions and checking metrics are less likely to get mixed together.

## Why This Section Is Needed

After learning dimensionality reduction, readers often think like this.

- Now the data can be seen in 2D.
- The points look like they split into lumps.
- So the structure must have become clear.

That expectation is only half correct.

| What is true | What still requires caution |
| --- | --- |
| The large flow becomes easier to inspect at a glance | The original structure was not copied exactly |
| It becomes easier to find lump and outlier candidates quickly | Lump and distance interpretations can be exaggerated |
| It is very useful for explanation and presentation | Visual effect can create excessive confidence |

So P4-18.2 is the Section for learning not just `how to make a picture`, but `where to stop when reading one`.

## Why Does Reducing Dimensions Cause Information Loss?

As seen in P4-18.1, dimensionality reduction summarizes many axes into fewer axes. That immediately means all information cannot remain exactly as it was.

For example, when a 50-dimensional dataset is reduced to two dimensions:

- some large variations can be preserved
- some small differences or local relations can become weaker
- some directional information can merge or disappear

Dimensionality reduction is essentially close to compression.

Compression always involves a choice.

- What should be preserved first?
- What should be considered less important and reduced?

Because of that choice, information loss follows naturally.

The compression process always includes a choice about `what to keep and what to weaken`. Strong global patterns may stay, but small detailed relationships may become weaker or disappear.

If this point is read a little more practically, it looks like this.

| What we used to read in the original data | How it may change after reduction | What to recheck because of that |
| --- | --- | --- |
| Large overall directional differences | They may remain relatively well | Does that large flow also connect to a real business difference? |
| Ambiguous samples near a boundary | They may look more merged or more separated | What values were ambiguous in the original features? |
| Fine differences in minority samples | They may be buried during compression | Does a small group need to be reviewed separately again? |
| Small changes spread across many axes | They may be flattened into one or two axes | Which features became faint during summarization? |

## Easy To See Is Not The Same As Preserving The Original Structure

A 2D [scatter plot](/AiBook/en/reference/concept-glossary-alpha/s/#scatter-plot) can look neat, but that does not mean the original high-dimensional structure was copied directly onto a 2D plane.

The important distinction is the following.

- Easy to view: the state is easy for people to interpret
- Structure preservation: the original data relations remain sufficiently intact

These can overlap, but they are not always the same thing.

Visualization is `a human-friendly representation`, not automatically `a complete structural copy`.

## If Two Points Look Close, Were They Really Close Originally?

The most common misunderstanding is this.

`If two points look almost attached in a 2D plot, then they must also be almost the same in the original data.`

But in the process of reducing dimensions:

- points that were far apart originally can become close in the picture
- points that were close originally can move slightly apart in the picture

This is a natural distortion that comes from pressing high-dimensional structure into fewer axes.

If that feeling is viewed as a diagram, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-2-mermaid-02-en.mmd"
```

This diagram emphasizes that distance in a 2D plot is not always identical to distance in the original high-dimensional space. Two points that look close in the figure are not guaranteed to be close originally, and points that look farther apart may still be more similar in the original structure.

A difference can arise between visual distance and original distance.

For example, even if customers A and B look almost attached in a 2D figure, they may still be quite different in the original features as follows.

| Customer | Visit count | Purchase amount | Recency | Impression in the 2D plot |
| --- | --- | --- | --- | --- |
| A | High | High | Medium | Looks very close to B |
| B | High | Medium | High | Looks very close to A |

In the figure, both may look like `similar active customers`, but in the original features, A may be stronger on purchase size while B may be stronger on recency of activity. So if people are grouped under the same operational policy only because they look close in 2D, information loss has already turned into interpretation error.

## Why Do Different Methods Try To Preserve Different Things First?

Not every dimensionality-reduction method tries to make the same kind of picture. Some methods preserve large overall variation first, while others put more weight on nearby-neighbor structure.

| The question asked first | The closer method | What a beginner should read first |
| --- | --- | --- |
| Do we want to preserve large global variation as much as possible? | PCA | It keeps large-variance directions first |
| Do we want to see nonlinear structure or nearby-neighbor relations more strongly? | t-SNE, UMAP | They are more sensitive to local-neighborhood structure than to the whole layout |

This distinction should be fixed first so that later quality metrics are not mistaken for answers to the same question.

## What Do t-SNE And UMAP Try To Preserve More Strongly?

Not every method works like PCA by preserving large-variance directions. In visualization, t-SNE and UMAP are often mentioned because they lean more toward preserving local-neighborhood relations.

| Method | Introductory core to hold | What often appears in the picture because of that |
| --- | --- | --- |
| PCA | Preserves large global variation first | Overall direction and spread are easy to read, but local groups may be weaker |
| t-SNE | Tries to make nearby-neighbor relations in the original space appear similarly in low dimensions | Local lumps can look very clear, but distances between lumps must be read carefully |
| UMAP | Tries to preserve local-neighbor graph structure in low dimensions as well | It often shows local structure well while making the overall layout somewhat easier to read |

t-SNE can be summarized very briefly like this.

- It computes something like probabilities for `who is a close neighbor of whom` in the original high-dimensional space
- It then adjusts low-dimensional point positions so that similar neighbor relations appear there too
- So it has a strong force that `makes nearby points appear together`

UMAP can be summarized very briefly like this.

- It builds a neighborhood graph in the original space
- It arranges points so that the graph relation is preserved in lower dimensions as much as possible
- So it tends to `preserve local neighborhood structure while also trying to keep the whole picture readable`

If this difference is compressed into interpretation sentences, it looks like this.

| Question to ask first when looking at the picture | What to be especially careful about in t-SNE and UMAP |
| --- | --- |
| How much can we trust closeness inside the same lump? | Local neighborhood structure is often useful as a hint, but still not perfectly preserved |
| How much can we trust the distance between one lump and another? | It can be exaggerated or compressed depending on the method and parameters, so caution is even more important |
| Is the number of lumps itself the true structure? | Visual separation may hint at structure, but it still cannot be finalized immediately |

So t-SNE and UMAP are not `tools for making pretty pictures`. They are better read as `tools for trying to move neighborhood relations from the original space into low dimensions somehow`. That is why they are stronger for `local-structure hints`, but require more caution in reading `global distance` and `absolute separation`.

## What Does Reconstruction Error Calculate?

If we already saw that `some methods preserve large global variation more strongly while others preserve local structure more strongly`, then it is better not to read every quality metric as asking the same question.

| Checking question | The closer metric |
| --- | --- |
| How well can the reduced representation rebuild the original information? | reconstruction error |
| How much can we trust the neighborhood relations that look close in the low-dimensional plot? | trustworthiness |

In other words, reconstruction error belongs to the `rebuilding` question, while trustworthiness belongs to the `preservation of nearby relations` question.

When people want to read information loss numerically, one concept that often appears is reconstruction error. Its meaning is simple.

`If dimensions are reduced and then the data are reconstructed back into the original dimension, how different does the reconstructed data become from the original data?`

Its most basic form is usually written like this.

\[ \text{Reconstruction Error} = \frac{1}{n}\sum_{i=1}^{n}\lVert x_i - \hat{x}_i \rVert^2 \]

Here:

- \(x_i\): original data
- \(\hat{x}_i\): data reconstructed after reduction
- \(\lVert x_i - \hat{x}_i \rVert^2\): squared difference between the original and the reconstructed value

So this can be read as averaging `how different the original and reconstructed values are` for each sample.

This formula is especially natural in methods like PCA, where reduction is followed by a reconstruction step.

| Reconstruction error is small | Reconstruction error is large |
| --- | --- |
| Even the reduced axes can rebuild the original information relatively well | More information was lost during the reduction process |
| There is a good chance the large structure was preserved | Important differences may have been flattened heavily |

But even here, immediate overinterpretation is not safe.

| What should also be remembered | Why |
| --- | --- |
| A small reconstruction error does not automatically mean the visualization is easy to interpret | Rebuilding may work well while the 2D picture still distorts lump shapes |
| The same style of reconstruction error cannot be attached directly to t-SNE or UMAP | Because those methods are closer to `preserving neighborhood structure` than to `rebuilding` in the first place |

So reconstruction error is a metric for `how much of the original information can be rebuilt`, not a direct metric for `how convincing the picture looks`.

## What Does Trustworthiness Ask?

Among visualization quality metrics, trustworthiness asks, just as its name suggests, `how much can we trust the neighborhood relations in this low-dimensional figure?` Put very briefly, it asks the following.

`If some points newly appear as close neighbors in the low-dimensional picture, were they really close in the original high-dimensional space too?`

The formula is written like this.

\[ T(k) = 1 - \frac{2}{nk(2n - 3k - 1)} \sum_{i=1}^{n}\sum_{j \in U_k(i)}(r(i,j)-k) \]

Here:

- \(n\): number of samples
- \(k\): how many nearest neighbors are being checked
- \(U_k(i)\): points that appear as close neighbors in low dimensions but were not among the top \(k\) neighbors in the original space
- \(r(i,j)\): the neighbor rank of point \(j\) for point \(i\) in the original high-dimensional space

If this formula is translated into words, it becomes:

- find points that suddenly look close in the low-dimensional figure
- penalize them based on how far away they really were in the original space
- the smaller those penalties are, the higher trustworthiness becomes

So trustworthiness can be read like this.

| Trustworthiness is high | Trustworthiness is low |
| --- | --- |
| The nearby-neighbor relations in the low-dimensional figure match the original space relatively well | There are more relations that look close in the figure even though they were far apart originally |
| You can trust interpretations of `points that look attached` a bit more | You must be more cautious with `they look attached, so they must be similar` |

This metric is not all-powerful either.

| What the metric directly tells us | What it does not directly tell us |
| --- | --- |
| How well nearby-neighbor relations are preserved | Whether distances between whole groups are correctly interpreted |
| Whether many false close neighbors were newly created in low dimensions | How persuasive the plot looks in a presentation |

So trustworthiness acts as a brake that asks again `how much should we trust proximity in this picture?` The official scikit-learn documentation also describes it as a value that asks how much local structure was retained. After looking at a reduced plot, when people start wanting to group `points that look attached` too quickly into the same type, this is exactly the question that trustworthiness throws back at them.

## Safe Reading Order

To reduce visual illusion, dimensionality-reduction results should be read in the following order.

1. First inspect the large flow and lumps.
2. Check what original features those lumps connect to.
3. Check whether similar patterns appear under other axis counts or other methods.
4. If needed, recheck through reconstruction error, trustworthiness, and comparison with the original features.

If this order is compressed into a flow, it looks like the following.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-2-mermaid-03-en.mmd"
```

The key sentence of this Section is the last one.

`A dimensionality-reduction plot can help generate hypotheses, but it cannot prove those hypotheses by itself.`

## Cases And Examples

### Case 1. Why Is It Risky To Conclude Immediately That Two Product Groups Are Really Different Just Because They Look Far Apart In A 2D Plot?

Suppose a product-planning team reduces dozens of product features into a 2D plot and sees two point clouds far apart. Looking only at the figure, they may seem like `completely different product families`, but in the original features, price range and core functions may still be quite similar while some auxiliary features only became more visible during projection. Conversely, products that look slightly overlapped in the figure may still be well separated in the original high-dimensional space. So a reduced plot is useful for building a separation hypothesis, but final judgment must be rechecked through summaries of original features and follow-up analysis.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-2-mermaid-05-en.mmd"
```

If this scene is left as an interpretation memo, it can be organized like this.

| Structure seen first in the picture | Interpretation boundary to attach immediately | Review question to check again |
| --- | --- | --- |
| Two point clouds look far apart | Do not conclude from 2D distance alone that the original features are fully different | Does the same split appear when original features are summarized? |
| Some points look overlapped | They may look more mixed than they really are because of projection | Do they overlap similarly under other axis counts or other methods too? |

So the core of the visualization Section is to keep together `visible structure -> interpretation boundary -> next verification question`. Even when figures look similar on the surface, some visible structures are confirmed again in the original features while others weaken as projection illusion, so review memos need to keep those paths separate.

### Case 2. Why Is It Risky To Remove One Far-Away Point Immediately Just Because It Sticks Out?

Suppose a data-analysis team reduces operating logs and notices one point far away from the main point cloud. The figure alone can make it feel like `one abnormal log`, but in the original features that point may instead represent normal traffic right after a deployment or a temporary spike caused by a specific campaign. Of course it could still be a real problematic log, so the important thing is not only the fact that `it looks far away`, but also asking again `why does it look far away?`

| Signal seen first in the picture | Misunderstanding that is easy to jump to | What to recheck first |
| --- | --- | --- |
| One point sticks out unusually far | It must be an outlier and should be removed immediately | Original log features, time window, deployment history |
| A small group appears separately | It must be an error-user group | Whether a real common property exists, and whether the same split appears under other axis counts |

This case shows that a dimensionality-reduction plot is useful for finding outlier candidates, but the removal decision should be made only after going back to original features and time context.

## Practice And Example

This example reduces five features to 2D with PCA and checks how nearby neighbors can differ between the original space and the 2D space.

- Problem situation: check whether a nearby product candidate in a 2D plot should also be read as nearby in the original features
- Input: product candidates expressed through five score features
- Expected output: variance ratio retained by PCA, nearby neighbors in the original space, and nearby neighbors in the 2D space
- Concepts to check:
  - a 2D reduced representation is not a copy of the original space
  - nearby-neighbor order can change before and after reduction
  - a reduced plot is the starting point for follow-up review, not the conclusion

```python
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

items = pd.DataFrame(
    [
        {"id": "A", "price_score": 2, "battery": 7, "camera": 5, "service": 10, "design": 8},
        {"id": "B", "price_score": 3, "battery": 9, "camera": 8, "service": 3, "design": 6},
        {"id": "C", "price_score": 8, "battery": 3, "camera": 3, "service": 2, "design": 1},
        {"id": "D", "price_score": 5, "battery": 1, "camera": 6, "service": 5, "design": 2},
        {"id": "E", "price_score": 4, "battery": 1, "camera": 2, "service": 5, "design": 1},
        {"id": "Q", "price_score": 8, "battery": 3, "camera": 10, "service": 2, "design": 7},
    ]
)

features = ["price_score", "battery", "camera", "service", "design"]
X_scaled = StandardScaler().fit_transform(items[features])

pca = PCA(n_components=2, random_state=0)
points_2d = pca.fit_transform(X_scaled)

raw_distances = pairwise_distances(X_scaled)
reduced_distances = pairwise_distances(points_2d)
q_index = items.index[items["id"] == "Q"][0]


def nearest_ids(distance_matrix):
    order = distance_matrix[q_index].argsort()[1:4]
    return items.iloc[order]["id"].tolist()


print("explained_variance=", [round(float(v), 3) for v in pca.explained_variance_ratio_])
print("nearest_in_original=", nearest_ids(raw_distances))
print("nearest_in_2d=", nearest_ids(reduced_distances))

for item_id, point in zip(items["id"], points_2d):
    print(item_id, "2d=", [round(float(value), 2) for value in point])
```

The output is as follows.

```text
explained_variance= [0.505, 0.348]
nearest_in_original= ['D', 'B', 'C']
nearest_in_2d= ['B', 'D', 'C']
A 2d= [2.55, -1.23]
B 2d= [1.63, 0.87]
C 2d= [-1.96, 0.04]
D 2d= [-0.83, -0.38]
E 2d= [-1.19, -1.62]
Q 2d= [-0.19, 2.32]
```

There are three things to read from this example.

1. Even when the first two PCA axes retain a large part of the overall variance, they do not preserve the original space completely.
2. In the original space, the nearest candidate to Q is D, but in the 2D space B appears first.
3. Therefore, when a candidate looks close in a 2D plot, readers still need to recheck the original feature distance and the actual feature values.

The visualization-review memo for this scene can be written as follows.

| Common record language | What to write for this exercise |
| --- | --- |
| Structure seen first | In the 2D PCA space, Q appeared closest to B |
| Interpretation boundary | In the original feature space, Q's nearest candidate was D, so do not treat 2D distance as original distance |
| Next question | Should we place the original feature values of Q, B, and D side by side and recheck which axes were compressed by the projection? |

## Checklist

- Do you understand that a dimensionality-reduction plot is useful for exploring structure and for explanation, but that an easy-to-view figure does not automatically mean preserved structure?
- Are you reading distance in a 2D figure as if it were the same as distance in the original high-dimensional space?
- Can you explain that PCA preserves large overall variation first, while t-SNE and UMAP place more weight on nearby-neighbor structure?
- Are you passing visible lumps or outlier candidates directly into policy judgment without follow-up review?
- Can you explain that reconstruction error asks `how much can be rebuilt`, while trustworthiness asks `how much can we trust nearby-neighbor relations`?
- Are you distinguishing whether the current check you need is `rebuildability` or `preservation of nearby relations`?
- Are you reading a dimensionality-reduction plot as the starting point of follow-up review rather than as a final conclusion?
- Are you prepared to recheck the visible structure through original features, other methods, or other axis counts?

## Sources And References

- scikit-learn developers, `2.5. Decomposing signals in components (matrix factorization problems)`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/decomposition.html](https://scikit-learn.org/stable/modules/decomposition.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `PCA`, scikit-learn API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `TSNE`, scikit-learn API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `trustworthiness`, scikit-learn API Reference, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.manifold.trustworthiness.html](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.trustworthiness.html){: target="_blank" rel="noopener noreferrer" }
- UMAP Project, `How UMAP Works`, UMAP documentation, accessed 2026-07-26. [https://umap-learn.readthedocs.io/en/latest/how_umap_works.html](https://umap-learn.readthedocs.io/en/latest/how_umap_works.html){: target="_blank" rel="noopener noreferrer" }
