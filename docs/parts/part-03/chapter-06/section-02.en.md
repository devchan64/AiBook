# P3-6.2 What Intermediate Representations Can We Add When Features Alone Are Not Enough

> Section ID: `P3-6.2`
> Version: `v2026.07.24`

Features such as averages, slopes, and variability are good starting points. But in some cases, a few numbers alone are not enough to describe the segment-level structure fully. Suppose there is a pattern that rises slowly in the early phase, stays flat in the middle phase, and then drops quickly in the late phase. If that structure is left as only two or three numbers, it can feel insufficient both when a person reads it again and when a model compares it. So in Part 3, [intermediate representation](/AiBook/reference/concept-glossary/#glossary-intermediate-representation) is read together as a human-led input re-expression that remains between raw logs and summary features so the structure can stay more visible.

This section does not repeat feature design itself again. Instead, it focuses on how far we can go in adding intermediate representations such as segment expressions and tokenization when numerical features from the previous section alone do not preserve enough structure.

This is where segment expressions and tokenized expressions appear. The core idea is simple. Instead of staring at the long raw curve as it is, we divide the whole thing into a few ranges and convert the direction and strength of each range into short symbols or short summary values.

| Segment | Numerical summary | Example of symbolic summary |
| --- | --- | --- |
| Early phase | Average rate of rise is positive | `UP` |
| Middle phase | Average change is almost zero | `FLAT` |
| Late phase | Rate of decline is large | `DOWN` |

If we divide the raw curve into segments as in the graph below, tokenization becomes visible not as simply naming things, but as `turning the curve's direction and strength into shorter reading units`.

![Graph that divides a raw curve into five segments and turns them into the tokens UP2, UP1, FLAT, DOWN1, and DOWN2](/AiBook/assets/part-03/chapter-06/segment-tokenization-curve-en.png)

Once this is done, a long curve shrinks into a short sequence such as `UP, FLAT, DOWN`. This expression is easy for people to read, and it also lets a model receive the structure of the curve as an input with more regular length. In other words, a segment expression is the act of converting a complex time series into `an intermediate representation that people and models can both look at`.

This representation can also be read in three levels. At the simplest level, it leaves only direction, such as `UP`, `DOWN`, `FLAT`. At a slightly finer level, it also leaves intensity, such as `UP1`, `UP2`, `DOWN3`. Going further, we can also inspect how many times each symbol repeated and in which ranges it stayed for long. Seen this way, tokenization is not a simple substitution. It is a way of rewriting the same raw curve at several resolutions.

| Representation level | What remains | What is easy to lose | When it is useful |
| --- | --- | --- | --- |
| Keep only direction | Rise, fall, flatness | Differences in the magnitude of change | When a very fast comparison is needed |
| Direction + intensity | Strength of rise or fall | Fine-grained fluctuation shape | When we want more explainable features |
| Include repetition length | Duration of the same pattern | Fine changes in the original time spacing | When we want to inspect repetition and state shifts |

This table shows that tokenization becomes easier to read the more strongly it compresses, but at the same time it also loses more. So which level to use is not a matter of technical taste. It is part of the problem definition. The level of representation that should remain can differ depending on whether we want a report that an operator can scan quickly or a structure that may later be reused as model input.

If we split once more the question `why do we need this representation`, the role of segment expressions between the summary table and the raw log becomes clearer.

| What we already have | Why we convert more | What becomes visible right after conversion |
| --- | --- | --- |
| A few segment averages | We want to see order and direction in a shorter way | A pattern like `UP, FLAT, DOWN` |
| One overall average | We want to reveal structural differences that the average hides | Same average, different shape |
| The full raw log | We need an intermediate representation a person can compare quickly | The outline of repeating structures |

The code below reads a segment-slope CSV and changes the token boundaries in two settings, showing how the same raw slopes can turn into different token sequences.

Problem situation: check what becomes easier to see when continuous numerical slopes are converted into a short symbol sequence.

Input: the segment-slope CSV by action, [p3_6_2_segment_slopes.csv](/AiBook/assets/part-03/chapter-06/p3_6_2_segment_slopes.csv), and the token-boundary candidates `token_settings`

Expected output: output where each action's slope list is turned into a token sequence such as `UP2`, `UP1`, `FLAT`, `DOWN1`, `DOWN2`. If the boundaries change, the number of segments left as `FLAT`, the number of strong rise/fall tokens, and the list of changed actions also change.

Concept to check: tokenization does not leave the raw structure as-is. It turns sequence and direction into an easier-to-read intermediate representation. Token boundaries are not fixed answers; they are design values that should be checked against the problem.

```python
# This example adds an intermediate representation between raw logs and final features to trace calculation evidence.
import csv
from collections import defaultdict
from pathlib import Path

data_path = Path("docs/assets/part-03/chapter-06/p3_6_2_segment_slopes.csv")
token_settings = {
    "sensitive": {"strong_threshold": 0.80, "weak_threshold": 0.20},
    "conservative": {"strong_threshold": 0.90, "weak_threshold": 0.30},
}


def slope_to_token(slope: float, strong_threshold: float, weak_threshold: float) -> str:
    if slope >= strong_threshold:
        return "UP2"
    if slope >= weak_threshold:
        return "UP1"
    if slope <= -strong_threshold:
        return "DOWN2"
    if slope <= -weak_threshold:
        return "DOWN1"
    return "FLAT"


rows = list(csv.DictReader(data_path.open(encoding="utf-8")))
for row in rows:
    row["segment_order"] = int(row["segment_order"])
    row["slope"] = float(row["slope"])

events = defaultdict(list)
for row in rows:
    events[row["event_id"]].append(row)

reports = {}
for setting_name, thresholds in token_settings.items():
    event_reports = []
    token_counts = defaultdict(int)
    for event_id, event_rows in sorted(events.items()):
        ordered_rows = sorted(event_rows, key=lambda row: row["segment_order"])
        slopes = [row["slope"] for row in ordered_rows]
        tokens = [
            slope_to_token(
                slope,
                thresholds["strong_threshold"],
                thresholds["weak_threshold"],
            )
            for slope in slopes
        ]
        for token in tokens:
            token_counts[token] += 1
        event_reports.append(
            {
                "event_id": event_id,
                "slopes": slopes,
                "tokens": tokens,
            }
        )
    reports[setting_name] = {
        "thresholds": thresholds,
        "events": event_reports,
        "token_counts": dict(sorted(token_counts.items())),
    }

sensitive_tokens = {
    report["event_id"]: report["tokens"]
    for report in reports["sensitive"]["events"]
}
changed_events = []
for report in reports["conservative"]["events"]:
    event_id = report["event_id"]
    if report["tokens"] != sensitive_tokens[event_id]:
        changed_events.append(event_id)

print("1) input rows:", len(rows))
print("2) event count:", len(events))
for setting_name, report in reports.items():
    print(f"[{setting_name}] thresholds =", report["thresholds"])
    print("token_counts =", report["token_counts"])
    for event in report["events"][:3]:
        print(event)
    print()
print("3) events changed when thresholds become conservative:", changed_events)
```

Expected output:

```text
1) input rows: 40
2) event count: 8
[sensitive] thresholds = {'strong_threshold': 0.8, 'weak_threshold': 0.2}
token_counts = {'DOWN1': 9, 'DOWN2': 3, 'FLAT': 15, 'UP1': 9, 'UP2': 4}
{'event_id': 'A', 'slopes': [0.92, 0.31, 0.05, -0.42, -1.0], 'tokens': ['UP2', 'UP1', 'FLAT', 'DOWN1', 'DOWN2']}
{'event_id': 'B', 'slopes': [0.62, 0.24, 0.01, -0.22, -0.74], 'tokens': ['UP1', 'UP1', 'FLAT', 'DOWN1', 'DOWN1']}
{'event_id': 'C', 'slopes': [0.18, 0.12, 0.04, -0.1, -0.18], 'tokens': ['FLAT', 'FLAT', 'FLAT', 'FLAT', 'FLAT']}

[conservative] thresholds = {'strong_threshold': 0.9, 'weak_threshold': 0.3}
token_counts = {'DOWN1': 7, 'DOWN2': 1, 'FLAT': 23, 'UP1': 7, 'UP2': 2}
{'event_id': 'A', 'slopes': [0.92, 0.31, 0.05, -0.42, -1.0], 'tokens': ['UP2', 'UP1', 'FLAT', 'DOWN1', 'DOWN2']}
{'event_id': 'B', 'slopes': [0.62, 0.24, 0.01, -0.22, -0.74], 'tokens': ['UP1', 'FLAT', 'FLAT', 'FLAT', 'DOWN1']}
{'event_id': 'C', 'slopes': [0.18, 0.12, 0.04, -0.1, -0.18], 'tokens': ['FLAT', 'FLAT', 'FLAT', 'FLAT', 'FLAT']}

3) events changed when thresholds become conservative: ['B', 'D', 'E', 'F', 'H']
```

The key point to watch in this output is not only the moment when continuous numbers turn into a short symbol sequence, but also which actions actually change interpretation when the boundaries change. The values to manipulate here are `strong_threshold` and `weak_threshold` inside `token_settings`. In the conservative setting, more small changes remain `FLAT`, and the token sequences change for actions near the boundary, such as `B`, `D`, `E`, `F`, and `H`. By contrast, an action like `A`, where the strong rise and strong fall are clear, keeps its main structure even when the setting changes.

When several actions are viewed together, it becomes clearer that a token rule is not a simple label but a design judgment. People can now read the structure quickly as `rise, gentle rise, almost flat, decline, large decline`, but they can also re-check which threshold folded which segment into `FLAT`.

If this example is checked in the following order, the role of tokenization becomes clearer.

1. Check into which token each slope was converted.
2. Think about whether the token boundaries are too coarse or too dense.
3. Write how a person would read this token sequence in one sentence.

For example, `['UP2', 'UP1', 'FLAT', 'DOWN1', 'DOWN2']` can be summarized as `the early rise is strong, the middle flattens for a while, and the late decline becomes larger`.

It is also important that the token sequence can differ even when the average is the same. For example, even if the average flow of two actions is 2.5 in both cases, one may be `UP, FLAT, DOWN` while the other is `FLAT, FLAT, FLAT`. They look similar if we inspect only the average, but the token sequence reveals that one had structural change while the other remained stable. Because of this, tokenization is not mere decoration. It is a representation that complements structure missed by average-based summaries.

We can also check this difference with a small vectorization example. The code below compares a ranking based only on the numerical average with a ranking that vectorizes the token sequence using `TfidfVectorizer` and sorts candidates by similarity to a query.

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

patterns = pd.DataFrame(
    [
        {"event_id": "A", "overall_mean": 2.5, "token_sequence": "UP2 UP1 FLAT DOWN1 DOWN2"},
        {"event_id": "B", "overall_mean": 2.5, "token_sequence": "FLAT FLAT FLAT FLAT FLAT"},
        {"event_id": "C", "overall_mean": 2.4, "token_sequence": "UP1 UP1 FLAT DOWN1 DOWN1"},
        {"event_id": "D", "overall_mean": 2.8, "token_sequence": "DOWN2 DOWN1 FLAT UP1 UP2"},
    ]
)

query_mean = 2.5
query_text = "UP2 UP1 FLAT DOWN1 DOWN2"

patterns["mean_distance"] = (patterns["overall_mean"] - query_mean).abs()
mean_rank = patterns.sort_values(["mean_distance", "event_id"])[
    ["event_id", "overall_mean", "mean_distance"]
]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
matrix = vectorizer.fit_transform(patterns["token_sequence"])
query_vector = vectorizer.transform([query_text])
patterns["token_similarity"] = cosine_similarity(query_vector, matrix)[0]
token_rank = patterns.sort_values(["token_similarity", "event_id"], ascending=[False, True])[
    ["event_id", "token_sequence", "token_similarity"]
]

print("rank by numeric mean")
print(mean_rank.to_string(index=False))
print()
print("rank by token sequence")
print(token_rank.to_string(index=False))
```

The output looks like this.

```text
rank by numeric mean
event_id  overall_mean  mean_distance
       A           2.5            0.0
       B           2.5            0.0
       C           2.4            0.1
       D           2.8            0.3

rank by token sequence
event_id           token_sequence  token_similarity
       A UP2 UP1 FLAT DOWN1 DOWN2          1.000000
       C UP1 UP1 FLAT DOWN1 DOWN1          0.511833
       D DOWN2 DOWN1 FLAT UP1 UP2          0.392319
       B FLAT FLAT FLAT FLAT FLAT          0.120765
```

If we inspect only the numerical average, `A` and `B` are equally close candidates. But `B` is actually flat in every segment and does not have the same rise-flat-decline structure as the query. When the token sequences are vectorized, `A` becomes the closest candidate, and `C`, which shares part of the rise and decline structure, moves next. The point is not that `TfidfVectorizer` is the correct answer. The point is that once human-defined segment tokens are turned into real library input, we can compare order and direction differences that average-based summaries erased.

This matters because segment tokens are still human-defined expressions, yet they already have the property of being `a sequence with order`. So they can preserve structure more directly when numerical features alone might miss it, and they also let us carry the same input structure forward naturally when sequential data or representation learning is explained later.

But this clearly has limits too. The moment we convert a curve into symbols, information loss appears, and the choice of where to place the boundaries for `UP`, `DOWN`, and `FLAT` also reflects the designer's judgment. In other words, tokenization is not universal. It is a compression that gains explainability while throwing away some detail.

So it is safer to understand this expression not as something that replaces the raw log, but as an `intermediate representation` placed between the raw log and the summary table. The raw log has the most information, the summary table is advantageous for comparison, and the tokenized expression makes structure more visible in the middle. Once we understand this relationship, it also becomes clearer `why some problems need more than an average` and `why some problems do not require us to inspect the entire raw log every time`.

So when reading a tokenized representation, we should always carry two questions together. `What becomes easier to see because of this representation?` and `What was lost by turning it into this representation?` Only with this sense of balance do we stop seeing a token sequence as a mysterious code and start reading it as an intermediate representation built for a purpose.

The same judgment can be summarized more briefly like this.

| What we need right now | The more direct representation |
| --- | --- |
| Numerical comparison and simple model input | Numerical features |
| Fast reading of segment order and direction | Segment expressions |
| Comparing structure as a short symbol sequence | Tokenized expressions |

So numerical features and intermediate representations are not in competition. They are tools separated according to what we want to make more visible.

This section can be read not as an introduction to one particular token rule, but as the problem of `what intermediate representation should be placed between raw structure and summarized features`.

## A Small Diagram

The core of this section is that we do not immediately discard the raw curve or close it too quickly into a few numbers. Once the curve is segmented and turned through numerical summaries into a token sequence, one more layer appears: the `intermediate representation`.

--8<-- "assets/part-03/chapter-06/p3-6-2-mermaid-01-en.mmd"


So tokenization is more accurately read not as an isolated technique, but as a choice about `at what resolution the structure should remain` between leaving the raw log as it is and summarizing it too strongly.

## Sources and Further Reading

- TensorFlow, `Subword tokenizers`. Because it explains subword tokenizers as a representation between word-based tokenization and character-based tokenization, it can help explain the generalized view that Part 3's segment tokens also sit as an intermediate representation between raw logs and strong summaries. The part that connects this directly to time-series tokenization is an analogical application based on the official explanation. [https://www.tensorflow.org/text/guide/subwords_tokenizer](https://www.tensorflow.org/text/guide/subwords_tokenizer){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `feature engineering`. Because it explains feature engineering as the process of deciding transformations helpful for model training, it supports the point that intermediate representations are also transformations that do not leave raw values untouched but convert them into forms helpful for comparison and learning. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
