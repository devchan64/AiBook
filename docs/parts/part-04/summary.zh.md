# Part 4 总结：机器学习整理

> Section ID: `P4-summary`
> Version: `v2026.07.12`

Part 4 是把机器学习重新整理成 `问题定义、数据结构、学习、评估、应用` 这一条流，而不是模型名字清单的一段。这里先处理的是深度学习以前的传统模型，但目的并不是整理老技术目录，而是把那些到了下一 Part 的神经网络、再下一 Part 的 LLM 和生成式 AI 里仍然会反复出现的共同问题固定下来。

这一 Part 最重要的目标，是先形成这样一种习惯：比起先问 `模型在算什么`，更早要问 `它在解决什么问题`、`它在读什么数据`、`这个结果到底凭什么可信`。监督学习、无监督学习、强化学习都在从数据里学东西，但它们的输入输出定义、学习信号、评估标准和应用风险并不一样。

重新翻开 Part 4 时，最快的方法是抓住代表性 Section。学习类型划分先看 `P4-2.1` 到 `P4-2.3`，validation 和 test 的区分在 `P4-4.2`，overfitting 和 underfitting 在 `P4-5.1`，评估指标在 `P4-6.1`，feature selection 和 preprocessing 在 `P4-7.1` 到 `P4-7.2`，基准模型在 `P4-8.2`，linear regression 在 `P4-10.1`，logistic regression 在 `P4-11.1`，`k-NN` 在 `P4-12.1`，`SVM` 在 `P4-13.1`，decision tree 在 `P4-14.1`，random forest 在 `P4-15.1`，gradient boosting 在 `P4-16.1`，clustering 在 `P4-17.1`，dimensionality reduction 在 `P4-18.1`。同一 Part 里的后续 Section，如果能和这些代表位置以及 [概念词汇表](/AiBook/en/reference/concept-glossary/) 一起重读，语境就不容易散掉。

尤其要维持住在 P1-8 里固定下来的区分。监督学习是在匹配标签；无监督学习是在没有人工标签时读结构；强化学习则是通过行动后的 reward 来调整 policy，而不是通过标签。不要把强化学习里的 reward 读成监督学习里的 label，这是这一整 Part 里很重要的一条边界。

## 这一 Part 的目的

Part 4 的目的，是让机器学习被读成共同问题与判断标准的流程，而不是算法目录。

## 这一 Part 的目标

完成这一 Part 之后，读者应该能把问题定义、数据切分、泛化、评估指标、基准模型和应用边界一起读。

如果把这个目标压成最短的评估阅读顺序，会变成下面三行。

| 最先要留下的评估阅读顺序 | 为什么这个顺序重要 |
| --- | --- |
| confusion matrix | 因为只有先看错在什么地方，分数表遮掉的错误方向才会露出来 |
| representative error case | 因为只有看到真实输入场景，才读得到数据问题和边界案例 |
| baseline 比较 | 因为只有到最后，才能判断这个改进是不是真的有意义 |

## 这一 Part 走过的核心流程

Part 4 的流程可以整理成下面这样。

1. 重新固定 AI、machine learning、deep learning 的区分。
2. 分开 supervised learning、unsupervised learning、reinforcement learning。
3. 看数据切分、validation、overfitting 与 generalization。
4. 读评估指标与业务判断的连接。
5. 把 feature selection、preprocessing、model selection、基准模型、tuning 绑在一起看。
6. 看 linear regression、logistic regression、k-NN、SVM。
7. 看 decision tree、random forest、gradient boosting。
8. 看 clustering 和 dimensionality reduction。
9. 看 value-based、policy-based reinforcement learning 以及应用注意点。
10. 整理进入 Part 5 深度学习前需要保留的共同感觉。

这条流程并不意味着 `知道的算法名字越多，就越懂机器学习`。在这本书里，机器学习首先是一种阅读问题的语言，然后才是选择算法的系统。也就是说，比起 `哪个模型更有名`，更早的问题是 `这个问题应该通过什么学习结构来读`。

