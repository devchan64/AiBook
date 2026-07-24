# P5-10.2 Representations In Deep Layers

> Section ID: `P5-10.2`
> Version: `v2026.07.20`

In P5-10.1, we explained representation learning as `the process in which the model learns useful internal features on its own`. The next question then follows naturally.

Then in a deep neural network, how do we say the representations change as the layers get deeper?

As layers get deeper, representations usually move from more local and simple patterns toward more abstract patterns that are closer to the task.

When you need to confirm again how to read the claim that representations change as layers get deeper, return to the glossary entry on [representation](/AiBook/reference/concept-glossary-parts/13-pieup/#representation).

## The Question Of How Deep Layers Change Representations

- What do low-level features and high-level representations mean?
- Why do we say stacking many layers makes more abstract representations possible?
- In what ways do deep-layer representations look similar, and in what ways do they look different, across data domains?
- Why should this explanation be read not as a perfect law, but as an intuitive tendency?

This section first closes deep-layer representation as `the tendency to move from simple patterns close to raw input toward more abstract representations that are closer to the task`, and focuses on explaining that intuition safely.

At the same time, it is clear what we will not widen right away in this section. Hierarchical representation in images reconnects in P5-11.1 and P5-11.2, and sequential-data and attention-based representation reconnect in P5-12.1, P5-12.2, P5-13.1, P5-13.2, and the main Transformer sections from P5-14.1 through P5-14.6.

In other words, here we safely explain the intuition of hierarchical representation without creating exaggerations such as `deeper layers are automatically more intelligent`.

## Standards For Low-Level And High-Level Features

- You can explain deep-layer representation as `the tendency to move from simple patterns toward more abstract representations`.
- You can state that the reason for stacking layers is connected not only to increasing the number of parameters, but also to changing the level of representation.
- You can compare the intuition of hierarchical representations in images, speech, and text.
- Through an executable Python example, you can confirm the intuition that the representation space changes as the signal passes through multiple layers.

## What Do Low-Level And High-Level Mean

At the introductory stage, the following distinction is enough.

- low-level features: the most immediate raw patterns
- high-level representations: abstract combinations that are closer to the task

For example, in images:

- early on: edges, directions, simple textures
- in the middle: partial shapes
- later: object clues

That is, in images a hierarchy is often observed where low-level features pass through partial shapes and lead to object clues further back.

The important point is that this is not a formula that applies identically to every network, but an educational intuition that is often observed.

If we write the same content more clearly by layer role, it becomes the following.

| Representation level | Common explanation | Distance from the task |
| --- | --- | --- |
| low-level | edges, short frequency patterns, token-neighborhood clues | still close to raw input |
| mid-level | partial shapes, syllable clues, syntactic patterns | intermediate structure linking input and task |
| high-level | object clues, speaker characteristics, sentence-semantic roles | closer to task judgment |

## Why Can The Representation Change When We Stack Layers

One layer makes combinations on top of the output of the previous layer. So later layers use the representations created earlier as material, rather than looking directly at the original input.

That is:

- the first layer handles signals close to the input
- the next layer handles combinations of those signals
- deeper layers then handle combinations of those combinations

This repetition is why we explain that representations become more abstract as layers become deeper.

It is enough to remember it like this.

`A deep layer does not deal with the original data itself so much as it recombines already organized intermediate representations to create representations that are closer to the task.`

If we turn this process into a small work analogy, it becomes easier.

- The first stage writes down clues that stand out in the raw record.
- The next stage groups those clues into more meaningful intermediate judgment material.
- The final stage uses that intermediate material to reach a conclusion that is closer to the real task.

Each layer of a neural network does not work in exactly the same way, but at the introductory stage it can be read similarly as `clue -> intermediate structure -> representation close to the task`.

What matters here is the sense that later layers do not simply reread the original input as-is, but rather recombine the representation already organized by earlier layers.

```mermaid
--8<-- "assets/part-05/chapter-10/layered-recomposition-flow-en.mmd"
```

That is, depth is more accurately read not simply as `the number of layers increased`, but as `an additional stage was added that recombines representations that were already made`.

## The Intuition Of Hierarchical Representation In Images

The image domain is the field where this explanation sounds the most intuitive.

For example, if we think of a CNN:

- early filters can react to edges or small patterns
- middle layers can react to partial structures such as eyes, ears, or wheels
- later layers can be explained as combining larger clues such as tank outlines, valve arrangements, or warning-light positions

Of course, the actual inside of a network is more complex than this. But here the key flow is `small pattern -> partial structure -> larger meaningful clue`.

## The Intuition Of Hierarchical Representation In Speech And Text

This intuition is useful outside images as well.

### Speech

- raw waveform or short frequency clues
- pronunciation fragments
- clues such as syllables, words, and speaker characteristics

That is, in speech too, a hierarchy is often observed where low-level frequency clues pass through pronunciation fragments and lead to larger language clues.

### Text

- token-level information
- neighboring-context patterns
- sentence-level meaning and role

That is, in text too, token and nearby-context patterns accumulate and often lead to sentence-level meaning and role clues.

So even when the data domain changes, the hierarchical explanation that `the front deals with signals that are closer, while the later part deals with structures that are closer to the task` is often still valid.

If we place them side by side by domain, the differences and commonalities become clearer.

| Domain | What is more visible in the front | What becomes more visible later |
| --- | --- | --- |
| image | boundaries, directions, small textures | partial structures, object clues |
| speech | short frequency patterns, pronunciation fragments | syllables, words, speaker characteristics |
| text | tokens, neighboring context | sentence roles, semantic relations, task clues |

## But We Should Not Overstate This Explanation

The intuition of hierarchical representation is very useful in education, but the following points should also be known.

- not every layer has one neatly separable meaning
- the way representations appear differs by domain and structure
- in modern models, more complex interactions appear than a simple one-line hierarchy

That is, the explanation in this section is not a strict universal law, but `a safe basic map for reading the learning flow`.

In particular, it is better to avoid the following misunderstandings.

| Common misunderstanding | Safer phrasing |
| --- | --- |
| deeper layers are always smarter | deeper layers tend to create representations that are closer to the task |
| each layer has exactly one fixed meaning | layer representations overlap and mix, and interpretation is not always clean |
| every model shows the same hierarchy | the hierarchical intuition is useful, but it differs by structure and domain |

## Drawn Very Simply

```mermaid
--8<-- "assets/part-05/chapter-10/hierarchical-representation-flow-en.mmd"
```

This diagram is the most compressed form of the intuition behind deep-layer representation.

## Cases And Examples

### Representative Case. Classifying Sealing Defects In Images

Suppose we separate normally sealed pouches from pouches whose edges are slightly lifted on a packaging line. At first, people easily try to judge only from local clues that are immediately visible, such as the length of bright lines or the number of lifted segments. But if the camera angle changes a little or a strong reflection enters, the same weak seal can look normal when judged only by line length and brightness. Early layers react first to local patterns such as short boundaries, brightness changes, and small wrinkle fragments, and deeper layers then combine larger quality clues such as how the sealing line is connected, the curvature of the edge, and the way wrinkles and reflections appear together. So we can explain that as layers get deeper, the representation approaches not simple sparkling points or short line fragments, but `how the overall sealing structure is connected`, and that more stable quality separation becomes possible even between images that share similar local patterns.

So the result to check in this case is whether pouches that were confusing when looking only at short brightness changes become more stably separated into normal and weak seal once the clue of the whole sealing structure is reflected.

| Standard that is easy for a person to see first | Standard to reread from the hierarchical-representation viewpoint |
| --- | --- |
| if a few shiny lines look similar, it is easy to feel the quality is the same | even if early layers react together to similar reflections, deeper layers can separate the whole connected structure of the seal |
| if we look only at short boundary fragments, normal and weak seals are easy to confuse | when those partial fragments accumulate and are recombined into edge curvature and connection style, the distinction can become more stable |
| it is easy to feel that going deeper only means more values appear | what matters is not the number of values, but `which quality-separation axis becomes clearer` |

The same viewpoint applies to other data as well. But the key to hold onto in this section is not the domain name, but `are the nearby clues from the front part regrouped into a larger structural judgment axis in the later layers`.

| Scene | Result that is easy for a person to see first | What actually needs to be distinguished from the hierarchical-representation viewpoint | What to check next right away |
| --- | --- | --- | --- |
| classifying sealing defects in images | if shiny lines and boundary fragments are similar, the quality looks the same | even if early local patterns are similar, deeper layers may preserve the overall connection structure of the seal as a more important axis | check whether normal and weak seals are split more stably by overall-structure clues |
| reidentifying an equipment-camera scene | if the large cylinder impression looks similar, it is easy to feel it is the same scene | even when lighting and angle differ, deeper layers may preserve a structural axis such as tank-pipe-valve layout more strongly | check whether equipment-structure clues remain more than local reflection wobble |
| sentence classification | if a few key words are similar, it is easy to feel the type is the same | in deeper representations, sentence intent and risk direction may remain as a more important axis than the words themselves | check whether a sentence that looked like a status report becomes separated as a reinspection request |
| production-batch time series | if the most recent values are similar, the states can look similar | in deeper representations, repeated rhythm and response order may remain as a more important axis than the recent average value | check whether risk and stable groups separate earlier |

## Practice And Example

The goal of this example is to see how anomaly signals from production batches are rearranged into a different representation space as they pass through one layer and then two layers.

Problem situation:

- even production batches that look similar in the shallow input space can change into a representation space that is easier to distinguish as they pass through layers
- however, the weights in this example are not values obtained by actual learning, but fixed transforms for seeing how layer-by-layer changes alter the representation space

Input:

- 4 production batches with two anomaly-signal indicators
- two stages of fixed weight transformation

Output:

- the batch signals in input space
- the first hidden representation
- the second hidden representation
- how distances between batches change as the layers get deeper
- a comparison of which batch pairs become closer and which become less close

Concepts to confirm:

- a learned deep representation can rearrange the input into a more useful space rather than leaving it as-is
- this example does not implement the whole learning process, but isolates only the phenomenon where layer-by-layer transforms change coordinates and distance relations
- to read the meaning of depth, we need to see how distances between batches change across one layer and then two layers
- it is more accurate to look not only at the final labels, but also at the change in intermediate hidden representations
- deep-layer representations can reorganize in a new coordinate system `which batches become more similar and which become less similar`

For beginners, it is better to read this example in the following three steps.

| Reading step | What to look at first | The question to hold onto right after |
| --- | --- | --- |
| 1 | `signals`, `h1`, `h2` | as the signal passes through layers, is the same input batch placed in a different coordinate system again? |
| 2 | the distance outputs | which batch pairs become closer faster, and which remain relatively less close? |
| 3 | the two graphs | is not just distance reduction but actual `re-ranking of relations` visible? |

Input:

We use the production-batch anomaly-signal vectors and the layer-wise weight transforms summarized above.

Here `w1` and `w2` are not values meant to claim they are trained model parameters. In real deep learning, such transforms are adjusted through data, loss, and the optimizer. Here, instead of that learning process, we only confirm how the representation space and distance relations change when we pass through the already fixed transforms `signals -> h1 -> h2`.

Before reading the code, it helps to predict how some batch pairs may change.

| Comparison | Change to predict first | Reason for the prediction |
| --- | --- | --- |
| `batch_1` vs `batch_2` | they may become closer | even if the input indicators differ, as they pass through layers they may compress onto a similar anomaly-combination axis |
| `batch_1` vs `batch_4` | they may still remain farther apart | pairs that start with a difference may not come together to the same degree even in deeper representations |

The purpose of this table is to first hold onto not `everything moves the same way as depth increases`, but `the representation space rearranges the relations among batches`.

```python
# This example shows how production-batch signals pass through two layers and rearrange distance relationships in h1 and h2 representation spaces.
import numpy as np

def relu(x):
    return np.maximum(0, x)

def pair_distance(a, b):
    return round(float(np.linalg.norm(a - b)), 3)

signals = np.array([
    [1.0, 2.0],
    [2.0, 1.0],
    [0.5, 3.0],
    [3.0, 0.5],
])

w1 = np.array([
    [0.8, 0.2, 0.5],
    [0.1, 0.7, 0.4],
])

w2 = np.array([
    [0.5, 0.3],
    [0.2, 0.9],
    [0.6, 0.1],
])

h1 = relu(signals @ w1)
h2 = relu(h1 @ w2)

print("signals =")
print(np.round(signals, 3))
print()
print("h1 =")
print(np.round(h1, 3))
print()
print("h2 =")
print(np.round(h2, 3))
print()
print("distance(batch_1, batch_2) in signals =", pair_distance(signals[0], signals[1]))
print("distance(batch_1, batch_2) in h1 =", pair_distance(h1[0], h1[1]))
print("distance(batch_1, batch_2) in h2 =", pair_distance(h2[0], h2[1]))
print("distance(batch_1, batch_4) in signals =", pair_distance(signals[0], signals[3]))
print("distance(batch_1, batch_4) in h1 =", pair_distance(h1[0], h1[3]))
print("distance(batch_1, batch_4) in h2 =", pair_distance(h2[0], h2[3]))
```

In the output, look first at `signals`, `h1`, and `h2` in order, and then see how the distance between `batch_1` and `batch_2` changes as it passes through the layers.

```text
signals =
[[1.  2. ]
 [2.  1. ]
 [0.5 3. ]
 [3.  0.5]]

h1 =
[[1.   1.6  1.3 ]
 [1.7  1.1  1.4 ]
 [0.7  2.2  1.45]
 [2.45 0.95 1.7 ]]

h2 =
[[1.6   1.87 ]
 [1.91  1.64 ]
 [1.66  2.335]
 [2.435 1.76 ]]

distance(batch_1, batch_2) in signals = 1.414
distance(batch_1, batch_2) in h1 = 0.866
distance(batch_1, batch_2) in h2 = 0.386
distance(batch_1, batch_4) in signals = 2.5
distance(batch_1, batch_4) in h1 = 1.639
distance(batch_1, batch_4) in h2 = 0.842
```

- input batch signals do not go straight to the answer, but are rearranged while passing through intermediate representations `h1` and `h2`
- even the same two batches can become closer or farther apart as they pass through layers
- it is better to read deep-layer representation not as `the numbers simply increase`, but as a process where the relations between batches themselves can change through layer-wise transforms
- in an actually trained model, we would need to confirm together whether this relation change was adjusted in the direction that reduces the loss

If we separate the distance changes into a graph, it becomes clearer that even when both batch pairs become closer, they do not become closer at the same speed or to the same degree. `batch_1` and `batch_2` remain closer neighbors in `h2`, while `batch_1` and `batch_4` also move closer but remain relatively farther apart.

![Distance changes between batch pairs across hierarchical representation stages](/AiBook/assets/part-05/chapter-10/hierarchical-representation-distance-trace-en.png)

If we look only at the final `h2` representation space, we can see that the deep-layer representation did not simply shrink the values, but rearranged the positional relations between batches.

![Production batches rearranged again in the h2 representation space](/AiBook/assets/part-05/chapter-10/hierarchical-representation-h2-space-en.png)

The output should be read not by looking at `one distance` alone, but by reading together `how the relations between batches are reorganized`.

| Comparison | The key to read now |
| --- | --- |
| `batch_1` vs `batch_2` | They differ in input space, but as the layers get deeper they are compressed into a closer representation. |
| `batch_1` vs `batch_4` | This pair also gets closer, but still remains farther than `batch_1` vs `batch_2`, showing that deep layers are re-ranking relations. |
| overall interpretation | Depth is not the process of pushing every batch into one place, but, in a learned model, the viewpoint that `which batches are more similar and which are less similar` can be reorganized in a new coordinate system useful for the task. In this example, we isolate only the coordinate change and relation rearrangement. |

Even when reading the output numbers, we should separate `does the distance decrease` from `which pair remains as the more important neighbor`.

| Comparison | What appears first in the output | Interpretation that is easy to leave if we look only at distance | Interpretation that changes once we include hierarchical representation |
| --- | --- | --- | --- |
| `batch_1` vs `batch_2` | It quickly becomes closer as `1.414 -> 0.866 -> 0.386`. | It can look as if everything simply becomes similar as the layers get deeper. | Under this fixed transform, these two batches are reordered into closer neighbors. In a real model, we would also have to check whether this reordering is useful for the task. |
| `batch_1` vs `batch_4` | It also becomes closer as `2.5 -> 1.639 -> 0.842`. | It is easy to think that in the end all batches simply become similar. | Even though it becomes closer, it still remains farther than `batch_1` vs `batch_2`, so what matters is that deep layers are newly ranking the relations. |
| overall interpretation | All distances seem to shrink. | Depth can feel like only a process of compressing values. | The key is not compression itself, but that which relations remain closer can change along with the coordinate system. Whether they are right for the task must be checked through learning and evaluation. |

The viewpoint of representation in deep layers is the key axis that explains why deep learning was different from shallow models. It is not simply that there are many layers, but that the explanation `it forms hierarchical representations` shows why CNNs, RNNs, and Transformers are not just large functions.

This viewpoint makes the immediately previous P5-10.1 representation learning more concrete as `internal representations also change when layers are added`, and then naturally spreads into CNNs in P5-11.1 and P5-11.2, sequential models in P5-12.1 and P5-12.2, and attention in P5-13.1 and P5-13.2. It also continues into representation-learning research, deep-learning interpretability research, and discussions of embeddings and hidden representations in LLMs, so this section of Part 5 also serves as an important conceptual bridge into the later part of Part 5.

If we pause here once and briefly fix `when should we read first from the viewpoint of hierarchical representation rather than from the layer count itself`, the explanation of depth naturally turns into an explanation of structure when we move to the next CNN chapter.

| Question to think of first | Why the hierarchical-representation viewpoint is needed first | What the next section continues from here |
| --- | --- | --- |
| is the reason for stacking more layers more than just increasing the number of parameters? | because it can recombine earlier representations and create representations that are closer to the task | how CNNs enlarge local patterns layer by layer |
| why do we separate low-level features from high-level representations? | because before the structure explanation, we need to read `what is gradually becoming more abstract` | the difference in representation across images, sequences, and attention |
| why do we say deep models differ from shallow models? | because it is safer to read depth as a sequence of internal-representation rearrangements rather than just the size of the function | how later structures learn representations |

## Checklist

- Can you explain the intuition that as layers get deeper, representations move toward more abstract and task-nearer patterns?
- Can you say together that this explanation is a tendency rather than an absolute law?
- Can you explain that one reason for stacking many layers is not only increasing parameters, but also changing the level of representation?
- Can you explain depth not only as `there are many layers`, but as `the number of stages that recombine intermediate representations increases`?
- Can you say that the intuition of hierarchical representation is often valid across images, speech, and text?
- Can you state clearly that the low-level, mid-level, and high-level distinction is a basic educational map, not a strict law?
- When you are explaining depth only through parameter increase, can you think first of the hierarchical-representation viewpoint?
- When reading the next CNN chapter, are you ready to think first about `how local patterns grow hierarchically`?

## Sources And References

- Yoshua Bengio, Aaron Courville, Pascal Vincent, `Representation Learning: A Review and New Perspectives`, IEEE TPAMI, 2013, checked on 2026-07-19. [https://arxiv.org/abs/1206.5538](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Dumitru Erhan et al., `Why Does Unsupervised Pre-training Help Deep Learning?`, JMLR, 2010, checked on 2026-07-19. [https://jmlr.org/papers/v11/erhan10a.html](https://jmlr.org/papers/v11/erhan10a.html){: target="_blank" rel="noopener noreferrer" }
