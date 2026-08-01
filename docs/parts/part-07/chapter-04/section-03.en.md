# P7-4.3 Representation-Normalization Practice

> Section ID: `P7-4.3`
> Version: `v2026.08.01`

Normalization changes a representation and therefore can change which differences a model treats as important. This practice compares a fixed task before and after normalization, then reads recovered cases, remaining cases, and newly wrong cases separately.

## Keep the comparison accountable

- Hold the task, split, and evaluation rows fixed.
- State the normalization transformation and what statistics it uses.
- Compare metric changes with sample-level prediction transitions.
- Record limitations and the next boundary case to collect.

An improved average does not make normalization automatically appropriate for every input. The project record must identify what changed, for whom, and what remains uncertain.

## Learning questions and criteria

- Which expression directly creates a wrong operational route, and which only lowers coverage?
- Why must a rule be evaluated for prediction regression as well as for its coverage increase?
- How can an undecided zero-signal or tied-score input be kept separate from a confident class prediction?

You have completed this practice when you can run the same evaluation rows before and after one stated normalization map, name every recovered or regressed case, and choose a reversible next action.

## Compare two routing expressions before and after normalization

Use the same [`p7-4-support-routing-dataset.csv`](../../../assets/part-07/chapter-04/p7-4-support-routing-dataset.csv){ .csv-preview } evaluation set as P7-4.2. The practice map is `캔슬 → 취소`, `스케줄 → 일정`, and `하자 → 불량`. It changes expressions only at whitespace-separated boundaries, avoiding substitutions inside a longer token.

| Evaluation sample | Original text | Normalized text | What to inspect |
| --- | --- | --- | --- |
| 평가-05 | `캔슬 후 송장 남아 있어요` | `취소 후 송장 남아 있어요` | Whether a missing cancellation intent is restored. |
| 평가-07 | `하자 제품 환불 스케줄 알고 싶어요` | `불량 제품 환불 일정 알고 싶어요` | Whether coverage improves even when the label stays correct. |

The case flow turns this into two different priorities. Low coverage is shared evidence; the outcome and the key expression determine the action.

```mermaid
--8<-- "assets/part-07/chapter-04/p7-4-3-normalization-case-flow-en.mmd"
```

The comparison output in the current dataset is:

```text
original accuracy: 0.857
normalized accuracy: 1.000
coverage increased: 평가-05, 평가-07
prediction changed: 평가-05
original undecided samples: none
normalized undecided samples: none
```

| Sample | Before | After | Review decision |
| --- | --- | --- | --- |
| 평가-05 | Coverage 0.200; predicted delivery, wrong | Coverage 0.400; predicted refund, correct | Prioritize normalization: `캔슬` directly caused an error. |
| 평가-07 | Coverage 0.333; predicted refund, correct | Coverage 0.667; predicted refund, correct | Next cleanup candidate: `하자` and `스케줄` lower coverage but do not cause this error. |

The priority is not simply the number of OOV tokens. First normalize an expression that creates an operationally wrong decision. Then schedule low-coverage expressions whose current prediction is correct. If a rule raises coverage but turns a correct prediction into an error or an undecided output, record “revert or recheck” ahead of any coverage benefit.

The full workflow holds the evaluation set fixed and places the safety checks after the before/after comparison.

```mermaid
--8<-- "assets/part-07/chapter-04/p7-4-3-normalization-workflow-en.mmd"
```

## Leave a normalization record

| Field | What to write |
| --- | --- |
| Raw expression | The original phrase, such as `캔슬`. |
| Normalized expression | The replacement, such as `취소`. |
| Coverage change | The before/after fraction of known tokens. |
| Prediction change | Team label, error status, or undecided status. |
| Remaining OOV | Expressions that still have no training-vocabulary match. |
| Review decision | Prioritize, next cleanup candidate, add data/rule, or revert/recheck. |

