# P6-19.1 以限制和结构转换的流程阅读 LLM 发展史

> Section ID: `P6-19.1`
> Version: `v2026.07.24`

理解今天的 LLM(large language model，大语言模型)时，常见误解是只把它看成`突然出现的巨大模型`。但实际上，今天的生成体验是由语言模型(language model)、嵌入(embedding)、序列模型(sequence model)、attention、Transformer 和大规模预训练(pretraining)相互重叠后形成的。

本节不会把这条流程整理成事件名称列表，而是用`为了减少什么限制，才出现了下一种结构`这一标准重新连接它。这里比说明本章位置更重要的，是先学会为什么 n-gram 之后会出现嵌入，为什么 RNN 之后会出现 attention 和 Transformer。

## 从限制到结构转换的流程

核心问题如下。

- LLM 之前，人们如何对语言建模？
- 嵌入和序列模型试图解决什么问题？
- 为什么 attention 和 Transformer 成为转折点？
- 预训练 LLM 改变了什么？

阅读 LLM 发展史时，用`为了减少什么限制，才出现了下一种结构`这一大流程会更安全。结构转换顺序应该先于事件名称出现。

这里不需要记住所有细节结构，而要先把`什么限制引出了下一次转换`连接起来。既然前面已经读过 token、Transformer、GPT 和预训练，现在重要的是能否按`限制 -> 下一种结构`的顺序重新说明这些结构是怎样到来的。

如果只压缩必须留下的转换，下面七步就足够。

| 转换 | 试图减少的限制 | 要留下的一句话 |
| --- | --- | --- |
| n-gram | 对长上下文的泛化很弱 | 语言开始被当作概率问题处理。 |
| 嵌入 | 词只被当作完全分离的符号 | 相似表达可以被看得更近。 |
| RNN/Seq2Seq | 难以长距离处理顺序 | 试图把前面上下文更久地连接到后面解释。 |
| Attention | 固定长度压缩瓶颈 | 让模型能回看需要的位置。 |
| Transformer | 顺序计算瓶颈 | 把关系计算放到结构中心。 |
| 预训练 | 每个任务都要从头适配 | 先学习大规模语言模式，再复用。 |
| GPT 型接口 | 任务被不同模型分开的感觉 | 多种任务可以通过一个生成接口完成。 |

## 区分事件名称和结构转换流程

- 你可以用几个大的转折点解释 LLM 发展史。
- 你可以区分统计语言模型、嵌入、RNN、attention、Transformer 和预训练的位置。
- 你可以把 LLM 解释为语言模型家族中的一条流程，而不是 AI 的全部。
- 你可以准备好区分直接谱系和周边证据。

## 第 1 步. 语言开始被当作概率问题处理

早期语言模型的核心问题很简单。

- 给定前面的词，下一个词最可能是什么？
- 哪个词序列看起来更合理？

在这个阶段，n-gram 等方法被广泛使用。它们通过统计短上下文中的词频，来近似下一个词的概率。

这一时期的关键贡献是：

- 语言开始不只被当作规则列表，而是被当作概率(probability)问题处理；
- `下一个词预测`这一视角变得清楚。

但限制也很明显。

- 长上下文很难处理。
- 罕见表达和新组合很弱。
- 很难在相似词之间泛化。

## 第 2 步. 词开始被表示为向量

下一次转换是嵌入。

如果不把词保留为 one-hot 向量那样完全分离的符号，而是表示成由多个数字组成的向量，那么在相似上下文中使用的词就可以处在某种更接近的位置。

这个阶段的重要问题是：

- 模型如何把 `cat` 和 `dog` 这种用法相似的词看得更近？
- 文本如何转成可计算的连续表示(continuous representation)？

word2vec 等研究广泛传播了这种直觉。此后，语言建模强烈转向不仅学习`下一个词概率`，也学习好的`表示空间(representation space)`。

## 第 3 步. 顺序开始由神经结构处理

语言是序列(sequence)数据，所以得到词向量还不够。结构还必须更好地处理前面上下文如何影响后面解释。

