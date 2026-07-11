# P4-1.2 从数据中学习规则这句话是什么意思

> Section ID: `P4-1.2`
> Version: `v2026.07.11`

在 P4-1.1 中，我们区分了 AI、machine learning、deep learning、generative AI、LLM 的位置。现在要把 machine learning 再拉近一点来看。

Part 3 并不是想覆盖整个 data science，而是把重点放在 `把原始数据变成能进入学习与分析的问题结构的前段设计` 上。也就是先决定什么算一条案例、哪些列留下来当作 feature、哪些值可以当作 target 候选、哪些东西则要为了识别和解释而分开保存。

在解释 machine learning 时，人们经常会说 `从数据中学习规则`。这句话很容易让人误解成：模型会直接找出人类能读懂的 `if-then` 规则。其实，machine learning 更准确地说，是从数据案例中估计输入和输出之间的关系，并把这种关系用到新数据上。

也就是说，如果 Part 3 讨论的是 `怎样做出一张可以学习的表`，那么 Part 4 前半段讨论的就是 `模型站在这张表上，到底学到了什么`。与其把它理解成 `学会规则`，更准确的理解是：`看过许多案例之后，形成判断下一条案例的标准`。这一节要说明的，就是 `由人直接写标准` 和 `从数据案例中拟合标准` 这两种方式到底有什么不同。

## 本节范围

这一节说明 rule-based approach 和 learning-based approach 的差别。supervised learning、unsupervised learning、reinforcement learning 的具体区分会在下一章展开。

- 人写规则，到底是什么意思？
- 从数据中学习规则，到底是什么意思？
- 模型真的会找到人能理解的规则吗？
- training data、feature、label、model 是怎样连起来的？
- 为什么学出来的 model 一定还要评估？

## 本节目标

- 能区分 rule-based approach 和 learning-based approach。
- 能把 `从数据中学习规则` 更安全地改写成 `从数据中估计关系`。
- 能说出 training data、feature、label、model、prediction 之间的流程。
- 能理解 machine learning 不是发现唯一正确规则，而是做出满足性能标准的 model。
- 能说明 `在训练数据上很贴合` 和 `在新数据上也能工作` 是两回事。

## 先从一个很小的例子开始

先想想区分水果这个问题。

| 观察到的东西 | 可能的判断 |
| --- | --- |
| 圆的、红色的、手掌大小 | 很可能是苹果 |
| 长的、黄色的、表皮光滑 | 很可能是香蕉 |
| 圆的、橙色的、皮较厚 | 很可能是橙子 |

人可以用语言解释这种判断，也可以直接写出 `如果又黄又长，就很可能是香蕉` 这样的规则。但现实数据往往更复杂。会有颜色很像的水果、大小不那么明确的情况，也会有因为照片光线不同而让颜色看起来变化的情况。

machine learning 处理这类情况的方式，是把这些案例收集起来，去拟合输入和输出之间的关系。这里的输入，是水果的颜色、形状、大小等观察值；输出，则是苹果、香蕉、橙子这样的 label。这个小例子能帮助你把 machine learning 理解成 `根据案例调整判断标准`，而不是 `发现唯一的正确规则`。

## 先比较一下这两种方法

rule-based 和 learning-based approach 都是接收输入，再输出结果。差别在于：判断标准是由谁、用什么方式做出来的。

| 区分 | rule-based approach | learning-based approach |
| --- | --- | --- |
| 标准是怎样做出来的 | 由人直接写出判断标准 | 从数据里估计输入和输出之间的关系 |
| 标准长什么样 | 往往比较显式，比如条件、列表、阈值、policy 文档 | 会因 model 不同而不同，比如权重、分裂、距离、概率或内部表示 |
| 优点 | 易于说明，也更容易控制 | 能从数据中找到人很难全部写出的模式 |
| 弱点 | 一旦例外变多，规则管理会迅速复杂 | 对数据质量、偏差和评估方式依赖很大 |
| 要追问的问题 | `人能不能理解并修改这条规则？` | `它在没见过的数据上还能不能保持性能？` |

这张表里最重要的一点，不是说其中一个才是唯一正确答案。真实系统里，显式规则和学习出来的 model 很可能会一起使用。比如 model 先算出垃圾邮件概率，而服务 policy 再根据这个分数决定拦截、复核还是放行。

下面这张图把两种方法的差别画成流程。rule-based approach 是先由人写标准，learning-based approach 则是从数据案例中做出 model。两条路线最后都可以连到服务的判断或动作上。

```mermaid
--8<-- "assets/part-04/chapter-01/rule-vs-learning-judgment-flow-zh.mmd"
```

