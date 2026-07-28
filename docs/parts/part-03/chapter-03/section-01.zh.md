# P3-3.1 为什么不能把原始数据立刻读成学习问题

> Section ID: `P3-3.1`
> Version: `v2026.07.25`

第一次拿到原始数据时，很多人几乎会反射性地先想到：`能用这个预测什么？` 因为眼前有表、有很多值，还有按时间流动记录下来的测量，所以看起来像是可以立刻改造成某种学习问题。但这种反应通常太快了。眼前这张表更可能还不是 `训练数据集`，而只是[被记录下来的原始数据](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-source-data)，最多也只是一个[数据集候选](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-dataset-candidate)。

这里首先要固定的是：[问题表示结构](/AiBook/zh/reference/concept-glossary-pinyin/w/#glossary-problem-representation-structure) 比 `学习问题框架` 更早。必须先明确这个警告：现在还不是去挑预测问题、分类问题、异常检测问题这类学习问题框架的时候。

进入这一章时，Chapter 2 里建立起来的 `数据集候选` 视角，会再收窄一步。

| 上一章留下来的东西 | 这一章额外确定的东西 | 要交给下一章的结构 |
| --- | --- | --- |
| 存储结构和数据集候选的差别、读新表时的第一轮检查 | 为什么原始数据还不该被提升成学习问题 | 实际去确定样本单位和表结构的判断 |

来看一种情况：每一次自动执行动作，都会留下控制参数时间序列和传感器时间序列。看到这种表时，通常最先跳出来的是下面这些想法。

- 既然有传感器值，就能改成异常检测问题。
- 动作结果有些差异，那就可以改成分类问题。
- 如果时序很长，也许能直接送进时序预测问题。

这些想法本身并不一定错。问题在于，在 `什么算一条案例`、`到底想预测什么`、[监督学习标签(supervised learning label)](/AiBook/zh/reference/concept-glossary-pinyin/l/#glossary-label)是否真的存在都还没定下来之前，学习问题框架就先出现了。在这种状态下，我们还没有定义数据问题，只是比数据本身更早地先想出了学习问题框架。

这种情况之所以经常发生，原因很清楚。第一，只要看到一张表，人就很容易立刻把它当成 `已经整理好的数据`。第二，如果过往 AI 学习经验主要是按学习问题类型留下来的，那么比起问题表达，预测方式会更早浮现。第三，原始时间序列越长、越复杂，越容易先出现一种期待：`是不是可以就这样直接送进学习问题？`

但是，如果把原始数据立刻读成数据集，就会跳过一些关键问题。

| 最容易先想到的问题 | 实际上更应该先问的问题 |
| --- | --- |
| 该把它读成什么学习问题？ | 什么该算一条[样本(sample)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)？ |
| 标签该放什么？ | 现在真的已经有稳定标签了吗？ |
| 怎样提高准确率？ | 该重新整理成什么表，比较才会成立？ |

这个差别不只是顺序问题。第一次看原始数据时，更需要做的不是选择学习问题，而是 `重新追问这张表到底是什么`。你现在看到的是按时点记录的测量值、一次动作的摘要，还是某个近期区段的聚合，这会让后面所有关于 [feature](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)、[baseline](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-baseline)、[target](/AiBook/zh/reference/concept-glossary-pinyin/m/#glossary-target) 的说明都发生变化。

例如，只看下面这一小段原始数据，学习问题框架就可能过早跳出来。

| event_id | second | pressure | flow |
| --- | --- | --- | --- |
| A | 0 | 1.0 | 0.0 |
| A | 1 | 2.0 | 1.4 |
| A | 2 | 2.4 | 1.6 |

只看这张表，很容易马上想到 `分类问题`、`预测问题`、`时序学习问题` 这样的词。但我们甚至还没有决定：这张表到底是 `时点记录`，还是 `单次动作表`。因此，如果此时立刻选学习问题框架，就会变成问题形式先跑到问题本身前面。

## 用一个小图来看

如果按 `原始记录 -> 先补空着的问题 -> 再整理样本和标签候选` 这条顺序重读，就会更清楚：为什么不能太早把原始数据提升成学习问题。

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-1-mermaid-01-zh.mmd"
```

问题情境：拿到按时点记录的日志表时，确认如果立刻把它读成学习问题，会有哪些关键问题仍然空着。

输入(input)：在每个 `event_id` 下混有多个时点测量值的原始日志表 [p3_3_1_source_operation_log.csv](/AiBook/assets/part-03/chapter-03/p3_3_1_source_operation_log.csv)，以及要作为标签候选来检查的列名 `label_column_to_try`

输入文件中的一行，是某一次动作(`event_id`)中某个具体秒数(`second`)测得的传感器记录。表里同时有 `batch_id`、`recipe`、`pressure`、`flow`、`vibration`、`temperature`，但现在还没有决定其中哪一列是样本标识符、哪一列是标签。

期望输出(output)：显露出 `现在就把它读成分类问题` 和 `先补齐那些空着的问题` 会导向不同结果。改变 `label_column_to_try` 后，也会看出列是否存在和能不能作为标签候选不是同一件事。

要确认的概念：在把原始数据读成学习问题之前，必须先定下什么是 `一条样本`、`标签候选`、`比较表`。学习问题判断不是一句固定的话，而必须根据当前表里的列和归组标准来确认。

```python
# 这个例子避免过早把原始日志读成学习问题，而是先重构为 event 级汇总表。
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

raw_log_path = "docs/assets/part-03/chapter-03/p3_3_1_source_operation_log.csv"
label_column_to_try = "review_label"

column_unit = {
    "batch_id": "operation_context",
    "recipe": "operation_context",
    "pressure": "time_point_sensor_value",
    "flow": "time_point_sensor_value",
    "vibration": "time_point_sensor_value",
    "temperature": "time_point_sensor_value",
    "review_label": "event_label",
}

raw = pd.read_csv(raw_log_path)

print("1) raw input shape and first rows")
print("shape:", raw.shape)
print(raw.head())
print()

print("2) too-early reading")
print("- maybe this is a classification problem")
print("- label column:", "found" if label_column_to_try in raw.columns else "not found yet")
print("- one training sample: not decided yet")
print()

column_exists = label_column_to_try in raw.columns
candidate_unit = column_unit.get(label_column_to_try, "unknown")
same_unit_as_sample = column_exists and candidate_unit == "event_label"
stable_label_meaning_known = same_unit_as_sample
usable_label_candidate = column_exists and same_unit_as_sample and stable_label_meaning_known

print("3) label candidate check")
print("- column to try:", label_column_to_try)
print("- column exists:", column_exists)
print("- candidate unit:", candidate_unit)
print("- same unit as one event:", same_unit_as_sample)
print("- stable label meaning known:", stable_label_meaning_known)
print("- usable label candidate:", usable_label_candidate)
print()

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        batch_id=("batch_id", "first"),
        recipe=("recipe", "first"),
        row_count=("second", "count"),
        duration_seconds=("second", "max"),
        max_pressure=("pressure", "max"),
        mean_flow=("flow", "mean"),
        max_vibration=("vibration", "max"),
        end_temperature=("temperature", "last"),
    )
)
print("4) questions that must be settled first")
print("- one sample: one event")
print("- candidate comparison table: one row per event")
print("- label candidate:", "usable" if usable_label_candidate else "still not decided")
print()

print("5) event-level table after defining the sample")
print(event_summary.round(2))
```

期望输出：

```text
1) raw input shape and first rows
shape: (36, 8)
  event_id batch_id    recipe  second  pressure  flow  vibration  temperature
