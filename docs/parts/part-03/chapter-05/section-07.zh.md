# P3-5.7 折叠多个后续事件的规则

> Section ID: `P3-5.7`
> Version: `v2026.07.23`

_副标题: 同一个样本之后的多个事件应该按什么规则折叠进一个表结构？_

即使样本单位和输入窗口都已经定好了，表结构里仍然常常会再卡住一个地方：同一个样本之后挂着多个后续事件。比如，一次动作之后，可能依次留下 `review`、`warning`、`failure`、`revisit`。如果不先决定要怎样把它们折叠成一个结果列，同一个样本在不同表里就很容易变成不同含义。

如果后续事件有多个，就应该先写清：它们是按什么规则被折叠进同一个表结构里的。

常见的折叠规则有下面这些。

| 折叠规则 | 含义 |
| --- | --- |
| `any` | 只要发生过一次，就记为 1 |
| `first` | 把最早出现的后续事件作为代表 |
| `worst` | 把最严重的状态作为代表 |
| `count` | 直接保留发生次数 |

例如，假设同一个样本之后，留下了下面这样的后续事件。

| event_id | follow_up_events |
| --- | --- |
| A | review, failure |
| B | review |
| C | none |

把它折叠成什么样的表，会直接改变结果列的含义。

| event_id | any_failure | first_event | event_count |
| --- | ---: | --- | ---: |
| A | 1 | review | 2 |
| B | 0 | review | 1 |
| C | 0 | none | 0 |

也就是说，即使面对的是同一个源事件，只要 `代表结果到底选什么` 的规则不同，表结构就会不同。这个问题本质上是一个数据建模问题：要先决定用什么规则把代表结果折叠进表里。

先留下下面这些备注，后面的混乱会少很多。

| 先写下来的备注 | 为什么需要 |
| --- | --- |
| 哪些后续事件被看成同一组 | 为了固定这张表所处理的结果范围 |
| 使用了 `any`、`first`、`worst`、`count` 里的哪一种 | 为了重新解释结果列到底是什么意思 |
| 折叠出来的结果是用于报告，还是预测候选 | 为了避免把比较报告和目标候选混在一起 |

小例子：

问题情境：确认当同一个样本之后存在多个后续事件时，`first`、`worst`、`count`、`any` 这些不同规则会生成不同的结果列。

输入(input)：样本名册 [p3_5_7_sample_roster.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_sample_roster.csv)、后续事件日志 [p3_5_7_follow_up_events.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv)、事件严重程度表 [p3_5_7_event_severity.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_event_severity.csv)，以及要作为失败标准候选的严重程度阈值 `failure_severity_cutoffs`

第一个 CSV 中的一行，是最终结果表里必须保留的一个样本。第二个 CSV 中的一行，是样本之后实际发生过的一个后续事件。第三个 CSV 把事件名称转换成严重程度数字，用来计算 `worst` 和 `any_failure` 规则。

期望输出(output)：即使是同一个源事件，`first_event`、`worst_event`、`event_count`、`event_sequence`、`any_failure` 也会被生成成不同结果。改变 `failure_severity_cutoffs` 时，失败候选样本数和样本列表也会改变。

要确认的概念：当多个后续事件被折叠成一个结果列时，必须先写明折叠规则，否则表结构的含义会漂移

```python
# 这个例子把同一样本之后的多个后续事件折叠进表结构，并确定代表标签。
import csv
from collections import defaultdict
from pathlib import Path

sample_roster_path = Path("docs/assets/part-03/chapter-05/p3_5_7_sample_roster.csv")
follow_up_events_path = Path("docs/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv")
event_severity_path = Path("docs/assets/part-03/chapter-05/p3_5_7_event_severity.csv")

selected_failure_severity_cutoff = 4
failure_severity_cutoffs = [4, 3, 2]
preview_row_count = 12


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


sample_roster = read_csv(sample_roster_path)
follow_ups = read_csv(follow_up_events_path)
severity_table = read_csv(event_severity_path)
severity_by_type = {row["event_type"]: int(row["severity"]) for row in severity_table}

for row in follow_ups:
    row["days_after_sample"] = int(row["days_after_sample"])
    row["severity"] = severity_by_type[row["event_type"]]

ordered_events = sorted(follow_ups, key=lambda row: (row["sample_id"], row["days_after_sample"]))
events_by_sample = defaultdict(list)
for row in ordered_events:
    events_by_sample[row["sample_id"]].append(row)

folded = []
for sample in sample_roster:
    sample_id = sample["sample_id"]
    events = events_by_sample.get(sample_id, [])
    if events:
        first_event = events[0]["event_type"]
        worst = sorted(events, key=lambda row: (-row["severity"], row["days_after_sample"]))[0]
        worst_event = worst["event_type"]
        worst_severity = worst["severity"]
        event_sequence = " > ".join(row["event_type"] for row in events)
    else:
        first_event = "none"
        worst_event = "none"
        worst_severity = 0
        event_sequence = "none"
    folded.append(
        {
            "sample_id": sample_id,
            "first_event": first_event,
            "worst_event": worst_event,
            "worst_severity": worst_severity,
            "event_count": len(events),
            "event_sequence": event_sequence,
            "any_failure": int(worst_severity >= selected_failure_severity_cutoff),
        }
    )

cutoff_results = []
for cutoff in failure_severity_cutoffs:
    failed = [row for row in folded if row["worst_severity"] >= cutoff]
    cutoff_results.append(
        {
            "failure_severity_cutoff": cutoff,
            "failure_sample_count": len(failed),
            "failure_samples": ",".join(row["sample_id"] for row in failed) or "none",
        }
    )

print("1) raw follow-up events")
print("sample_id  days_after_sample       event_type source_system")
for row in follow_ups[:preview_row_count]:
    print(
        f"{row['sample_id']:>9} {row['days_after_sample']:>18} "
        f"{row['event_type']:>16} {row['source_system']:>13}"
    )
print(f"... {len(follow_ups) - preview_row_count} more follow-up events")
print()
print("2) severity rule table")
print("      event_type  severity")
for row in severity_table[:preview_row_count]:
    print(f"{row['event_type']:>16} {int(row['severity']):>9}")
print(f"... {len(severity_table) - preview_row_count} more severity rules")
print()
print("3) folded result when failure_severity_cutoff = 4")
print(
    "sample_id      first_event      worst_event  worst_severity  event_count"
    "             event_sequence  any_failure"
)
for row in folded[:preview_row_count]:
    print(
        f"{row['sample_id']:>9} {row['first_event']:>16} {row['worst_event']:>16} "
        f"{row['worst_severity']:>15} {row['event_count']:>12} "
        f"{row['event_sequence']:>26} {row['any_failure']:>12}"
    )
print(f"... {len(folded) - preview_row_count} more folded samples")
print()
print("4) sensitivity by failure_severity_cutoff")
print(
    " failure_severity_cutoff  failure_sample_count"
    "                                                                     failure_samples"
)
for row in cutoff_results:
    print(
        f"{row['failure_severity_cutoff']:>24} {row['failure_sample_count']:>21} "
        f"{row['failure_samples']:>83}"
    )
```

