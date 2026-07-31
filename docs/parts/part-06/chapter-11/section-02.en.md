# P6-11.2 RAG Flow That Separates Retrieval Failure from Generation Failure

> Section ID: `P6-11.2`
> Version: `v2026.07.31`

When looking at RAG failure, separate `retrieval_result`, `retrieval_gap`, `generation_input`, `generated_answer`, `failure_stage`, and `repair_action`. These fields let you fix a wrong retrieval candidate separately from a case where evidence existed but the answer was generated incorrectly.

In P6-11.1, we saw that retrieval-augmented generation (RAG) attaches external evidence before answering. Now we need to see where that evidence sits in the actual input flow and how to split answer failures into different causes.

In RAG, retrieval results are not decorations appended after an answer. They are material placed into the model input context before generation. That means even when two answers look equally wrong, we need to separate `what was retrieved` from `how the retrieved material was rewritten`.

## How retrieval and generation are combined

The first standards to settle in a retrieval-generation flow are these three.

| Question | Standard to keep here |
| --- | --- |
| How are retrieval results used before generation? | Retrieved documents are attached to the model input context. |
| Is adding more documents always better? | Relevance, order, and conflict management matter more than volume. |
| When the answer is wrong, where should we inspect first? | Inspect retrieval failure and generation failure separately. |

If the question in P6-11.1 was `why attach documents before answering`, the question here is `how the attached documents work between input context and final answer`. After that, P6-12 moves to the storage structures and indexes used to retrieve those documents again.

## Where retrieval results are attached

In the simplest form, parts of retrieved documents enter the prompt context.

For example, the input may be built from these pieces.

- User question
- Retrieved document excerpts
- Answer-format instruction

In other words, the model does not receive `the question only`. It receives `the question + related documents + response instructions`.

`RAG is a structure that keeps retrieval results outside the model, then attaches them to the input context immediately before answering.`

The first record to keep is which documents were considered relevant enough to attach, which evidence sentences were selected, and whether the final answer exaggerates or leaves those documents. Those retrieval records and answer-inspection notes are what let us separate retrieval failure from generation failure. Later, the same records will be reread in P6-12.1 and P6-12.2 as retrieval-quality checks, in P6-16 as evaluation material, in P6-17 as operational judgment, and in Part 6 as retrieval logs and reflection notes.

## Is adding more documents always better?

No. The important factor here is not `amount`, but `relevance` and `organization`.

If too many documents are attached:

- the main evidence can be buried
- conflicting sentences can be mixed together
- the context window can be wasted
- the model can become more confused

So retrieval results should not be judged by `collecting a lot`. It is more important to attach the right material for the question, in an appropriate size and order.

One step further, we can also see that there is already a document-preparation stage before `retrieval-generation combination`. Retrieval works well only when documents have been organized in advance into a form that can be found and attached when a question arrives.

So this Section discusses `where retrieved documents are attached`, but before that there is already a stage that `organizes documents so they can be attached`. This difference is what lets vector databases and indexes be read not as simple storage, but as an extension of `retrievable document preparation`.

Split again by request timing, the safer reading is this.

| Stage | First question to ask | Common failure |
| --- | --- | --- |
| Document preparation stage | Were documents organized so they were searchable before this question arrived? | Old versions mixed in, duplicate documents, overly long chunks |
| Retrieval stage | Did the system actually retrieve documents that fit the current question? | Irrelevant documents ranked high, current documents missing |
| Generation stage | Did the answer rewrite the retrieved documents without leaving them? | Missing conditions, overclaiming, general memory mixed in |

In short, `retrieval-generation combination` should include not only the two steps after a request arrives, but also the earlier document-preparation stage.

## How retrieval failure differs from generation failure

This distinction is critical.

### Retrieval failure

- The relevant document was not found.
- An old document appeared first.
- A document unrelated to the question was mixed in.

### Generation failure

- The document was retrieved, but summarized incorrectly.
- The answer relied on general memory more than document evidence.
- The source was connected incorrectly.

So when a RAG system gives a strange answer, we cannot always say only that `the model is bad`. First, we need to separate whether retrieval was wrong or generation was wrong.

