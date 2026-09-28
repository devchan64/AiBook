# P3-2.3 第一次拿到新表时，应该先写下什么

> Section ID: `P3-2.3`
> Version: `v2026.09.19`

第一次拿到一张新表时，很多人很容易立刻想到均值、分布、模型候选。但在这之前更应该先写下来的，是 `这张表的一行表示什么`、`什么能被归到一起`、`还有什么仍然缺着`。只有把这三点先整理出来，才能分清：现在手上的，到底已经是可以直接比较的样本表，还是仍然需要重新归组的原始记录。与其一看到新表就先决定它是不是 `训练数据集`，不如先把这三点写下来，这对解释会更有帮助。这样一来，后面的样本设计和数据集重设计也会少很多抽象感。

这里首先要抓住的视角，是[格式一致性(format consistency)](/AiBook/zh/reference/concept-glossary-pinyin/d/#data-modeling)和第一次[数据质量检查](/AiBook/zh/reference/concept-glossary-pinyin/d/#data-modeling)。格式一致性，指的是先检查指向同一个对象的键是不是用同样的格式写的，时间列是不是能真正读出顺序，同样意义的值有没有因为单位或字符串规则不同而混在一起。第一次质量检查，是再往后一步：提早检查那些会立刻破坏比较结构的问题有没有出现，比如缺失值、顺序断裂、重复行，或是无法顺利归组的孤立行。

第一次读一张新表时，先写下 `一行是什么`、`什么能归组`、`还有什么缺着` 会更安全。`一行是什么` 这个问题，对应的是统计和数据整理里对 `observation` 单位的确认；`什么能归组`，对应的是时间数据里应该先把 `key` 和 `index` 显露出来的原则；至于保留 `原始证据` 的项目，也连到同一条原则：只有 data provenance 和 traceability 保留着，后面才能重新判断质量和可信度。

如果把同样那份五行备忘录，再按格式与质量的视角重读一次，就可以整理成下面这样。

| 检查视角 | 先确认什么 | 为什么要尽早抓住 |
| --- | --- | --- |
| 格式一致性 | 键格式是否一致、时间列是否可排序、单位和记法是否混杂 | 因为如果把同一个对象读成不同对象，或把时间顺序读错，后面所有比较都会跟着晃动 |
| 第一次质量检查 | 有没有缺失、重复、顺序断裂、无法归组的行 | 因为在重构样本之前，就要先把已经无法比较的案例单独标出来 |

## 最先写下的五件事

第一次读一张新表时，先写下下面这五个问题会更稳妥。它们是避免漏掉 `行单位`、`归组标准`、`时间结构`、`可比较性`、`原始证据` 的最小检查项。

1. 一行表示什么？
2. 把同一个对象归在一起的标识符是什么？
3. 有没有表示时间顺序或流程顺序的列？
4. 现在这个单位能不能直接比较，还是还得先重新归组？
5. 如果有东西看起来奇怪，应该回到什么原始证据去看？

把这五点压成表，就是下面这样。

| 先写下的项目 | 为什么需要它 |
| --- | --- |
| 行的含义 | 因为必须先区分它是时间点记录、一次完整动作，还是近期区段聚合 |
| 标识符 | 因为必须知道多行是否属于同一条样本 |
| 时间/顺序列 | 因为必须判断它是时间序列结构还是静态表 |
| [可比较性](/AiBook/zh/reference/concept-glossary-pinyin/k/#glossary-comparability) | 因为必须决定样本能不能直接比，还是要先做摘要表 |
| 原始证据位置 | 因为奇怪案例以后还得能追溯回去 |

只要先把这五项写下来，读表时就会少很多把存储结构和问题表达结构混在一起的情况。

这五项的阅读顺序也很重要。`行的含义`、`标识符`、`时间/顺序列` 属于先检查格式一致性的那一轴；`可比较性` 和 `原始证据位置` 属于转向第一次质量检查的那一轴。这样写下来之后，我们就能按顺序分清楚：到底是 `格式先不对`，还是 `格式没问题，但质量问题仍然让比较无法成立`，而不只是含糊地说一句 `质量看起来不好`。

## 错误的起步和更好的起步

| 一看到表就容易做的事 | 为什么太早了 | 更好的第一步 |
| --- | --- | --- |
| 先去算均值和最大值 | 一行和一条样本可能还不是一回事 | 先写下行的含义和标识符 |
| 先想到分类或回归 | 将来承接标签的单位可能还没显现 | 先看它是不是直接可比较的单位 |
| 先想到时序深度学习 | 就算有时间列，样本边界也可能还没定 | 先看时间/顺序列和归组标准 |
| 对某一条奇怪的值立刻赋义 | 那一行不一定能代表整个样本 | 把原始证据和候选摘要结构一起记下 |

也就是说，第一阶段更接近 `确认身份`，而不是 `开始计算`。

## 从行含义到可比性的检查 {#_3}

第一次读一张新表时，更安全的顺序是：`确认行的含义 -> 确认归组标准 -> 检查格式/质量 -> 判断应重组还是核对原始记录`。

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-3-mermaid-01-zh.mmd"
```

## 非常短的读表备忘录

如果先写下下面五行，就能很快分清这张表的身份和可比较性。

- 一行表示 `_____`。
- 把同一个对象归在一起的键是 `_____`。
- 表示时间或流程顺序的列是 `_____`。
- 比较问题是 `_____`，所需的重组及尚未确认的条件是 `_____`。
- 回头核对奇怪案例的原始证据是 `_____`。

例如，要用下面的 CSV 比较各次动作的平均流量，可以这样写。

- 一行表示 `动作中的某一个时点测量值`。
- 把同一个对象归在一起的键是 `event_id`。
- 时间列是 `elapsed_seconds`。
- 比较动作均值需要按 `event_id` 归组；是否完整观测动作、运行条件是否一致，尚未确认。
- 回头核对奇怪案例的原始证据，是按 `event_id` 保存的原始日志。

一旦有了这五行备忘录，Chapter 3 里那句 `按问题重设计数据集`，读起来也会少很多抽象感。

再往前走一步，还可以把格式一致性和第一次质量检查分开写。

- 格式一致性：先看 `event_id` 是否能用一致格式把同一个动作归在一起，`elapsed_seconds` 是否真能读出时间顺序。
- 第一次质量检查：检查有没有某些 `event_id` 的行数异常地多或少，时间是否倒退或缺段，以及在比较前是否已有需要单独标记的缺失值。

## 顺序错误与需要核对原始记录的情况

下面复制并修改后文 CSV 中 A 的前三条记录作对照。原始 `(时间, 流量)` 为 `(0, 0.80), (1, 0.92), (2, 1.05)`，单位分别为秒和 L/min。假定这个小区段每秒采样一次。原始 CSV 保持不变。

| 对副本的改动 | 发生了什么变化 | 下一步行动 |
| --- | --- | --- |
| 不改：0→1→2 秒 | 顺序和间隔符合本区段的假设 | 继续检查其他质量项目 |
| 仅把行顺序倒为 2→1→0 秒 | 时刻与测量值不变，只改变存储顺序 | 确认时间含义后，对副本排序 |
| 再追加一条完全相同的 1 秒记录 | 同一事件、时刻和测量值重复 | 核对是否重复采集，再决定处理规则 |
| 追加一条流量改为 9.00 的 1 秒记录 | 同一事件、时刻出现 0.92 与 9.00 两个冲突值 | 暂缓该事件的汇总，核对原始记录 |
| 删除 1 秒记录：0→2 秒 | 时间递增，但预期间隔中出现空缺 | 核对是否漏记，不随意填入 0 |

`event_id` 重复是把同一事件的多个时点记录归组所必需的。这里怀疑重复的依据是 `(event_id, elapsed_seconds)` 组合重复。如果实际日志包含多个传感器，应先确认键中是否还需要传感器标识。排序只改变顺序，不能选出正确的冲突值，也不能恢复缺失的测量值。

原始证据备忘录应保留文件路径、版本或采集时间、原始行号和事件标识。派生表的处理历史应记录哪些行被排序、排除或暂缓处理，以及原因。例如，A 的 1 秒流量出现冲突时，应同时核对原始 CSV 的数据行 2（含表头的文件行 3）与新增冲突行。保留原始文件，才能对照处理前后的记录。

## 分别检查行数、时间顺序与重复记录 {#_5}

问题情境：第一次拿到一张新日志表时，检查它能不能直接被读成样本比较表。

输入(input)：保存在 [p3_2_3_first_table_log.csv](/AiBook/assets/part-03/chapter-02/p3_2_3_first_table_log.csv) 里的原始日志表，以及用于观测点数量条件的最少行数 `minimum_rows_per_event`

期望输出(output)：确认哪些事件通过行数条件，再通过改变同一组三条记录的顺序、重复情况、数值或缺失情况，区分应排序还是核对原始记录。

要确认的概念：一行不一定是一个事件。通过行数条件并不证明完整观测了动作或具备可比性；即使时间有序，也要单独检查重复、缺口和条件差异。

```python
# 检查行数条件与时间顺序，再比较副本中重复、冲突和缺失情况的下一步行动。
import csv
from collections import defaultdict
from pathlib import Path

minimum_rows_per_event = 12
preview_row_count = 8

input_path = Path("docs/assets/part-03/chapter-02/p3_2_3_first_table_log.csv")

with input_path.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

for row in rows:
    row["elapsed_seconds"] = int(row["elapsed_seconds"])
    row["flow"] = float(row["flow"])
    row["pressure"] = float(row["pressure"])

events = defaultdict(list)
for row in rows:
    events[row["event_id"]].append(row)

print("1) quick structural check")
print(f"row_count: {len(rows)}")
print(f"event_id_count: {len(events)}")
has_time_order = all(
    all(a["elapsed_seconds"] < b["elapsed_seconds"]
        for a, b in zip(event_rows, event_rows[1:]))
    for event_rows in events.values()
)
print(f"has_time_order: {'yes' if has_time_order else 'no'}")
print()

print("2) repeated rows per event")
for event_id, event_rows in sorted(events.items()):
    enough_rows = len(event_rows) >= minimum_rows_per_event
    print(f"{event_id}: row_count={len(event_rows)}, enough_rows={enough_rows}")
print()

print("3) if we compare rows as if each row were a sample")
for row in rows[:preview_row_count]:
    print(
        f"{row['event_id']} at {row['elapsed_seconds']}s: "
        f"flow={row['flow']:.1f}"
    )
print(f"... {len(rows) - preview_row_count} more time-point rows")
print()

print("4) after regrouping into one row per event")
for event_id, event_rows in sorted(events.items()):
    times = [row["elapsed_seconds"] for row in event_rows]
    observed_span = max(times) - min(times)
    mean_flow = sum(row["flow"] for row in event_rows) / len(event_rows)
    peak_pressure = max(row["pressure"] for row in event_rows)
    enough_rows = len(event_rows) >= minimum_rows_per_event
    print(
        f"{event_id}: observed_span={observed_span}s, mean_flow={mean_flow:.2f}, "
        f"peak_pressure={peak_pressure:.1f}, enough_rows={enough_rows}"
    )

print()
print("5) controlled changes to A's first three records")
base_records = [dict(row) for row in events["A"][:3]]
cases = {
    "original": base_records,
    "reversed": list(reversed(base_records)),
    "duplicate": base_records + [dict(base_records[1])],
    "conflict": base_records + [dict(base_records[1], flow=9.0)],
    "missing": [base_records[0], base_records[2]],
}
for name, records in cases.items():
    times = [row["elapsed_seconds"] for row in records]
    ordered = all(a < b for a, b in zip(times, times[1:]))
    same_time = defaultdict(set)
    for row in records:
        same_time[row["elapsed_seconds"]].add((row["flow"], row["pressure"]))
    duplicate_time = len(times) != len(same_time)
    conflicting_values = any(len(values) > 1 for values in same_time.values())
    unique_times = sorted(same_time)
    gap = any(b - a != 1 for a, b in zip(unique_times, unique_times[1:]))
    if conflicting_values or duplicate_time or gap:
        next_action = "check_source"
    elif not ordered:
        next_action = "sort_copy"
    else:
        next_action = "continue_checks"
    print(
        f"{name}: ordered={ordered}, duplicate_time={duplicate_time}, "
        f"conflict={conflicting_values}, gap={gap}, next={next_action}"
    )
```

期望输出：

```text
1) quick structural check
row_count: 36
event_id_count: 3
has_time_order: yes

2) repeated rows per event
A: row_count=18, enough_rows=True
B: row_count=12, enough_rows=True
C: row_count=6, enough_rows=False

