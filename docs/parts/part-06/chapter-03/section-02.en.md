# P6-3.2 Nearby Vectors That Make Candidates, Not Answers

> Section ID: `P6-3.2`
> Version: `v2026.07.26`

In P6-3.1, we explained an embedding as a representation method that turns tokens or sentences into vectors. Once vectors have been made, the next problem is how to read them.

If embedding vectors have been made, what does it actually mean to say that two expressions are close? The expressions meaning and distance refer to a computational view that compares expressions with similar uses as nearby candidates in an embedding space.

The first distinction to make here is between `nearby candidate` and `correct evidence`. Distance and similarity are comparison standards that first narrow candidates; they do not guarantee that the candidate is immediately the answer or current evidence.

## Standards for Comparing Vector Candidates

When first reading meaning and distance, hold onto the questions below.

- What does `close` mean in vector space?
- How can distance and similarity be read differently?
- Why does a nearby vector not immediately mean the answer or truth?
- How does this view connect to search, recommendation, and RAG?

First hold meaning and distance as the question `by what comparison standard should embedding vectors be read as nearby candidates`. Embedding training flow, fast candidate search, and actual use inside search systems will broaden in later sections, but the standard needed now is the basic comparison sense used in search and recommendation.

Rather than memorizing formulas, read `distance in embedding space` as the language of actual comparison and search.

If the embedding explanation in P6-3.1 handled `do we turn an expression into a vector`, this section handles by what standard the vectors made that way should be read as close or far from each other. This comparison standard later grows into questions about Transformer internal computation, RAG, and search candidate selection in vector databases.

So the core is not stopping at `a vector has been made`, but reading by what standard that vector should be compared.

| Focus at this stage | Question that follows | Where to read it broadly again |
| --- | --- | --- |
| Embedding | What vector representation should text or sentences be changed into? | P6-3.1 |
| Meaning and distance | By what standard should those vectors be compared as nearby candidates? | P6-3.2 |
| Search and RAG | How are nearby candidates used for actual document search and generation coupling? | P6-12.1, P6-12.2, P6-13.1, P6-13.2 |
| Recommendation and later selection | By what contextual standards are nearby candidates filtered again for final selection? | Cases in P6-3.2 and service contexts in general |

In other words, the core of the current chapter is moving from `making vectors` to `reading those vectors as a candidate-comparison standard`. This standard must be fixed so that later, when reading RAG and vector search, you do not mix nearby document candidates with final answer evidence.

## Separating Nearby Candidates from Correct Evidence

This distinction extends the embedding of P6-3.1 from `making vectors` to `comparing vectors`, and becomes a core foundation for understanding search and external-knowledge connection. After reading this section, you should be able to explain distance and similarity as candidate-comparison standards, and say both that a nearby vector `may be a similar candidate` and that it is `not immediately the answer`.

## What Does `Close` Mean?

An embedding vector is a representation made of several numbers. Distance or similarity can be mathematically defined between these vectors.

You can understand it as follows.

- A short distance -> vectors are close to each other
- High similarity -> vectors have more similar directions or positions

What matters here is that this comparison is not `string comparison`, but `learned representation comparison`.

That is:

- Similar expressions can become close even without the same words
- Expressions with the same words can become far if the context differs

## How Are Distance and Similarity Different?

At the introductory stage, you do not need to distinguish the two too strictly. But the reading direction can differ.

| Expression | Reader intuition |
| --- | --- |
| Distance | How far apart they are |
| Similarity | How similar they are |

Both are the same in that they are `comparison standards`.

In practice, the comparison function used can differ depending on the search system or embedding model. But what readers should first take is not the formula name, but the view of asking `by what standard are questions and documents, products, or sentences read as close to each other`.

## Why Are Nearby Vectors Useful?

Finding nearby vectors makes the following possible.

- Finding similar questions
- Finding related document candidates
- Finding similar products or content
- Finding duplicate or nearly identical expressions