Even when the wrong answer looks similar on the surface, the first signal changes which record to inspect and what action to take next.

| First visible signal | First failure axis to suspect | Record to revisit first | Immediate check | Conclusion not to rush |
| --- | --- | --- | --- | --- |
| The attached document title or excerpt is off-topic. | Retrieval failure | Recheck which documents were attached, what the relevance scores were, and which evidence sentences were selected. | Revisit why a document ranked high, and first remove documents unrelated to the question. | Do not assume that changing only the prompt wording will solve it. |
| The attached document is right, but the answer drops conditions or exaggerates. | Generation failure | Recheck whether the draft answer left the actual evidence sentence and where the grounding check became unstable. | Check whether the draft answer leaves the evidence, then revisit the summarization instruction and grounding rule. | Do not assume retrieval quality is already sufficient. |
| Retrieval looks awkward and the answer is unstable too. | Retrieval failure spreading into generation | Inspect the retrieval record and answer draft together. | First reduce retrieval contamination, then adjust generation instructions. | Do not expand one wrong answer into a general model-capability problem. |

## Why answer quality can become unstable

RAG combines two stages, so it also gains more possible failure points.

- Retrieved document selection
- Document length and excerpting
- Document order
- Generation instruction design
- Citation format

For this reason, it is more accurate to read RAG as a `retrieval pipeline + generation pipeline`, not as one retrieval step plus one generation step in a vague sense.

## A minimal diagram

```mermaid
--8<-- "assets/part-06/chapter-11/p6-c11-s02-rag-combine-flow-en.mmd"
```

The point of this diagram is that retrieval results are not attached after the answer. They enter the input context `before the answer`.

## Cases and examples

### Case 1. Product support chatbot

Imagine a product support chatbot where a customer asks, `Where do I go to turn off autosave?` In this scene, it is easy to feel that retrieval or generation does not matter as long as `one good answer comes out`. But the retrieval stage first needs to fetch the relevant paragraph in the current manual that contains `autosave`, `settings`, and `preferences`. Then the generation stage should not simply copy the paragraph, but rewrite it into the steps the customer needs to follow: which menu to click and in what order. For example, the document may only list a path such as `Preferences > Editing > Autosave`, while generation turns that path into a sentence a user can follow.

If retrieval brings a paragraph from another product version, generation can be fluent and still guide the user to the wrong feature. The standard changes from `write the answer directly` to `first find the right paragraph, then rewrite it into the shape of the question`. The misunderstanding to correct here is the expectation that `if the sentence is natural, the previous stage must also be right`. The result to check in this case is whether the current manual path is correctly reflected in the answer sentence and whether the retrieved path and final procedure point to the same version.

### Case 2. Legal-document assistant

Suppose a legal-document assistant is asked, `Does this clause allow immediate contract termination?` Once the relevant statute or clause is found, it may feel almost finished. But the retrieval stage is the work of finding related clauses and case summaries similar to the current question, while the generation stage reorganizes those documents into an answer such as `immediately possible`, `additional conditions required`, or `judgment withheld`. For example, if the document says `termination is possible after a demand to cure within a reasonable period`, but generation drops the intermediate condition and states `immediate termination is possible`, retrieval was right but the final answer becomes risky.

The standard changes from `the document was found, so the job is done` to `did the answer preserve the conditions in the found document`. In this case, we need to inspect `accuracy in finding the document` and `rewriting without leaving the document` separately. The misunderstanding to correct is the judgment that `if a related clause is attached, the final sentence is automatically safe`. The result to check is whether the final answer avoids overclaiming `immediately possible`, preserves the original condition, and does not add a stronger conclusion from outside the document.

### Case 3. Developer-documentation Q&A

Imagine a developer asking, `Where do I put the timeout option in this API?` People often feel that once retrieval brings the right version of the official documentation, the work is nearly done. But if generation mixes an old code example with the new document, or changes the option name into a similar parameter, the final answer can still fail. For example, if the document says `request_timeout` but generation changes it to `timeout_ms`, a familiar name from another library, the document was right but the answer breaks immediately. Retrieval being correct does not automatically make the answer correct.

