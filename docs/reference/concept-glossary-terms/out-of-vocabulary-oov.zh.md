## 词表外(out-of-vocabulary, OOV)

- 含义：词表外是指某个词或 token 落在当前 vocabulary 或 tokenization 规则之外，模型不能把它稳定表示成熟悉单位的状态。人可能看到有意义的表达，但模型侧可能只能看到陌生或破碎的片段。
- 为什么重要：分类、搜索或生成任务中 OOV 项很多时，模型实际读取到的输入会减少。这个概念能帮助读者把性能下降看成可能的 tokenizer 或 vocabulary 设计问题，而不只是模型能力问题。
- 相关概念：`tokenization`，`token coverage`，`embedding`
- 核心 Section：`P7-4.2`
- 出现 Section：`P6-2.5`，`P7-4.1`，`P7-4.3`，`P7-summary`
