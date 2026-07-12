# Part 6 收尾：LLM 与生成式 AI 整理

> Section ID: `P6-summary`
> Version: `v2026.07.12`

Part 6 是这样一个区段：它让读者从把生成式 AI 当作 `很会回答的机器` 来消费，再往前走一步，通过真正的解释把 LLM（large language model）会读取什么输入单位、在什么结构上学习、又在什么服务结构里实际运作重新绑在一起。

这个 Part 的核心，是不要停在把 LLM 看成单纯 `很会说话的模型`。只有把 token、embedding、Transformer、pretraining、fine-tuning、RAG、tool use、agent、evaluation、运营约束（constraints）连成一条流，生成式 AI 的真实结构才会显出来。

换句话说，Part 6 是那个必须真正解释 Part 1 到 Part 4 里用 `后面再解释` 留下来的 GPT、next-token prediction、instruction tuning、RAG、tool use、agent 的 Part。

重新展开这一 Part 时，最稳妥的方式，是先区分当前说明属于哪一个层次。

| 要重新抓住的层次 | 这里要确认的问题 | 代表主题 |
| --- | --- | --- |
| 模型内部原理 | 模型怎样读取输入，又怎样挑出下一个输出？ | token、embedding、Transformer、GPT |
| 调整与使用体验 | 同样的结构为什么会带来指令跟随与对话质量差异？ | pretraining、fine-tuning、instruction tuning、alignment |
| 服务连接 | 模型外面还要加上什么，才会成为真正功能？ | prompt、RAG、向量检索、tool use、agent、MCP |
| 运营判断 | 怎么把回答质量与服务质量分开来看？ | evaluation、cost、latency、failure handling |
| 背景轴 | 应当放在什么谱系与比较下重新读主流干线？ | LLM 发展史、BERT 系列 |

## 这一 Part 走过的核心流程

Part 6 的流程可以整理成下面这样。

| 流程阶段 | 这一阶段要抓住的问题 |
| --- | --- |
| token 与 tokenization | 模型用什么输入单位来读一句话？ |
| embedding 与语义空间 | 符号怎样被变成可以比较的表征？ |
| Transformer、GPT 系列、next-token prediction | 为什么 next-token prediction 会连到长文本生成与指令跟随？ |
| pretraining、fine-tuning、instruction tuning、alignment | 同样的结构怎样被调成不同的使用体验？ |
| prompt、RAG、向量数据库 | 当模型内部记忆不够时，会从外面接上什么？ |
| tool use、function calling、agent | 流程怎样从回答继续连到查询与执行？ |
| MCP、harness | 工具连接与执行记录环境应该按什么视角整理？ |
| evaluation、自动评估、人类评估 | 什么该交给自动检查，什么还要留给人工判断？ |
| 服务约束、失败应对、运营视角 | 为什么好回答与可运营服务不是一回事？ |
| 重新绑成一个小型生成式 AI 功能流 | 一个问题怎样通过检索、回答、评估、记录而闭合？ |
| 把发展史与 BERT 系列重新整理成背景轴 | 直接谱系与比较背景怎样分开读？ |

在这条流程里要确认的结果，是你已经能把 `模型本身` 与 `模型周围的系统` 分开来读。完成 Part 6 之后，写 prompt、接检索、调工具、在运营里记录失败，应该都能看出它们是不同层次的问题。尤其重要的是不要丢掉 `模型内部原理 -> 调整层 -> 服务连接 -> 运营判断` 这个顺序。

按当前目录来看，这个 Part 更自然的阅读方式是 `输入与表征 -> LLM 核心结构 -> 学习与调整 -> prompt 与依据连接 -> 执行结构 -> 评估、运营与综合练习 -> 背景轴`。也就是说，更稳定的方式是先把 Chapter 1 到 Chapter 17 当成主流干线，然后再把 Chapter 18 `LLM 发展史` 与 Chapter 19 `BERT 系列` 当成后接的背景轴。

如果再把当前 Part 6 的代表 Section 固定一次，那么 P6-10.1 负责 RAG，P6-14.2 负责 harness，P6-15.1 负责 evaluation，P6-15.2 负责自动评估与人工评估，P6-17.2 负责请求执行记录，P6-18.2 负责直接谱系与周边依据，P6-19.1 负责 BERT 比较轴。复习时也先抓住这些基线，会更容易顺着概念词汇表与正文之间的连接走。

第一次复习时，先抓住下面三行就够了。

