<a id="vocabulary"></a>

## vocabulary

- 含义：tokenizer vocabulary 是 tokenizer 能生成的 token 片段，以及这些片段对应 ID 的内部列表。这里的 vocabulary 不是人使用的词典，而是模型输入片段的计算用查询表。
- 为什么重要：同一个原始字符串会因为 vocabulary 和切分规则不同，变成不同的 token 片段、token 数和 token ID。这个概念能帮助读者把 token ID 看成 vocabulary 项目编号，而不是词义说明；也能解释 tokenizer 选择为什么会影响成本和上下文长度。
- 相关概念：`token`，`tokenization`，`token ID`，`embedding`
- 核心 Section：`P6-2.2`
- 出现 Section：`P6-2.2`，`P6-2.5`，`P7-4.1`
