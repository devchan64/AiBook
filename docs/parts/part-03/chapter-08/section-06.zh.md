# P3-8.6 只留在部分案例上的确认标签

> Section ID: `P3-8.6`
> Version: `v2026.07.25`

_副标题: 当确认标签只存在于被复核案例上时，解读里还要一起写什么？_

在解读阶段，有时不仅要看`数字差异如何`，还要看谁获得了确认[标签](/AiBook/zh/reference/concept-glossary-pinyin/l/#glossary-label)。在真实运营里，并不是每个事件都会接受同样深度的复核。往往只是那些看起来异常的部分案例，才会被人工再看一遍，并且只有这些案例上才会留下确认标签。如果把这种[选择性标签（selective labels）](/AiBook/zh/reference/concept-glossary-pinyin/x/#glossary-selective-labels)结构隐藏起来，读者就很容易把`有标签的案例集合`读成`全部事件集合`。

如果确认标签只留在被复核的案例上，就不能立刻把这些标签读成对整体的代表。

| 表面上看到的状态 | 解读里还要一起写的内容 |
| --- | --- |
| 只有部分案例有确认标签 | 这些案例为什么会被单独复核，是按什么标准选出来的？ |
| `review_needed=0` 的案例几乎没有被重新确认 | 没有标签到底是正常，还是尚未确认？ |
| 标签集中在某个时期或某台设备 | 标签集合本身是否存在[偏见](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-bias)？ |

来看下面这张表。

| event_id | review_needed | manually_reviewed | confirmed_root_cause |
| --- | ---: | ---: | --- |
| A | 1 | 1 | sensor_drop |
| B | 1 | 1 | valve_delay |
| C | 0 | 0 | None |
| D | 0 | 0 | None |

如果只看有 `confirmed_root_cause` 的这两条，就去描述整体运营的原因分布，解释就可能被夸大。还需要一起写清楚：为什么只有 A 和 B 被人工复核，C 和 D 的空白到底是因为它们确实正常，还是只是因为还没被看过。

在解读阶段，像下面这样的备注就已经足够。

| 先写下的备注 | 为什么需要它 |
| --- | --- |
| 成为复核对象的规则 | 为了显露出标签是被选择性留下的结构 |
| 缺失标签的含义 | 为了不把正常和未确认混在一起 |
| 有标签集合的范围偏向 | 为了不把解读强度说得过重 |

这里重要的点是：`选择性附着的确认标签，可以成为解读依据，但在把它当作代表所有事件的完整答案集合之前，必须先写出复核路径和可能的偏向。` 因此，确认标签表首先不该被读成`全部事件的答案表`，而应被读成通过[复核候选队列（review queue）](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-review-queue)等复核路径后，对部分事件得到的确认结果。

下面的例子把这个问题缩小成一次小型模型评估。在真实运营里，未被复核事件的最终结果可能并不知道。因此，代码中的 `actual_failure_for_demo` 只是学习用的隐藏结果。目的不是把这个值当作答案表，而是确认：如果只用被复核案例上留下的标签来评估模型，会出现什么样的错觉。

问题场景：当确认标签只存在于被复核案例上时，想确认模型分数会怎样随着复核路径而看起来不同。

输入(input)：`risk_score`、`manually_reviewed`、演示用隐藏结果 `actual_failure_for_demo`。

期望输出(output)：标签覆盖情况、在被复核标签上的准确率、为了演示而打开全部事件时的准确率，以及按复核路径汇总的错误数。

要确认的概念：如果只看选择性复核后的标签，模型可能看起来很好，但错误可能隐藏在未复核区间里。

```python
# 这个例子用来确认只使用选择性复核标签时，评估会如何偏斜。
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

events = pd.DataFrame(
    [
        {"event_id": "A", "risk_score": 0.92, "manually_reviewed": 1, "actual_failure_for_demo": 1},
        {"event_id": "B", "risk_score": 0.88, "manually_reviewed": 1, "actual_failure_for_demo": 1},
        {"event_id": "C", "risk_score": 0.81, "manually_reviewed": 1, "actual_failure_for_demo": 0},
        {"event_id": "D", "risk_score": 0.76, "manually_reviewed": 1, "actual_failure_for_demo": 1},
        {"event_id": "E", "risk_score": 0.69, "manually_reviewed": 0, "actual_failure_for_demo": 1},
        {"event_id": "F", "risk_score": 0.62, "manually_reviewed": 0, "actual_failure_for_demo": 0},
        {"event_id": "G", "risk_score": 0.55, "manually_reviewed": 0, "actual_failure_for_demo": 1},
        {"event_id": "H", "risk_score": 0.48, "manually_reviewed": 0, "actual_failure_for_demo": 0},
        {"event_id": "I", "risk_score": 0.37, "manually_reviewed": 0, "actual_failure_for_demo": 1},
        {"event_id": "J", "risk_score": 0.29, "manually_reviewed": 0, "actual_failure_for_demo": 0},
    ]
)

reviewed = events[events["manually_reviewed"].eq(1)]

model = DecisionTreeClassifier(random_state=0, max_depth=2)
model.fit(reviewed[["risk_score"]], reviewed["actual_failure_for_demo"])
events["predicted_from_reviewed_only"] = model.predict(events[["risk_score"]])
events["error"] = events["predicted_from_reviewed_only"].ne(events["actual_failure_for_demo"])

print("label coverage")
print(events.groupby("manually_reviewed")["event_id"].count().to_dict())
print("failure rate in reviewed labels:", reviewed["actual_failure_for_demo"].mean())
print("failure rate in all events for demo:", events["actual_failure_for_demo"].mean())
print(
    "accuracy on reviewed labels:",
    accuracy_score(reviewed["actual_failure_for_demo"], model.predict(reviewed[["risk_score"]])),
)
print(
    "accuracy on all events for demo:",
    accuracy_score(events["actual_failure_for_demo"], events["predicted_from_reviewed_only"]),
)
print("errors by review path:", events.groupby("manually_reviewed")["error"].sum().to_dict())
print(
    events[
        [
            "event_id",
            "manually_reviewed",
            "actual_failure_for_demo",
            "predicted_from_reviewed_only",
            "error",
        ]
    ].to_string(index=False)
)
```

期望输出：

```text
label coverage
{0: 6, 1: 4}
failure rate in reviewed labels: 0.75
failure rate in all events for demo: 0.6
accuracy on reviewed labels: 1.0
accuracy on all events for demo: 0.7
errors by review path: {0: 3, 1: 0}
event_id  manually_reviewed  actual_failure_for_demo  predicted_from_reviewed_only  error
       A                  1                        1                             1  False
       B                  1                        1                             1  False
       C                  1                        0                             0  False
       D                  1                        1                             1  False
       E                  0                        1                             1  False
       F                  0                        0                             1   True
       G                  0                        1                             1  False
       H                  0                        0                             1   True
       I                  0                        1                             1  False
       J                  0                        0                             1   True
```

只看被复核标签时，准确率是 `1.0`。但为了演示而打开全部事件的真实结果后，准确率会降到 `0.7`，而且 3 个错误全部都在 `manually_reviewed=0` 路径上。这个输出说明，有确认标签的案例未必代表全部事件。在真实运营中，未被复核事件的结果可能并不知道，所以更应该一起留下：`缺失标签是正常，还是未确认`，以及 `人工是按什么标准只复核了部分事件`。

## 用一个小图来看

这一节的核心，是不要把 `只留在被复核案例上的确认标签` 直接读成全部事件的答案表。只要出现确认标签，就应当把 `缺失标签的含义`、`复核路径` 和 `偏向可能性` 一起写出来，避免把解读强度说得过重。

--8<-- "assets/part-03/chapter-08/p3-8-6-mermaid-01-zh.mmd"

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。它提供了标签是附着在 example 上的结果信息这一基本框架，因此可以补强本节的说明：如果确认标签只留在部分案例上，那么这个有标签集合未必代表与全部事件集合相同的范围。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Himabindu Lakkaraju, Jon Kleinberg, Jure Leskovec, Jens Ludwig, Sendhil Mullainathan, `The Selective Labels Problem: Evaluating Algorithmic Predictions in the Presence of Unobservables`, KDD 2017。它说明在选择性标注数据中，观测到的结果可能只是既有人类决策选择之后才留下的结果，而不是整体人群的随机样本，因此直接支持本节的提醒：不要把只留在被复核案例上的标签读成全部事件的答案表。 [https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres](https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- W3C, `PROV-Overview`。它提供了记录某个结果是经过什么复核过程产生的 provenance 视角，因此可作为本节的一般依据：在解读选择性标签时，要把复核路径和缺失标签的含义一起写出来。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
