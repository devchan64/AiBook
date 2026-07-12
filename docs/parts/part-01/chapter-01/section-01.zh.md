# P1-1.1 AI 这个词的范围

> Section ID: `P1-1.1`
> Version: `v2026.07.12`

重新学习 AI 时，第一个困难往往不是技术本身，而是这个词的范围。同一个 `AI`，在某些语境里指规则式程序，在另一些语境里指机器学习模型，最近又常被几乎等同于生成式 AI 或 LLM。

这一节不是要用一句完美的话把 AI 一次性定义完，而是整理这个词的范围，让后面关于规则式系统、机器学习、深度学习、生成式 AI 和 LLM 的内容都能放在同一张地图上阅读。

在 Part 1 中，`AI` 是最外层、最宽的类别。后面的 Section 再次出现这个词时，只保留当前问题所需的最小连接；如果需要重新拆分这个范围，就回到这一节，以及 [Concept Glossary (English)](/AiBook/en/reference/concept-glossary/)。

## 这一节的范围

这一节整理以下问题：

- 为什么 AI 这个词会被用得这么宽？
- 规则式 AI、机器学习、深度学习、生成式 AI 分别坐落在怎样的一张大地图里？
- 为什么把最近的 LLM 使用经验当成整个 AI，会带来混乱？

这一节不会深入展开以下内容：

- 机器学习算法的细部结构
- 深度学习训练过程的内部实现
- 生成式 AI 产品的比较，以及最新模型谱系

这些更细的技术脉络，会在 Part 1 Chapter 2、Chapter 3，以及 Part 4 之后重新展开。这里先固定一条基准线：`AI 是最外层、最宽的类别`。

## 这一节的目标

- 解释为什么 AI 这个词会被广泛使用。
- 把 AI 看成处理问题的领域，而不是某一个产品或某一个最新模型的名字。
- 把 AI、机器学习、深度学习、生成式 AI 之间的关系，整理到后面章节还能继续复用的程度。

## 先连起来的概念

这一节也是几个核心术语第一次被同时引入的入口。下面这些概念先只固定最短含义；如果之后需要更完整的定义，再回到对应词条。

