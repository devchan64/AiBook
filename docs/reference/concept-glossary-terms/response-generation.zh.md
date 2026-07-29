<a id="response-generation"></a>

### LLM 响应生成(response generation)

- 含义：LLM 响应生成是 LLM 接收 prompt 后生成自然语言回复的执行过程。它可以理解为使用已学习参数、输入 prompt 和采样设置，继续产生输出 token 的过程。
- 为什么重要：LLM 的 inference 结果常常表现为自然语言句子，而不是分类标签或数字，因此很容易把模型执行和真实思考过程混在一起。这个概念能帮助我们理解：即使回复看起来自然，它的事实性、依据和逻辑连接仍然需要另外检查。
- 相关概念：`推断(inference)`, `提示(prompt)`, `采样(sampling)`, `生成(generation)`
- 核心 Section: `P1-5.2`
