<a id="cross-entropy"></a>

## 交叉熵(cross-entropy)

- 含义: 交叉熵是一种概率型损失。模型给正确答案的概率越低，损失就越大。它常用于分类任务和下一 token 预测。
- 为什么重要: 它不只看排第一的答案是否正确，还会看模型到底给正确候选分配了多少概率。这个概念能把分类损失、softmax 输出和 LLM 的 next-token loss 连到同一条线索上。
- 相关概念: `损失函数(loss function)`, `softmax`, `对数损失(log loss)`, `下一 token 预测(next-token prediction)`
- 核心 Section: `P5-4.2`
- 出现 Section: `P5-4.1`
