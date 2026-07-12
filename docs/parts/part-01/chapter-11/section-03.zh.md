# P1-11.3 Transformer 与预训练 LLM(pretrained LLM)

> Section ID: `P1-11.3`
> Version: `v2026.07.12`

在 11.1 中，我们看了语言模型(language model)与嵌入(embedding)；在 11.2 中，我们又看了 RNN、Seq2Seq、Attention 如何处理顺序与上下文。

这里要看的是，形成现代 LLM(large language model)直接谱系的两个关键转折：

> 把 Attention 提升为中心结构的 Transformer  
> 先在大规模文本上学习的预训练(pretraining)

这里的核心问题是：如果 Attention 变得如此重要，那么现代 LLM 是如何建立在 Transformer 与预训练之上并不断扩大的？

这里重要的脉络是：

> Transformer 把 self-attention 放到中心，使同一序列里的 token 能直接互相参考；  
> 预训练 LLM 则先在大规模文本中学习语言模式，再通过 fine-tuning、prompt 或 in-context learning 连接到多种任务。

在 Part 1 中，本节先建立 `Transformer`、`self-attention`、`positional encoding`、`Encoder`、`Decoder`、`预训练(pretraining)`、`fine-tuning`、`BERT`、`GPT`、`in-context learning` 的基本区分。11.2 先解释了 RNN、Seq2Seq、Attention 为什么会出现，这里则在那条脉络之上整理：`现代 LLM 是建立在什么结构与学习流程上的？`

## 本节范围

这里不会详细解释 Transformer 的公式、multi-head attention 的内部计算，也不会详细讨论大规模训练基础设施。Transformer block 和 self-attention 的结构会在 Part 5 重新出现，现代 LLM 服务结构则会在 P1-14.1 到 P1-14.6 再连回来。

`Transformer`、`self-attention`、`Encoder`、`Decoder`、`预训练`、`BERT`、`GPT`、`in-context learning` 在开始时都可能听起来像现代 LLM 里的相似名词。先简短区分一下它们的作用：

| 术语 | 极简含义 | 本节中的作用 |
| --- | --- | --- |
| Transformer | 以 self-attention 为中心的序列模型结构 | 现代 LLM 的核心结构家族 |
| self-attention | 计算同一序列中 token 之间相关度的结构 | Transformer 的核心机制 |
| positional encoding | 添加 token 位置信息的装置 | 在没有 recurrence 的情况下补足顺序信息 |
| Encoder | 构造完整输入上下文化表示的结构 | 理解 BERT 家族的基础 |
| Decoder | 根据前面的 token 生成下一个 token 的结构 | 理解 GPT 家族的基础 |
| 预训练 | 先从大规模文本中学习的阶段 | 获得广泛语言模式的关键 |
| fine-tuning | 为特定任务做额外调整的阶段 | 预训练之后的重要使用方式 |
| in-context learning | 不更新权重，只通过 prompt 上下文改变行为的方式 | GPT-3 之后用户体验变化的核心 |

这里至少要保留的区分是：`Transformer 以 self-attention 为中心`、`BERT 以 encoder 为中心`、`GPT 以 decoder 为中心`、`先预训练，再使用`。

这里主要聚焦四个问题：

| 主题 | 本节要看的问题 |
| --- | --- |
| Transformer | 为什么 Attention 会成为模型的中心结构？ |
| Encoder 与 Decoder | 为什么 BERT 和 GPT 家族会以不同方式被使用？ |
| 预训练(pretraining) | 为什么模型要先在大规模文本上训练？ |
| 文脉内学习(in-context learning) | 为什么 prompt 里的例子会改变模型行为？ |

prompt 写法会在 P1-12.1 到 P1-12.3 中再讲；向量检索和 RAG 会在 P1-13.1 到 P1-13.4 以及 P1-14.2 中再讲；AI 服务架构会在 P1-14.1 到 P1-14.6 再讲。这里的目标只是抓住一条大线索：现代 LLM 不是突然出现的，而是语言建模、嵌入、sequence modeling、Attention 与预训练结合后的结果。这里仅区分 `结构`、`学习流程`、`用户体验的变化`。

## 本节目标

- 把 Transformer 理解为以 self-attention 为中心的结构。
- 把 self-attention 理解为计算 token 之间相关度的方式，而不是人类式注意。
- 从直觉上理解为什么需要 positional encoding。
- 区分 Encoder、Decoder、Encoder-Decoder 的角色差异。
- 理解 BERT 与 GPT 都属于 Transformer 家族，但学习目标和使用方向不同。
- 区分 pretraining 与 fine-tuning。
- 理解 GPT-2 与 GPT-3 如何引出 zero-shot、few-shot 与 in-context learning 的使用体验。
- 不把 LLM 等同于全部 AI。

## 三个基准

