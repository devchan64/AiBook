# P4-18.2 Visualization And Information Loss

> Section ID: `P4-18.2`
> Version: `v2026.07.11`

In P4-18.1, we saw that dimensionality reduction reexpresses many features through fewer axes. The next step is to ask how far the resulting picture should be trusted.

If reducing dimensions makes the data easier to view as a picture, how far can that picture be trusted?

A two-dimensional or three-dimensional plot built through dimensionality reduction is useful for inspecting structure, but it does not preserve every relationship in the original high-dimensional data exactly as it was.

Visualization is a very strong tool, but it can also create very strong illusions.

This Section does not repeat the basic definition of dimensionality reduction at length. The core intuition `many features are reexpressed through fewer axes` reconnects through P4-18.1 and the [concept glossary](../../../reference/concept-glossary.md), and here the focus is only on what kinds of information loss and interpretation risk that picture creates.

## Scope Of This Section

This Section answers the following questions.

- Why is a dimensionality-reduction result easy to see but not a complete copy?
- What kinds of information are relatively well preserved, and what kinds may disappear?
- Why can two points that look close in 2D fail to be close in the original space?
- How should dimensionality-reduction results be used safely in exploratory analysis?
- When interpreting t-SNE, UMAP, reconstruction error, and trustworthiness, what minimum ideas should be understood?

This Section focuses at an introductory level on `how far the reduced picture can be trusted` and `how information loss should be read`. So this Section directly covers what kinds of structure t-SNE and UMAP try to preserve more strongly, and how reconstruction error and trustworthiness should be read as minimum criteria. By contrast, implementation optimization, detailed tuning, and extended metric comparisons are not developed here at length.

## Goals Of This Section

- You can explain that dimensionality-reduction visualization is a tool for structure exploration.
- You can describe that reducing dimensions creates some information loss.
- You can understand that distances in a 2D picture can differ from distances in the original high-dimensional space.
- You can hold the attitude that visualization results should be read as the starting point of follow-up review rather than as a final conclusion.

## Reading Order For This Section

This Section moves quickly because `risks in interpreting the picture`, `what each method preserves`, and `quality metrics` all appear together. On a first read, it helps to hold on to only the following four questions in order.

1. Why is a dimensionality-reduced picture easy to view but not a complete copy?
2. What do PCA, t-SNE, and UMAP each try to preserve more strongly?
3. Then how far should we trust `points that look close` and `structures that look like lumps`?
4. In what direction do reconstruction error and trustworthiness recheck those risks?

Once this order is fixed, it becomes less confusing to distinguish what is an interpretation question and what is a checking tool, even when method names, formulas, and visual effects are mixed together.

## Why This Section Is Needed

After learning dimensionality reduction, people often form expectations like these.

- Now the data can be seen in two dimensions
- The points seem to split into groups
- So the structure feels clearer

That expectation is only half correct.

| What is true | What still requires caution |
| --- | --- |
| A picture makes structure easier to inspect | The picture does not preserve the original structure completely |
| It is good for exploring lumps and patterns | Lumps can be exaggerated or compressed |
| It is useful in explanation and presentation | Visual effect can create too much confidence |

So P4-18.2 is the Section for learning `how to read a picture`.

### When Should Interpretation Of A Visualization Be Stopped And Rechecked?

The prettier and clearer the dimensionality-reduction plot looks, the faster you should check `am I confusing easy viewing with structure preservation?`

| What appears in the picture | Why you should stop first | What to check together |
| --- | --- | --- |
| Two points look extremely close in 2D | Because that does not guarantee the same closeness in the original high-dimensional space | The relation inside the original feature space |
| A lump looks very clear and you want to read it immediately as a cluster | Because the projection may have exaggerated the grouping | Whether a similar pattern appears under other parameters or methods |
| You want to remove one distant point immediately as an outlier | Because the compression process may have distorted it | The original data and other validation methods |
| A presentation plot looks too convincing | Because visual effect can create excessive confidence | Separate exploratory result from finalized conclusion |
| You want to go straight from a 2D figure to policy judgment | Because visualization is an exploration tool, not a final decision tool | Follow-up labels, outcomes, and original-feature comparison |

