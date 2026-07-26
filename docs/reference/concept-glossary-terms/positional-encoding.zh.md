<a id="positional-encoding"></a>

## 位置编码(positional encoding)

- 含义：位置编码是在 token 自身含义向量之外，告诉模型该 token 位于序列哪个位置的信息。它让模型能够区分同一个词出现在句首、句中还是句尾。
- 为什么重要：位置编码是让 Transformer 在没有顺序 recurrence 的情况下也能反映词序的基本装置。即使 self-attention 能很好地比较 token，如果没有单独供应位置信息，模型也很难稳定地区分 `谁先出现`。这个概念把 `这是什么 token` 和 `它放在哪里` 连接起来。
- 相关概念：`Transformer`，`self-attention`，`token`
- 核心 Section：`P1-11.3`
- 出现 Section：`P6-4.3`
