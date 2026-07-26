# P6-20.2 Understanding-Centered Tasks that Output Judgment Values Before Long Answers

> Section ID: `P6-20.2`
> Version: `v2026.07.26`

If the BERT family is read as a Transformer-encoder-based representation model, you also need to distinguish which task groups those representations lead to. Understanding-centered tasks read the whole input and judge `what it is` or `how well it matches`, such as classification, relevance judgment, search, and embeddings. These tasks fit BERT-family representation models well.

## Output Forms in Understanding-Centered Tasks

Understanding-centered output begins from these questions.

- How can `understanding-centered task` be explained?
- In which tasks was the BERT family especially useful?
- How can classification, search, sentence-pair comparison, and embeddings be tied into one flow?

It is safest to hold understanding-centered tasks as `a task group that reads input and outputs a label, score, or vector`. Then why this flow fits the BERT family also becomes clearer.

This comparison criterion can be recovered again in P6-12.1 vector databases and P6-12.2 indexes and search quality when reading how structures split inside a search pipeline.

Rather than listing many task names, it is more important to understand `a flow that reads input and judges`. If the previous section set the position of the BERT family as a comparison criterion, this section narrows that comparison into actual task groups and first distinguishes why `labels`, `scores`, `ranks`, and `vectors` belong to one output family.

So we should look at the difference between `a structure that reads and outputs judgment values` and `a structure that generates long text`, rather than memorizing task names. Instead of learning understanding-centered tasks as a new list, it is enough to hold the commonality that classification, relevance judgment, search, and embeddings all `read input and output judgment values`.

## Separating Long Answer Generation from Judgment-Value Output

- You can explain understanding-centered tasks at an introductory level.
- You can group classification, relevance judgment, search, and embeddings as the same family of work.
- You can say why these tasks fit the BERT family.
- You can read the contrast with the GPT family more clearly.

## What Is an Understanding-Centered Task?

Here, `understanding-centered task` does not mean philosophical human-like understanding. It refers to task groups such as:

- What label does this input belong to?
- Are these two sentences close in meaning?
- How relevant is this question to this document?
- What vector represents this sentence?

So the output leads not to a long generated sentence, but to:

- label,
- score,
- relevance, or
- representative expression.

## Input and Output of Understanding-Centered Tasks

This flow becomes easier to grasp by asking `what judgment result does the input produce?`, rather than `does the model continue writing the next sentence?`

| Task | Input | Output |
| --- | --- | --- |
| Classification | one sentence | label |
| Sentence-pair judgment | two sentences | relation label or score such as related / not related |
| Search ranking | question and document candidates | relevance score, sorted order |
| Embedding | sentence or document | vector representation |

The output of an understanding-centered task is usually not `the next sentence`, but `an artifact for judgment`.

## Representative Task 1. Document and Sentiment Classification

The most familiar example is classification.

For example:

- spam / normal email classification,
- inquiry category classification,
- sentiment classification(positive / negative / neutral).

These tasks read the whole sentence and judge `which category it belongs to`.

Because the BERT family creates representations that reflect the whole input context, it fits these tasks well.

## Representative Task 2. Sentence-Pair Judgment

Tasks that judge the relationship between two sentences are also important.

For example:

- Are two sentences close in meaning?
- Do the question and answer match each other?
- Does sentence A entail sentence B?

These tasks go one step beyond single-sentence classification and ask about the relationship between two inputs.

It is enough to understand it this way:

`Sentence-pair judgment is not reading one input, but comparing the relationship between two inputs and outputting a score or label.`

## Representative Task 3. Search and Ranking

Search can also be read as an understanding-centered task.

Given a question as input, the system judges:

- which document is related;
- which document should be placed higher among several candidates.

Here, the BERT family can connect in two ways.

- Read the question and document together and output a relevance score.
- Convert the question and document into representation vectors separately and compare them.

The latter connects directly to embedding search.

## Representative Task 4. Embeddings and Representation Reuse

The BERT family and later encoder-centered models are also widely used to turn sentences into embeddings.

For example:

- finding similar sentences,
- finding duplicate FAQ questions,
- clustering documents,
- generating dense vectors for search.