The purpose of this table is not to make visualization untrustworthy. It is to stop first at the point `where something easy to see starts changing into excessive confidence`.

If this tension is compressed into a diagram, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-2-mermaid-01-en.mmd"
```

This diagram shows the strengths and limits of a dimensionality-reduction plot at once. Reducing dimensions makes the structure much easier for people to see, but that ease always arrives together with some distortion or loss.

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

A 2D scatter plot can look neat, but that does not mean the original high-dimensional structure was copied directly onto a 2D plane.

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

## What Is Preserved Relatively Well, And What Can Become Weaker?

Methods such as PCA try to preserve directions that explain large variance first. That usually creates the following tendency.

| What may be preserved relatively well | What may become weaker |
| --- | --- |
| Large global trends | Small detailed differences |
| Major directions of variation | Local patterns on less important axes |
| Overall spread structure | Fine relations among exceptional minority samples |

Dimensionality reduction usually helps with `the big picture`, but fine-grained judgment still requires caution.

### Why Do Different Methods Try To Preserve Different Things First?

From here on, the important distinction is `do all dimensionality-reduction methods make the same kind of picture?` Even in the official documentation, PCA is more strongly tied to explained variance, while manifold-learning families are more strongly tied to nonlinear structure and local neighborhoods.

| The question asked first | The closer method | What a beginner should read first |
| --- | --- | --- |
| Do we want to preserve large global variation as much as possible? | PCA | It builds summary axes while keeping large-variance directions first |
| Do we want to see nonlinear structure or nearby-neighbor relations more strongly? | t-SNE, UMAP, and other manifold families | They are more sensitive to preserving local structure than to preserving the whole layout |

This distinction needs to be fixed first so that reconstruction error and trustworthiness are later read as answers to different questions.

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

\[
\text{Reconstruction Error} = \frac{1}{n}\sum_{i=1}^{n}\lVert x_i - \hat{x}_i \rVert^2
\]

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

\[
T(k) = 1 - \frac{2}{nk(2n - 3k - 1)}
\sum_{i=1}^{n}\sum_{j \in U_k(i)}(r(i,j)-k)
\]

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

## If It Looks Like A Cluster, Is It Really A Cluster?

When looking at a reduced plot, several groups of points may appear like separate lumps. But there are two possibilities.

1. The original high-dimensional data really contain some grouping structure
2. The projection process made it look like a group

A cluster in the picture can be `a hint of real structure`, but it is not sufficient evidence by itself.

If we connect back to the clustering discussion in Chapter 17, a dimensionality-reduced plot can suggest a clustering hypothesis, but it does not finalize that hypothesis.

The visual illusions that often appear here look like the following.

| What is seen first in the picture | What might really be going on | What to do immediately next |
| --- | --- | --- |
| Two lumps look clearly separated | The projection may have made the split appear stronger than it is | Check whether the same split appears in original-feature summaries and under other axis counts |
| One point sticks out far away | It may be a real outlier, or only projection distortion | Look together at the original data, other visualizations, and other outlier criteria |
| Several points seem tightly compressed into one place | Differences that existed across several axes may have been pressed flat | Recheck the original feature distribution before summarization |

## What Is Visualization Most Useful For?

Dimensionality-reduction plots are usually very useful for the following purposes.

| Use | Why it is useful |
| --- | --- |
| Seeing the overall data flow | It reveals large groups, spread, and direction at a glance |
| Exploring outliers | It makes unusually distant points easy to notice |
| Building clustering hypotheses | It allows exploratory inspection of how many groups seem to appear |
| Explanation and communication | It shares complicated high-dimensional data more intuitively |

So visualization is very useful for `exploration and explanation`.

If that usefulness is organized more concretely, it looks like this.

| Scene where visualization helps especially well | Why it helps | Why you should not stop there |
| --- | --- | --- |
| First pass over the overall flow of the data | Because large structure can be captured quickly | Because large structure is not automatically a final conclusion |
| Building a follow-up clustering hypothesis | Because it shows exploratorily what looks like a few lumps | Because visible lumps may still be projection illusions |
| Choosing representative cases | Because it becomes easy to see what is central, boundary-like, or peripheral | Because case interpretation can be exaggerated if original features are not inspected together |
| Preparing explanation material | Because complicated high-dimensional structure can be shared more intuitively | Because a presentation figure can create stronger confidence than the evidence supports |

## But What Should It Not Be Used For Immediately?

It is risky to make judgments like the following from one picture alone.

- These two points are almost the same customer
- This lump must be a separate product family
- This point is an outlier, so let us remove it immediately
- This cluster is a risk group, so let us apply a different policy

That is because the picture is a compressed representation of the structure, not a complete judgment of the original relation.

So a dimensionality-reduction plot should be read as `an exploration tool`, not as `a finalization tool`. Even structures that look strong in the picture are better left first as signals that need review, and should not be turned immediately into policy or causal statements before comparison with original features and other methods.

In other words, dimensionality-reduction visualization is strong for finding patterns and for explanation, but one plot alone cannot replace a final conclusion or proof.

## Safe Reading Order

To reduce visual illusion, dimensionality-reduction results should be read in the following order.

1. First inspect the large flow and lumps.
2. Check what original features those lumps connect to.
3. Check whether similar patterns appear under other parameters or other methods.
4. If necessary, go back to the original high-dimensional data or downstream model performance for confirmation.

If this is drawn as a flow, it looks like the following.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-2-mermaid-03-en.mmd"
```

