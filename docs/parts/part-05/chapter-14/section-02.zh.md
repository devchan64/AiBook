# P5-14.2 Transformer block 的四个部件分别负责什么？

> Section ID: `P5-14.2`
> Version: `v2026.07.20`

在 P5-14.1 里，我们已经看到，只用 self-attention 解释 Transformer 是不够的。现在需要更直接地拆开 block 里面的角色分工。

在 Transformer block 里，self-attention、feed-forward network、residual connection、layer normalization 分别负责什么？

核心不是背部件名字，而是区分角色。要读懂同一个 token 表示在 block 里经过的路径，就必须区分`关系读取`、`按位置加工`、`保留原始信息`、`稳定数值范围`。

## block 角色分工处理的问题

- self-attention 负责什么？
- feed-forward network 和 attention 有什么不同？
- residual connection 与 layer normalization 为什么常常一起出现？

| 本节现在要读的内容 | 交给后续小节的内容 |
| --- | --- |
| 各部件在 block 中负责的角色 | 用数字例子看表示实际怎样移动 |
| 关系读取和按位置加工的差别 | 并行处理和长上下文的计算感觉 |

## self-attention 读取关系

正如第 13 章看到的，self-attention 是每个 token 参考同一序列里其他 token，并重新计算自己表示的方式。

`self-attention 是一个装置：它决定为了理解当前这个 token，现在应该更强地看句子里的哪里。`

核心是`关系读取`。它让当前 token 从句子里的其他位置带回自己需要的上下文。

## feed-forward network 加工当前位置表示

self-attention 会混合 token 之间的关系，但这个结果并不会自动成为足够好的表示。feed-forward network 会把已经混入上下文的当前位置表示，再做一次非线性加工。

`如果 attention 是把和其他 token 的关系反映进来、混合上下文，那么 feed-forward 就会把每个位置的表示再加工得更丰富。`

这里的`每个位置`很重要。self-attention 更接近决定当前位置要从其他位置带回什么信息；feed-forward network 则是在同一个位置内部改变已经混合好的表示。相同的 feed-forward network 会应用到各 token 位置上，但由于输入表示不同，各位置被打磨出的意义也不同。

```mermaid
--8<-- "assets/part-05/chapter-14/feed-forward-position-update-zh.mmd"
```

这张图里，每一行表示不同的 token 位置。虚线表示相同的 feed-forward network 权重会在多个位置共享，实线表示每个位置的表示会在自己的位置内部被分别加工。因此 feed-forward network 不是重新选择要参考哪个 token 的装置，而是把已经混入上下文的表示，改成该位置的下一个表示。

以工作许可句为例，attention 会让 `restart` 位置同时看到 `pressure unreleased` 和 `held`。feed-forward network 会在当前位置内部再次加工这个结果，让 `restart` 表示不再只是一个简单动作名，而更像是`因为带有条件而必须被阻断的动作`。

只看一个 token 时，差异会更清楚。

| 阶段 | 首先提出的问题 | 角色 |
| --- | --- | --- |
| self-attention | 这个 token 应该参考其他 token 中的哪些？ | 读取外部关系 |
| feed-forward | 混入参考上下文后的当前表示，要在这个位置怎样改变？ | 加工当前位置内部的表示 |

所以不能把 feed-forward network 读成简单后处理。attention 打开的是`要一起看什么`，feed-forward 负责的是`混合后的表示要怎样成为当前位置的下一个表示`。只有抓住这个差别，才能把 Transformer block 读成有角色分工的重复单元，而不是 attention 一个部件。

为什么 feed-forward network 能把相同权重应用到多个位置，同时又在每个位置产生不同表示，会在 [P5-14.6 补充学习：feed-forward network 为什么负责按位置表示加工](section-06.zh.md) 中另行整理。

## residual connection 留下原始信息流

在深层神经网络里，新的计算不断重复时，原始信息可能被覆盖得太厉害，学习也可能变得不稳定。residual connection 会把前一阶段表示和新计算结果一起传下去，从而保留原始信息流。

`不要只相信全新的计算，也把原始输入表示一起留下并送到下一阶段的安全装置。`