这里最重要的点在于，`model prediction` 不等于最终动作。model 可以给出 score 或分类结果，但真实服务仍然可能把成本、风险、policy、用户体验一起考虑进去，再决定最终行为。

## 人写规则的方式

在 rule-based approach 里，判断标准由人直接写出来。

可以想一个简单的垃圾邮件过滤系统。

- 标题里出现某些广告词，就标成垃圾邮件。
- 发件地址如果在封锁名单里，就标成垃圾邮件。
- 正文里可疑链接过多，就标成垃圾邮件。

这种方式很好理解，也比较容易解释为什么被判成垃圾邮件。但一旦例外增多，规则会很快变复杂。新的表达、绕开的写法、正常邮件和垃圾邮件之间混杂的边界，都会让 `由人把所有情况都直接写出来` 变得越来越困难。

这并不意味着 rule-based approach 就不好。它在真实服务里仍然很有用。只是因为很难只靠手写规则维持所有判断，所以才需要一种能利用数据里重复模式的方法。

## 从数据中估计关系的方式

在 machine learning 里，不再由人把所有规则直接写完，而是先准备案例数据。

先把这些案例数据分成下面三个格子来看，会更清楚。

| 区分 | 简单说明 | 例子 |
| --- | --- | --- |
| example | 一个被观察的对象 | 一封邮件、一个客户、一个商品 |
| feature | 描述这个案例的输入值 | 词数、链接数、购买金额、访问次数 |
| label | model 想匹配的输出 | 垃圾/正常、流失/留存、合格/不合格 |

只要这三个格子立起来，`从数据中学习` 这句话就不那么抽象了。model 会看着案例的 feature，朝着匹配 label 的方向去调整自己的内部标准。从更大的 data science 流程来看，machine learning 并不是代替收集、清洗、探索、解释的总称，而更接近于在这些整理好的案例、feature、target 上构建学习 model 的那一段。

如果回想 Part 3 里整理过的表，这里也要再次分清 `什么应该直接用作学习输入`，以及 `什么应该先被分开`。

| 列的性质 | 这一阶段要做的事 | 会不会直接当作模型输入或目标 |
| --- | --- | --- |
| feature 列 | 把它整理成描述案例的输入 | 通常会 |
| label / target 候选 | 确认它是不是以后想预测的值 | 有条件地会 |
| identifier 列 | 用来重新找到并追踪案例 | 通常不会 |
| 运营备注列 | 用来保留人做解释时需要的语境 | 通常不会 |

所以，machine learning 不是把眼前整张表直接塞进去，而是先把同一张表中承担不同角色的列区分开。

如果再拿垃圾邮件分类做例子，需要的数据可以像下面这样。

| 从邮件正文里提取出的 feature | label |
| --- | --- |
| 广告词数量、链接数量、发件人信息、句式模式 | 垃圾邮件 |
| 广告词数量、链接数量、发件人信息、句式模式 | 正常邮件 |

model 会从这些数据里学习 feature 和 label 之间的关系。之后一封新邮件进来时，也会用同样方式做出 feature，训练好的 model 就会给出它是垃圾邮件的可能性，或给出分类结果。

这里所谓 `学规则`，并不意味着 model 会做出人能直接朗读的句子规则。不同的 model，内部表示不同。线性模型学习的是 weight，树模型学习的是 split 标准，k-NN 则是通过找相近案例来判断，deep learning model 还会学到更复杂的表示。

整理一下表达：如果人直接写规则，那是 rule-based approach；如果从数据中估计输入和输出关系，那是 learning-based approach；如果再把估计出来的关系用到新数据上，那就是 model inference 或 prediction。

## `从数据中学习` 的三个步骤

`从数据中学习` 并不是一下子发生的神奇动作。它可以分成下面三个步骤。

1. 先表示出来。
   把现实中的案例变成 model 能处理的输入。比如邮件正文可以变成词数、链接数、发件人信息等 feature。

2. 再去拟合。
   model 会在 training data 上调整内部值，让输入和 target 之间的关系尽量匹配起来。这一步就是 training。

3. 最后再确认。
   用没有拿去训练的数据来检查性能。如果没有这一步，就很难分清 model 学到的到底是关系，还是只是把 training data 背住了。

这三个步骤会在整个 Part 4 中不断重复。如果表示方式变了，model 能看到的问题就会变；如果学习标准变了，model 改进的方向也会变；如果评估数据本身不够好，就可能对真实性能作出错误判断。

这里第一步 `先表示出来`，一定要直接和 Part 3 连起来读。Part 3 里做过的 question、sample、table 结构、feature、baseline、output structure 设计，其实就是这个表示步骤的前半段。只有这些准备做完之后，machine learning 才能相对稳定地决定 `什么作为输入 X`，`什么作为目标 y`。