这里不会去计算 Transformer 的公式，而是集中整理现代 LLM 的直接谱系。只要抓住下面三个基准，整体脉络就会清楚。

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| Transformer 把 Attention 提升为中心结构 | 这能说明为什么一讲现代 LLM 就绕不开 Transformer。 | 只要理解成 token 会直接参考其他 token 即可。 |
| pretraining 是先在大规模文本上学习的阶段 | 这能解释为什么 LLM 在面对具体任务前就已经具备广泛语言行为。 | 只要知道模型会先在大型语料上学习，再被用于具体任务即可。 |
| BERT 与 GPT 同属 Transformer 家族但角色不同 | 这能防止把 Transformer 误解成单一产品。 | 只要理解成同一结构家族里也会有不同学习目标与使用方向即可。 |

## Transformer 把 Attention 放到了中心

在 11.2 中，RNN 是通过不断传递 hidden state 来处理序列的。这种方式与有顺序的数据天然契合，但面对很长的输入时，会产生一步步计算的负担。

Attention 展示了另一种可能：如果模型能够直接参考输入中相关的位置，就不必把所有信息都塞进单一的 fixed-length vector。

Transformer 把这个想法从辅助装置提升为主结构。Vaswani 等人在 2017 年的论文中提出了一种不依赖 recurrence 或 convolution，而以 attention 为核心的 sequence transduction 架构。论文标题 *Attention Is All You Need* 正是这个转折的象征。

核心直觉可以写成：

> 句子中的每个 token  
> 会查看同一句子里的其他 token  
> 并据此更新自己的表示。

例如看这句话：

> 该模型会根据前面的上下文预测下一个 token。

在处理 `预测` 时，`模型`、`前面的上下文`、`下一个 token` 都可能相关。self-attention 会计算权重，让同一序列里的 token 互相参考。

这里的 `self` 并不是“只看自己”，而是指：在同一输入序列内部，token 彼此互相参考。

## positional encoding 用来补足顺序信息

RNN 因为按顺序处理输入，所以顺序信息会自然地嵌进结构里。但 Transformer 使用的是没有 recurrence 的 self-attention，因此需要一种额外装置来提供顺序信息。

这就是 positional encoding 的作用。

> token embedding：  
> 表示这个 token 是什么的向量
>
> positional encoding：  
> 表示这个 token 位于什么位置的信息

从入门角度，可以这样理解：

> “我在读书”
>
> 我：token 含义 + 第 1 个位置  
> 在：token 含义 + 第 2 个位置  
> 读书：token 含义 + 第 3 个位置

这并不表示 Transformer 不知道顺序，而是说：它不是像 RNN 那样靠顺序传递 hidden state 来表达顺序，而是把位置信息加进 self-attention 的计算中。

## Encoder 与 Decoder 的角色不同

原始 Transformer 论文使用的是 Encoder-Decoder 结构。Encoder 负责构造输入序列的表示，Decoder 负责生成输出序列。

| 结构 | 代表性脉络 | 直觉 |
| --- | --- | --- |
| Encoder | BERT 家族 | 查看完整输入并构造上下文化表示(contextual representation)。 |
| Decoder | GPT 家族 | 根据左侧上下文生成下一个 token。 |
| Encoder-Decoder | 原始 Transformer 翻译结构 | 读取输入序列，再把它转换成输出序列。 |

这个区分对于理解 BERT 与 GPT 很重要。

BERT(Bidirectional Encoder Representations from Transformers) 使用的是 Transformer encoder。Devlin 等人的 BERT 论文说明：它通过 masked language model 与 next sentence prediction 来预训练 deep bidirectional representation，再把这些表示 fine-tuning 到多种任务上。

GPT(Generative Pre-Training) 则属于 Transformer decoder 的脉络。Radford 等人在 2018 年的 GPT 论文中提出：先做 generative pre-training，再做 task-specific fine-tuning。GPT 家族基本上与根据前文预测下一个 token 的 autoregressive language model 脉络更接近。

但这个区分不能被过度简化成：

> BERT 会理解，GPT 会思考

这种说法会带来误解。更安全的表达是：

> BERT 家族：  
> 以 encoder 为中心，擅长构造输入的上下文化表示
>
> GPT 家族：  
> 以 decoder 为中心，擅长根据前面的 token 上下文生成下一个 token

## 预训练让模型先学会语言模式

预训练(pretraining)意味着：模型不是一开始就直接针对某个具体任务训练，而是先从大规模文本中学习一般性的语言模式。

> pretraining：  
> 先在大规模文本语料中学习
>
> fine-tuning：  
> 之后再针对具体任务做调整

这条脉络并不是只在 Transformer 之后才出现。ELMo 提出了 deep contextualized word representation，强调单词含义会随上下文改变；ULMFiT 则系统地展示了先预训练语言模型、再针对目标任务 fine-tuning 的流程。

Transformer 家族把这条脉络扩展到了更大规模。GPT 把 generative pre-training 与 supervised fine-tuning 结合起来；BERT 则通过 masked language model 来预训练双向表示。

这里需要特别注意的是：

> 预训练并不意味着模型把事实当作已验证真理储存起来。  
> 它更准确的含义是：  
> 模型通过大规模文本中的下一个词预测、遮蔽词恢复、上下文关系等目标，  
> 学习语言模式与表示。

