# P6-3.1 Embeddings That Turn Token IDs into Comparable Coordinates

> Section ID: `P6-3.1`
> Version: `v2026.07.26`

In Chapter P6-2, we saw that an LLM reads text in token units, and that token length connects directly to cost and context length. But token numbers alone cannot let the model compute meaning, so tokens must soon be changed into another numerical representation.

What numerical representation does tokenized input become inside the model? An embedding is a representation method that turns tokens or sentences into vectors the model can compute with.

The first thing to separate here is `assigning a number` and `turning something into comparable coordinates`. A token ID is a number that points to an item in a vocabulary, while an embedding vector is a coordinate representation that lets that item be compared and computed with other representations.

## Token Numbers Become Vector Representations

When first reading embeddings, hold onto the questions below.

- What kind of representation is an embedding for?
- How are token IDs and embedding vectors different?
- What intuition explains the phrase `similar meanings become close`?
- Why do embeddings seem like a common foundation for LLMs and search services?

Here, first hold embeddings as `a foundation that turns tokens or sentences into computable vector representations`. Family-specific training backgrounds, fast search structures, and RAG connections will be handled more broadly in later sections, but the starting point needed now is why token IDs and vector representations are different.

An embedding is not `a magical meaning storehouse`. It is a representation method that places text in a space the model can compute over. The core is moving away from the idea that token numbers themselves contain meaning, and understanding that they are changed into vector representations later computation can use.

| Focus at this stage | Already established | What follows later |
| --- | --- | --- |
| Internal representation level of the model | Tokens and tokenization | Semantic distance, vector search, and the foundation of RAG |

## Separating Token IDs from Embedding Vectors

If Chapter P6-2 established `what tokens are` and `why length and cost matter`, we now need to see how those tokens become vectors and connect to model computation and search. The understanding needed here is not memorizing complex formulas first, but reading `token ID`, `embedding vector`, and `comparison result between vectors` as different levels.

## How Are Token IDs and Embeddings Different?

After tokenization, text can first be changed into discrete indexes such as token IDs.

For example:

- `"AI"` -> `1042`
- `"model"` -> `3881`

These numbers themselves have almost no meaning. They are only numbers pointing to items in a vocabulary.

An embedding goes one step further here. It changes each token into a vector made of multiple numbers.

Intuitively, you can think of it like this.

```text
token id 1042 -> [0.12, -0.08, 0.44, ...]
token id 3881 -> [0.09, -0.02, 0.39, ...]
```

In other words:

- A token ID is `a number that points to what it is`
- An embedding vector is `a numerical representation used for computation`

## Why Turn It into a Vector?

The Transformer we saw in Part 5 computes relationships among tokens. But relationship computation happens not on text strings themselves, but on numerical vectors.

Embeddings are needed for the following reasons.

- Numerical operations must be possible
- Similar uses among tokens must be placeable in somewhat similar positions
- They must connect to later computations such as attention, similarity search, and classification heads

You can understand it as follows.

`An embedding is the step that turns a token into something like coordinates that model computation can use.`

## What Does `Similar Meanings Become Close` Mean?

This phrase is heard often, but it is easy to misunderstand.

A safer explanation is as follows.

`Expressions that are often used in similar contexts or play similar roles can become closer vectors in a learned embedding space.`

For example:

- `car` and `automobile`
- `document summarization` and `summary generation`

Expressions like these can become close if they were used in similar contexts, even if they are not completely identical.

But this is not an absolute rule. Embeddings differ depending on training data, model structure, and objective function. So it is dangerous to read `close = perfectly understands the meaning`.

## Why Do Embeddings Seem Important in Both LLMs and Search?

Embeddings play important roles in both internal LLM computation and search services.

### Inside an LLM

- Tokens are changed into vectors
- Those vectors are used in attention and feed-forward computation

### Search and RAG

- Questions and documents are changed into vectors
- Nearby documents are found and provided back to the LLM

