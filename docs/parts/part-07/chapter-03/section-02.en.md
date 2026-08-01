# P7-3.2 Comparing CNN, Sequential, and Attention Families

> Section ID: `P7-3.2`
> Version: `v2026.08.01`

CNN, sequential, and attention-family models are compared here as responses to different input relations, not as a ranking of architectures. A local visual neighborhood, an ordered sequence, and a long-range relation each make different information easy or difficult to use.

## What each family makes available

| Family | Strongest structural assumption | Review question |
| --- | --- | --- |
| CNN | Nearby locations share useful local patterns | Is local spatial structure decisive? |
| Sequential model | Earlier and later positions carry order | Does order change the meaning? |
| Attention family | Distant positions may need direct comparison | Which long-range relations matter? |

A family does not prove that its assumed structure is present in the data. Compare the representation, task output, error cases, computational cost, and missing evidence before claiming a better choice.

## Learning review

For each candidate, write one fact about the input relation it can use, one limitation it introduces, and one next experiment. A model label alone is not a project explanation.

## Learning questions and criteria

- Which held-out sample supplies the error evidence for the next trial?
- What portion of the issue is a data-range, representation, or model-family question?
- Why does a weak spatial patch make a CNN question more direct than a sequential-model question?

Complete the review by preserving the exact error, writing one bounded hypothesis at each level, and naming one fixed regression case for the next run.

## Read one weak-scratch failure as a structure question

In the surface-patch practice, the third evaluation patch is a weak scratch. Its brightness distribution remains close to normal surface values, but a faint vertical scratch appears near the center-right columns. The simple classifier produces these test probabilities.

```text
test probabilities =
[[0.994, 0.006],
 [0.003, 0.997],
 [0.730, 0.270],
 [0.973, 0.027]]
```

The third row’s true label is scratch warning, but the model favors normal surface. This is a case where a weak location pattern is confused with ordinary illumination variation.

| Question | Short answer |
| --- | --- |
| Why preserve this sample? | It gives more review evidence than a single accuracy value. |
| What should be checked? | Defect strength, training-data range, and spatial information. |
| What should the record contain? | Confirmed fact, model-family hypothesis, and next improvement plan. |

| Candidate family | Strength to consider first | Question raised by this failure |
| --- | --- | --- |
| CNN | Retains nearby spatial patterns | Would the faint scratch location be clearer with local spatial features? |
| Sequential model | Uses ordered accumulation | This is a two-dimensional location problem, so order is not the first hypothesis. |
| Attention family | Relates distant elements directly | Is a larger context or relation between separated regions actually needed? |

The safe conclusion is not “add a larger model.” First ask whether the weak location was missed, whether similarly weak defects were in training data, and whether the flattened representation lost the spatial relation. For this 8×8 patch, CNN is a more direct next question than a sequential model; attention becomes relevant only if wider context is supported by evidence.

```mermaid
--8<-- "assets/part-07/chapter-03/p7-3-2-model-selection-case-flow-en.mmd"
```

## Separate data, representation, and model hypotheses

| Level | Question in this practice | Follow-up model-family question |
| --- | --- | --- |
| Data | Were weak-scratch examples sufficiently represented in training? | Does the same error remain after adding comparable cases? |
| Representation | Does flattening 8×8 grayscale values preserve the weak location adequately? | Should an encoding retain local spatial neighborhoods? |
| Model family | Is a simple linear boundary too limited for shadow versus faint scratch? | Should a CNN be tested before a wider-context family? |

These are hypotheses, not established causes. A small synthetic patch set cannot prove why one sample was wrong. It can prioritize the next controlled comparison.

## Record an error as a reusable project artifact

| Record field | Why it is needed |
| --- | --- |
| Error sample ID | Lets a later experiment find the same patch. |
| Review reason | Separates low confidence, misclassification, and data-range concern. |
| Follow-up item | States whether data, representation, or structure is examined first. |
| Common retrospective sentence | Lets another project reuse the same result format. |

