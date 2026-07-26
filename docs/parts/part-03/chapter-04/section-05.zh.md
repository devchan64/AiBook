# P3-4.5 现在收集到的样本，在多大程度上代表了整体运行情况

> Section ID: `P3-4.5`
> Version: `v2026.07.25`

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

输入(input)：保存在 [p3_4_5_sample_coverage.csv](/AiBook/assets/part-03/chapter-04/p3_4_5_sample_coverage.csv) 里的动作样本表，以及最低观察标准 `minimum_count`。这张表里包含 `shift`、`load_mode`、`machine_id`、`maintenance_phase`。

期望输出(output)：一个 `coverage summary`，显示哪些条件出现得很多，哪些条件几乎是空的。只要改变 `minimum_count`，被标为代表性空白的条件数量也会改变。

要确认的概念：一条样本定义正确，和样本集合均匀代表整体运行范围，是两个不同的问题。代表性判断需要观察标准。

```python
# 这个例子按类别和时间区段检查已收集样本对整体运行情况的代表性。
import csv
from collections import Counter
from pathlib import Path

minimum_count = 9
preview_sample_count = 8

input_path = Path("docs/assets/part-03/chapter-04/p3_4_5_sample_coverage.csv")
coverage_scopes = ["shift", "load_mode", "machine_id", "maintenance_phase"]

with input_path.open(newline="", encoding="utf-8") as file:
    samples = list(csv.DictReader(file))

coverage_summary = []
for scope in coverage_scopes:
    counts = Counter(sample[scope] for sample in samples)
    ordered_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    most_seen, most_seen_count = ordered_counts[0]
    least_seen, _ = sorted(counts.items(), key=lambda item: (item[1], item[0]))[0]
    under_minimum = sum(1 for count in counts.values() if count < minimum_count)
    coverage_summary.append(
        {
            "scope": scope,
            "most_seen": most_seen,
            "count": most_seen_count,
            "least_seen": least_seen,
            "unique_conditions": len(counts),
            "under_minimum_conditions": under_minimum,
        }
    )

print("1) raw sample coverage table")
for sample in samples[:preview_sample_count]:
    print(
        f"{sample['event_id']}: shift={sample['shift']}, "
        f"load_mode={sample['load_mode']}, machine_id={sample['machine_id']}, "
        f"maintenance_phase={sample['maintenance_phase']}"
    )
print(f"... {len(samples) - preview_sample_count} more event-level samples")
print()
print(f"2) coverage summary when minimum_count = {minimum_count}")
for item in coverage_summary:
    print(
        f"{item['scope']}: most_seen={item['most_seen']} ({item['count']}), "
        f"least_seen={item['least_seen']}, "
        f"unique_conditions={item['unique_conditions']}, "
        f"under_minimum_conditions={item['under_minimum_conditions']}"
    )
```

期望输出：

```text
1) raw sample coverage table
E01: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E02: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E03: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E04: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E05: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E06: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E07: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
E08: shift=day, load_mode=normal, machine_id=M1, maintenance_phase=stable
... 28 more event-level samples

2) coverage summary when minimum_count = 9
shift: most_seen=day (26), least_seen=night, unique_conditions=2, under_minimum_conditions=0
load_mode: most_seen=normal (25), least_seen=low, unique_conditions=3, under_minimum_conditions=2
machine_id: most_seen=M1 (22), least_seen=M2, unique_conditions=3, under_minimum_conditions=2
maintenance_phase: most_seen=stable (28), least_seen=after-maintenance, unique_conditions=2, under_minimum_conditions=1
```

这个例子里真正重要的，不是某种分类技巧，而是让人一眼就看见 `当前这张表到底看到了什么很多，什么又几乎没看到`。这里可以调节的值是 `minimum_count`。当 `minimum_count = 9` 时，有些范围如 `shift` 的所有条件都超过标准，而 `load_mode`、`machine_id`、`maintenance_phase` 中则有部分条件会被标为代表性空白。降低这个值，空白会减少；提高这个值，更多条件会被标为不足。这样才能同时用数字和表解释：`样本数虽然有 36 条，为什么代表性仍然会因条件而不同。`

读这张表时，最好一起检查三件事。它能不能说明样本来自怎样的时间、模式和设备范围？能不能把几乎没看到的条件写下来？等以后读评估分数时，能不能连这个代表性范围也一起想起来？只有把这样的记录附上去，样本表才不只是 `整理好的表`，而会变成 `同时记录了自己代表什么运行范围的表`。

