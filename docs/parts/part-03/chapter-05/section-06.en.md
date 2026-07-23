# P3-5.6 Overlapping Input Windows and Sample Counts

> Section ID: `P3-5.6`
> Version: `v2026.07.23`

_Subtitle: Why can sample counts look larger than reality when the same event is cut into multiple windows?_

Once the input window has been fixed, we can create several windows from the same source time series. At that point, one problem is often missed. It becomes easy to read `there are more windows, so there must also be more samples`. But when many windows overlap, this often means `we are cutting the same event several times`, not that the number of independent events has increased by the same amount.

The number of input windows and the number of source events may not be the same.

| Distinction | Meaning |
| --- | --- |
| Number of source events | The number of actual full actions or actual events |
| Number of input windows | The number of learning-input pieces cut from those events |

For example, if we cut one action with length 30 and stride 10, one event can expand into several inputs.

| event_id | Source length | Window length | stride | Number of windows created |
| --- | ---: | ---: | ---: | ---: |
| A | 100 | 30 | 10 | 8 |
| B | 100 | 30 | 10 | 8 |

If we look at this table and say only `there are 16 samples`, that is only half correct. The real number of events is 2, while the number of input windows is 16. So in a comparison report or a judgment about representativeness, the fact that there were still only `2 events` should be written together.

The more overlapping windows there are, the more easily the following problems appear.

| Problem that appears | Why caution is needed |
| --- | --- |
| The sample count looks larger | The evidence can look exaggerated compared with the actual number of events |
| Similar windows repeat | The pattern of one event can appear several times, weakening independence |
| Recent events are cut more often | The influence of a specific event can become too large in the table |

At this stage, we do not need to cover complicated evaluation design. Still, it is safer to leave behind the following notes.

| Note to write down first | Why it is needed |
| --- | --- |
| Number of source events | So the actual evidence unit does not get hidden |
| Number of input windows | So model-input scale can be viewed separately |
| Window length and stride | So the rule by which the windows grew can be explained again |

The small example below makes the point clearer.

Problem situation: check what illusion appears if the number of windows and the number of source events are read as the same number when many input windows overlap.

Input: the source-event table [p3_5_6_source_events.csv](/AiBook/assets/part-03/chapter-05/p3_5_6_source_events.csv) and the movement interval to test, `stride_to_try`. Each row in this table is one source event, with an event length (`length`) and window length (`window`).

Expected output: output showing how many windows each event expands into and how much larger the `window` count becomes than the `source_event` count. If `stride_to_try` changes, the window count and expansion ratio also change.

Concept to check: the number of input windows is only the number of derived pieces and should not be read in the same unit as the number of source events

```python
# This example checks whether overlapping input windows inflate the sample count by counting the same event repeatedly.
import csv
from collections import defaultdict
from pathlib import Path

stride_to_try = 10
preview_event_count = 8
source_events_path = Path("docs/assets/part-03/chapter-05/p3_5_6_source_events.csv")

with source_events_path.open(newline="", encoding="utf-8") as file:
    events = []
    for row in csv.DictReader(file):
        length = int(row["length"])
        window = int(row["window"])
        window_count = ((length - window) // stride_to_try) + 1
        events.append(
            {
                "event_id": row["event_id"],
                "line_id": row["line_id"],
                "mode": row["mode"],
                "length": length,
                "window": window,
                "stride": stride_to_try,
                "window_count": window_count,
                "source_event_weight": 1,
            }
        )


def print_event_preview(rows):
    print("event_id line_id     mode  length  window  stride  window_count")
    for row in rows:
        print(
            f"{row['event_id']:>8} {row['line_id']:>7} {row['mode']:>8} "
            f"{row['length']:>7} {row['window']:>7} {row['stride']:>7} "
            f"{row['window_count']:>13}"
        )


def print_expansion_preview(rows):
    print("event_id  window_count")
    for row in rows:
        print(f"{row['event_id']:>8} {row['window_count']:>13}")

print("1) how many windows each source event creates")
print_event_preview(events[:preview_event_count])
print(f"... {len(events) - preview_event_count} more source events")
print()
print("2) source-event count vs window count")
print("          unit  count")
print(f"0  {'source_event':<12} {sum(row['source_event_weight'] for row in events):>5}")
print(f"1  {'window':>12} {sum(row['window_count'] for row in events):>5}")
print()
print("3) expansion per source event")
print_expansion_preview(events[:preview_event_count])
print(f"... {len(events) - preview_event_count} more source events")
print()
print("4) expansion summary by line and mode")
groups = defaultdict(lambda: {"source_event_count": 0, "window_count": 0})
for row in events:
    group = groups[(row["line_id"], row["mode"])]
    group["source_event_count"] += row["source_event_weight"]
    group["window_count"] += row["window_count"]

print("line_id     mode  source_event_count  window_count  mean_windows_per_event")
for line_id, mode in sorted(groups):
    group = groups[(line_id, mode)]
    mean_windows = group["window_count"] / group["source_event_count"]
    print(
        f"{line_id:>7} {mode:>8} {group['source_event_count']:>19} "
        f"{group['window_count']:>13} {mean_windows:>23.2f}"
    )
print()
print("5) expansion ratio")
print(round(sum(row["window_count"] for row in events) / len(events), 2))
```

