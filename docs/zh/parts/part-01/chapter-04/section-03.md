# P1-4.3 特征(feature)、表征(representation)与参数(parameter)

> Section ID: `P1-4.3`
> Version: `v2026.07.11`

4.2 已经整理了 `input`、`output` 与 `data`，也就是模型要看什么、又想从它那里拿回什么。这一节继续往里走一步，解释这些输入在模型内部会变成怎样的计算材料。

核心问题在于：模型看到的是不是原样输入，还是会先把输入改写成更容易计算的值。

这一节会以入门层级整理 `feature`、`representation` 和 `parameter`。它延续 4.2 的客户支持消息例子，重点是固定读懂模型时必需的术语位置。

在 Part 1 中，这一节会固定从“模型计算”视角阅读 `feature`、`representation` 与 `parameter` 的基本标准。`representation learning` 与 `rule-based approach` 的对照已经在 3.3 先整理过，`input`、`output`、`data`、`example` 和 `label` 的基本结构已经在 4.2 固定过。这里更窄的焦点是：`输入在模型内部会变成什么计算材料`。

## 这一节的范围

4.3 不是教人直接搭建模型的章节。该选什么算法、模型结构如何设计、学习流程如何组织，会在 Part 4 的机器学习章节和 Part 5 的深度学习章节里再回来。

这里需要的问题更小：当我们看一个已经定义好的模型时，输入会变成什么值，模型内部又有哪些值会被用来计算输出？

这里的目标不是模型制作流程，而是具备一套能读懂模型计算流向的基础词汇。

## 这一节的目标

- 把 `feature` 理解成模型从输入中实际使用的值。
- 把 `representation` 理解成把原始数据改写成更易计算形式后的结果。
- 把 `parameter` 理解成模型内部、参与输出计算的已调整数值。
- 区分原始输入、特征、表征和参数不是同一个东西。
- 为 4.4 中“问题定义与模型选择的关系”做准备。

## 三个基准

阅读模型内部术语时，先要分开下面三个点。

| 基准 | 为什么重要 | 这一节需要达到的理解程度 |
| --- | --- | --- |
| `feature` 是模型实际用于计算的输入值 | 这样能看见原句和计算值可能不同。 | 区分人读到的句子和模型用到的数字线索并不总是一回事。 |
| `representation` 是把数据变成更易计算形式后的结果 | 这会成为理解深度学习与 embedding 的过渡桥梁。 | 记住同一份数据可以被改写成不同表征。 |
| `parameter` 是模型内部被调整的值 | 这会成为理解后续 learning 与 inference 的关键连接点。 | 区分被调整的不是输入本身，而是模型内部的值。 |

`feature`、`representation`、`parameter`、`vector` 和 `activation` 都会在计算里出现，但它们指向的位置不同。

| 术语 | 极简含义 | 在这一节里的角色 |
| --- | --- | --- |
| feature | 模型实际使用的输入值 | 从原始输入抽出的计算线索 |
| representation | 把数据改写成更易计算形式后的结果 | 模型看到的内部输入形式 |
| parameter | 模型内部被调整过的值 | 影响输出计算的内部标准 |
| vector | 把多个数字并排列开的数值束 | 承载表征的常见形式 |
| activation | 计算过程中产生的中间值 | 表征穿过多层时某一刻的值 |

这里可以先按下面的位置来读：`feature` 是输入线索，`representation` 是改写后的形式，`parameter` 是内部标准，`vector` 是数字束，`activation` 是中间计算值。

这里尤其容易混淆的是 `feature` 和 `representation`。在这一节里，最安全的读法是：把 `feature` 看成模型在输入侧直接使用的值，把 `representation` 看成把原始数据改写成这种值时所得到的整体形式或结果。也就是说，像 `存在配送线索` 这样的一格值更接近 feature，而把整句转换成数字向量的状态更接近 representation。

## 原始输入通常不能直接拿来计算

回到 4.2 的客户支持消息例子。

