# P4-1.1 AI、机器学习、深度学习之间的关系

> Section ID: `P4-1.1`
> Version: `v2026.07.11`

Part 1 看过 AI 这个词的广义范围。Part 2 重新读过公式、Python、数组、表格和图表。现在到了 Part 4，要在这个基础上把 machine learning 单独拎出来看。

这一节会区分 AI、machine learning、deep learning、generative AI、LLM 分别指向什么范围，并说明为什么在 Part 4 里不是直接进入深度学习，而是先重新回看传统机器学习。

因此，这一节的重点是分清楚 `machine learning 在 AI 这个大领域里处在什么位置`，以及 `为什么不直接跳到 LLM 或 deep learning，而要先看数据、模型、学习、评估`。

## 本节范围

这一节是用来固定术语位置的导入。这里不会深入处理具体算法的公式、scikit-learn 的用法、神经网络结构或 Transformer 结构。

- AI 和 machine learning 是同一个意思吗？
- machine learning 和 deep learning 有什么不同？
- generative AI 和 LLM 能代表整个 AI 吗？
- 为什么 Part 4 要先看传统机器学习，再看 deep learning？
- Part 2 里学过的公式和 Python 工具会在这里怎样再次出现？

## 本节目标

- 能大致说明 AI、machine learning、deep learning、generative AI、LLM 之间的包含关系。
- 能把 machine learning 理解成 `从数据中学习模式，并把它用于预测或判断的方法`。
- 能说明 deep learning 是 machine learning 中非常重要的一条路线，但不是整个 machine learning 的同义词。
- 能把 LLM 看成现代 AI 经验中一个很强的代表性案例，但不会把它当成整个 AI。
- 能理解 Part 4 的学习主题是数据、模型、学习、评估这条流程。

## 阅读顺序

如果按包含关系和角色顺序来读，这些术语会更清楚。

1. AI 是最宽的词。
2. machine learning 是其中一种从数据里学习关系的方法。
3. deep learning 是 machine learning 中通过深层神经网络来学习表示的一条路线。
4. generative AI 和 LLM 在现代 AI 经验里非常重要，但它们不等于整个 AI。
5. 在 Part 4 里，我们会先看所有这些路线下面共同存在的数据、模型、学习和评估。

这个顺序不是为了死记学术分类，而是为了后面读文档时，至少能分出 `自己现在看到的内容是在谈数据问题、模型问题，还是服务问题`。

## 先用一句话把它们分开

术语一多起来时，比起只背包含关系，更清楚的做法是先看每个词在回答什么问题。

| 术语 | 一句话说明 | 中心问题 |
| --- | --- | --- |
| AI (artificial intelligence) | 用计算机创造或模仿智能行为的宽广领域。 | 机器能不能做出看起来像智能的事？ |
| machine learning | 通过数据经验让模型或算法性能变好的方法。 | 不把所有规则都写死，能不能让系统从数据里学会？ |
| deep learning | 用多层神经网络学习表示的 machine learning 路线。 | 模型能不能更直接地从输入中学到需要的表示？ |
| generative AI | 生成文本、图像、音频、代码等新输出的 AI 模型与服务。 | 模型能不能不只做分类和预测，而是生成新结果？ |
| LLM | 通过大规模文本学习来处理语言输入与输出的模型族。 | 模型能不能根据语言语境生成下一句表达或回答？ |

这个区分不是考试定义，而是阅读地图。同一个词在论文、产品文档、新闻报道和服务宣传里，范围都可能略有不同。所以在 Part 4 里，比起术语本身，我们更把数据、模型、学习、评估这条反复出现的结构放在中心。

## 从最大范围开始看

AI 是最宽的词。它可以包含 rule-based systems、search、heuristics、knowledge representation、probabilistic inference、machine learning、deep learning、generative AI、agents 等多种方法。

machine learning 是其中一种从数据中学习模式的方法。它不是由人把所有规则都直接写完，而是从数据中找关系、形成 model，再把这个 model 用到新数据上。

deep learning 是 machine learning 内部一条很强的路线，它通过把 neural network 堆深来学习 representation。它在图像、音频、自然语言和生成模型里带来了很大的成果，但并不是所有 machine learning 都属于 deep learning。

generative AI 指的是生成文本、图像、音频、代码等新输出的模型与服务。今天大量 generative AI 和 deep learning 紧密相连，但 generative AI 这种使用体验并不等于整个 AI。

LLM 指 large language model。现在很多人第一次真正接触 AI，往往就是通过 LLM 体验，但 LLM 不是整个 AI，而是围绕语言发展出来的一类特定模型。

```mermaid
--8<-- "assets/part-04/chapter-01/ai-scope-map-zh.mmd"
```

这张图更像学习地图，而不是严格分类表。真实研究和产品里，很多技术会混在一起。比如一个服务里，search system、rule-based filter、machine learning model、LLM 都可能同时工作。

下面这张图会把 `包含关系` 和 `真实服务组合方式` 分开来看。上面那张图是在说明 `术语的大致位置`，而下面这张图强调的是 `一个服务里可以同时运行多种方法`。

