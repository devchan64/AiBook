# Part 4. 机器学习

> Section ID: `P4-index`
> Version: `v2026.07.20`

Part 2 重新补回了阅读公式、Python、数组、表格、图表和运行环境的基础。现在在 Part 4，我们要整理这些工具究竟是为了什么而使用，也就是 `从数据中学习规则` 这句话到底是什么意思。

很多读者已经用过 AI 服务，但这里更重要的是把这些经验重新整理成标准概念。与其背模型名字，不如先弄清楚什么算机器学习问题、需要收集什么数据、模型学到的是什么、什么叫学习得好、以及为什么有些模型看起来很准却依然可能在实际中有风险。

Part 4 的核心目标，是把机器学习读成 `问题 - 数据 - 学习 - 评估 - 应用` 的流程，而不是模型目录。线性回归、逻辑回归、决策树、随机森林、Boosting、聚类、降维、强化学习都不是需要分开背诵的项目。它们是在 `要解决什么问题、输入和输出是什么、用什么标准判断好坏` 的前提下出现的选择。

Part 4 也遵守同样的原则：在同一个 Part 内，核心概念尽量先在一个代表性 Section 里集中说明，后续 Section 只保留当前语境所需的最小解释。所以 `supervised learning` 先以 `P4-2.1` 为代表说明位置，`unsupervised learning` 先以 `P4-2.2` 为代表说明位置，`reinforcement learning` 先以 `P4-2.3` 为代表说明位置，`validation` 与 `test` 的角色区分放在 `P4-4.2`，`overfitting` 与 `underfitting` 放在 `P4-5.1`，`metric` 放在 `P4-6.1`，`feature selection` 放在 `P4-7.1`，`preprocessing` 放在 `P4-7.2`，`baseline` 放在 `P4-8.2`，`linear regression` 放在 `P4-10.1`，`logistic regression` 放在 `P4-11.1`，`k-NN` 放在 `P4-12.1`，`SVM` 放在 `P4-13.1`，`decision tree` 放在 `P4-14.1`，`random forest` 放在 `P4-15.1`，`gradient boosting` 放在 `P4-16.1`，`clustering` 放在 `P4-17.1`，`dimensionality reduction` 放在 `P4-18.1`。再次出现时，要和 [概念词汇表](/AiBook/en/reference/concept-glossary/) 以及当前语境一起读。

所以，Part 4 会按下面这个顺序把机器学习的地形图重新连起来。

1. AI、机器学习、深度学习之间的区分
2. 监督学习、无监督学习、强化学习之间的差异
3. 数据切分、验证、过拟合、泛化、评估指标
4. 特征选择、预处理、模型选择、基准模型、调参
5. 代表性传统模型的直觉
6. 向聚类、降维、强化学习的扩展
7. 为进入 Part 5 深度学习而整理的共同视角

## 这一 Part 处理的主要问题

Part 4 不是先把算法名字排出来，而是先立住阅读机器学习说明时反复要抓住的问题。

- 什么样的问题会分成 supervised learning、unsupervised learning、reinforcement learning？
- input、output、label、reward 各自是什么意思，又是在什么位置分开的？
- 为什么 training、validation、test 要分开，generalization 又是怎么确认的？
- metric 会揭示什么错误，又可能遮住什么错误？
- 为什么 feature selection、preprocessing、基准模型、tuning 要比模型名字更先检查？
- 代表性的传统模型能带来什么问题感，它们的强项到哪里、局限又从哪里开始？

## 把机器学习读成共同问题与判断标准

这一 Part 的任务，是先抓住机器学习的大结构，把很久以前学过的入门知识重新接回标准流程。

机器学习之所以难，不只是因为算法很多。就算面对同一份数据，随着问题定义方式不同，它也会被读成 classification、regression、clustering、dimensionality reduction 或 reinforcement learning。比起先选模型，更重要的是先理解为什么 training data、validation data、test data 要分开，为什么 overfitting 和 generalization 要分开看，以及 metric 应该怎么读。

Part 4 要把这层基础立住。目标不是把所有算法的数学都深挖，而是让读者在读机器学习说明时，能够自己复原这条流程：定义问题、看数据、决定输入和输出、决定模型学什么、分开学习和评估、阅读指标、检查模型的局限与适用条件。

这里还要直接带上在 P1-8 建立的三分法。监督学习，是在同时有 `输入和标签` 的例子里匹配目标输出的问题；无监督学习，是在 `没有人工贴好标签` 的情况下寻找结构与表示的问题；强化学习，则是在 `不是标签而是动作之后返回的奖励` 上调整策略的问题。特别是，强化学习里的 reward 不是监督学习里的 label，这个区分会在 Part 4 全篇里持续保持。

## 机器学习中要收住的核心问题

读完 Part 4 后，希望至少形成下面这一级别的理解。