In other words, an embedding is both `an internal representation of a generative model` and `a comparison representation for a search system`.

## Drawn Very Simply

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s01-embedding-flow-en.mmd"
```

The result to check in this diagram is that an embedding is not a function that directly produces the final answer. It is the starting point that moves input into vector space so later computations such as similarity search and representation comparison become possible.

## Cases and Examples

The diagram below groups the three cases in this section again under the shared question `which comparable coordinates does the expression become`, rather than `do we read the string as-is`.

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s01-embedding-use-cases-en.mmd"
```

What you should check in this diagram is that even if tasks differ, the first needed step is the same. Instead of directly computing on the string itself, all cases first move tokens or sentences into `comparable vector coordinates`, then the next computation begins.

### Case 1. Internal Representation in a Language Model

Imagine a user reading a document that contains `foundation model` and `model card`. People may feel that the meaning is already fixed as soon as they see the same spelling, `model`. But in the actual context, one points to the whole model family, and the other points to a model description document, so the role changes depending on the neighboring word.

Conversely, there can be expressions such as `system` or `architecture` that have different spellings but appear together in similar explanatory contexts. If we hold only onto strings, it is difficult to handle these relationships through numerical computation.
The model changes tokens into embedding vectors and only then proceeds to the next stage after creating comparison standards needed for how often they appear together in the same context, their distance from other tokens, and attention computation.

The standard changes here from `reading a word` to `placing a word in computable coordinates`. The model does not read words like fixed dictionary definitions. Instead, it places them in computable coordinates based on what they are used with in which context. So even the same spelling such as `model` can be placed in a different relationship when surrounding clues differ, and conversely, different spellings can gather into closer coordinates if they often appear together in the same explanatory flow.

Even for the same word or different words, the comparison standard differs depending on context.

| Expression scene | What first appears to human eyes | What the embedding view sees again |
| --- | --- | --- |
| `model` in `foundation model` | The same spelling, `model` | Contextual relationship pointing to the whole model family |
| `model` in `model card` | Again the same spelling, `model` | A different role relationship: a model description document |
| Different spellings such as `system`, `architecture` | Surface-level different words | Relationships that appear together in similar explanatory contexts |

The misunderstanding this table corrects is the expectation that `if spellings are the same, the meaning is also almost the same computationally`. Embeddings make relationships in context a more direct comparison standard than surface spelling.

The judgment to close in this case is clear. Token IDs can point to the same string, but later computation continues on vector relationships made together with the surrounding context.

### Case 2. Sentence Search

A user may ask `what are the limits of prompts`, while a document says `can prompts alone guarantee factuality`. People usually feel that the same topic requires the same words to repeat. So if only string matching is used, a document with many words absent from the question can easily be pushed backward.

But both sentences handle the same problem scene: `are prompts alone enough`. The standard changes here from whether the words look identical to comparing whether they point to the same explanatory flow and problem scene. Embedding-based search places the question and document in the same vector space, so even when surface words differ, it can find sentences in a similar direction nearby. Embedding-based search is needed not to memorize more words, but to compare more directly whether the question and document point to the same problem scene.

Even in the same search scene, candidates differ depending on the standard.

| Relationship between question and document | What a string standard can easily miss first | What an embedding standard tries to catch first |
| --- | --- | --- |
| Question: `what are the limits of prompts` | Related documents that do not contain the word `limits` | The same problem scene: `are prompts alone enough` |
| Document: `can prompts alone guarantee factuality` | Can be pushed backward because surface words are not completely the same | The same explanatory flow and limitation discussion |
| Question and document differ only in expression | Keyword overlap looks small | Vector relationships in the same direction |

The important standard in this case is separating `are the same words present` from `are they talking about the same problem`. Embeddings matter in sentence search because these two often diverge in practice.

The judgment to close in this case is the meaning of search results. A nearby vector candidate is not a confirmed answer. It is a first candidate likely to handle the same problem scene. How to verify this candidate and attach it as evidence will be revisited in the later sections on vector search and RAG.