| 先重新抓住的把手 | 这里马上要确认的内容 |
| --- | --- |
| Chapter 1-17 主流干线 | 输入、生成、检索/执行、评估/运营怎样闭成一个请求流程 |
| Chapter 18-19 背景轴 | 这条主流干线立在什么历史与比较标准上 |
| 转成 Part 6 的产出物 | 这个结构应该改写成什么样的 run record 与回顾文档 |

同样的流程如果再压成请求层面的一句话，就是下面这样。

`把问题按 token 读进去 -> 必要时接上文档或工具 -> 生成回答 -> 再用评估与记录确认一次。`

如果再把主流干线和背景轴分开，最稳定的读法会变成下面这样。

| 先读的主流干线 | 这里要确认的内容 |
| --- | --- |
| token、embedding | 输入单位与表征 |
| Transformer、GPT、next-token prediction | 生成结构的核心 |
| pretraining、fine-tuning、instruction tuning、alignment | 改变使用体验的调整层 |
| prompt、RAG、向量检索、tool use、agent | 模型外部的检索与执行连接 |
| evaluation、operations、综合小练习 | 质量判断与记录结构 |

| 后接的背景轴 | 这里重新读到的内容 |
| --- | --- |
| LLM 发展史 | 当前主流干线立在哪条谱系上 |
| BERT 系列比较 | 怎样区分生成中心的 GPT 系列与阅读中心的系列 |

也就是说，Part 6 最安全的读法，是先读 `它怎样工作`，再贴上 `它从哪里来、又和什么不同`。

如果把这条主流干线再压成一次服务请求的最短流程，就会变成下面四步。

| 一个请求的主流流程 | 这里先要确认的内容 |
| --- | --- |
| 读取输入 | token、embedding、上下文表征 |
| 生成或调整回答 | Transformer、GPT、pretraining、instruction tuning |
| 不够时从外部补强 | RAG、tool use、agent、MCP |
| 检查并留下结果 | evaluation、operations、记录、下一步动作 |

第一次复习时，再确认下面两行，就能很快把主流干线与背景轴重新整理起来。

| 要重新抓住的标准 | 一句话整理 |
| --- | --- |
| Chapter 1-17 | 解释生成式 AI 主流干线的章节 |
| Chapter 18-19 | 让那条主流干线被读得更准确的发展史与比较背景轴 |

如果从 Part 6 向后交出去的 `产出物` 角度改写这条流程，会变成下面这样。

| 在 Part 6 里理解到的结构 | 在 Part 6 里实际要留下的产出物 |
| --- | --- |
| token 与输入表征 | token 长度笔记、上下文上限检查表、输入比较记录 |
| 生成与 next-token prediction | 生成结果比较表、decoding 设置笔记、输出质量观察记录 |
| RAG 与检索结合 | 检索候选列表、选择依据笔记、依据与回答连接记录 |
| agent 执行循环 | 步骤计划、执行结果记录、最终回顾摘要 |
| evaluation 与 operations | 回顾摘要、失败案例记录、下一步改进行动 |

## 必须记住的概念

Part 6 里尤其该长久留下来的概念如下。

| 区分 | 要记住的视角 |
| --- | --- |
| token | 模型读取输入与输出时，是按 token 单位，而不是按人看到的整句来读。 |
| embedding | embedding 是把符号（symbol）变成可比较意义的向量（vector）表征。 |
| Transformer | 当前 LLM 的中心结构立在 self-attention 与并行计算之上。 |
| pretraining | LLM 会先通过 next-token prediction 从大规模数据里学会语言模式。 |
| fine-tuning 与 alignment | 还存在单独的阶段，把模型进一步调向特定任务（task）或指令（instruction）。 |
| prompt | prompt 是组织输入的方法，不是重新训练模型知识本体的过程。 |
| RAG | RAG 不是增加模型内部记忆，而是检索外部依据并把它接成输入上下文。 |
| 向量检索 | 它是按语义相近去找文档，但检索质量同时受 embedding 质量与索引结构影响。 |
| agent | agent 是一个把目标连成多步骤计划、行动、观察流程的执行结构。 |
| MCP 与 harness | MCP 整理的是工具连接接口，harness 整理的是执行、评估、记录环境。 |
| evaluation 与 operations | 好回答示例与好服务运营不是一回事。必须同时看质量、成本、延迟、失败应对。 |

把这张表都读完之后，最后还应该留下下面这个区分。

- `模型结构`：token、embedding、Transformer、pretraining
- `服务连接`：prompt、RAG、向量检索、tool use、agent
- `运营判断`：evaluation、自动/人工复核、cost、latency、failure handling