These tasks are closer to `representation reuse` than to `generation`.

So the BERT family can be read not only as classification models, but also as a common representation engine for many judgment tasks.

## Why These Tasks Belong to One Flow

These tasks look different on the surface, but their central questions are similar.

- What is it?
- How similar are they?
- How relevant is it?
- Which category does it belong to?

They are closer to `reading input and judging` than to `generating the next sentence at length`.

They can be grouped into one flow as follows.

```mermaid
--8<-- "assets/part-06/chapter-20/p6-c20-s02-understanding-output-flow-en.mmd"
```

This diagram groups the practical use intuition of the BERT family in the simplest way. The result to confirm is whether work that first needs `reading, distinguishing, and connecting` appears separately from long answer generation.

## Distinguishing Output Forms

The distinction to keep first is one line:

`The BERT family is more natural for reading input and creating labels, scores, relevance, and embeddings than for generating long answers.`

Once this line is fixed, you do not need to memorize every detailed task name to read the GPT and next-token prediction explanations in P6-5.1 and P6-6.1 or the RAG explanations in P6-11.1 and P6-11.2.

## Cases and Examples

### Case 1. Customer Inquiry Classification

Classifying customer inquiries into `shipping`, `account`, `payment`, and `error` is a typical understanding-centered task. Even in this scene, it is easy to think that a good service is one where the model writes a long and kind explanation. But in real operation, deciding `which handling flow should receive this?` is more important than a long answer.

For example, a sentence such as `The payment went through, but I cannot see the order` shows payment and order together, but the actual operation needs to know which team should look first. Sending it first to `payment confirmation` or `order synchronization check` affects service handling speed more directly than writing a long answer.

If the request is sent to the wrong queue, even a well-written answer can slow the actual resolution. The important work is not writing a long response, but reading the incoming sentence and deciding which handling flow it should enter. The misunderstanding to correct is the feeling that `a good explanation helps first`. In reality, only after `who should handle it first?` is closed does the next explanation matter. The result to confirm in this case is whether the request first enters the right handling queue, and whether the queue choice alone lets the next operation continue immediately, more than answer-sentence quality.

### Case 2. FAQ Search

Comparing a user question with existing FAQs to find the closest item is a case where relevance judgment and embedding search are used together. In this scene, it is easy to think, `Wouldn't it look better if the model rewrote a new explanation nicely?` But even people usually first choose `which existing answer fits best`, instead of writing a new explanation.

For example, `I forgot my password` and `How do I reset my login password?` are better connected to the same help article even though their surface expressions differ. If an existing FAQ already includes step-by-step screenshots, connecting to that item accurately is much safer than generating a new answer.

Conversely, if the system chooses an unrelated FAQ and adds a new natural-sounding sentence, the user can be sent down the wrong path. The core here is not `creating a new sentence`, but `choosing the best matching document`. The misunderstanding to correct is the expectation that `a generative answer always looks smarter than search`. In reality, accurately connecting an existing correct document is often far more practical. The result to confirm in this case is whether the closest FAQ item is connected first, before a new answer is generated, and whether that connection alone lets the user take the next action.

### Case 3. Document Duplicate Detection

Determining whether two document titles and bodies are almost the same can be read as a sentence-pair comparison and similarity judgment flow. In this task too, it is easy to think first of having the model summarize or merge the documents. But people usually first check `how similar are they?` before `rewriting both`.

For example, if two notices differ only in sentence order and have the same core content, grouping them as duplicates may matter more operationally than creating a new answer. Even if one title is `maintenance guide` and the other is `service maintenance notice`, duplicate judgment is more important if the bodies explain the same event.

If duplicates are missed, similar documents keep piling up and search results become messy. This case also belongs to the same family because it is `reading, comparing, and scoring`. The shift here is from asking `should a new explanation be generated?` to asking `are the two documents actually one group?` The misunderstanding to correct is the expectation that `text work is generation first`. The result to confirm in this case is whether duplicate documents are actually organized into one group, instead of being left as new documents, and whether the judgment value can be used directly for later search cleanup.