在这个阶段，RNN(recurrent neural network)、LSTM(long short-term memory) 和 GRU(gated recurrent unit) 变得重要。

这些结构试图解决下面的问题。

- 前面看到的信息能否传到后面？
- 有顺序的句子能否被累积成状态(state)？
- 在长上下文中能否少丢失一些信息？

对于机器翻译(machine translation)等问题，Seq2Seq(sequence-to-sequence)也是一次重要转换。

- 读取输入句子。
- 构建内部表示。
- 生成输出句子。

这个流程由此成为可能。

## 第 4 步. Attention 减少了瓶颈

基于 RNN 的 Seq2Seq 很强，但它有一个瓶颈问题：整个输入必须被压缩成一个固定长度表示。

Attention 试图减少这个问题。

- 生成一个输出词时，
- 回看整个输入，
- 并给相关位置更大的权重。

可以这样记住。

`Attention 是让模型在需要时回看输入相关部分的结构。`

这个阶段很重要，因为通向 LLM 的直接结构转换从这里开始。

## 第 5 步. Transformer 改变了中心结构

Transformer 把 attention 从辅助装置变成了中心结构。

这次转换的意义很大。

- 它较少受长顺序计算束缚。
- 它更适合并行处理(parallel processing)。
- 它可以更直接地计算 token 之间的关系。

正如 Part 6 前面所见，Transformer 把 self-attention 放在中心，通过大规模矩阵运算处理 token 到 token 的关系。

这种结构很适合大规模 GPU 训练。因此，Transformer 不再只是`一个翻译模型`，而成为后来 LLM 扩散的基础结构。

## 第 6 步. 预训练改变了模型的使用方式

下一次转换是预训练。

核心做法不再是立刻把模型适配到一个小的特定任务，而是先从大规模文本中学习通用语言模式，再把模型连接到许多任务。

这个阶段的重要变化是：

- 先广泛学习语言模式。
- 再通过 fine-tuning 或 prompt-based use 连接到任务。
- 增加一个大模型处理多种任务的可能性。

这个转换在 BERT 和 GPT 家族中以不同方向强烈出现。

## 第 7 步. LLM 扩展了生成接口

随着 GPT 家族模型变大，用户体验也改变了。

- 用户可以用自然语言给出指令。
- 少量示例可以改变行为。
- 同一个模型开始看起来像是能摘要、分类、翻译、起草和生成代码。

到这里，用户常常会感觉`所有 AI 都变成了 LLM`。但更安全的解释是：

`LLM 不是 AI 的全部。它是在语言和生成接口上制造巨大转换的一个家族。`

## 非常简单地画出流程

```mermaid
--8<-- "assets/part-06/chapter-19/p6-c19-s01-history-flow-zh.mmd"
```

这个图不是为了容纳所有复杂细节，而是为了抓住`大的转换顺序`。需要从中确认的结果是：你能否不把统计语言模型、嵌入、序列模型、attention、Transformer 和大规模预训练混在一起，而是按顺序说明它们如何连接。

## 案例和例子

### 案例 1. 翻译

翻译一开始很容易被想象成`把词替换成另一种语言的词`。但句子变长后，前面部分的主语、否定和修饰范围会影响后面的选词，所以简单替换很快崩塌。这个场景很快显示出，为什么发展史需要`短频率计算 -> 顺序处理 -> 回看相关位置`。这个案例中要确认的结果是，处理更长句子关系的结构是否确实比词替换规则更稳定。

| 容易先抓住的简单直觉 | 实际缺少什么 | 变得必要的结构 |
| --- | --- | --- |
| 只要改词义 | 长距离关系和整句状态 | Seq2Seq、attention |
| 从前往后依次替换词 | 后面上下文可能改变前面选择 | 回看相关位置的结构 |
| 很多词典映射就够了 | 自然的整句构成 | 基于 Transformer 的宽上下文处理 |

### 案例 2. 搜索和嵌入

