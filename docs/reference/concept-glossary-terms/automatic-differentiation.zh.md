<a id="automatic-differentiation"></a>

## 自动微分(automatic differentiation)

- 含义: 自动微分是一种让程序记录计算步骤，并利用这些记录自动计算导数的方法。它不是让人手动展开一个大公式，而是沿着实际执行过的运算来组织梯度。
- 为什么重要: 它是深度学习框架执行反向传播的实际基础。理解自动微分之后，就能看出梯度是如何通过计算路径、中间值和局部求导规则被组织起来的。
- 相关概念: `计算图(computation graph)`, `反向传播(backpropagation)`, `梯度(gradient)`
- 核心 Section: `P5-5.2`