这三个步骤也可以重新压缩成一句话：`先决定放什么进去，再去拟合关系，最后拿没见过的案例重新确认。` 一旦这句话站住，`fit`、`predict`、`evaluation` 就不再只是 API 名字，而会变成工作顺序。

在实际工作里，还经常要先判断：`现在更合适的是继续多写一点人工规则，还是已经到了该改用学习方法的时候？`

| 当前问题状态 | 更自然的起点 | 原因 |
| --- | --- | --- |
| 标准很清楚，例外也不多 | rule-based approach | 因为人工写的标准仍足以控制这个问题 |
| 例外表达很多，人已经很难把所有标准写出来 | learning-based approach | 因为从数据中估计重复关系更现实 |
| 只靠 model 输出马上行动风险很高 | learning-based approach + policy / human review | 因为 prediction 和最终 decision 应该分开 |

## 学习的基本流程

machine learning 的流程，可以读成下面五步。

```mermaid
--8<-- "assets/part-04/chapter-01/machine-learning-basic-flow-zh.mmd"
```

在这张图里，`X` 是送进 model 的输入数据。通常最容易把它理解成一种 `行是 sample、列是 feature` 的数组或表。`y` 则是在监督学习里 model 想匹配的目标值。对于分类问题，它可以是 label；对于回归问题，它可以是数值。

scikit-learn 的基本使用流程也和这个结构很像。先创建 model object，再用 `fit` 在 `X` 和 `y` 上学习，最后用 `predict` 对新输入计算输出。这里最重要的不是背 API 名字，而是理解 `fit` 是学习阶段，`predict` 是把学好的 model 用起来的阶段。

## 不同 model 学出来的结果长得不一样

必须小心 `学规则` 这个说法，最大的原因就在于：不同 model，学习后留下来的东西形态并不一样。

| model 例子 | 学完后留下来的直觉 | 它和人能读懂的规则是什么关系 |
| --- | --- | --- |
| linear model | 表示每个 feature 影响大小的 weight | 可以读成数值关系，但不是句子规则 |
| decision tree | 按数值切分的 split | 相对容易读成规则 |
| k-NN | 根据距离找相近案例的标准 | 不一定显式造规则，而是借助附近案例 |
| probabilistic model | 观察到的 feature 与结果之间的概率关系 | 它算的是可能性，但最终 decision 规则仍可另放 |
| neural network | 多层权重和表示 | 会变成很难由人直接阅读的内部表示 |

所以，如果把学习出来的 model 只理解成 `规则集合`，就会很容易错过 model 之间真正的差别。更一般的表达应该是：`model 根据数据调整了把输入变成输出的计算方式。`

## `学规则` 这个说法的局限

`从数据中学习规则` 这个说法在入门阶段是有帮助的，但如果就停在这里，会产生几种误解。

第一，容易误以为 model 总会做出人能读懂的规则。decision tree 确实比较像规则，但线性模型的 weight 或神经网络的内部表示，就不是人写出来的句子规则。

第二，容易误以为数据里一定藏着唯一正确规则，而 model 终究会把它找出来。现实数据里有 noise、缺失、bias、measurement error。model 并不是在寻找完整真理，而是在给定数据和目标标准下，估计一个还算可用的关系。

第三，容易误以为只要 training data 上拟合得好，现实问题就一定解决得好。如果 model 只是把 training data 记住了，它在新数据上的性能反而会下降。这就会接到 overfitting 问题。

因此，在 Part 4 里，比起 `学规则`，会更常使用下面这些表达。

- 在数据里寻找 pattern
- 估计 input 和 output 之间的 relationship
- 训练一个能提升 prediction 性能的 model
- 评估它是否能 generalize 到没见过的数据

## 小例子：预测考试分数

先想一个非常简单的问题：用学习时间来预测考试分数。

| 学习时间 | 考试分数 |
| --- | --- |
| 1 小时 | 50 |
| 2 小时 | 60 |
| 3 小时 | 65 |
| 4 小时 | 75 |

如果由人写规则，可能会写成 `学习时间达到 3 小时以上，合格的可能性较高` 这样的标准。

在 machine learning 方法里，则是从数据中估计 `学习时间` 和 `分数` 的关系。model 可以把 `学习时间越长，分数大致会增加一些` 这种趋势用数字表达出来。如果有个新学生学习了 5 小时，model 就会利用它从历史数据中学到的关系来预测分数。