> 如果明天还收不到配送，我就取消。

人会同时看到好几条线索。

| 人能看到的线索 | 可能代表的含义 |
| --- | --- |
| 配送 | 与配送相关的咨询 |
| 明天之前 | 截止时间条件 |
| 还收不到 | 可能发生配送延迟 |
| 我就取消 | 取消意图或施压 |

但模型不会像人那样直接理解整句。为了进行计算，输入必须先被改写成某种值。这时就会出现 `feature` 和 `representation`。

> original input -> feature or representation -> model computation -> output

这个流程把“模型直接理解输入”的直觉，换成了“模型先把输入变成可计算的值再使用”的视角。这里最关键的是明确区分：`原始文本` 和 `模型实际计算所用的值` 可能不同。

## feature 是模型实际使用的输入值

Google 的 Machine Learning Glossary 把 feature 解释成机器学习模型的输入变量。一条 example 可以同时拥有一个或多个 features 以及一个 label。

如果把客户支持消息分类问题极度简化，feature 可以长成下面这样。

| 原始输入 | feature |
| --- | --- |
| `我想退款。` | 是否出现 `退款` 这个词 |
| `配送什么时候到？` | 是否出现 `配送` 这个词 |
| `商品寄来时是坏的。` | 是否出现与损坏有关的表达 |
| `我想改地址。` | 是否出现与地址修改有关的表达 |

这些 feature 可以由人事先定义。例如，每条消息句子都可以被赋上下面这样的值。

| 消息句子 | `退款` 线索 | `配送` 线索 | `损坏` 线索 | label |
| --- | ---: | ---: | ---: | --- |
| `我想退款。` | 1 | 0 | 0 | 退款 |
| `配送什么时候到？` | 0 | 1 | 0 | 配送 |
| `商品寄来时是坏的。` | 0 | 0 | 1 | 换货 |

这里 `1` 表示线索存在，`0` 表示不存在。真实模型可以使用远比这更复杂的值，但在这一节里，只要把 feature 理解成“模型用来计算的输入值”就够了。

## feature 并不等于原始输入

重要的是，feature 并不是原始输入本身。

| 区分 | 例子 |
| --- | --- |
| 原始输入 | `我昨天收到的商品坏了，想再寄一个新的。` |
| 人设计的 feature | 存在损坏线索，存在补发线索 |
| 输出 label | 换货或补发 |

原始句子是自然语言，而 feature 是从句子里抽出来、让模型能计算的值。

如果不区分这一层，就很容易以为“把数据喂给模型，它就会自己懂”。现实里真正重要的是：抽出了什么值、保留了什么线索、舍弃了什么线索，以及输入最终以什么形式进入模型。

如果把这一点和 4.2 连起来看，一次输入束也可能展开成多个 feature。比如输入是 `消息句子 + 订单状态 + 最近配送事件`，模型可以从里面得到 `存在配送线索`、`已经发货`、`最近出现延迟事件` 这类多个计算值。这里关键是不要把 `一条输入` 和 `多个 features` 当成同一个东西。输入是模型收到的原材料，而 feature 是从原材料里提出来供计算使用的值。

在同样的意义上，feature 往往也能被看成 representation 的一部分。不过，为了减少初学者混淆，4.3 会先保持更简单的区分：`feature` 是计算里直接用到的具体值，`representation` 是这些值所处的更大形式。

## representation 是把数据变得更容易计算后的结果

Google 的 glossary 把 `representation` 描述成把数据映射成有用 feature 的过程。4.3 会把 representation 稍微读宽一些：它是“把原始数据改写成模型更容易计算的形式之后得到的结果”。

例如，同一条消息句子可以被改写成多种不同的 representation。