The standard changes from treating `retrieval success` and `final answer correctness` as the same thing to separately asking whether the retrieved name is preserved in the answer. The misunderstanding to correct is the expectation that `if the official document is attached, generation will naturally adapt`. The result to check is whether the official option name retrieved from the document is preserved in the final answer, whether it is not changed into a similar parameter name, and whether the example code keeps the same interface as the retrieved document.

The three cases can be grouped again by stage separation.

| Situation | What retrieval must first get right | What generation must then preserve |
| --- | --- | --- |
| Product support chatbot | Retrieve the accurate current-version menu-path paragraph. | Rewrite the paragraph into user-facing procedure sentences accurately. |
| Legal-document assistant | Retrieve related clause and condition paragraphs. | Avoid dropping conditions or using categorical language. |
| Developer-documentation Q&A | Retrieve the current official option paragraph. | Do not change the option name into a similar name. |

The same content can be reread as a stage-splitting structure.

```mermaid
--8<-- "assets/part-06/chapter-11/p6-c11-s02-rag-failure-split-en.mmd"
```

The key point is that `even if RAG looks like one step, retrieval and generation can fail separately inside it`.

## Where retrieval failure and generation failure diverge

If we apply the earlier table again after the cases, the judgment questions compress into three. Instead of jumping from `the answer feels wrong` to a total model problem, place the retrieval record and generated answer side by side first.

| If you suspect this | First question to ask |
| --- | --- |
| `The attached evidence itself feels unfamiliar.` | Which document ranked high, and why? |
| `The evidence seems right, but the answer speaks too strongly.` | Did the answer assert more than the actual sentence says? |
| `I do not know where it started going wrong.` | Did I inspect the retrieval record and final answer separately? |

The standard to learn first is simple. Even when RAG looks like one step, we need to inspect the `retrieval stage` and the `generation stage` separately to find the cause.

## Exercise and example

The goal of this example is to build the habit of not collapsing retrieval and generation into one step. We separate `the stage that finds documents` from `the stage that attaches those documents and creates an answer`. Using the same document set, we change the retrieval question and `generation_style` to see whether retrieval contamination and generation overclaiming appear as failures in different stages.

Suppose the user asks, `Why do we need vector search?` The retrieval stage must choose related documents, and the generation stage must rewrite those documents into an explanation for the reader. Even if retrieval is right, an overclaiming generation style can still distort the final answer.

The example below uses two CSV files as input.

- Document list: [p6-11-rag-documents-en.csv](/AiBook/assets/part-06/chapter-11/p6-11-rag-documents-en.csv){ .csv-preview }
- Experiment conditions: [p6-11-rag-experiments-en.csv](/AiBook/assets/part-06/chapter-11/p6-11-rag-experiments-en.csv){ .csv-preview }

One row in the document list is one candidate document fragment for retrieval. The key columns are `title`, `text`, `category`, and `source_role`. If `category` is `retrieval`, the row is an evidence document related to the current question. If it is `irrelevant`, the row is an unrelated document that can be mixed in when retrieval conditions become unstable.

One row in the experiment file means one RAG request. `retrieval_terms` are search signals used to build the question, and `generation_style` is the generation mode used when converting retrieved documents into an answer. In the output, we inspect the retrieved document titles and similarities, the answer sentence, and separate checks for retrieval failure and generation failure. In particular, `source_trace` keeps the document ID, title, role, similarity, and text preview attached just before generation, so we can inspect which evidence documents entered the input context instead of reading only the final answer.

The first settings to change directly in this example are these.

| Experiment | Value to manipulate | Core point to read |
| --- | --- | --- |
| `clean_grounded` | Related retrieval terms and conservative generation | Normal flow |
| `noisy_retrieval` | Retrieval conditions mixed with unrelated terms | Retrieval failure spreading into generation |
| `clean_but_overclaim` | Retrieval is normal, but only generation condition is overclaiming | Generation failure |

