# P6-3.3 Supplement: Embedding Learning That Learns Nearby and Distant Expressions

> Section ID: `P6-3.3`
> Version: `v2026.07.26`

In P6-3.1, we established that embeddings are a representation method that turns tokens and sentences into vectors. In P6-3.2, we held onto the standard for reading those vectors through distance and similarity. Here, we go one step further and organize the big picture of how that vector space is made in the first place.

What often gets mixed up here is `the problem of finding nearby candidates` and `what the system learned to place close in the first place`. The question to close first is the latter: what placement standard the representation space learned.

## Standards for Learning a Representation Space

- What does embedding learning try to place closer, and what does it try to place farther away?
- What do word2vec, GloVe, and sentence embeddings use as representative vectors?
- What learning sense does contrastive learning provide?
- Why should representation-quality problems be separated first from search-speed problems?

Here, first hold onto `the problem of making a good representation space`. The problem of quickly narrowing nearby candidates at practical speed, and the problem of attaching representation space to storage and indexes inside a search system, will broaden again in later sections.

| Current focus | Question that follows | Where to read it broadly again |
| --- | --- | --- |
| Representation learning | What did it learn to place close? | P6-3.3, P6-7.1, P6-8.1 |
| Fast candidate search | How can that representation space be narrowed faster? | P6-3.4, P6-13.1, P6-13.2 |

So the central question is `how embeddings learn to place similar things close`.

## Separating Representation-Space Learning from Fast Candidate Search

- You can explain embedding learning as `the problem of making a representation space`.
- You can distinguish representative embedding families by purpose.
- You can explain contrastive learning as a flow that learns both `what should become closer` and `what should become farther`.
- You can separate representation-quality problems from search-speed problems as different levels.

## Why Look at Learning Separately?

Once you can read `nearby candidates` in P6-3.2, it is easy to form the misunderstanding, `then isn't it enough to choose nearby things first?` But there is a question that must be asked before that.

`What did that vector space learn to place close in the first place?`

If inquiries with the same meaning keep scattering into different candidate groups, this may be a representation-space problem before it is a search-speed problem. Conversely, if sentences pointing to the same problem scene gather well but responses are slow, then the search-speed problem comes first.

## What Do Representative Embedding Families See Differently?

Read representative families as follows.

| Family | Introductory intuition | What becomes the representative vector |
| --- | --- | --- |
| word2vec | Learns word representations from surrounding context | Word |
| GloVe | Reflects co-occurrence statistics more directly | Word |
| sentence embedding | Makes a whole sentence into a comparable vector | Sentence, paragraph |

The core of this distinction is not memorizing names. What is needed first is seeing `what you want to make into one comparison unit`.

For example, in FAQ search, it is usually more natural to use a sentence or paragraph as the comparison unit than one word. Conversely, when explaining the first intuition of embeddings, it is easier to start from surrounding context around words.

## What Sense Does Contrastive Learning Give?

If contrastive learning is reduced to the shortest form, it asks the following two questions together.

- What pairs should become close?
- What pairs should become far apart?

For example, it can learn to place:

- `Can I get a refund?` and `How do I cancel my payment?` close
- `Can I get a refund?` and `I want to change my shipping address` far apart

In other words, contrastive learning is closer to learning the placement `same problem scenes close, different problem scenes far apart` than to memorizing one answer sentence.

## How Do Representation-Quality Problems Appear?

Representation-quality problems usually appear first in the scenes below.

| Phenomenon first seen | What to suspect first in practice |
| --- | --- |
| Inquiries with the same intent scatter into different candidate groups | Are similar sentences actually placed close? |
| Sentences about different problems often mix into one candidate group | Are sentences that should be far enough separated? |
| Odd candidates increase only when specific domain terms appear | Does the learned space distinguish those domain expressions properly? |

What matters here is not lumping everything together as `search is strange`. First check `whether the space was placed incorrectly`, because the next action changes depending on that.

## Cases and Examples

### Case 1. When Same-Intent Inquiries Scatter

Suppose a customer center receives sentences such as `Can I get a refund?`, `How do I cancel my payment?`, and `I want my money back`. If the same words are absent, they can easily look like different inquiries.
But in the actual handling flow, it is more natural for these three to first gather into the same candidate group.

This case supports this section because it shows that the core of embedding learning is not `finding the same words`, but `placing expressions that point to the same resolution flow closer`. From the contrastive learning view, the refund inquiries above are close to positive pairs, while a sentence such as `I want to change my shipping address` is close to a negative pair.

