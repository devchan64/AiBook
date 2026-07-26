<a id="token-id"></a>

## token ID

- 含义：token ID 是 tokenizer 生成的 token 片段在模型 vocabulary 中对应的编号。它不是可见字符串的意义，而是用来在内部词表中查找该片段的识别符。
- 为什么重要：LLM 不会直接计算原文字符串，而是接收 token ID 顺序列，把这些 ID 转成 embedding 向量后再计算。这个概念能避免把 token 字符串、token 数和 token ID 混在一起，也能避免把 ID 数字大小误读成意义强弱或重要度。
- 相关概念：`token`，`tokenization`，`vocabulary`，`embedding`
- 中心 Section：`P6-2.2`
- 出现 Section：