3) if we compare rows as if each row were a sample
A at 0s: flow=0.8
A at 1s: flow=0.9
A at 2s: flow=1.1
A at 3s: flow=1.2
A at 4s: flow=1.3
A at 5s: flow=1.4
A at 6s: flow=1.5
A at 7s: flow=1.6
... 28 more time-point rows

4) after regrouping into one row per event
A: observed_span=17s, mean_flow=1.25, peak_pressure=2.0, enough_rows=True
B: observed_span=11s, mean_flow=0.88, peak_pressure=1.5, enough_rows=True
C: observed_span=5s, mean_flow=0.98, peak_pressure=1.5, enough_rows=False

5) controlled changes to A's first three records
original: ordered=True, duplicate_time=False, conflict=False, gap=False, next=continue_checks
reversed: ordered=False, duplicate_time=False, conflict=False, gap=False, next=sort_copy
duplicate: ordered=False, duplicate_time=True, conflict=False, gap=False, next=check_source
conflict: ordered=False, duplicate_time=True, conflict=True, gap=False, next=check_source
missing: ordered=True, duplicate_time=False, conflict=False, gap=True, next=check_source
```

第 1、2 步的 `has_time_order` 只检查**从文件读入的顺序是否在每个事件内严格递增**。时刻重复或顺序倒置都会得到 `no`，但原因不同。即使像 0→2 秒那样缺少中间记录，也能通过递增检查。

`minimum_rows_per_event` 为 12 时，A、B 通过行数条件；降到 6 时，A、B、C 都通过。`enough_rows=True` 只表示这个条件成立。重复行也计入行数，因此它不能证明有足够的独立观测点或已观测完整动作。动作开始与结束记录、采样间隔和运行条件仍需分别确认。

第 4 步的 `observed_span` 是最后观测时刻减去首次观测时刻。A 的 `17s` 表示观测覆盖 0~17 秒，不表示动作在 17 秒时结束。平均流量和峰值压力也只是现有记录的摘要，并非可以立即比较的判定。

第 5 步仅复制 A 的前三条记录进行实验。`reversed` 只改变顺序，因此得到 `sort_copy`；重复、冲突和缺失情况得到 `check_source`。冲突情况应暂缓汇总，直到核对原始记录。`gap` 检查的是本实验每秒采样一次的假设，不检查区段开始之前、结束之后的漏记或单元格缺失值。`continue_checks` 也不表示所有质量检查都已通过。

请把 `conflict` 中新增的流量从 9.0 改为原始值 0.92。虽然 `conflict` 变为 False，但 `duplicate_time` 仍为 True，因此仍需核对原始记录。再把 `missing` 中缺少的 1 秒记录补回，`gap` 就会变为 False。即使同样出现顺序异常信号，也应分别写出原因和下一步行动。

## 检查清单

- 是否用五行写下了新表的行含义、标识符、时间列、比较条件和原始证据？
- 能否区分事件标识重复与同一事件、时刻组合重复？
- 能否针对逆序、冲突值和缺失记录，说明排序、暂缓汇总或核对原始记录的选择及理由？
- 是否区分了行数条件通过、观测区段长度与完整动作观测的证据？
- 是否记录了原始文件与行位置，并保留派生表的处理历史？

## 来源与参考资料

- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. 它区分了变量、观测值和表结构，因此支持本节的出发点：应该先写下 `一行表示什么`。 [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Earo Wang, Dianne Cook, Rob J. Hyndman, `A New Tidy Data Structure to Support Exploration and Modeling of Temporal Data`, *Journal of Computational and Graphical Statistics* 29(3), 2020. 它提供了通过区分 key 和 index 来阅读时间数据的原则，因此强化了这样的判断：`什么能归组`、`有没有时间/顺序列` 应该最先检查。 [https://robjhyndman.com/publications/tsibble/](https://robjhyndman.com/publications/tsibble/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. 它同时处理 provenance 和 traceability，因此支持本节最后那一项检查：一旦出现奇怪案例，回头要看的原始证据应该在一开始就写下来。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
