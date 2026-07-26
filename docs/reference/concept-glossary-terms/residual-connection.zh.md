<a id="residual-connection"></a>

## 残差连接

- 含义：残差连接会把原始输入表示和新计算结果一起传给下一层。也就是说，每一层不会完全覆盖前一层表示，而是保留一条让原始信息继续流动的路径。
- 为什么重要：深层神经网络反复改写表示时，信息流和训练过程可能变得不稳定。残差连接帮助 Transformer block 在多层堆叠时保留原始表示，使学习和信息传递更稳定。核心直觉是：`加入新计算，但不切断原来的路径`。
- 相关概念：`Transformer`，`layer normalization`，`feed-forward network`
- 中心 Section：`P5-14.7`
- 出现 Section：`P5-14.1`, `P5-14.2`