This diagram organizes the safe interpretation order. Even after a pattern is found in the plot, the reader must go back to original features, confirm whether similar behavior appears under other methods, and only then use the pattern at the level of a hypothesis.

The core of this Section is the last step.

`A dimensionality-reduced plot helps generate a hypothesis, but it cannot prove that hypothesis on its own.`

If the judgment so far is regrouped into one table, the safest way to read it is the following.

| What you are trying to inspect now | The first question to raise | Immediate next check |
| --- | --- | --- |
| Large global spread | What direction of major variation remained? | Does it connect to original features? |
| Nearby-neighbor structure | Did points that look attached also stay close in the original space? | trustworthiness, original-feature comparison |
| Rebuildability | How much of the original information can be rebuilt from the reduced representation? | reconstruction error, recheck differences by original axes |
| Hypotheses about lumps or outliers | Does this structure remain without projection illusion? | Other axis counts, other methods, original-data review |

### Memo To Leave Right After Seeing The Plot

After looking at a visualization result, the following kind of short memo helps reduce excessive confidence.

| Item | Example memo |
| --- | --- |
| Structure seen first | `A small point group seems to stand separately in the lower-left` |
| Interpretation boundary | `Do not finalize it as a separate product family only from the 2D separation` |
| Original-feature recheck | `Recheck through a table of price, core function, and usage frequency` |
| Comparison with other methods | `Check whether the split remains in PCA 2D and under other axis counts` |
| Next verification | `Review whether the hypothesis survives through follow-up clustering or original-feature summaries` |

The purpose of this memo is not to stop at `the plot looked neat`, but to separate `what was seen` from `what is still unknown`.

## What Should Be Watched Out For When Used Together With Clustering?

Connecting back to Chapter 17, people often color a dimensionality-reduction plot using cluster results. This can be very useful, but it can also be dangerous.

- If the clusters look beautifully separated, overconfidence grows easily.
- A colored plot can feel more clearly separated than the evidence actually supports.
- On the other hand, even if groups look mixed in the plot, they may still be more separable in the original high-dimensional space.

In other words, clustering results and dimensionality-reduction plots help each other, but when they meet, visual illusion can become stronger as well.

