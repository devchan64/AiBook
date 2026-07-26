# P4-2.1 监督学习

> Section ID: `P4-2.1`
> Version: `v2026.07.25`

在 P4-1.2 里，我们把 [machine learning](/AiBook/zh/reference/concept-glossary-pinyin/m/#machine-learning) 看成 `从数据中估计输入和输出关系的方法`。现在要看其中最先会遇到的一种形式：[监督学习](/AiBook/zh/reference/concept-glossary-pinyin/j/#supervised-learning)。

监督学习，是用已经带有 [label](/AiBook/zh/reference/concept-glossary-pinyin/l/#label) 或 [target](/AiBook/zh/reference/concept-glossary-pinyin/m/#target) value 的案例来训练 model 的方式。这里的 label 不只是名字标签，而是 model 想匹配的输出。因为案例会告诉它 `给定这种输入时，应该出现什么结果`，所以才会用 `supervised` 这个词。

监督学习可以先读成 `看着同时带有例子和答案的案例，再去猜新案例输出` 的方式。但 model 并不是在理解人写的解释，它是在大量案例中不断调整自己的内部标准，让输入和输出之间的关系尽量匹配。

这一节会说明 `supervised learning`、`输入 X 与目标 y`、[classification](/AiBook/zh/reference/concept-glossary-pinyin/c/#classification) 和 [regression](/AiBook/zh/reference/concept-glossary-pinyin/h/#regression) 的基本区分。后面的章节会带着这个抓手继续判断当前语境，而基于标签的学习到底是什么意思这个基础含义，会以本节和 [概念词汇表](/AiBook/zh/reference/concept-glossary/) 为基准再次接回。

## 本节范围

这一节说明监督学习的基本结构。像 linear regression、logistic regression、decision tree 这样的具体算法会在后面分别展开。具体来说，linear regression 会在 P4-10 再处理，logistic regression 会在 P4-11 再处理，decision tree 会在 P4-14 再处理。

- 在监督学习里，输入和 label 各自是什么？
- classification 和 regression 有什么不同？
- [training](/AiBook/zh/reference/concept-glossary-pinyin/x/#training)、[evaluation](/AiBook/zh/reference/concept-glossary-pinyin/e/#evaluation)、[prediction](/AiBook/zh/reference/concept-glossary-pinyin/y/#prediction) 是怎样连起来的？
- 有了 label，就表示 model 已经知道正确答案了吗？
- 在监督学习里，一开始最先该小心的误解是什么？

## 用监督学习留下的判断标准

- 能把监督学习说明成 `从带标签的案例里学习输入与输出关系的方法`。
- 能区分输入数据 `X` 和 label / target `y` 的角色。
- 能用例子说明 classification 和 regression 的差别。
- 能说明为什么要分开 training data 和 evaluation data。
- 能区分 model 的 prediction 和服务的最终 decision。

## 先用一个场景来理解

想一想自动分类客户咨询的场景。

| 客户咨询内容 | 人工贴上的 label |
| --- | --- |
| `已经付款了，但货还没到。` | 配送咨询 |
| `退款要在哪里申请？` | 退款咨询 |
| `我忘记密码了。` | 账户咨询 |

在监督学习里，会把这样的案例展示给 model。咨询内容是输入，人工贴上的咨询类型是 label。model 会被训练成：当新的咨询进来时，去预测它更接近哪个 label。

这个例子里最关键的是 `已经有 label`。如果没有 label，model 就不会直接知道自己应该匹配什么。正因为 label 存在，它才有办法朝着匹配输入和输出关系的方向学习。

## 监督学习的基本形状

在监督学习里，案例会被准备成 `输入 - 输出` 的配对。

| 案例 | 输入 feature | label 或 target |
| --- | --- | --- |
| 邮件 1 | 标题、正文词语、链接数量、发件人信息 | 垃圾邮件 |
| 邮件 2 | 标题、正文词语、链接数量、发件人信息 | 正常邮件 |
| 房屋 1 | 面积、位置、房间数、建造年份 | 价格 |
| 客户 1 | 访问次数、购买金额、最近登录日期 | 是否流失 |

输入通常写成 `X`，label 或 target value 写成 `y`。如果沿用 Part 2 里的表格视角，`X` 就是一份有很多行列的数据；行表示一个案例，列表示一个 feature。`y` 则承担每个案例的答案角色。

与其把 `X` 和 `y` 当成数学符号死记，不如按它们承担的角色去理解。

| 记号 | 先联想到的话 | 例子 |
| --- | --- | --- |
| `X` | 给 model 看的输入集合 | 从邮件内容提取的 feature、客户记录、商品信息 |
| `y` | model 想匹配的输出集合 | 垃圾/正常、流失/留存、价格 |
| 一行 row | 一条案例 | 一封邮件、一个客户、一套房子 |
| 一列 column | 一个 feature | 链接数、购买金额、房间数 |

这里 `答案` 这个词仍然要谨慎。label 是学习数据里 model 想去匹配的值，但它并不保证就是现实世界对所有情况都成立的完整真理。人工贴的 label 可能出错，测量值里也可能有 noise。

如果把 Part 3 里整理数据的流程带进来，那么在进入监督学习之前，下面四种东西必须先分开。

| 先要分开的东西 | 在当前阶段是什么意思 | 会不会直接进入监督学习 |
| --- | --- | --- |
| 一条案例 | 一行是不是代表一种同类动作或对象的一次记录 | 会 |
| 输入 feature 列 | 它是不是准备用作模型输入的描述值 | 会 |
| 目标候选 | 它是不是以后想预测的结果值 | 有条件地会 |
| 识别 / 运营列 | 它是不是用来重新找到案例或说明运营语境的值 | 通常不会 |

这里写成 `有条件地会`，是因为就算某个值看起来像目标候选，也不代表它立刻就是监督学习问题。首先要确认 label 标准是否一致、以后还能不能按同样标准重新贴、以及模型应该匹配的问题到底是 classification 还是 regression。identifier 列也是一样。它对重新找到案例很重要，但通常不会原样直接送进 model，而是分开管理。

## 按流程来看

监督学习的流程可以读成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-1-mermaid-01-zh.mmd"
```

在这张图里，`train model` 是 model 在 training data 上调整内部值，让输入与 label 之间的关系尽量匹配的阶段。`evaluate` 是拿没有参与训练的数据，把 prediction 和真实 label 拿来比较的阶段。`prediction` 则是把训练好的 model 用到一个新输入上的阶段。

最后的 `service decision` 是故意分开摆出来的。就算 model 给出了 `垃圾邮件概率 0.92`，也不代表服务一定要立刻拦截。服务仍然可能同时考虑 policy、成本、风险和用户体验，再决定是拦截、人工复核还是放行。

## 分清 training、evaluation、prediction

第一次接触监督学习时，最容易混在一起的几个词，就是 training、evaluation、prediction。

| 阶段 | 在做什么 | 简单问题 |
| --- | --- | --- |
| training | 用带标签的数据去拟合 model 的内部标准 | `从这些案例里能学到什么关系？` |
| evaluation | 用没有参与训练的数据检查 model 到底多准 | `放到新案例里还能不能工作？` |
| prediction | 把训练好的 model 用在真实的新输入上 | `这个新案例更可能得到什么结果？` |

只要这三步区分开，`我们做出了一个模型` 这句话就会更清楚。训练 model、证明它真的可用、以及把它放到服务里运行，根本不是同一件事。

## classification 和 regression

监督学习通常会先按 classification 和 regression 这两个大类来说明。

| 区分 | model 想匹配的输出 | 例子 |
| --- | --- | --- |
| classification | category 或 class | 垃圾/正常、合格/不合格、流失/留存 |
| regression | 连续数值 | 房价、需求量、温度、营收 |

classification 问的是 `它属于哪个类别？` 例如，一封邮件是垃圾还是正常、一条评论是正面还是负面、一张图片是猫还是狗。

regression 问的是 `它大概是多少？` 例如，房价是多少、明天的需求量有多少、配送时间大概需要多少分钟。

二者的共同点，是都在学习输入和输出之间的关系。差别在于输出的性质。如果输出是类别，它更接近 classification；如果输出是数值大小，它就更接近 regression。

## 小例子：学习时间和是否通过

考虑下面这样一份小数据，它同时包含学习时间、模拟考试分数和是否通过。

| 学习时间 | 模拟考试分数 | 是否通过 |
| --- | --- | --- |
| 1 小时 | 45 | 未通过 |
| 2 小时 | 55 | 未通过 |
| 4 小时 | 72 | 通过 |
| 5 小时 | 80 | 通过 |

如果目标是 `是否通过`，那它是一个 classification 问题。model 的目标，是根据新学生的学习时间和模拟分数，预测 `通过` 或 `未通过`。

反过来，如果目标是 `真实考试分数`，它就变成了 regression 问题。model 的目标，是根据学习时间和模拟分数，预测 `大概会考多少分`。

同一份数据，只要你把什么放进 `y` 改掉，问题就会变。这正是监督学习里 `问题定义` 之所以重要的原因。

## label 是从哪里来的

监督学习需要 label。label 可以通过多种方式形成。

- 由人直接分类
- 使用既有业务系统的结果
- 使用传感器或测量设备的记录
- 使用后来真实发生的结果

例如，在客户流失预测里，像 `30 天内是否取消服务` 这样的真实结果可以当作 label；在不良品分类里，检验员贴上的判定可以当作 label；在房价预测里，实际成交价可以当作 target value。

但 `有 label` 并不总是代表你已经拥有了一个好的监督学习问题。如果 label 本身不准确、label 标准中途改变、或 label 对某些群体存在偏差，那么 model 也会把这些问题一起学进去。

所以必须把 `label 存在` 和 `立刻就能拿来做监督学习` 分开看。

| 看见的状态 | 直接下结论为什么危险 | 还要再确认的问题 |
| --- | --- | --- |
| 有 label 列 | 标准可能并不一致 | 以后还能不能按同样标准重新贴上？ |
| 有旧系统里的结果值 | 其中可能已经混入业务规则变化 | 它现在还表示同一个目标吗？ |
| 有人工判断结果 | 不同人之间可能判断标准不同 | 人与人之间分歧大不大？ |

也就是说，监督学习不是从 `发现了一列 label` 开始，而是从确认 `这个 label 能不能稳定地表达我们真的想预测的结果` 开始。

实际工作里，往往还要先很短地判断一下：`当前问题到底是不是监督学习。`

| 当前状态 | 要不要按监督学习来读 | 原因 |
| --- | --- | --- |
| 输入 feature 和目标 label 一起存在，而且还能按同样标准再次贴上 | 要 | 因为可以相对稳定地构成输入 `X` 和目标 `y` |
| 虽然有 label 列，但标准经常变化，或不同人之间差异很大 | 不能直接算 | 因为得先重新检查 label 质量和目标定义 |
| 只有输入，没有要预测的结果 label | 不要 | 因为此时更先需要结构探索或其他问题定义 |

## 为什么要拆分数据

model 在 training data 上表现好，并不够。我们真正想要的是：它在没见过的数据上也有用。

所以在监督学习里，会把数据拆开来看。

| 数据拆分 | 角色 |
| --- | --- |
| training data | 用来让 model 学会关系 |
| validation data | 用来选 model 或调整设置 |
| test data | 用来做最终性能确认 |

先把 training data 和 test data 的区分立清楚非常重要。关键点在于：`把已经学过的问题答对` 和 `把第一次看到的问题答对`，不是同一回事。

## 在监督学习里一开始最先要小心的误解

在监督学习里，首先要避开的误解有下面这些。

- 不要以为有了 label，问题就会自动变简单。
- 不要把 label 当成现实里完整无误的真答案。
- 不要把 training data 上的分数，当成真实服务里的性能。
- 不要把 model prediction 当成服务的最终 decision。
- 不要先按算法名字来区分 classification 和 regression，而要先看输出本身的性质。

监督学习不是 `把正确答案告诉模型让它死记`。更准确地说，它是利用带有 label 的案例去估计输入和输出之间的关系，再去确认这种关系能不能 generalize 到新的案例。

## 案例与示例

### 案例 1. 当客户咨询已经有人类答案时，为什么它适合读成监督学习

假设某个团队想把客户咨询自动分成 `配送`、`退款`、`账户` 等类型。如果历史咨询记录和客服人工贴上的类型已经一起留下来了，人就很容易想到：`能不能利用这些答案，把新咨询也分好？`

这个场景里最重要的是：`已经存在能充当答案角色的 label`。model 可以学习 `咨询内容` 这个输入，与 `客服贴上的类型` 这个输出之间的关系。于是，它就成了一个去预测新咨询更接近哪一种类型的问题。

这也就是为什么本节会把监督学习解释成 `X` 和 `y` 同时存在的问题。咨询内容、链接数量、长度等会变成 `X`，人工贴上的类型会变成 `y`。只有这套结构立住，model 才会清楚自己到底在匹配什么。

真正可检查的结果，会出现在没有用于训练的新咨询评估里。如果它不只是对历史咨询表现好，在新咨询上的分类准确率也能保持，那么这个问题就被整理成了一个结构比较稳的监督学习问题。

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-1-mermaid-02-zh.mmd"
```

## 检查清单

- 能不能说明在什么状态下，`有 label` 和 `可以立刻当成监督学习问题来用` 必须分开看？
- 能不能说明为什么即使是同一份数据，只要 `y` 放的东西不同，classification 和 regression 就会改变？
- 能不能在监督学习语境里说明，model prediction 和服务最终 decision 是不同阶段？
- 能不能说明监督学习是从同时带有输入 `X` 和 label 或 target `y` 的案例里学习关系的方法？
- 能不能说明 label 是 model 想匹配的输出，但并不保证就是现实里的完整真理？
- 能不能区分 training 是拟合关系的阶段，而 evaluation 是在没见过的数据上确认的阶段？

## 来源与参考资料

- Google, `Machine Learning Glossary`, 包含 `supervised learning`、`label`、`classification`、`regression` 等条目，确认日期：2026-07-26. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google for Developers, `Supervised Learning`, Machine Learning, 确认日期：2026-07-26. [https://developers.google.com/machine-learning/intro-to-ml/supervised](https://developers.google.com/machine-learning/intro-to-ml/supervised){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Supervised learning`, scikit-learn User Guide, 确认日期：2026-07-26. [https://scikit-learn.org/stable/supervised_learning.html](https://scikit-learn.org/stable/supervised_learning.html){: target="_blank" rel="noopener noreferrer" }
