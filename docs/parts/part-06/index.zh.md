# Part 6. LLM 与生成式 AI

> Section ID: `P6-index`
> Version: `v2026.07.12`

Part 6 是 `从这里开始真正解释` LLM 与生成式 AI 的 Part。如果说 Part 1 到 Part 5 负责先确定位置、准备基础，那么到了 Part 6，就不再把解释往后推。从这里开始，正文必须真正说明 `LLM 是在什么结构上运作的`、`为什么 next-token prediction 也能导出长回答与指令执行`、`为什么会接上检索、工具、agent`。

这个 Part 更适合按这样的规则来读：同一个 Part 里，某个核心概念的详细说明只在正文里第一次完整出现一次，后面的章节只保留当前语境所需的最小解释。所以更稳妥的基线抓法是：把 `P6-1.1` 先作为 `token` 的代表说明位置，把 `P6-2.1` 先作为 `embedding` 的代表说明位置，把 `P6-3.1` 先作为 `从 LLM 角度重读 Transformer 的标准`，把 `P6-10.1` 先作为 `RAG`，把 `P6-13.1` 先作为 `agent`，把 `P6-14.1` 先作为 `MCP`，把 `P6-15.1` 先作为 `evaluation`，后面的节再回连概念词汇表与代表 Section，会更安全。

这个 Part 的核心目的，是让读者能够解释 `为什么生成式 AI 服务会长成现在这样的结构`。很多读者已经有聊天机器人、文档摘要、检索增强、代码生成、agent 等使用经验。但只靠这些经验，仍然很难把 token、Transformer、GPT、pretraining、instruction tuning、RAG、tool use、MCP 连成一条线。Part 6 的责任，正是在正文里真正兑现这个承诺。

所以 Part 6 先把主流干线立起来。

1. token 与 tokenization
2. embedding 与表征
3. 从 LLM 视角重新读 Transformer
4. GPT 系列与 next-token prediction
5. pretraining、fine-tuning、instruction tuning、alignment
6. prompt、RAG、向量检索
7. tool use、agent、MCP、harness
8. evaluation、operations 与一个小型综合练习

在这个过程中，BERT 系列与 LLM 发展史被当作阅读主流干线所需的 `背景地图`。也就是说，背景说明是需要的，但这个 Part 的中心轴仍然是 `生成式 AI 的工作原理与服务连接`。

这个 Part 里，各章不宜都当成同一种说明来读。当前正在读的层次，可以先按下面的方式抓住。

| 当前阅读的层次 | 这里先问的问题 | 代表主题 |
| --- | --- | --- |
| 模型内部原理 | 模型怎样读取输入，又怎样挑出下一个输出？ | token、embedding、Transformer、GPT |
| 调整与使用体验 | 同样的结构为什么会表现成不同的回答风格？ | pretraining、fine-tuning、instruction tuning、alignment |
| 服务连接 | 模型外面还要接上什么，才会变成真正功能？ | prompt、RAG、向量检索、tool use、agent、MCP |
| 运营判断 | 一个生成得不错的回答，为什么不等于一个可运营的服务？ | evaluation、latency、cost、failure handling |
| 背景轴 | 现在读到的主流干线来自哪里、又和什么不同？ | LLM 发展史、BERT 系列比较 |

Part 6 现在不是大幅重排 Chapter 编号，而是在 `保持当前顺序` 的前提下，让主流干线与背景轴读得更清楚。因此，更稳定的读法是先把 Chapter 1 到 Chapter 17 当成主流干线，再把 Chapter 18 `LLM 发展史`、Chapter 19 `BERT 系列` 当成后接的比较/背景轴。

而且这个 Part 不只是解释概念，还会一起要求读者看到 `先检查什么，又会连到什么判断`，例如：

- tokenization -> 输入是怎样被切开的，又怎样影响上下文长度？
- RAG -> 找到了什么依据，又为什么选了这个依据？
- agent -> 通过哪些步骤执行，又在哪个位置需要复核？
- evaluation / operations -> 回答质量、失败案例、下一步动作应该怎样整理？

## 这一 Part 的阅读顺序

Part 6 按下面顺序来读，整体流程会更稳定。

1. 先通过 token、tokenization、embedding 去看模型到底把什么当成输入来读。
2. 然后通过 Transformer、GPT、next-token prediction 来读生成的核心结构。
3. 接着用 pretraining、instruction tuning、alignment 去看为什么同样的结构会导出不同的使用体验。
4. 最后再通过 RAG、tool use、agent、MCP、evaluation、operations 去读服务连接结构。
5. 把主流干线读完之后，再把 LLM 发展史与 BERT 系列贴上去，重新整理 `直接谱系` 与 `比较标准`。

