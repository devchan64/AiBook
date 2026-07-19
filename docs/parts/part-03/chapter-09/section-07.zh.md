# P3-9.7 输入和结果满足什么条件，才能被读成预测问题

> Section ID: `P3-9.7`
> Version: `v2026.07.20`

如果已经决定把问题提升成预测问题，那么现在就要把它的结构是否真的满足预测条件这一点关上。重要的不是长篇理论，而是四个检查：哪些列是输入，哪些列是结果候选，预测时点之后的信息有没有混进来，以及你究竟看到哪一段信息、要去预测哪个时点的结果。

这一节会先把四件事关上：输入/结果区分、泄漏防止、运营时点可复现性、以及时间边界。

| 先要关上的东西 | 如果改写成问题 |
| --- | --- |
| 输入和结果的区分 | 哪些列是特征，哪些列是目标候选？ |
| 防止未来信息泄漏 | 预测时点还不知道的值，有没有被混进来？ |
| 运营时点可复现性 | 训练时做出的输入，能不能在运营里按同样规则重新做出来？ |
| cutoff / horizon | 看到哪一段信息，又要去预测哪个后续结果？ |

## 先看一个场景

即使还是同一张事件表，只要像下面这样把`预测前可知道的列`和`预测后才生成的列`混在一起，问题结构就会立刻被破坏。

| event_id | recent_diff | repeatability | review_result | target_candidate |
| --- | --- | --- | --- | --- |
| A | -0.32 | high | manual_reviewed | review_needed |
| B | -0.06 | low | skipped | normal |

这里的 `recent_diff` 和 `repeatability` 是可以在预测前构造出来的列。相反，`review_result` 只有在人已经完成复核之后才会出现。如果把这一列也放进输入里，那么表面上看表结构仍然正常，但实际上已经变成了`看过答案之后再构造输入`的结构。这样一来，即使训练时分数很高，也等于利用了真实预测时点并不存在的信息，因此不能再把它视为同一个问题。

## 用一个小图来看

输入/结果契约并不是`把列分开`就结束了，还必须按下面顺序关到只剩预测时点真正可用的值。

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-7-mermaid-01-zh.mmd"
```

所以，关上输入/结果契约，不只是`把列名分开`。还必须把`每一列是在什么时候生成的`一起写下来。要让一行样本输入成立，这一行里的所有值都必须是在同一个预测时点上真实能够被构造出来的值。

即使样本边界保持不变，输入表达也不必只能固定成一种形式。有的情况下，一行特征向量更自然；也有的情况下，保留时间顺序的一组输入更自然。真正重要的是，不管采用哪种表达方式，先要满足的都是：`这个输入在预测时点是否真的可用`，以及`结果候选和时间边界是否已经一起被关上了`。所以这里处理的，不是`随便一张表`，而是样本边界和时间边界都已经关上的输入结构。核心不是`把表传过去`，而是`把在预测时点成立的输入/结果契约关上`。更广一点说，这里关上的，是`输入定义`、`结果定义`、`时点可用性`、`可复现性`一起匹配的预测契约。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `feature`, `label`, `label leakage`。用于确认术语依据：特征是模型的输入变量，而标签泄漏是把标签的代理值混入特征中的设计缺陷。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Google, *Datasets: Dividing the original dataset*。用于确认训练/验证/测试数据应分离、相同特征变换也应应用到真实运营数据、验证/测试数据应贴近模型会遇到的真实数据这一观点。 [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*。用于确认 provenance 视角下应保留处理步骤、可复现性、版本管理和派生关系。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