如果用户搜索 `my refund is late`，而文档写的是 `reimbursement processing delay`，很容易认为找不到是自然的，因为相同词没有出现。但在真实服务中，用户表达和文档表达会持续偏离，单靠词匹配会漏掉相关文档。这个场景压缩了为什么`表示空间`在历史中变得重要，以及这条流程后来如何连接到向量搜索和 RAG。这个案例中要确认的结果是，即使没有相同词，意义相似的文档能否重新作为候选出现。

| 从表面匹配看 | 真实服务中的问题 | 表示空间思维带来的变化 |
| --- | --- | --- |
| 没有相同词，就像是另一个问题 | 常漏掉意义相近的文档 | 意义相近的表达可以被比较为更近 |
| 搜索像是词匹配游戏 | 用户措辞变化时搜索质量下降 | 表达不同也可以恢复相关候选 |
| 只匹配标题词似乎足够 | 正文措辞差异和间接表达会被漏掉 | 直接连接到向量搜索和 RAG |

### 案例 3. 聊天机器人体验

当用户在一个聊天窗口里连续要求摘要、分类、修改句子时，很容易感觉`从一开始就出现了一个能做一切的巨大助手`。实际上，`下一个词预测`、`表示学习`、`长上下文处理`、`attention`、`Transformer` 和`大规模预训练`逐步累积，才到达`多种任务可以在一个接口中完成`。这个案例中要确认的结果是：今天的聊天机器人体验能否被解释为结构转换的累积，而不是一次突然发明。

三个案例可以通过发展史流程这样连接起来。

| 情况 | 起初看起来简单的事 | 实际累积的结构转换 |
| --- | --- | --- |
| 翻译 | 词替换问题 | 扩展到长句关系、attention 和 Transformer |
| 搜索和嵌入 | 找到相同词 | 把意义相近的表达放得更近的表示学习 |
| 聊天机器人体验 | 一个聊天窗口处理一切 | 让多个任务在一个接口中完成的结构累积 |

## 通过结构转换流程重新阅读的场景

初读发展史时，一个常见误解是只关注按顺序记住事件名称，而漏掉`为什么下一种结构变得必要`。标准不应是年份记忆，而应是`哪种限制推动了下一次转换？`。转换成实践问题，可以这样读。

| 如果出现这种疑问 | 首先要问的问题 |
| --- | --- |
| `为什么又需要另一种结构？` | 前一种结构做不到什么？ |
| `这是搜索故事还是模型故事？` | 是否区分了表示泛化和长顺序处理？ |
| `看起来 LLM 好像突然什么都会做。` | 多次转换按什么顺序累积起来？ |

先学会的标准很简单。发展史更安全的读法不是`名称列表`，而是试图减少限制的结构转换序列：`频率计算限制 -> 表示空间需求 -> 长顺序处理需求 -> 回看相关位置 -> Transformer -> 预训练`。

## 在历史轴上观察结构转换

本节需要的活动不是运行代码检查一个小结果值，而是把眼前的功能或案例重新放回历史轴。理解 LLM 发展史时，更重要的能力不是`能模仿什么计算`，而是用语言区分`哪种限制让下一种结构变得必要`。

下面的表把前面的案例重新折回历史轴。每一行中，需要确认的不是技术名称本身，而是它试图减少的限制，以及为什么它通向下一种结构。

| 观察到的场景 | 直接对应的历史阶段 | 读者现在应获得的判断 |
| --- | --- | --- |
| 从短上下文频率预测下一个词 | 统计语言模型的起点 | 只靠频率对长上下文和新组合很弱。 |
| `refund` 和 `reimbursement`，或 `late` 和 `delay` 这类表达虽然词不同，却应被归为一组 | 嵌入和表示泛化的方向 | 需要表示空间来比较没有相同词的相近意义。 |
| `Approved` 和 `not approved` 会因顺序和否定改变意义 | RNN、LSTM、GRU 等顺序处理背后的问题意识 | 即使词看起来相似，如果漏掉前后状态，句子解释也会崩塌。 |
| 长句翻译中，生成某个词时必须重新查看输入中的相关位置 | Attention 和 Transformer 转换 | 需要时回看相关位置的计算进入结构中心。 |
| 一个大模型通过同一接口处理摘要、分类、翻译和起草 | 预训练和 GPT 型接口 | 直觉应从分开的任务专用模型，转向复用大型语言模式。 |

