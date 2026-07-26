<a id="weighted-sum"></a>

## 加权和(weighted sum)

- 含义：加权和是把每个输入分别乘上自己的权重，再把结果加成一个值的计算。例如 \(x_1w_1 + x_2w_2\) 会用不同强度反映两个输入，并把它们折成一个分数。
- 为什么重要：感知机、线性层、矩阵乘法、attention 分数等很多 AI 模型内部计算都会反复使用这种结构。这个概念能帮助读者看清：权重不只是拿来相乘的数字，而是控制某个输入被反映得多强的值。
- 相关概念：`权重(weight)`, `线性组合(linear combination)`, `矩阵乘法(matrix multiplication)`, `感知机(perceptron)`
- 中心 Section：`P2-3.3`
- 出现 Section：`P5-1.1`, `P5-1.2`
