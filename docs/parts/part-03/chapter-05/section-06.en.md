# P3-5.6 Why Can the Number of Samples Look Larger than Reality When Many Input Windows Overlap

> Section ID: `P3-5.6`
> Version: `v2026.07.17`

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

Input: a source-event table where event length and `window`, `stride` are given

Expected output: output showing how many windows each event expands into and how much larger the `window` count becomes than the `source_event` count

Concept to check: the number of input windows is only the number of derived pieces and should not be read in the same unit as the number of source events

```python
import pandas as pd

events = pd.DataFrame(
    [
        {"event_id": "A", "length": 100, "window": 30, "stride": 10},
        {"event_id": "B", "length": 100, "window": 30, "stride": 10},
    ]
)

events["window_count"] = ((events["length"] - events["window"]) // events["stride"]) + 1
events["source_event_weight"] = 1

print("1) how many windows each source event creates")
print(events[["event_id", "length", "window", "stride", "window_count"]])
print()
print("2) source-event count vs window count")
print(
    pd.DataFrame(
        [
            {"unit": "source_event", "count": events["source_event_weight"].sum()},
            {"unit": "window", "count": events["window_count"].sum()},
        ]
    )
)
print()
print("3) expansion per source event")
print(events[["event_id", "window_count"]])
```

Expected output:

```text
1) how many windows each source event creates
  event_id  length  window  stride  window_count
0        A     100      30      10             8
1        B     100      30      10             8

2) source-event count vs window count
          unit  count
0  source_event      2
1        window     16

3) expansion per source event
  event_id  window_count
0        A             8
1        B             8
```

The purpose of this example is less to calculate the number of windows than to check `how much larger the window count can make the real number of events look`. So in stage 1, we look at how many windows one event expands into. In stage 2, we count `source_event` and `window` separately. In stage 3, we check again the degree of expansion for each event. The important point here is that `overlapping input windows can be the result of cutting the same event several times, so the number of windows should not immediately be read like the number of events`.

## A Small Diagram

The core of this section is to separate `the window count grew` from `the number of source events increased`. If many overlapping windows are created from the same two events, the number of input pieces grows, but the event count itself stays the same.

--8<-- "assets/part-03/chapter-05/p3-5-6-mermaid-01-en.mmd"

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example assumes the unit where features and labels attach, it supports the judgment in this section that the mere creation of many input windows does not automatically mean the number of source events itself has increased. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because the provenance framework says we should be able to trace which derivation created which entity, it provides the higher-level frame that each input window should remain separated by which source event it came from, so that window count and event count do not get confused. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Google for Developers, `Datasets: Dividing the original dataset`. Because it provides the general perspective that training examples should be distinguished from the source data and the rules that created them, it helps generalize the explanation in this section that even when many windows overlap, source-event units and input-piece units should still be written separately. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
