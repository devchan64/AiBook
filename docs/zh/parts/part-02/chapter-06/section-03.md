# P2-6.3 梯度下降的直觉

> Section ID: `P2-6.3`
> Version: `v2026.07.09`

P2-6.1 把最优化引入成候选搜索，P2-6.2 又把错误变成了损失。下一步问题就变得很具体：当我们已经有了一个想要减小的数字，模型参数到底怎样移动？

## 本节范围

本节用直觉方式介绍 `gradient descent`、`gradient`、`learning rate`、`update`、`iteration`，不完整推导更新公式或各类优化器。

## 中心问题

为什么学习不是一步跳到答案，而是从当前位置一点点移动？

## 先固定的术语

| 术语 | 很短的意思 | 本节中的作用 |
| --- | --- | --- |
| gradient descent | 朝更低损失重复移动的方法 | 本节核心方法 |
| gradient | 损失上升的局部方向信息 | 移动方向线索 |
| learning rate | 每次移动的步长 | 步幅大小 |
| update | 用新参数替换旧参数 | 一次移动结果 |
| iteration | 重复同一调整循环 | 让学习变成过程 |

![梯度下降在损失曲线上逐步降低损失](../../../assets/part-02/chapter-06/gradient-descent-loss-curve-en.svg)

## 记住的视角

- 梯度下降是重复的局部调整，不是一次到位。
- 梯度给出上坡方向，所以要往反方向走。
- 学习率决定每一步走多大。

## 简短检查

- 能说明为什么梯度下降是重复方法。
- 能说明为什么移动方向与梯度相反。
- 能把学习率解释成步长。
- 能说明为什么方向对了但步子不合适也会出问题。

## 来源与参考资料

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