如果丢掉这个顺序，Part 6 很容易看起来像 `术语列表`。反过来，只要保住这个顺序，它就会被读成 `输入单位 -> 生成结构 -> 使用体验调整 -> 服务连接` 的一条流。

### 当前推荐阅读路径

| 阅读捆绑 | 对应 Chapter | 这样读的原因 |
| --- | --- | --- |
| 主流 1. 输入与表征 | Chapter 1-2 | 只有先抓住 token、tokenization、embedding，后面的结构才不容易发虚。 |
| 主流 2. 生成结构 | Chapter 3-5 | Transformer、GPT、next-token prediction 是 Part 6 最重要的结构轴。 |
| 主流 3. 学习与调整 | Chapter 6-8 | pretraining、fine-tuning、instruction tuning、alignment 被当作同一条调整轴来读。 |
| 主流 4. 服务连接 | Chapter 9-14 | prompt、RAG、向量检索、tool use、agent、MCP 被捆成服务结构。 |
| 主流 5. 评估与整合 | Chapter 15-17 | evaluation、operations、小型综合练习用来区分 `好模型` 和 `好服务`。 |
| 背景轴 | Chapter 18-19 | 发展史与 BERT 系列比较在后面补上，让主流干线被读得更准确。 |

在这组结构里，Chapter 4、6、8、10 不再往前硬挪。Chapter 4 紧跟在 Transformer 之后，立即把 GPT 的生成位置闭住；Chapter 6 是在 next-token prediction 之后第一次打开 `学习究竟先学到了什么` 的章节；Chapter 8 则是在 pretraining 与 fine-tuning 之后，用来闭合 `让模型跟随用户指令的调整层`；而 Chapter 10 只有在先确认了 prompt 单独不够的地方之后，才会自然读成 `接上外部依据的结构`。所以当前顺序最符合主流干线的流动方式。

如果把主流干线再压短一些，可以变成下面这些阶段。

| 主流阶段 | 核心问题 | 当前捆在一起的 Chapter |
| --- | --- | --- |
| token 与输入表征 | 模型把什么当成输入来读？ | Chapter 1-2 |
| Transformer 与 GPT 生成结构 | 为什么 next-token prediction 会连到生成？ | Chapter 3-5 |
| 学习与调整 | 为什么同样的结构会变成不同的使用体验？ | Chapter 6-8 |
| 检索与执行连接 | 什么时候 prompt 单独不够，什么时候需要 RAG、tool、agent？ | Chapter 9-14 |
| 评估与运营 | 为什么好回答与可运营服务不是一回事？ | Chapter 15-17 |
| 背景轴 | 应该用什么发展史与比较视角重新读这条主流干线？ | Chapter 18-19 |

这个表最关键的一点，是让 Chapter 18 与 Chapter 19 读成 `在主流干线读完之后贴上的背景轴`，而不是 `挡在前面的前置背景`。

如果从服务体验角度再压一下，一个请求的主流干线可以整理成下面四步。

| 一个请求的主流流程 | 这里先看的东西 |
| --- | --- |
| 读取输入 | token、embedding、上下文表征 |
| 生成或调整回答 | Transformer、GPT、pretraining、instruction tuning |
| 不够时从外部补强 | RAG、tool use、agent、MCP |
| 检查结果 | evaluation、operations、失败原因、下一步动作 |

## 这一 Part 必须真正回收的前文预告

Part 6 必须真正补上前面各 Part 延后的 LLM 与生成式 AI 说明。尤其下面这些项目，不能只是名字介绍，而必须在这里有正文解释。

| 前面 Part 延后的主题 | 这个 Part 必须真正解释的内容 |
| --- | --- |
| token 与 tokenization | 为什么输入不是按完整单词，而是按 token 单位切开，又为什么这会连到成本与长度 |
| Transformer 与 next-token prediction | 为什么这种结构会连到长生成与指令执行 |
| GPT 与 BERT | 为什么结构与强任务方向会分叉 |
| pretraining 与 instruction tuning | 模型是在什么层次上学会一般语言模式与指令跟随 |
| RAG 与向量检索 | 为什么必须把模型外部的依据拉进来 |
| tool use、agent、MCP | 为什么光有生成还不够，为什么还会接上执行环境 |
| evaluation 与 operations | 为什么好回答与好服务不是同一件事 |

如果这个标准缺失，Part 6 就会再次变弱成 `生成式 AI 术语地图`。