In other words, the concept of distance in embedding space naturally connects to topics later in Part 6 such as RAG, vector databases, and recommendation.

## Why a Nearby Vector Is Not Immediately the Answer

This point must be fixed first so that you do not mix the judgment `close` with the judgment `correct` or `current`.

A `nearby vector` usually means `a candidate with high relatedness`, not an answer or truth.

Consider cases like these.

- A document whose expression is similar but whose facts are wrong
- A document that is superficially similar to the question but needs a different context
- A document that is old and no longer current
- A document that a general embedding cannot distinguish well enough in a specialized field

Therefore, in similarity search or RAG, you must separate `the step that finds nearby candidates` from `the step that checks whether those candidates are actually correct evidence`.

## Drawn Very Simply

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s02-similarity-flow-en.mmd"
```

The result to check in this diagram is that `finding something close` and `organizing it as the final answer` are different steps. Even if search is correct, answer organization goes through a separate judgment.

When reading the diagram, first separate `first-stage candidate` from `final confirmation`.

| What to separate first | Why it is needed |
| --- | --- |
| The step that chooses nearby candidates | To first fix what distance and similarity do |
| The step that opens and checks candidates | To hold onto the fact that closeness is not immediately an answer |
| The step that checks freshness and exception conditions again | Because it naturally connects to later explanations of RAG and search quality |

## Cases and Examples

The diagram below groups the three cases in this section again under the shared question `what should be raised first as a nearby candidate`, rather than `what is the same`.

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s02-similarity-use-cases-en.mmd"
```

What you should check in this diagram is that even if tasks differ, the common step is `first choose nearby candidates`. But that does not mean the candidate is immediately the answer, so later review and organization steps are separately needed.

### Case 1. Finding Similar Questions

Imagine a user asking in a help window, `Can prompts alone prevent false answers?` If you think a question is easy to find only when the words inside the question appear exactly in the document title, you first search for words such as `false answers` or `prevent`. But the actual knowledge base may only have documents organized in more technical expressions such as `limits of prompts and methods for strengthening factuality`. If you match only keywords at this point, you can miss a related document, and the user may misunderstand that `there must be no document`.

The standard changes here beyond word matching, toward comparing whether the two sentences actually point to the same problem scene. Similarity search sees `preventing false answers` and `strengthening factuality` as fairly close problems and raises that document as a candidate.

The misunderstanding to correct here is the feeling that `if the same words are absent, it is not the same question`. The result to check in this case is whether a document handling the same problem appears as an actual candidate even when the question words are not present as-is, and whether you can explain from the candidate alone why that document was grouped as the same scene.

The judgment to close in this case is simple. Distance comparison first finds the same problem scene, but checking the candidate body and evidence remains a separate step.

### Case 2. Document Search

Imagine asking `When is the travel-expense settlement deadline?` among hundreds of internal policy documents. If title is used as the first standard, it feels as if the answer will appear immediately only when `travel expense`, `settlement`, and `deadline` all appear in the title. But in the actual document structure, the title may be `Travel Operations Guide`, and only a table in the middle of the body may contain `submit within five business days each month` and `overseas travel exceptions`. Even if you open one document with a matching title, the answer can still be slow or wrong if you miss the key paragraph.

The standard changes here from ending at choosing one document title to lowering the search unit and first gathering a few paragraphs closest to the question. Similarity search gathers a few paragraphs close to the question as candidates, and then the LLM reads those paragraphs and organizes a natural-language answer.

The misunderstanding to correct here is the expectation that `if the title matches, the document is already the answer`. The result to check in this case is not one document with a matching title, but whether the key paragraph containing the actual deadline is included among the candidates, and whether the paragraph with exception clauses also appears.

The judgment to close in this case is separating title match from answer evidence confirmation. First gather nearby paragraph candidates, then open them again and check whether they contain the actual deadline and exception clauses.

### Case 3. Recommendation System