| 表征方式 | 例子 | 优势 | 限制 |
| --- | --- | --- | --- |
| 关键词特征 | `配送` 出现、`取消` 出现 | 简单、易解释 | 容易漏掉上下文 |
| 数值特征 | 句子长度、感叹号个数 | 易和表格数据结合 | 可能难以承载足够语义 |
| 类别特征 | 消息渠道：App、邮件、电话 | 易和业务数据连接 | 本身不承载句子意义 |
| 学到的表征 | 把句子转成内部向量 | 更擅长处理相似性与上下文 | 人很难直接读取 |

3.3 已经比较过 rule-based approach 与 representation learning。这里不重复那部分讨论，只保留一个建模视角下最重要的点：`输入被表示成什么样，决定了模型能看到怎样的世界`。

## 好的表征会把真正重要的差别显露出来

Bengio、Courville 和 Vincent 的综述解释过，机器学习算法的成功在很大程度上依赖于数据表示方式。即使数据相同，不同的表示也可能把重要因素显露出来，也可能把它们藏起来。

再看客户支持消息例子。

> 我想取消付款。  
> 如果物流还不到，我就取消。

两句话都包含 `取消` 这个词，但前一句更接近付款取消或退款，后一句更接近“物流延迟下的条件性取消”。

如果只把“是否出现这个词”作为 feature，这两句可能会显得太像。

| 表征 | 容易区分这两句吗？ | 为什么 |
| --- | --- | --- |
| 只看是否出现 `取消` | 不容易 | 两句都包含 `取消` |
| 同时看 `配送` 线索与 `取消` 线索 | 稍微好一些 | 第二句里的配送语境变得可见 |
| 使用更广的整句语义表征 | 可能好很多 | 条件、意图和上下文可以一起被反映 |

好的 representation 会把模型真正需要区分的差别显露出来。差的 representation 则可能遮住重要差异，或者把不重要的差别放大。

## parameter 是模型内部被调整过的值

如果说 feature 和 representation 更接近“进入模型时值的形状”，那么 parameter 就是模型内部被调整的值。

Google 的 Machine Learning Glossary 把 parameter 解释成模型在训练过程中学到的 weights 和 biases。这里可以先更简单地理解成下面这样。

> parameter = 模型把输入变成输出时所依赖的、可调整的内部值

这里常见的一个词是 `weight`。weight 是一种 parameter，用来表示某个输入值或内部值会多大程度影响输出计算。

有时人们会用 `connection strength` 这种比喻来解释 weight。这个比喻在说明 neural network 这类多个计算单元互相连接的结构时很有帮助。但 4.3 的目标并不是解释神经网络。像线性模型、概率模型、树模型这样的其他结构也存在，并不是所有 parameter 都长得像神经网络里的连接。

所以这里保留 `parameter` 作为基础术语。`weight` 只是一个代表性的 parameter，而 `connection strength` 只保留为以后学习神经网络时可以重新拿出来用的有限比喻。

把客户支持消息分类再简化一点，可以直观想成下面这样。

| feature | 对退款输出应该连接多强？ | 对配送输出应该连接多强？ |
| --- | ---: | ---: |
| `退款` 线索 | 强 | 弱 |
| `配送` 线索 | 弱 | 强 |
| `取消` 线索 | 中 | 中 |

这个表不是在展示真实参数值，它只是帮助建立直觉。在学习过程中，模型会借由许多案例去调整这类内部值。

这一节里更重要的不是“参数是怎么学出来的”，那部分会在后面再讲。现在只要先理解：当我们看一个训练完成的模型时，模型内部已经存在被调整好的值，而这些值会参与把输入表征转换成输出的计算。

## 为什么会短暂提到学习

4.2 说过，数据是一组输入和输出案例。要解释 parameter，就不得不短暂提到 training，因为 parameter 并不是从一开始就固定成有意义的值，而是会随着训练数据和学习目标被调整。

> 输入案例 -> 特征/表征 -> 模型预测 -> 与正确答案比较 -> 参数调整

假设训练数据里有很多下面这样的案例。

| 输入 | label |
| --- | --- |
| `我想退款。` | 退款 |
| `可以取消付款吗？` | 退款 |
| `配送什么时候到？` | 配送 |
| `今天会发货吗？` | 配送 |

