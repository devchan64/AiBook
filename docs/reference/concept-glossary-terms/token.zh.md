<a id="token"></a>

## token

- 含义：token 是模型处理文本时切分出来的基本计算单位。它不一定等于一个词；一个词可能被拆成多个 token，几个短表达也可能被当作一个片段处理。人眼看到的一整句话，在模型内部会变成 token 序列来计算。
- 为什么重要：必须区分人阅读的词和模型实际计算的单位，才能正确理解 next-token prediction 与 LLM 生成过程。成本、上下文窗口长度和 token 覆盖问题都从这个计算单位开始。理解 token 以后，prompt 设计和上下文长度限制为什么要看 token 数，而不只是字符数，也会更清楚。
- 相关概念：`下一词元预测(next-token prediction)`，`语言建模(language modeling)`，`嵌入(embedding)`，`分词(tokenization)`，`上下文窗口(context window)`
- 中心 Section：`P6-2.1`
- 出现 Section：`P1-10.2`，`P5-13.1`，`P5-13.2`，`P6-2.1`，`P6-2.2`，`P6-2.3`，`P6-2.4`，`P6-2.5`，`P7-4.1`，`P7-4.2`