期望输出：

```text
1) raw follow-up events
sample_id  days_after_sample       event_type source_system
      S01                  1           review   human_queue
      S01                  3          warning       monitor
      S01                  5          failure   maintenance
      S02                  2           review   human_queue
      S02                  4          warning       monitor
      S03                  1          revisit       service
      S04                  1          warning       monitor
      S05                  1          revisit       service
      S05                  2           review   human_queue
      S06                  3 minor_adjustment      operator
      S07                  1          warning       monitor
      S07                  6          failure   maintenance
... 24 more follow-up events

2) severity rule table
      event_type  severity
            none         0
         revisit         1
minor_adjustment         1
      inspection         2
          review         2
         warning         3
         failure         4
critical_failure         5
    sensor_noise         0
   operator_note         1
     calibration         1
   slow_recovery         2
... 24 more severity rules

3) folded result when failure_severity_cutoff = 4
sample_id      first_event      worst_event  worst_severity  event_count             event_sequence  any_failure
      S01           review          failure               4            3 review > warning > failure            1
      S02           review          warning               3            2           review > warning            0
      S03          revisit          revisit               1            1                    revisit            0
      S04          warning          warning               3            1                    warning            0
      S05          revisit           review               2            2           revisit > review            0
      S06 minor_adjustment minor_adjustment               1            1           minor_adjustment            0
      S07          warning          failure               4            2          warning > failure            1
      S08           review           review               2            1                     review            0
      S09          revisit          revisit               1            1                    revisit            0
      S10          warning          warning               3            1                    warning            0
      S11       inspection       inspection               2            1                 inspection            0
      S12           review          warning               3            2           review > warning            0
... 24 more folded samples

4) sensitivity by failure_severity_cutoff
 failure_severity_cutoff  failure_sample_count                                                                     failure_samples
                       4                     5                                                                 S01,S07,S13,S19,S25
                       3                    12                                     S01,S02,S04,S07,S10,S12,S13,S16,S19,S22,S25,S28
                       2                    21 S01,S02,S04,S05,S07,S08,S10,S11,S12,S13,S16,S17,S18,S19,S21,S22,S24,S25,S26,S28,S29
```

这个例子的关键在于：即使看的是同一个源事件，`first_event`、`worst_event`、`event_count`、`event_sequence`、`any_failure` 也可能被生成成不同的结果列。S01 的第一个后续事件是 `review`，但最严重的事件是 `failure`；S02 的第一个事件是 `review`，但最严重的事件是 `warning`。像 S30 这样没有后续事件的样本，也仍然在样本名册里，所以会被折叠成 `none` 和 0，并保留在最终表中。这里可以操作的值是 `selected_failure_severity_cutoff` 和 `failure_severity_cutoffs`。阈值为 4 时，只有带有 `failure` 的 S01、S07、S13、S19、S25 成为失败候选；如果阈值降到 3，最严重事件为 `warning` 的样本也会进入失败候选；如果降到 2，最严重事件为 `review` 或 `inspection` 的样本也会被包括进来。也就是说，如果不写清折叠规则和阈值，同一份后续事件日志在不同表里就会被读成不同含义。

## 用一个小图来看

这一节压缩的是一点：`多个后续事件` 并不会自动变成同一个结果列。同一组事件，按 `any`、`first`、`worst`、`count` 里的不同规则折叠后，会得到不同的代表结果列。

--8<-- "assets/part-03/chapter-05/p3-5-7-mermaid-01-zh.mmd"

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `label` 与 `labeled example`。因为结果信息必须先被固定到某个 example 上，所以它支持这一节的判断：当多个后续事件被折叠进一个结果列时，必须先说明使用的是 `any`、`first`、`worst`、`count` 中的哪一种规则。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `label leakage`。因为它说明构造规则不清晰的结果列，很容易和预测候选混淆，所以它强化了“先写清折叠规则，才能固定表结构含义”这一点。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. provenance framework 说明派生关系和活动上下文应当可追踪，因此它提供了一个更高层的框架：多个后续事件究竟按什么规则被折叠成一个代表结果列，也应该是可追踪的。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
