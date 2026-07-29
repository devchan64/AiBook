<a id="tokenization"></a>
<a id="glossary-tokenization"></a>

### token 化(tokenization)

- 含义：token 化把原始文本转换成模型可以处理的 token 序列。人看到的一整句话，在模型那里会变成按顺序排列的 token 片段。
- 为什么重要：token 化会影响 token 数、成本、上下文占用、切块边界和输入解释。在 P3-6.2 中，这个想法被类比用于区段 token：把原始曲线改写成更短的序列，从而比较顺序和方向。
- 相关概念：`词元(token)`, `上下文窗口(context window)`, `字节对编码(BPE, Byte Pair Encoding)`
- 核心 Section：`P6-2.2`
- 出现 Section：`P3-6.2`，`P6-2.2`，`P6-2.3`，`P6-2.4`，`P6-2.5`，`P7-4.1`，`P7-4.2`
