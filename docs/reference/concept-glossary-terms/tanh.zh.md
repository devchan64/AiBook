## tanh

- 含义: tanh 是一种以 0 为中心的 S 形函数，会把输入分数压缩到 -1 与 1 之间。负输入会保留成负输出，正输入会保留成正输出，而 0 会对应到 0。
- 为什么重要: 它提供了和 sigmoid 的直接对比。两者都会压缩数值，但 tanh 会围绕 0 保留方向，因此适合说明隐藏层表征怎样携带带符号的信号。
- 相关概念: `激活函数(activation function)`, `sigmoid`, `ReLU`, `隐藏层(hidden layer)`
- 核心 Section: `P5-3.3`
- 出现 Section: `P5-3.5`
