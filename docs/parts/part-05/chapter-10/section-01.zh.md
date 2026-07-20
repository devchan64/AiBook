# P5-10.1 表征学习（representation learning）

> Section ID: `P5-10.1`
> Version: `v2026.07.20`

走到 P5-9 章时，我们已经看到：深度学习会按 batch 重复大规模 tensor 计算，并且依靠 GPU 和并行处理，才扩散到真正实用的规模。现在如果把问题重新转回模型内部，就会自然冒出下一个提问。

做完这么多计算之后，神经网络到底学到了什么？

回答这个问题时最关键的表达，就是表征学习（representation learning）。

表征学习，指的是：不再由人逐项设计 feature，而是由模型自己从数据里学出有用的内部表征。

如果后面在结构章节里又把`表征`和`表征学习`混在一起，更适合一起回到[英文概念词汇表里的 representation 条目](/AiBook/en/reference/concept-glossary/#representation)和[representation learning 条目](/AiBook/en/reference/concept-glossary/#representation-learning)重新对齐。

## representation learning 怎样改变特征的问题

- representation 到底是什么意思？
- representation learning 和 feature engineering 有什么不同？
- 为什么在深度学习里，representation learning 会被当成一个转折点？
- `模型学到了内部表征`这句话，到底该怎样对读者解释？

这一节先把 representation learning 关成：`模型自己形成有用内部 feature 的过程`，并专注于抓住它和过去由人直接挑 feature 的做法到底差在哪里。

同时，这一节也明确把下一个问题交出去。更深层里的表征为什么会看起来更抽象，会在下一节 P5-10.2 继续说明。图像领域里的表征会在 P5-11.1、P5-11.2 重新接回；序列和 attention 相关表征，则会在 P5-12.1、P5-12.2、P5-13.1、P5-13.2 里继续展开。

## 内部特征与任务连接的判断标准

- 能把 representation learning 解释成`模型自己形成有用内部 feature 的过程`。
- 能比较：人直接制作 feature 的方式，和深度学习方式到底有什么差异。
- 能说明：为什么深度学习会随着 representation learning 的成功一起迅速扩散。
- 能通过可执行的 Python 例子，把人定义的 feature 和简单的 representation learning 直觉放在一起比较。

## 什么是 representation

`representation` 这个词对读者来说很容易显得抽象。先把它理解到下面这个程度就够了。

`原始数据被改写成一种更方便模型处理的内部数字形式`

例如，同一份设备运行记录，可以用两种方式来看。

- 原始输入：最近温度偏离次数、压力波动持续时间、重启延迟时间
- 内部表征：模型在计算里组合出来的热负担、运行不稳定性、后续点检紧迫度之类更抽象的数字组合

当然，模型自己并不会真的给这些数字贴上这样的名字。但这里重要的是那种感觉：`它会把原始输入改写成更容易参与后续计算的中间表征。`

如果把同样的想法拆成输入、人可读的说明、模型内部使用的表征，这三层差异会更清楚。

| 层位（level） | 人是怎样读的 | 模型是怎样处理的 |
| --- | --- | --- |
| 原始数据 | 最近温度偏离次数、压力波动持续时间、重启延迟时间这些观测值 | 数字 vector 或 tensor 输入 |
| 人写出的说明 | 热负担大、运行不稳定之类的解释性说法 | 还不是模型内部计算本身 |
| 内部表征 | 没有标签的中间数字组合 | 会被送入下一层计算和最终预测 |

也就是说，representation learning 不是在逐字学会人写出来的解释句子，而更接近于：在模型内部长出一套对预测有用的坐标系。

## 它和 feature engineering 有什么不同

在较早的机器学习和更传统的方法里，由人直接设计 feature 是非常重要的。

例如，在图像问题里，人可能会先做出这样的 feature：

- edge count
- texture descriptor
- color histogram

在文本问题里，也会由人整理：

- 单词出现频率
- 文档长度
- 是否包含某种特定模式

representation learning 的转折点就在于：这些 feature 组合中的很大一部分，开始由模型自己直接从数据中学出来。

也就是说：

- feature engineering 更接近一种由人先决定`应该看什么`的方式
- representation learning 更接近一种由模型在学习过程中内部发现`什么才是有用的`的方式

如果把这件事再压缩成一句：`同样输入到底是谁把它改写到什么坐标系里`，就会更清楚。

| 提问 | 以 feature engineering 为中心的做法 | 以 representation learning 为中心的做法 |
| --- | --- | --- |
| 谁来决定 feature？ | 人先决定 | 模型在学习中形成 |
| 开发者最中心的工作 | 用领域知识设计 feature | 设计数据、结构、学习设置 |
| 优势 | 解释相对更直接 | 能更宽地捕捉复杂组合 |
| 负担 | 每个问题都要付出较高手工设计成本 | 数据和计算资源变得更重要 |

如果再用`谁在把同样输入改写到什么坐标系里`这个视角把差别压成一个流程，大致就是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-10/manual-vs-learned-coordinates-zh.mmd"
```

也就是说，feature engineering 更像是人先在外部挑出一套容易读的轴；representation learning 则更像是模型在学习过程中，内部长出一套对任务更有用的新轴。

## 为什么这个差异很重要

这件事重要，并不只是因为它变得更自动化了。

人造 feature 本身是有边界的。

- 每个问题都需要一套不同的 feature 设计
- 人可能会错过某些组合
- 数据一旦变复杂，手工做 feature 设计会非常困难

深度学习就是朝着这样一个方向发展起来的：通过很多层和非线性变换，直接从 raw input 中学出更有用的表征。

先把它记成下面这句话就够了。

`深度学习的强项，不只是模型大，而是它会自己长出 feature。`

## 在图像、语音、文本里，representation learning 会怎么出现

即使数据领域不同，representation learning 仍然共享类似的思路。

### 图像

- 前面层里可能先出现 edge 或简单 pattern
- 更深一层会出现局部形状
- 再往后则会出现更接近 object 的线索

### 语音

- 不再只是原始波形本身
- 而是更有用的内部表征，例如发音模式、音节线索、说话人特征

### 文本

- 不再只是字符或 token 本身
- 而是更能承载上下文、句法、语义关系的内部表征

也就是说，虽然数据类型不同，representation learning 共享的结构仍然是：`把输入改写成更有用的中间形式。`

如果把这种视角重新放回工作场景里，感觉会更具体。

| 场景 | 人更容易直接做出的 feature | 模型可能更擅长学出的表征 |
| --- | --- | --- |
| 维修优先级推荐 | 最近报警数、返工呼叫数、停机时长 | 相似故障簇、风险转移倾向、重复干预模式这类潜在模式 |
| 生产 batch 异常早检 | 最近温度偏离数、最近压力波动数 | 会随时间变化的不稳定模式、多异常信号的组合 |
| 文档分类 | 单词频率、文档长度 | 会随上下文变化的主题表征、相似句式的聚类 |

接下来 Part 5 后面的章节，会把同一个 representation learning 再按`不同数据结构更自然会被什么神经网络结构读取`来重新拆开。

| 后面要接上的结构 | 首先面对的数据问题 | representation learning 在这里的表现方式 |
| --- | --- | --- |
| CNN | 像图像这样邻近位置一起形成意义的问题 | 从局部 pattern 逐步走向更大的视觉结构 |
| RNN/LSTM/GRU | 像句子、语音、时序这样顺序会改变意义的问题 | 通过承接前一状态形成顺序语境 |
| Attention/Transformer | 需要直接比较远距离位置关系的问题 | 通过权重去读哪些位置彼此更重要 |

也就是说，后面那些章节并不是在不断增加新的模型名词，而是在把同一个`representation learning`拆成：它在图像、顺序数据、长上下文关系问题里，各自会被什么结构更自然地实现。

## 为什么它会像深度学习历史里的转折点

深度学习之所以会被广泛关注，并不只是因为层数变深了。真正重要的是：`深层结构开始真的学到了有用的表征。`

例如，AlexNet 之后 CNN 在图像识别里变得如此醒目，也正是因为它展示了：相比人手工做的 feature，模型能学到更强的层次化表征。

这个点，也会和 Part 1 里已经看到的深度学习范式扩散重新接回。

也就是说，representation learning 是把深度学习呈现成`一种会替代 feature engineering 的计算方式`的核心因素之一。

## 如果把这件事画得极简

```mermaid
--8<-- "assets/part-05/chapter-10/feature-engineering-vs-representation-learning-zh.mmd"
```

这张图是在压缩：传统 feature engineering 和深度学习 representation learning 之间，看问题的角度差在哪里。

## 案例与示例

### 代表案例. 维修优先级推荐

假设设备维护团队要决定先检查哪条产线。人一开始很容易觉得，只要做出`最近 7 天报警数`、`返工呼叫次数`、`平均停机时间`这样的统计列，就已经足够。这种方式很快，也容易说明。但真实里，真正重要的可能是`温度报警反复出现，随后压力不稳定跟上，再接着返工呼叫增加`这样的流程组合，而这种组合并不容易被一个单独数字直接暴露出来。

representation learning 模型可以把每条产线的报警历史和处理信息一起读进去，再压缩出故障簇和风险转移模式之类的内部表征。于是它就不只是在沿用简单的报警计数规则，而是更容易抓住：`眼下这条产线到底哪种后续检查更紧急。` 结果上，维护优先级不再只是简单按频率排序，而会更贴合上下文地变化。

这个案例里要确认的结果，并不是把最近报警数相近的产线排得更像，而是把真正风险转移流程更接近的产线，推荐到更相似的后续检查项。

| 人最容易先看的标准 | 用 representation learning 视角重读的标准 |
| --- | --- |
| 几个统计量，比如报警数、停机时间，看起来就已经够了 | 不同异常组合可能被埋在相同的统计值后面 |
| 用单个分数给产线排队，看起来最方便 | 单一分数会把风险转移方向这类潜在模式压扁 |
| 数值相近就容易被看成故障状态也相近 | 实际上在另一套表征轴上，它们可能离得更远 |

同样的视角也适用于别的数据。只是这一节真正要抓住的核心，不是领域名字，而是：`那些会被一句规则或手工坐标埋掉的模式，能不能在新的坐标系里重新展开。`

| 场景 | 人最容易先看到的结果 | 用 representation learning 视角真正要区分的东西 |
| --- | --- | --- |
| 图像质检 | 亮线长度、翘起区段数量这些规则看起来就够了 | 反光、褶皱、纹理组合这类模式更重要，却不容易塞进手工规则 |
| 维修日志检索 | 只数词频，看起来也能把相似日志聚起来 | 表面词汇不同，但处理流程语境相似的日志，可能会在表征空间里更近 |
| 质量检测自动化 | 裂纹长度、斑点数量这类两三个标准似乎就足够 | 位置、方向、周边亮度变化的组合，往往会被手工两三个数字漏掉 |

## 练习与例子

这个例子的目标，是把维修优先级推荐场景里，人手工做出的单一风险分数，和从数据里算出来的二维中间表征并排放在一起。

输入：

- 4 条设备产线的连续温度报警次数、压力不稳定次数、返工呼叫次数
- 一个人定义的单一风险分数规则
- 从输入数据里计算出的两个表征轴

输出：

- hand-crafted risk score
- 二维 data-driven representation
- 每条设备产线在新坐标系里的位置
- 那些在单一分数里看起来相近、但在表征坐标里可能分开的产线比较

问题场景：

- 要理解 representation learning，首先需要确认那种感觉：不要继续盯着原特征不放，而是把它们改写到另一套坐标系里再读
- 也要一起看到：单一风险分数里埋掉的差异，在新的 representation 坐标中可能会被重新拉开
- 如果 representation 轴仍然由人手工指定，就会误读`有用的轴其实是在数据和学习过程中形成的`这个核心点，因此即使在这个例子里，轴也必须先从数据中算出来
- 还要能通过改动 `line_B` 的返工呼叫次数，确认人做出的分数和从数据里得到的 representation 坐标是怎样一起变化的

要确认的概念：

- representation 可以被看成是把原输入重新排到另一组轴上之后的结果
- 只要一起看各条产线在新坐标系里的位置，就更容易看到中间表征为什么重要
- 哪怕 hand-crafted risk score 相同，只要 representation 坐标不同，就可能意味着它们属于不同模式

输入（input）：

我们会先把上面整理好的原始数据做标准化，再用线性代数计算，求出两个最能把数据分开的辅助表征轴。

这个例子并不是在完整实现神经网络的 representation learning。更准确地说，它是一个辅助实验，用来在进入这一节之前，先确认：人手工写下的一行分数规则，和从数据里算出来的中间坐标，会留下怎样不同的阅读结果。由于这里不会把表征轴由人直接写死，而是先由输入数据算出来再去阅读，所以注意力可以更集中地放在`被规定好的分数`和`从数据得到的表征`之间的差异上。

在看代码之前，可以先预测会出现什么样的比较。

| 比较 | 可以先预测的差异 | 预测理由 |
| --- | --- | --- |
| `risk_score` | 很可能只会把设备产线排成一条单维风险线 | 因为人手工写出的规则会把几个异常信号压进同一个轴 |
| `representation` | 即使原始数据相同，也可能在两个轴上出现不同位置 | 因为由数据计算出来的辅助轴，能够把温度、压力、返工之间的组合方向分开保留 |
| 分数相近的产线 | 在 representation 坐标里可能会被拉开 | 因为单一分数里埋住的风险类型差异，可以在两个轴上重新露出来 |

这张表的目的，是先把`单行分数`和`多轴表征`分开来读。

要实验的值是 `line_b_rework_calls`。一开始把它设为 `5.0` 运行一次，然后再像 `1.0` 那样调低，比较 `line_B` 在表征坐标里会怎样移动。

```python
# 这个例子比较人工设计的 risk_score 和从数据计算出的二维 representation 坐标会留下什么不同读法。
import numpy as np

lines = ["line_A", "line_B", "line_C", "line_D"]
line_b_rework_calls = 5.0
data = np.array([
    [6.0, 5.0, 1.0],  # repeated temperature alarms, then pressure instability
    [2.0, 3.0, line_b_rework_calls],  # fewer alarms, but repeated rework calls
    [1.0, 1.0, 1.0],
    [5.0, 4.0, 5.0],
])

# hand-crafted feature: one risk score chosen by a person
risk_score = data[:, 0] * 3 + data[:, 1] * 4 + data[:, 2] * 5

# data-driven representation: compute two auxiliary axes from the input data
mean = data.mean(axis=0)
std = data.std(axis=0)
standardized = (data - mean) / std

_, _, components = np.linalg.svd(standardized, full_matrices=False)
axes = components[:2].copy()
if axes[0, 0] < 0:
    axes[0] *= -1
if axes[1, 2] < 0:
    axes[1] *= -1
representation = standardized @ axes.T

for line, raw, score, rep in zip(lines, data, risk_score, representation):
    print(
        f"{line}: raw={raw.tolist()}, "
        f"risk_score={score:.2f}, "
        f"representation={np.round(rep, 2).tolist()}"
    )

score_gap = round(float(risk_score[0] - risk_score[1]), 2)
rep_gap = round(float(np.linalg.norm(representation[0] - representation[1])), 2)
print("score_gap(line_A, line_B) =", score_gap)
print("representation_gap(line_A, line_B) =", rep_gap)
```

输出时，先比较单一分数 `risk_score` 和 `representation` 同时保留了哪些轴信息即可。

```text
line_A: raw=[6.0, 5.0, 1.0], risk_score=43.00, representation=[1.56, -1.2]
line_B: raw=[2.0, 3.0, 5.0], risk_score=43.00, representation=[-0.5, 1.11]
line_C: raw=[1.0, 1.0, 1.0], risk_score=12.00, representation=[-2.04, -0.77]
line_D: raw=[5.0, 4.0, 5.0], risk_score=56.00, representation=[0.99, 0.86]
score_gap(line_A, line_B) = 0.0
representation_gap(line_A, line_B) = 3.09
```

- `risk_score` 是人用单一标准压缩出来的单维分数。
- `representation` 则把同一输入重新展开到从数据中算出的两个辅助轴上，因此通常能把`温度与压力方向的差异`和`返工呼叫方向的差异`分开读。
- 真正的深度学习表征学习不会停在这种手工解释轴或简单分解上，而会在学习过程中形成更多中间表征，并同时调整哪些表征更有利于任务。

第一项结果，是人手工写出的单行风险分数。`line_A` 和 `line_B` 的分数都为 `43.00`，因此在这一视角下它们看起来像是同样风险。

![表征学习示例中的 hand-crafted risk score](/AiBook/assets/part-05/chapter-10/representation-risk-score-zh.png)

第二项结果，是把同一输入放到两个辅助表征轴上的坐标。在单行分数里相同的 `line_A` 和 `line_B`，在表征坐标里却被拉开，因此原本被单一分数盖住的维护模式差异可以被重新读出来。

![表征学习示例中的二维 representation 坐标](/AiBook/assets/part-05/chapter-10/representation-coordinate-space-zh.png)

再把这两种结果并排比较一次，表征学习带来的差异会更清楚。

| 比较 | 现在应该抓住的重点 |
| --- | --- |
| `risk_score` | 设备产线只会被排成一条单维风险线。 |
| `representation` | 同一条产线也可能在两个轴上暴露出不同类型的风险。 |
| `line_A` vs `line_B` | 只看分数会像是相同风险，但在 representation 里，它们仍是`温度-压力迁移型产线`和`返工扩散型产线`这两种相距较远的模式。 |

读输出数字时，也要把`分数差`和`表征坐标差`分开看。

| 比较 | 输出里先看到的事实 | 只看分数时容易留下的解读 | 结合表征学习后会改变的解读 |
| --- | --- | --- | --- |
| `risk_score` | `line_A` 和 `line_B` 的分数差是 `0.0`。 | 很容易把两条产线读成同一风险状态。 | 单行分数会把温度报警、压力波动、返工呼叫的不同组合压扁，从而隐藏不同维护模式。 |
| `representation` | 同样两条产线的坐标距离是 `3.09`，并不小。 | 会误以为分数一样时，表征坐标的差异被夸大了。 | 新坐标系会分别保留温度与压力方向的差异，以及返工呼叫方向的差异，因此总分相同背后的模式差异会重新显现。 |
| `line_A` vs `line_B` | 两者都有风险信号，但突出的轴不同。 | 因为风险分数相同，就容易觉得同一套后续措施就够了。 | 表征坐标不同，意味着后续点检顺序和需要的处理动作也可能不同。 |

如果把 `line_B` 的 `rework_calls` 降到 `1.0` 后再执行一次，`line_B` 的分数和表征坐标都会变化。这时真正要抓住的问题不是`哪个分数更大`，而是`当输入组合改变时，人写的一行风险分数和从数据得到的表征坐标，会不会以相同方式移动`。

表征学习（representation learning）之所以是深度学习教学里的核心概念，是因为只有抓住它，下面这些问题才能放在同一条线上理解。

- 为什么深度学习并不只是一个更大的线性回归
- 为什么 CNN、RNN、Transformer 会表现得强
- 为什么 embedding 和 LLM 的内部表示如此重要

从历史脉络看，更该确认的转折是：思考重心从 feature engineering，转到了 data-driven internal representation 的学习。只用 GPU 或规模去解释深度学习的扩散，只解释到了其中一半；还要把表征学习一起放进去，整体脉络才算完整。

这里可以先停一下，把`什么时候应该先提表征学习视角，而不是先报结构名字`短暂固定下来。这样后面读 CNN、RNN、Transformer 时，共同的理解主轴会更稳。

| 先想到的问题 | 为什么要先用表征学习视角 | 后面会继续接到哪里 |
| --- | --- | --- |
| 为什么同一输入需要更会区分的内部坐标？ | 因为比原始数值更适合预测的中间表征，往往决定了性能差异。 | 深层中表征会怎样继续变化 |
| 为什么传统 feature engineering 会有明显边界？ | 因为人预先写下的规则，很难完全覆盖复杂组合和潜在模式。 | 不同领域结构更擅长学出哪些表征 |
| 为什么 CNN、embedding、LLM 能放在同一条线上解释？ | 因为不同结构都在追求让内部表征变得更有用这一共同目标。 | 图像、序列、长上下文中的表征学习 |

## 检查清单

- 能解释表征学习（representation learning）和手工特征设计有什么不同吗？
- 能用内部表征的视角回答`深度学习到底学到了什么`吗？
- 能说明表征学习是模型自己形成有用内部特征的过程吗？
- 能指出传统特征工程和深度学习的差异，关键就在于`由谁来形成特征`吗？
- 能用一个实际场景说明，人写的单一分数与模型形成的多维表征有何不同吗？
- 能把深度学习的转折解释成不仅是计算资源扩大，也包括表征学习能力扩大吗？
- 当结构名词很多、共同理解主轴变模糊时，能先想到表征学习视角吗？
- 当需要把 CNN、embedding、LLM 放到同一条线上时，能重新指出它们都在追求更有用的内部表征吗？

## 来源与参考资料

- Yoshua Bengio, Aaron Courville, Pascal Vincent, `Representation Learning: A Review and New Perspectives`, IEEE TPAMI, 2013，确认日期：2026-07-19。[https://arxiv.org/abs/1206.5538](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016，确认日期：2026-06-29。[https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, `ImageNet Classification with Deep Convolutional Neural Networks`, NeurIPS 2012，确认日期：2026-07-19。[https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html){: target="_blank" rel="noopener noreferrer" }
