## token 覆盖率(token coverage)

- 含义：token 覆盖率是指，在评估句子或文档中的 token 里，有多少比例能按当前 vocabulary 或 tokenizer 规则被实际读取。即使输入在人看来完整，这个值也用来检查模型侧有多少内容被保留成可用的 token 单位。
- 为什么重要：如果输入中很多部分落在词表外，同样的准确率数字也可能有不同解释。token 覆盖率能帮助读者先检查输入表达是否被充分保留，而不是立刻把低性能只归因于模型结构。
- 相关概念：`tokenization`，`token`，`out-of-vocabulary, OOV`
- 核心 Section：`P7-4.2`
