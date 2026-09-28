# P3-4.5 How Well Does the Sample Set We Collected Represent the Overall Operating Situation

> Section ID: `P3-4.5`
> Version: `v2026.09.19`

Even when each sample correctly represents one action, whether the collection covers its intended operating environment remains a separate question. **Representativeness concerns how the target distribution and collection process are reflected in the data, rather than equal counts across conditions.** Total sample count, minimum counts, and model accuracy provide different information.

## Read Operating Shares Alongside Collection Shares {#a-small-diagram}

The [fictional action CSV](/AiBook/assets/part-03/chapter-04/p3_4_5_sample_coverage.csv) contains 36 actions, E01–E36. Each row is one action: `shift` is day/night, `load_mode` is load condition, `machine_id` identifies equipment, and `maintenance_phase` distinguishes stable operation from after-maintenance. This is our teaching case for coverage and evaluation, not actual operating statistics.

**Assume** the target operation is 80% day and 20% night. These are separately specified target shares, not values inferred from the CSV.

| shift | Assumed operating share | Collected actions | Collected share |
| --- | ---: | ---: | ---: |
| day | 80% | 26 | 26/36 ≈ 72.2% |
| night | 20% | 10 | 10/36 ≈ 27.8% |

More daytime records do not alone establish bias. Under this assumption, night’s collected share is about 7.8 percentage points above its target share. Nor does a share difference in this small table establish a pass or fail for representativeness. Check how records were selected and which periods, machines, and conditions were omitted.

You might deliberately collect more night records to assess night performance separately. That can help condition-specific evaluation, but the changed collection shares must not be reported as overall operating shares. The CSV has no collection timestamps, so these columns cannot establish seasonal or period coverage.

## What the Nine-Record Rule Actually Counts

Set `minimum_count = 9` as an illustrative inspection rule and mark conditions with **fewer than nine actions**. Nine is neither a standard sufficient sample size nor a threshold that certifies representativeness.

| Grouping column | Actions by condition | Observed condition types | Conditions below nine |
| --- | --- | ---: | --- |
| shift | day 26, night 10 | 2 | None: 0 |
| load_mode | normal 25, high 6, low 5 | 3 | high, low: 2 |
| machine_id | M1 22, M2 7, M3 7 | 3 | M2, M3: 2 |
| maintenance_phase | stable 28, after-maintenance 8 | 2 | after-maintenance: 1 |

The number below the minimum for `shift` is zero because both `26 < 9` and `10 < 9` are false. “Both conditions exceed the rule” does not mean “the target operation is represented.” Counts of condition types such as 2 or 3 are also neither action counts nor correct predictions.

Raising the minimum to 10 still does not flag the ten night actions; raising it to 11 does. Lowering it to 5 leaves zero under-minimum conditions in all four columns above. This changes the display rule without adding observations.

## Search Separately for Zero Counts and Combinations

The table counts only values present in the CSV. If the target scope separately includes M4, add M4 with **zero records**. Do not invent a missing machine without establishing that it belongs to the target scope. This is why the target-condition list must be compared with observed values.

Individual conditions may all be present while a combination is empty. The following table counts machine and load together, selecting only `night` actions from the same CSV.

| Night actions | normal | high | low |
| --- | ---: | ---: | ---: |
| M1 | 3 | 1 | 0 |
| M2 | 1 | 0 | 1 |
| M3 | 2 | 1 | 1 |

The full dataset has ten night actions, seven M2 actions, and six high-load actions, but **night + M2 + high has zero records**. Record a gap if this combination can occur and is in evaluation scope. An impossible combination is not a collection target. Equal counts for every possible combination are not the goal.

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-5-mermaid-01-en.mmd"
```

## Read Model Scores with Condition-Specific Denominators {#small-code-example}

Run a model on the same CSV, creating `needs_review` with the fictional rule **1 for `high` load or `after-maintenance`, otherwise 0**. Because this exercise label is made from input conditions, it does not measure real fault prediction. It tests how a model reproduces a known rule from its training data.

Fix E01–E24 as training and E25–E36 as evaluation. These are ID ranges, not assumed chronological ranges. Counts by load are:

| load_mode | Training actions | Evaluation actions |
| --- | ---: | ---: |
| high | 4 | 2 |
| low | 0 | 5 |
| normal | 20 | 5 |
| Total | 24 | 12 |

`dummy` always predicts the more common training label, 0. `tree` is a decision tree that branches on input conditions. `OneHotEncoder` converts categories into 0/1 columns; for an unseen category it sets that feature’s encoded columns to zero. Being able to execute a prediction does not mean that condition was learned.

Run the code from the repository root. Change input columns through `features` and inspect the total correct count alongside `test_events` and `errors` for each load. Category transformation and model fitting use only training data.

```python
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