## 必须记住的概念

Part 4 里最应该长期带走的概念，是结构和标准。

| 区分 | 要记住的视角 |
| --- | --- |
| 问题定义 | 机器学习第一步，是先决定这个问题该读成 classification、regression、clustering 还是 reinforcement learning |
| 数据切分 | 把 train、validation、test 分开，是为了把模型拟合和可信评估分开 |
| 泛化 | 在训练数据上表现好，不等于在新数据上也表现好 |
| overfitting 与 underfitting | 太复杂是问题，太简单也是问题 |
| 评估指标 | metric 是一个数字，但它的意义会随着问题类型和成本结构改变 |
| 特征与预处理 | 模型表现不只取决于算法，也取决于保留了哪些特征、做了什么 preprocessing |
| 基准模型 | baseline 不是低起点，而是判断改进是否真正有意义的标准 |
| tuning | 性能可以提高，但 validation 成本和 overfitting 风险也会一起升高 |
| 传统模型 | linear regression、logistic regression、tree、random forest、boosting 各自对应不同的问题直觉与假设 |
| 无监督学习 | clustering 与 dimensionality reduction 是在没有正确标签时读取结构 |
| 强化学习 | reinforcement learning 通过行动和 reward 调整 policy，但因为 reward 设计和 exploration 成本，现实应用并不会立刻容易 |

如果把这些传统模型再压成最短的起点，可以写成下面这样。

| 如果场景像这样 | 先想到的起点 |
| --- | --- |
| 预测连续值 | linear regression |
| 类别分类 | logistic regression、decision tree |
| 在表格数据上比较强候选 | random forest、gradient boosting |
| 找无标签分组 | clustering |
| 压缩变量、做可视化 | dimensionality reduction |
| 优化行动结果 | reinforcement learning |

这个表的目的不是选出 `正确模型`，而是记住：一旦问题定义变了，最先比较的起点也会跟着变。

一旦这个连接固定下来，后面再看 deep learning，就不会只读成 `更大的模型`，而会看到同样的共同问题再次出现。

## 容易误解的地方

Part 4 里尤其要避免的误解有下面这些。

- 知道很多算法名字，并不会自动把问题定义好
- validation 分数高，并不直接证明现实部署价值
- test 分数不是可以反复拿来调参的记分板
- 特征加得越多，并不一定越能 generalize
- 比 baseline 稍微好一点，并不自动等于有实务价值
- 无监督学习里的 cluster 不能被读成正确标签
- 降维得到的 2D 图不能被直接读成原始数据的真相
- 强化学习因为常被说成 `会自己学习的 AI`，很容易被误读成在现实里也能随便 exploration
- 模型性能提升与运营绩效提升，并不是同一句话
- machine learning 和 deep learning 的差别，不能只被压成 `性能差异`

为了减少这些误解，这一 Part 一直把数据、指标、应用条件放在模型说明前面。Part 4 的关键，不是赞美或排斥某个具体模型，而是学会模型应该在什么条件下被阅读。

## 这一 Part 解释了什么，也没有解释什么

Part 4 集中在说明机器学习的共同结构。所以，各算法的严格证明、大规模 tuning 自动化、最新 deep learning 和生成模型的内部计算，都不会在这里结束，而是交给后面的 Parts。

## 这一 Part 故意不在这里收掉的问题

Part 4 故意把下面这些问题保持打开。

- 为什么神经网络会成为更强的 representation-learning 结构？
- loss、gradient、optimizer 会怎样在 deep learning 里重新出现？
- 生成模型和 LLM 会怎样扩展这套共同结构？

这些问题会在 Part 5 的神经网络与 representation learning，以及 Part 6 的生成模型与 LLM 里被实际收回来。

评估指标的范围，也可以用同样方式整理。Part 4 本篇集中在帮助读者理解 `在什么问题里，什么错误要先读`；而 ROC、PR、log loss、calibration、silhouette 这些更细的阅读工具，则被收进补充学习 P4-6.4。threshold 和 calibration 如何再接回实际决策 policy，则会在 P4-15.3 再回来，所以这里更稳的做法，是先把评估问题的骨架固定住。