If that relation is compressed, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-18/p4-18-2-mermaid-04-en.mmd"
```

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

This toy exercise shows that if three features are reduced into one summary score, the result becomes easier to read, but some per-feature differences disappear. It also adds one more case where the summary value stays similar while the original pattern differs, so that the reader can see why it is risky to conclude from only a plot or one-dimensional summary.

- Problem situation: inspect what becomes convenient and what disappears when several features are reduced into one axis
- Input: samples expressed through three features
- Expected output: one summary value
- Concepts to check:
  - Dimensionality reduction simplifies representation
  - Once simplified, per-axis differences become weaker

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

What the reader should read from this example is:

1. Once three axes are reduced into one, the overall flow becomes easier to inspect.
2. But the detailed differences among `f1`, `f2`, and `f3` are pressed into the summary value.
3. So simplification and information loss arrive together.

### Change One Value: The Original Pattern Can Differ Even When The Summary Is The Same

This time, change the third sample so that the average remains similar while the axis-by-axis pattern changes.

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

The summary value of the third sample is still `6.0`, but now the three axes are not uniformly large because `f3` is relatively lower. If you look only at the summary value, this seems like the same conclusion as before, but if you go back to the original features, the sample pattern is not actually the same. That difference is exactly why reduced plots or summary axes must always be read in a back-and-forth movement with the original features.

### How Does This Exercise Recover The Goal Of Part 4?

Part 4 is not only about how to read one model output. It is also the stage for learning how to judge what becomes visible and what becomes hidden when the representation itself changes. This exercise keeps together `the structure that became easier to see after compression` and `the axis-level differences that disappeared because of compression`, so dimensionality reduction is read as an interpretation tool rather than a simple visualization technique. If the learner does not feel the Part goal here, the missing piece is usually not more PCA formula. It is the practical scene `the summary value can stay the same even while the original pattern differs`.

| Shared recording language | What to record immediately in this exercise |
| --- | --- |
| What structure appeared | If only a one-dimensional summary is seen, different samples can look like they occupy the same place |
| Interpretation boundary | A reduced plot or summary axis does not preserve every difference from the original features |
| Next question | Does the same separation remain in the original feature space or under another projection method? |

## What To Remember From This Section

- Dimensionality-reduction visualization is a tool for making high-dimensional structure easier to inspect.
- But compression into fewer axes introduces information loss and distortion.
- Distance in a 2D figure can differ from distance in the original high-dimensional space.
- Lumps in the figure can suggest structure hypotheses, but they are not themselves the correct answer or evidence.
- Dimensionality-reduction results should be read as tools for exploration and explanation, then checked again through original data and follow-up review.

| What should be looked at together | The question read first in this Section | Where it goes immediately next |
| --- | --- | --- |
| Visible structure | What split or lump appeared first in the figure? | Organizing cluster and outlier hypotheses |
| Interpretation boundary | How far should that structure be trusted, and where should reading stop? | Review of original features and comparison with other visualization methods |
| Next verification question | What additional checking is needed to keep or reject the hypothesis? | Follow-up model evaluation and original-data reinspection |

## Short Check

- Are you reading distance in a 2D picture as if it were the same thing as distance in the original high-dimensional space?
- Are you sending a structure that looks like a lump directly into cluster or policy judgment without further review?
- Are you using visualization as an exploration tool and comparing it again with original features and other methods?

## When Should This View Come To Mind First?

- When a 2D figure looks so clear that you want to conclude immediately, recall first the possibility of projection distortion and information loss.
- When you need to doubt whether points that look close are also close in the original space, separate high-dimensional distance from visual distance again.
- When clustering results and reduced plots are read together and illusion can grow stronger, bring back the boundary that visualization should remain only a hypothesis-generation tool.

## Sources And References

- scikit-learn developers, `2.5. Decomposing signals in components (matrix factorization problems)`, scikit-learn User Guide, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/decomposition.html](https://scikit-learn.org/stable/modules/decomposition.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `PCA`, scikit-learn API Reference, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html){: target="_blank" rel="noopener noreferrer" }