这里重要的是，residual connection 并不是消除新计算的装置。self-attention 或 feed-forward 做出的新表示仍然需要存在。只是如果只把新表示传到下一阶段，原来 token 本身具有的基本意义太容易被盖住。所以 residual connection 应该被读成留下`新计算结果 + 原始输入表示`的路径。

```mermaid
--8<-- "assets/part-05/chapter-14/residual-connection-skip-path-zh.mmd"
```

这张图里，实线路径是新计算生成的表示，虚线路径是原始输入表示绕过后再相加的路径。residual connection 的核心不是阻止新计算，而是让新计算和原始表示一起进入下一阶段。

如果 feed-forward 负责`当前表示要怎样改变`，residual connection 负责的是`改变后的表示如何不完全失去原来的出发点`。如果 layer normalization 是整理数值范围的装置，residual connection 更接近留下信息通过的旁路。

| 区分 | 首先提出的问题 | 角色 |
| --- | --- | --- |
| feed-forward network | 混入上下文后的当前表示要怎样改变？ | 生成新表示 |
| residual connection | 新表示会不会完全盖住原始表示？ | 把原始信息流也一起留下 |
| layer normalization | 这个范围是否便于下一步计算处理？ | 整理数值范围 |

这个差别能避免把 residual connection 降低成单纯加法。更准确的直觉是：`即使新计算进入，也给原始信息留下通路，让深层 block 重复能撑住的装置`。

为什么 residual connection 不是简单跳过，而是让原始表示与新计算一起传下去的路径，会在 [P5-14.7 补充学习：residual connection 为什么留下原始表示的路径](section-07.zh.md) 中另行整理。

## layer normalization 整理数值范围

多层和大矩阵运算反复出现时，表示值的大小和分布可能会摇晃。layer normalization 会把每个位置的表示整理到更容易处理的范围，让下一步计算不那么摇晃。

`layer normalization 是一种装置：它整理表示值的大小和分布，让下一步计算能稳定继续。`

这里的整理，不是重新判断意义。self-attention 和 feed-forward 做出的表示由多个数字轴组成，再加上 residual connection 后，有些轴可能过大，有些轴可能相对较小。如果数值尺度持续散开，即使下一步 attention 或 feed-forward 接收的是同类输入，也会在很难处理的范围里计算。

layer normalization 会在一个位置的表示内部重新调整数值的平均和分散程度，让下一个部件能从相近的基准线开始计算。入门阶段不用背公式，可以先这样读。

```mermaid
--8<-- "assets/part-05/chapter-14/layer-normalization-value-scale-zh.mmd"
```

这张图里重要的是，layer normalization 不会重新选择 token 之间的关系，也不会额外添加保留原始信息的路径。它只是重新对齐一个位置表示内部的数值范围，避免下一步 self-attention 或 feed-forward 收到过度摇晃的输入。

| 容易误解的读法 | 更合适的读法 |
| --- | --- |
| layer normalization 会选择意义 | 选择意义更直接由 attention 和 feed-forward 负责 |
| 它像 residual connection 一样留下原始信息 | 留下原始信息路径的是 residual connection |
| 它只是把数值变小 | 它把数值分布整理到下一步计算能处理的基准线 |

所以 Transformer block 中 residual connection 和 layer normalization 常常一起出现，但它们做的不是同一件事。residual connection 留下`信息通过的路径`，layer normalization 则对齐`计算基准线`，让经过那条路径的表示在下一步计算里不至于过度摇晃。

为什么 layer normalization 是一个位置表示内部的数值基准线整理，而不是意义选择，以及它和 batch normalization 有什么不同，会在 [P5-14.8 补充学习：layer normalization 为什么要对齐数值基准线](section-08.zh.md) 中另行整理。

把四个部件放在一起看，同一个 token 表示面对的问题其实不同。

| 部件 | 在表示中首先看的东西 | 不直接负责的事 |
| --- | --- | --- |
| self-attention | 当前位置应该参考哪个其他位置 | 在当前位置内部重新加工参考到的表示 |
| feed-forward network | 混入上下文的当前位置表示该怎样改变 | 选择新的参考 token 位置 |
| residual connection | 新计算是否完全盖住原始表示 | 直接创造新意义 |
| layer normalization | 数值范围是否便于下一步计算处理 | 选择意义或保留原始信息 |