出于同样原因，Part 4 的评估阅读不会用 `一张分数表` 就结束。先通过 confusion matrix 和 representative error case 读出 `错在什么地方`，再把它和 baseline 放在一起，问 `这个改进到底是不是有意义`。这就是 Part 4 的默认态度。只有这个轴固定住，后面的 tuning 或算法 Section 才能分开数字上涨和真实价值上涨。

再压短一点，就是下面这样。

| 先看什么 | 紧接着看什么 | 最后问什么 |
| --- | --- | --- |
| confusion matrix | representative error case | 是否比 baseline 有意义地更好？ |

这个问题结构，也会接到 Part 7 的项目回顾语言。

| 从 Part 4 先留下来的东西 | 在 Part 6 里重新使用的记录语言 |
| --- | --- |
| baseline、train/test、threshold 之类检查值 | fact |
| error case 和分差暗示了什么 | interpretation |
| 下一轮实验还要继续看什么指标、数据或 policy 调整 | next question |

无监督学习那一边，也可以用同样的语言来整理。

| 在 Part 4 的无监督学习里先留下什么 | 用同样结构重新写时的记录语言 |
| --- | --- |
| 最先看到了什么 grouping 或低维结构 | fact |
| 那个结构能信到哪里，解释应该停在哪里 | interpretation |
| 接下来应该用原始特征、不同参数或后续指标再确认什么 | next question |

所以，Part 4 里的监督学习和无监督学习虽然表面不同，但都建立在同一个原则上：`看见的结构`、`解释边界`、`下一步验证顺序` 必须一起留下。强化学习也一样，不能只停在高 reward 或听起来很像样的 policy 说明上，失败成本和后续验证顺序也要一起留下。

## 进入下一 Part 前要确认的问题

进入 Part 5 之前，读者应该能回答下面这些问题。

- 能否从输入与学习信号角度解释 supervised learning、unsupervised learning、reinforcement learning 的区别？
- 能否说明为什么要把 train、validation、test 分开？
- 能否举例说明 overfitting、underfitting、generalization 的差别？
- 能否说出 evaluation metric 的意义会随着问题类型和成本结构改变？
- 能否区分 feature selection、preprocessing、model selection、基准模型、tuning 的角色？
- 能否以入门层级比较 linear regression、logistic regression、decision tree、random forest、gradient boosting？
- 能否把 clustering 和 dimensionality reduction 解释成 `无标签结构读取`？
- 能否说明为什么 reward、exploration、sim-to-real gap 在强化学习里很重要？
- 能否说明模型性能和现实运营价值并不总是同一句话？

没有必要每一个问题都回答得完美。Part 4 的目的，不是把所有模型都学完，而是留下以后读 deep learning 和 generative AI 时会不断回来的标准点。

## Part 4 收尾

完成 Part 4，并不代表已经完全掌握了所有模型的内部数学。它真正代表的是：现在读到机器学习说明时，已经知道先从哪里检查。

先看问题类型。再看输入和输出是什么。接着确认数据是怎么切分的。然后去读指标到底表示什么，并把它和 baseline 放在一起。最后再检查这个模型在现实里到底有什么边界和运行条件。

这种态度在 Part 5 之后也仍然需要。即使模型规模和结构换成了神经网络、LLM、生成式 AI，问题最终还是会回到数据、学习、泛化、评估、应用。

Part 4 就是把这些共同问题明确化的一段。而这些问题，只有在 `看见的结构`、`解释边界`、`下一步验证问题` 一起留下时，才会最安全地运作。

最后再压到最短，可以留下下面这个顺序。

| 先留下什么 | 紧接着分开什么 | 绝不能拖到最后的是什么 |
| --- | --- | --- |
| 看见的分数、分组、结构 | 这个结构的解释边界 | 下一步验证问题 |

## 来源与参考资料

这个总结页是对 Part 4 全体内容的内部整理，没有直接引用外部资料。