```mermaid
--8<-- "assets/part-04/chapter-01/ai-service-composition-map-zh.mmd"
```

在这张图里，LLM 不是整个服务，而只是多个组成部分中的一个。模型输出还可以和 policy judgment 结合，而当风险高或置信度低时，也可能转到 human review。

## 只看包含关系为什么还不够

入门说明里，`AI 里面有 machine learning，machine learning 里面有 deep learning` 这样的图很有用。但如果只记住这张图，一旦去看真实服务，就很容易产生误解。

例如，一个推荐服务可能会用基于用户点击记录的 machine learning model；同时，它也可能还带有排除禁售商品的 rule-based filter，以及 search index 或 database 查询。客户支持服务也未必只靠 LLM，还可能一起用到 search、permission check、policy rule、logging、human review。

因此，在 Part 4 里真正需要的视角不是 `哪种技术更新`，而是下面这种追问方式。

- 在这个问题里，哪些部分是由人直接写规则？
- 哪些部分必须从数据中学习？
- 模型输出的是 score、class、numeric prediction，还是 generation result？
- 服务做最终决定时，除了模型输出，还一起用了哪些 policy 或约束？

这些问题会把 Part 1 里看到的 AI 大地图、Part 2 里看到的数据表示方式，连接到 Part 4 的机器学习学习流程里。

## 为什么 Part 4 要把机器学习单独拿出来看

Part 4 不会直接跳到 deep learning 或 LLM，而是先看 machine learning 的基本流程。

原因很简单。就算以后去看 deep learning 和 LLM，下面这些问题还是会不断返回。

- 用的是什么 data？
- input 和 label 分别是什么？
- model 究竟在预测或分类什么？
- learning 时到底在改哪些值？
- evaluation 是按什么标准做的？
- 它在没见过的数据上还能不能工作？

传统 machine learning 非常适合用比较小的例子来展示这些问题。像 linear regression、logistic regression、decision tree、k-NN 这样的模型，结构比 deep learning 更简单。因此，它很适合先理解数据拆分、overfitting、generalization、metric。

在小型 machine learning 例子里，`准备数据`、`训练模型`、`应用到新数据`、`检查有没有猜对` 这条流程是看得见的。只要这条流程能看见，之后再去看 deep learning 或 LLM，就会先问结构，而不是先盯着模型名字。

## Part 4 的最小单位

重新看机器学习时，比起记住大量算法名字，更重要的是先把反复出现的最小单位固定下来。

| 最小单位 | 要问的问题 | 例子 |
| --- | --- | --- |
| problem | 想预测或区分什么？ | 垃圾邮件、价格、流失可能性 |
| data | 收集了什么样的案例？ | 历史邮件、交易记录、传感器测量值 |
| feature | 准备给模型的输入表示是什么？ | 词数、金额、时间、类别 |
| label / target | 模型想匹配什么？ | 垃圾/正常、实际价格、是否购买 |
| model | 什么样的学习后计算会把输入变成输出？ | 线性模型、树、最近邻 |
| training | 通过数据会调整什么值？ | 权重、分裂标准、距离标准 |
| evaluation | 它在新数据上到底有多可用？ | 准确率、误差、召回率、成本 |

这些最小单位在后面的 deep learning 和 LLM 里也不会完全消失。只是结构更大了、输入表示更复杂了，但 `数据是什么、模型学了什么、用什么标准评估` 这种追问习惯还是必须保留。

这张表其实是一组问题。`想解决什么`、`给什么输入`、`想匹配什么`、`怎么确认它有没有匹配对`，正是阅读机器学习文档时最先该检查的问题。

## 用同一个问题看三种视角

如果拿垃圾邮件分类来举例，区分会更容易。

| 视角 | 问题 | 可能的方法 |
| --- | --- | --- |
| 规则型方法 | 如果出现某个词，就把它看成垃圾邮件吗？ | 由人来写规则。 |
| machine learning 方法 | 能不能从历史邮件和标签里学出垃圾模式？ | 用 feature 和 label 训练 model。 |
| deep learning 方法 | 模型能不能更直接学到邮件文本的表示？ | neural network 一起学习表示和分类边界。 |
| LLM 利用 | 能不能让模型用自然语言理解邮件的意图和语境？ | 可以一起用 prompt、分类指令和工具连接。 |

这四种视角不是完全互相替代的。真实服务里，rule-based filter、machine learning model、基于 LLM 的 review 完全可能一起使用。所以更合适的理解不是 `最新方法会消灭旧方法`，而是 `根据问题和限制，把不同方法组合起来`。

在实际阅读文章或开会时，如果先判断 `现在最准确的说法应该是哪一个`，混乱会减少很多。

| 现在要说明的对象 | 首先该用的词 | 原因 |
| --- | --- | --- |
| 服务整体的智能功能范围 | AI | 因为它可以把搜索、规则、模型、人工复核一起包含进去。 |
| 通过数据学习关系并做预测或分类的那一部分 | machine learning | 因为这里核心是学习出来的模型，而不是手写规则。 |
| 基于神经网络的表示学习和大模型结构 | deep learning | 因为在 machine learning 内部，神经网络结构是这里的中心。 |
| 生成文本、图像、代码等新输出的体验或服务 | generative AI | 因为对用户来说，核心体验是生成而不是分类。 |
| 处理语言输入和输出的大型模型 | LLM | 因为它能在 generative AI 内部更准确地指向语言模型。 |