- 能从大体流程上说明 AI、machine learning、deep learning 之间的关系。
- 能从数据与问题定义的角度区分 supervised learning、unsupervised learning、reinforcement learning。
- 能说明 training data、validation data、test data 为什么要分开。
- 能解释 overfitting、underfitting、generalization 的差别。
- 能理解 metric 既是模型的数字表现，也是和业务判断相连的标准。
- 能说明 feature selection、preprocessing、model selection、基准模型、tuning 的作用。
- 能区分 linear regression、logistic regression、decision tree、random forest、gradient boosting 的直觉与使用场景。
- 能把 clustering 和 dimensionality reduction 解释成 `在没有答案标签时阅读结构` 的方法。
- 能把 reinforcement learning 理解成通过动作和奖励来调整策略的学习，并在入门层面区分 value-based 和 policy-based 的差别。

## 机器学习要解释的边界与留下的问题

Part 4 是说明机器学习共同结构的 Part。因此，在正文范围内会解释下面这些内容。

- supervised learning、unsupervised learning、reinforcement learning 的大区分
- 数据切分、验证、过拟合、泛化、评估指标
- 特征选择、预处理、基准模型、模型选择、调参
- 代表性传统模型、聚类、降维、强化学习的直觉

相对地，下面这些内容不会在这一 Part 全部深入展开。

- 各个算法严格的数学推导与证明
- 大规模超参数搜索的自动化体系
- 最新深度学习结构和大型生成模型的内部计算

这里的省略不是回避，而是范围控制。Part 4 的责任，是立住 `阅读机器学习时共同要问的问题`。深度学习正文和大型生成模型说明，会在后续 Parts 中实际回收。

## 这里究竟解释什么

Part 4 大致由四条流程组成。

首先重新建立机器学习内部的大区分。先看 AI、机器学习、深度学习之间的关系，再整理监督学习、无监督学习、强化学习的差别。这一段的目标不是记住算法名字，而是理解 `问题类型是怎么不同的`。

在这里，读者最先要抓住的比较轴是学习信号。监督学习读取人工贴上的标签，无监督学习读取没有标签的结构，强化学习读取动作之后返回的奖励。如果这个区分不稳，后面关于分类、聚类、价值型强化学习的说明就不会再被读成不同的问题设定。

接下来处理阅读学习的共同基础。这里包括数据切分、验证、过拟合、泛化、评估指标、特征选择、预处理、模型选择、基准模型、调参。这一段是 Part 4 的中心，因为无论后面遇到什么算法，读者最终都要重新追问：数据是怎么拆开的、模型学到了什么、分数该怎么读、现在看起来不错的结果到底能不能信。

评估指标的范围也会在这条流程里明确下来。Part 4 正文里优先处理的是那些能够先抓住 `面对这种问题应该先问什么` 的指标，比如 accuracy、precision、recall、F1、MAE、RMSE、R2。像 ROC、PR、log loss、calibration、reliability、silhouette 这类会让分数解释更细致的项目，会放到 P4-6.4 的补充学习里做入门说明，而 threshold 与 calibration 会在 P4-15.3 再次回收。

这里读者还要同时抓住两个比较装置。confusion matrix 和 error case 让你读出 `模型错在了哪里、怎么错的`，baseline 则要求你追问 `这个分数到底算不算有意义的提升`。Part 4 更看重的是培养把错误结构和基线一起阅读的习惯，而不是把分数当作独立数字背下来。

这条流程按下面顺序来读。

| 评估阅读顺序 | 先检查的问题 | 为什么需要 |
| --- | --- | --- |
| confusion matrix | 模型在哪些格子里错得最多？ | 它能先揭示只看 accuracy 时被遮住的错误方向。 |
| 代表性 error case | 模型到底在什么输入上、因为什么而错？ | 它能暴露光看数字时看不见的数据问题和边界情形。 |
| baseline 比较 | 这个提升真的有意义吗？ | 它能区分 `因为问题很容易所以看起来高` 和 `真的变好了`。 |

在 Part 4 前半段尤其要先抓住的评估，是下面三步。

| 先看什么 | 紧接着要问的问题 | 下一节会继续到哪里 |
| --- | --- | --- |
| confusion matrix 和 error case | 错在了哪里、漏掉了什么输入？ | P4-6 评估指标 |
| baseline 比较 | 这个分数真的比简单基准更好吗？ | P4-8 基准模型 |
| tuning 结果 | 小幅分数上升值得付出成本和复杂度吗？ | P4-9 超参数 |

这个顺序也可以再压缩成下面三行。

| 阅读评估的最小顺序 | 为什么这个顺序要先来 |
| --- | --- |
| confusion matrix | 因为必须先看到模型错在什么地方，才读得出分数的方向。 |
| 代表性 error case | 因为必须先看到真实输入，才能检查数据问题和边界情况。 |
| baseline 比较 | 因为只有到最后，才能判断这点差异是否真的是有意义的提升。 |

贯穿整个 Part 4 的记录语言，也会在这条流程里一起固定下来。即使某个分数或结构看起来很像那么回事，也要先把应该记成事实的东西，与还需要更多检验的解释分开记录。