### Case 3. Recommendation and Similarity Comparison

Suppose a video service wants to recommend similar lectures. People easily judge lectures with many of the same words in their titles as similar. But even if both titles include `intro`, one may focus on math while the other focuses on practice. Conversely, even if titles differ, viewers may actually continue watching the same type of lecture.

If only title strings are compared, it is easy to miss these differences and make recommendations drift. The standard changes here from counting title characters to placing actual consumption flow and lecture characteristics together in the same comparison coordinate system. If information such as lecture descriptions, viewing patterns, and thumbnail features is placed together in an embedding space, different signals can be handled in one comparison coordinate system.

As a result, the recommender can put `lectures actually consumed together` ahead of `lectures with similar letters`. The result to check in this case is whether lectures with similar actual learning flows gather higher in recommendations than lectures with matching title words.

If we group the three cases again from the expression-coordinate view, it becomes the following.

| Situation | What surface strings can easily miss | What we want to see more in embedding coordinates |
| --- | --- | --- |
| Internal representation in a language model | Same spelling can have different roles by context | Relationships used together in the same context |
| Sentence search | Related documents are missed if question words are not present as-is | Proximity between sentences handling the same problem scene |
| Recommendation and similarity comparison | Even with the same title words, actual consumption flow can differ | Similarity in actual usage patterns and characteristics |

The judgment to close in this case is the same. An embedding is not the final answer for recommendation. It is a representation foundation that narrows candidates, and candidates are filtered again later through filters and policy judgment.

## Separating Numbers, Coordinates, and Comparison Results

After reading this section, even if you do not yet know complex vector formulas, you can follow an example that first separates `whether what I am seeing now is a number, coordinates, or a comparison result` as below.

| Value you are seeing now | Misunderstanding easy to recall first | Question to ask first from the embedding view |
| --- | --- | --- |
| One token ID | It is easy to feel that this number itself contains meaning | Is this value only a number in the vocabulary, or comparable coordinates? |
| One embedding vector row | Because there are many numbers, it is easy to pass it over as just a complex internal value | How is this vector used to compare distance or direction with other expressions? |
| A result saying two sentences are close | It is easy to end by thinking it must be because many words are the same | Was similar context and role read as close, beyond surface words? |

What matters in this table is not guessing the correct numeric answer in advance. What is needed first is separating `am I seeing a number`, `am I seeing expression coordinates`, and `am I seeing a candidate comparison result`.

The levels that are often mixed up are exactly these three.

- When seeing a token ID, it is easy to feel that meaning comparison has already begun.
- When seeing an embedding vector, it is easy to treat it as too internal and pass it by.
- When seeing a `close` result, it is easy to accept it immediately as the answer.

To read explanations of meaning and distance, RAG, and vector search, you must first be able to separate these three levels.

## Practice and Examples

The goal of this practice is to distinguish that `a token ID is only a number, and actual comparison happens on embedding vectors`. First, use Python to confirm a scene where ID order and vector-distance order differ, then read the same values again by hand.

### Example. Comparing ID Order and Vector-Distance Order

This example is not code that trains actual LLM embeddings. Instead, it makes a small representation table with `numpy` arrays and shows how numeric order of item IDs differs from order by closeness to a query vector. The values to manipulate directly are `query_vector` and `embeddings`. If you change the values, distance order and the nearest expression item change.

