# P2-12.3 准备学习数据集的直觉

> Section ID: `P2-12.3`
> Version: `v2026.07.09`

P2-12.3 把“读表”进一步连到模型准备语言：`X`、`y`、sample、feature、train/validation/test 划分，以及“会学到规则的变换只从 train 学”这一原则。

## 本节范围

本节聚焦入门级数据集准备逻辑，而不是完整预处理流水线。

## 中心问题

我们怎样把一张表重新组织成 `X` 与 `y`，同时不把标识列、答案列、训练阶段规则混在一起？

## 记住的视角

- 表不会原样送进模型，而是要按学习问题重新组织。
- `X` 与 `y` 必须清楚分开。
- 标识列与答案列不能被当成普通特征直接留下。
- 先划分，再只在 train 上学习规则，才能避免评估泄漏。

## 简短检查

- 能说明为什么在训练前先拆成 `X` 与 `y`。
- 能说明为什么 ID 列与标签列不能直接留在特征列里。
- 能说明为什么 train/validation/test 的顺序会影响评估可信度。

## 来源与参考资料

- scikit-learn, [Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
- scikit-learn, [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
