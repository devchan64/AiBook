# P3-9.11 候选目标与变化的标准

> Section ID: `P3-9.11`
> Version: `v2026.09.20`

同一样本可能同时记录是否需要复核、检查后的状态和处理优先级。这些列回答不同问题。应把“本次选择哪个[目标](/AiBook/zh/reference/concept-glossary-pinyin/m/#target)来学习”和“记录该目标依据什么标准判定”分开处理。

## 位于同一行，不表示是同一个答案

下表 A、B、C 是本节虚构的已完成动作。`review_needed` 表示按规定复核标准判断的需要程度，`final_status` 表示检查范围内确认的最终状态。最终状态定义为 `inspection-status-v1`：检查完成后确认异常则记为 `abnormal`，未确认异常则记为 `normal`。`normal` 不表示以后也不会发生故障。

| event_id | `review_needed` | `final_status` | `label_status` |
| --- | ---: | --- | --- |
| A | 1 | ? | pending |
| B | 1 | normal | confirmed |
| C | 0 | normal | confirmed |

本教学表假设三个动作都纳入了检查。C 即使复核需要为 0，也完成了单独检查，因此有 `normal`；不是把需要 0 直接复制成正常标签。A 的 `pending` 是确认状态，不是与 `normal`、`abnormal` 并列的最终结果类别。

若要复现复核标准的判断，A、B 的 `review_needed=1` 是同一个答案。若要根据动作完成时的信息预测之后的检查状态，目标则是 `final_status`，A 的答案尚不存在。也不能仅凭 B、C 两个正常结果就认定训练数据充足。输入限于检查前的信息，不能包含检查结果。

本节选择“预测检查后状态”作为主要问题，因此记录 `target_name=final_status`、`target_definition_version=inspection-status-v1`，复核需要和处理排名分别保留。代表目标确定的是本次学习与评估要回答的问题。也可以选择其他问题，或设计同时预测多个结果的任务，但每个结果都应分别说明定义、观察条件与评估方式。

## 对同一观测应用两套标准

再看仅改变复核需要标准的独立案例 X。`recent_diff` 表示相同条件下近期平均流量减去基线平均流量，单位为 L/min。固定原始资料、聚合窗口、基线与计算版本后，X 的值为 `-0.25`。以下是教学规则，不是真实安全标准。

| 复核定义版本 | 生效时刻（KST） | 生成 `review_needed` 的规则 | 同一 X=-0.25 的结果 |
| --- | --- | --- | ---: |
| `review-rule-v1` | 2026-09-01 00:00 | `recent_diff <= -0.30` 时为 1，否则为 0 | 0 |
| `review-rule-v2` | 2026-09-15 00:00 | `recent_diff <= -0.20` 时为 1，否则为 0 | 1 |

两套规则都包含等号。X 不满足 `-0.25 <= -0.30`，但满足 `-0.25 <= -0.20`。因此从 0 变为 1 是因为**定义改变**，而不是观测恶化。这一判断可以直接按规则计算，并非一定需要模型来复现。

[P3-9.8](section-08.zh.md)改变模型分数阈值，是在固定结果定义下改变安排策略。本节改变的则是生成 `review_needed` 本身的规则。若把该列作为训练答案，答案定义就改变了；`final_status` 的检查定义并没有随之改变。

## 区分生效日期与历史资料重新判定

本例约定，新标准适用于生效后作出的新判断。X 在 9 月 10 日的原始判断保留为 `review-rule-v1`、结果 0。如果 9 月 16 日用新标准重新判定旧 X，应新增 `review-rule-v2`、结果 1 的记录并关联原记录，不覆盖历史观测时刻或原始判断。

| 重新判定前要检查的内容 | 本例应保留的记录 |
| --- | --- |
| 原始标准与判定时刻 | X 原记录 ID、9 月 10 日判定、`review-rule-v1`、值 0 |
| 新标准适用范围 | `review-rule-v2` 适用于 9 月 15 日 00 时之后的新判断；历史重新判定单独记录 |
| 可重新判定的依据 | 能否用相同原始资料、单位、聚合和基线确认 `recent_diff=-0.25`？ |
| 新判断与负责人 | 9 月 16 日、`review-rule-v2`、值 1；在实际记录中填写负责人及修改理由 |
| 合并训练资料时的选择 | 使用按同一定义重新判定的资料，或按版本分开；注明无法重新判定的记录范围及原因 |

如果只剩旧标签 0，没有原始 `recent_diff` 或计算依据，就无法确认新标签。旧标准下的 0 既包括新标准下变成 1 的 -0.25，也包括仍为 0 的 -0.10。不能只改版本名就当作定义已经统一。同一观测的两次判断，也不应扩充为两个独立样本。

## 整理候选目标与判断标准版本 {#_2}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-11-mermaid-01-zh.mmd"
```

确定每个结果的定义及确认状态后，再检查版本差异。标准改变时，应先确认改变了什么，以及能否用同样依据重新判定。这样，当月度标签 1 的比例变化时，才能分别检查观测变化和定义变更。

练习：① `recent_diff=-0.30` 和 `-0.20` 在各版本中分别是什么标签？② 若只保留 X 的旧结果 0，能否将 v2 结果改为 1？③ A 的最终状态尚未确认，能否用 `review_needed=1` 替代最终状态答案？

解答：① -0.30 在 v1、v2 中都为 1；-0.20 在 v1 中为 0、v2 中为 1。② 缺少原始观测及依据就不能确认；只有能确认本例 X=-0.25 时，才能计算新规则结果 1。③ 两列回答不同问题，不能替代。A 应保留 `final_status=?`、`label_status=pending`，这与 [P3-9.10](section-10.zh.md) 的未确认处理一致。

## 检查清单

- 能否说明本次代表目标的选择理由，以及其他候选回答的问题？
- 能否通过计算说明 X 的 0→1 来自定义变更，而非观测变化？
- 能否保留生效日期、原判断、重新判定依据及历史，而不是直接合并不同版本的标签？

## 来源与参考资料

- Google, *Machine Learning Glossary*, `label`, `proxy labels`。用于确认术语依据：标签是监督学习样本的答案或结果部分，而 proxy label 是在数据集中无法直接取得标签时用来近似实际标签的数据。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*。用于确认 provenance 视角下应保留处理步骤、可复现性、版本管理和派生关系。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
