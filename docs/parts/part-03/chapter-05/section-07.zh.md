# P3-5.7 同一个样本之后出现多个后续事件时，应该怎样折叠到表结构里

> Section ID: `P3-5.7`
> Version: `v2026.07.17`

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

输入(input)：按样本整理的后续事件列表，以及事件严重程度顺序

期望输出(output)：即使是同一个源事件，`first_event`、`worst_event`、`event_count`、`any_failure` 也会被生成成不同结果

要确认的概念：当多个后续事件被折叠成一个结果列时，必须先写明折叠规则，否则表结构的含义会漂移

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

期望输出：

```text
  event_id  any_failure first_event worst_event  event_count
0        A            1      review     failure            2
1        B            0      review      review            1
2        C            0        none        none            0
```

这个例子的关键在于：即使看的是同一个源事件，也可以同时生成不同的结果列，例如 `first_event` 是 `review`，`worst_event` 是 `failure`，而 `event_count` 是 2。所以，如果不先写清折叠规则，那么同一个样本 `A` 在不同表里就可能被读出不同含义。只要同一个样本之后有多个后续事件，就应该先写清：它们是按什么规则被折叠成一个结果列的，这样表结构的含义才不会晃动。

## 用一个小图来看

这一节压缩的是一点：`多个后续事件` 并不会自动变成同一个结果列。同一组事件，按 `any`、`first`、`worst`、`count` 里的不同规则折叠后，会得到不同的代表结果列。

--8<-- "assets/part-03/chapter-05/p3-5-7-mermaid-01-zh.mmd"

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `label` 与 `labeled example`。因为结果信息必须先被固定到某个 example 上，所以它支持这一节的判断：当多个后续事件被折叠进一个结果列时，必须先说明使用的是 `any`、`first`、`worst`、`count` 中的哪一种规则。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- Google for Developers, `Machine Learning Glossary` 中的 `label leakage`。因为它说明构造规则不清晰的结果列，很容易和预测候选混淆，所以它强化了“先写清折叠规则，才能固定表结构含义”这一点。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- W3C, `PROV-Overview`. provenance framework 说明派生关系和活动上下文应当可追踪，因此它提供了一个更高层的框架：多个后续事件究竟按什么规则被折叠成一个代表结果列，也应该是可追踪的。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
