# P3-9.7 如何区分预测时可用的输入与之后的结果

> Section ID: `P3-9.7`
> Version: `v2026.09.20`

[P3-9.6](section-06.zh.md)检查了标签含义和判断条件。现在需要用结果揭晓前实际可用的信息构造输入。[预测契约](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-prediction-contract)共同约定预测对象、输入的构造时点与规则，以及要预测的结果定义。不仅要看列名，还要核实每个值何时变得可用。

## 用 10 时的输入预测之后七天

下面用虚构设备说明时间边界。一次预测针对 `equipment_id=M-01` 在 `2026-09-01 10:00` 的状态，所有时间均采用韩国标准时间（KST）。即使是同一设备，预测时点不同也视为不同样本。

| 项目 | 本例的值与定义 |
| --- | --- |
| 输入截止时间 `cutoff_at` | 2026-09-01 10:00。只使用截至此时系统实际可读取的信息 |
| 预测跨度 `horizon_days` | 7 天 |
| 结果窗口 | 2026-09-01 10:00 及之后，2026-09-08 10:00 之前。包含起点、不包含终点 |
| 目标 `failure_within_7d` | 确认设备在该窗口内发生故障则为 1；检查完整窗口且没有故障则为 0 |
| 尚未确认的结果 | 保留为未确认。未复核或观察未完成不能填成 0 |

本例将故障定义为“设备自身异常导致计划动作未能完成，并且原因已在维修记录中确认”。排除计划停机，将该定义记为 `failure-v1`。下文的数值和 ID 用于说明，不代表真实设备风险。

## 过去测量的值也可能到达太晚

[特征](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)是提供给模型的输入值。这里的 `recent_diff` 是相同测量条件下近期平均流量减去基线平均流量。近期均值 2.20 L/min、基线均值 2.52 L/min 得到 `2.20 − 2.52 = −0.32 L/min`。

| 信息或计算 | 发生或覆盖时间 | 实际可用时间 | 是否作为 9 月 1 日 10 时输入 |
| --- | --- | --- | --- |
| `base-v1` 基线 2.52 | 截至 8 月 31 日 17:00 的已确认资料 | 8 月 31 日 18:00 | 可用。保留当时确认的资料及计算版本 |
| 近期均值 2.20 与 `recent_diff=-0.32` | 9 月 1 日 09:55 前完成的动作 | 9 月 1 日 09:58 | 可用。假设原始记录此时也已到达并核实 |
| 新增传感器测量 | 9 月 1 日 09:59 测量 | 9 月 1 日 10:02 到达 | 排除。虽已发生，但在截止后才到达 |
| 后来重新计算的 `recent_diff` | 基线纳入了截至 9 月 2 日 17:00 的记录 | 9 月 2 日 18:00 | 排除。计算材料包含未来资料 |
| `review_result` | 9 月 1 日 10:20 完成复核 | 9 月 1 日 10:21 记录 | 排除。判断产生于预测之后 |
| `failure_within_7d=1` | 9 月 3 日 14:00 故障，经维修确认 | 本例在 9 月 8 日 10:10 写入结果表 | 关联为训练结果；排除在 9 月 1 日输入之外 |

`feature_available_at` 表示系统实际能够使用该特征值的时刻。除了原始数据到达，还需要完成必要的计算。即使都叫 `recent_diff`，9 月 1 日确定的值与使用 9 月 2 日资料重算的值也不同。事后创建的表即使标上过去的日期，也不会变成当时的输入。

## 把之后的结果作为输入，相当于提前给出答案