| 概念 | 这里先固定的意思 | 为什么现在需要 |
| --- | --- | --- |
| [AI](/AiBook/en/reference/concept-glossary/#ai-artificial-intelligence) | 最宽的外层类别 | 为了把后面出现的多种方法放在同一张地图上 |
| [machine learning](/AiBook/en/reference/concept-glossary/#machine-learning) | 从数据中学习模式的方法 | 为了区分规则式方法和学习式方法 |
| [deep learning](/AiBook/en/reference/concept-glossary/#deep-learning) | 用神经网络学习复杂表征的一条技术主线 | 为了固定机器学习内部的重要扩展方向 |
| [generative AI](/AiBook/en/reference/concept-glossary/#aigenerative-ai) | 生成文本、图像、音频等结果的一条技术流 | 为了避免把最近的 AI 经验理解得过窄 |
| [LLM](/AiBook/en/reference/concept-glossary/#llm) | 以语言数据为中心的大规模语言模型 | 为了区分生成式 AI 和 AI 整体 |
| [system](/AiBook/en/reference/concept-glossary/#system) | 接收输入并产出结果的实际实现结构 | 为了区分“领域”与“实现” |
| [input](/AiBook/en/reference/concept-glossary/#input) | 系统接收的信息 | 为了阅读系统依据什么做判断 |
| [output](/AiBook/en/reference/concept-glossary/#output) | 系统产生的结果 | 为了阅读分类、推荐、生成等差异 |
| [goal](/AiBook/en/reference/concept-glossary/#goal) | 为什么要得到某种输出的目的 | 为了看到同样的输出也可能服务于不同目的 |
| [prediction](/AiBook/en/reference/concept-glossary/#prediction) | 根据当前信息估计结果 | 为了避免和生成、推荐、分类混成一类 |
| [recommendation](/AiBook/en/reference/concept-glossary/#recommendation) | 在多个候选中挑出接下来值得看的内容 | 为了看出 AI 不只是在生成答案 |
| [rule-based system](/AiBook/en/reference/concept-glossary/#rule-based-system) | 由人写规则并导出结论的系统 | 为了避免把 AI 缩窄成只有最近的学习模型 |

## 主要学习点

这一节会出现很多术语，但只要不把它们一开始就当成处在同一概念层级，整体结构其实并不难。下面三点就是这节的总地图。

| 基准 | 为什么重要 | 这一节需要达到的理解程度 |
| --- | --- | --- |
| `AI` 不是某一个产品名，而是宽广的领域 | 这样才不会把机器学习、深度学习、LLM 混成整个 AI。 | 先把 AI 固定成最外层、最宽的类别。 |
| 即使都叫 `AI`，不同时代的实现方式也不同 | 这样才看得见规则、搜索、概率、学习、深度学习为什么会一起出现。 | 先区分 AI 的定义与 AI 的实现方式并不是同一回事。 |
| 最近的 LLM 只是 AI 内部的一条技术流 | 这样能减少把当前产品经验误读成整个 AI 的情况。 | 把生成式 AI 与 LLM 看成宽大地图后半段的技术流。 |

`领域(field)`、`系统(system)`、`输入(input)`、`输出(output)`、`目标(goal)` 一开始听起来很像，这里先这样分工：

| 术语 | 最短意思 | 这一节里的角色 |
| --- | --- | --- |
| 领域 | 把多个问题和方法包在一起的宽广学术与技术范围 | 把 AI 读到最宽时所处的位置 |
| 系统 | 实际接收输入并产出结果的实现结构 | 规则式系统、推荐系统、聊天机器人等例子 |
| 输入 | 系统接收的信息 | 句子、记录、图像、传感器值 |
| 输出 | 系统产生的结果 | 分类、推荐、预测、生成结果 |
| 目标 | 为什么某种输出算“好”的目的 | 审批辅助、推荐、搜索、回答生成 |
| 影响 | 输出对人的判断或环境造成的结果 | 审批决定、排序变化、工作流变化 |

这一节最先应该留下的基准，是 `AI 是宽广领域`，而 `AI 系统是具有输入、目标与输出的结构`。这里之所以把 `影响(impact)` 也放进来，是因为同一种输出在真实环境中可能导致完全不同的后果。

例如，若把“在线商店的商品推荐”压缩成一行：AI 是包含这类推荐问题的宽广领域；`recommendation system` 是实际实现的系统；输入是点击记录与购买记录；输出是推荐商品列表；目标是挑出用户下一步可能愿意看的商品；`impact` 是某些商品被更频繁地曝光，用户的选择路径也会随之变化。即使后面换成别的案例，也最好先拆成这六格，而不是直接去背术语。

## 细化学习

### AI 不是某一种技术的名字

AI 更接近于一个宽广的研究领域与系统类别，而不是某一种单独技术的名字。所以，若只从“这是不是在真正思考？”开始理解 AI，阅读很快就会卡住。更稳定的起点，是先问：“它想解决什么问题？又是用什么方式去解决？”

下棋时寻找下一步的系统、识别图像中物体的模型、翻译句子的模型、回答用户问题的聊天机器人，从表面上看差异很大。但它们共享一个宽泛结构：接收输入，经过某种计算过程，产生输出、决策、推荐、预测或生成结果。

在主要英语词典、东亚参考资料和机构定义中，AI 通常都被解释为：计算机系统、机器或算法执行或模拟与人类智能相关的一部分功能。反复出现的功能包括语言、图像、问题求解、学习、预测、推荐和决策。

因此，本书会这样理解 AI：

> 人工智能(artificial intelligence, AI) 是一个宽广的总称，它既指相关研究领域，也指那些被设计出来、用以执行与人类智能相关部分功能的计算机系统、机器与算法。

在理解 AI 时，图灵测试(Turing test) 也仍然是重要的历史起点。图灵没有直接去定义“机器能否思考”，而是把问题改写成：人能否仅通过对话区分出对面是机器还是人。这个转向，是早期用可观察行为而不是不可见内部结构来讨论智能的代表性尝试。

但图灵测试本身并不足以解释现代 AI 的全部。今天我们不仅要问它在对话中看起来是否像人，还要问它用了什么数据、训练了怎样的模型结构、通过了什么评估标准，以及它在真实环境里造成什么影响。因此，这本书不会把图灵测试当作 AI 定义的全部，而是把它看成“我们应如何判断智能”这一问题的早期开端。

OECD 在 2023 年的说明，把 AI 系统描述为一种基于机器的系统：它在显式或隐式目标之下，接收输入，并生成预测、内容、推荐、决策等输出。这个定义强调的不是“它像不像人一样思考”，而是输入、目标与输出之间的关系。

这和本书的出发点是一致的。本书不会先把 AI 理解成“完整复制人类智能”，而是把它读成：把问题转成可计算形式，并生成会影响环境的输出的系统。

### 为什么 AI 这个词会越来越宽

AI 这个词之所以显得很宽，是因为它并不只指某一个算法，而是把多个时代的问题求解方式一起装了进去。早期 AI 的核心，是显式设计规则(rule)、知识(knowledge)和搜索过程(search procedure)。当可能答案太多时，就用启发式(heuristic)减少搜索范围。

随着数据量增大、存储与处理基础设施扩展，AI 叙述的中心也逐渐转向“从数据里学判断标准”。数据挖掘(data mining)和数据驱动的决策支持流程虽然不等于 AI 模型本身，但它们构成了一个重要背景：收集数据、分析数据，再把分析结果接到判断上，变得越来越常见。

在这样的背景下，机器学习(machine learning) 成为一种主要方法：不再要求人把每条规则都写死，而是让系统从数据里学习模式。深度学习(deep learning) 又在此基础上，把神经网络(neural network)、权重(weights)和表征学习(representation learning) 结合起来，进一步扩展到更复杂的输入和输出。

因此，这本书不会只把 AI 理解成“像人一样行动的机器”。它会把人直接写规则的方法、从数据中学习判断标准的方法，以及把这些结果接到服务和决策上的方法一起放在同一张地图上。

| 层级(level) | 产生判断的方式 | 这一节中的位置 |
| --- | --- | --- |
| 规则式 AI | 人显式写规则和知识 | 属于 AI 内部较早的一类方法 |
| 搜索与启发式 | 搜索候选，但用经验标准缩小范围 | 在 Part 1 Chapter 7 重新展开 |
| DSS/BI/DW/OLAP | 收集数据并把它连接到决策 | AI 周边以数据为中心的系统背景 |
| 数据挖掘与机器学习 | 从数据中发现模式与预测标准 | 在 Part 1 Chapter 3 之后及 Part 4 重新展开 |
| 深度学习与生成式 AI | 学习表征与权重来产生复杂输出 | 在 Part 1 Chapter 9 之后及 Part 5、Part 6 重新展开 |

这样的区分，是为了避免把词典式定义和历史演化混成一团。词典意义上的 AI，是执行与人类智能相关功能的系统或领域；历史演化上，完成这些功能的实现方式，则经历了规则、搜索、概率、数据学习和深度学习的扩展。

### AI 的范围会随语境变化

AI 这个词会因语境不同而有不同用法。

| 表达 | 常见使用语境 | 需要注意什么 |
| --- | --- | --- |
| AI | 具有“智能”行为的系统整体 | 太宽时，具体实现方式会消失 |
| machine learning | 从数据中学习模式或关系的方法 | 不是所有 AI 都是机器学习 |
| deep learning | 用神经网络学习复杂表征的方法 | 不是所有机器学习都是深度学习 |
| generative AI | 生成文本、图像、音频、代码的模型与服务 | 会生成不等于内容就一定真实 |
| LLM | 大规模语言模型 | 不是所有生成式 AI 都是 LLM，即便用了 LLM，也未必等于整个服务 |

因此，这本书会先把 AI 放在最外层，再按问题求解方式把内部概念分出来。

```mermaid
--8<-- "assets/part-01/chapter-01/ai-scope-map-zh.mmd"
```

这张图是一张学习地图。它把 `AI` 放在最外层，并展示规则式方法、搜索与规划、概率推理、机器学习、深度学习、生成式 AI 与 LLM 之间的大致位置关系。重要的不是把每条箭头背成严格包含关系，而是看清：`LLM` 不是整个 AI，`rule-based approach` 也不是 AI 的外部，而是其内部的一条方法流。

### 本书用什么问题来读 AI

关键并不是一次性判断“它到底算不算 AI”，而是看眼前这个系统如何回答下面这些问题：

- 输入是什么？
- 输出是什么？
- 规则是人直接写的，还是系统从数据里学出来的？
- 它怎样处理不确定性？
- 它的结果会怎样影响真实环境或用户判断？

有了这些问题，宽泛的 “AI” 才能被切成更稳定、更小的单位。后面会再出现的规则式 AI、启发式、概率、机器学习、深度学习、LLM，都可以重新放回这套框架里。

### 一个简短的区分练习

试着先为下面三个场景写出它们的 `input`、`output` 和 `decision style`。这样做会让 “AI” 这个词的范围稳定得多。

| 场景 | 输入是什么？ | 输出是什么？ | 人应先问什么？ |
| --- | --- | --- | --- |
| 贷款初筛规则表 | 申请金额、收入、逾期记录 | 暂缓、进一步审查、拒绝 | 规则是人直接写的，还是从数据里学出来的？ |
| 商品推荐模型 | 用户点击记录、购买记录、商品信息 | 推荐商品排序列表 | 模式是否来自历史数据学习？ |
| 文档摘要聊天机器人 | 用户问题、原始文档、系统指令 | 摘要句子、回答句子 | 它只是生成，还是还结合了检索与规则？ |

这个练习的重点，不是马上决定“算不算 AI”，而是先区分：即使都属于 AI，这里面也可能有人直接写规则，也可能是系统从数据里学习，也可能是生成模型再加上检索与规则。

## 案例与示例

### 案例 1. 把聊天机器人当成整个 AI

如果一个用户第一次接触的 AI 只有聊天机器人，就很容易觉得：`AI 就是回答问题的服务。` 但在同一个组织里，可能同时还存在规则式审批系统、推荐系统、搜索排序模型和需求预测模型。人自然会围绕最显眼的对话体验来缩窄地定义 AI。本书采用的更稳定基准，是先问：它接收什么输入，又产生什么输出。这个案例说明：最近的 LLM 经验可以是 AI 的代表性案例之一，但并不等于整个 AI。

### 案例 2. 规则式系统也可以落在 AI 范围内

假设一个贷款审核系统只用人工写好的规则表来做初筛。读者可能会觉得：没有训练数据，也不会聊天，这好像不是真正的 AI。可这个系统依然会接收输入，依据规则和目标给出判断，并且影响人的决策与环境。从这个更宽的意义上说，它仍可以被放进 AI 里，作为“被设计出来、执行与智能相关部分功能的系统”。这个案例说明：如果把 AI 缩窄成只有最近的学习模型，就会漏掉很重要的一层。

## 检查清单

- 你可以说明：AI 不仅是某种技术名，也是一种宽广的领域与系统类别。
- 你可以说明：若把 AI、机器学习、深度学习、生成式 AI、LLM 当成同一层级的词，会产生什么混乱。
- 你可以区分词典式意义与历史扩展后的使用语境。
- 你可以从输入、目标、输出和影响的角度来看 AI 系统。
- 你可以区分“生成结果读起来很自然”和“生成结果是真的”并不是一回事。
- 你可以说明：AI 不是某一个产品名，而是一个以输入、目标与输出来组织的宽广系统类别。
- 你可以说明：如果只用最近的生成式 AI 使用经验来定义整个 AI，就很容易忽略规则式系统、搜索、推荐和预测等其他层次。

## 来源与参考

- OECD.AI, Stuart Russell, Karine Perset, Marko Grobelnik, [Updates to the OECD’s definition of an AI system explained](https://oecd.ai/en/wonk/ai-system-definition-update){: target="_blank" rel="noopener noreferrer" }, 2023-11-29, 确认日期: 2026-06-22.
- NIST AI Resource Center, [Glossary](https://airc.nist.gov/glossary/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-22.
- Merriam-Webster, [Artificial intelligence Definition & Meaning](https://www.merriam-webster.com/dictionary/artificial%20intelligence){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-22.
- Cambridge Dictionary, [Meaning of artificial intelligence in English](https://dictionary.cambridge.org/dictionary/english/artificial-intelligence){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-22.
- Britannica Dictionary, [Artificial intelligence Definition & Meaning](https://www.britannica.com/dictionary/artificial-intelligence){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-22.
- 汉典, [人工智能](https://www.zdic.net/hans/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, 确认日期: 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-22.
- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://doi.org/10.6028/NIST.AI.600-1){: target="_blank" rel="noopener noreferrer" }, NIST AI 600-1, 2024-07, 确认日期: 2026-06-22.
- Wayne Xin Zhao et al., [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223){: target="_blank" rel="noopener noreferrer" }, arXiv:2303.18223, 确认日期: 2026-06-22.
- Usama M. Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, [From Data Mining to Knowledge Discovery in Databases](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" }, AI Magazine, 1996, 确认日期: 2026-06-22.
- D. J. Power, [A Brief History of Decision Support Systems](https://dssresources.com/history/dsshistory.html){: target="_blank" rel="noopener noreferrer" }, DSSResources.COM, version 4.0, 2007-03-10, 确认日期: 2026-06-22.
