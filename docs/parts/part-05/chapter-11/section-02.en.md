# P5-11.2 Convolution And Pooling

Section ID: `P5-11.2`
Version: `v2026.07.17`

In P5-11.1, we explained a CNN as `a neural network that repeatedly reads local patterns in images`. The next question remains.

What is the core operation that actually computes those local patterns, and why does pooling so often appear together with it?

Convolution is the operation that computes local-pattern scores with a small filter, and pooling is the operation that organizes those results into a smaller, more summarized form.

When the operation names become mixed up again, it is useful to reread together the glossary entries on [convolution](/AiBook/reference/concept-glossary/#convolution) and [pooling](/AiBook/reference/concept-glossary/#pooling).

## Scope Of This Section

- What does convolution compute?
- What do filter and feature map mean?
- Why is pooling used, and what does it reduce?
- When the two operations appear together, how should we read the representation flow of a CNN?

This section focuses not on proving the convolution formula rigorously, but on first closing `the flow in which a CNN scores local patterns and then summarizes those responses`.

At the same time, it is clear what we will not widen immediately in this section. A broader comparison of vision structures after CNNs is revisited in supplementary reading P5-11.3 around `CNN and Vision Transformer (ViT)`. Padding, stride, and dilation are handled only as much as needed here to understand `how the filter reads the input`.

## Goals Of This Section

- You can explain convolution as `the operation where a small filter computes local-pattern scores`.
- You can explain a feature map as `the spatial record of filter responses`.
- You can say why pooling is used to reduce spatial size and summarize important responses.
- Through an executable Python example, you can confirm the intuition of convolution and max pooling.

## The Order For Reading This Section

1. First look at how convolution computes local-pattern scores.
2. Then look at how the result remains as a response map called a feature map.
3. Then look at how pooling passes that response onward in a smaller and more summarized form.
4. Then organize how convolution and pooling connect into one flow.
5. Finally look again at how `padding`, `stride`, and `dilation` change the way this flow is read.

## What Does Convolution Do

Convolution moves a small filter across many positions in the image and scores how well each position matches a certain pattern.

The core point is that the filter carries the small pattern it wants to find and sweeps across the image to produce response scores.

- the filter can be seen like `a small pattern template to find`
- it performs multiplications and additions with each local patch of the image
- and produces a response score for that position

That is, convolution does not judge the whole image at once. It is a way of repeatedly applying `a small pattern detector` to the full set of positions.

## What Does A Filter Mean

A filter is usually a small array of numbers. For example, a 3x3 filter can look at a 3x3 local patch.

`A filter is a small bundle of weights that is learned to respond to patterns such as edges, directions, textures, or small shapes.`

As a CNN is trained, these filter values also change to fit the data. That is, a person does not directly design every filter. The model also learns which filters are useful.

## What Is A Feature Map

If one filter is applied across the whole image, the result is a new 2D array that stores how strongly that filter reacted at each position. This is called a feature map.

That is:

- over the input image
- the filter is applied at each position
- and the recorded response values become

the feature map.

The key point is that a feature map is the result that records, by position, where and how strongly one specific filter reacted in the image.

`A feature map is a map that records where in the image, and how strongly, a specific filter reacted.`

At this point it helps readers to fix the following distinction together.

| Name | What it means |
| --- | --- |
| filter | a small pattern template to find |
| convolution result | the pattern score computed at each position |
| feature map | the resulting map that gathers those scores by position |

## Why Is Pooling Needed

If we only keep stacking convolution results as they are, the spatial size can remain large and the amount of computation can also become large. It is also not always best to keep carrying every bit of detailed position information all the way to the end.

Pooling plays the role of reducing such information into a more summarized form.

For example, max pooling leaves only the largest response inside a small region.

`Pooling reduces some detailed position information, but passes important responses onward in a more compressed way.`

## Why Is Max Pooling Intuitive

Max pooling chooses one largest value inside a small window. This gives the reader the following intuition.

- it keeps the strongest pattern response in that region
- it can become less sensitive to small position changes
- it compresses the computation by reducing spatial size

That is, max pooling is best read as `a summary that keeps the most noticeable signal`.

If we compare this difference more briefly, it becomes the following.

| Stage | What it mainly does |
| --- | --- |
| convolution | finds patterns |
| pooling | summarizes the responses it found |

If we split the same image scene into those two stages, the difference becomes more direct.

| The same scene | What convolution does first | What pooling does immediately after |
| --- | --- | --- |
| a black line on a white background | scores where the boundary response is strong | keeps only the strongest boundary response in that region and passes it on in smaller form |
| near upper pipes of a mixing tank | first reacts to small structures such as valve outlines, pipe boundaries, and warning-light reflections | compresses the strong responses so the next layer can read larger equipment parts more easily |
| a surface-defect image | raises the response at positions with small scratches or cracks | summarizes defect-candidate signals so they are easier to keep for defect judgment |

## How Should We Read Convolution And Pooling Together

If we connect them in a very simple form, it looks like this.

```mermaid
--8<-- "assets/part-05/chapter-11/convolution-pooling-flow-en.mmd"
```

This diagram shows the three actions `find -> record -> summarize`.

1. Convolution first finds a local pattern.
2. The feature map records that response by position.
3. Pooling passes that record on in a smaller and more summarized form.

This flow is easier to read when we place a practical inspection scene and a numeric array side by side. The example below simplifies `a small sealing patch where the left-right column heat distribution changes sharply at the sealing edge`.

| Scene | Value representation |
| --- | --- |
| small inspection patch | a 4x4 sealing patch where a high heat distribution on the left continues into a lower heat distribution on the right |
| sample input matrix | `[[3, 3, 1, 1], [3, 3, 1, 1], [3, 3, 1, 1], [3, 3, 1, 1]]` |

Now suppose we place a `2x2 filter that reacts to left-right column differences` over this input.

| Item | Value |
| --- | --- |
| filter | `[[1, -1], [1, -1]]` |
| reading style | compares the left and right columns to find a sealing-boundary change |

If we move the filter one step at a time and compute, the following feature map appears.

| Stage | Sample matrix |
| --- | --- |
| input image | `[[3, 3, 1, 1], [3, 3, 1, 1], [3, 3, 1, 1], [3, 3, 1, 1]]` |
| convolution result | `[[0, 4, 0], [0, 4, 0], [0, 4, 0]]` |
| 2x2 max-pooling result | `[[4]]` |

If we divide the same transform into one step at a time, it can be read as follows.

![Convolution input sealing patch](/AiBook/assets/part-05/chapter-11/convolution-pooling-input-en.png)

The input patch is still closer to the small heat-distribution scene seen by a person. High values on the left and low values on the right are placed together, but at this stage `where is the boundary` has not yet been separated into a score.

![Convolution feature map](/AiBook/assets/part-05/chapter-11/convolution-pooling-feature-map-en.png)

After convolution, it becomes a response map showing how well each position matches the filter. Here, the value `4` repeats only at the middle position where the left-right column difference actually appears, meaning the input scene has turned into `a position map of boundary responses`.

![Max-pooling summary result](/AiBook/assets/part-05/chapter-11/convolution-pooling-max-pool-en.png)

Max pooling does not pass that whole response map onward 그대로. Instead, it keeps only the strongest response inside the small region. What changes at this stage is that rather than the detailed position, the summary signal `there was a strong sealing-boundary change in this region` is passed to the next layer.

The key to reading these numbers is the following.

- `0` means a position where the left-right difference expected by the filter is almost absent
- `4` means a position where the heat-distribution boundary the filter wanted was captured strongly
- `[[4]]` after max pooling means that even if detailed position is reduced, the key point `there was a region with a strong sealing-boundary change` remains

That is, the small inspection patch holds onto the human scene, while the sample matrices show what kind of numeric summary convolution and pooling actually produce.

This flow shows that a CNN:

- first finds a pattern
- then records that response
- then passes it on to the next layer in a more compressed form

That is, `convolution scores local patterns, and pooling passes those scores onward in a smaller form that the next layer can read more easily.`

Before moving to the next ViT comparison section from here, if we fix once more what unit a CNN actually uses for computation, it can be seen as follows.

```mermaid
--8<-- "assets/part-05/chapter-11/cnn-local-window-baseline-en.mmd"
```

The points to hold onto first in this baseline diagram are the following.

- the first computation unit of a CNN is not the whole image, but `a small local window that moves with overlap`
- what each window first produces is a local response score to the question `how well does this position match the filter pattern`
- so when we later look at ViT patch tokens, we can compare `a method that sweeps over small windows` and `a method that reads already cut patches` on the same input

If we read CNN only as a past structure that existed before Part 5 or before Transformers, it is easy for it to look like `an old model name for images`. But in Part 5, the responsibility of the CNN is already closed here. That is, the CNN is a structure that has its own answer to `how should we detect and summarize local patterns in images`, and the later parts only need to continue by handling different data-structure problems, not by replacing this answer.

## What Do Padding, Stride, And Dilation Mean

Although convolution and pooling are the center of this section, it is still better to fix at least the minimum meaning of `padding`, `stride`, and `dilation`, whose names already appeared above.

All three adjust `how the filter reads across the input`.

| Term | What it changes | Beginner-level intuition |
| --- | --- | --- |
| padding | adds values around the edges of the input | lets us miss the border less and prevents output size from shrinking too fast |
| stride | decides how many cells the filter jumps each time | decides whether to look densely one cell at a time or jump farther by two |
| dilation | increases the spacing between filter cells | lets us see a wider range without increasing the filter size itself |

The differences among the three are the following.

- `padding` is the choice to add margins outside the edges
- `stride` is the choice to determine the step size of the filter movement
- `dilation` is the choice to widen the spacing between cells inside the filter

If we compress this into three ways of reading the same input, it becomes the following.

```mermaid
--8<-- "assets/part-05/chapter-11/filter-reading-options-en.mmd"
```

The result to confirm first in this diagram is that all three change not `what the filter is trying to find`, but `how it sweeps across the input`.

This section does not unfold the three terms into formulas, but when reading the convolution explanation below, it is enough first to hold onto them as devices that adjust `the content of the filter`, `the movement of the filter`, and `the range the filter covers`. The small scene below shows that difference directly.

First imagine that we are reading the same 1D line.

```text
input = [A B C D E]
filter size = 3
```

At that point, the three terms answer different questions.

- padding: `shall we put margins at both ends?`
- stride: `how many cells shall we move at a time?`
- dilation: `shall we read the filter cells right next to one another, or with gaps between them?`

That is, all three are choices that change `how we sweep`, rather than changing convolution itself.

### Why Is Padding Needed

Without padding, the filter cannot go outside the edges of the input, so information near the boundary is relatively easy to read less often.

For example, if we move a 3x3 filter over a 5x5 image as-is, the filter center moves stably only in the inner region rather than on the outer border. In that case, a small line or corner on the border can be reflected less.

Padding is the way of placing one more margin around that outside.

- without a margin, it ends immediately at the border
- with a margin, positions near the border get one more chance to be read

That is, padding creates one more chance to read near the border so that edge information is not lost too quickly.

Written with a very short line example, it becomes:

```text
without padding: [A B C] [B C D] [C D E]
with padding:    [0 A B] [A B C] [B C D] [C D E] [D E 0]
```

The key here is that `the border also gets a chance to be computed`.

### What Does Stride Change

Stride determines how many cells the filter moves at once.

Seen very simply:

- if stride is 1, it moves `one cell at a time` and reads densely
- if stride is 2, it jumps `two cells at a time` and reads more coarsely

For example, if a filter of width 2 reads across a line of length 4:

- with stride 1 it reads with overlap like `[1-2]`, `[2-3]`, `[3-4]`
- with stride 2 it jumps more broadly like `[1-2]`, `[3-4]`

That is, stride is the choice that decides `how densely shall we sweep`. As stride grows, the output size shrinks faster and the computation is summarized more coarsely.

If we reread this in terms of images:

- stride 1: we look at almost every position without skipping
- stride 2: we do not look one by one, but more sparsely

That is, if stride grows, `the output shrinks faster, but detailed position differences are seen less`.

### Why Does Dilation Have Its Own Name

Dilation widens the spacing between filter cells so that a wider range can be seen without making the filter itself larger.

For example, if we place a 3-cell filter normally, it reads directly neighboring cells. But if dilation is added, it can read positions farther apart together, like `first cell`, `a cell after skipping one`, `another cell after skipping one more`.

That is, dilation is:

- a choice that does not greatly increase the number of parameters
- used when we want to see a wider receptive field
- by widening the spacing between cells inside the filter

So dilation is the choice that lets the filter see a wider receptive field by widening the spacing inside it without greatly increasing the number of parameters.

Seen with a 1D line example, the difference becomes even simpler.

```text
without dilation: [A B C]
with dilation:    reads separated positions together like [A _ C _ E]
```

That is, the number of filter cells stays the same, but only `the range seen at once` becomes wider.

If we regroup the three terms again in one line, it becomes the following.

| Term | One beginner sentence |
| --- | --- |
| padding | puts margins outside the border so edge information does not disappear too quickly |
| stride | decides whether the filter will move one cell at a time or jump farther |
| dilation | widens the spacing between filter cells so it can see a wider range together |

At the introductory stage, it is enough to recheck them through the following questions.

- padding: `do we want to let the border be read more too?`
- stride: `shall we read more densely, or jump farther?`
- dilation: `do we want to see a wider range without increasing the filter size?`

### If We Look At All Three Differences Together Through A Small Numeric Example

If we only talk about them in words, the three terms can feel similar, so let us regroup them again through a scene where the same 3x3 filter reads a very small 5x5 input.

```text
input
1 0 0 0 1
0 1 0 1 0
0 0 1 0 0
0 1 0 1 0
1 0 0 0 1

filter
1 0 1
0 1 0
1 0 1
```

At this point, what the reader should look at first is not the `filter values` themselves, but `what position grouping is read at once`.

| Setting | How the scene the filter actually reads changes | Difference that appears first |
| --- | --- | --- |
| padding 0, stride 1, dilation 1 | reads only the inside of the input densely | the border gets fewer chances to be read, and the output becomes 3x3 |
| padding 1, stride 1, dilation 1 | reads with one layer of zero margin around the outside | the border is read one more time too, and the output remains 5x5 |
| padding 0, stride 2, dilation 1 | reads while jumping two cells at a time | the number of reading positions decreases, so the output becomes smaller |
| padding 0, stride 1, dilation 2 | reads more widely with spacing between filter cells | even with the same 3x3 filter, a larger range is covered at once |

That is, all three settings are devices that change not `what the filter finds`, but `with what interval and over what range the filter moves`.

### A Small Example For First Seeing The Difference In Settings

The goal of this small example is to confirm with our eyes how `padding`, `stride`, and `dilation` change the output size and the region actually read. The goal is not to memorize every convolution value, but to hold onto that `even with the same filter, if the scanning method changes, the output shape and the patch being read change together`.

Before reading the code, if we look in order at the following three values first, the structural difference in this section spreads less.

| Value to look at first | Why it should be looked at first |
| --- | --- |
| `shape` | because we can see at a glance how the output size changes first when the setting changes |
| `first_patch` | because we can directly compare what range the filter actually reads at the first position |
| `result` | because in the end we can group together how those first two differences change the full response map |

Input:

- a 5x5 sealing-inspection patch
- a 3x3 filter
- different `padding`, `stride`, and `dilation` settings

Output:

- the shape of the output matrix for each setting
- the patch actually read at the first position
- the convolution result for each setting

Problem situation:

- although the names `padding`, `stride`, and `dilation` sound similar, they make the filter read the image range differently

Concepts to confirm:

- convolution settings change both the result shape and the actual patch range
- when we look at the first-position patch together with the final result, the difference of each setting becomes more visible

Input:

We use the input image, filter, and several `padding`, `stride`, and `dilation` settings summarized above.

```python
# This example compares how padding, stride, and dilation change convolution output shape, the first patch, and result values.
import numpy as np

image = np.array([
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1],
], dtype=float)

kernel = np.array([
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1],
], dtype=float)

def conv2d(image, kernel, padding=0, stride=1, dilation=1):
    padded = np.pad(image, padding, mode="constant", constant_values=0)
    kernel_h, kernel_w = kernel.shape
    effective_h = kernel_h + (kernel_h - 1) * (dilation - 1)
    effective_w = kernel_w + (kernel_w - 1) * (dilation - 1)
    out_h = ((padded.shape[0] - effective_h) // stride) + 1
    out_w = ((padded.shape[1] - effective_w) // stride) + 1
    output = np.zeros((out_h, out_w))

    first_patch = None
    for out_i in range(out_h):
        for out_j in range(out_w):
            row = out_i * stride
            col = out_j * stride
            sampled = padded[
                row:row + effective_h:dilation,
                col:col + effective_w:dilation,
            ]
            if first_patch is None:
                first_patch = sampled.copy()
            output[out_i, out_j] = np.sum(sampled * kernel)

    return output, first_patch

settings = [
    ("base", 0, 1, 1),
    ("padding=1", 1, 1, 1),
    ("stride=2", 0, 2, 1),
    ("dilation=2", 0, 1, 2),
]

for name, padding, stride, dilation in settings:
    result, first_patch = conv2d(
        image=image,
        kernel=kernel,
        padding=padding,
        stride=stride,
        dilation=dilation,
    )
    print(f"[{name}]")
    print("shape =", result.shape)
    print("first_patch =")
    print(first_patch)
    print("result =")
    print(result)
```

In the output, it is enough to look in order at how the shape of the result, the first patch, and the final result values connect to one another.

```text
[base]
shape = (3, 3)
first_patch =
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
result =
[[3. 0. 3.]
 [0. 5. 0.]
 [3. 0. 3.]]
[padding=1]
shape = (5, 5)
first_patch =
[[0. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
result =
[[2. 0. 2. 0. 2.]
 [0. 3. 0. 3. 0.]
 [2. 0. 5. 0. 2.]
 [0. 3. 0. 3. 0.]
 [2. 0. 2. 0. 2.]]
[stride=2]
shape = (2, 2)
first_patch =
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
result =
[[3. 3.]
 [3. 3.]]
[dilation=2]
shape = (1, 1)
first_patch =
[[1. 0. 1.]
 [0. 1. 0.]
 [1. 0. 1.]]
result =
[[5.]]
```

The first points to read from this result are the following.

- `padding=1` keeps the output at 5x5 and leaves the border as a computation target
- `stride=2` makes the filter jump two cells at a time, so the output quickly shrinks to 2x2
- `dilation=2` makes the 3x3 filter actually read a wider 5x5 range sparsely

That is, all three terms do not turn convolution into a `different operation`, but are choices that change `what range and what interval the same convolution uses to read the input`.

## Cases And Examples

### Representative Case. The Intuition Of Edge Detection

Imagine an image where a black line passes across a white background. When people look at this kind of scene, they first try to find `where the line is`. But if a computer only sees the raw pixel numbers as they are, it is hard to immediately distinguish which value change is a line and which value change is only noise. For example, if the line moves only one pixel to the side, the raw numeric array can look completely different. A filter can be made to react strongly exactly at positions where the brightness change is large. Then in the feature map, places with a line or boundary appear as larger values, and the model begins to read `where structure exists` numerically.

So the result to confirm in this case is whether, instead of looking at all raw pixel values at once, positions with boundaries actually first become large in the convolution response and that response becomes the starting point for the next-stage judgment.

The same viewpoint extends directly into equipment-scene images and medical or industrial vision. But the core to hold onto in this section is not the domain name, but `where convolution first creates a large local response and how pooling leaves that response into the next stage`.

If we place the three cases together, it becomes clearer why convolution and pooling should be read not as `the names of two operations`, but as `one flow that separates where a response is created and what is left behind`.

If we regroup the three cases into one line, it becomes the following.

| Situation | Why convolution matters | Why pooling matters |
| --- | --- | --- |
| edge detection | to score where the brightness-change location is | to summarize the strong edge response |
| equipment-scene image | to find local structures such as valve, pipe, and warning-light boundaries | to pass partial responses onward in a more compressed form |
| medical/industrial vision | to find tiny defects or boundaries | to summarize important anomaly signals in a smaller form |

| Standard that is easy for a person to see first | Standard to reread from the convolution/pooling viewpoint |
| --- | --- |
| if the overall image impression looks similar, the internal computation should be similar too | even if only one local boundary differs, the convolution response and pooling result can split strongly |
| pooling feels like a stage that merely throws information away | the key is that instead of keeping every value, it lets strong responses survive into the next-stage judgment |
| it is easy to memorize the names filter, feature map, and pooling separately | in reality `where the response is made`, `where it is recorded`, and `what is left behind` have to connect as one flow |

## Practice And Example

The goal of this example is to confirm, in an automatic inspection scene of packaging seals, how convolution first scores `where the abnormal boundary appeared` and how pooling shows `whether that abnormal signal survives into the next stage`.

Before reading the code, the three values that actually need to be seen in this example are the following.

| Value to look at first | Why it should be seen first |
| --- | --- |
| `normal_conv`, `weak_conv` | because we can directly compare which position response differs between a normal seal and a weak seal |
| `normal_pool`, `weak_pool` | because we can check whether pooling leaves the large response rather than removing it |
| `weak seal max response` | because from the operation viewpoint we want to see how strongly a single local anomaly survives rather than the whole average |

Input:

- a 5x5 scan matrix that simplifies the heat distribution of a normal seal
- a 5x5 scan matrix where part of the seal weakened and the boundary suddenly became unstable
- a 2x2 filter that reacts to left-right change

Output:

- the convolution result for the normal and weak seals
- the max-pooling result for the normal and weak seals
- the position and magnitude where the largest abnormal response remains

Problem situation:

- in production-line automatic inspection, one small boundary anomaly can become the starting point of reinspection or line inspection more than the whole-image average

Concepts to confirm:

- convolution creates location-wise local responses and first reveals `where is it abnormal`
- max pooling can leave the largest abnormal signal even while compressing the local responses
- we see `what changed` more clearly only when we compare the normal scene and the abnormal scene side by side

Before reading the code, it helps to predict what values will split first between the normal seal and the weak seal.

| Comparison point | Result to predict first in the normal seal | Result to predict first in the weak seal |
| --- | --- | --- |
| `normal_conv` / `weak_conv` | the boundary response will be relatively small and even | the boundary response in one specific region will suddenly become larger |
| `normal_pool` / `weak_pool` | even if there is a large response, it will remain in a relatively low range | the largest abnormal response will survive even after pooling |
| maximum response value | it will be at a level that does not strongly suggest reinspection | one local anomaly can become large enough to change the whole judgment |

Input:

We use the scan matrices of the normal seal (`normal_seal`) and weak seal (`weak_seal`) summarized above.

```python
# This example compares convolution local responses and the largest anomaly signal preserved after max pooling for normal and weak seals.
normal_seal = [
    [2, 2, 2, 2, 2],
    [2, 3, 3, 3, 2],
    [2, 3, 4, 3, 2],
    [2, 3, 3, 3, 2],
    [2, 2, 2, 2, 2],
]

weak_seal = [
    [2, 2, 2, 2, 2],
    [2, 3, 3, 3, 2],
    [2, 3, 6, 2, 1],
    [2, 3, 4, 2, 1],
    [2, 2, 2, 2, 2],
]

kernel = [
    [1, -1],
    [1, -1],
]


def convolve_2x2(image, kernel):
    out = []
    for i in range(len(image) - 1):
        row = []
        for j in range(len(image[0]) - 1):
            score = 0
            for di in range(2):
                for dj in range(2):
                    score += image[i + di][j + dj] * kernel[di][dj]
            row.append(float(score))
        out.append(row)
    return out


def max_pool_2x2(feature_map):
    pooled = []
    for i in range(0, len(feature_map) - 1, 2):
        row = []
        for j in range(0, len(feature_map[0]) - 1, 2):
            block = [
                feature_map[i][j],
                feature_map[i][j + 1],
                feature_map[i + 1][j],
                feature_map[i + 1][j + 1],
            ]
            row.append(max(block))
        pooled.append(row)
    return pooled


normal_conv = convolve_2x2(normal_seal, kernel)
weak_conv = convolve_2x2(weak_seal, kernel)
normal_pool = max_pool_2x2(normal_conv)
weak_pool = max_pool_2x2(weak_conv)

print("normal_conv =", normal_conv)
print("normal_pool =", normal_pool)
print("weak_conv =", weak_conv)
print("weak_pool =", weak_pool)
print("weak seal max response =", max(max(row) for row in weak_conv))
```

In the output, it is enough to read in order the response difference between the normal seal and the weak seal, and then whether the strongest abnormal signal remains even after pooling.

```text
normal_conv = [[-1.0, 0.0, 0.0, 1.0], [-2.0, -1.0, 1.0, 2.0], [-2.0, -1.0, 1.0, 2.0], [-1.0, 0.0, 0.0, 1.0]]
normal_pool = [[0.0, 2.0], [0.0, 2.0]]
weak_conv = [[-1.0, 0.0, 0.0, 1.0], [-2.0, -3.0, 4.0, 2.0], [-2.0, -4.0, 6.0, 2.0], [-1.0, -1.0, 2.0, 1.0]]
weak_pool = [[0.0, 4.0], [-1.0, 6.0]]
weak seal max response = 6.0
```

| Output to look at first | What this output means | What changes if you change it |
| --- | --- | --- |
| difference between `normal_conv` and `weak_conv` | even under the same inspection procedure, the boundary response becomes much larger in a specific region of the weak seal | if the abnormal position in `weak_seal` changes, the cell that reacts strongly also moves |
| `6.0` in `weak_pool` | even after pooling, the strongest abnormal signal remains and becomes a next-stage reinspection candidate | if the pooling-window size changes, how coarsely it is summarized also changes |
| difference between the normal scene's maximum response `2.0` and the abnormal scene's maximum response `6.0` | local anomaly scores can matter more for operational judgment than the overall image impression | if the filter direction changes, it can become more sensitive to a different kind of boundary anomaly |

Even when reading output numbers, we have to separate `where was the response created` from `which of those responses survived`.

| Comparison | What first appears in the output | Interpretation that is easy to keep if we only look at the values | Interpretation that changes when we include convolution and pooling |
| --- | --- | --- | --- |
| `normal_conv` vs `weak_conv` | in the weak seal, certain position responses jump to values like `4.0` and `6.0` | it is easy to see only that the numbers became larger | convolution first scores local abnormal boundaries by position, revealing which patch is the problem |
| `normal_pool` vs `weak_pool` | even after pooling, the large response on the weak-seal side remains | it can look as if pooling threw information away and only happened to leave a large value | even without keeping every position, pooling is compressing and passing on the large abnormal signal that matters for the next-stage judgment |
| `weak seal max response` | the maximum value `6.0` becomes the top reinspection candidate | it is easy to think one large maximum alone is enough | the key is not the maximum itself but which local response created by convolution survives after pooling and changes the operational judgment |

- convolution reads each position patch and produces an `abnormal boundary score`
- the collection of those scores becomes the feature map, and the key point is that one position in `weak_conv` suddenly became much larger
- pooling reduces information, but it can still leave the large response that matters for reinspection

That is, this example shows an operating scene where `even if the overall image looks mostly similar, if the boundary response rises sharply at part of the sealing edge, it should be reinspected`. We look at convolution and pooling together not just to memorize the calculation order, but to understand `which local anomaly survives into the next stage`.

In CNN education, convolution and pooling are almost always introduced together. That is because the two of them show the core computational flow of a CNN in the most compressed form.

Historically too, through structures such as LeNet and AlexNet, convolution-based local-pattern detection and pooling-based summarization spread widely as the basic intuition of image recognition. Later structures became more varied, but at the introductory stage this is still the most important basic axis.

It is useful to pause here once and briefly fix `when should we first read how the model sweeps and what it leaves behind rather than the operation names themselves`, so the computational intuition of CNNs spreads less before moving to the next chapter on sequential data.

| Question to recall first | Why the convolution/pooling viewpoint is needed first | What will continue in the next section |
| --- | --- | --- |
| Why do some positions react strongly and others weakly even in the same image? | because convolution turns local pattern fit into a position-wise score | how the next structure reads the feature map |
| Why do we reduce things instead of keeping every detailed position? | because pooling compresses important responses so the next layer can read larger structures more easily | how this differs from the memory structure needed for sequential data |
| Why do we need to understand the difference among padding, stride, and dilation first? | because not only what is being found, but also over what range and interval the input is swept changes the output structure | the comparison that when the input structure changes in later architecture sections, the reading method changes too |

## Checklist

- Can you explain convolution as an operation where a filter scores local patterns?
- Can you explain what convolution and pooling each compute?
- Can you explain why local-pattern reading and summarization appear together?
- Can you explain that convolution is the operation where a small filter computes local-pattern scores?
- Can you describe a feature map as the result in which filter responses are recorded spatially?
- Can you explain pooling not only as `size reduction`, but as `the role of summarizing strong responses and passing them to the next layer`?
- Can you explain that a CNN builds up representations by repeating local-pattern detection and summarization?
- When you know the operation names but it is unclear how the model sweeps across the image and what it leaves behind, can you recall the convolution/pooling viewpoint first?
- Can you say that padding, stride, and dilation are all choices that change `how the filter will sweep`?

## Sources And References

- Yann LeCun et al., `Gradient-Based Learning Applied to Document Recognition`, Proceedings of the IEEE, 1998, checked on 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, `ImageNet Classification with Deep Convolutional Neural Networks`, NeurIPS 2012, checked on 2026-06-29.