## 如果画得非常简单

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-block-flow-zh.mmd"
```

这张图把一个 Transformer block 压缩到入门层次。可以把流程读成：`关系读取 -> 加回并整理原始表示 -> 加工当前位置表示 -> 再次稳定传递`。

## 案例与示例

### 案例：用四个部件读取 `restart` 位置表示

看一句工作许可句：`Restart is held while the pressure remains unreleased.` 当前关注的位置是 `restart`。如果人只快速看单词，很容易把 `restart` 读成单纯执行动作。但句子里还有 `pressure unreleased` 这个条件和 `held` 这个判断。

这里太容易提前下的判断是：`出现了 restart 这个词，所以这是执行请求。` 如果按 Transformer block 的角色来读，这个判断不是一下子被改掉的。同一个位置表示会在经过多个部件时回答不同问题。

先把输入按 token 位置拆开，可以这样看。

| 位置 | token | 理解 `restart` 时承担的线索 |
| --- | --- | --- |
| 1 | `pressure` | 说明正在讨论什么条件的对象 |
| 2 | `unreleased` | 表示条件尚未解决的状态 |
| 3 | `while` | 把前面状态连接成后面动作的条件 |
| 4 | `restart` | 当前要解释的动作 |
| 5 | `held` | 表示该动作不是执行，而是暂缓的判断 |

如果只单独看 `restart` 位置，它像是执行动作。但本节中心不是 `restart` 最终是什么意思，而是这个位置表示在 Transformer block 中经过各部件时怎样改变。

| 读取阶段 | 当前 `restart` 位置提出的问题 | 过快阅读会产生的误解 |
| --- | --- | --- |
| 起始表示 | 这个位置的基本单词是什么？ | 只看到 `restart` 这个动作名 |
| self-attention | 这个位置应该一起看句子里的哪些地方？ | 以为 attention 已经给出最终判断 |
| feed-forward network | 混入上下文后，当前位置表示要怎样改变？ | 以为 feed-forward 会再次选择相关 token |
| residual connection | 新计算会不会完全盖住原始动作轴？ | 以为 residual 会跳过新计算 |
| layer normalization | 数值范围是否便于下一步计算处理？ | 以为 normalization 会只留下重要意义 |

在 self-attention 阶段，`restart` 位置会同时参考 `pressure unreleased` 和 `held`。这里要确认的结果是，`restart` 不再只是孤立的执行单词，而是同时看到了前面的条件和后面的判断。但此时当前位置表示还没有完全整理成`有条件的阻断动作`。

在 feed-forward network 阶段，attention 混入的上下文会在当前位置内部再次加工。`restart` 表示会比单纯动作名更清楚地转向：因为压力条件而应该被暂缓的动作。这个阶段的核心不是选择新的参考单词，而是把已经带进来的上下文变成当前位置表示。

在 residual connection 阶段，不会只留下新加工出的阻断意义。原来的 `restart` 动作轴也必须保留，后续 block 才不会忘记到底要暂缓的是什么。所以 residual connection 不是跳过新计算的路径，而是把新计算结果和原始输入表示一起传下去的路径。

在 layer normalization 阶段，不会重新选择意义。经过 attention、feed-forward、residual 后，当前表示的多个数值轴已经混在一起，layer normalization 会把它整理到下一个 block 能处理的基准线。对齐数值范围和判断意义不是同一件事。

只缩小到 `restart` 位置表示的变化，可以写成下面这样。

| block 内部位置 | 用语言解释 `restart` 位置表示 | 这里要学到的角色区分 |
| --- | --- | --- |
| 输入表示 | `restart` 这个动作名 | 前面条件和后面判断还没有充分反映 |
| self-attention 之后 | 同时看过 `pressure unreleased` 和 `held` 的动作 | 带回了关系线索，但还没有最终打磨当前位置表示 |
| feed-forward 之后 | 因压力条件而更偏向暂缓而不是执行的动作 | 在当前位置内部再次加工了混入上下文的表示 |
| residual 之后 | 暂缓侧意义和原始 `restart` 动作轴一起留下的表示 | 新计算没有完全盖住原始动作信息 |
| layer normalization 之后 | 被整理到下一个 block 易处理范围里的表示 | 对齐的是计算基准线，不是重新选择意义 |

因此，这个案例的输出不是单纯结论 `restart is held`。更重要的输出是：`关系读取`、`按位置加工`、`保留原始信息`、`稳定数值范围`是不同部件的工作。只要这个区分固定下来，就能把 Transformer block 读成多个角色反复出现的表示更新单元，而不是`attention 给出答案的装置`。

如果从输出角度收住同一个案例，可以这样整理。

| 部件 | 在这个案例中直接造成的变化 | 不直接负责的事 |
| --- | --- | --- |
| self-attention | 让 `restart` 位置同时看到 `pressure unreleased` 和 `held` | 把当前位置表示加工成最终意义 |
| feed-forward network | 把混入上下文的 `restart` 加工到 `conditional blocked action` 一侧 | 选择新的参考 token 位置 |
| residual connection | 把 `conditional block` 意义和原始 `restart` 动作轴一起留下 | 重新选择重要意义 |
| layer normalization | 把合并后的表示数值范围整理成下一步计算基准线 | 保留原始动作轴或重新选择关系 |

这个案例要确认的结果是：`restart` 表示不是像魔法一样一次改变。self-attention 读取关系，feed-forward 加工当前位置表示，residual connection 留下原始信息流，layer normalization 为下一步计算对齐数值基准线。只有把这四个问题拆开，才能把 Transformer block 读成有角色分工的重复单元，而不是 attention 一个部件。

## 练习与例子

### 示例：用数字跟踪 action token 表示移动

把同样的角色区分缩小到另一个运维日志场景里，就可以直接看到：即使是同一个 action token，只要 attention 行不同，表示移动的方向也会不同。这里不计算 layer normalization，只跟踪 `input -> after attention -> after feed-forward -> after residual`。值范围整理会在下一节稳定化内容里另行处理。

读代码时，不要一次记住整个矩阵。先只看 action token 对其他线索参考得有多强。

| 要操作的值 | 要观察的输出 | 要确认的问题 |
| --- | --- | --- |
| action token 行的 attention 权重 | `after attention` | action token 更强地混入自身、症状线索，还是部署线索？ |
| 同一个混合表示经过 feed-forward 之后 | `after feed-forward` | 混入的上下文在当前位置表示内部怎样被重新加工？ |
| residual 之后的 action token | `after residual` | 原始动作轴仍然保留时，block 输出方向怎样改变？ |

```python
# 这个例子比较 rollback 是否确认时，action token 表示怎样经过 attention、feed-forward、residual 移动。
import numpy as np