这也是为什么预训练 LLM(pretrained LLM)仍然可能生成看似合理却没有依据的内容。模型学到的是语言模式，而不是被保证过的真相。

## 上下文化表示超越了静态嵌入

11.1 中提到的早期嵌入，可以理解成给每个单词分配相对固定的向量。但在真实语言里，词义会随着上下文改变。

> 我把钱存进了银行。  
> 我在河岸边看到了一排树。

`银行/岸` 在表面词形上可能相同或近似，但语境不同。ELMo 正是为处理这种问题而提出：单词表示应随着上下文而变化。BERT 也利用 Transformer encoder 构造会反映完整输入上下文的表示。

这对于理解 LLM 很重要。LLM 并不会把单词只当作固定词典条目，而是会计算 token 在周围上下文中的角色。

## GPT-2 与 GPT-3 扩大了基于 prompt 的使用体验

GPT-2 强调：语言模型可以通过自然语言指令与示例，表现出多种任务行为。论文展示了用 WebText 训练的模型在 zero-shot setting 下，不需要单独的 task-specific fine-tuning 也能完成多个 downstream task。

GPT-3 把这条脉络扩展得更大。Brown 等人在 2020 年的论文中用一个 175B 参数模型比较了 zero-shot、one-shot、few-shot 设置。这里关键是：few-shot 并不意味着重新训练模型权重。

> fine-tuning：  
> 使用训练数据更新模型权重(weight)
>
> in-context learning：  
> 把指令和示例放进 prompt 中，改变输出行为  
> 但基础权重通常不被更新

这条脉络直接通向今天的使用体验：人们会用自然语言向 LLM 描述任务，并在 prompt 中加入例子。

这里不会详细讨论 prompt 写法技巧。prompt 的组成与限制会在 12.1 到 12.3 中再展开。这里先记住更窄的一点就够了：

> GPT-2 与 GPT-3 扩大了这样一种体验：  
> 自然语言输入本身就可以成为指定任务的方式

GPT-3 论文也指出了局限。few-shot 性能变好，并不自动证明模型像人一样真正学会了一个新任务。论文提到，很难区分模型究竟是在真正学习新任务，还是在识别训练数据里已见过的模式。

## 本节要避免的缩写式误解

理解 LLM 时，下面这些缩写式说法都很危险：

| 危险缩写 | 更安全的表达 |
| --- | --- |
| Transformer 就等于 LLM | Transformer 是现代 LLM 中被广泛使用的核心结构，但不等于整个 LLM |
| 预训练就是背事实 | 预训练是在大规模文本中学习语言模式与表示 |
| BERT 会理解，GPT 会思考 | BERT 与 GPT 是 Transformer 家族里结构与学习目标不同的两条脉络 |
| prompt 示例会重新训练模型 | in-context learning 通常是在不更新权重的情况下，通过输入上下文改变行为 |
| AI 最后就是 LLM | LLM 是现代 AI 中很重要的一条脉络，但并不等于全部 AI |

尤其最后一条很重要。今天人们很容易把 AI 直接等同于 LLM，但 AI 还包括规则式系统、搜索、机器学习、强化学习、计算机视觉、语音识别、机器人、推荐系统等多种脉络。更安全的立场是：

> LLM 是在语言与生成接口上造成巨大变化的一条重要支流，  
> 但它并不等于全部 AI。

## 检查清单

- 我可以把 Transformer 解释成以 self-attention 为中心的结构。
- 我可以把 self-attention 解释成 token 之间相关度的计算，而不是人类式注意。
- 我可以说明为什么需要 positional encoding。
- 我可以区分 Encoder、Decoder、Encoder-Decoder 的角色。
- 我可以说明 BERT 与 GPT 都属于 Transformer 家族，但在结构与学习目标上不同。
- 我可以区分 pretraining 与 fine-tuning。
- 我可以把 ELMo 与 ULMFiT 描述成大型预训练 Transformer 之前的重要前兆。
- 我可以把 in-context learning 解释成不更新权重、只通过输入上下文改变行为的方式。
- 我不会把 LLM 等同于全部 AI。
- 我可以把 Transformer、预训练、BERT、GPT 不当作一团最新术语，而是拆成 `结构`、`学习流程`、`用户体验变化` 来解释。
- 我可以把现代 LLM 解释成建立在 self-attention 结构与大规模预训练之上的成长谱系，而不是某个单一产品名称。

## 来源与参考资料

- Ashish Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762){: target="_blank" rel="noopener noreferrer" }, arXiv, 2017, 确认日期: 2026-06-23.
- Matthew E. Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, 确认日期: 2026-06-23.
- Jeremy Howard, Sebastian Ruder, [Universal Language Model Fine-tuning for Text Classification](https://arxiv.org/abs/1801.06146){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, 确认日期: 2026-06-23.
- Alec Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI, 2018, 确认日期: 2026-06-23.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, 确认日期: 2026-06-23.
- Alec Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI, 2019, 确认日期: 2026-06-23.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, 确认日期: 2026-06-23.
