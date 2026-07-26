<a id="linear-combination"></a>

## 线性组合(linear combination)

- 含义：线性组合是把多个值或向量分别乘上标量权重后再相加的计算。在感知机里，它常表现为 \(w_1x_1 + w_2x_2 + b\) 这样的中间分数。
- 为什么重要：矩阵乘法、线性层以及神经网络在激活前形成的第一个分数，都反复使用这种结构。理解它以后，读者就能把`乘一下再加起来`读成从输入形成新表示或判断分数的基本方式。
- 相关概念：`加权和(weighted sum)`, `标量乘法(scalar multiplication)`, `向量加法(vector addition)`, `激活函数(activation function)`
- 中心 Section：`P2-3.2`
- 出现 Section：`P5-1.2`
