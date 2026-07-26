## SentencePiece

- 含义：SentencePiece 是一种 tokenizer 家族，它不预设空白已经是固定单词边界，而是从包含空白标记的原始字符串本身学习并应用 subword 片段。
- 为什么重要：在语言、数字、符号混合的输入中，只靠空白很难稳定决定计算片段。理解 SentencePiece 后，读者能把 tokenizer 家族差异读成是否以及怎样处理包含空白在内的整个字符串。
- 相关概念：`tokenization`，`Byte Pair Encoding`，`WordPiece`
- 核心 Section：`P6-2.5`
- 出现 Section：`P6-2.5`，`P7-4.1`