The three cases can be grouped again from the viewpoint of understanding-centered tasks.

| Situation | Judgment needed before generation | What remains first as actual output |
| --- | --- | --- |
| Customer inquiry classification | Which handling queue should receive it? | label |
| FAQ search | Which existing item is closest? | relevance rank |
| Document duplicate detection | Do the two documents say the same thing? | similarity score or duplicate judgment |

## Scenes Where Judgment Values Are Needed First

A common misunderstanding when first reading understanding-centered tasks is to think `AI should first generate a long answer`. But the first thing to check is whether the needed output is a label, score, or rank rather than long-form generation. Turned into practical questions, this reads as follows.

| If this suspicion appears | First question to ask |
| --- | --- |
| `Should this write an answer, or classify first?` | Is the needed output a sentence or a label? |
| `Isn't the existing document better?` | Should relevance ranking be produced before new generation? |
| `They look similar, but are they the same handling flow?` | Should the comparison result remain first as a score or judgment? |

The first criterion to learn is simple. Understanding-centered tasks are closer to a judgment structure of `read -> label/score/rank/vector` than to `long answer generation`. The BERT family should therefore be read not as a generation competitor, but as a front-end structure that reads and distinguishes.

## Exercise and Example

The goal of the example is to check, with a small vector-representation experiment, that understanding-centered tasks actually output judgment results such as `labels`, `relation scores`, and `search ranks`.

Unlike a generative response, the example below checks the structure where an understanding-centered task reads and outputs judgment values. The input CSV [p6-20-understanding-task-cases-en.csv](/AiBook/assets/part-06/chapter-20/p6-20-understanding-task-cases-en.csv){ .csv-preview } contains 12 cases each for classification, sentence-pair judgment, and search ranking. One row is one judgment case. `task_type` indicates the output form, and `scenario_pattern` indicates the observation role, such as direct signal, boundary signal, or different intent.

The key to confirm is that understanding-centered tasks output labels, scores, and ranks before long answers. Here we do not download and run BERT directly. Instead, we use locally reproducible TF-IDF vectors as small substitute representations. In a real BERT family model, those representations become richer contextual representations, but the output flow `turn input into representation, then output a judgment value` is the same.

The value to try changing in the code is `relation_threshold`. If you raise it, sentence-pair judgment becomes more conservative, and some boundary cases move from `related` to `not_related`. This change shows that the output of an understanding-centered task is closer to `which judgment value is produced from scores between representations` than to a long sentence.