```python
# Example confirming that token ID numeric order and embedding vector distance order are different.
import numpy as np

token_ids = {
    "prompt_limit_phrase": 1042,
    "factuality_risk_phrase": 3881,
    "vector_search_phrase": 2210,
}

# Manipulation variables: changing expression vectors or query_vector changes the order of nearby items.
embeddings = {
    "prompt_limit_phrase": np.array([0.12, -0.08, 0.44]),
    "factuality_risk_phrase": np.array([0.09, -0.02, 0.39]),
    "vector_search_phrase": np.array([-0.30, 0.11, 0.15]),
}
query_vector = np.array([0.10, -0.01, 0.41])

def squared_distance(a, b):
    return float(np.sum((a - b) ** 2))

id_order = sorted(token_ids.items(), key=lambda item: item[1])
distance_order = sorted(
    (
        (name, token_ids[name], squared_distance(query_vector, vector))
        for name, vector in embeddings.items()
    ),
    key=lambda item: item[2],
)

print("ID order:")
for name, token_id in id_order:
    print(name, token_id)

print("\nVector distance order:")
for name, token_id, distance in distance_order:
    print(name, "token_id=", token_id, "distance=", round(distance, 3))
```

An example output is as follows.

```text
ID order:
prompt_limit_phrase 1042
vector_search_phrase 2210
factuality_risk_phrase 3881

Vector distance order:
factuality_risk_phrase token_id= 3881 distance= 0.001
prompt_limit_phrase token_id= 1042 distance= 0.006
vector_search_phrase token_id= 2210 distance= 0.242
```

The value to see in this output is that `ID order` and `Vector distance order` are different. The item with the smallest ID is `prompt_limit_phrase`, but the item closest to the query vector is `factuality_risk_phrase`. Therefore, token IDs are identification numbers, and embedding vectors are coordinate representations used later for distance comparison.

The values to observe are the following three groups.

| Item | Token ID | Explanatory embedding vector | Distance from query vector |
| --- | ---: | --- | ---: |
| `prompt_limit_phrase` | `1042` | `[0.12, -0.08, 0.44]` | `0.006` |
| `factuality_risk_phrase` | `3881` | `[0.09, -0.02, 0.39]` | `0.001` |
| `vector_search_phrase` | `2210` | `[-0.30, 0.11, 0.15]` | `0.242` |

Assume the query vector is `[0.10, -0.01, 0.41]`. The distance values are explanatory values calculated in advance to show how close each expression vector is to the query vector. What matters now is not memorizing the distance formula, but understanding that `the size of an ID number` and `closeness in vector space` are different judgments.

If the expression items are sorted by distance, they become the following.

| Rank | Item | Distance | Meaning to read |
| ---: | --- | ---: | --- |
| 1 | `factuality_risk_phrase` | `0.001` | The expression item closest to the query vector |
| 2 | `prompt_limit_phrase` | `0.006` | A close item, but not rank 1 |
| 3 | `vector_search_phrase` | `0.242` | A relatively distant item in this example |

The concept to check immediately in this table is one thing. Comparison using embeddings does not compare token ID matches or ID size. It chooses nearby items based on distance and direction in vector space.

## Distance Differences Seen in Representation Space

The previous example is not a procedure for training embeddings. It is the shortest scene showing that `assigning a number` and `turning something into a comparable numerical representation` are different. Finally, fix the levels by answering the three questions below. For each question, answer by yourself first, then compare with the explanation below.

| Scene | Question to answer first |
| --- | --- |
| A token ID is visible | Is this value a number pointing to an item, or coordinates for meaning comparison? |
| An embedding vector is visible | With what distance and direction can this expression be compared to other items? |
| A nearby item order is visible | Is this order a confirmed answer, or first-stage candidate selection? |

Explanation: A token ID is a number pointing to an item. The fact that the number `1042` is smaller or larger than `3881` alone cannot tell us that the meanings of the two expression items are closer. An embedding vector is a comparable coordinate representation, so distance from the query vector can be calculated. The order of nearby items is not a confirmed answer. It is the result of first-stage candidate selection to pass to later search, evidence checking, and generation.

In other words, the close of this section is not memorizing that `an embedding is a vector`, but becoming able to read `number`, `coordinate`, and `candidate comparison` as different levels. The core to read here is that the numeric difference between `1042` and `3881` itself means nothing, but in vector space a comparison becomes possible: the query is closer to `factuality_risk_phrase` than to `vector_search_phrase`. If an ID is for identification, an embedding is the starting point of a representation space that enables later similarity comparison and context computation.