0        A     B-17  standard       0       1.0   0.0       0.02         24.1
1        A     B-17  standard       1       2.0   1.4       0.04         24.4
2        A     B-17  standard       2       2.4   1.6       0.07         24.8
3        A     B-17  standard       3       2.2   1.2       0.08         25.0
4        B     B-17  standard       0       1.1   0.1       0.03         24.0

2) too-early reading
- maybe this is a classification problem
- label column: not found yet
- one training sample: not decided yet

3) label candidate check
- column to try: review_label
- column exists: False
- candidate unit: event_label
- same unit as one event: False
- stable label meaning known: False
- usable label candidate: False

4) questions that must be settled first
- one sample: one event
- candidate comparison table: one row per event
- label candidate: still not decided

5) event-level table after defining the sample
  event_id batch_id     recipe  row_count  duration_seconds  max_pressure  mean_flow  max_vibration  end_temperature
0        A     B-17   standard          4                 3           2.4       1.05           0.08             25.0
1        B     B-17   standard          4                 3           1.9       0.78           0.06             24.7
2        C     B-18       fast          4                 3           2.8       1.05           0.22             26.8
3        D     B-18       fast          4                 3           2.6       1.02           0.16             26.2
4        E     B-19   standard          4                 3           2.1       0.90           0.07             24.8
5        F     B-19   standard          4                 3           2.5       1.12           0.09             25.3
6        G     B-20  high-load          4                 3           3.1       1.35           0.28             27.5
7        H     B-20  high-load          4                 3           2.9       1.30           0.24             27.0
8        I     B-21   standard          4                 3           2.3       0.98           0.08             25.1
```

这个例子的核心，在于第 2 步和第 3 步的差别。第 2 步里先跳出来的只有一句 `也许这是个分类问题`，但实际上，`label_column_to_try` 指定的 `review_label` 列并不存在，连“一条训练样本”都还没有定下来。这里可以操作的值是 `label_column_to_try`。如果把它改成 `"flow"`，`column exists` 会变成 `True`，但 `candidate unit` 是 `time_point_sensor_value`，`usable label candidate` 仍然是 `False`。这是因为 `flow` 不是附着在一次动作上的稳定标签，而是时点级传感器值。相反，第 4 步先把结构固定成 `一条样本是一条动作`、`比较表是一条动作一行`。只有在这之后，才会像第 5 步那样出现包含 `row_count`、`duration_seconds`、`max_pressure`、`mean_flow`、`max_vibration`、`end_temperature` 的动作级比较表。也就是说，如果太快把原始数据读成学习问题，就会变成问题形式先被固定，而那些仍然空着的问题被遮过去了。

如果把“学习问题框架先跳出来时还空着的问题”并排写出来，问题会更明显。

| 最容易先跳出来的话 | 仍然空着的问题 |
| --- | --- |
| `异常检测问题` | 什么才算异常？ |
| `分类问题` | 稳定标签真的已经存在吗？ |
| `时序学习问题` | 一条样本是一个时点束，还是一次完整动作？ |

这张表的重点，不在于学习问题的名字错了，而在于：在那个框架之前必须先回答的问题仍然空着。数据建模，正是填这些空白的前段设计。

所以，第一次拿到原始数据时最常见的错误，就是把 `记录结构` 误当成 `学习结构`。仅仅因为存在按时点记录的日志，并不意味着预测问题已经被定义出来。只有在我们决定如何归组这些日志、留下什么、拿什么去比较之后，`数据集` 这个词才用得更准确。一旦学习问题框架先出现，这段前置设计就很容易被跳过，后面又得回头把样本单位和表结构拆开重做。如果把这一节重新读成一个管理 `问题提升(problem escalation)` 时点的问题，就会更清楚：核心并不是 `让模型名字晚一点再出现`，而是在样本单位和标签候选还没整理好之前，不要过早把它提升成学习问题。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。它说明 labeled example 由 features 和 label 构成，因此支持这一点：在一条样本和标签都还没定下来的原始数据上，不应该立刻把它读成学习问题。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `label leakage`。它说明 feature 变成 label proxy 的设计缺陷，因此强化了这个警告：如果先选问题框架，就有可能把还没整理好的原始列错误地读进糟糕的学习结构。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. provenance framework 说明它应该支持 identifying an object 和 representing derivation，因此强化了这个上位框架：必须先定下什么算一个对象，以及通过什么转换才做出了数据集候选。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