The key point to check in the code is that RAG failure should be split into cases where retrieval is wrong and cases where generation speaks beyond the document. Retrieval uses the same `TfidfVectorizer` flow as P6-11.1, while generation failure is captured separately when retrieval is right but the answer sentence is stronger than the evidence. The code focuses on the practice of keeping retrieval records and answer-inspection records separately, then deciding which stage record to revisit first.

```python
# Example that records retrieval results and generated answers separately.
import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

question = "Why do we need vector search?"

document_path = Path("docs/assets/part-06/chapter-11/p6-11-rag-documents-en.csv")
experiment_path = Path("docs/assets/part-06/chapter-11/p6-11-rag-experiments-en.csv")

def read_csv(path):
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))

documents = read_csv(document_path)
experiments = read_csv(experiment_path)

# Vectorize document titles and bodies together to create a retrieval space.
document_texts = [
    f"{doc['title']} {doc['text']}"
    for doc in documents
]
vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
document_vectors = vectorizer.fit_transform(document_texts)

def build_query(experiment):
    terms = experiment["retrieval_terms"].split(";")
    return f"{question} {' '.join(terms)}"

def retrieve_documents(query, top_k=2):
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, document_vectors).ravel()
    ranked_indexes = scores.argsort()[::-1]

    retrieved = []
    for index in ranked_indexes:
        if scores[index] <= 0:
            continue
        retrieved.append(
            {
                **documents[index],
                "similarity": round(float(scores[index]), 3),
            }
        )
        if len(retrieved) == top_k:
            break
    return retrieved

def generate_answer(retrieved_docs, generation_style):
    first = retrieved_docs[0]["text"] if retrieved_docs else "There is no reference document."
    second = retrieved_docs[1]["text"] if len(retrieved_docs) > 1 else "Additional evidence is missing."

    if generation_style == "overclaim":
        return (
            f"{first} "
            "Therefore, it always guarantees current information and correct answers automatically."
        )

    return (
        f"{first} "
        f"Therefore, {second}"
    )

def inspect_result(retrieved_docs, answer):
    source_trace = [
        {
            "doc_id": doc["doc_id"],
            "title": doc["title"],
            "source_role": doc["source_role"],
            "similarity": doc["similarity"],
            "text_preview": doc["text"][:34],
        }
        for doc in retrieved_docs
    ]
    contains_irrelevant_doc = any(
        doc["category"] == "irrelevant" for doc in retrieved_docs
    )
    irrelevant_fragments = [
        doc["text"].split(".")[0]
        for doc in retrieved_docs
        if doc["category"] == "irrelevant"
    ]
    answer_mentions_irrelevant_content = any(
        fragment and fragment in answer
        for fragment in irrelevant_fragments
    )
    answer_overclaims = "always guarantees current information and correct answers automatically" in answer

    return {
        "source_trace": source_trace,
        "doc_titles": [doc["title"] for doc in retrieved_docs],
        "doc_similarities": [doc["similarity"] for doc in retrieved_docs],
        "top_doc_category": retrieved_docs[0]["category"] if retrieved_docs else "none",
        "contains_irrelevant_doc": contains_irrelevant_doc,
        "answer_mentions_irrelevant_content": answer_mentions_irrelevant_content,
        "answer_overclaims": answer_overclaims,
        "retrieval_failed": contains_irrelevant_doc,
        "generation_failed": (not contains_irrelevant_doc) and answer_overclaims,
    }

reports = []
for experiment in experiments:
    query = build_query(experiment)
    retrieved_docs = retrieve_documents(query)
    answer = generate_answer(retrieved_docs, experiment["generation_style"])
    inspect = inspect_result(retrieved_docs, answer)
    reports.append(
        {
            "experiment": {
                "name": experiment["name"],
                "query": query,
                "generation_style": experiment["generation_style"],
            },
            "answer": answer,
            "inspect": inspect,
        }
    )

summary = {
    "retrieval_failure_count": sum(report["inspect"]["retrieval_failed"] for report in reports),
    "generation_failure_count": sum(report["inspect"]["generation_failed"] for report in reports),
    "irrelevant_leak_count": sum(report["inspect"]["answer_mentions_irrelevant_content"] for report in reports),
    "overclaim_count": sum(report["inspect"]["answer_overclaims"] for report in reports),
    "retrieval_failure_ratio": round(
        sum(report["inspect"]["retrieval_failed"] for report in reports) / len(reports),
        2,
    ),
    "generation_failure_ratio": round(
        sum(report["inspect"]["generation_failed"] for report in reports) / len(reports),
        2,
    ),
}

print("[summary]")
print(summary)
print()

selected_names = {
    "clean_grounded_vector_search",
    "noisy_retrieval_marketing_copy",
    "clean_but_overclaim_vector_search",
}
selected_reports = [
    report for report in reports
    if report["experiment"]["name"] in selected_names
]

for report in selected_reports:
    print("=" * 80)
    print("[experiment]")
    print(report["experiment"])
    print("[generated answer]")
    print(report["answer"])
    print("[inspect]")
    print(report["inspect"])
```