也就是说，Part 6 必须守住的标准是 `前面预告过的主题，是否真的在这里被回收了`。如果只是名字重新出现而解释仍然空着，这个 Part 就没有尽到责任。

## 这一 Part 的目的

这个 Part 是为了从 `模型结构`、`生成机制`、`服务连接结构` 三个层次重新理解 LLM 与生成式 AI 的区段。

很多时候，生成式 AI 很容易只被记成 `会回答问题的聊天机器人`。但现实里，下面这些问题会一起跟上来。

- LLM 是怎样读取数据、又怎样挑出下一个输出的？
- GPT 和 BERT 到底哪里不同，为什么使用目的也会分开？
- 什么事情只用 prompt 就够，什么事情需要 RAG 或工具？
- 为什么 agent 与 MCP 不是 prompt 扩展问题，而是执行环境问题？
- 为什么一个生成式 AI 服务不会只靠单一模型就结束？

Part 6 的作用，就是让读者有准备去回答这些问题。它不会深入论文实现细节或大规模分布式训练系统。相反，它的目的是让读者在阅读 LLM 相关文档、产品说明、实务结构时，能先区分 `现在解释的是模型内部原理、调整层、服务组件，还是运营判断`。

## 这一 Part 解释什么，不解释什么

Part 6 是解释 LLM 与生成式 AI 主流干线的 Part。因此，下面这些内容会在正文范围内解释。

- token、embedding、Transformer、GPT、next-token prediction 的基本结构
- pretraining、fine-tuning、instruction tuning、alignment 的角色区分
- prompt、RAG、vector search、tool use、agent、MCP、harness 的连接结构
- evaluation、operations、failure handling，以及一个小型综合功能流程

相对地，下面这些内容不会在这一 Part 里全部深入展开。

- 快速变化的最新商用模型代际产品比较与数值竞赛
- 大规模分布式学习基础设施与论文实现细节
- 所有 agent framework 与 vendor 工具的详细使用方法

这些省略并不是回避核心，而是范围控制。Part 6 的责任，是解释 `为什么生成式 AI 服务会长成这种结构`，而当前产品竞赛与框架细部使用方式则被放在当前版本正文范围之外。

## 这一 Part 的目标

读完 Part 6 之后，目标是形成大致如下层级的理解。

- 能解释为什么 Transformer 是 LLM 的核心结构。
- 能解释 GPT 系列是通过 `next-token prediction` 来完成生成任务的。
- 能在大的流程里说明 temperature、decoding、instruction tuning 在生成中各自扮演什么角色。
- 能区分 BERT 系列与 GPT 系列为什么分别更擅长 `读后判断任务` 与 `生成任务`。
- 能解释什么时候需要 RAG，以及它的局限在哪里。
- 能解释 embedding、vector search、tool use、agent、MCP、harness 分别是为了补什么问题而接上去的。
- 能从 evaluation 与 operations 的角度读出生成式 AI 服务的失败样态。
- 能说明一个小型生成式 AI 功能应该按什么流程实现并回顾。

如果从为 Part 6 做准备的角度重写这些目标，也可以整理成下面这样。

| 在 Part 6 要理解的结构 | 在 Part 6 要一起检查的代表判断标准 |
| --- | --- |
| token 与输入表征 | token 长度、上下文上限、输入设计判断 |
| 生成与 next-token prediction | 生成结果比较、decoding 设置检查、输出质量观察 |
| RAG 与检索结合 | 检索候选、选中的依据、依据与回答连接判断 |
| agent 与工具执行 | 步骤计划、执行结果、需要人工复核的位置 |
| evaluation 与 operations | 失败案例解释、运营约束判断、下一步改进行动 |

## 面向入门读者的阅读标准

这个 Part 里，熟悉的服务体验与陌生的结构术语会一起出现。与其一次抓住所有实现细节，不如先用下面三个问题把层次分开。

| 先抓住的问题 | 为什么需要这个问题 | 在这一 Part 抓到什么程度就够 |
| --- | --- | --- |
| 现在解释的是 `模型内部原理`，还是 `服务连接方式`？ | 在 LLM 语境里，token、attention、RAG、agent 即使同时出现在一篇文档里，也不是同一层次的概念。 | 先抓住 Transformer 与 next-token prediction 是模型原理，RAG 与 tool use 是服务连接方式。 |
| 这个系统 `直接生成` 的是什么，又有什么是 `从外面取回或执行` 的？ | 要理解生成式 AI，就必须区分模型只靠内部知识回答的情况，与接上外部文档或工具的情况。 | 先区分只靠 prompt 的事情和需要 RAG/工具的事情。 |
| 让结果变好，说的是 `模型性能提升`，还是 `服务设计改善`？ | 生成质量问题并不总是只能靠重新训练模型解决。检索、prompt、工具连接、评估设计会一起作用。 | 必须把模型本体与服务组件分开看。 |

