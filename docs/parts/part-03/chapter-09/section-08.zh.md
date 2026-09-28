# P3-9.8 预测分数通过什么规则转化为行动

> Section ID: `P3-9.8`
> Version: `v2026.09.20`

[P3-9.7](section-07.zh.md)区分了预测时可用的输入和之后的结果。模型给出[分数](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-score)后，仍需另外决定实际复核谁。分数是模型输出，[策略规则](/AiBook/zh/reference/concept-glossary-pinyin/y/#decision)则是将输出转化为行动的标准。

## 写明分数来源与一次预测的对象

以下是**本节给定的虚构模型输出**。它们不是实际训练或运行模型得到的结果，也不同于前面按比较差值或安全条件手工规定顺序的队列。假设本例模型预测一次已完成的动作是否需要额外复核。`review_score` 是用于该判断的分数，越高越优先考虑复核。

A～D 是本节内部的动作 ID。假设同一个虚构模型 `demo-model-v1` 在各动作完成时给出分数，D 在本次复核批次确定前加入。A～C 的分数不重新计算。行动单位也固定为对一次动作安排复核。

| event_id | 给定的 `review_score` | 进入候选批次的顺序 |
| --- | ---: | --- |
| A | 0.82 | 初始批次 |
| B | 0.80 | 初始批次 |
| C | 0.79 | 初始批次 |
| D | 0.95 | 安排确定前加入 |

不能仅因分数在 0～1 之间就认定它是故障概率或需要复核的概率。本节只使用分数顺序并应用策略。实际复核结果尚未给出，因此不能将被选动作视为实际阳性，也不能将未选动作改成已确认正常。

## 阈值与前两名是不同规则

今天最多能复核两项。先比较尚未施加容量限制的达标情况与按排名选择的结果。这里**“不低于 0.80”指 `score >= 0.80`**，包含恰好 0.80。分数相同时，按 `event_id` 的字母升序处理。这是本教学策略的约定，不是所有工具共同的默认行为。

| 比较的策略 | 只有 A、B、C 时 | D 加入后 |
| --- | --- | --- |
| 阈值：所有分数不低于 0.80 的候选 | A、B，共 2 项 | D、A、B，共 3 项 |
| 前两名：分数降序，同分按 ID 升序 | A、B，共 2 项 | D、A，共 2 项 |

阈值一行列出的是达标名单，不是今天两个名额的最终安排。D 加入后，B 的分数和达标状态都没变，变化的是它在候选中的排名。反过来，只取前两名的规则没有最低分数要求，所以即使所有分数都很低，也可能选出最多两项。

## 将达标情况与今天的安排状态分开

把同时使用两种约束的策略命名为 `threshold-capacity-v1`。先保留分数不低于 0.80 的候选，再在其中按分数降序、同分 ID 升序安排最多两项今天复核。不用未达标候选填补空位。

| event_id | 分数 | `meets_threshold` | `selected_today` | 策略确定的安排状态 |
| --- | ---: | ---: | ---: | --- |
| D | 0.95 | 1 | 1 | 安排今天复核 |
| A | 0.82 | 1 | 1 | 安排今天复核 |
| B | 0.80 | 1 | 0 | 达标，因容量不足等待 |
| C | 0.79 | 0 | 0 | 未达标，不纳入本次安排 |

B、C 都是 `selected_today=0`，但原因不同。B 因容量限制等待，C 不满足当前阈值。两者都不是复核结果，也不表示是否发生故障。同样，`selected_today=1` 只表示安排复核，不表示负责人已经完成复核。实际执行情况应通过单独的完成记录确认。

## 从分数到阈值与运行策略 {#_1}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-8-mermaid-01-zh.mmd"
```

图中展示了对包含 D 的候选批次应用 `threshold-capacity-v1` 的结果。为了对相同批次和策略复现同一安排，应保留模型版本、预测对象和时刻、分数、候选清单、阈值、容量、同分规则及策略版本。B 的 0.80 与等待原因一起保留，才能区分模型输出和安排决定。

## 改变边界与容量后作出判断

练习：保持包含 D 的四个候选不变。① 只把容量增至三项，B、C 会怎样？② 容量为两项时把阈值提高到 0.83，要用 A 填补空位吗？③ 另设一种情况：加入分数为 0.82 的 E，阈值 0.80、容量两项，应安排谁？

解答：① 安排 D、A、B，C 仍未达标。② 只有 D 达标，因此只安排一项，不用 A 填补空位。此时 B 未被选中的原因也从容量等待变为未达标。③ D 之后 A、E 同分，但 ID 升序使 A 在前，因此安排 D、A；E、B 都是达标但等待的候选。ID 规则是复现顺序的约定，不是 A 比 E 更危险的证据。

在改变策略的过程中，原有候选的模型分数保持不变。阈值或容量改变后选择结果不同，并不能说明模型更准确。选择错误的成本将在 [P3-9.12](section-12.zh.md) 中继续讨论。

## 检查清单

- 能否说明虚构模型分数的来源，以及预测和行动的单位？
- 能否区分 B 的 0.80 达标的原因，与 D 加入后 B 等待的原因？
- 能否依照规则处理同分、空位和未达标情况，并区分安排复核与完成复核？

## 来源与参考资料

- Google, *Thresholds and the confusion matrix*。用于确认：要把模型的原始数值输出转换成类别，需要选择分类阈值；阈值不同，预测结果也可能不同。 [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-09-20
- Google, *Classification: ROC and AUC*。用于确认：AUC 与把正例排在负例之前的能力相关，而实际分类取决于所选择的阈值。 [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Google, *Machine Learning Glossary*, `classification threshold`, `AUC`。用于确认分类阈值和 AUC 的术语依据。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
