# P3-4.2 一旦样本单位摇摆，哪些东西会一起摇摆

> Section ID: `P3-4.2`
> Version: `v2026.07.25`

[样本(sample)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)单位，是后面几乎所有概念的基准点。所以，如果把测量值和样本混在一起，问题不会只是“某个术语用错了”这么简单。[特征(feature)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)的含义会一起摇摆，[标签(label)](/AiBook/zh/reference/concept-glossary-pinyin/l/#glossary-label)的含义会一起摇摆，甚至连[评估(evaluation)](/AiBook/zh/reference/concept-glossary-pinyin/e/#glossary-evaluation)到底在评估什么，也会跟着一起摇摆。如果前一节已经定下了什么算一条样本，那么这一节要看的，就是那个决定还会一起固定什么、一起摇晃什么。

这一节不会重新定义样本单位本身，而是聚焦于一件事：为什么前一节固定下来的样本单位，会一路牵动后面的特征、标签、分割和评估。

先从最常见的混淆开始。假设有一张在动作执行过程中按 1 秒间隔测量出来的时间序列表。在很多情况下，人会直接把这张表的一行当成 `一条样本`。这样一来，压力、流量、温度这些当前值就会立刻被当成特征一样贴上去。但如果我们真正想知道的是 `这次动作的整体结构是不是和平常不同`，那么单个时点的一行，并不是能回答这个问题的样本。

问题可以按下面几项来整理。

## 1. 特征的含义会摇摆

如果把一次完整动作当作样本，那么总动作时长、前段均值、后段下降率、波动性这些值都可以成为特征。反过来，如果把单个时点的一行当作样本，那么同样这些列要么还没法计算，要么就算计算了，在那一行上意义也不完整。

## 2. 标签的含义会摇摆

如果某个运营标签是 `needs review`，那么它通常并不是贴在某一个测量点上，而是贴在一次完整动作或某个近期区段上。可一旦把单个时点行读成样本，连标签到底该贴在哪一行上都会变得含糊。

## 3. 评估单位会摇摆

如果样本是一整次动作，那么训练和评估也应该在动作级别上进行。但如果把单个时点行当成样本，那同一次动作里彼此很近的行就很容易同时混进训练和评估。

## 4. 运营解释会摇摆

运营人员真正想知道的，通常不是 `某一个时点的数值是多少`，而是 `整个动作到底怎么样`。可一旦测量值和样本混淆，运营问题和数据结构就会开始不匹配。

把这四个问题放在一起看，就会更清楚为什么样本单位绝不是单纯的术语问题。

再用一个简短的运营场景看，会更直观。假设生产线上的自动清洗动作每天会重复几百次。运营人员真正会问的，通常不是 `12:03:01 的流量正常吗？`，而更像是 `刚刚结束的这次清洗是不是比平时更不稳定？` 或 `最近 30 分钟里同样的异常是不是在重复？` 可一旦把单个时点行当成样本，运营问题指向的是“一次完整动作”，而[数据集(dataset)](/AiBook/zh/reference/concept-glossary-pinyin/d/#glossary-dataset)却指向按秒记录。就在这一刻，特征会被切得过细，标签会被重复复制，评估也会开始偏离真正的运营判断单位。

| 会一起摇摆的东西 | 为什么会一起摇摆 |
| --- | --- |
| 特征 | 因为应该摘要什么，取决于样本单位 |
| 标签 | 因为什么结果该贴到一条案例上，取决于样本单位 |
| 分割和评估 | 因为什么东西要被分到训练和评估里，取决于样本单位 |
| 运营语句 | 因为人把什么看成一条案例，取决于样本单位 |

这里如果把 `贴错的问题` 和 `应该重新贴回去的问题` 分开来看，样本单位的不匹配会更明显。

| 贴错的问题 | 为什么不对齐 | 应该重新贴回去的问题 |
| --- | --- | --- |
| 这一行正常吗？ | 一行只是时点记录，可能不能代表整个动作 | 这一次完整动作的结构和以往相比是否不同？ |
| 标签能贴在这一行上吗？ | 标签通常贴在一次动作或一个近期区段上 | 标签到底是贴在某个时点，还是贴在一整次动作上？ |
| 这一行能当一条训练样本吗？ | 同一次动作里相邻的行可能会同时混进训练和评估 | 分割对象是时点行，还是动作级样本？ |

所以，样本单位并不是只在 Part 3 某一节里才需要做的决定。它是 feature engineering、[基准线(baseline)](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-baseline)比较、[review queue](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-review-queue)，甚至后续预测输入结构解释都一起依赖的底层结构。

## 用一个小图来看

前面那几段的核心其实只有一个。样本单位一旦摇摆，feature、label、split、evaluation 和运营解释并不是各自单独跑偏，而是会一起失去同一个基准点。

--8<-- "assets/part-03/chapter-04/p3-4-2-mermaid-01-zh.mmd"

下面这个例子，会展示同一份[源数据(source data)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-source-data)在被读成 `时点表` 和 `动作级表` 时，特征、标签和分割解释会怎样变化。

问题情境：确认同一份日志在被读成 `时点表` 和 `动作级表` 时，特征、标签和 train/test 分割会如何一起摇摆。

输入(input)：按 `event_id` 存放的时点流量值，以及 `review_needed`

期望输出(output)：`row` 和 `event` 两种单位会产生不同的样本数、重复标签和分割稳定性

要确认的概念：样本单位一变，feature、label、split 的解释都必须在同一个单位上重新对齐

```python
# 这个例子检查样本单位摇摆时，特征、标签和基准是否也一起变化。
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.5, "review_needed": 1},
        {"event_id": "A", "second": 1, "flow": 1.8, "review_needed": 1},
        {"event_id": "A", "second": 2, "flow": 1.1, "review_needed": 1},
        {"event_id": "B", "second": 0, "flow": 0.4, "review_needed": 0},
        {"event_id": "B", "second": 1, "flow": 1.1, "review_needed": 0},
        {"event_id": "B", "second": 2, "flow": 1.0, "review_needed": 0},
        {"event_id": "C", "second": 0, "flow": 0.6, "review_needed": 1},
        {"event_id": "C", "second": 1, "flow": 1.9, "review_needed": 1},
        {"event_id": "C", "second": 2, "flow": 1.3, "review_needed": 1},
    ]
)

per_row = raw[["event_id", "second", "flow", "review_needed"]]
per_event = (
    raw.groupby("event_id", as_index=False)
    .agg(
        flow_mean=("flow", "mean"),
        flow_max=("flow", "max"),
        late_drop=("flow", lambda s: s.iloc[-2] - s.iloc[-1]),
        review_needed=("review_needed", "max"),
    )
)

row_split = raw.assign(split=lambda df: df["second"].map({0: "train", 1: "train", 2: "test"}))
event_split = per_event.assign(split=lambda df: df["event_id"].map({"A": "train", "B": "train", "C": "test"}))

unit_summary = pd.DataFrame(
    [
        {
            "unit": "row",
            "sample_count": len(per_row),
            "feature_example": "flow at one second",
            "label_rows": per_row["review_needed"].sum(),
            "train_events": ",".join(sorted(row_split.loc[row_split["split"] == "train", "event_id"].unique())),
            "test_events": ",".join(sorted(row_split.loc[row_split["split"] == "test", "event_id"].unique())),
        },
        {
            "unit": "event",
            "sample_count": len(per_event),
            "feature_example": "flow_mean / flow_max / late_drop",
            "label_rows": per_event["review_needed"].sum(),
            "train_events": ",".join(sorted(event_split.loc[event_split["split"] == "train", "event_id"].unique())),
            "test_events": ",".join(sorted(event_split.loc[event_split["split"] == "test", "event_id"].unique())),
        },
    ]
)

print("1) sample counts change with the chosen unit")
print("row-level samples:", len(per_row))
print("event-level samples:", len(per_event))
print()
print("2) row-level labels are repeated because the label belongs to the whole event")
print(per_row.groupby("event_id", as_index=False)["review_needed"].sum())
print()
print("3) event-level features and labels line up on the same unit")
print(per_event)
print()
print("4) split stability differs by unit")
print(unit_summary)
```

期望输出：

```text
1) sample counts change with the chosen unit
row-level samples: 9
event-level samples: 3

2) row-level labels are repeated because the label belongs to the whole event
  event_id  review_needed
0        A              3
1        B              0
2        C              3

3) event-level features and labels line up on the same unit
  event_id  flow_mean  flow_max  late_drop  review_needed
0        A   1.133333       1.8        0.7              1
1        B   0.833333       1.1        0.1              0
2        C   1.266667       1.9        0.6              1

4) split stability differs by unit
    unit  sample_count                    feature_example  label_rows train_events test_events
0    row             9                 flow at one second           6        A,B,C       A,B,C
1  event             3  flow_mean / flow_max / late_drop           2          A,B           C
```

这段输出同时展示了三件事。第一，`review_needed` 是贴在整次动作上的标签，但在时点表里，它会在 A 和 C 上各重复三次。第二，像 `late_drop` 这样的特征，只有在数据先被归成一次完整动作后才算得出来。第三，如果看 `unit summary`，在时点级分割里，同一个 `event_id` 可能同时出现在训练和评估两边；但在动作级分割里，就能把整个 `C` 都完整地留作测试。正是这个差别，说明了为什么 feature、label、split、evaluation 这些单位会一起摇摆。

如果先检查下面三个问题，而不是直接盯着输出值看，这个例子会更清楚。

1. `review_needed` 是贴在某个时点数值上，还是贴在一次完整动作上？
2. `flow_mean`、`flow_max` 是从单独一行直接读出来的值，还是把多行归组后得到的值？
3. 真要做训练/评估分割时，我们分的是 `per_row`，还是 `per_event`？

只要把这三个问题答出来，就会更明白为什么那句 `同一份原始数据也必须先固定样本单位` 会被反复强调。

同样的问题也可以缩小成一次真实模型评估来看。下面的代码不是为了教学怎样用好 `DecisionTreeClassifier`。它只是用来确认：如果同一次动作的行同时进入训练和评估，评估分数可能看起来过高；而按动作整体留出测试时，这种错觉会变小。

问题场景：想确认同一份原始日志用行级分割评估和用动作级分割评估时，可能得到不同分数。

输入(input)：包含 `event_id`、`second`、`flow`、`review_needed` 的小型动作日志。

期望输出(output)：在行级分割中同时进入训练和评估的 `event_id`、行级评估分数、动作级评估分数。

要确认的概念：如果同一次动作中的相邻行混进训练和评估两边，模型看起来像是在预测新动作，但更接近于重新匹配已经见过的动作附近的数值。

```python
# 这个例子用来确认同一份原始日志的分割单位会如何改变评估分数。
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

raw_rows = []
labels = {"A": 1, "B": 0, "C": 1, "D": 0, "E": 1, "F": 0, "G": 0, "H": 1}
base_flow = {"A": 10, "B": 30, "C": 50, "D": 70, "E": 90, "F": 110, "G": 130, "H": 150}

for event_id, label in labels.items():
    for second, offset in enumerate([0.0, 0.2, -0.1]):
        raw_rows.append(
            {
                "event_id": event_id,
                "second": second,
                "flow": base_flow[event_id] + offset,
                "review_needed": label,
            }
        )

raw = pd.DataFrame(raw_rows)

# 行级分割：每个 event_id 的部分行会同时进入 train 和 test。
row_train = raw[raw["second"].isin([0, 1])]
row_test = raw[raw["second"].eq(2)]

# 动作级分割：test event_id 会从训练中被完整排除。
event_train = raw[raw["event_id"].isin(["A", "B", "C", "D"])]
event_test = raw[raw["event_id"].isin(["E", "F", "G", "H"])]


def evaluate(train, test):
    model = DecisionTreeClassifier(random_state=0)
    model.fit(train[["flow"]], train["review_needed"])
    predictions = model.predict(test[["flow"]])
    return accuracy_score(test["review_needed"], predictions), [
        (event_id, int(prediction), int(actual))
        for event_id, prediction, actual in zip(test["event_id"], predictions, test["review_needed"])
    ]


row_accuracy, _ = evaluate(row_train, row_test)
event_accuracy, event_predictions = evaluate(event_train, event_test)
leaked_events = sorted(set(row_train["event_id"]) & set(row_test["event_id"]))

print("leaked events in row split:", leaked_events)
print("row split accuracy:", row_accuracy)
print("event split accuracy:", event_accuracy)
print("event split predictions:", event_predictions)
```

期望输出：

```text
leaked events in row split: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
row split accuracy: 1.0
event split accuracy: 0.5
event split predictions: [('E', 0, 1), ('E', 0, 1), ('E', 0, 1), ('F', 0, 0), ('F', 0, 0), ('F', 0, 0), ('G', 0, 0), ('G', 0, 0), ('G', 0, 0), ('H', 0, 1), ('H', 0, 1), ('H', 0, 1)]
```

在行级分割中，所有 `event_id` 都同时进入训练和评估。所以分数看起来很好，达到 `1.0`。但这与其说是模型很好地预测了新动作，不如说是它重新匹配了同一次动作附近的行。这种错觉也需要从[数据泄漏(data leakage)](/AiBook/zh/reference/concept-glossary-pinyin/d/#glossary-data-leakage)角度检查。动作级分割中，`E`、`F`、`G`、`H` 整体都没有进入训练，所以分数降到 `0.5`。这个差异通过模型输出说明：样本单位也必须一起固定评估单位。

这段代码里可以改两个值。改变 `event_train` 和 `event_test` 中的 `event_id` 组合，动作级评估会改变。把 `second` 这样的列也加入特征时，模型用于预测的依据也可能改变。重要的不是分数本身，而是 `把什么切成一个样本` 会改变评估结果的含义。

再补一层很短的说明，就能更直接地读出摇摆的方向。

- 如果 `review_needed` 是动作级标签，那么 `per_row` 分割就有很高风险把标签单位切错。
- 如果 `flow_mean`、`flow_max` 是把多行归组后生成的特征，那么一旦把时点行当成样本，特征的含义也会一起改变。
- 所以样本单位一旦摇摆，feature、label、split 并不是各自独立地摇摆，而是会一起失去对齐。

把同样的内容再压缩一点，可以这样读。

| 如果把一条时点行当成样本 | 如果把一次完整动作当成样本 |
| --- | --- |
| 标签会被重复复制到多行 | 标签只会贴一次到一条动作上 |
| 很难直接做出完整动作特征 | 摘要特征能用同样方式贴上去 |
| 同一个动作可能同时混进训练和评估 | 可以按动作单位分割 |
| 运营问题和数据单位会错位 | 运营问题和数据单位会对齐 |

所以，当样本单位摇摆时，这个问题不应该被读成简单的记号混乱，而应该被读成一种一致性崩塌：feature、label、split、evaluation 开始指向不同单位。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。因为一个 example 要求 features 和 label 对齐在同一个单位上，所以它为这个判断提供依据：样本单位一旦摇摆，feature 和 label 的含义也会一起摇摆。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `label leakage`。它说明 feature 成为 label proxy 的设计缺陷，因此强化了这个警告：如果在错误单位上混用行级 feature 和动作级 label，就会产生结构性错误。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- scikit-learn developers, `Cross-validation: evaluating estimator performance`。它说明在 grouped data 中，同一组里的相互依赖样本不应同时出现在训练 fold 和验证 fold，因此直接强化了本节关于分割/评估的警告：如果把时点行当作样本，同一动作中的相邻行可能会混进训练和评估。 [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. provenance framework 说明它应支持 reproducibility 和 derivation，因此强化了这个上位框架：只有可复现地记录“特征和标签是在什么单位上做出来的”，split 和 evaluation 才可能维持同一套标准。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