Imagine a user who finished an introductory linear algebra lecture and now needs a next lecture recommendation. It is easy to first group lectures as similar if they share the tag `introductory`. But in reality, one may focus on blackboard formulas while the other focuses on NumPy practice, so the learning rhythm can be quite different. For example, if a user who watched formula-explanation videos to the end moves directly to a code-practice-centered lecture, drop-off can increase. In other words, the same tag does not guarantee a similar consumption experience.

The standard changes here from matching one tag to also seeing what lectures were consumed in what flow. If nearby items are found in a vector space that reflects both viewing behavior and lecture features, candidates with similar actual learning flows can be chosen more naturally than with simple tags.

The misunderstanding to correct here is the feeling that `if the label is the same, the experience is also the same`. The result to check in this case is whether candidates with similar actual learning rhythm gather toward the front more than candidates with the same tag, and whether that candidate choice also reduces the chance of leaving the next learning step.

The judgment to close in this case is the same. Nearby recommendation candidates are not final choices but inputs to later filters, so conditions such as difficulty, goal, and freshness must be checked again.

If we group the three cases again from the candidate-selection view, it becomes the following.

| Situation | What first appears to human eyes | Candidate similarity search tries to raise first |
| --- | --- | --- |
| Finding similar questions | Questions with the same words | Questions handling the same problem |
| Document search | Documents with similar titles | Paragraphs containing the key answer |
| Recommendation system | Items with the same tag | Items with similar actual consumption flow |

## Separating Candidate Selection from Answer Confirmation

After reading this section, even if you do not yet know distance functions in detail, you can follow an example that first separates `choosing nearby candidates` from `confirming the final answer`.

| Result you see now | Misunderstanding easy to recall first | Question to ask first from the meaning-and-distance view |
| --- | --- | --- |
| A document is rank 1 by distance | It is easy to feel that the document is immediately the final answer | Is this value a first-stage candidate order, or final answer confirmation? |
| Two candidates are both close | It is easy to feel that you only need rank 1 and can discard the rest | Did you reopen top-k candidates by actual body and freshness standards? |
| A document similar to the question appears | It is easy to feel that if it is similar, the facts must also be right | Did you separately check freshness, exceptions, and factual match in addition to relatedness? |

What matters in this table is not memorizing distance scores. What is needed first is reading `candidate selection` and `answer confirmation` as different steps.

The steps often mixed up here are exactly these two.

- Once a nearby candidate is found, it is easy to feel that the answer is finished.
- When the top-1 document appears, it is easy to feel that the other candidates are meaningless.
- When relatedness is high, it is easy to feel that factuality automatically follows.

But to read the later sections on RAG, search quality, and operational constraints, you must be able to separate `what was raised first as a candidate` from `what was confirmed as final evidence`.

## Practice and Examples

The goal of this practice is to separate the sense that `nearby candidates are chosen first` from the point that `closeness is not immediately the answer`. First set the judgment position with a small numerical example, then check the same structure with two search signals.

Assume the question is `When is the travel-expense settlement deadline?`, and the search system raised the following three candidates.

| Rank | Candidate | Distance | Updated | Memo |
| ---: | --- | ---: | --- | --- |
| 1 | `doc_A` | `0.02` | `2026-03` | Last quarter policy |
| 2 | `doc_C` | `0.05` | `2026-06` | Includes latest exception clause |
| 3 | `doc_B` | `1.0` | `2025-12` | Different topic |

In this table, the distance value is `a signal that first orders candidates close to the question`, while the update date and memo are `signals that must be checked again to see whether the item can be used as final evidence`.

Here, the fact that `doc_A` is rank 1 by distance means it is `a candidate to open first`. But `doc_A` is last quarter's policy, while `doc_C` contains the latest exception clause even though it is rank 2 by distance. Therefore, distance rank is the output of the candidate-selection step, and final evidence confirmation is possible only after checking the body and metadata again.

## What Diverges in Search Candidate Judgment