## 练习：把功能场景放到历史轴上

看下面的功能，先写出它最直接连接到哪种历史问题意识。如果很难只选一个，就在 `frequency`、`representation`、`order`、`referring back to relevant positions`、`pretraining` 中写两个。

1. 客户说 `my refund is late`，系统仍能找到文档 `reimbursement processing delay guide`。
2. 系统摘要一长串邮件的最终请求。
3. 一个聊天接口看起来能处理翻译、起草和分类。
4. 同一个问题下，稍微改变给出的示例，回答风格也随之改变。

先分类这四个场景，再和下面说明比较。

| 功能场景 | 先标记的历史轴 | 说明 |
| --- | --- | --- |
| 客户说 `my refund is late`，系统仍能找到文档 `reimbursement processing delay guide` | representation | 因为即使没有相同词，也必须把相似意义归在一起，所以嵌入和表示空间的问题意识最直接。 |
| 系统摘要一长串邮件的最终请求 | order, referring back to relevant positions | 系统必须跟随长输入的流程，也要重新查看当前摘要需要的位置，所以顺序处理和 attention 会一起出现。 |
| 一个聊天接口看起来能处理翻译、起草和分类 | pretraining, GPT-style interface | 中心是先通过许多指令学习大规模语言模式，再复用这个模型，而不是构建分开的任务专用模型。 |
| 同一个问题下，稍微改变给出的示例，回答风格也随之改变 | pretraining, context use | 模型把当前输入上下文中的示例读成条件，并改变生成行为，这连接到预训练之后的 prompt-based use。 |

在这个练习中，理由比答案更重要。如果能通过结构转换的理由说明一个功能，例如`搜索是表示问题`、`摘要是长上下文和相关位置问题`、`聊天接口是预训练之后的使用问题`，本节目标就达成了。

## 连接限制和下一种结构的标准

看完整个流程之后，也会更清楚：现在不需要记住每个阶段的全部实现细节。此刻下面这些就足够。

| 现在只需留下的内容 | 在主流程中回到哪里 |
| --- | --- |
| 语言建模从`预测下一个表达`的问题开始 | P6-6.1 Next token prediction |
| 嵌入是从符号到可计算向量的转换 | P6-3.1 把 token ID 变成可比较坐标的 embedding |
| Attention 和 Transformer 是结构转折点 | P6-4.1 Transformer 如何导向 LLM 中的 next-candidate score |
| 预训练改变了模型的使用方式 | P6-7.1 Pretraining |

更重要的问题不是`能否完整背诵整段历史？`，而是`能否解释为什么主流程按这个顺序排列？`

需要确认的结果是：GPT、next-token prediction、pretraining 等说明能否被重新读取为一个流程，而不是功能列表；在这个流程中，每种结构填补一种限制，并通向下一阶段。

- 它把 Part 6 前面的 Transformer 重新放回 Part 6 的 LLM 谱系中。
- 它减少之后阅读 BERT、GPT、pretraining、instruction tuning 和 RAG 时的结构混淆。
- 它减少把 LLM 等同于全部 AI 的误解。

## 检查清单

- 你应该能够把 LLM 发展史解释为 `frequency -> representation -> order -> referring back to relevant positions -> pretraining` 的转换流程，而不是`事件名称列表`。
- 你应该能够说出翻译、搜索、聊天机器人体验背后分别对应哪种历史阶段的问题。
- 你应该能够解释，只有同时抓住 Transformer 之前的问题意识和预训练之后的使用转换，才能更准确地阅读今天的 LLM。

## 参考资料

- Yoshua Bengio et al., [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, accessed 2026-07-19.
- Tomas Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-07-19.
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, accessed 2026-07-19.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, accessed 2026-07-19.
- Ashish Vaswani et al., [Attention Is All You Need](https://papers.nips.cc/paper/7181-attention-is-all-you-need){: target="_blank" rel="noopener noreferrer" }, NeurIPS, 2017, accessed 2026-07-19.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-07-19.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-07-19.