## Part 2 的语言会在哪里再次出现

Part 2 里学过的表达方式，会立刻在 Part 4 里重新出现。

| Part 2 里的表达 | 在 Part 4 中重新出现的方式 |
| --- | --- |
| row、column | 用来表示 sample 和 feature。 |
| array、shape | 用来说明输入数据 `X` 的形状。 |
| label | 在监督学习里会表现成目标值 `y`。 |
| function | 会变成把输入变成输出的计算。 |
| loss、error | 会变成衡量预测错了多少的标准。 |
| mean、variance | 会再次用于阅读数据分布和评估结果。 |
| plot | 会用于查看学习结果、误差、分布和决策边界。 |

在 scikit-learn 文档里，输入数据 `X` 也通常会被解释成 `行是 sample、列是 feature` 的矩阵。监督学习里，目标值 `y` 会和它一起出现，模型先通过 `fit` 学习，再通过 `predict` 对新输入计算结果。

## 一开始最先要避开的误解

开始 Part 4 时，最先要避开的误解有下面这些。

- 不要把 AI 当成 machine learning 的同义词。
- 不要把 machine learning 当成 deep learning 的同义词。
- 不要把 deep learning 当成 LLM 的同义词。
- 不要把使用 LLM 的经验当成整个 AI 的标准。
- 不要把知道很多模型名字，当成已经理解 machine learning。
- 不要把训练数据上拟合得好，当成真正把现实问题解决得好。

Part 4 的核心不是模型目录，而是数据、学习、评估这条流程。算法名字必须放进这条流程里理解。

## 案例与示例

### 案例 1. 用过聊天机器人，并不等于已经懂了整个机器学习

假设有一位学习者重新开始学 AI，而他已经经常使用聊天机器人和图像生成工具。于是他很容易觉得：`AI 最后不就是 LLM 或 generative AI 吗？`

因为现在很多 AI 服务体验都是以 LLM 为中心进入的，所以这种想法会很自然地出现。但如果把服务内部拆开来看，会发现 search、rule-based filter、recommendation model、policy judgment、human review 可以一起工作，而 LLM 只是其中的一个部分。

这也正是本节要把 AI、machine learning、deep learning、generative AI、LLM 的包含关系分别立住的原因。LLM 经验是理解现代 AI 的重要起点，但如果把它当成代表整个 AI 的唯一名字，Part 4 里要重新看的数据、模型、学习、评估流程就会被遮住。

真正可检查的结果，会在把服务结构拆成问题之后显现出来。如果某一部分由 search 负责、另一部分由分类模型负责、还有一部分由 LLM 负责生成回答，那么光靠 `AI = LLM` 这个简单等式已经解释不够了。

```mermaid
--8<-- "assets/part-04/chapter-01/ai-llm-scope-misconception-flow-zh.mmd"
```

## 本节要记住的视角

- AI 是最大范围，machine learning 是其中从数据中学习的方法，而 deep learning 又是 machine learning 里以神经网络为中心的一条路线。
- generative AI 和 LLM 是现代 AI 经验里非常重要的部分，但不能把它们当成整个 AI。
- 真实服务里，规则、搜索、machine learning model、LLM、人工复核往往会一起工作。
- Part 4 之所以先看 machine learning，是因为数据、模型、学习、评估这些共同问题，在后面的 deep learning 和 LLM 里还会不断回来。

## 检查清单

- 能不能说明为什么 `AI`、`machine learning`、`deep learning`、`generative AI`、`LLM` 不能当成可互换的名字？
- 能不能说明为什么就算表面上看见的是 LLM，服务内部仍可能同时包含规则、搜索、model 和人工复核？
- 能不能说明为什么 Part 4 不是直接跳到 deep learning 或 LLM，而要先看 machine learning 的结构？

## 什么时候要先想到这个视角

- 当讨论太快地从聊天机器人经验跳到 `AI = LLM` 时，要先回到这一节。
- 当需要区分现在谈的是整个服务、学习出来的 model，还是其中的语言模型组件时，就回到这里。
- 当要把 Part 2 的工具语言重新接到 Part 4 的 machine learning 流程里时，这一节就是基准。

## 来源与参考资料

- Google, `Machine Learning Glossary`, 包含 `machine learning`、`deep learning`、`LLM` 等条目，确认日期：2026-07-10. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- IBM, `What is machine learning?`, 确认日期：2026-07-10. [https://www.ibm.com/think/topics/machine-learning](https://www.ibm.com/think/topics/machine-learning){: target="_blank" rel="noopener noreferrer" }
- IBM, `What is deep learning?`, 确认日期：2026-07-10. [https://www.ibm.com/think/topics/deep-learning](https://www.ibm.com/think/topics/deep-learning){: target="_blank" rel="noopener noreferrer" }