一开始，模型内部的标准可能并不适合这个任务。当预测错误时，学习过程会把内部值往“减少误差”的方向调整。随着这种调整在大量案例上重复，模型就会逐渐把输入表征和输出之间的关系对齐。

但 parameter 会被调整，并不意味着模型像人一样理解现实意义。parameter 只是为了配合训练数据和学习目标而被调整的计算值。

## 同一个“parameter”也可能指不同层级

初学者常见的一个混淆点是：在 AI 工具里，像 `temperature`、`top-p`、`max tokens` 这样的值有时也会被叫作 parameter。但它们和 4.3 里说的模型内部参数，并不是同一回事。

Google 的 glossary 把 `temperature` 说明为控制模型输出随机程度的 hyperparameter。在 LLM 场景里，它通常更适合被理解成：在选择下一个 token 时，用来控制概率分布有多尖锐或多平缓的生成设置值。

| 区分 | 例子 | 谁来设定？ | 什么时候使用？ | 含义 |
| --- | --- | --- | --- | --- |
| model parameter | weight, bias | 在训练中学得 | 模型内部计算 | 经学习调整并存放在模型里的值 |
| hyperparameter | learning rate, batch size | 人或调参流程 | 训练设置 | 决定学习过程条件的值 |
| generation setting | temperature, top-p, max tokens | 用户或服务设置 | 推理与生成 | 改变训练后模型如何选输出的值 |

所以，即使看到 `temperature parameter` 这样的说法，也不能立刻把它读成“模型内部学出来的参数”。在这里，更准确的读法是“控制 LLM 生成行为的设置值”。

## 术语边界笔记

4.3 的核心术语是 feature、representation 与 parameter。不过，当你阅读真实 AI 工具或聊天机器人文档时，还会遇到一些看起来和它们混在一起的词。这里先只划出边界，避免混淆。

| 术语 | 在 4.3 里的位置 | 之后更详细处理的位置 |
| --- | --- | --- |
| intent | 把输入解释成业务意图或标签后的结果，或其中间判断 | AI 服务架构、聊天机器人结构 |
| temperature | 不是模型内部参数，而是 LLM 生成设置值 | LLM 与生成式 AI |
| hyperparameter | 调节学习或使用条件的值 | 机器学习 |
| embedding | 可被看成向量表征的一种形式 | LLM 与向量检索 |

例如，intent analysis 可以看成下面这样。

> 用户句子 -> 特征/表征 -> intent label -> 后续业务处理

Google 的 glossary 把自然语言理解（NLU, Natural Language Understanding）解释成自然语言处理的一个子领域，用来判断用户说了什么或输入了什么，以及它的意图是什么。不过 4.3 不会深入讲 intent analysis。这里唯一需要划清的是：intent 不是模型 parameter，它更接近使用输入表征后得到的一种业务解释或输出。

## 把三个术语放在一起看

feature、representation 与 parameter 彼此连接，但不是同一个东西。

| 术语 | 问题 | 客户支持消息例子 |
| --- | --- | --- |
| feature | 模型从输入里用了哪些值？ | `配送` 线索、`退款` 线索、句子长度 |
| representation | 原始数据被改写成了什么可计算形式？ | 关键词表、数字向量、学到的句子表征 |
| parameter | 计算里用了哪些已调整内部值？ | 对应于各线索影响输出程度的内部值 |

把它们串成流程，大致是这样。

```mermaid
--8<-- "assets/part-01/chapter-04/representation-model-parameter-flow-en.mmd"
```

这个图是简化版。真实模型里，feature 和 representation 的边界可能会变模糊；在深度学习里，representation 本身也可能经过多层逐步学出来。这里先只读出一个主干：`输入会变成模型能用的值，再和模型内部已调整的值一起参与输出计算`。