```python
# This example reads classification, sentence-pair relation, and document-ranking
# cases from CSV and checks how input representations become labels, relation
# scores, and document ranks.
import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

case_path = Path("docs/assets/part-06/chapter-20/p6-20-understanding-task-cases-en.csv")

domain_terms = {
    "shipping": ["shipping", "package", "sent", "address", "arrived", "box", "delivery"],
    "account": ["account", "login", "password", "verification", "code", "lock", "reset", "email"],
    "payment": ["payment", "refund", "cancel", "receipt", "billing", "money", "record", "order"],
    "document": ["FAQ", "notice", "duplicate", "document", "maintenance", "guide"],
    "equipment": ["resignation", "offboarding", "equipment", "asset", "return", "recovery"],
}

queue_prototypes = {
    "shipping": "shipping delay package sent address box shipping lookup delivery address",
    "account": "login password account verification code lock authentication email reset",
    "payment": "payment refund cancel receipt billing money record order payment status",
}

def enrich(text):
    if text == "-":
        return ""
    lowered = text.lower()
    tags = []
    for tag, terms in domain_terms.items():
        if any(term.lower() in lowered for term in terms):
            tags.extend([tag, tag])
    return text + " " + " ".join(tags)

def cosine_scores(left_texts, right_texts):
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
    matrix = vectorizer.fit_transform([enrich(text) for text in left_texts + right_texts])
    left_matrix = matrix[:len(left_texts)]
    right_matrix = matrix[len(left_texts):]
    return cosine_similarity(left_matrix, right_matrix)

with case_path.open(encoding="utf-8", newline="") as file:
    cases = list(csv.DictReader(file))

classification_rows = [row for row in cases if row["task_type"] == "classification"]
pair_rows = [row for row in cases if row["task_type"] == "pair_relation"]
ranking_rows = [row for row in cases if row["task_type"] == "ranking"]

queue_names = list(queue_prototypes)
queue_scores = cosine_scores(
    [row["text_a"] for row in classification_rows],
    list(queue_prototypes.values()),
)
classification_outputs = []
for row, scores in zip(classification_rows, queue_scores):
    best_index = scores.argmax()
    classification_outputs.append(
        {
            "case_id": row["case_id"],
            "pattern": row["scenario_pattern"],
            "output": queue_names[best_index],
            "score": round(float(scores[best_index]), 2),
        }
    )

relation_threshold = 0.24
strict_relation_threshold = 0.34
pair_scores = cosine_scores(
    [row["text_a"] for row in pair_rows],
    [row["text_b"] for row in pair_rows],
)
pair_outputs = []
for index, row in enumerate(pair_rows):
    similarity = float(pair_scores[index][index])
    pair_outputs.append(
        {
            "case_id": row["case_id"],
            "pattern": row["scenario_pattern"],
            "similarity": round(similarity, 2),
            "output": "related" if similarity >= relation_threshold else "not_related",
            "strict_output": "related" if similarity >= strict_relation_threshold else "not_related",
        }
    )

ranking_outputs = []
for row in ranking_rows:
    candidates = [row["candidate_1"], row["candidate_2"], row["candidate_3"]]
    scores = cosine_scores([row["text_a"]], candidates)[0]
    ranked = sorted(zip(candidates, scores), key=lambda item: item[1], reverse=True)
    ranking_outputs.append(
        {
            "case_id": row["case_id"],
            "pattern": row["scenario_pattern"],
            "top_document": ranked[0][0],
            "top_score": round(float(ranked[0][1]), 2),
        }
    )

by_task = {
    "classification": classification_outputs,
    "pair_relation": pair_outputs,
    "ranking": ranking_outputs,
}

print("[dataset]")
print("case_count =", len(cases))
print("task_counts =", {task: len(items) for task, items in by_task.items()})
print("representation = char_wb 2-4 gram TF-IDF + domain terms")
print("relation_threshold =", relation_threshold)
print("strict_relation_threshold =", strict_relation_threshold)
print()

for task_type in ["classification", "pair_relation", "ranking"]:
    print(f"[{task_type} preview]")
    for item in by_task[task_type][:3]:
        print(item)
    print("---")

changed = [item for item in pair_outputs if item["output"] != item["strict_output"]]
print("[threshold sensitivity]")
print("changed_pair_cases =", changed[:5])
```

An example run can be read as follows. The `representation` line means this example does not only count text as raw keywords. It turns sentences into a small vector representation and then produces labels, relation scores, and document ranks.

```text
[dataset]
case_count = 36
task_counts = {'classification': 12, 'pair_relation': 12, 'ranking': 12}
representation = char_wb 2-4 gram TF-IDF + domain terms
relation_threshold = 0.24
strict_relation_threshold = 0.34

[classification preview]
{'case_id': 'C01', 'pattern': 'direct_label', 'output': 'shipping', 'score': 0.61}
{'case_id': 'C02', 'pattern': 'direct_label', 'output': 'account', 'score': 0.56}
{'case_id': 'C03', 'pattern': 'direct_label', 'output': 'payment', 'score': 0.61}
---
[pair_relation preview]
{'case_id': 'P01', 'pattern': 'same_intent', 'similarity': 0.65, 'output': 'related', 'strict_output': 'related'}
{'case_id': 'P02', 'pattern': 'different_intent', 'similarity': 0.07, 'output': 'not_related', 'strict_output': 'not_related'}
{'case_id': 'P03', 'pattern': 'same_intent', 'similarity': 0.63, 'output': 'related', 'strict_output': 'related'}
---
[ranking preview]
{'case_id': 'R01', 'pattern': 'semantic_match', 'top_document': 'Offboarding equipment return guide', 'top_score': 0.57}
{'case_id': 'R02', 'pattern': 'semantic_match', 'top_document': 'Login password reset guide', 'top_score': 0.53}
{'case_id': 'R03', 'pattern': 'semantic_match', 'top_document': 'Refund request procedure after cancellation', 'top_score': 0.46}
---
[threshold sensitivity]
changed_pair_cases = [{'case_id': 'P05', 'pattern': 'same_intent', 'similarity': 0.31, 'output': 'related', 'strict_output': 'not_related'}, {'case_id': 'P10', 'pattern': 'near_boundary', 'similarity': 0.24, 'output': 'related', 'strict_output': 'not_related'}]
```

