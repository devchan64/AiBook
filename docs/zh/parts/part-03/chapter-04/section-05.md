# P3-4.5 现在收集到的样本，在多大程度上代表了整体运行情况

> Section ID: `P3-4.5`
> Version: `v2026.07.11`

一旦把样本单位定成“一次完整动作”或“一个近期区段”之类的形式之后，还有一个很容易被漏掉的问题会留下来。那就是：`现在收集到的这组样本，在多大程度上代表了整体运行情况？` 即使表本身整理得很好，如果里面的案例只来自某一种工艺模式、某一段时期，或者某一种设备状态，那么这张表也可能没法均匀地描述整个运行场景。样本单位选得对，和样本集合能够均匀代表整体情况，并不是同一回事。

## 样本集合的代表性要和什么区分开

代表性的问题，在于：不再只问“一条样本定义得对不对”，而是进一步追问“这组样本到底覆盖了哪些运行范围”。

| 表面上看起来的状态 | 在 Part 3 里更应该先问的问题 |
| --- | --- |
| 样本单位已经整理好了 | 这些样本是在什么运行条件下收集的？ |
| 特征和标签候选也有了 | 它们会不会只集中在某个时期或某个模式里？ |
| 表的条数看起来也不少 | 它真的均匀覆盖了整体运行场景吗？ |

也就是说，`一条样本的定义` 和 `样本集合的代表性` 是两个不同的问题。

## 代表性容易变弱的典型场景

即便所有样本单位都已经统一成 `一次完整动作`，代表性还是可能因为它们来自哪里而差很多。

| 当前收集到的样本状态 | 为什么代表性会变弱 |
| --- | --- |
| 大多数来自白天正常运行 | 夜班、高负载、切换区间几乎没看到 |
| 大多数来自维护后时段 | 平时长期运行状态覆盖得较少 |
| 大多数来自某一台设备 | 设备之间的差异可能被忽略 |
| 只集中在一个月中的某一周 | 季节性、周期变化、策略变化可能被忽略 |

所以，哪怕样本数很多，只要覆盖条件很窄，代表性仍然可能偏弱。

## 先写下来的四件事

在 Part 3 里，现阶段比起正式的抽样理论，更重要的是先写下下面四样东西。

| 先写什么 | 换成问题就是 |
| --- | --- |
| 时间范围 | 样本来自哪一段时期？ |
| 运行模式范围 | 样本是在什么条件和状态下收集的？ |
| 设备 / 个体范围 | 样本来自哪些设备或哪些对象？ |
| 缺失范围 | 哪些条件或模式几乎没有出现？ |

这些记录不是为了以后证明泛化，而是为了先显露出：当前这张表代表了什么，以及还没有代表什么。

## 用一个小图来看

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-5-mermaid-01-zh.mmd"
```

这个图说明：即便所有样本单位都统一成 `一次完整动作`，它所覆盖的运行范围仍然可能明显偏向一边。换句话说，这一节例子的重点，不是去读很多原始数值，而是先看清 `哪些条件被过度代表了，哪些条件几乎是空的`。

## 为什么这个问题必须放在样本单位之后

只有在样本单位先定下来的前提下，代表性的问题才读得出来。如果连一行到底表示时点记录还是完整动作都还不清楚，那么诸如 `夜班动作有多少条？`、`高负载条件样本有多少条？` 这类问题，连正确计数都做不到。

所以顺序应该是下面这样。

1. 先决定什么算一条样本。
2. 再去看这些样本实际覆盖了哪些条件范围。

只有把这些记录留下来，后面读结果时，才能同时想到 `这一组样本到底来自哪些条件范围`，也不会漏掉 `哪些运行条件几乎没见过`。从这个意义上说，代表性问题更接近于：先写下当前样本集合到底覆盖了什么、又漏掉了什么。

## 小型代码示例

问题情境：即使所有样本单位都已经正确统一成 `一次完整动作`，也要检查实际的样本集合偏向了哪些条件。

输入(input)：包含 `shift`、`load_mode`、`machine_id`、`maintenance_phase` 的动作样本表

期望输出(output)：一个 `coverage summary`，显示哪些条件出现得很多，哪些条件几乎没出现

要确认的概念：一条样本定义正确，和样本集合均匀代表整体运行范围，是两个不同的问题

```python
import pandas as pd