The code in this section builds document candidates in two ways. First, it uses `TfidfVectorizer` to make a reproducible baseline close to character overlap. Then it uses an Ollama embedding model to check actual embedding-based candidate order. The rankings of the two outputs can differ. But the center to read is the same: separate `nearby candidate`, `candidate group to review`, and `final evidence` as different steps.

### Basic Example. Separating Top-k Candidates from Final Evidence Candidates

This example uses `TfidfVectorizer` like a small search model instead of an actual embedding model. The core is not the type of search model, but confirming in output that nearby candidate order and final evidence candidates can differ. The values to manipulate directly are `query`, `top_k`, and `min_similarity`.

```python
# Example separating nearby top-k candidates from final evidence candidates.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    {
        "doc_id": "doc_A",
        "title": "Travel expense settlement policy",
        "text": "The travel expense settlement deadline and submission deadline are within five business days each month. This is based on last quarter.",
        "current_version": False,
        "contains_exception": False,
    },
    {
        "doc_id": "doc_C",
        "title": "Latest travel expense settlement exceptions",
        "text": "For overseas travel exception conditions and urgent approval exception conditions, check the latest notice link.",
        "current_version": True,
        "contains_exception": True,
    },
    {
        "doc_id": "doc_B",
        "title": "Meeting room reservation",
        "text": "Meeting room reservations are requested in the internal calendar, and equipment rental status is recorded together.",
        "current_version": True,
        "contains_exception": False,
    },
]

# Manipulation variables: changing query, top_k, and min_similarity changes the candidate group to review.
query = "What are the travel expense settlement deadline and exception conditions?"
top_k = 3
min_similarity = 0.10

vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
document_vectors = vectorizer.fit_transform([doc["text"] for doc in documents])
query_vector = vectorizer.transform([query])
similarities = cosine_similarity(query_vector, document_vectors)[0]

ranked = sorted(
    zip(documents, similarities),
    key=lambda item: item[1],
    reverse=True,
)[:top_k]

print("retrieved candidates:")
for rank, (doc, score) in enumerate(ranked, start=1):
    print(
        rank,
        doc["doc_id"],
        "similarity=", round(float(score), 3),
        "current=", doc["current_version"],
        "exception=", doc["contains_exception"],
    )

grounding_candidates = [
    doc["doc_id"]
    for doc, score in ranked
    if score >= min_similarity and doc["current_version"] and doc["contains_exception"]
]

print("grounding_candidates =", grounding_candidates)
```

An example execution result can be read as follows.

```text
retrieved candidates:
1 doc_A similarity= 0.459 current= False exception= False
2 doc_C similarity= 0.408 current= True exception= True
3 doc_B similarity= 0.046 current= True exception= False
grounding_candidates = ['doc_C']
```

In this output, `doc_A` is rank 1 by similarity, but it is based on last quarter and has no exception condition. Conversely, `doc_C` is rank 2, but it is the latest document and contains exception conditions, so it becomes the final evidence candidate. In other words, finding nearby candidates first and confirming them as answer evidence are different steps.

### Optional Example. Comparing the Same Candidates with a Local Embedding Model

If Ollama is installed and the `nomic-embed-text` model has been downloaded, you can check the same structure with an actual embedding model. The purpose of this optional example is not comparing model performance. It is to confirm that even when candidates are built with vectors made by an embedding model rather than string-overlap-based vectorization, `nearby candidates` and `final evidence candidates` must be separated again.

First prepare the model in a local terminal.

```bash
ollama pull nomic-embed-text
```

Then run the code below. This code uses the Python package `ollama`. If the code prints `Ollama embedding model is not ready.`, the Ollama server is off or the `nomic-embed-text` model is not ready yet.

