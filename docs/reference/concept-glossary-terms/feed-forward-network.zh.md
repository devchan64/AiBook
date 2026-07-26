<a id="feed-forward-network"></a>

## 前馈网络

- 含义: 前馈网络让输入沿层向前流动，没有循环反馈。在 Transformer block 中，它通常指 attention 之后按位置重新加工表示的小网络。
- 为什么重要: 它把“读取 token 之间的关系”和“重新加工每个位置的表示”分开。这个概念也帮助读者区分前向层结构和循环结构。
- 相关概念: `Transformer`, `self-attention`, `layer normalization`
- 核心 Section: `P5-14.6`
- 出现 Section: `P5-14.1`, `P5-14.2`, `P6-4.1`