Expected output:

```text
1) how many windows each source event creates
event_id line_id     mode  length  window  stride  window_count
     E01      L1 baseline     100      30      10             8
     E02      L1 baseline      96      30      10             7
     E03      L1 baseline      92      30      10             7
     E04      L1 baseline      88      30      10             6
     E05      L1 baseline      84      30      10             6
     E06      L1 baseline      80      30      10             6
     E07      L1   recent     110      30      10             9
     E08      L1   recent     104      30      10             8
... 28 more source events

2) source-event count vs window count
          unit  count
0  source_event    36
1        window   237

3) expansion per source event
event_id  window_count
     E01             8
     E02             7
     E03             7
     E04             6
     E05             6
     E06             6
     E07             9
     E08             8
... 28 more source events

4) expansion summary by line and mode
line_id     mode  source_event_count  window_count  mean_windows_per_event
     L1 baseline                   6            40                    6.67
     L1   recent                   6            42                    7.00
     L2 baseline                   6            40                    6.67
     L2   recent                   6            43                    7.17
     L3 baseline                   6            34                    5.67
     L3   recent                   6            38                    6.33

5) expansion ratio
6.58
```

The purpose of this example is less to calculate the number of windows than to check `how much larger the window count can make the real number of events look`. The value to manipulate here is `stride_to_try`. If `10` is changed to `20`, the window count and expansion ratio fall. If it is changed to a smaller value, more input pieces are created from the same source events. But the number of `source_event` rows remains 36. So overlapping input windows can be the result of cutting the same event several times, and the number of windows should not immediately be read like the number of events. If we group again by line and operating mode as in stage 4, each condition still has 6 source events, but the derived window count grows differently depending on the event length and window setting.

## A Small Diagram

The core of this section is to separate `the window count grew` from `the number of source events increased`. If many overlapping windows are created from the same two events, the number of input pieces grows, but the event count itself stays the same.

--8<-- "assets/part-03/chapter-05/p3-5-6-mermaid-01-en.mmd"

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example assumes the unit where features and labels attach, it supports the judgment in this section that the mere creation of many input windows does not automatically mean the number of source events itself has increased. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because the provenance framework says we should be able to trace which derivation created which entity, it provides the higher-level frame that each input window should remain separated by which source event it came from, so that window count and event count do not get confused. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Datasets: Dividing the original dataset`. Because it provides the general perspective that training examples should be distinguished from the source data and the rules that created them, it helps generalize the explanation in this section that even when many windows overlap, source-event units and input-piece units should still be written separately. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- scikit-learn developers, `Cross-validation: evaluating estimator performance`. Because it explains that dependent samples from the same source process can break the independent-and-identically-distributed assumption, and that grouped data should avoid placing samples from the same group in both training and validation folds, it reinforces this section's caution that overlapping input windows may be dependent pieces derived from the same event rather than new real events. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
