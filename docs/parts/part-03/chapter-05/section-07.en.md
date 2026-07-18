# P3-5.7 How Should We Fold Multiple Follow-Up Events After the Same Sample into a Table Structure

> Section ID: `P3-5.7`
> Version: `v2026.07.17`

Even after the sample unit and the input window are fixed, one more point often blocks the table structure. It is the case where several follow-up events attach after the same sample. For example, after one action, we may record `review`, `warning`, `failure`, and `revisit` in sequence. If we do not decide how to fold them into one result column, the same sample can easily change meaning from table to table.

If there are several follow-up events, we should first write down by what rule they were folded into one table structure.

Common folding rules look like this.

| Folding rule | Meaning |
| --- | --- |
| `any` | If at least one occurred, write 1 |
| `first` | Keep the earliest follow-up event as the representative |
| `worst` | Keep the most severe state as the representative |
| `count` | Keep the number of occurrences itself |

For example, suppose the following follow-up events remained after the same samples.

| event_id | follow_up_events |
| --- | --- |
| A | review, failure |
| B | review |
| C | none |

Depending on how we fold this into a table, the meaning of the result column changes.

| event_id | any_failure | first_event | event_count |
| --- | ---: | --- | ---: |
| A | 1 | review | 2 |
| B | 0 | review | 1 |
| C | 0 | none | 0 |

So even when we are looking at the same source event, the table structure changes according to `what we choose as the representative result`. This is a data-modeling problem in which we must first decide by what rule the representative result will be folded and left in the table.

Leaving the notes below first reduces later confusion.

| Note to write down first | Why it is needed |
| --- | --- |
| Which follow-up events are treated as one bundle | To fix the result range handled by the table |
| Which of `any`, `first`, `worst`, `count` was used | To explain again what the result column means |
| Whether the folded result is for reporting or a prediction candidate | To avoid mixing comparison reports with target candidates |

Small example:

Problem situation: check that when several follow-up events exist after the same sample, different folding rules such as `first`, `worst`, `count`, and `any` create different result columns.

Input: a follow-up-event list by sample and a severity order among events

Expected output: output showing that even for the same source event, `first_event`, `worst_event`, `event_count`, and `any_failure` are created differently

Concept to check: when folding several follow-up events into one result column, we should first specify by what rule they were folded, so the meaning of the table structure does not drift

```python
import pandas as pd

follow_ups = {
    "A": ["review", "failure"],
    "B": ["review"],
    "C": [],
}

severity = {"none": 0, "review": 1, "warning": 2, "failure": 3}
rows = []
for event_id, events in follow_ups.items():
    first_event = events[0] if events else "none"
    worst_event = max(events, key=lambda name: severity[name]) if events else "none"
    rows.append(
        {
            "event_id": event_id,
            "any_failure": int("failure" in events),
            "first_event": first_event,
            "worst_event": worst_event,
            "event_count": len(events),
        }
    )

result = pd.DataFrame(rows)
print(result)
```

Expected output:

```text
  event_id  any_failure first_event worst_event  event_count
0        A            1      review     failure            2
1        B            0      review      review            1
2        C            0        none        none            0
```

The key point in this example is that even while looking at the same source event, different result columns can be created at the same time: for example, `first_event` becomes `review`, `worst_event` becomes `failure`, and `event_count` becomes 2. So if the folding rule is not written down, the same sample `A` can be read with a different meaning from one table to another. If several follow-up events exist after the same sample, we should first write down by what rule they were folded into one result column, so the meaning of the table structure does not shake.

## A Small Diagram

This section compresses one point: `several follow-up events` do not automatically become one result column. The same event list turns into different representative result columns depending on whether it is folded by `any`, `first`, `worst`, or `count`.

--8<-- "assets/part-03/chapter-05/p3-5-7-mermaid-01-en.mmd"

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `label` and `labeled example`. Because result information first has to be fixed to a given example, it supports the judgment in this section that when several follow-up events are folded into one result column, we should first specify which rule among `any`, `first`, `worst`, and `count` was used. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Google for Developers, `Machine Learning Glossary`: `label leakage`. Because it shows that result columns with unclear construction rules are easy to confuse with prediction candidates, it reinforces the explanation that the folding rule should be written first to fix the meaning of the table structure. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because it explains that a provenance framework should leave derivation and activity context traceable, it provides the higher-level frame that we should also be able to trace by what rule several follow-up events were folded into one representative result column. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
