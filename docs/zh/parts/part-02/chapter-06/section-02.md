# P2-6.2 损失函数与目标函数

> Section ID: `P2-6.2`
> Version: `v2026.07.09`

P2-6.1 把最优化看成候选比较。这里继续问：在模型学习里，这个比较标准到底叫什么？

## 本节范围

本节入门介绍 `loss function`、`objective function`、`error`、`mean loss`、`metric`。

## 中心问题

模型“错了”这件事，怎样被变成学习真正能推动的数字标准？

## 先固定的术语

| 术语 | 很短的意思 | 本节中的作用 |
| --- | --- | --- |
| loss function | 把错误变成数字的函数 | 学习标准入口 |
| objective function | 训练真正要优化的整体标准 | 最优化目标 |
| error | 预测与真实值之间的差 | 许多损失的原料 |
| mean loss | 多个样本损失的汇总 | 整体趋势 |
| metric | 给人解释和比较的指标 | 不能自动等同于损失 |

## 记住的视角

- 损失把“错得多严重”变成一个数值信号。
- 目标函数是训练真正要优化的更大标准。
- metric 与 loss 应该区分，而不是默认相同。

## 简短检查

- 能把损失函数解释成把错误数值化的方法。
- 能说明单样本损失与平均损失的区别。
- 能说明为什么汇报用指标不一定等于训练损失。

## 来源与参考资料

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