代表性空白之后也会出现在模型评估里。下面的例子继续使用同一个 CSV，把前 24 条作为训练集合，把后 12 条作为确认集合。训练集合里 `normal` 和 `stable` 条件很多，而确认集合里 `low` 和 `after-maintenance` 条件更多。这里把 `high` 负载或维修后条件标为 1，做成一个观察用的简化标签 `needs_review`，并比较一个简单基准模型和一棵小决策树。

问题场景：想确认在代表性偏斜的训练集合中，基准模型和模型的错误会集中在哪些条件上。

输入(input)：同一个 `p3_4_5_sample_coverage.csv`、类别条件列，以及简化标签 `needs_review`。

期望输出(output)：训练/确认集合的条件分布、基准模型和决策树的准确率、按 `load_mode` 汇总的错误数。

要确认的概念：如果只看一个整体准确率，几乎没见过的运行条件可能会被隐藏，所以代表性空白必须和条件级错误一起读。

```python
# 这个例子用来确认训练覆盖偏斜时，基准模型和模型错误会集中在哪里。
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

input_path = Path("docs/assets/part-03/chapter-04/p3_4_5_sample_coverage.csv")
samples = pd.read_csv(input_path)

# 这是本节观察用的简化标签。真实运行标签需要另外经过业务检视来定义。
samples["needs_review"] = (
    samples["load_mode"].eq("high") | samples["maintenance_phase"].eq("after-maintenance")
).astype(int)

train = samples[samples["event_id"].between("E01", "E24")]
test = samples[samples["event_id"].between("E25", "E36")]
features = ["shift", "load_mode", "machine_id", "maintenance_phase"]

preprocess = ColumnTransformer(
    [("category", OneHotEncoder(handle_unknown="ignore"), features)]
)
models = {
    "dummy": DummyClassifier(strategy="most_frequent"),
    "tree": DecisionTreeClassifier(random_state=0, max_depth=3),
}

print("train coverage")
print(train.groupby(["load_mode", "maintenance_phase"])["event_id"].count())
print()
print("test coverage")
print(test.groupby(["load_mode", "maintenance_phase"])["event_id"].count())
print()

for name, estimator in models.items():
    model = make_pipeline(preprocess, estimator)
    model.fit(train[features], train["needs_review"])
    predicted = model.predict(test[features])
    result = test.assign(
        predicted=predicted,
        error=lambda df: df["predicted"].ne(df["needs_review"]),
    )
    print(f"{name} accuracy:", accuracy_score(test["needs_review"], predicted))
    print("errors by load_mode:", result.groupby("load_mode")["error"].sum().to_dict())
```

期望输出：

```text
train coverage
load_mode  maintenance_phase
high       stable                4
normal     after-maintenance     2
           stable               18
Name: event_id, dtype: int64

test coverage
load_mode  maintenance_phase
high       after-maintenance    1
           stable               1
low        after-maintenance    2
           stable               3
normal     after-maintenance    3
           stable               2
Name: event_id, dtype: int64

dummy accuracy: 0.4166666666666667
errors by load_mode: {'high': 2, 'low': 2, 'normal': 3}
tree accuracy: 0.75
errors by load_mode: {'high': 0, 'low': 3, 'normal': 0}
```

如果只看整体准确率，决策树看起来比基准模型好。但 `errors by load_mode` 显示，`low` 条件上仍然留下了错误。这个条件在训练集合里没有出现，而是在确认集合中第一次出现。因此这段输出会让我们先问的不是 `模型分数有多好`，而是 `评估前几乎没有见过哪些条件`。代表性检查既是模型训练前的表格检查，也是阅读模型评估时必须回头看的条件检查。

样本单位选得对，并不自动意味着这组样本就能代表整个运行情况。所以，在 Part 3 里，时间范围、模式范围、设备范围以及剩余空白，都应该一起写下来。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。因为必须先固定 example 单位，后面才能继续追问“哪些 example 的集合代表了当前问题”，所以它强化了本节的出发点：一条样本的定义和样本集合的代表性应当分开来读。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. 它说明 provenance 和 activity context 应当一起保留，因此提供了这个上位框架：如果想说明代表性的覆盖范围，就必须能追踪当前样本集合来自什么时间段、什么设备、什么运行模式。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. 它说明在比较当前表现与过去表现时，样本应来自相同本质条件，因此提供了一般依据：比起样本数，更应该先整理这些数据究竟覆盖了哪些运行条件。 [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
