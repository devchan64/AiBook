<a id="bpe-byte-pair-encoding"></a>
<a id="bpebyte-pair-encoding"></a>

## BPE，字节对编码

- 含义：BPE（字节对编码）是一类 tokenizer 方法，它通过不断合并经常一起出现的字符片段或 subword 片段来构建 subword vocabulary。它从较小单位开始，逐步把高频组合当作更大的 token 单位。
- 为什么重要：BPE 说明 tokenization 不是简单按空格切分。学到的 vocabulary 会影响 token 数、成本以及稀有词或高频词的切分方式，因此用户看到的文本长度和模型实际计算的长度可能不同。
- 相关概念：`tokenization`，`WordPiece`，`SentencePiece`
- 核心 Section：`P6-2.2`
- 出现 Section：`P6-2.2`，`P6-2.5`，`P7-4.1`