```python
# Optional example comparing top-k candidates and final evidence candidates again with Ollama's local embedding model.
from math import sqrt

import ollama

documents = [
    {
        "doc_id": "doc_A",
        "title": "Travel expense settlement policy",
        "text": "The travel expense settlement deadline and submission deadline are within five business days each month. This is based on last quarter.",
        "current_version": False,
        "contains_exception": False,
    },
    {
        "doc_id": "doc_C",
        "title": "Latest travel expense settlement exceptions",
        "text": "For overseas travel exception conditions and urgent approval exception conditions, check the latest notice link.",
        "current_version": True,
        "contains_exception": True,
    },
    {
        "doc_id": "doc_B",
        "title": "Meeting room reservation",
        "text": "Meeting room reservations are requested in the internal calendar, and equipment rental status is recorded together.",
        "current_version": True,
        "contains_exception": False,
    },
]

# Manipulation variables: changing query, top_k, and min_similarity can change search candidates and evidence candidates.
query = "What are the travel expense settlement deadline and exception conditions?"
top_k = 3
min_similarity = 0.25
model_name = "nomic-embed-text"

def embed(text: str) -> list[float]:
    return ollama.embed(model=model_name, input=text).embeddings[0]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

try:
    query_vector = embed(query)
    document_vectors = [embed(doc["text"]) for doc in documents]
except Exception as error:
    print("Ollama embedding model is not ready.")
    print(type(error).__name__, error)
    raise SystemExit

ranked = sorted(
    zip(documents, document_vectors),
    key=lambda item: cosine_similarity(query_vector, item[1]),
    reverse=True,
)[:top_k]

print("embedding candidates:")
for rank, (doc, vector) in enumerate(ranked, start=1):
    score = cosine_similarity(query_vector, vector)
    print(
        rank,
        doc["doc_id"],
        "similarity=", round(float(score), 3),
        "current=", doc["current_version"],
        "exception=", doc["contains_exception"],
    )

grounding_candidates = [
    doc["doc_id"]
    for doc, vector in ranked
    if (
        cosine_similarity(query_vector, vector) >= min_similarity
        and doc["current_version"]
        and doc["contains_exception"]
    )
]

print("grounding_candidates =", grounding_candidates)
```

An example execution result was as follows.

```text
embedding candidates:
1 doc_C similarity= 0.85 current= True exception= True
2 doc_A similarity= 0.833 current= False exception= False
3 doc_B similarity= 0.813 current= True exception= False
grounding_candidates = ['doc_C']
```

In this optional example, the actual embedding model raised `doc_C` as rank 1. But you should not read this alone as the embedding model having found the final answer. `doc_A` and `doc_B` were also raised with high similarities. In a small example with few short document candidates, broad business documents, request procedures, and policy sentences can be captured as close to each other. Even when using an actual embedding model, closeness is a `candidate-selection signal`, not a judgment value that automatically guarantees freshness and exception conditions.

### Exercise 1. Reading Ranking Differences Between Two Search Signals

When the two execution results are placed side by side, the rank-1 candidate differs even for the same question.

| Execution method | Rank-1 candidate | Signal to read together |
| --- | --- | --- |
| `TfidfVectorizer` baseline | `doc_A` | Deadline expressions overlap a lot, but `current_version=False` and there is no exception condition |
| Ollama embedding model | `doc_C` | The exception-condition document appears first, but other candidates also appear with high similarity |

Answer by yourself first.

- Why did `doc_A` appear first in `TfidfVectorizer`?
- Why can `doc_C` appear first in the Ollama embedding model?
- Even if the two outputs differ, what must be checked in common before confirming final evidence?

Explanation: `TfidfVectorizer` strongly sees overlap between character pieces. So `doc_A`, which has much overlap with expressions such as `travel expense`, `settlement`, and `deadline`, appears first. The Ollama embedding model sees the semantic relationship of the whole sentence more broadly, so it can raise `doc_C`, which contains `exception conditions`, first. But both methods still require checking the document body, freshness, and exception conditions before final evidence is confirmed.

### Exercise 2. Do Not Immediately Trust High Similarity

If you only look at the Ollama embedding output, all three candidates appear to have high similarity.