> `캔슬 후 송장 남아 있어요` is misrouted to delivery before normalization. Replacing `캔슬` with `취소` raises coverage from 0.200 to 0.400 and changes the prediction to the correct refund team. `하자 제품 환불 스케줄 알고 싶어요` remains correctly routed while coverage rises from 0.333 to 0.667. Add the error-causing synonym first; leave the already-correct low-coverage phrases as a later cleanup priority.

## Run a boundary-aware comparison

Run this code from the repository root. It uses the same whitespace tokenization and class-profile scorer as P7-4.2, but labels a zero-feature or tied-score row as `undecided` rather than silently selecting the first class.

```python
import csv
import re
from pathlib import Path
import numpy as np

rows = list(csv.DictReader(Path("docs/assets/part-07/chapter-04/p7-4-support-routing-dataset.csv").open(encoding="utf-8")))
train_rows = [row for row in rows if row["split"] == "train"]
test_rows = [row for row in rows if row["split"] == "test"]
normalization_map = {"캔슬": "취소", "스케줄": "일정", "하자": "불량"}

def tokenize(text): return text.split()
def normalize(text):
    for raw, replacement in sorted(normalization_map.items(), key=lambda item: len(item[0]), reverse=True):
        text = re.sub(rf"(?<!\S){re.escape(raw)}(?!\S)", replacement, text)
    return text

vocabulary = sorted({token for row in train_rows for token in tokenize(row["text"])})
index = {token: position for position, token in enumerate(vocabulary)}
def vectorize(texts):
    matrix, coverages, oov_lists = np.zeros((len(texts), len(vocabulary))), [], []
    for row_number, text in enumerate(texts):
        tokens = tokenize(text); known, oov = 0, []
        for token in tokens:
            if token in index: matrix[row_number, index[token]] += 1; known += 1
            else: oov.append(token)
        coverages.append(round(known / len(tokens), 3) if tokens else 0.0); oov_lists.append(oov)
    return matrix, coverages, oov_lists

X_train, _, _ = vectorize([row["text"] for row in train_rows])
y_train = np.array([int(row["label"]) for row in train_rows])
profiles = np.vstack([X_train[y_train == label].sum(axis=0) for label in (0, 1)])
def predict(matrix):
    scores = matrix @ profiles.T
    winner = scores.argmax(axis=1)
    return np.where((matrix.sum(axis=1) > 0) & (np.ptp(scores, axis=1) > 0), winner, -1)
def status(prediction, actual): return "undecided" if prediction == -1 else "correct" if prediction == actual else "incorrect"

original = [row["text"] for row in test_rows]; normalized = [normalize(text) for text in original]
X_before, coverage_before, oov_before = vectorize(original)
X_after, coverage_after, oov_after = vectorize(normalized)
y_test = np.array([int(row["label"]) for row in test_rows]); before, after = predict(X_before), predict(X_after)
print({"original_accuracy": round(float((before == y_test).mean()), 3), "normalized_accuracy": round(float((after == y_test).mean()), 3), "coverage_increased": [row["sample_id"] for row, old, new in zip(test_rows, coverage_before, coverage_after) if new > old], "prediction_changed": [row["sample_id"] for row, old, new in zip(test_rows, before, after) if old != new]})
for row, old_text, new_text, old_cov, new_cov, old_oov, new_oov, old_pred, new_pred, actual in zip(test_rows, original, normalized, coverage_before, coverage_after, oov_before, oov_after, before, after, y_test):
    if row["sample_id"] in {"평가-05", "평가-07"}:
        print({"sample": row["sample_id"], "before": old_text, "after": new_text, "coverage": (old_cov, new_cov), "oov": (old_oov, new_oov), "status": (status(old_pred, actual), status(new_pred, actual))})
```

The code makes two safety rules explicit. First, replacements run from longest expression to shortest and only at whitespace boundaries; a rule for a word cannot silently modify part of a longer token. Second, the program does not turn a tie into a confident refund prediction. Both rules make the before/after record more trustworthy.

