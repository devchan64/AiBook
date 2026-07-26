## WordPiece

- 含义：WordPiece 是一种 tokenizer 系列，它按 vocabulary 的效率选择 subword 片段，并用较小的可复用片段稳定表示少见词。它不是把每个完整单词都记住，而是学习有用片段，再用这些片段拆分新词。
- 为什么重要：WordPiece 说明，不同 tokenizer 方法可能把同一文本切成不同的计算单位。这会影响 token 数、模型输入长度和成本，所以预训练模型使用了哪种 tokenizer，不只是实现细节，而会改变输入表示本身。
- 相关概念：`tokenization`，`Byte Pair Encoding`，`SentencePiece`
- 核心 Section：`P6-2.2`
- 出现 Section：`P6-2.2`，`P6-2.5`，`P7-4.1`