samples = pd.DataFrame(
    [
        {"event_id": "A", "shift": "day", "load_mode": "normal", "machine_id": "M1", "maintenance_phase": "stable"},
        {"event_id": "B", "shift": "day", "load_mode": "normal", "machine_id": "M1", "maintenance_phase": "stable"},
        {"event_id": "C", "shift": "day", "load_mode": "high", "machine_id": "M1", "maintenance_phase": "stable"},
        {"event_id": "D", "shift": "day", "load_mode": "normal", "machine_id": "M2", "maintenance_phase": "stable"},
        {"event_id": "E", "shift": "night", "load_mode": "normal", "machine_id": "M1", "maintenance_phase": "stable"},
        {"event_id": "F", "shift": "day", "load_mode": "normal", "machine_id": "M1", "maintenance_phase": "after-maintenance"},
    ]
)

coverage = pd.DataFrame(
    [
        {"scope": "shift", "most_seen": samples["shift"].value_counts().idxmax(), "count": samples["shift"].value_counts().max(), "least_seen": samples["shift"].value_counts().idxmin()},
        {"scope": "load_mode", "most_seen": samples["load_mode"].value_counts().idxmax(), "count": samples["load_mode"].value_counts().max(), "least_seen": samples["load_mode"].value_counts().idxmin()},
        {"scope": "machine_id", "most_seen": samples["machine_id"].value_counts().idxmax(), "count": samples["machine_id"].value_counts().max(), "least_seen": samples["machine_id"].value_counts().idxmin()},
        {"scope": "maintenance_phase", "most_seen": samples["maintenance_phase"].value_counts().idxmax(), "count": samples["maintenance_phase"].value_counts().max(), "least_seen": samples["maintenance_phase"].value_counts().idxmin()},
    ]
)

print("1) raw sample coverage table")
print(samples)
print()
print("2) coverage summary")
print(coverage)
```

期望输出：

```text
1) raw sample coverage table
  event_id  shift load_mode machine_id  maintenance_phase
0        A    day    normal         M1             stable
1        B    day    normal         M1             stable
2        C    day      high         M1             stable
3        D    day    normal         M2             stable
4        E  night    normal         M1             stable
5        F    day    normal         M1  after-maintenance

2) coverage summary
               scope most_seen  count         least_seen
0              shift       day      5              night
1          load_mode    normal      5               high
2         machine_id        M1      5                 M2
3  maintenance_phase    stable      5  after-maintenance
```

这个例子里真正重要的，不是某种分类技巧，而是让人一眼就看见 `当前这张表到底看到了什么很多，什么又几乎没看到`。在第 1 步里，我们看到实际进入表里的条件组合；在第 2 步里，我们立刻读出每个范围中什么被过度代表，什么几乎不可见。只有这样，才能同时用数字和表去解释：`样本数虽然有 6 条，为什么代表性还是偏弱。`

读这张表时，最好一起检查三件事。它能不能说明样本来自怎样的时间、模式和设备范围？能不能把几乎没看到的条件写下来？等以后读评估分数时，能不能连这个代表性范围也一起想起来？只有把这样的记录附上去，样本表才不只是 `整理好的表`，而会变成 `同时记录了自己代表什么运行范围的表`。

样本单位选得对，并不自动意味着这组样本就能代表整个运行情况。所以，在 Part 3 里，时间范围、模式范围、设备范围以及剩余空白，都应该一起写下来。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。因为必须先固定 example 单位，后面才能继续追问“哪些 example 的集合代表了当前问题”，所以它强化了本节的出发点：一条样本的定义和样本集合的代表性应当分开来读。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- W3C, `PROV-Overview`. 它说明 provenance 和 activity context 应当一起保留，因此提供了这个上位框架：如果想说明代表性的覆盖范围，就必须能追踪当前样本集合来自什么时间段、什么设备、什么运行模式。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. 它说明在比较当前表现与过去表现时，样本应来自相同本质条件，因此提供了一般依据：比起样本数，更应该先整理这些数据究竟覆盖了哪些运行条件。 [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