## Read the before/after output

The output establishes the following facts for the current practice CSV:

| Observation | Before normalization | After normalization | Meaning for the record |
| --- | --- | --- | --- |
| Aggregate accuracy | `0.857` | `1.000` | One previously incorrect evaluation row recovered. |
| Test-05 coverage | `0.200` | `0.400` | The cancellation synonym became a known refund expression. |
| Test-05 status | Incorrect delivery route | Correct refund route | This rule is an immediate normalization priority. |
| Test-07 coverage | `0.333` | `0.667` | Two familiar expressions became available to the scorer. |
| Test-07 status | Correct refund route | Correct refund route | This is a cleanup candidate, not evidence of an already fixed error. |

The aggregate improvement is a useful summary, but it is not the decision on its own. The sample transition identifies why the accuracy changed and which rule should be retained first. Keeping both levels in the record prevents a one-row recovery from becoming a broad claim about every synonym.

### Four possible normalization outcomes

Every proposed map entry can be classified by its sample-level transition.

| Before status | After status | Review decision | Reason |
| --- | --- | --- | --- |
| Incorrect or undecided | Correct | Prioritize normalization | The change restores a usable decision. |
| Correct | Correct, with higher coverage | Later cleanup candidate | The rule may improve robustness but has not corrected this case. |
| Correct | Incorrect or undecided | Revert or recheck | A coverage gain never outweighs a prediction regression. |
| Incorrect or undecided | Incorrect or undecided | Add rule or data | The current change did not repair the decision. |

This table also explains why coverage must not be optimized in isolation. A rule can increase the number of known tokens while changing the class evidence in an unsafe way. The actual label and the undecided state are part of the evaluation contract.

## Separate a safe rule from a broad replacement

The map in this practice contains narrow expression substitutions. It is not permission to replace any word that appears near a class label. A rule should have a documented scope, examples it is expected to change, and examples that could reveal overreach.

| Rule | Intended effect | Evidence in the current rows | Boundary risk to test |
| --- | --- | --- | --- |
| `캔슬 → 취소` | Recover a cancellation request | Test-05 changes from incorrect to correct | Does the term occur in a non-cancellation context? |
| `하자 → 불량` | Make a defect synonym familiar | Test-07 coverage rises | Does the replacement alter another product-status meaning? |
| `스케줄 → 일정` | Make a schedule synonym familiar | Test-07 coverage rises | Is schedule used as an unrelated technical term? |

The practice scorer uses whitespace tokens, so its behavior is deliberately simple. In a production tokenizer, the same question becomes: which token sequence is replaced, what is the scope of the rule, and how is the original text retained for audit? The before text must stay available even when an input representation is normalized.

## Test independent scenarios

Start every scenario from the original CSV and the default three-entry map. Do not leave a changed row or a deliberately bad rule in the next scenario; otherwise a later result cannot be attributed to one intervention.

1. Change test-05 to `캔슬 후 남아 있어요`.
   - Before normalization, no known token remains and the output should be `undecided` rather than a first-class guess.
   - After normalization, coverage is `0.250` and the refund route is restored.
   - Record that the recovery comes from giving the scorer a known cancellation signal.

2. Append an unseen word such as `ASAP` to test-07.
   - Coverage can rise after normalization while an OOV term remains.
   - If the route stays correct, write a tokenization or data-coverage question, not “problem solved.”

3. Add a multiword rule, `환불 요청 → 환불`.
   - Confirm that the longest boundary-aware rule runs as one expression.
   - Test a longer token such as `환불 요청서` and verify that it is not partially changed.

4. Deliberately add an unsafe rule, `환불 → 배송`, for the default test-07.
   - The coverage may remain high while a correct refund route becomes incorrect.
   - The only valid review decision is to revert or recheck the rule; remove it after the test.