最短可以整理成下面这样：LLM 是一个预测下一个 token 的结构，而这个结构会通向长文本生成与指令执行。为了补足知识限制与执行限制，会接上 RAG 与工具；而在真实服务里，还必须把 agent、MCP、evaluation、operations 一起看。

## 它解释什么

Part 6 大体可以读成五个捆绑：`输入与表征`、`LLM 核心结构`、`学习与调整`、`服务连接与运营`、`背景轴`。

首先，前半段会处理 tokenization 与 embedding。这个区段解释模型到底把什么当成输入单位来读，又是通过什么表征开始计算。

接着，主流干线会处理 Transformer、GPT 系列、next-token prediction、生成过程、pretraining、fine-tuning、instruction tuning、alignment。这个捆绑是解释 `LLM 为什么能生成` 与 `使用体验怎样被调整` 的核心区段。

再往后，会处理 prompt、RAG、向量数据库、tool use、agent、MCP、harness、evaluation、operations、综合小练习。这里不再停留在单个模型说明，而是去看一个生成式 AI 服务实际上通过什么连接结构运作，并在最后把这个结构重新压成一个很小的功能流程。

最后的背景轴会重新阅读 LLM 发展史与 BERT 系列。这个区段的目的，不是拖慢主流干线，而是把前面读到的 GPT 中心说明重新放回历史与比较视角。

这一段最重要的是，不要把背景轴和主流干线混在一起。发展史与比较当然需要，但这个 Part 的主问题始终是 `生成式 AI 为什么会按这样的结构工作`。

## 为什么需要这一 Part

重新学习生成式 AI 时，最常见的混乱，就是 `模型在做的事` 与 `服务额外接上的事` 会混在一起。

例如，如果分不清一个回答之所以变好，到底是因为：

- 换了更大的模型
- 改了 prompt
- 接上了外部文档
- 调用了计算器
- 把任务拆成了多个执行步骤

那么最后记住的就不是生成式 AI 的结构，而只是一个功能列表。

Part 6 正是为了减少这种混乱而建立共同结构。从 token、Transformer 这类内部原理开始，一路看到为什么会接上 RAG、tool use，为什么还需要 agent 与 MCP，这样以后再看产品文档或实务系统设计时，就能用同样的结构重新解释它们。

同时，一旦理解了这个结构，也会更清楚地区分：哪些问题是输入设计问题，哪些问题是依据连接问题，哪些问题是执行阶段问题。

## 完成这一 Part 后会留下的理解

完成这一 Part 之后，你应该能把生成式 AI 看成不是单纯的聊天机器人功能，而是多个层次连接在一起的结构。token 变成表征的过程、Transformer 反映上下文的过程、next-token prediction 连到生成的过程、instruction tuning 与 decoding 改变使用体验的过程、RAG 与 tool use 补足模型局限的过程、以及 agent、MCP、evaluation、operations 决定服务质量的过程，都应该在同一条流程里变得可见。

一旦形成这种理解，就能跳出 `LLM 就等于 AI 全部` 这种过度简化，也能减少 `只要模型更强，服务问题都会自动解决` 这样的误解。Part 6 是用来建立一个基线，让读者把 LLM 与生成式 AI 读成有结构、有约束的技术体系，而不是流行词。

因此，这个 index 页最后要确认的结果，就是 Part 6 能不能被读成不是 `聊天机器人功能集合`，而是同时解释模型内部原理与服务连接结构的主流干线 Part。

## 完成标准

- 能解释为什么 Transformer 是 LLM 的核心结构。
- 能解释 GPT 系列是基于 next-token prediction 的生成模型。
- 能把 BERT 系列与 GPT 系列的差别解释成阅读中心任务与生成中心任务的差别。
- 能解释 prompt、RAG、向量检索、tool use 分别在补什么限制。
- 能解释 agent、MCP、harness 属于执行环境主题，而不是 prompt 主题。
- 能从 evaluation 与 operations 角度说出生成式 AI 系统的主要失败类型。
- 能说明一个小型生成式 AI 功能应当怎样按请求流程来设计和回顾。

## 来源与参考资料

这个文档是整理 Part 6 目的与学习路径的内部概览，不直接引用外部资料。
