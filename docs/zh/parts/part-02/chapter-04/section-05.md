# P2-4.5 梯度补充学习：从高中微分到多变量微分

> Section ID: `P2-4.5`
> Version: `v2026.07.09`

P2-4.3 把导数、偏导数、梯度接起来了，P2-4.4 又把它们连到学习。这里补上最容易卡住的过渡地带。

## 本补充节范围

这不是梯度或梯度下降的代表性主说明，而是帮助读者跨过“单变量微分 -> 多变量学习”之间的陌生感。

## 常见断点

| 高中记忆 | 为什么会在这里卡住 | 现在重新抓住的表达 |
| --- | --- | --- |
| `y = f(x)` 单变量函数 | 输入一多，问题就不止一个 | 多变量函数 |
| 一个斜率 | 损失会同时对多个参数有反应 | 多个偏导数组成的集合 |
| 切线斜率 | 很少区分坐标轴方向与任意方向 | 偏导数、方向导数 |
| 微分做题 | 学习更关心往哪边移动 | 梯度、梯度下降 |
| 解一道题 | 深度学习需要高效算很多梯度 | 反向传播 |

![从一个导数扩展到多个偏导与梯度](../../../assets/part-02/chapter-04/gradient-single-to-multiple-directions-en.svg)

![偏导数与方向导数比较](../../../assets/part-02/chapter-04/partial-vs-directional-derivative-en.svg)

![梯度在向量分析中的位置](../../../assets/part-02/chapter-04/vector-calculus-context-en.svg)

![损失等高线上的梯度方向](../../../assets/part-02/chapter-04/gradient-direction-loss-contour-en.svg)

![梯度下降的小步下山过程](../../../assets/part-02/chapter-04/gradient-descent-steps-en.svg)

![梯度下降更新直觉](../../../assets/part-02/chapter-04/gradient-descent-update-intuition-en.svg)

![反向传播里的前向与反向流](../../../assets/part-02/chapter-04/backpropagation-gradient-flow-en.svg)

## 记住的视角

- 梯度、梯度下降、反向传播彼此相关，但不是同一个东西。
- 这里的陌生感通常不是“全新数学”，而是“单变量直觉被扩展到多个方向”。
- 这一节先分清角色，比一次掌握所有公式更重要。

## 简短检查

- 能说明单变量图景怎样扩展到多输入。
- 能区分梯度、梯度下降、反向传播。
- 能说明方向导数为什么不等于偏导数。

## 来源与参考资料

- OpenStax, [Calculus Volume 3](https://openstax.org/details/books/calculus-volume-3){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