5. Add `취소 → 배송` while keeping the default test-05.
   - The cancellation expression becomes known, but the wrong route remains.
   - Classify this as rule-or-data reinforcement rather than success.

These scenarios are teaching controls, not recommended production rules. Their value is that they make the regression and residual-error branches observable without changing the task, labels, or evaluation rows.

## Build a project normalization log

Use one line per affected expression and one line per affected evaluation case. Do not combine these two levels: one expression can occur in multiple cases, and one case can contain multiple OOV expressions.

```text
rule identifier:
raw expression and normalized expression:
boundary or tokenizer rule:
training-vocabulary evidence:
evaluation sample identifier:
before text and normalized text:
coverage before/after:
OOV before/after:
prediction and status before/after:
review decision:
next data or rule test:
```

For the current run, a concise handoff could read:

> Test-05 was incorrectly sent to delivery with coverage 0.200. The boundary-aware `캔슬 → 취소` rule raised coverage to 0.400 and restored the refund route. Retain the rule as a priority candidate, test it on new cancellation wording, and keep the original text for audit. Test-07 stayed correct while coverage rose from 0.333 to 0.667, so its two synonym rules remain secondary cleanup candidates.

The wording distinguishes facts from the plan. It does not say the rules are universally correct, and it does not hide that test-07 was already correct before the change.

## Limits and next questions

This is a small synthetic dataset with a fixed vocabulary and a transparent class-profile scorer. It cannot establish how a larger language model, a subword tokenizer, or a production support queue will behave. It can establish the comparison discipline needed before adopting a normalization change.

- Would the rule still help on newly collected cancellation phrasing?
- Does a label guideline distinguish cancellation from delivery-status questions clearly enough?
- Which remaining OOV expressions recur across correct and incorrect cases?
- Does a more flexible tokenizer reduce the need for manual normalization without introducing another failure mode?
- Which regression test must remain in the evaluation set before the map is changed again?

Answering these questions can lead to more data, revised labeling, a new tokenizer, or a constrained rule map. The evidence in this section is only sufficient for the first, reversible next step.

## Final self-review

Use this checklist after each normalization experiment:

| Check | Question |
| --- | --- |
| Fixed conditions | Did the task, labels, split, and evaluation rows remain unchanged? |
| Rule scope | Is the replacement boundary-aware and documented? |
| Evidence | Are original and normalized texts both retained? |
| Coverage | Did the log show known-token fraction and remaining OOV tokens? |
| Prediction | Did it show class prediction or `undecided` before and after? |
| Recovery | Which incorrect or undecided row became correct? |
| Regression | Did any correct row become incorrect or undecided? |
| Residual risk | Which row remains incorrect, undecided, or low coverage? |
| Next action | Is the decision a priority rule, cleanup, revert, or added data? |

### What not to collapse

Keep these pairs distinct in the final note:

- **Coverage improvement** and **prediction improvement** are related but not identical.
- **Correct now** and **robust to new phrasing** are different claims.
- **A rule candidate** and **a validated production rule** have different evidence requirements.
- **No signal / score tie** and **a confident prediction for class zero** are different states.

The distinction is especially important when a score table appears to improve. A result can contain a genuine recovery, a harmless cleanup, and an unsafe regression at the same time. The review record must make each path visible.

### Handoff to the next iteration

Before changing the normalization map again, freeze the current map, evaluation rows, and before/after record. Add the recovered test-05 expression and at least one possible regression case to the next regression set. Then propose only one map or data change, rerun the comparison, and explain any changed transition. This small discipline keeps normalization from becoming an untraceable collection of text edits.

## Design a safe follow-up experiment

The next iteration should answer one question that the current comparison cannot answer. Choose the question before editing the map.