samples = pd.read_csv("docs/assets/part-03/chapter-04/p3_4_5_sample_coverage.csv")
samples["needs_review"] = (
    samples["load_mode"].eq("high")
    | samples["maintenance_phase"].eq("after-maintenance")
).astype(int)
train = samples[samples["event_id"].between("E01", "E24")]
test = samples[samples["event_id"].between("E25", "E36")]
# Change input columns and inspect errors together with evaluation counts.
features = ["shift", "load_mode", "machine_id", "maintenance_phase"]
models = {
    "dummy": DummyClassifier(strategy="most_frequent"),
    "tree": DecisionTreeClassifier(random_state=0, max_depth=3),
}
results = {}
for name, estimator in models.items():
    model = make_pipeline(OneHotEncoder(handle_unknown="ignore"), estimator)
    model.fit(train[features], train["needs_review"])
    result = test[["event_id", "load_mode", "needs_review"]].copy()
    result["prediction"] = model.predict(test[features])
    result["error"] = result["prediction"].ne(result["needs_review"])
    correct = int((~result["error"]).sum())
    print(f"{name}: correct={correct}/{len(result)}, accuracy={correct / len(result):.3f}")
    print(result.groupby("load_mode").agg(
        test_events=("error", "size"), errors=("error", "sum")
    ).to_string())
    results[name] = result
```

```text
dummy: correct=5/12, accuracy=0.417
           test_events  errors
load_mode
high                 2       2
low                  5       2
normal               5       3
tree: correct=9/12, accuracy=0.750
           test_events  errors
load_mode
high                 2       0
low                  5       3
normal               5       0
```

The baseline gets five of twelve actions right: `5/12 ≈ 41.7%`. The tree gets nine right: `9/12 = 75%`. All three tree errors are in `low`, whose accuracy is `(5−3)/5 = 2/5 = 40%`. High is 2/2 and normal is 5/5, but these are results on a small evaluation set, not guarantees of future performance.

The low-load errors in this run are E27, E28, and E29. All are `stable`, so their synthetic target is 0, but the model predicts 1. Note that training contained no `low` examples, without generalizing that unseen conditions always fail or are the only cause of errors. Results also depend on input representation and learned branches.

Try `features = ["load_mode"]` to remove maintenance information. Tree accuracy becomes `6/12 = 50%`; errors by load are high 0/2, low 3/5, and normal 3/5. The input no longer distinguishes the labels of after-maintenance normal-load actions E25, E26, and E34. Coverage and available input information both affect results. After using these evaluation scores to choose inputs, avoid reusing the same set as final performance verification.

## Record the Supported Scope and Remaining Gaps

Correct “Minimum counts passed and accuracy is 75%, so the data is sufficient for all operations.” One answer is: “Day and night exceed the illustrative nine-record rule, but target shares, collection methods, and additional conditions need checking. This synthetic-rule experiment gets nine of twelve actions right; low load, absent from training, gets two of five right. Night + M2 + high and collection-period coverage remain unsupported.”

For actual data, record collection periods and methods, target conditions, important zero-count or sparse combinations, and where to collect more or defer application. Neither total count nor one accuracy score replaces that record.

## Checklist

- Do you distinguish assumed target shares of 80/20 from observed shares of 26/36 and 10/36?
- Have you calculated why shift has zero under-minimum conditions at nine?
- Can you explain why lowering the rule removes warnings without adding data?
- Have you checked zero-count target conditions and intersections such as night + M2 + high?
- Do you read overall 9/12 alongside low-load 2/5 and state the synthetic label’s limits?
- Have you recorded what this CSV cannot establish, such as observation-period coverage?

## Sources and Further Reading

- Google for Developers, [Deep Learning Tuning Playbook: Additional guidance](https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook/additional-guidance){: target="_blank" rel="noopener noreferrer" }. Supports evaluation on data representative of production. The 80/20 shares and nine-record rule are assumptions for this example. / Accessed: 2026-09-19
- scikit-learn developers, [OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html){: target="_blank" rel="noopener noreferrer" }. Documents categorical encoding and unseen-category handling with `handle_unknown="ignore"`. / Accessed: 2026-09-19