The relevant project inputs are [`p7-3-surface-patches.csv`](../../../assets/part-07/chapter-03/p7-3-surface-patches.csv){ .csv-preview }, [`p7-3-error-review.csv`](../../../assets/part-07/chapter-03/p7-3-error-review.csv){ .csv-preview }, and [`p7-3-followup-actions.csv`](../../../assets/part-07/chapter-03/p7-3-followup-actions.csv){ .csv-preview }. The first states what training patterns existed; the second records prediction and confidence; the third lists candidate actions.

```mermaid
--8<-- "assets/part-07/chapter-03/p7-3-2-error-review-flow-en.mmd"
```

## A safe retrospective statement

> The weak-scratch evaluation patch was classified as normal despite a scratch-warning label. The current training set is centered on clearer normal and scratch patterns; flattening the 8×8 patch may weaken the local vertical-dimming signal; and the simple classifier may not separate weak scratch from shadow variation. Add weak-scratch and shadow boundary patches first, then compare a spatial representation before claiming that a different model family is necessary.

This statement preserves the observed error, limits the causal interpretation, and names a next experiment. It avoids describing the classifier as simply “bad” or treating one incorrect patch as proof that attention or a sequential model is required.

## Review checklist for a structure decision

| Check | Question to answer |
| --- | --- |
| Error sample | Can the exact patch and its confidence margin be retrieved? |
| Data range | Does training contain a comparable weak-defect pattern? |
| Representation | Which spatial information is kept or discarded? |
| Family hypothesis | Which family directly matches the relationship to preserve? |
| Next trial | What fixed evaluation case will decide between data and structure hypotheses? |

## Checklist

| Check | Question to answer |
| --- | --- |
| Locality | Are nearby values meaningfully related? |
| Order | Would reordering inputs change the task? |
| Long range | Must distant positions interact directly? |
| Comparison | Is the evaluation set and representation fixed fairly? |
| Limit | What error remains unexplained? |

## Read the review files as separate evidence

The surface-patch file, error-review file, and follow-up-action file have different responsibilities. A review becomes unreliable when one file is treated as if it answered every question.

| File | Direct evidence | Question it cannot settle alone |
| --- | --- | --- |
| Surface patches | Training and evaluation pattern names, labels, and pixel values | Why a specific prediction was produced. |
| Error review | Actual label, predicted label, probabilities, margin, and review flag | Whether a data or model change will recover the error. |
| Follow-up actions | Candidate data, representation, and structure actions | Which action is already validated. |

For the weak scratch, the review record reports actual scratch warning, predicted normal surface, probabilities `[0.730, 0.270]`, and margin `0.459`. That is a confirmed held-out error. The next action list supplies hypotheses, not explanations already proven by the error row.

## Build a three-level error record

| Level | Bounded hypothesis | Smallest controlled trial |
| --- | --- | --- |
| Data | Weak scratches or shadow combinations may be missing from training range | Add labeled boundary patches while retaining current test cases. |
| Representation | Flattening may make the local vertical pattern less explicit | Compare a stated spatial profile with raw flattened pixels. |
| Model family | A linear boundary may be too limited after the first two checks | Test a local spatial model on the same regression set. |

The ordering matters. A CNN trial can be a useful hypothesis, but it should not hide an untested data-range gap. Likewise, a new training patch cannot prove that locality never mattered. Keep each explanation conditional and each trial narrow.

## Classify candidate actions by what they change

| Action type | Example | What remains fixed |
| --- | --- | --- |
| Data coverage | Add weak-scratch intensity examples | Current representation and regression patches. |
| Data coverage | Add shadow-with-defect combinations | Label mapping and error-review record. |
| Representation | Compare a center-band or location-aware feature | Split and classifier setting. |
| Model family | Test a locality-preserving CNN | Data version and named regression cases. |
| Needs clarification | A vague “improve preprocessing” task | Do not run until expected change is stated. |

An action that cannot be classified should remain unclassified. Assigning it to data or model work without evidence makes the retrospective harder to reproduce.

## Design a safe next trial

1. Preserve the weak scratch and shadow normal as fixed evaluation references.
2. Choose one intervention: new boundary data, a representation comparison, or a local spatial model.
3. State the expected transition before the run, such as “weak scratch changes from incorrect to correct without a shadow-normal regression.”
4. Run the intervention and list every recovered, newly wrong, and still-unresolved patch.
5. Update the hypothesis only after comparing the same reference patches.

This procedure converts an architecture discussion into an experiment. It also prevents a later accuracy improvement from hiding an expensive new false warning.

## Family selection by input relation

| Family | Input relation it assumes is useful | Evidence needed before priority |
| --- | --- | --- |
| CNN | Nearby pixels form local visual patterns | Weak or off-center defects remain after comparable data checks. |
| Sequential | Earlier and later positions form meaningful order | The input becomes a true ordered signal, not an arbitrary image scan. |
| Attention | Distant regions need direct interaction | The task requires context beyond local patches. |

For the current 8×8 patch, a faint vertical local pattern makes the CNN question more direct. A sequential family would need a documented sequence meaning, and an attention family would need evidence that distant context changes the decision. These are priorities for investigation, not a rank of model prestige.

## Example retrospective

> The weak-scratch evaluation patch was predicted normal despite a scratch-warning label. The record confirms the error and preserves the input, probability, and margin. Comparable weak patterns may be absent from the training range; flattening may make the local vertical dimming less explicit; and a local spatial model is a later question if data and representation checks do not resolve the case. The next trial will add specified weak and shadow boundary patches while keeping the weak scratch and shadow normal as regression cases. This result does not establish that any model family is universally required.

## Final reviewer questions

- Can the exact error sample be retrieved from the review CSV?
- Is an incorrect row distinguished from a correct low-margin row?
- Does the next action state whether it changes data, representation, or model structure?
- Are the weak scratch and shadow normal retained for regression testing?
- Does the selected family match a documented input relation?
- Is the conclusion limited to the current synthetic patch evidence?

## Work from a reproducible error summary

Before proposing an architecture, create a summary that separates review volume from confirmed errors.

```text
evaluation rows reviewed:
incorrect rows:
review candidates:
incorrect-and-review rows:
representative error ID:
representative error probabilities and margin:
training-pattern comparison:
candidate actions by category:
```

The following program makes that summary from the three project files. Run it from the repository root so the paths resolve. It is an error-analysis record, not a new CNN, sequential, or attention implementation.

```python
import csv
from pathlib import Path

asset_dir = Path("docs/assets/part-07/chapter-03")
surface_rows = list(csv.DictReader((asset_dir / "p7-3-surface-patches.csv").open(encoding="utf-8")))
review_rows = list(csv.DictReader((asset_dir / "p7-3-error-review.csv").open(encoding="utf-8")))
action_rows = list(csv.DictReader((asset_dir / "p7-3-followup-actions.csv").open(encoding="utf-8")))

target_id = "평가-결함-약함"
label_name = {0: "normal surface", 1: "scratch warning"}
training_patterns = {row["pattern_name"] for row in surface_rows if row["split"] == "train"}

def action_category(action):
    if any(term in action for term in ["학습 데이터", "변형 추가", "라벨", "hard negative", "평가 묶음", "조도 구간"]):
        return "data coverage"
    if any(term in action for term in ["정규화", "전처리", "촬영"]):
        return "representation"
    if "공간 구조" in action or "모델" in action:
        return "model family"
    return "needs clarification"

records = []
for row in review_rows:
    actual, predicted = int(row["true_label"]), int(row["pred_label"])
    records.append({
        "sample": row["sample"],
        "pattern": row["pattern_name"],
        "actual": actual,
        "predicted": predicted,
        "probabilities": [float(row["class_0_prob"]), float(row["class_1_prob"])],
        "margin": float(row["confidence_margin"]),
        "review_needed": row["review_needed"] == "예",
        "incorrect": actual != predicted,
    })

target = next(record for record in records if record["sample"] == target_id)
target_record = {
    "sample": target["sample"],
    "actual": label_name[target["actual"]],
    "predicted": label_name[target["predicted"]],
    "probabilities": target["probabilities"],
    "margin": target["margin"],
    "incorrect": target["incorrect"],
    "weak_defect": target["pattern"] == "약한 스크래치",
    "pattern_present_in_training": target["pattern"] in training_patterns,
}
actions = [
    {"action": row["action"], "category": action_category(row["action"]), "reason": row["reason"]}
    for row in action_rows
]
summary = {
    "evaluation_samples": len(records),
    "incorrect_samples": sum(record["incorrect"] for record in records),
    "review_candidates": sum(record["review_needed"] for record in records),
    "incorrect_and_review": sum(record["incorrect"] and record["review_needed"] for record in records),
    "follow_up_actions": len(actions),
}

print("review summary =", summary)
print("target error =", target_record)
print("first three actions =")
for action in actions[:3]:
    print(action)
```