The result to check here is whether `the same resolution flow` is placed closer than surface words.

The judgment to close in this case is not `same words`, but `same resolution flow`. Refund inquiries should become close to each other, and address-change inquiries should become far away, so representation placement quality must be checked before search speed.

### Case 2. When Candidates Suddenly Shake After Domain Terms Change

Search that worked well for general inquiries can suddenly shake when internal terms such as `settlement deadline`, `policy exception`, and `approval routing` appear. The misunderstanding to pass beyond first in this scene is the thought that `it is because search is slow or the index is weak`.

In reality, the learned space may not have sufficiently captured how those expressions should be close inside the same domain. For example, if `approval routing` and `approval-line assignment` are close expressions in the same work flow but are placed far apart, the same-meaning candidate will not rise stably no matter how fast search becomes.

This case supports this section because it shows that embedding quality does not end with general language sense. It depends on which domain expressions the model learned to place close to each other.

The judgment to close in this case is not flattening domain expressions into a general search failure. First check whether expressions in the same work flow are actually close, then pass speed improvement or ANN adjustment to the next problem.

### Case 3. When Speed Improves but Candidates Stay Wrong

If ANN is applied more aggressively and speed improves, but the top candidates remain wrong, the problem may be representation quality rather than speed. A system that shows wrong candidates faster makes users feel the failure immediately.

So the sentence to close first in this case is this.

`If the representation space is unstable, the root problem remains even if search becomes faster.`

This case supports this section because it shows that `how the representation space was learned` and `how fast that space is searched` are different levels. If similar sentences were placed far away in the first place, ANN only searches that incorrect placement faster.

The judgment to close in this case is separating representation quality from search speed. If candidates are wrong, check placement quality before speed. ANN improvement becomes more meaningful only after the representation space is stable enough.

If we group the three cases again, they become the following.

| Situation | What should improve first | Misunderstanding not to mix in |
| --- | --- | --- |
| Same-intent inquiries scatter | Placement in the representation space | Treating different words as different problems |
| Domain terms shake results | Distinguishing domain expressions | First concluding it is an index problem |
| Speed improved but candidates are wrong | Representation quality | Treating speed improvement as quality improvement |

## Separating Representation-Space Placement Problems

If you look at practical phenomena again from the representation learning view, even before you can write training code directly, you can first separate `whether the thing shaking now is a placement problem` as below.

| Phenomenon you see now | Misunderstanding easy to recall first | Question to ask instead first |
| --- | --- | --- |
| Similar inquiries scatter into different candidate groups | It is easy to feel that search is slow or the index is weak | Are sentences with the same intent actually placed close to each other? |
| Completely different inquiries appear together in the same candidate group | It is easy to pass it over as normal because there are several top candidates | Are sentences that should be far apart separated enough? |
| Quality drops sharply only for certain domain expressions | It is easy to feel that nothing can be done because they are exceptional inputs | Does the learned space separately distinguish those domain expressions? |

The purpose of this table is not to make you memorize more algorithm names. It is to avoid lumping everything into one sentence, `search is strange`, and first make you briefly ask `was the representation space placed incorrectly`.

## Practice and Examples

The goal of this practice is to place `pairs that should become close` and `pairs that should become far` together, then visually confirm why this is the core sense of representation learning. Before writing actual training code, just judging positive pairs and negative pairs from inquiry sentence pairs can hold the placement standard of a representation space.

First look at the following sentences.

| Sentence ID | Sentence |
| --- | --- |
| `refund_a` | `Can I get a refund?` |
| `refund_b` | `How do I cancel my payment?` |
| `address` | `I want to change my shipping address` |

If these sentences are grouped from the representation learning view, they can be read as follows.

| Pair | Label | Why read it this way |
| --- | --- | --- |
| `refund_a` <-> `refund_b` | positive pair | Surface words differ, but they point to the same refund resolution flow. |
| `refund_a` <-> `address` | negative pair | One is a refund problem, and the other is a shipping-address-change problem. |

The core to read in this example is not numerical calculation.

- Positive pairs should become closer.
- Negative pairs should become farther apart.
- If this placement shakes, same-intent sentences will not gather well in one candidate group no matter how much search latency is reduced.

After reading the example, answer the questions below first. For each question, answer by yourself first, then compare with the explanation immediately on the right.

