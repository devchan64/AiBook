# P5-9.2 Batch And Tensor Computation

Section ID: `P5-9.2`
Version: `v2026.07.19`

In P5-9.1, we saw why deep learning fits GPUs and parallel processing so well. The next question appears immediately.

Then in what actual shape of grouped data are the deep-learning computations that GPUs handle well given to the model?

The expressions that appear repeatedly when answering this question are batch and tensor.

A batch is a grouping for calculating multiple samples at once, and a tensor is the general name for the multidimensional numeric arrays that deep learning handles, including such groupings.

When you need to review shape and computation units again in a short form, return to the glossary entries on [batch](/AiBook/reference/concept-glossary/#batch) and [tensor](/AiBook/reference/concept-glossary/#tensor).

## Scope Of This Section

- Why is a batch needed?
- How does a tensor extend from vectors and matrices?
- How is batch-level computation related to parallel processing?
- Why is the habit of reading input shapes important?

This section focuses on grasping what kinds of batch groupings and tensor shapes `the computations GPUs handle well` actually take. In other words, rather than a rigorous definition of tensor mathematics, we first close `what shapes deep-learning computation flows through`.

At the same time, it is also clear what we will not widen immediately in this section. The intuition of `why shape matters` and `how large matrix computation continues` is revisited later in P5-13.2 on attention and in P5-14.3 and P5-14.5 on Transformer computation structure.

## Goals Of This Section

- You can explain a batch as `a computation unit that processes multiple samples at once`.
- You can explain a tensor as `a multidimensional array that includes vectors and matrices`.
- You can state why the habit of reading shapes is important in deep-learning practice.
- You can confirm the intuition of batch and tensor shapes through an executable Python example.

## Why Is A Batch Needed

In deep learning, the same model is applied repeatedly to many samples. We can process samples one by one in sequence, but then it becomes hard to make full use of the advantages of parallel processing.

A batch is a way of grouping multiple samples and calculating them at once.

For example:

- instead of processing only 1 image, we process 32 images together
- instead of putting in only 1 sentence, we put in many sentences together
- tabular data also passes multiple rows into the model at the same time

The following understanding is enough.

`A batch lets the model group repeated computation into one chunk when the same operation has to be applied to multiple samples.`

## What Becomes Better When We Use Batches

The reason for using batches is not only convenience.

- they can use GPU parallel computation more effectively
- computation can become more efficient than handling one sample at a time
- gradients can also reflect information from multiple samples at once

Of course, if a batch becomes too large, it can use a lot of memory or change the learning dynamics. But at the introductory stage, it is enough to understand it first as `the basic unit of parallel computation`.

## What Is A Tensor

In Part 2, we saw scalars, vectors, and matrices. A tensor is the natural extension of that flow.

It is enough to explain it with the following table.

| Name | Example | Number of dimensions |
| --- | --- | --- |
| scalar | `3.14` | 0D |
| vector | `[1, 2, 3]` | 1D |
| matrix | `[[1, 2], [3, 4]]` | 2D |
| tensor | image/sentence arrays with a batch attached | includes 3D and higher |

That is, a tensor is not some magical special concept. It is the broad name for `a multidimensional numeric array`.

`In deep learning, it is enough to think that inputs, intermediate representations, and outputs all flow as tensors.`

## What Tensors Do Images, Sentences, And Tabular Data Look Like

In deep learning, even though the data types differ, in the end they are all organized into tensor shapes.

For example:

- tabular data: `(batch_size, feature_count)`
- grayscale image: `(batch_size, height, width)`
- color image: `(batch_size, channel, height, width)` or, depending on the framework, the channel position can differ
- sentence embedding: `(batch_size, sequence_length, embedding_dim)`

So tensors work as a common computational language across data domains.

## Why Is The Intuition Of Reading Shape Important

One of the most common errors in practice is misreading a shape and getting confused about `which axis is the batch`, and `which axis is the length, channel, or feature dimension`.

For example:

- if we forget the batch dimension
- if we flip rows and columns
- if we confuse the channel position
- if the label shape and output shape do not match

then the model may not run at all, or it may run while performing the wrong computation.

The following habit matters.

`In deep-learning practice, do not look only at the values. Always look at the shape together.`

## The Connection Between Batch Computation And Parallel Processing

In P5-9.1, we saw that the strength of the GPU lies in processing many similar operations at the same time. A batch is exactly the way this structure is provided in a form suited to deep-learning computation.

That is:

- the model keeps the same weights
- for the many samples inside the batch
- it repeats the same forward and backward pattern

As that repetition is grouped under the batch dimension, it connects naturally to parallel computation.

If we draw it in a very simple form, it looks like this.

```mermaid
--8<-- "assets/part-05/chapter-09/batch-tensor-flow-en.mmd"
```

## Cases And Examples

### Case. Reading The Same Batch Axis Across Tables, Images, And Sentences

Let us imagine at once a production-batch feature table, inspection images, and maintenance-log embeddings. At first, people easily feel that these are different kinds of input because tables are read as tables, images as pictures, and sentences as lines of text. But in deep-learning computation, all three are first read through the same frame: `batch axis + the structure that remains behind it`. In other words, `(32, 20)` is a tabular input that processes `32 batches at once`, `(32, 3, 224, 224)` is an input that processes `32 images at once`, and `(16, 128, 768)` is an input that processes `16 documents at once`.

The human-first standard here tends to be `tables count rows`, `images count pictures`, and `sentences count length`. But with only that standard, it is easy to miss what the model is actually processing simultaneously. Once we reread it from the shape viewpoint, the thing that has to be fixed first is always the first axis. The first axis is the `group of samples that enter the model at the same time`, that is, the batch axis, and after that we must separate whether the remaining axes mean features, channels and space, or tokens and embeddings.

So there are three results we should confirm first in this case.

- Is the first axis always read as `the number of samples processed together`?
- When we take out one batch item, does tabular data leave feature structure, images leave channel-space structure, and sentences leave token-embedding structure?
- Do practice errors decrease only when we read shapes not as number bundles but as `axis roles`?

If this case is fixed first, it becomes more natural to understand below why the comparison table and Python example keep telling us to look together at `the first axis` and `the structure left after taking one batch item out`.

| Scene | Result that is easy for people to see first | What we actually need to distinguish from the shape viewpoint | What to check next right away |
| --- | --- | --- | --- |
| tabular-data classification | It is easy to see it as data where table rows are read one by one. | The first axis is the number of batches computed together, and the rest is the feature axis. | In `(32, 20)`, try separating the roles of `32` and `20`. |
| image classification | It is easy to count only roughly how many pictures there are. | We need to read batch axis, channel axis, and spatial axes separately for convolution and pooling to make sense. | In `(32, 3, 224, 224)`, say what each axis is. |
| sentence model | It is easy to feel that we only need to look at sentence length. | We need to read batch axis, token axis, and embedding axis together so that attention and sequence computation can follow. | In `(batch, sequence_length, embedding_dim)`, distinguish the role of each axis. |

If we lay the three inputs side by side under the shape standard, they can be read like this.

```mermaid
--8<-- "assets/part-05/chapter-09/batch-shape-modality-compare-en.mmd"
```

The points to fix first in this comparison diagram are the following.

- In all three cases, the first axis is the `group of samples processed together`, that is, the batch axis.
- What changes is the structure attached after that first axis: tabular data keeps a feature axis, images keep channel and spatial axes, and sentences keep token and embedding axes.
- So when reading a shape, we must distinguish first not how many numbers it has, but `what remains after the first axis`, if we want to reduce practice errors.

## Practice And Example

The goal of this example is to confirm directly that the same `first axis` is read as `the batch axis` across production-batch tabular data, inspection-image tensors, and maintenance-log embeddings.

Input:

- a production-batch feature table
- a 4D tensor similar to inspection images
- a 3D tensor similar to maintenance-log embeddings

Output:

- the shape of each tensor
- the number of batches indicated by the first axis
- the structure that remains when one batch item is taken out
- a comparison of what misunderstanding appears when axes are read incorrectly

Problem situation:

- tabular data, images, and sentence embeddings can all be handled as tensors, but the meaning of their axes differs
- if we look at a shape only as a number bundle, it becomes easy to mix up the role of the first axis with the roles of the remaining axes

Concepts to confirm:

- tensor interpretation starts not from the values themselves, but from reading `shape` and the meaning of the axes first
- it becomes easier to distinguish each axis role when we look at what structure remains after taking out one batch item
- if we read axes incorrectly, we can confuse `number of batches`, `number of channels`, and `number of tokens`

For beginners, it is better to read this example in the following three steps.

| Reading step | What to look at first | The question to hold onto right after |
| --- | --- | --- |
| 1 | each tensor's `shape[0]` | is the first axis really read as the batch size? |
| 2 | the remaining `shape` after taking out one batch item | how does the structure left after the first axis differ for tables, images, and sentences? |
| 3 | `[wrong reading check]` | if we swap the meanings of the batch axis, channel axis, and token axis even though the numbers are the same, what misunderstanding appears? |

Input:

We use the production-batch feature table, the inspection-image tensor, and the maintenance-log embedding-style tensor summarized above.

Before reading the code, it helps to predict what `the first axis` means in each tensor, and what the axes left after taking out one batch item mean.

| Tensor | Comparison to predict first | Reason for the prediction |
| --- | --- | --- |
| `tabular_batch` | the first axis will likely be the number of production batches, and taking out one item will leave a feature vector | because tabular data is read in a `(batch, feature)` structure |
| `image_batch` | the first axis will likely be the number of images, and taking out one item will leave `(channel, height, width)` | because an image keeps separate channel and spatial axes outside the batch |
| `text_batch` | the first axis will likely be the number of maintenance-log documents, and taking out one item will leave `(sequence_length, embedding_dim)` | because sentence tensors keep both token and embedding axes |

The difference we need to confirm here also does not end with memorizing shapes. If we cannot correctly read `the first axis` as the batch size, we end up counting images and channels interchangeably, or confusing the number of documents with the token length. In other words, the core of this section is not guessing numbers, but connecting `how many samples are fed into the model` and `what structure remains inside one sample` to practical judgment.

The purpose of this table is to read separately `what the first axis is` and `what remains after taking out one batch item`.

```python
import numpy as np

tabular_batch = np.array([
    [12, 180, 1],
    [4, 95, 0],
    [9, 140, 1],
])

# (batch, channel, height, width)
image_batch = np.arange(2 * 3 * 2 * 2).reshape(2, 3, 2, 2)

# (batch, sequence_length, embedding_dim)
text_batch = np.arange(2 * 4 * 3).reshape(2, 4, 3)

print("tabular_batch shape =", tabular_batch.shape)
print("number of production batches =", tabular_batch.shape[0])
print("one batch feature row =", tabular_batch[0].tolist())
print()

print("image_batch shape =", image_batch.shape)
print("number of images =", image_batch.shape[0])
print("first image shape =", image_batch[0].shape)
print("first image, first channel =")
print(image_batch[0, 0])
print()

print("text_batch shape =", text_batch.shape)
print("number of maintenance logs =", text_batch.shape[0])
print("first log embedding shape =", text_batch[0].shape)
print("first token embedding =", text_batch[0, 0].tolist())
print()

print("[wrong reading check]")
print("if image_batch.shape[1] is read as number of images ->", image_batch.shape[1])
print("actual number of images ->", image_batch.shape[0])
print("if text_batch.shape[1] is read as number of logs ->", text_batch.shape[1])
print("actual number of logs ->", text_batch.shape[0])
```

In the output, first look at how the shape of each batch and the structure of the first sample differ by data type.

```text
tabular_batch shape = (3, 3)
number of production batches = 3
one batch feature row = [12, 180, 1]

image_batch shape = (2, 3, 2, 2)
number of images = 2
first image shape = (3, 2, 2)
first image, first channel =
[[0 1]
 [2 3]]

text_batch shape = (2, 4, 3)
number of maintenance logs = 2
first log embedding shape = (4, 3)
first token embedding = [0, 1, 2]

[wrong reading check]
if image_batch.shape[1] is read as number of images -> 3
actual number of images -> 2
if text_batch.shape[1] is read as number of logs -> 4
actual number of logs -> 2
```

- In all three cases, the first axis is `the number of batches processed at the same time`.
- When we take out one batch item, the table leaves a feature row, the image leaves a channel-space structure, and the sentence leaves a token-embedding structure.
- Reading a shape does not mean merely counting how many numbers there are. It means interpreting what each axis stands for.

| Tensor | The key to read now |
| --- | --- |
| `tabular_batch` | Read the first axis as the number of production batches, and when one batch item is taken out a feature vector remains. |
| `image_batch` | The first axis is the number of images, and the second axis `3` is not the number of images but the number of channels. |
| `text_batch` | The first axis is the number of maintenance logs, and the second axis `4` is not the number of logs but the token length. |

Even when reading the output numbers, we should separate `array size` from `axis meaning`.

| Comparison | What appears first in the output | Interpretation that is easy to leave if we look only at the numbers | Interpretation that changes once we read up through the shape viewpoint |
| --- | --- | --- | --- |
| `tabular_batch shape = (3, 3)` | The two numbers are the same, so they can look like they play the same role. | It is easy to think both are just `3`, so there is not much difference. | The first `3` is the number of production batches, while the second `3` is the number of features in each batch, so their roles are completely different. |
| `image_batch shape = (2, 3, 2, 2)` | The `3` stands out and is easy to mistake for the number of images. | It is easy to treat the second axis like another sample count. | The actual number of images is the first axis `2`, while the second axis `3` is the channel count, so if we swap the axis reading the meaning of the computation breaks. |
| `text_batch shape = (2, 4, 3)` | The `4` looks large, so it is easy to mistake it for the number of documents. | It is easy to pass over by reading the middle number as the number of logs. | The first axis `2` is the number of logs, `4` is the token length, and `3` is the embedding dimension, which becomes the standard for reading attention inputs later. |

| Practice-judgment standard | Misunderstanding that easily appears if the axis is read incorrectly | Judgment that changes once we read up through the shape viewpoint |
| --- | --- | --- |
| setting a tabular-data input | it is easy to feel that if the shape is `(3, 3)`, swapping any axis should be similar | because the first axis is the batch size, we must first see that if the feature axis is placed wrongly, we can already be wrong about how many samples enter one step |
| checking image-model input | it is easy to read `3` as the number of images and misunderstand the batch as 3 pictures | the real batch is 2 images and `3` is the channel count, so if we swap batch and channel axes even the interpretation of the convolution becomes wrong |
| checking text-model input | it is easy to read `4` as the number of logs and think 4 documents are fed at once | in reality 2 documents are fed, each cut to length 4, so we must separate token axis from batch axis when checking padding and attention input |

In other words, the first question a reader should hold onto in shape interpretation is not `how many numbers are there`, but `is this axis sample count, channel count, or length`.

If we turn this result into a practice scene, someone who reads shapes correctly checks not only `why does the model fail to run`, but first `where did I swap the batch axis, channel axis, and token axis in my reading`. By contrast, if shapes are seen only as number bundles, it becomes easier to repeat the same errors while noticing late that the input itself was defined incorrectly.

The expressions batch and tensor are not merely library syntax. They became generalized together with deep learning settling as a system of large-scale parallel numerical computation. As GPU-based learning spread, the intuition of seeing data not as `one single sample`, but as `a grouped tensor` effectively became standard.

That is because the following are joined here into one language of shape:

- the linear algebra and NumPy arrays of Part 2
- the input matrices and feature tables of Part 3
- the GPU parallel processing of P5-9.1

So it is better to see tensors not as a new difficult concept, but as the result of expanding the array intuition learned earlier into deep-learning scale.

If we pause here once and briefly fix `when should we read first from the shape and batch viewpoint rather than from the data-type viewpoint`, the baseline will shake less when we move to the later explanations of attention and Transformer computation.

| Question to think of first | Why the batch/tensor viewpoint is needed first | What later sections continue from here |
| --- | --- | --- |
| why does the input fail to run, or why does it perform the wrong computation? | because before the values, the meaning of the axes and the consistency of the shape must match first | reading the shapes of query, key, and value in attention |
| why do tables, images, and sentences all look like the same computational language? | because even when data types differ, once they are grouped under tensors and batch dimensions we can read a shared computation structure | the large matrix computation of Transformers |
| why are multiple samples handled at once? | because the batch dimension makes parallel computation and gradient aggregation possible | the computational burden caused by long sequences and large batches |

## Checklist

- Can you explain what basic units batch and tensor are in deep-learning computation?
- Can you describe how the structure of processing many samples at once connects to GPU computation?
- Can you explain that a batch is a computation unit that processes multiple samples at once?
- Can you say that a tensor is the general name for the multidimensional numeric arrays handled by deep learning?
- Can you explain a batch not as `several samples arranged for convenience`, but as `the unit that sends the same computation into multiple samples at the same time`?
- When you see a shape such as `(batch_size, sequence_length, embedding_dim)`, can you actually separate and read the axis names?
- When reading a shape, can you first check whether the current axis is the batch, length, or channel, and whether the input and output match the expected structure?
- Can you explain tabular data, images, and sentence data again through the common computational language of tensors and shapes rather than only through separate intuitions?

## Sources And References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Aurelien Geron, `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow`, 3rd ed., O'Reilly, 2022, checked on 2026-06-29.
- NumPy Developers, `ndarray`, NumPy Documentation, checked on 2026-06-29. [https://numpy.org/doc/stable/reference/arrays.ndarray.html](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }
