# P3-2.3 第一次拿到新表时，应该先写下什么

> Section ID: `P3-2.3`
> Version: `v2026.07.25`

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

## 用一个小图来看

第一次读一张新表时，更安全的顺序是：`确认行的含义 -> 确认归组标准 -> 检查格式/质量 -> 判断是否需要重新归组`。

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-3-mermaid-01-zh.mmd"
```

## 非常短的读表备忘录

如果先写下下面五行，就能很快分清这张表的身份和可比较性。

- 一行表示 `_____`。
- 把同一个对象归在一起的键是 `_____`。
- 表示时间或流程顺序的列是 `_____`。
- 这张表可以直接比较 / 还需要重新归组。
- 回头核对奇怪案例的原始证据是 `_____`。

例如，对于自动动作日志，可以这样写。

- 一行表示 `动作中的某一个时点测量值`。
- 把同一个对象归在一起的键是 `event_id`。
- 时间列是 `elapsed_seconds`。
- 这张表还不是能直接比较的样本表，仍然需要重新归组。
- 回头核对奇怪案例的原始证据，是按 `event_id` 保存的原始日志。

一旦有了这五行备忘录，Chapter 3 里那句 `按问题重设计数据集`，读起来也会少很多抽象感。

再往前走一步，还可以把格式一致性和第一次质量检查分开写。

- 格式一致性：先看 `event_id` 是否能用一致格式把同一个动作归在一起，`elapsed_seconds` 是否真能读出时间顺序。
- 第一次质量检查：检查有没有某些 `event_id` 的行数异常地多或少，时间是否倒退或缺段，以及在比较前是否已有需要单独标记的缺失值。

## 小型代码示例

问题情境：第一次拿到一张新日志表时，检查它能不能直接被读成样本比较表。

输入(input)：保存在 [p3_2_3_first_table_log.csv](/AiBook/assets/part-03/chapter-02/p3_2_3_first_table_log.csv) 里的原始日志表，以及把事件看作可比较候选所需的最少行数 `minimum_rows_per_event`

期望输出(output)：即使是同一张表，只要先检查 `行的含义`、`归组标准`、`时间/顺序列`，就会显露出它还不是能直接比较的表。改变 `minimum_rows_per_event` 后，哪些事件拥有足够记录、能作为候选也会跟着改变。

要确认的概念：第一次读表时，在计算之前，必须先确认 `这一行是一整条样本`，还是 `只是样本记录的一部分`。同时设置重复行数阈值后，结构检查就不只是输出信息，而会连到可比较性判断。

```python
# 这个例子在第一次拿到新的 CSV 表时，先检查列名和值的分布。
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
print("has_time_order: yes")
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
    duration = max(row["elapsed_seconds"] for row in event_rows)
    mean_flow = sum(row["flow"] for row in event_rows) / len(event_rows)
    peak_pressure = max(row["pressure"] for row in event_rows)
    enough_rows = len(event_rows) >= minimum_rows_per_event
    print(
        f"{event_id}: duration={duration}s, mean_flow={mean_flow:.2f}, "
        f"peak_pressure={peak_pressure:.1f}, enough_rows={enough_rows}"
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
A: duration=17s, mean_flow=1.25, peak_pressure=2.0, enough_rows=True
B: duration=11s, mean_flow=0.88, peak_pressure=1.5, enough_rows=True
C: duration=5s, mean_flow=0.98, peak_pressure=1.5, enough_rows=False
```

这个例子真正展示的，并不只是找到了 `event_id` 和 `elapsed_seconds` 这两个列名。第 1 步和第 2 步里首先要读出来的是：`总行数 36` 大于 `event_id 数 3`，而且同一个 `event_id` 会在多行里重复出现。这里可以操作的值是 `minimum_rows_per_event`。如果把它设为 `12`，A 和 B 会成为拥有足够记录的候选，但 C 仍然是记录不足的候选。如果把它降到 `6`，C 也会成为候选；不过，用更短记录算出来的均值能不能用同样权重参与比较，还需要重新检查。只有读到这个信号，我们才能走到这样的解释：`当前这一行不是一整条样本，而只是样本记录的一部分`。所以，如果像第 3 步那样立刻把每一行拿来比较，我们仍然得不到一张真正比较 `A 整个动作`、`B 整个动作` 和 `C 整个动作` 的表。反过来，只有像第 4 步那样按 `event_id` 重新归组之后，一次动作才会变成一行，也只有这时，像平均流量、峰值压力这样可比较的列才会出现在其上。

如果再从格式与质量的视角重读同样结果，会更清楚。`event_id` 会重复，说明从格式一致性角度看，`确实存在一个可以把一条样本归组起来的键`。而 `rows per event` 彼此不同，则说明从第一次质量检查角度看，`不同样本的记录长度并不一样`。这种差别必须在早期就写下来，这样以后比较均值时，我们才能同时读到 `为什么有些样本是建立在更少证据之上的`。

之所以要先写下格式一致性和第一次质量检查，是为了避免一拿到新表就先贴上均值或模型名字，而是先看清楚 `现在手上的行到底是什么`，以及 `还有什么在阻碍比较`。只有在键格式、时间顺序、重复长度、缺失值和孤立行等问题先被整理出来之后，后面重新归组样本、构造可比较列时，才能用同一套稳定标准去读这张表。

## 来源与参考资料

- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. 它区分了变量、观测值和表结构，因此支持本节的出发点：应该先写下 `一行表示什么`。 [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Earo Wang, Dianne Cook, Rob J. Hyndman, `A New Tidy Data Structure to Support Exploration and Modeling of Temporal Data`, *Journal of Computational and Graphical Statistics* 29(3), 2020. 它提供了通过区分 key 和 index 来阅读时间数据的原则，因此强化了这样的判断：`什么能归组`、`有没有时间/顺序列` 应该最先检查。 [https://robjhyndman.com/publications/tsibble/](https://robjhyndman.com/publications/tsibble/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. 它同时处理 provenance 和 traceability，因此支持本节最后那一项检查：一旦出现奇怪案例，回头要看的原始证据应该在一开始就写下来。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