但这仍然只是一个简化预测。学习时间并不能完全解释考试分数。基础能力、试卷难度、睡眠、题型等因素也都会影响结果。这个例子说明：machine learning 并不是在找到一条完全解释现实的规则，而是在有限 data 和 feature 内，估计一个有用的关系。

## 小例子：客户咨询分类

再看一个工作里更常见的例子：客户咨询分类。

如果由人写规则，可能会写成这样。

- 标题里有 `退款`，就分到退款咨询。
- 正文里有 `东西还没到`，就分到配送咨询。
- 有 `登录`、`密码`，就分到账户咨询。

但真实咨询往往不会这么整齐。像 `已经付款了，但货没到，还想取消` 这样的问题里，可能同时混着几种意图。同一个意思，也可能用很多不同说法表达。如果只靠 rule-based approach，例外规则会越来越多。

在 learning-based approach 里，会先收集历史咨询和人工贴好的分类 label。model 学习表达和 label 之间的关系，再在新咨询进来时预测它更接近哪个类型。即使如此，真实业务也未必只靠 model 就结束。置信度低时可以转给人处理，像退款这种高风险业务，也可能还会单独加上审批流程。

这个例子说明，machine learning 不一定是完全取代业务判断，而更常用来帮助处理重复性的分类或优先级判断。

## 为什么需要评估

仅仅因为 model 能把 training data 解释得很好，并不够。machine learning 里更重要的问题是：`它在新数据上也能工作吗？`

所以，Part 4 很快就会进入数据拆分。

- training data：用来让 model 学关系
- validation data：用来挑选 model 或调参数
- test data：最后用来确认性能

这个区分是 machine learning 的核心。因为从数据中估计关系的 model，总会有 `过度贴合 training data` 的风险。所以要判断它到底是否有用，就必须用没有参与学习的数据来评估。

## 案例与示例

### 案例 1. 团队要决定客户咨询该靠手写规则，还是该改用数据学习时

假设某个团队想把客户咨询自动分成 `配送`、`退款`、`账户`、`其他`。在初期，他们完全可以先直接写规则，比如标题里有某些词，就把它送到对应部门。

这种方式一开始很快，但表达方式只要稍微变化，例外就会迅速增加。像 `已经付款了，但货没到，还想取消` 这种混合意图咨询一多起来，只靠规则维护就会很快变得复杂。

这时候，learning-based approach 就会出现。如果把历史咨询案例和人工贴好的 label 收集起来，model 就可以估计输入表达和 label 之间的关系，并对新咨询进行分类。但这不意味着它会直接生成可阅读的句子规则，同时 `在训练数据上拟合得好` 也依然不同于 `在新咨询上泛化得好`。

真正可检查的结果，会出现在新咨询评估里。rule-based classifier 可能只要措辞稍微一变就漏掉，而 learning-based model 如果确实从历史案例里学到了相似模式，就能更稳定地预测。相反，如果它只是在训练数据上表现好，一遇到新咨询就频繁出错，那说明它的 generalization 还不够。

```mermaid
--8<-- "assets/part-04/chapter-01/inquiry-rule-vs-learning-flow-zh.mmd"
```

## 本节要记住的视角

- rule-based approach 是由人直接写判断标准，learning-based approach 则是让 model 从数据里估计关系。
- `从数据中学习规则` 更安全的理解，是 `从数据中估计关系` 或 `根据案例调整判断标准`。
- 在训练之前，表仍然必须先分出 example、feature、label、identifier、运营语境这些不同角色。
- `在训练数据上拟合得好` 和 `能 generalize 到没见过的数据` 不是一回事，所以 evaluation 不可缺少。

## 检查清单

- 能不能说明为什么 `学习规则` 并不总等于生成可读的句子规则？
- 能不能说明 Part 3 里的表格设计，是怎样接到 machine learning 里的 `什么成为 X`、`什么成为 y`？
- 能不能说明为什么只做 prediction 还不够，仍然必须在没见过的数据上做 evaluation？

## 什么时候要先想到这个视角

- 当有人把 machine learning 直接理解成 `更复杂的手写规则` 时，要先回到这一节。
- 当要判断当前问题应继续留在 rule-based approach，还是该转到 learning-based approach 时，要先想到这里。
- 当训练开始前，需要重新分开 feature、target、identifier、运营备注时，这一节就是基准。

## 来源与参考资料

- Google, `Machine Learning Glossary`, 包含 `feature`、`label`、`training`、`prediction` 等条目，确认日期：2026-07-10. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Getting Started`, scikit-learn documentation, 确认日期：2026-07-10. [https://scikit-learn.org/stable/getting_started.html](https://scikit-learn.org/stable/getting_started.html){: target="_blank" rel="noopener noreferrer" }