Example output can be read like this.

```text
[summary]
{'retrieval_failure_count': 12, 'generation_failure_count': 12, 'irrelevant_leak_count': 12, 'overclaim_count': 12, 'retrieval_failure_ratio': 0.33, 'generation_failure_ratio': 0.33}

================================================================================
[experiment]
{'name': 'clean_grounded_vector_search', 'query': 'Why do we need vector search? semantic vector search', 'generation_style': 'grounded'}
[generated answer]
Vector search finds semantically similar text by placing it near the query in vector space. It can retrieve by meaning even when keywords differ. Therefore, Keyword search first checks whether the same words appear, while semantic search compares whether the question and document meanings are similar. This can retrieve related documents even when wording differs.
[inspect]
{'source_trace': [{'doc_id': 'R01', 'title': 'Vector Search Basics', 'source_role': 'primary_evidence', 'similarity': 0.586, 'text_preview': 'Vector search finds semantically s'}, {'doc_id': 'R02', 'title': 'Keyword Search and Semantic Search', 'source_role': 'primary_evidence', 'similarity': 0.459, 'text_preview': 'Keyword search first checks whethe'}], 'doc_titles': ['Vector Search Basics', 'Keyword Search and Semantic Search'], 'doc_similarities': [0.586, 0.459], 'top_doc_category': 'retrieval', 'contains_irrelevant_doc': False, 'answer_mentions_irrelevant_content': False, 'answer_overclaims': False, 'retrieval_failed': False, 'generation_failed': False}
================================================================================
[experiment]
{'name': 'noisy_retrieval_marketing_copy', 'query': 'Why do we need vector search? marketing copy promotion', 'generation_style': 'grounded'}
[generated answer]
This explains how to vary marketing campaign copy and promotional banner sentences. It is not evidence for vector search. Therefore, This explains how to combine unrelated marketing copy into more varied promotional text. It is not directly related to retrieval quality inspection.
[inspect]
{'source_trace': [{'doc_id': 'X02', 'title': 'Promotional Banner Sentence Candidates', 'source_role': 'off_topic_noise', 'similarity': 0.456, 'text_preview': 'This explains how to vary marketin'}, {'doc_id': 'X01', 'title': 'Marketing Copy A/B Test', 'source_role': 'off_topic_noise', 'similarity': 0.423, 'text_preview': 'This explains how to combine unrel'}], 'doc_titles': ['Promotional Banner Sentence Candidates', 'Marketing Copy A/B Test'], 'doc_similarities': [0.456, 0.423], 'top_doc_category': 'irrelevant', 'contains_irrelevant_doc': True, 'answer_mentions_irrelevant_content': True, 'answer_overclaims': False, 'retrieval_failed': True, 'generation_failed': False}
================================================================================
[experiment]
{'name': 'clean_but_overclaim_vector_search', 'query': 'Why do we need vector search? semantic vector search', 'generation_style': 'overclaim'}
[generated answer]
Vector search finds semantically similar text by placing it near the query in vector space. It can retrieve by meaning even when keywords differ. Therefore, it always guarantees current information and correct answers automatically.
[inspect]
{'source_trace': [{'doc_id': 'R01', 'title': 'Vector Search Basics', 'source_role': 'primary_evidence', 'similarity': 0.586, 'text_preview': 'Vector search finds semantically s'}, {'doc_id': 'R02', 'title': 'Keyword Search and Semantic Search', 'source_role': 'primary_evidence', 'similarity': 0.459, 'text_preview': 'Keyword search first checks whethe'}], 'doc_titles': ['Vector Search Basics', 'Keyword Search and Semantic Search'], 'doc_similarities': [0.586, 0.459], 'top_doc_category': 'retrieval', 'contains_irrelevant_doc': False, 'answer_mentions_irrelevant_content': False, 'answer_overclaims': True, 'retrieval_failed': False, 'generation_failed': True}
```