| 在这一 Part 里反复要留下的内容 | 最短记录语言 |
| --- | --- |
| 实际看到的分数、结构、比较结果 | fact |
| 这些结果到底能信到哪里、又该在哪一步停下来 | interpretation |
| 下一次实验或下一项要检查的问题 | next question |

接着会去看代表性的传统模型。这里会处理 linear regression、logistic regression、k-NN、SVM、decision tree、random forest、gradient boosting，并看它们各自擅长什么、又该从哪里开始谨慎。这里的目标不是公式推导，而是建立问题感。

在这里，更重要的不是背模型名字，而是像下面这样确认：`在一个小型数据场景里，首先应该联想到什么`。

| 小型数据场景 | 首先联想到的模型族 | 为什么它是起点 |
| --- | --- | --- |
| 需要用数值输入预测连续值 | linear regression | 因为它适合最快检查最简单的关系与 baseline。 |
| 需要区分 yes/no 或若干类别 | logistic regression、decision tree | 因为它们适合比较分类问题的基本基线和规则感。 |
| 在表格型数据上需要强性能候选 | random forest、gradient boosting | 因为它们是处理非线性关系和特征交互的代表性选择。 |
| 想在没有标签时先看相似分组 | clustering | 因为它是阅读无答案结构的最直接起点。 |
| 变量太多，想先减少坐标轴 | dimensionality reduction | 因为此时表示压缩和可视化比预测更优先。 |
| 面对动作结果会延后返回的问题 | reinforcement learning | 因为这里最核心的是 state、action、reward 结构，而不是输入-答案对。 |

最后，这一 Part 会向无监督学习和强化学习扩展。通过聚类、降维和强化学习算法，把 `不只是学会把答案猜对` 的领域也纳入机器学习这一点整理清楚。

## 为什么需要这一 Part

仅仅有使用 AI 服务的经验，还不足以说已经理解了整个机器学习。像 `模型被 fit 在训练数据上`、`validation 分数升了但 test 分数反而掉了`、`改了特征预处理之后 overfitting 降低了`、`虽然比 baseline 高了 1%，但业务意义还不明确` 这样的说法会非常常见。

要读懂这些句子，必须先懂结构，再看算法名字。你需要知道 `fit` 究竟意味着什么、为什么 validation 和 test 要分开、为什么性能提升并不会自动等于可以上线。

另外，还经常会出现下面这些误解。

- 只要换模型，性能问题就会解决。
- 只要某一个分数高，系统就是好的。
- 数据一多，generalization 就会自动变好。
- 强化学习会自己学，所以现实里多试试就行。

Part 4 正是用来减少这些误解的。它提供的不是模型目录，而是阅读、比较、怀疑机器学习说明所需要的基本素养。

## 这一 Part 不打算在这里结束的问题

因为 Part 4 解释的是机器学习的共同结构，所以会有意识地把下面这些问题留到 Part 5 和 Part 6。

- representation learning 为什么会成为比传统模型更大的转折点？
- gradient、loss、optimizer 会怎样在神经网络里延伸成更大的计算结构？
- 生成模型和大型语言模型会怎样扩展这一共同结构？

这些问题会在后续正文中回收：representation learning 和神经网络计算结构放在 Part 5，生成模型和 LLM 的扩展放在 Part 6。

## 学完这一 Part 后会形成的理解

读完这一 Part 后，机器学习就不再只是模型名字列表，而会被看成一条工作流程：定义问题、选择数据、决定输入和输出、训练模型、检查是否泛化、阅读指标、检视适用条件和局限，这些步骤会连成一体。

一旦形成这种理解，linear regression、logistic regression、random forest、clustering、reinforcement learning 就不再像互不相干的名字。它们会显现为面向不同问题的选择，而在它们之前总有数据定义和评估标准，在它们之后总有适用边界和运营判断。

换句话说，Part 4 不是模型名称集合，而是反复留下 `问题结构 -> 检查标准 -> 下一问题` 的 Part。这里的检查标准，不应立刻跳到原因定论或策略结论，而应该先留下 `还需要进一步检查的信号` 和 `下一步该按什么顺序确认`。

## 完成标准

- 能从 supervised learning、unsupervised learning、reinforcement learning 的角度区分机器学习问题。
- 能说明 training、validation、test 数据为什么要分开。
- 能结合例子说明 overfitting、underfitting、generalization 的差别。
- 能说明评估指标会随着问题类型和业务目标而变化。
- 能区分 feature selection、preprocessing、基准模型、tuning 的作用。
- 能以入门层面说明 linear regression、logistic regression、decision tree、random forest、gradient boosting 的直觉和差异。
- 能说明 clustering 和 dimensionality reduction 是阅读无标签数据结构的方法。
- 能把 reinforcement learning 理解成围绕动作和奖励展开的学习，并说明它在应用时的注意点。
- 能说明为什么 Part 4 会把 deep learning 单独处理，以及它如何向后连接。

## 来源与参考资料

这个概览页是整理 Part 4 目的与学习路径的内部概览，不直接引用外部资料。
