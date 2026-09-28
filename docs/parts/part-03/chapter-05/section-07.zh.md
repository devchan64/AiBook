# P3-5.7 折叠多个后续事件的规则

> Section ID: `P3-5.7`
> Version: `v2026.09.19`

_副标题: 同一个样本之后的多个事件应该按什么规则折叠进一个表结构？_

即使[样本(sample)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)单位和输入窗口都已经定好了，表结构里仍然常常会再卡住一个地方：同一个样本之后挂着多个后续事件。比如，一次动作之后，可能依次留下 `review`、`warning`、`failure`、`revisit`。如果不先决定要怎样把它们折叠成一个结果列，同一个样本在不同表里就很容易变成不同含义。

如果后续事件有多个，就应该先写清：它们是按什么[折叠规则(folding rule)](/AiBook/zh/reference/concept-glossary-pinyin/d/#data-modeling)被折叠进同一个表结构里的。

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

也就是说，即使面对的是同一个[源事件(source event)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-source-data)，只要 `代表结果到底选什么` 的规则不同，表结构就会不同。这个问题本质上是一个数据建模问题：要先决定用什么规则把代表结果折叠进表里。

先留下下面这些备注，后面的混乱会少很多。

| 先写下来的备注 | 为什么需要 |
| --- | --- |
| 哪些后续事件被看成同一组 | 为了固定这张表所处理的结果范围 |
| 使用了 `any`、`first`、`worst`、`count` 里的哪一种 | 为了重新解释结果列到底是什么意思 |
| 折叠出来的结果是用于报告，还是预测候选 | 为了避免把比较报告和目标标签候选(target candidate)混在一起 |

最终表中也要让折叠规则可追踪。例如留下 `folding_rule`、`severity_cutoff`、`follow_up_window_days`、`source_event_count`、`target_candidate_name` 作为 备注，就能再次说明 `any_selected_event=1` 是在哪个事件范围和阈值下得到的。即使来自同一个后续事件日志，`first_event` 和 `worst_event` 也是不同列，不能只看一个列名就把它固定成实际目标标签。

汇总后续事件之前，还要定义观察期间和去重规则。如果目标是`7 天内是否失败`，第 9 天的失败不应计入。如果传输重试使同一事件存储了两次，就要核对事件标识，避免 `count` 重复计数。`first` 应按发生时间排序确定，并预先规定同时发生或严重程度相同的事件如何排序。

下面的示例假定样本清单中的所有样本都已完成追踪，后续事件日志已限定在分析期间内，而且没有重复记录。只有在这些假设下，才能给没有事件的 S30 标记 0。仍在观察中的样本，即使尚未发生事件，也必须保留为 `pending`。

小例子：

问题情境：确认当同一个样本之后存在多个后续事件时，`first`、`worst`、`count`、`any` 这些不同规则会生成不同的结果列。

输入(input)：样本名册 [p3_5_7_sample_roster.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_sample_roster.csv){ .csv-preview }、后续事件日志 [p3_5_7_follow_up_events.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv){ .csv-preview }、事件严重程度表 [p3_5_7_event_severity.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_event_severity.csv){ .csv-preview }，以及要比较的严重程度阈值候选 `severity_cutoffs`

第一个 CSV 中的一行，是最终结果表里必须保留的一个样本。第二个 CSV 中的一行，是样本之后实际发生过的一个后续事件。第三个 CSV 把事件名称转换成严重程度数字，用来计算 `worst` 和 `any_selected_event` 规则。

期望输出(output)：即使是同一个源事件，`first_event`、`worst_event`、`event_count`、`event_sequence`、`any_failure`、`any_selected_event` 也会被生成成不同结果。改变 `severity_cutoffs` 时，所选样本数和样本列表也会改变。

要确认的概念：当多个后续事件被折叠成一个结果列时，必须先写明折叠规则和[阈值(threshold)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-threshold)，否则表结构的含义会漂移

## 手动汇总 S01、S02 和 S30

以下 CSV 是为本例设计的虚构数据。观测期为样本之后第 1～7 天，包含两端，并假设名单中的 36 个样本都已完成追踪。`days_after_sample` 是天数位置，不是精确发生时刻。CSV 没有追踪完成标记，也没有单个后续事件的 ID，因此仅凭这些文件无法验证追踪完成或没有重复记录。

| sample_id | 观测期内记录 | first_event | worst_event | event_count | any_failure |
| --- | --- | --- | --- | ---: | ---: |
| S01 | 第 1 天 review → 第 3 天 warning → 第 5 天 failure | review | failure | 3 | 1 |
| S02 | 第 2 天 review → 第 4 天 warning | review | warning | 2 | 0 |
| S30 | 无，假设追踪完成 | none | none | 0 | 0 |

`any_failure` 表示是否存在事件类型为 `failure` 或 `critical_failure` 的记录。这是本例的类型映射，不随严重程度阈值改变。`count` 统计观测期内所有后续事件，而非仅统计失败。`first` 会隐藏后来的失败，`worst` 会隐藏之前警告与复查的顺序；需要顺序时应保留 `event_sequence`。

严重程度是本例设定的顺序等级。review=2、warning=3、failure=4 只规定排序，并不表示失败比复查严重两倍。`any_selected_event` 回答的是**是否存在达到所选严重程度阈值的事件**，与 `any_failure` 不同。S02 在阈值 4 时为 0，阈值 3 时为 1，但仍没有失败记录。

例子仅纳入第 1～7 天，`first` 按天数排序。同一天的记录按 CSV 行顺序处理，不能据此断定实际发生先后。`worst` 依次按严重程度降序、天数升序、原始行顺序选择。实际运行中应取得更精确的发生时刻与事件 ID，再制定并列与去重规则。

```python
# 这个例子把同一样本之后的多个后续事件折叠进表结构，并确定代表标签。
import csv
from collections import defaultdict
from pathlib import Path

sample_roster_path = Path("docs/assets/part-03/chapter-05/p3_5_7_sample_roster.csv")
follow_up_events_path = Path("docs/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv")
event_severity_path = Path("docs/assets/part-03/chapter-05/p3_5_7_event_severity.csv")

selected_severity_cutoff = 4
severity_cutoffs = [4, 3, 2]
follow_up_window_days = 7
failure_types = {"failure", "critical_failure"}
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

period_events = [row for row in follow_ups if 1 <= row["days_after_sample"] <= follow_up_window_days]
ordered_events = sorted(period_events, key=lambda row: (row["sample_id"], row["days_after_sample"]))
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
            "any_failure": int(any(row["event_type"] in failure_types for row in events)),
            "any_selected_event": int(any(row["severity"] >= selected_severity_cutoff for row in events)),
        }
    )

cutoff_results = []
for cutoff in severity_cutoffs:
    selected = [row for row in folded if row["event_count"] > 0 and row["worst_severity"] >= cutoff]
    cutoff_results.append(
        {
            "severity_cutoff": cutoff,
            "selected_sample_count": len(selected),
            "selected_samples": ",".join(row["sample_id"] for row in selected) or "none",
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
print(f"3) folded result when severity_cutoff = {selected_severity_cutoff}")
print(
    "sample_id      first_event      worst_event  worst_severity  event_count"
    "             event_sequence  any_failure  any_selected_event"
)
for row in folded[:preview_row_count]:
    print(
        f"{row['sample_id']:>9} {row['first_event']:>16} {row['worst_event']:>16} "
        f"{row['worst_severity']:>15} {row['event_count']:>12} "
        f"{row['event_sequence']:>26} {row['any_failure']:>12} {row['any_selected_event']:>19}"
    )
print(f"... {len(folded) - preview_row_count} more folded samples")
print()
print("4) sensitivity by severity_cutoff")
print(
    " severity_cutoff  selected_sample_count"
    "                                                                     selected_samples"
)
for row in cutoff_results:
    print(
        f"{row['severity_cutoff']:>24} {row['selected_sample_count']:>21} "
        f"{row['selected_samples']:>83}"
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

3) folded result when severity_cutoff = 4
sample_id      first_event      worst_event  worst_severity  event_count             event_sequence  any_failure  any_selected_event
      S01           review          failure               4            3 review > warning > failure            1                   1
      S02           review          warning               3            2           review > warning            0                   0
      S03          revisit          revisit               1            1                    revisit            0                   0
      S04          warning          warning               3            1                    warning            0                   0
      S05          revisit           review               2            2           revisit > review            0                   0
      S06 minor_adjustment minor_adjustment               1            1           minor_adjustment            0                   0
      S07          warning          failure               4            2          warning > failure            1                   1
      S08           review           review               2            1                     review            0                   0
      S09          revisit          revisit               1            1                    revisit            0                   0
      S10          warning          warning               3            1                    warning            0                   0
      S11       inspection       inspection               2            1                 inspection            0                   0
      S12           review          warning               3            2           review > warning            0                   0
... 24 more folded samples

4) sensitivity by severity_cutoff
 severity_cutoff  selected_sample_count                                                                     selected_samples
                       4                     5                                                                 S01,S07,S13,S19,S25
                       3                    12                                     S01,S02,S04,S07,S10,S12,S13,S16,S19,S22,S25,S28
                       2                    21 S01,S02,S04,S05,S07,S08,S10,S11,S12,S13,S16,S17,S18,S19,S21,S22,S24,S25,S26,S28,S29
```

所选样本数在阈值 4 时为 5，阈值 3 时为 12，阈值 2 时为 21。把 4 降为 3，新纳入的是 **S02、S04、S10、S12、S16、S22、S28**，共 7 个最严重记录为 warning 的样本。这不是产生了新的失败，而是扩大了选择范围。有失败类型记录的样本数仍为 5。

运行前先预测把 `selected_severity_cutoff` 改为 3 时，S02 的两个标记会怎样变化。答案是 `any_selected_event=1`、`any_failure=0`。再假设 S01 的 failure 发生在第 9 天而非第 5 天，七天内结果就变为 first=review、worst=warning、count=2、any_failure=0。该事件落在观测期外，不代表它从原始历史中被删除。

如果 S30 尚未完成追踪，就不能把结果确定为 none 和 0。这段代码假设虚构名单已完成追踪；真实的未完成资料需要增加完成状态，并单独处理为 `pending`。也不能把这些未来结果混入样本时点的预测输入。结果列是否作为[监督学习标签](/AiBook/zh/reference/concept-glossary-pinyin/j/#supervised-learning-label)，应在确定预测时点与目标之后判断。


## 将多个后续事件汇总为样本级结果 {#_1}

这一节压缩的是一点：`多个后续事件` 并不会自动变成同一个结果列。同一组事件，按 `any`、`first`、`worst`、`count` 里的不同规则折叠后，会得到不同的代表结果列。

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-7-mermaid-01-zh.mmd"
```

## 检查清单

- 能否说明 S02 的阈值从 4 降为 3 是改变选择范围，而不是产生失败？

- 你是否写明了后续事件的观察期间、去重和代表标签选择规则？
- 你是否区分了后续事件为 0 条与观察未完成？

## 来源与参考资料

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary#label){: target="_blank" rel="noopener noreferrer" }. 参考 label 与 labeled example 的定义。any/first/worst/count、严重程度等级与失败类型映射均为本例自行设计。 / 2026-09-19
- W3C, [PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }. 提供追踪数据生成与派生过程的一般依据，并不直接规定本节的汇总规则。 / 2026-09-19