| Question | Fixed evidence | One permitted change | Expected observation |
| --- | --- | --- | --- |
| Does the cancellation rule generalize? | Current train rows and regression rows | Add new cancellation wording to evaluation | Count correct, incorrect, and undecided transitions. |
| Is the defect synonym safe? | Current map except the tested entry | Add one context with `하자` | Check whether its normalized route remains appropriate. |
| Do remaining OOV terms matter? | Current tokenization and scores | Add one recurring unfamiliar term | Compare its coverage and status, not coverage alone. |
| Is a new data example preferable to a rule? | Same evaluation rows | Add a documented training example | Re-run with the map unchanged. |

The “one permitted change” column is not bureaucracy. It is what allows a reviewer to connect a changed outcome to a candidate cause. If both the map and the training data change together, a recovery can no longer be assigned to either intervention.

### Interpret no change correctly

A rule can produce no visible metric change for several reasons. The expression may not appear in the evaluation set, it may already be represented by another known term, or it may be irrelevant to the class scores. Record the rule and the no-change result. Do not delete it from the experiment history merely because it did not improve the displayed accuracy.

Likewise, do not keep a rule solely because it changes a number. A tiny coverage increase with no identifiable input meaning may not justify the added maintenance burden. The project should define who owns the map, when entries expire or are reviewed, and which regression set protects the routing behavior.

## Compare source text and model text

Normalization changes the model input, not necessarily the text a support agent or auditor should see. Preserve both forms.

| Field | Example | Why it is retained |
| --- | --- | --- |
| Source text | `캔슬 후 송장 남아 있어요` | It is the evidence of the customer’s actual wording. |
| Model text | `취소 후 송장 남아 있어요` | It makes the applied representation explicit. |
| Rule ID | `cancel_synonym_v1` | It lets another reviewer locate the transformation. |
| Prediction record | delivery → refund | It records the operational consequence. |

This distinction is especially important when the map is maintained over time. A later reviewer may disagree with a rule, but can still reproduce the previous prediction if the original sentence and the exact rule version remain available.

### Questions for a reviewer

Ask a reviewer to answer these questions from the record alone:

1. Which exact expression was changed, and at which token boundary?
2. Which fixed evaluation row recovered, regressed, or remained unresolved?
3. Did the result contain a prediction, an error, or an undecided tie?
4. What evidence makes this rule a priority rather than a later cleanup task?
5. Which next experiment would disprove the current interpretation?

If the record cannot answer those questions, the normalization result is not ready to guide the next iteration.

Keep the current map version with the comparison output.
Keep the original source rows unchanged during every independent scenario.
Keep recovered and regressed samples in the next regression set.
Keep the causal interpretation narrower than the observed transition.

## Try independent changes

1. Change evaluation sample 05 to `캔슬 후 남아 있어요`.
   - Before normalization, coverage is `0.000` and the class-score tie should be shown as undecided rather than as a confident first-label prediction.
   - After normalization, coverage becomes `0.250` and the refund prediction is restored.
2. Add another unfamiliar token to sample 07, such as `ASAP`.
   - Observe that coverage can improve after normalization while an OOV still remains.
   - If the refund prediction remains correct, record a cleanup or tokenization question rather than a solved error.
3. Add a longer phrase rule such as `환불 요청 → 환불`.
   - Check the rule at token boundaries and record whether it changes prediction or only coverage.

Normalization is an experiment variable. Restore the original row before each independent scenario, preserve the same evaluation set, and do not generalize one rule’s success to every operational phrase.

## Checklist

| Check | Question to answer |
| --- | --- |
| Transformation | What representation change was applied? |
| Reference | Which training information determined it? |
| Recovery | Which case became correct? |
| Regression | Which case became newly wrong? |
| Next question | What further representation or data test is needed? |

## Sources and references

Keep the original row before each normalization scenario.
Record the exact rule and its source evidence.
Test the named recovery and every regression reference.
Separate coverage changes from prediction changes.
Use the same evaluation rows for the next comparison.
Do not promote a local rule into a general language claim.
Keep the unresolved phrase as a project artifact.

The normalization practice is book-created material.