这个区分，也是 Part 6 里决定先记录什么的标准。

- 如果解释的是模型结构，后面就应该留下 `输入与输出记录`。
- 如果解释的是服务连接，后面就应该留下 `依据与工具结果记录`。
- 如果解释的是运营判断，后面就应该留下 `评估状态与失败记录`。

## 容易误解的地方

在 Part 6 里，尤其要小心下面这些误解。

- 不能把 LLM 当成 AI 的全部。
- 不能把 prompt 与 fine-tuning 读成同一件事。
- 不能把 RAG 误读成 `模型已经完全理解了外部事实`。
- 接上 tool use 并不自动等于就是 agent。
- 不能把 MCP 读成单一产品名或某个 vendor 专用功能。
- 不能把 harness 固定成某一个单独工具名。
- 自动评估分数高，不等于真实用户体验就一定足够好。
- 即使生成质量看起来不错，如果 cost、latency、permission、failure handling 没准备好，也不能算服务完成。
- 分别理解了检索、tool use、evaluation，也不等于马上就能把它们实现成一个请求流程。
- 不能把深度学习历史里所有有名事件都直接读成 LLM 的直接谱系。

Part 6 后半段尤其要再次确认的误解，还有下面这些。

| 容易混淆的场景 | 更准确的区分 |
| --- | --- |
| 既然有出处链接，groundedness 也一定够了 | 链接存在与实际解释正确不是一回事。 |
| 自动评估通过了，服务质量也一定够了 | 自动检查与人工复核抓的是不同失败。 |
| 模型更大就等于服务更好 | 质量、延迟、成本、吞吐量必须一起看。 |
| timeout 与 hallucination 都只是失败 | 系统失败与模型失败对应的处理路径不同。 |

## 这一 Part 不在这里结束的问题

Part 6 把重点放在解释生成式 AI 的结构与服务连接上，因此下面这些问题被有意交给 Part 7 的项目语境。

- 用真实数据与日志时，最先应该做哪个最小功能？
- baseline、改进实验、失败记录应该通过什么文档与产出物留下？
- 部署与运营复核应该按什么顺序进入项目文档？

换句话说，Part 6 是解释 `为什么需要这样的结构` 的 Part，而 Part 7 则是通过真实项目产出物再次验证这套结构的 Part。

此时被交出去的最重要转变，是下面这一点。

- 在 Part 6 里，你理解的是 `概念名称`。
- 在 Part 7 里，你要确认的是这些名字应该变成 `什么记录项`。

例如：

- tokenization 应该留下成输入长度与上下文使用量记录
- RAG 应该留下成选中依据与回答连接笔记
- agent 应该留下成执行步骤与审批状态记录
- 运营失败 应该留下成失败原因与下一步动作记录

这里尤其被交出去的实践问题，是下面这些。

- 哪些问题只靠 prompt 就能闭合，哪些问题需要 retrieval 或 tool？
- 检索失败、依据不足、执行失败要留在什么 run record 里？
- 自动评估与人工复核应该按什么顺序放进真实项目文档？

## 进入下一 Part 前要确认的问题

在进入 Part 7 之前，你应当能回答下面这些问题。

- 能解释为什么 token 与 tokenization 会影响模型成本与输出长度吗？
- 能在 RAG 语境里解释 embedding 与 vector retrieval 吗？
- 能从大流程上说明为什么 Transformer 会成为 LLM 的基础结构吗？
- 能区分 pretraining、fine-tuning、instruction tuning、alignment 吗？
- 能说出 prompt、RAG、tool use、agent 各自属于什么层次的问题吗？
- 能从 `整理执行环境` 的角度解释 MCP 与 harness 吗？
- 能解释模型质量与服务质量为什么并不总是同一回事吗？
- 能把一个小型生成式 AI 功能重新绑成请求、依据、输出、记录的流程吗？
- 能在讲发展史时区分直接谱系与周边依据吗？

## Part 6 收尾

完成 Part 6 之后，当再听到生成式 AI 相关说明时，你应当已经能区分：哪些是模型内部结构问题，哪些是服务设计问题，哪些是运营与评估问题。

一旦有了这个区分，就会更清楚地看到，光说一句 `LLM 很聪明` 是远远不够的。现实里，输入单位、表征、学习方式、检索连接、工具调用、执行环境、评估标准、运营约束都会一起工作。

Part 6 正是把这套结构整理好、再交给 Part 7 的真实项目单元之前的最后一道整理关。

## 来源与参考资料

这个文档是对 Part 6 全体内容的内部总结，不直接引用外部资料。