The current files produce the following facts.

```text
review summary = {'evaluation_samples': 36, 'incorrect_samples': 14,
                  'review_candidates': 22, 'incorrect_and_review': 14,
                  'follow_up_actions': 36}
target error = {'sample': '평가-결함-약함', 'actual': 'scratch warning',
                'predicted': 'normal surface', 'probabilities': [0.73, 0.27],
                'margin': 0.459, 'incorrect': True, 'weak_defect': True,
                'pattern_present_in_training': False}
first three actions = data coverage, data coverage, model family
```

The first three actions are candidates, not verified remedies. They say to add weak-scratch cases, add shadow-plus-defect variants, and inspect a model that reads spatial structure. The record therefore makes the sequence of claims explicit: the weak scratch is an observed error; incomplete data coverage and a locality-preserving model are next hypotheses to test.

Use the same named target in every later comparison. If a trial recovers this target but creates a new shadow-normal error, retain both transitions in the project record.

The review count is not a model score. It is an inventory of evidence that tells the reviewer which rows need a decision or a follow-up experiment.

The error-review dataset can contain more review candidates than incorrect rows. A correct but low-margin case is useful preventive evidence; it should not be described as an error. Conversely, an incorrect high-margin case can be more urgent because the classifier is confidently on the wrong side of the current boundary.

### Error, review candidate, and stable reference

| Status | Meaning | How to use it next |
| --- | --- | --- |
| Incorrect | Prediction disagrees with known label | Preserve it as a required regression case. |
| Correct but review-needed | A selected signal calls for inspection | Preserve it as a preventive regression case. |
| Correct and stable | No current review condition is triggered | Keep it as a reference for unwanted regressions. |
| Uncertain label | Label guideline or source evidence is incomplete | Resolve label evidence before attributing failure to a model. |

This distinction lets a review meeting prioritize without pretending that every interesting sample is a model failure.

## Explain confidence without overinterpreting it

The class-probability difference is a score from this trained model. It is useful for sorting cases, but it is not a calibrated statement that a physical defect has a known probability of existing.

| Probability pattern | Safe reading | Unsafe reading |
| --- | --- | --- |
| `0.730 / 0.270` on weak scratch | The current classifier favors normal for this stored input | The patch is 27 percent likely to be defective in the world. |
| Near-equal probabilities | The model has little separation under this representation | The label is necessarily ambiguous. |
| High confidence, wrong label | The current model strongly favors the wrong class | The source label must be wrong. |

The weak scratch margin `0.459` is not below the small low-margin threshold used in P7-3.1, yet it is still an error. This is a useful teaching case: review criteria should always include incorrect predictions, not only low margins.

## Compare a data trial and a structure trial

The same target error can motivate different experiments. Keep their claims separate.

| Trial | Change | Fixed evidence | Question answered |
| --- | --- | --- | --- |
| Weak-data expansion | Add labeled weak and shadow boundary patches | Current flattening and error references | Does data coverage recover the weak scratch? |
| Spatial-profile comparison | Replace 64 raw values with a stated spatial summary | Same split and simple classifier | Is a compact spatial relation sufficient? |
| CNN comparison | Use a locality-preserving model | Data version and regression cases | Does an explicit local pattern representation change the error? |
| Wider-context comparison | Add context only if task requires it | Local patch references | Do distant regions actually change the decision? |