### Exercise 1. Separate ID Size from Semantic Distance

Observations:

| Item | Value |
| --- | --- |
| ID of `prompt_limit_phrase` | `1042` |
| ID of `factuality_risk_phrase` | `3881` |
| Distance of `prompt_limit_phrase` | `0.006` |
| Distance of `factuality_risk_phrase` | `0.001` |

Answer by yourself first.

- Does the fact that `3881` is larger than `1042` mean `factuality_risk_phrase` is more important or farther away?
- Can you tell which expression item is closer to the query by looking only at ID numbers?

Explanation: No. `1042` and `3881` are only item numbers in a vocabulary or storage system, so semantic relationships cannot be judged from the difference in size between the two numbers. The calculation `3881 - 1042 = 2839` is possible, but that value does not tell how similar the two expression items are to the query. What this exercise must first separate is that `it looks like a number that can be calculated with` and `it is a coordinate that can be used for semantic comparison` are not the same.

### Exercise 2. Directly Compare Vector Distances

Observations:

| Item | Distance from query vector |
| --- | --- |
| `prompt_limit_phrase` | `0.006` |
| `factuality_risk_phrase` | `0.001` |
| `vector_search_phrase` | `0.242` |

Answer by yourself first.

- Which item is closest?
- Which item is farthest?
- This judgment used which value as the standard, not the ID?

Explanation: The closest item is `factuality_risk_phrase`, which has the smallest distance value. The farthest item is `vector_search_phrase`, which has the largest distance value. The comparison standard here is not the ID, but the distance between the query vector and each expression vector. Therefore, even though the ID `1042` of `prompt_limit_phrase` is the smallest, in this example's vector space `factuality_risk_phrase` is closer to the query. This is why embeddings should be read as `comparable coordinate representations`.

### Exercise 3. Do Not Mistake a Nearby Item for the Answer

Observations:

| Rank | Item | Distance |
| --- | --- | --- |
| 1 | `factuality_risk_phrase` | `0.001` |
| 2 | `prompt_limit_phrase` | `0.006` |
| 3 | `vector_search_phrase` | `0.242` |

Answer by yourself first.

- Is the rank-1 item immediately the answer?
- Can a nearby item be used directly in the answer?
- What should this result be used for in the next step?

Explanation: The rank-1 item is not a confirmed answer. Even if `factuality_risk_phrase` is closest to the query vector, you must separately check whether there is enough evidence to answer the actual question and whether it matches the scope the user asked about. Therefore, this result should be used not as `the answer right away`, but as `a candidate list to review first`. The embedding view is not an answer judge. It is a representation foundation that makes candidate comparison possible where numbers alone could not.

## Background Only

Embeddings are not a concept that appeared only in the LLM era. In natural language processing, research has long continued on turning words into distributed representations, and studies such as word2vec spread the sense that `words in similar contexts can become similar vectors`.

In the LLM era, this concept has widened.

- Not only words, but also tokens, sentences, and documents became embedding targets
- The internal representations of generative models and the representations of search services became more directly connected

## Checklist
- Can you explain embeddings again as `coordinate representations that computation can use`?
- Can you distinguish the roles of token IDs and embedding vectors?
- Can you explain that after making vectors, the next question is `what standard should be used to call something close`?

## Sources and References

- Yoshua Bengio et al., [A Neural Probabilistic Language Model](https://jmlr.csail.mit.edu/papers/v3/bengio03a.html){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, accessed 2026-07-19. Used as background evidence for learning distributed representations of words and using them for language-model generalization.
- Tomas Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-07-19. Used as background evidence for dense word vectors in the word2vec family and context-based representation learning.
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, 3rd ed. draft](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, online manuscript released January 6, 2026, accessed 2026-07-19. Used as general NLP background evidence for embeddings, vector representations, and language-model input explanations.