| Candidate | Similarity | Current version | Exception condition |
| --- | ---: | --- | --- |
| `doc_C` | `0.850` | Yes | Yes |
| `doc_A` | `0.833` | No | No |
| `doc_B` | `0.813` | Yes | No |

Answer by yourself first.

- Can `doc_B` be used as final evidence because its similarity came out high?
- Can last quarter's policy be put into the answer because `doc_A` had high similarity?
- Why is the final evidence candidate narrowed to `doc_C` in this output?

Explanation: `doc_B` is the current version but does not contain the core exception condition for travel expense settlement. `doc_A` is close to the question, but it is last quarter's policy. Therefore, even if all three candidates look close, the final evidence candidate must be narrowed to `doc_C`, where `current_version=True` and `contains_exception=True`. Similarity here is not a final judgment for discarding or trusting a candidate. It is an order for deciding what to open first.

### Exercise 3. Choose the Next Action

For each scene below, choose what should come first among `review document body`, `check freshness`, `additional search`, and `confirm evidence candidate`, then write the reason in one sentence.

| Scene | First action to choose |
| --- | --- |
| The top-1 document is closest to the question but contains only last year's policy | ? |
| The top-3 candidates are all similarly close, but only one contains the latest notice link | ? |
| The entire top-k candidate set is far from the question and barely overlaps with key words | ? |
| The top-1 candidate looks plausible but does not mention exception clauses at all | ? |

Explanation: In the first scene, freshness checking comes first. Even a nearby candidate cannot become final evidence if it contains only last year's policy. In the second scene, document-body review and freshness checking must be done together. If top-k candidates are all close, do not look only at distance order. Open the actual notice link and evidence paragraph. In the third scene, additional search comes first. If the entire candidate set is distant and key words barely overlap, the current search query or index may be wrong. In the fourth scene, document-body review comes first. Even if the top-1 candidate looks plausible, it is difficult to confirm the answer if there is no exception clause. The core in all four scenes is reading `nearby candidate selection` separately from `final evidence confirmation`.

This example shows that in an actual service, `finding nearby vectors` means not `confirming the answer immediately`, but `narrowing candidates to review first in order`. The TF-IDF baseline and the Ollama embedding model can create different rankings, but neither confirms final evidence on its own. So even when reading later sections on search, RAG, and recommendation, the core is less the distance calculation itself and more `what is raised as a candidate, and by which next step is it reviewed`.

The concepts of embedding and distance are deeply connected to the flow of representation learning after statistical language models. Instead of treating words only as separated symbols like one-hot vectors, the attempt to express relationships inside vector space expanded into search and generative services in general.

In the LLM era, this view has become more important.

- Inside the model, it leads to attention computation
- Outside the service, it leads to embedding search and RAG

## Checklist

- You should be able to explain distance and similarity as `candidate-comparison standards`.
- You should be able to think of the nearest vector and the final answer separately.
- You should be able to explain both `why similar questions and documents appear together` and `why the nearest candidate is not always the answer`.

## Sources and References

- Tomas Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-07-19. Used as background evidence for dense word vectors and similar-context representations.
- Tomas Mikolov et al., [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-07-19. Used as background evidence for treating words and phrases as comparable representations in vector space.
- Nils Reimers, Iryna Gurevych, [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084){: target="_blank" rel="noopener noreferrer" }, arXiv, 2019, accessed 2026-07-19. Used as evidence for comparing sentence embeddings with cosine similarity in semantic similarity search.
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, 3rd ed. draft](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, online manuscript released January 6, 2026, accessed 2026-07-19. Used as general NLP background evidence for embeddings and similarity comparison.
- Ollama, [nomic-embed-text](https://registry.ollama.com/library/nomic-embed-text){: target="_blank" rel="noopener noreferrer" }, Ollama model registry, accessed 2026-07-24. Used to confirm model description and call flow for the optional execution example using a local embedding model.
