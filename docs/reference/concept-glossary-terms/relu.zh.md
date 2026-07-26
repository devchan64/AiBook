## ReLU(rectified linear unit)

- 含义: ReLU 是一种激活函数。输入为负时会被切成 0，输入大于等于 0 时则几乎原样通过。它通常写成 \(f(z)=\max(0,z)\)。
- 为什么重要: ReLU 是现代深度学习中常见的基本激活函数。它和 sigmoid、tanh 不同，在正值区间不会饱和，因此是理解隐藏层信号如何保留下来的重要比较基准。
- 相关概念: `激活函数(activation function)`, `sigmoid`, `tanh`, `隐藏层(hidden layer)`
- 核心 Section: `P5-3.4`
- 出现 Section: `P5-3.5`