If several trials are run, do not compare their scores as if they were one experiment. Each must state its changed component, stable reference cases, and newly wrong cases.

### Data additions need negative evidence too

Adding only positive weak-scratch examples can make a small experiment look easier without teaching it to reject similar normal variation. For every weak-scratch family, consider a nearby normal or shadow family. The goal is not to manufacture a high score; it is to define the boundary the model must learn.

| Added group | Label | Why include it |
| --- | ---: | --- |
| Faint central scratch | 1 | Covers the primary missed pattern. |
| Faint off-center scratch | 1 | Tests position dependence. |
| Shadow normal | 0 | Prevents darkening from becoming a shortcut. |
| Shadow plus scratch | 1 | Tests combined nuisance and defect conditions. |

Record the source and labeling rationale of every new group. Without that provenance, a later recovery cannot be distinguished from a changed task definition.

## Model-family questions by project type

The three families are not alternatives for every input. Use a project question to decide whether a family should be opened.

| Project input | First relation question | Family question that may follow |
| --- | --- | --- |
| Small surface patch | Are local neighboring pixels a meaningful pattern? | CNN or another locality-preserving view. |
| Sensor event over time | Does early versus late order change the label? | Sequential model or temporal feature representation. |
| Multiple distant regions or documents | Must separated elements be compared directly? | Attention-family context relation. |
| Customer table | Do feature combinations, not order or locality, determine the output? | Start with tabular representation before architecture family. |

This table avoids using an image failure as a pretext for an unrelated model family. It also makes it possible to state why a sequential or attention trial is deferred rather than rejected forever.

## A review note for each candidate family

Use the same template for every family so the comparison stays fair.

```text
candidate family:
input relation it is intended to preserve:
error sample motivating the trial:
data range already checked:
representation already checked:
training and evaluation cases held fixed:
expected recovery:
new regression to watch:
computational or data-cost limit:
result and next question:
```

A template cannot choose the right family. It makes a later choice explainable and keeps an appealing architecture label from substituting for evidence.

## Keep a regression set across iterations

The regression set should include more than the one weak scratch. It can include a stable normal, clear scratch, shadow normal, weak scratch, and any newly wrong patch. Use the same labels and original source representations unless the experiment explicitly tests a representation transformation.

| Regression case | Purpose |
| --- | --- |
| Stable normal | Detect new false warnings on ordinary surfaces. |
| Clear scratch | Verify that obvious defect detection is not lost. |
| Weak scratch | Target the original missed boundary. |
| Shadow normal | Detect a darkening shortcut. |
| New error from a trial | Prevent an aggregate gain from hiding a repeatable regression. |

An improved aggregate score that damages a regression case should be reported as a trade-off. The next action may be to revise data, representation, or operating threshold; it is not automatically to accept the change.

## Closing error-analysis practice

Write two statements after the next trial:

1. A fact-only statement listing fixed cases and their before/after transitions.
2. A limited interpretation stating which data, representation, or family hypothesis became more or less plausible.

Then write one next question. For example: “The weak scratch recovered after adding weak and shadow boundary patches, while the shadow normal remained correct. This supports a data-coverage hypothesis for this fixed set; it does not establish that a CNN is unnecessary. Next, compare the same expanded data using a locality-preserving representation.”

This format keeps the chapter’s purpose clear: use error evidence to select the next comparison, not to announce a final architecture winner.

## Final handoff

Keep the weak scratch and shadow normal as named references.
State whether the next trial changes data, representation, or model family.
Preserve the same evaluation split and the same review fields.
Report recoveries, new errors, and unresolved cases separately.
Limit each conclusion to the current synthetic patch evidence.
Use architecture names only after the input relation is documented.
Treat an unclassified action as a question, not as a result.
Keep the comparison reproducible for the next reviewer.

## Sources and references

The comparisons are explanatory practice material for this book.