tokens = np.array([
    [1.0, 0.2],   # symptom token: urgency high
    [0.8, 0.5],   # deploy clue token: cause evidence medium
    [0.3, 1.0],   # action token: recovery status important
])

attention_cases = {
    "rollback_confirmed": np.array([
        [0.6, 0.3, 0.1],
        [0.2, 0.5, 0.3],
        [0.1, 0.3, 0.6],
    ]),
    "rollback_not_confirmed": np.array([
        [0.6, 0.3, 0.1],
        [0.3, 0.5, 0.2],
        [0.3, 0.5, 0.2],
    ]),
}

ff_weights = np.array([
    [1.1, 0.4],
    [0.2, 1.0],
])

for name, attention_weights in attention_cases.items():
    contextual = attention_weights @ tokens
    ff_output = contextual @ ff_weights
    residual_added = ff_output + tokens
    action_trace = [
        ("input", tokens[2]),
        ("after attention", contextual[2]),
        ("after feed-forward", ff_output[2]),
        ("after residual", residual_added[2]),
    ]

    print(f"[{name}]")
    print("action attention row =", np.round(attention_weights[2], 3))
    print("action token stage trace")
    for stage, values in action_trace:
        print(f"{stage:24s}", np.round(values, 3))
    print("---")
```

输出示例可以这样读。

```text
[rollback_confirmed]
action attention row = [0.1 0.3 0.6]
action token stage trace
input                    [0.3 1. ]
after attention          [0.52 0.77]
after feed-forward       [0.726 0.978]
after residual           [1.026 1.978]
---
[rollback_not_confirmed]
action attention row = [0.3 0.5 0.2]
action token stage trace
input                    [0.3 1. ]
after attention          [0.76 0.51]
after feed-forward       [0.938 0.814]
after residual           [1.238 1.814]
---
```

解说：两个场景从相同输入 token 开始，但 action token 的 attention 行不同，所以表示移动路径也不同。`rollback_confirmed` 中，从 attention 之后开始，复归状态轴保留得更大；`rollback_not_confirmed` 中，症状/原因轴相对保留得更大。这个差异会经过 feed-forward 和 residual 留到 block 输出方向里。

自己确认时，可以把 `rollback_not_confirmed` 的 action token 行 `[0.3, 0.5, 0.2]` 改成 `[0.2, 0.4, 0.4]` 这样总和仍为 1 的值。action token 越多参考自身，`after attention` 之后复归状态轴怎样改变，就能直接比较。

![action token 的阶段性表示移动](/AiBook/assets/part-05/chapter-14/transformer-block-action-stage-trace-zh.png)

### 练习：给角色命名

判断下面说明最直接连接到哪个部件。

| 说明 | 更直接连接的部件 | 解说 |
| --- | --- | --- |
| 决定当前 token 应该更强地看句子里的哪些其他 token | self-attention | 关系读取角色 |
| 把混入上下文的 `restart` 表示在当前位置内部改向 `conditional block` | feed-forward network | 把 attention 带来的关系重新加工成当前位置表示 |
| 相同加工装置应用到各 token 位置，但因为每个位置的输入表示不同，会被打磨成不同意义 | feed-forward network | feed-forward 是重新变换各位置表示，而不是再次选择 token 关系 |
| 把加工出的 `conditional block` 意义和原始 `restart` 动作轴一起留下 | residual connection | 把新计算和原始表示一起传下去，保留信息流 |
| 不生成新表示，而是留下原始表示能通过的路径 | residual connection | 这是它和 feed-forward 的区别 |
| 新计算和原始表示相加后，重新对齐数值基准线 | layer normalization | 整理数值分布，让下一步计算稳定继续 |
| 传给下一步计算前整理数值范围 | layer normalization | 稳定化角色 |

解说：这个练习的核心不是背部件名字，而是区分：即使在同一个 block 里，`参考什么`、`怎样改变当前表示`、`怎样留下原始信息`、`怎样稳定计算`也是不同问题。

### 练习：修改误解句子

下面的句子都只说对了一部分，或者混在了一起。把它们改成更准确的说明。

| 误解句子 | 更准确的说明 | 解说 |
| --- | --- | --- |
| feed-forward network 会再次选择相关 token | self-attention 让模型参考相关 token；feed-forward network 会重新加工已经混入上下文的当前位置表示 | 要区分`看什么`和`这个位置表示怎样改变` |
| residual connection 让模型跳过新计算 | residual connection 会把新计算结果和原始输入表示一起传下去 | 它不是去掉新计算，而是留下原始信息的通路 |
| layer normalization 只留下重要意义 | layer normalization 会把一个位置表示的数值范围对齐到下一步计算能处理的基准线 | 核心是数值分布稳定化，不是意义选择 |
| 只要理解 self-attention，就足以说明 Transformer block | self-attention 负责关系读取，feed-forward、residual connection、layer normalization 分别负责表示加工和稳定化 | block 是有角色分工的重复单元，不是 attention 一个部件 |

解说：修改这些句子的目的不是记术语，而是建立边界感。四个部件都在同一条表示流里，但如果`关系选择`、`位置内变换`、`信息保留`、`数值稳定化`混在一起，后面读 Transformer 结构时计算流就会变得模糊。

## 检查清单

- 能说明 self-attention 和 feed-forward 的角色差异吗？
- 能把 residual connection 解释成留下原始信息流的装置吗？
- 能把 layer normalization 解释成深层 block 重复的稳定化装置吗？
- 能说明 action token stage trace 里的 `after attention`、`after feed-forward`、`after residual` 分别显示了什么表示移动吗？

## 来源与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 确认日期：2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
