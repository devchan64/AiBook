# P7-4.1 Reading Loss, Metrics, and Error Cases Together

> Section ID: `P7-4.1`
> Version: `v2026.08.01`

Loss, metrics, and individual error cases answer different questions. Read them together: loss describes the optimization signal, a metric summarizes task performance, and an error case identifies what a person should inspect next.

## Do not let one curve decide the project record

| Evidence | Question it answers |
| --- | --- |
| Training and validation loss | Is the optimization signal changing across epochs? |
| Metric | How well does the model meet the chosen task measure? |
| Error case | Which input and prediction require diagnosis? |

A lower loss does not by itself establish that every important error disappeared. A metric rise does not identify whether a minority or boundary case got worse. Preserve all three kinds of evidence in the run record.

## Reproduce a text-routing learning record

The project question is: “Should a customer inquiry go to the refund team or the delivery team?” Use [`p7-4-support-routing-dataset.csv`](../../../assets/part-07/chapter-04/p7-4-support-routing-dataset.csv){ .csv-preview } for 12 training inquiries and 7 evaluation inquiries. A majority-label baseline reaches `0.714`; the learned bag-of-words softmax model reaches `0.857` and leaves evaluation sample `평가-05` for review.

```python
import csv
from pathlib import Path
import numpy as np

rows = list(csv.DictReader(Path("docs/assets/part-07/chapter-04/p7-4-support-routing-dataset.csv").open(encoding="utf-8")))
train_rows = [row for row in rows if row["split"] == "train"]
test_rows = [row for row in rows if row["split"] == "test"]
def tokens(text): return text.split()
vocab = sorted({token for row in train_rows for token in tokens(row["text"])})
index = {token: position for position, token in enumerate(vocab)}
def vectorize(selected):
    matrix = np.zeros((len(selected), len(vocab)))
    for row_number, row in enumerate(selected):
        for token in tokens(row["text"]):
            if token in index: matrix[row_number, index[token]] += 1
    return matrix
X_train, X_test = vectorize(train_rows), vectorize(test_rows)
y_train = np.array([int(row["label"]) for row in train_rows]); y_test = np.array([int(row["label"]) for row in test_rows])
W, b = np.zeros((len(vocab), 2)), np.zeros(2)
Y = np.eye(2)[y_train]
def softmax(values):
    shifted = values - values.max(axis=1, keepdims=True)
    e = np.exp(shifted); return e / e.sum(axis=1, keepdims=True)
def loss_accuracy(X, y):
    probabilities = softmax(X @ W + b)
    return float(-np.log(probabilities[np.arange(len(y)), y] + 1e-12).mean()), float((probabilities.argmax(axis=1) == y).mean())
baseline = int(np.bincount(y_train).argmax())
baseline_accuracy = float((np.full_like(y_test, baseline) == y_test).mean())
history = []
for epoch in range(1, 13):
    probabilities = softmax(X_train @ W + b)
    W -= .35 * X_train.T @ (probabilities - Y) / len(X_train); b -= .35 * (probabilities - Y).mean(axis=0)
    train_loss, train_accuracy = loss_accuracy(X_train, y_train); eval_loss, eval_accuracy = loss_accuracy(X_test, y_test)
    history.append({"epoch": epoch, "train_loss": round(train_loss, 3), "eval_loss": round(eval_loss, 3), "train_accuracy": round(train_accuracy, 3), "eval_accuracy": round(eval_accuracy, 3)})
predictions = softmax(X_test @ W + b).argmax(axis=1)
errors = [row["sample_id"] for row, prediction, actual in zip(test_rows, predictions, y_test) if prediction != actual]
print("baseline accuracy =", round(baseline_accuracy, 3)); print("first/last epoch =", history[0], history[-1]); print("error samples =", errors)
```

In the current CSV, evaluation accuracy is `1.000` in the earliest epochs and ends at `0.857`, while evaluation loss falls from `0.620` to `0.363`. This is an important counterexample: a lower loss and a metric can move differently, and a final loss value does not erase a newly visible error. Read the `평가-05` error together with the tokens that could imply either a cancelled/refund request or a shipping-tracking request.

| Fact | Interpretation | Next question |
| --- | --- | --- |
| Baseline is 0.714 and final evaluation accuracy is 0.857. | The learned representation improves this fixed split. | Does the improvement persist across another split? |
| Evaluation loss declines while final accuracy is lower. | Aggregate confidence and the count of correct labels can move differently. | Which sample changed class as epochs continued? |
| `평가-05` remains wrong. | Its wording may mix routing signals. | Should vocabulary, labels, or boundary cases be reviewed? |

## What an epoch log records in this practice

This example uses full-batch learning deliberately. All 12 training inquiries are read, one parameter update is made, and that unit is recorded as one epoch. A production run often uses mini-batches, where an epoch contains several updates. The simplified structure makes the reading order visible.