The key points to read from this example are:

- understanding-centered tasks usually output `judgment results`;
- the center is not making long answers like a generative model;
- classification, relation judgment, and search ranking can all be tied into the same flow of `read and output a score or label`;
- even small TF-IDF vectors can show which input changes into which judgment value, while actual BERT-family models perform this scoring on richer contextual representations;
- if `relation_threshold` is raised, boundary sentence pairs more easily change to `not_related`, showing that the judgment criterion changes the output label; and
- the BERT family fits these judgment tasks well.

The chart below summarizes the number of cases by task and the appearances of output forms from the same CSV. What matters here is not the bar value itself, but that classification, sentence-pair judgment, and ranking all leave judgment values such as labels, scores, and ranks instead of long answers.

![Output types in understanding-centered tasks](/AiBook/assets/part-06/chapter-20/understanding-output-types-en.png)

## Reconnecting Through Operational Judgment

The three cases above show classification, relevance judgment, and similarity judgment. If we reduce the same idea again from an operational viewpoint, the questions that must be checked before generation become clearer.

| Scene | Judgment to make first | Problem if generation comes first |
| --- | --- | --- |
| Customer inquiry classification | Which handling queue should receive it? | Even a polite answer delays resolution if the responsible team is wrong. |
| FAQ search | Which existing answer is closest? | Adding a new sentence may connect the user to the wrong FAQ. |
| Document duplicate detection | Do the two documents say the same thing? | Missing duplicates keeps search results and document management messy. |

The key when reading this table is simple. Generative models can be strong at producing long and natural sentences, but at the first stage of real operation, `what must be classified, compared, and connected first?` is often more urgent.

For example, if a refund inquiry is routed to an account-lock queue, even a smooth answer sentence makes handling slower. Conversely, when routing and search judgment are accurate first, the generated answer attached afterward starts from a safer position. So the result to check again is not the naturalness of a long answer draft, but whether the inquiry enters the right handling flow first and the relevant document is connected accurately first.

BERT mattered not simply because it was a new structure. It strongly showed that Transformer-encoder-based pretrained representations transfer well across many NLP tasks.

Through this period, many practical teams began to treat:

- classification,
- search,
- ranking,
- sentence similarity, and
- embedding generation

as one family of representation-model work.

## Why Separate This from Generation-Centered Structures?

At this point, the need for comparison becomes clearer.

- Unlike the BERT family, which reads input and judges, how does the GPT family `continue generation`?
- Why did the user experience change more visibly in the GPT family?

These questions make us reread P6-5.1 `The GPT Family as a Decoder-Based Cumulative Generation Structure`. The point is not that generation structures are unimportant. It is that a separate `judgment structure that first classifies, compares, and connects` is often needed in the front end of services. With this criterion, GPT-family models are less likely to be read as `the structure that does everything`, and the BERT family can be separated again as `another axis responsible for reading and judgment`.

## Checklist

- You should be able to explain understanding-centered tasks as `a task group that reads input and outputs labels, scores, relevance, or embeddings`.
- You should be able to say that classification, search, sentence-pair judgment, and embeddings have different names but belong to the same judgment flow.
- You should be able to explain the task-level difference between GPT-family and BERT-family use by distinguishing generation structures from judgment structures as different output problems.

## Sources and References

- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-07-19.
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, draft materials, accessed 2026-07-19.
- Matthew E. Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-07-19.
- scikit-learn, [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-24.
- scikit-learn, [cosine_similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-24.