这个图最重要的作用，是让人先看见 `feature/representation` 和 `parameter` 虽然都重要，但它们位置不同。先把位置分清：`feature/representation` 在输入一侧，`parameter` 在模型内部。

## 这一节不做什么

4.3 不会深入处理下面这些内容。

| 这里不展开的内容 | 后续位置 |
| --- | --- |
| 如何选择模型结构 | Part 4 和 Part 5 |
| 学习算法如何调整参数 | Part 4 和 Part 5 |
| loss function、backpropagation 与 optimization 是什么 | Part 5 |
| 性能评价和模型选择如何进行 | P1-4.4 与 Part 4 |
| intent routing 与 tool calling 如何组织 | Part 6 |

在理解这些内容之前，这一节只先固定必要的基础位置，也就是 feature、representation 与 parameter 的基本位置。

## 常见混淆

| 混淆 | 更安全的理解 |
| --- | --- |
| 输入和 feature 是同一回事 | input 是原始进入的数据，feature 是为了让模型使用而做出的值 |
| representation 总是人能读懂的 | 学到的 representation 可能很难被人直接解释 |
| intent 是模型 parameter | intent 更接近把用户输入解释成业务目的或标签后的结果，而不是存放在模型里的参数 |
| parameter 是规则 | parameter 不是人能直接读的 IF-THEN 规则，而是学习调整出的内部值 |
| 所有 parameter 都是神经网络里的连接强度 | 连接强度只是解释神经网络时有用的比喻，并不是所有模型参数的通用定义 |
| temperature 也是模型 parameter | 在 LLM 里，temperature 不是模型内部学出来并存放的值，而是控制输出生成的设置值 |
| 参数越多就一定越好 | 模型规模本身不会自动带来好模型，数据、问题定义和评价也必须匹配 |
| 只要有数据，representation 就会自动变好 | 性能和限制仍然取决于用了什么 representation，以及它是用什么数据学出来的 |

这些混淆在后面会持续重要。尤其当讨论进入深度学习和 LLM 后，像参数数量、representation、embedding 这样的词会出现得越来越频繁。

## 这一节要记住的视角

模型不会把原始输入原样“理解”掉。输入会先变成 feature 或 representation，模型再把这些值和内部已调整的值，也就是 parameter，一起用于输出计算。

如果说 4.2 问的是“要把什么当成输入、又希望什么当成输出？”，那么 4.3 问的就是“这个输入进入模型后，会变成什么计算材料？”

下一节 4.4 会使用这些概念，说明为什么问题定义会决定模型与评价方式。

## 检查清单

- 我可以解释 feature 是模型使用的输入值。
- 我可以解释 representation 是把原始数据改写成更易计算形式后的结果。
- 我可以解释 parameter 是模型内部被调整、并参与输出计算的值。
- 我可以区分原始输入、feature、representation 与 parameter。
- 我可以解释好的 representation 会显露重要差异，差的 representation 可能会把它遮住。
- 我可以把 intent analysis 和 model parameter 区分开，并把它读成把输入解释成业务意图或标签的一层。
- 我可以区分 model parameter 和 LLM generation setting。
- 我可以区分：4.3 不是模型制作流程，而是用来读懂模型计算的一组基础术语。

## 什么时候应先想起这一节的视角

当你开始感觉原始输入数据和模型内部值被混在同一层理解时，就该把这一节的视角重新拿出来。

- 当原始句子、feature、representation 和 parameter 都开始像同一种“数据”时
- 当你很想把 `temperature` 这类生成设置直接理解成模型自己学到的 parameter 时
- 当你需要解释：为什么同样输入只因 representation 不同，就会让模型看见完全不同的差异时

这时，就重新按 `feature/representation 在输入侧`、`parameter 在模型内部` 的位置来切开。然后再看：哪些值是人设计的线索，哪些值是通过学习调整出来的内部标准。这样能很快减少术语混乱。

## 出处与参考资料

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary/){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, 确认日期：2026-06-22.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }, arXiv, 2012-06-24, 确认日期：2026-06-22.