The first point to notice is that `retrieval_failure_count` and `generation_failure_count` are counted separately. `noisy_retrieval` is a case where noise in the retrieval conditions selects unrelated documents and contaminates generation. `clean_but_overclaim` is a case where retrieval is right but the generation condition overstates beyond the document. This distinction lets us decide separately whether to fix retrieval or to fix generation instructions and evaluation.

So this example should leave two results.

- Retrieval results do not dissolve immediately into the final answer; until just before generation, they remain as separate input-evidence records such as `source_trace`.
- Retrieval failure and generation failure can look like the same wrong answer, but their causes differ, so their inspection items must also be separate.

The reader can directly adjust the example in these ways.

- Reduce unrelated search terms in `experiments[1]["retrieval_terms"]` and see whether retrieval failure disappears.
- Add one more row to `documents` and see how a larger document set affects the answer.
- Change `generate_answer` so document titles are kept like citations.
- Expand the `answer_overclaims` rule to catch more exaggerating expressions such as `always`, `perfectly`, and `solves automatically`.

## Failure stages split in a RAG pipeline

The example above is not a complete implementation of retrieval and generation. It is the shortest scene that shows that `the stage that finds documents` and `the stage that attaches those documents and creates an answer` are actually separate. The important thing is not the answer sentence itself, but the structure in which evidence documents remain independent input components until just before answering. If retrieval results look wrong, this also means we should revisit `which documents were attached` before changing the generation prompt. The fact that unrelated documents immediately destabilize the answer makes this separation clearer.

As a matrix of the three representative runs, the normal retrieval example turns on only related top-document retrieval and leaves no failure signal. The retrieval-contamination example turns on irrelevant-document inclusion, answer contamination, and retrieval failure together. The answer-overclaim example retrieves related documents but turns on overclaiming and generation failure separately. In other words, even results that look like the same wrong answer can be read by the stage where they became unstable. In RAG inspection, we should separate which stage record to revisit before concluding only that the answer is wrong.

![Matrix showing retrieval contamination and generation overclaiming as different failure locations in the RAG example](/AiBook/assets/part-06/chapter-11/rag-failure-split-en.png)

The conclusion to keep from this matrix is simple. The actual RAG combination flow has two stages: `attach documents first, then answer on top of them`. When an answer is wrong, we need to decide separately whether to fix retrieval or to fix generation instructions and evaluation. This distinction connects the next chapter on vector databases and indexes to retrieval-quality inspection, and the later evaluation chapter to answer-quality inspection.

## Checklist

- Can you explain that retrieval results are input components before generation, not attachments after the answer?
- Can you describe retrieval failure and generation failure as separate problems?
- Are you ready to read the next chapter as the problem of `how to find documents faster and more relevantly`?

## Sources and references

- Patrick Lewis et al., [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://papers.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html){: target="_blank" rel="noopener noreferrer" }, NeurIPS, 2020, accessed: 2026-07-19.
- OpenAI, [Retrieval](https://developers.openai.com/api/docs/guides/retrieval){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed: 2026-07-19.
- OpenAI, [File search](https://developers.openai.com/api/docs/guides/tools-file-search){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, accessed: 2026-07-19.
- scikit-learn developers, [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, accessed: 2026-07-22.
- scikit-learn developers, [Cosine similarity](https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, accessed: 2026-07-22.
