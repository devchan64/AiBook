# P3-9.13 交给 Part 4 之前的问题边界

> Section ID: `P3-9.13`
> Version: `v2026.09.20`

交给 Part 4 的不只是一张输入表，还应包括预测什么、何时预测、在哪些对象上验证性能，以及哪些条件尚未核实。[评估设计](/AiBook/zh/reference/concept-glossary-pinyin/p/#evaluation-design)就是依照这个问题划分学习与评估资料，并比较结果。

## 预测现有设备未来故障的交接备忘录

以下是延续 [P3-9.7](section-07.zh.md) 设备案例的**教学交接草案**，不表示真实原始记录或训练、评估结果已准备完毕。本次问题固定为“能否预测已经观察过的设备在之后七天内的故障”。

| 交接项目 | 本例的约定 |
| --- | --- |
| 目的与评估对象 | 预测现有设备的未来故障；对新设备性能的主张需要另行评估 |
| 一个样本 | `equipment_id` 与 `cutoff_at` 的组合；同一设备的不同预测时点是不同的行 |
| 预测时点示例 | M-01 的 `2026-09-01 10:00 KST` |
| 输入示例 | 09:55 前完成动作的近期均值 2.20 L/min、历史已确认基线 `base-v1` 均值 2.52 L/min、`recent_diff=-0.32 L/min`；该特征在 09:58 可用 |
| 输入依据 | 保留原始 ID、到达时刻、测量条件、聚合范围、基线版本、计算完成时刻；排除 10:02 到达测量与后来重算的基线 |
| 结果定义与窗口 | `failure_within_7d`、`failure-v1`；包含 9 月 1 日 10:00，不包含 9 月 8 日 10:00 |
| 标签确认条件 | 确认期间内发生故障则为 1；完整追踪并核实记录后确认没有故障则为 0；未确认单独保留状态 |
| 训练资料截止 | 假设在 8 月 31 日 18:00 KST 固定训练资料；只有输入、答案及版本依据当时可用的行才是候选 |
| 评估资料 | 训练资料固定之后，从 9 月 1 日 10 时开始的预测行；后续答案稍后关联，不能提前把最终评估答案用于模型或策略选择 |
| 输出与行动 | 故障分数及单独的复核安排策略；不能仅凭分数主张概率或干预效果 |
| 基准比较 | 在相同评估行上与全部判为 0 的简单基准比较；故障稀少时不能只满足于高准确率 |
| 尚未确认的事项 | 实际可用时刻、基线原始资料、设备及故障数量、追踪遗漏、干预历史、实际错误成本和复核容量 |

`failure-v1` 表示设备自身异常导致计划动作未能完成，并在维修记录中确认原因，排除计划停机。一个带输入数值的示例行不等于充足的训练数据。未确认事项需要查阅实际原始记录后补齐，不能把缺少依据的行作为已验证资料交接。

## 过去日期的行，也可能因答案迟到而不能用于训练

以 8 月 31 日 18 时的训练资料截止为准，比较两个候选。下列日期均为 2026 年 KST，并假设各输入在相应预测时点已经可用。

| 候选行预测时点 | 七天结果窗口终点（不包含） | 结果确认 | 本次训练是否可选 |
| --- | --- | --- | --- |
| 8 月 20 日 10:00 | 8 月 27 日 10:00 | 完整追踪后于 8 月 28 日 12:00 确认为 0 | 可以，但还需检查其他质量条件 |
| 8 月 28 日 10:00 | 9 月 4 日 10:00 | 8 月 31 日 18 时仍在观察，尚无确认故障 | 排除，当时没有确认答案 |

如果在 9 月得到第二行的答案后倒填进过去的训练，就会评估一个在 9 月 1 日无法实际运行的模型。反过来，最终评估行的答案在预测之后收集，本来就是正常的。关键区别是何时把结果用于学习或策略选择。这正是 [P3-9.10](section-10.zh.md) 需要确认状态和时刻的原因。

还要检查重叠输入窗口：是否随机拆行后把共享原记录、几乎相同的样本放到了两边，基线或变换计算是否混入未来资料。预测现有设备的未来时再次使用过去观测，并不总是泄漏。应依据实际可用时间与评估问题，检查重复和依赖关系。

## 评估新设备时，分离条件也不同

| 要验证的性能 | 时间与实体划分原则 |
| --- | --- |
| 现有设备的未来 | 同一设备可以出现在训练与评估中，但用过去资料评估之后的预测；这是本备忘录的选择 |
| 训练中没有的设备 | 训练与评估之间分离设备 ID；已知设备的重复行不能证明新设备性能 |
| 未来进入的新设备 | 同时应用设备 ID 分离和时间先后顺序 |

实体分离把一台设备的全部相关行作为一组。仅从输入中删除设备 ID，并不会让这些行变得独立。如果实际运行是预测未来，那么评估新设备时也要检查时间和输入可用性。划分应从“将应用到哪里”出发，而非只按存储行数的比例。

## 写明指标数什么，而不只写名称

| 评估备注 | 实际计数内容及局限 |
| --- | --- |
| 故障捕捉比例 | 确认故障样本中判为 1 的数量 / 全部确认故障样本数；检查少漏掉了多少，故障样本为零时无法计算比例 |
| 多余候选与处理量 | 分别记录实际 0 但判为 1 的数量，以及全部候选数；区分误报负担和处理容量 |
| 策略成本比较 | 在相同评估行上计算漏报数×漏报成本＋误报数×误报成本；实际成本假设和容量仍未确认 |
| 答案确认范围 | 在全部评估行中分别报告已确认、未确认数量；不能把确认子集的结果直接认定为整体性能 |

这里的计数单位是设备与预测时点组成的样本。多个预测行可能对应同一次实际故障，因此不能把捕捉样本数当成不同故障事件数。比较基准与模型时，期间、设备清单和策略必须一致。

如果目的是今天只复核前几项，就应围绕排名与选中候选的结果重新设计评估。结果若为状态类别，可能是多类别预测；若为数值，可能是连续值预测。做成一张表不等于必须进行 0/1 分类。本备忘录选择的是七天内故障与否。

## 移交前确认时间、实体与信息边界 {#_1}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-13-mermaid-01-zh.mmd"
```

练习：将 M-01 的 8 月和 9 月行按时间分开评估。① 能否据此说“在第一次见到的设备上也预测得很好”？② 能否把 8 月 28 日行尚未确认的答案填为 0 并加入训练？

解答：① 这是同一设备的未来评估，不足以证明新设备性能；若目标是新设备，需要获得与训练设备 ID 不重叠的评估对象。② 当时没有答案，应排除并保留未确认状态及排除原因。实际划分实现、模型选择与调参，将在 Part 4 中依据本备忘录的问题、约束及待解决事项展开。

## 检查清单

- 能否选择现有设备的未来或新设备作为评估对象，并解释对应边界？
- 能否区分输入截止、训练资料截止、结果窗口和确认时刻？
- 能否写出明确计数单位、未确认范围及待查记录的交接备忘录？

## 来源与参考资料

- Google, *Machine Learning Glossary*, `label leakage`。用于确认信息边界依据：预测时点之后的信息如果混入特征，就可能成为标签代理。确认日: 2026-07-20. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Classification: ROC and AUC*。用于确认 ranking/evaluation design 依据：AUC 和 ROC 关注把正例排在负例之前的能力，并且不同于具体 threshold 的选择。确认日: 2026-07-20. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*。用于确认 provenance 视角下记录处理步骤、可复现性、版本管理和派生关系的依据。确认日: 2026-07-20. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
- Hyndman, Athanasopoulos, *Forecasting: Principles and Practice (3rd ed.)*, Section 5.10 Time series cross-validation. 用于确认 time split 依据：在有时间顺序的问题里，训练集只应包含早于测试观测值的观测值，不能用未来观测值构造 forecast。确认日: 2026-09-20. [https://otexts.com/fpp3/tscv.html](https://otexts.com/fpp3/tscv.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, *Cross-validation: evaluating estimator performance*, cross-validation iterators for grouped data. 用于确认 group split 依据：当组内依赖重要时，同一 group 的样本不应同时出现在配对的训练侧和验证/测试侧。确认日: 2026-09-20. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" }