| Question | Explanation |
| --- | --- |
| Why are `refund_a` and `refund_b` a positive pair? | The two sentences have different surface words, but they point to the same refund resolution flow. From the representation learning view, same-intent sentences should be placed close, so they are treated as a positive pair. |
| Why are `refund_a` and `address` a negative pair? | One is a refund problem, and the other is a shipping-address-change problem. If they mix into the same candidate group, search quality shakes, so they are treated as a pair that should become far apart. |
| What do we not check yet in this example? | Actual ANN speed or index structure is not checked. The center is not how to find quickly, but what the model learned to place close. |

### Exercise 1. Judge Positive and Negative Pairs

Observations:

| Sentence ID | Sentence |
| --- | --- |
| `billing_a` | `I want to check this month's payment history` |
| `billing_b` | `Please tell me where this billed amount came from` |
| `login_a` | `I forgot my password` |
| `refund_a` | `Can I get a refund?` |

Answer by yourself first.

- Which positive-pair candidate should become closest to `billing_a`?
- Which negative-pair candidates should become far from `billing_a`?
- Is this judgment a search-speed problem or a representation-space placement problem?

Explanation: The candidate that should become closest to `billing_a` is `billing_b`. Both point to the same cost-checking flow: payment history and billed amount. `login_a` and `refund_a` are a login problem and a refund problem, so they are negative-pair candidates that should become far from `billing_a`. This judgment is not a search-speed problem. It is a problem of which sentences should be learned as close in the same space.

### Exercise 2. Find Incorrect Learning Signals

Observations:

| Learning pair | Current label |
| --- | --- |
| `Can I get a refund?` <-> `How do I cancel my payment?` | negative |
| `I forgot my password` <-> `I cannot log in` | positive |
| `Can I get a refund?` <-> `I want to change my shipping address` | positive |

Answer by yourself first.

- Which pairs are mislabeled?
- What problem can wrong labels create in the representation space?
- Why can't this problem be solved by search-speed tuning?

Explanation: The first pair is the same refund resolution flow, so it is closer to positive, not negative. The third pair is refund and shipping-address change, so it is closer to negative, not positive. If these labels enter incorrectly, sentences that should become close become far away, and sentences that should become far mix into the same candidate group. This is a wrong placement signal in the representation space, so increasing search speed only finds incorrectly placed candidates faster.

### Exercise 3. Separate Representation Quality from Search Speed

Observations:

| Phenomenon | Level to suspect first |
| --- | --- |
| Same-intent inquiries scatter into different candidate groups | ? |
| Candidate quality is good, but response time is too long | ? |
| Wrong candidates increase only for inquiries with domain terms | ? |

Answer by yourself first.

- Is each phenomenon a representation-quality problem or a search-speed problem?
- Why do actions go wrong if the two levels are mixed?

Explanation: The phenomenon where same-intent inquiries scatter is a representation-quality problem. The phenomenon where candidate quality is good but response time is long is closer to a search-speed problem. The phenomenon where wrong candidates increase only with domain terms is a representation-quality problem caused by insufficient placement of domain expressions. If the two levels are mixed, actions drift: tuning only the index when the representation space is unstable, or conversely misunderstanding good-quality but slow candidates as a learning problem.

So the final judgment of this section is simple. If candidates are wrong, first check whether the representation space actually places similar sentences close. Move to a search-speed problem only when candidate quality is good but late.

## Checklist

- Can you explain embedding learning as `the problem of making a good representation space`?
- Can you distinguish word2vec, GloVe, and sentence embeddings by `what becomes the representative vector`?
- Can you explain contrastive learning as a flow that learns both `what should become closer` and `what should become farther`?
- Can you first separate representation-quality problems from search-speed problems?

## Sources and References

- Tomas Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-07-19. Used as background evidence for word representation learning in the word2vec family.
- Jeffrey Pennington, Richard Socher, Christopher D. Manning, [GloVe: Global Vectors for Word Representation](https://aclanthology.org/D14-1162/){: target="_blank" rel="noopener noreferrer" }, EMNLP 2014, accessed 2026-07-19. Used as evidence for word vector learning that reflects global word-word co-occurrence statistics.
- Ting Chen et al., [A Simple Framework for Contrastive Learning of Visual Representations](https://proceedings.mlr.press/v119/chen20j.html){: target="_blank" rel="noopener noreferrer" }, ICML 2020, accessed 2026-07-19. Used as background evidence for explaining contrastive learning as a representation-placement sense involving positive and negative pairs.
- Nils Reimers, Iryna Gurevych, [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084){: target="_blank" rel="noopener noreferrer" }, arXiv, 2019, accessed 2026-07-19. Used as background evidence for learning sentence embeddings with siamese/triplet structures and similarity comparison.
