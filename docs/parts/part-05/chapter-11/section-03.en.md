# P5-11.3 Supplementary Reading: Comparing CNNs and Vision Transformers

> Section ID: `P5-11.3`
> Version: `v2026.07.26`

In P5-11.1 and P5-11.2, we first saw why convolutional neural networks (CNNs) fit images well, and what roles convolution and pooling play. From there the next question appears naturally.

What is different about the Vision Transformer (ViT), which is often mentioned after CNNs, and why is it useful to know this difference before trying to understand later generative AI and multimodal models?

When you need to briefly confirm again the different starting unit of a Vision Transformer, return to the glossary entry on [ViT (Vision Transformer)](/AiBook/en/reference/concept-glossary-alpha/v/#vit-vision-transformer).

## The Input Unit That Separates CNNs From ViTs

- How do CNNs and ViTs begin reading an image?
- What is the difference between reading centered on local patterns and reading centered on token relations?
- Why does this difference prepare us for later understanding of attention, Transformers, and generative AI?

This supplementary reading compares CNNs and ViTs through the question `with what computational unit do they begin reading an image`. The goal is not to explain a long model genealogy, but to help us first hold onto that later even images are read through the viewpoint of `input cut into token-like units` and `relation computation`.

The self-attention inside ViT reconnects later in P5-13.2 and P5-14.1. Here we organize only the initial difference between `do we first read local patterns` and `do we first read patch relations` from the image viewpoint, and why that difference is useful when moving toward generative AI.

## Distinguishing Local Patterns from Patch Relations

- You can compare the starting unit with which CNNs and ViTs read images.
- You can distinguish the CNN style of local-pattern-centered reading from the ViT style of patch-relation-centered reading.
- You can say what intuition patch tokens and self-attention give in image interpretation.
- You can connect why the viewpoint `treat the input like tokens` keeps returning in later sections on attention, Transformers, and generative AI.

## From the CNN Intuition to the ViT Intuition

1. First recall the starting point already familiar from CNNs: `read local patterns`.
2. Then compare how ViT splits an image into patch tokens and reads relations through attention.
3. Finally organize why this comparison prepares us for later Transformer-family models and generative-AI input interpretation.

## If We Compare in One Line First

| Structure | The first intuition for reading an image |
| --- | --- |
| CNN | repeatedly reads small local patterns |
| ViT | splits the image into patch tokens and reads relations among the tokens with attention |

This one line becomes the standard to return to later when the question `can images also be treated like tokens?` appears.

## What Feels Natural in CNNs

CNNs directly reflect into the structure the fact that nearby pixels in an image create meaning together.

- they first read small local clues such as edges, corners, and textures
- build those upward into larger partial structures
- and repeatedly apply the same filter at many positions

So CNNs fit well with the intuition that `local patterns matter in images`.

## What Feels Different in ViTs

ViTs split the image into small patch pieces, then treat each patch like a token. They then read, through attention, what relation each patch has with other patches.

The phrase that first needs to be unpacked here is `treating patches like tokens`. Just as tokens are the small units that make up a sentence in a language model, in a ViT the image is split into small square pieces, and each piece is treated as the basic computational unit.

That is, ViT does not start from `a 3x3 filter sweeping over neighboring pixels`, but from `splitting an image into many tiles and treating each tile as one input unit`.

So ViT is a structure that turns the image into patch-level tokens and computes the relations among those patches with attention.

- it splits the image into many small pieces
- it sees each piece as one token
- it uses attention to compute which pieces become important together with which other pieces

Written in a very simple flow, it becomes the following.

```mermaid
--8<-- "assets/part-05/chapter-11/vit-patch-flow-en.mmd"
```

This diagram compresses the order in which an image is grouped into relation computation among patches and then into a representation.

1. The image is split into small pieces.
2. Each piece is turned into one numeric vector.
3. Attention computes how much each piece refers to the other pieces.
4. Those results are combined and passed on to a representation describing the whole image.

That is, ViT is a structure that places into the computational flow from the beginning the question `what relation does this patch form with that patch`.

If we think of it as a very simple picture of four cells, it becomes the following.

| Stage | Introductory intuition |
| --- | --- |
| original image | one equipment photo where a tank and valve are seen together |
| patch split | split the photo into 4 or 16 small tiles |
| patch token | start reading each tile as one numeric vector |
| attention | check whether the tile containing the valve and the tile containing the tank body become important together |

That is, rather than assuming first only `relations immediately next to each pixel`, ViT more directly asks `how related is this piece to that piece`. This point also reconnects smoothly later when reading Transformer-family generative models.

If the CNN feels like `starting nearby and then rising to larger structure`, ViT is closer to `directly reading the relations among pieces`.

`CNNs stack local patterns upward, while ViTs try to read relations among patch tokens directly.`

## Why Is It Important That the Image Is Cut into Patches

When first reading a ViT, the most confusing point is often `why do we have to split the image into pieces at all?`

The core reason is that attention is a structure that computes `relations among input units`. In a sentence, the input units are tokens. In an image, patches take that role.

- In a sentence, word pieces form relations with one another.
- In ViT, image pieces form relations with one another.

That is, a patch is not just a preprocessing trick. It is the answer to the requirement that `even in images, attention needs a basic unit to read`.

The key point is that a patch is the starting point that turns a small region of the image into a basic vector unit that attention can read.

- one patch is one small square region of the image
- one patch later becomes one numeric vector
- attention computes how related those patch vectors are to one another

If the patches are made too small, the amount of computation grows. If they are made too large, fine local information can be blurred. Such design choices and learning recipes are details of ViT implementation, so we do not cover them in this section. For now, it is enough to firmly fix only the point that `ViT uses patches as its input units`.

If we reread this against a CNN, the difference becomes clearer.

- In a CNN, a small filter sweeps over `pixels nearby`.
- In a ViT, an already cut patch `becomes the basic reading unit from the start`.

That is, if the first question of a CNN is closer to `is there an edge or texture around here?`, then the first question of a ViT is closer to `what relation does this patch form with other patches?`

This difference continues exactly when reading later generative AI. In generative AI, text is split into tokens, images are also converted into units such as patches or latent tokens, and structures that compute relations among those units appear repeatedly. So if we first hold onto here `with what unit is the image split and read`, then even if model names change later, the basic viewpoint for interpreting the input shakes less.

## If We Place the Starting Units of CNN and ViT Side by Side

| Question | CNN | ViT |
| --- | --- | --- |
| unit touched by the first computation | a small receptive field | an already cut patch |
| what is emphasized first | local patterns among nearby pixels | relations among patches |
| change expected as layers deepen | reads larger part structures | reads broader patch relations |

## What Is Prepared If We Continue Toward Generative AI

The reason this section appears right after the CNN chapter is not only `it is useful to know ViT too`. The more important reason is to build in advance the intuition that even images can later be treated as `inputs split like tokens`.

One reason generative AI feels suddenly difficult to beginners is that we talk about tokens in text, but then expressions such as patches, latents, and multimodal tokens suddenly appear in images. But the underlying questions are not that different.

- Into what units should the input be split?
- Into what vector representation should those units be turned?
- By what method should the relations among those units be computed?
- How are the results passed into the next generation, classification, or explanation stage?

CNNs are closer to answering these questions by placing `nearby pixels and local patterns` first. ViTs are closer to answering them by placing `already cut patch tokens and their relations` first. When reading generative AI, the ViT-side viewpoint tends to reappear more often, because in image-generation models, vision-language models, and multimodal chatbots, structures that convert the input into regular units, compute relations among them, and sometimes handle them together with text tokens are repeated.

Of course, not every generative-AI model uses exactly the same structure as ViT. Some models read images as patch tokens, some use representations that have passed through a CNN-family encoder, and some use token-like units in a latent space. Even so, the common question the reader should hold onto first is the same. It is more productive to ask not `is the image processed as one whole block at once`, but `into what input units is it divided, and how are the relations among those units computed`.

If we place this viewpoint side by side with text and image inputs, it can be read as follows.

| Question | Text input | Image input (CNN intuition) | Image input (ViT intuition) |
| --- | --- | --- | --- |
| unit split first | token | nearby pixels in a small local window | patch token |
| what is emphasized first | token order and context relation | local patterns of nearby positions | relations among patches |
| question that becomes important later | which token connects to which other token | which position's local clue reacts first | which patch becomes important together with which other patch |
| preparation for generative AI | reading token-level input | intuition of local-feature extraction | intuition of tokenized image input and relation computation |

The purpose of this table is not to force text and images to be called the same thing. Rather, it is to show the shared frame that even for different inputs, we `split the input into basic units and compute the relations among those units`. Once that frame is fixed first, when expressions such as `text token`, `image token`, `patch embedding`, `vision encoder`, and `multimodal token` appear later, they can be organized again under the same question instead of being memorized separately.

## Cases and Examples

### Case 1. How Valves And Main Bodies Are Read In A Pipe Photo

Suppose we classify valve states from a pipe photo. At first, people easily think first of whether visible parts such as the valve handle, the pipe body, or the metal outline can be seen.

- From the CNN viewpoint, local responses such as valve boundaries, metal textures, and pipe outlines are captured first, and then those responses are stacked into a larger equipment representation across layers.
- From the ViT viewpoint, we can think more directly about whether the patch containing the valve and the patch containing the pipe body become important together through a certain relation.

| Question | What CNN sees first | What ViT establishes first |
| --- | --- | --- |
| when reading the valve and pipe body in a pipe photo | local responses such as valve boundaries, metal textures, and pipe outlines | whether the patch containing the valve and the patch containing the pipe body form the same piece of equipment together |

So the result to confirm in this case is not merely `do they both identify the pipe`, but whether CNNs pose the initial question `which local position reacts strongly first`, while ViTs pose the different initial question `which patch relation becomes important together`.

```mermaid
--8<-- "assets/part-05/chapter-11/cnn-vit-valve-body-case-flow-en.mmd"
```

This diagram compresses Case 1 again into `the same input -> CNN's local-clue question -> ViT's patch-relation question`, so that we can read at once where the two begin from different judgment starting points.

What matters in this comparison is not to split them too simply into `CNN looks at parts` and `ViT looks at the whole`. Both eventually go toward judging the whole image, but their starting intuitions differ in whether they are `local-pattern-centered` or `patch-relation-centered`.

This difference also matters immediately when connecting to generative AI. Later, when we encounter structures that split images like tokens, read the relations among many tokens with attention, and handle them together with text tokens, we are prepared here in advance for `why images can also be represented this way`.

## Practice and Example

The goal of this example is to compare on the same inspection frame how `local defect candidates` and `relations among distant regions` are read differently when we divide it through a CNN-like reading and a ViT-like reading. It does not implement a full CNN or ViT model, but it lets us directly see into what computation units the same frame is changed in the two structures.

Problem situation:

- even for the same inspection frame, a CNN starts from densely sweeping small defect candidates, while a ViT starts from comparing relations among larger region tokens

Input:

- a 6x6 inspection frame that contains a label-printing region, a blank background region, a sealing region, and a code region together
- 2x2 local patches read by the CNN
- 3x3 patch tokens read by the ViT

Output:

- top local defect candidates extracted in the CNN style
- patch-token means by region in the ViT style
- the differences between the code-region token and the other region tokens

Concepts to confirm:

- CNNs first read partial defect candidates by following overlapping local patches
- ViTs start by making non-overlapping patch tokens and comparing the relations among separated regions
- even for the same input, `what anomaly signal appears first now` changes depending on what computational unit the input is turned into

The `patch token mean` on the ViT side here is not a real patch embedding or self-attention result. Real ViTs project patches into vectors, add positional information, and then compute relations through many attention layers. This example shortens that process and confirms only `what kind of region-comparison question appears first when we turn the image into large non-overlapping patch units`.

Input:

We use the 6x6 packaging-inspection frame and the CNN/ViT-style split rules summarized above.

Before reading the code, there is one question to hold onto first. If we put the same frame into the two structures, the CNN places first `which small position jumps first`, while the ViT-side auxiliary computation places first `which region relation separates first`.

```python
# This example compares which anomaly signals appear first from overlapping CNN local scores and non-overlapping ViT-style patch-token means on the same inspection frame.
inspection_frame = [
    [4, 4, 4, 1, 1, 1],
    [4, 5, 4, 1, 2, 1],
    [4, 4, 4, 1, 1, 1],
    [2, 2, 2, 3, 3, 3],
    [2, 2, 2, 3, 8, 3],
    [2, 2, 2, 3, 3, 3],
]


def cnn_local_scores(image, window=2, stride=1):
    patches = []
    for i in range(0, len(image) - window + 1, stride):
        for j in range(0, len(image[0]) - window + 1, stride):
            values = []
            for di in range(window):
                for dj in range(window):
                    values.append(image[i + di][j + dj])
            local_score = max(values) - min(values)
            patches.append(((i, j), local_score, values))
    return sorted(patches, key=lambda item: (-item[1], item[0]))


def vit_patch_tokens(image, patch_size=3):
    tokens = []
    for i in range(0, len(image), patch_size):
        for j in range(0, len(image[0]), patch_size):
            values = []
            for di in range(patch_size):
                for dj in range(patch_size):
                    values.append(image[i + di][j + dj])
            mean_value = round(sum(values) / len(values), 2)
            tokens.append(((i, j), mean_value, values))
    return tokens


cnn_candidates = cnn_local_scores(inspection_frame, window=2, stride=1)[:5]
vit_tokens = vit_patch_tokens(inspection_frame, patch_size=3)
token_means = {position: mean for position, mean, _ in vit_tokens}

print("[cnn top local candidates]")
for position, score, values in cnn_candidates:
    print("position =", position, "score =", score, "values =", values)

print("[vit patch tokens]")
for position, mean, values in vit_tokens:
    print("position =", position, "mean =", mean, "values =", values)

print("seal_code_gap =", round(abs(token_means[(3, 0)] - token_means[(3, 3)]), 2))
print("blank_code_gap =", round(abs(token_means[(0, 3)] - token_means[(3, 3)]), 2))
```

In the output, first look at how the CNN's top local defect candidates and the ViT's region-token summaries raise different first questions.

```text
[cnn top local candidates]
position = (3, 3) score = 5 values = [3, 3, 3, 8]
position = (3, 4) score = 5 values = [3, 3, 8, 3]
position = (4, 3) score = 5 values = [3, 8, 3, 3]
position = (4, 4) score = 5 values = [8, 3, 3, 3]
position = (0, 2) score = 3 values = [4, 1, 4, 1]
[vit patch tokens]
position = (0, 0) mean = 4.11 values = [4, 4, 4, 4, 5, 4, 4, 4, 4]
position = (0, 3) mean = 1.11 values = [1, 1, 1, 1, 2, 1, 1, 1, 1]
position = (3, 0) mean = 2.0 values = [2, 2, 2, 2, 2, 2, 2, 2, 2]
position = (3, 3) mean = 3.56 values = [3, 3, 3, 3, 8, 3, 3, 3, 3]
seal_code_gap = 1.56
blank_code_gap = 2.45
```

Because the same frame begins making representations from different starting points, even later when we read attention and patch embedding, we should look together at `what is being treated like a token`.

If we view the CNN-style 2x2 local scores as a map, overlapping windows around the code region continuously become the top candidates. The first question that appears here is `which small position should be inspected again?`

![CNN-style 2x2 local-candidate score map](/AiBook/assets/part-05/chapter-11/cnn-vit-cnn-local-score-map-en.png)

If we imitate the ViT-style starting unit by looking separately at 3x3 patch means, the same frame is summarized into four large regions. These mean values are not real ViT attention values. They are auxiliary values that show what region-comparison question appears first when we start from patch tokens.

![ViT-style 3x3 patch-token mean map](/AiBook/assets/part-05/chapter-11/cnn-vit-patch-token-mean-map-en.png)

| Output to look at first | What this output means | What changes when we vary it |
| --- | --- | --- |
| CNN top candidates cluster around `(3, 3)` | it means CNN first strongly reveals `the local anomaly in the middle of the code region` | if we change the `window` size or `stride`, the density of local-defect candidates changes |
| the `(3, 3)` region is high at `3.56` in the ViT-style auxiliary patch mean | it means that if the whole code region is summarized as one patch unit, a starting point appears for comparing it with other regions | if we make `patch_size` smaller, it is split more finely, and if larger, the region summary becomes coarser |
| `seal_code_gap` and `blank_code_gap` are both computed | it means that in a patch-unit start, the question of comparing differences among separated regions appears naturally | if we compare different region pairs, we can read `which relation looks anomalous` in a different way |

Even when reading the output numbers, we should separate `which position rises first` from `which region relation spreads farther apart`.

| Comparison | What appears first in the output | The meaning to hold onto in this comparison |
| --- | --- | --- |
| CNN top candidates | the 2x2 windows around `(3, 3)` appear continuously at the top | it means a CNN is a structure that sweeps overlapping local windows and first establishes `which small position is the reinspection candidate` |
| patch-unit auxiliary values | the `(3, 3)` patch is summarized at mean `3.56`, while the `(0, 3)` patch is summarized at `1.11` | it means that if the image is turned into patch units, the question `how is this region different from another region` comes to the front |
| `seal_code_gap` vs `blank_code_gap` | the code-to-blank gap becomes larger than the code-to-seal gap | it means that on the ViT side, relation questions such as `which region is more misaligned with which other region` naturally come to the front |

That is, the core of this comparison is that a CNN starts from overlapping moving local windows and first creates `which place should be rechecked`, while a ViT starts from already cut patch tokens and continues toward comparing `which regions are more relationally misaligned`.

In this example, we can enlarge the `inspection_frame` or change `patch_size` and `stride`. Then, instead of only memorizing the sentence `CNN is partial, ViT is patch-based`, readers can directly compare into how many `local defect candidates` and how many `region-token relations` the same input is changed. This intuition also continues later when reading image token count, patch size, and multimodal input units in generative AI.

## How Does It Connect to Self-Attention

To understand ViT as an image Transformer, the connection `it treats patches like tokens, so self-attention can be used` must be visible after the phrase `patches like tokens`.

- In a sentence, tokens refer to one another.
- In ViT, patch tokens refer to one another.
- So self-attention can also be applied to images.

That is, ViT can be seen as a case showing that `the attention mechanism that was originally used in language can also be brought over to the problem of reading images`.

This connection matters especially when reading generative AI. Later, in text-generation models, image-description models, and multimodal question-answering models, even when the inputs differ, attention keeps appearing as the computation of `what refers to what among the units`. If we first see through ViT that images can also enter that computational frame, then later it becomes more natural to accept why attention expands beyond language.

However, we do not first deal here with the self-attention equation itself and the Q, K, V expansion. That core structure is organized again in P5-13.2, and the whole Transformer flow is revisited in P5-14.1.

## What Should We Remember for Generative AI

It is enough to remember a table like the following.

| Question | CNN | ViT |
| --- | --- | --- |
| what is emphasized first | local patterns | patch-token relations |
| core computational intuition | convolution + pooling | self-attention |
| the feel of the image explanation | rises from small parts to larger structure | directly reads relevance across many patches |
| preparation that continues toward generative AI | intuition of input based on local clues | intuition of tokenized image input and relation computation |

Once it is organized to this level, the preparatory sentences we can take directly from this section into generative AI are the following.

1. Images can also be split and read by some basic unit, just like text.
2. Depending on what that unit is, the model's starting question changes.
3. The ViT viewpoint lets us read image input in the frame of tokens and relation computation.
4. So later, when we meet terms such as image token, multimodal token, and vision encoder, they do not feel like a completely new language.

## Why Is This Important in the Flow of Part 5

This supplementary reading is needed because in the later part of Part 5 we learn about attention and Transformers, and after that terms such as `token`, `relation`, and `multimodal input` keep returning in generative AI.

- In P5-11, we first fix why CNNs are natural in images.
- In P5-13 and P5-14, we learn why attention and Transformers became turning points.
- Only then does the connection become more natural that `attention-family structures can also be used in images`, and `images can also be treated like tokens`.

That is, this supplementary reading is not a document that erases CNNs and jumps directly to ViT. It is the place where we organize in advance that the `image structure based on local patterns` and the `token-relation structure` begin from different problem settings.

If we pause here once and briefly fix `when is the CNN explanation alone not enough, and when should we separately bring up the ViT comparison viewpoint`, the connection with the later attention and Transformer sections becomes more stable.

| Question to think of first | Why the CNN-vs-ViT comparison viewpoint is needed first | What later sections continue from here |
| --- | --- | --- |
| why do image-attention structures not feel completely unfamiliar when they suddenly appear? | because if we fix in advance the starting difference of patch tokens and relation reading, we can connect attention even in the image context | the general computational structure of self-attention and Transformers |
| why should CNNs and ViTs not be read as a simple old-vs-new comparison? | because they differ in the first computation unit with which they read images and the relation they assume | by what question we read attention-based vision structures |
| why does the word patch become important? | because an image also needs a basic unit that can be treated like a token so that attention structures can be applied | patch tokens, self-attention, image-Transformer expansion, and multimodal input reading |

## Checklist

- Can you explain how the unit with which CNNs and ViTs begin reading images is different?
- Can you describe at the introductory level the difference between starting from local patterns and starting from tokens/patches?
- Can you explain that CNNs repeatedly read local patterns, while ViTs first treat image patches like tokens and then read relations among patches through attention?
- Can you explain CNNs and ViTs through the starting difference between `local-pattern-centered` and `patch-relation-centered` reading?
- Can you explain a patch not as a mere preprocessing trick, but as `the basic unit attention reads in an image`?
- When the attention-based image structure feels unfamiliar from the CNN explanation alone, can you think first of the CNN-vs-ViT comparison viewpoint?
- When trying to read CNNs and ViTs only as an old-vs-new comparison, can you bring back again the starting difference between local-pattern-centered and patch-relation-centered reading?
- When reading the later attention section, are you ready to think first `can image pieces also form relations like tokens`?

## Sources and References

- Alexey Dosovitskiy et al., `An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale`, ICLR 2021, URL: [https://openreview.net/forum?id=YicbFdNTTy](https://openreview.net/forum?id=YicbFdNTTy){: target="_blank" rel="noopener noreferrer" }, checked on 2026-06-30.
- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, URL: [https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }, checked on 2026-06-30.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-30. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