| Log field | What it means here |
| --- | --- |
| Epoch | One pass through the 12 training inquiries. |
| Step | One full-batch update in this simplified example. |
| Train loss | How strongly training probabilities support their correct labels. |
| Evaluation loss | The same probability-sensitive quantity on held-out inquiries. |
| Evaluation accuracy | The fraction of the 7 evaluation labels predicted correctly. |
| Baseline accuracy | The majority-label comparison result, fixed at 0.714. |

The first and final entries in the current run are:

```text
epoch 1:  train loss 0.589, evaluation loss 0.620, train accuracy 1.000, evaluation accuracy 1.000
epoch 2:  train loss 0.511, evaluation loss 0.567, train accuracy 1.000, evaluation accuracy 1.000
epoch 3:  train loss 0.451, evaluation loss 0.526, train accuracy 1.000, evaluation accuracy 1.000
epoch 10: train loss 0.237, evaluation loss 0.384, train accuracy 1.000, evaluation accuracy 0.857
epoch 11: train loss 0.221, evaluation loss 0.373, train accuracy 1.000, evaluation accuracy 0.857
epoch 12: train loss 0.207, evaluation loss 0.363, train accuracy 1.000, evaluation accuracy 0.857
```

This trace is more useful than a final score alone. Training loss falls throughout; evaluation loss also falls; evaluation accuracy changes from a perfect early value to six correct out of seven. The record should trigger a sample-level review rather than the claim that lower evaluation loss necessarily means a better final routing decision.

## Read the remaining routing error

| Evaluation sample | Text | Predicted team | Actual team | Probability reading |
| --- | --- | --- | --- | --- |
| 평가-05 | `캔슬 후 송장 남아 있어요` | Delivery | Refund | The wording includes a cancellation intent but a shipping-document term; the current representation favors delivery. |

The other six evaluation rows are correct at the last epoch. This one error is not enough to diagnose tokenization, label quality, or model capacity. It is enough to make a next review item concrete.

The project note should therefore retain both a stable summary and the individual record.

```text
Question: Route each support inquiry to refund or delivery.
Training count: 12
Evaluation count: 7
Baseline accuracy: 0.714
Final evaluation accuracy: 0.857
Evaluation loss at final epoch: 0.363
Remaining error sample: 평가-05
Next review: inspect cancellation vocabulary, shipping terms, and coverage for this sentence.
```

## Do not overread a curve

| Observation | What it supports | What it does not support |
| --- | --- | --- |
| Train loss declines | Parameters fit training labels more strongly. | That every evaluation group improves. |
| Evaluation loss declines | Correct-label probabilities changed on held-out rows. | That accuracy must rise at the same time. |
| Accuracy is above baseline at the end | The fixed split improves over the majority rule. | That the routing model is ready for every inquiry. |
| One error remains | A concrete review target exists. | A confirmed root cause. |

The phrase “learning has stopped” needs evidence from more than one number. Check whether loss has flattened, whether the error set is stable or changing, whether probabilities changed, and whether the comparison split is sufficiently large for a decision.

## Recreate the same record with a library

The NumPy implementation exposes loss and update mechanics. A production-oriented implementation may instead use a text vectorizer, a log-loss classifier, and a dummy baseline. The tooling changes, but the record fields do not: preserve baseline, epoch log, evaluation metric, error samples, split, and next question.

| Component | Role in a library workflow |
| --- | --- |
| `TfidfVectorizer` | Converts training text into reproducible feature weights. |
| `DummyClassifier` | Provides a simple comparison baseline. |
| `SGDClassifier` with log loss | Updates a linear text classifier by iterations. |
| Accuracy and log loss | Preserve metric and probability-sensitive reading. |

The library does not remove the need for error analysis. It makes the same question easier to repeat on a larger dataset, but it cannot decide whether `평가-05` is a vocabulary, coverage, data-range, or label-policy issue.

## Final project self-review

| Check | Question to answer |
| --- | --- |
| Baseline | Is the simple comparison score recorded? |
| Trace | Are train and evaluation loss/accuracy kept by epoch? |
| Unit | Is it clear whether an epoch contains one update or many batches? |
| Error | Is at least one remaining sentence identified by sample ID? |
| Interpretation | Are curve facts kept separate from a causal explanation? |
| Next fix | Does the note name a vocabulary, data, or evaluation check? |

## Checklist

| Check | Question to answer |
| --- | --- |
| Loss | Which split and epoch does the curve describe? |
| Metric | Is its definition appropriate for the task? |
| Error case | Which concrete example remains wrong? |
| Interpretation | What remains unproven by the curves? |
| Next question | What should be inspected or collected next? |

## Sources and references

The examples are book-created practice material.