构造模型时使用预测时不可得的信息，就是[数据泄漏](/AiBook/zh/reference/concept-glossary-pinyin/d/#glossary-data-leakage)。把后来确认的结果关联为训练答案是必要的，但若又把它放入同一样本的输入，就提供了未来信息。

| 单独的教学样本 | 窗口结束后确认的 `failure_within_7d` | 复制该结果的 `result_code` | 直接复制 `result_code` 作为答案 |
| --- | ---: | ---: | ---: |
| E | 1 | 1 | 1 |
| F | 0 | 0 | 0 |

这两行因为直接复制答案而得到 `2 / 2 = 100%`。这不是对模型未来预测能力的检验。案例用于说明泄漏，不表示泄漏总会使分数提高同样幅度。无论分数高低，都应先检查输入在预测时是否可用。

`review_result=skipped` 也不代表没有故障或正常运行。它表示跳过复核的处理状态。如果任务需要之后的故障结果，就必须另外寻找观察和确认记录。

## 在预测时点区分可用输入与后续结果 {#_3}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-7-mermaid-01-zh.mmd"
```

箭头表示时间先后和记录关联，并不按比例表示时间间隔。09:59 的测量虽然发生在 10 时截止之前，但 10:02 才到达，因此不能纳入当时的输入。事后构造训练表时，也应重建截止时实际可用的输入，将结果关联为单独的列。

## 向 Part 4 交接一行数据时需要的依据

| 交接字段 | 本例应保留的内容 |
| --- | --- |
| 样本标识 | `equipment_id=M-01` + `cutoff_at=2026-09-01 10:00 KST` |
| 输入及可用时间 | `recent_diff=-0.32 L/min`，`feature_available_at=2026-09-01 09:58 KST` |
| 计算依据 | 近期均值 2.20、`base-v1` 均值 2.52、原始记录 ID 列表、覆盖期间、聚合规则 |
| 结果边界 | `target_window_start=2026-09-01 10:00 KST`，`target_window_end=2026-09-08 10:00 KST`，`horizon_days=7`，包含起点、不包含终点 |
| 结果及依据 | `failure-v1`、`failure_within_7d=1`、故障及维修记录 ID，9 月 8 日 10:10 写入结果表 |
| `leakage_check_note` | 从输入中排除 10:02 到达的测量、未来基线重算值及复核后结果 |

实际交接时必须填写具体的原始记录、故障及维修记录 ID。这里仅列出需要关联的记录类型，因此该表本身不是已完成训练准备的真实数据。若有多个特征，要分别检查各特征的可用时刻。

练习：① 如果 09:59 测量提前到 09:59:30 到达，能否纳入均值？② 能否用 9 月 2 日基线重算的值覆盖 9 月 1 日的行？③ 能否把未复核状态改成结果 0？

解答：① 到达提前不等于自动纳入。本例的均值覆盖 09:55 前完成的动作，要先检查是否属于聚合范围。若改变输入定义，还必须在 10 时前完成原始数据核实与特征计算，并能在实际运行中复现同一规则。② 不能，因为会引入未来信息。应保留当时的基线及输入版本。③ 不能，未复核意味着结果尚未确认，不等于 0。

无论采用一行特征向量还是保留时间顺序的输入序列，都适用这些时间边界。交给 Part 4 的应包括输入值、结果及重建当时输入所需的依据。训练与评估划分将衔接 [P3-9.13](section-13.zh.md) 的交接项目。

## 检查清单

- 能否写明七天的起止时刻及端点是否包含，并区分输入时刻与结果观察期间？
- 能否解释为何应从输入中排除 09:59 测量但 10:02 才到达的值、未来基线重算值及复核后结果？
- 能否用当时的资料和版本重建输入，并区分未复核状态与结果 0？

## 来源与参考资料

- Google, *Machine Learning Glossary*, `feature`, `label`, `label leakage`。用于确认术语依据：特征是模型的输入变量，而标签泄漏是把标签的代理值混入特征中的设计缺陷。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Google, *Datasets: Dividing the original dataset*。用于确认训练/验证/测试数据应分离、相同特征变换也应应用到真实运营数据、验证/测试数据应贴近模型会遇到的真实数据这一观点。 [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*。用于确认 provenance 视角下应保留处理步骤、可复现性、版本管理和派生关系。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20

- [scikit-learn, Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }. 用于核实预测时不可用信息的泄漏，以及训练和运行中的一致输入变换。确认日：2026-09-20。
