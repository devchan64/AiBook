# P5-14.1 Transformer 的基本组成

Section ID: `P5-14.1`
Version: `v2026.07.17`

在 P5-13.2 里，我们已经说明：self-attention 是同一序列里的 token 彼此直接参考的方式，并且它会通向 Transformer 的核心直觉。这里接着就会出现下一个问题。

那么，Transformer 是不是一个只有 self-attention 的结构？还是说，在它周围还有其他基本组件一起构成这个结构？

Transformer 可以被理解成这样一种结构：它通过 self-attention 读取上下文关系，通过 feed-forward network 再加工每个位置的表示，并通过 residual connection 与 layer normalization 让这个计算 block 能稳定地继续下去而不至于崩掉。

当这些 block 组件名称又开始混在一起时，最好一起回到英文概念词汇表里的 [Transformer](/AiBook/en/reference/concept-glossary/#transformer)、[feed-forward network](/AiBook/en/reference/concept-glossary/#feed-forward-network)、[residual connection](/AiBook/en/reference/concept-glossary/#residual-connection)、[layer normalization](/AiBook/en/reference/concept-glossary/#layer-normalization) 条目重新对齐。

## 本节范围

- Transformer 的核心 block 由哪些部件组成？
- self-attention、feed-forward network、residual connection、layer normalization 分别扮演什么角色？
- 为什么这个结构会看起来像 RNN 之后的一个大转折点？
- 在 encoder / decoder 的细节之前，应该先抓住什么大图景？

本节首先要抓住的核心，是`Transformer 不是一个叫 self-attention 的单独想法，而是一种把上下文读取、表示加工、block 维持装置打包在一起的结构`。本章的手柄也会从`应该怎样参考需要的位置`，转向`这种参考计算该通过怎样的 block 结构被稳定地重复下去`。所以这里比起 optimizer、regularization 这类训练过程，我们更先看的是：Transformer block 里面的各个部件如何分工。

| 这一节当前要读的内容 | 交给下一节去读的内容 |
| --- | --- |
| self-attention、feed-forward、residual connection、normalization 在一个 block 里怎样分工 | 重复这个 block 之后，在并行处理、长上下文成本、计算规模上会发生什么变化 |
| block 内部的关系读取与表示加工 | 大规模训练流程与 long-context 优化 |

multi-head attention 与 query、key、value 的入门说明，会在补充学习 P5-13.3 里回收。并行处理和长上下文的优势，会在 P5-14.2 继续展开；encoder-only、decoder-only、encoder-decoder 的细分，则会在 P6-3.1 里从 LLM 视角再次比较。也就是说，这里先收住的是`Transformer block 里各组件怎样分工`。

在这里，我们不是顺着整篇 Transformer 论文往下走，而是先抓住：在 block 层级上到底组合了什么。

## 本节目标

- 能把 Transformer 解释成不是只有 self-attention，而是几个核心部件的组合。
- 能说明各个部件分别承担上下文读取、表示加工、学习稳定化中的哪一类角色。
- 以后即使去看别的模型家族，也能重新想起 Transformer 的基本 block。
- 能通过可运行的 Python 例子，直观确认 token 表示如何经过多个阶段而发生变化。

## 本节的阅读顺序

1. 先确认在 P5-13.2 看到的 self-attention 在 Transformer 里处于什么位置。
2. 然后分开阅读 self-attention、feed-forward、residual、layer normalization 各自的角色。
3. 接着看这些部件为什么会被绑成一个可重复的 block。
4. 最后整理：为什么这种 block 结构后来会成为生成模型的基本单位。

## 从很大的图景看 Transformer

先牢牢抓住下面四个元素，就已经够用了。

1. self-attention
2. feed-forward network
3. residual connection
4. layer normalization

把这四个元素说得再简单一点，就是下面这样。

- self-attention：决定哪些 token 应该参考哪些其他 token
- feed-forward：把每个位置的表示再加工一次
- residual connection：让原始信息流和新计算一起留下来
- layer normalization：整理数值尺度，帮助学习更稳定

也就是说，Transformer 是一种不断重复的结构：`一个 block 先读取上下文关系 -> 再加工表示 -> 再保持信息流稳定`。

它们的分工可以先用下面这张表来整理。

| 组件 | 首先要抓住的角色 |
| --- | --- |
| self-attention | 读取与其他 token 之间的关系 |
| feed-forward | 再加工每个位置的表示 |
| residual connection | 让原始信息流和新结果一起保留 |
| layer normalization | 整理数值范围，让学习不那么摇晃 |

如果在这里就先把最容易混在一起的两类问题分开，和下一节之间的边界会更清楚。

| 这一节当前回答的问题 | 交给下一节的问题 |
| --- | --- |
| `在一个 block 里，attention、feed-forward、residual、normalization 是怎样分工的？` | `这个 block 被重复很多次之后，为什么会在 GPU 并行处理和长上下文计算里显得更有优势？` |
| `表示是按照什么顺序被读取和加工的？` | `计算成本、处理速度和长上下文成本会怎样变化？` |

如果我们只追着一个当前 token 表示走，各个组件角色之间的差异会更直接。

| 同一场景 | 先应该看的组件 | 这个组件立刻在做什么 |
| --- | --- | --- |
| 当前 token 正在决定自己该更强地参考句子里的哪里 | self-attention | 通过读取和其他位置的关系，把需要的上下文聚合回来 |
| 聚合进来的上下文已经混到当前表示里以后，还要继续加工这个表示 | feed-forward | 在当前位置再加工一次表示，让特征更丰富 |
| 防止新计算把原始输入流覆盖得太厉害 | residual connection | 把之前的表示也一并保留，让信息流继续往下走 |
| 在把结果送去下一个计算之前整理数值范围 | layer normalization | 整理表示的大小与分布，让后续计算不那么摇晃 |

如果说 P5-13.2 是在讲`token 彼此参考的计算`，那么这一节就是要说明：在真实模型里，这个计算是如何和周围的支撑组件一起组成一个 block 的。

这里读者尤其要抓住的一点，是这并不是`各个组件彼此分散地摆在那里`。通常最容易理解 Transformer 的方式，是按下面这串问题顺序去读一个 block。

1. 当前 token 在其他 token 里该更强地参考哪里？
2. 聚合完这些上下文以后，当前这个位置的表示该怎样被重新反映？
3. 这个表示在每个位置上还要不要再加工一次？
4. 在整个过程中，原始信息和稳定性是怎样被保住的？

也就是说，把 Transformer block 读成`关系读取 -> 按位置加工 -> 稳定传递`，会更自然。

## self-attention 负责什么

正如在 P5-13 里看到的，self-attention 的角色，是让每个 token 重新参考其他 token，并重新计算出带有上下文的表示。

`self-attention 是一个装置：它决定为了理解当前这个 token，现在应该更强地看句子里的哪里。`

它的核心就是`读取关系`。

## 为什么还需要 feed-forward network

光靠 self-attention，确实可以读出 token 之间的关系，但我们还需要一个过程：把每个位置的表示再做一次更非线性的加工。这时 feed-forward network 就出现了。

关键在于，attention 负责把上下文关系混进来，而 feed-forward 则在当前位置进一步、更非线性地加工这个表示。

`如果 attention 是把和其他 token 的关系混进来，那么 feed-forward 就像一个小型 MLP，会把每个位置的表示再加工得更丰富。`

这种差别，即使只看一个 token 也能读出来。self-attention 这一段在问：`这个 token 要从其他 token 那里拿回什么？` 而 feed-forward 这一段在问：`当前这个已经混进上下文的表示，应该怎样在这个位置上再被打磨一次？` 也就是说，attention 更接近`和外部的关系`，feed-forward 更接近`当前位置内部的加工`。

## 为什么需要 residual connection

在深度学习里，层数一深，信息可能会被改得过头，或者学习会变得不稳定。residual connection 可以被看成一种装置：它会让前一阶段的表示继续和新结果一起流到下一步。

核心点在于，它不会只相信全新的计算结果，而是会把原来的输入表示也一并留住，再一起送下去，这样学习就不那么容易摇晃。

`不要只相信全新的计算结果；把原始输入表示也一起留着送下去，这是一种安全装置。`

residual connection 会减少信息损失，也会让学习更稳定。

## 为什么还会出现 layer normalization

当很多层和大矩阵计算不断重复时，数值的尺度和分布会影响训练稳定性。layer normalization 可以被看成一种装置：它会把每个位置的表示整理到更容易处理的范围里，从而帮助学习过程。

关键在于，它会整理表示值的大小和分布，让下一步计算更稳定地继续下去。

`layer normalization 是一种装置：它整理表示值的大小和分布，让下一步计算不那么摇晃。`

也就是说，Transformer 不只是有`强 attention`，它同时也带着`让深层学习能撑住的稳定化装置`。

## 如果把它画得非常简单

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-block-flow-zh.mmd"
```

这张图把一个 Transformer block 压缩成入门层次的样子。

如果把这条流程一行一行重新读，会是下面这样。

- `self-attention`：把和其他 token 的关系反映进来
- `add + norm`：整理结果，让原始信息流不要丢得太厉害
- `feed-forward`：再加工每个位置的表示
- `add + norm`：再一次稳定地把表示送往下一个 block

也就是说，Transformer block 并不是`把上下文混进来就结束`，而是`混完上下文之后，还要继续加工表示，并稳定地传给下一个 block`。

如果只盯着同一个当前表示看它在 block 里面怎样变化，就可以读成下面这样。

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-representation-update-zh.mmd"
```

从这张图里首先要固定住的是下面几点。

- self-attention 先决定`该参考什么`，并把上下文混进当前表示。
- feed-forward 会把已经混进上下文的当前表示，再加工成在这个位置上更清楚的意义。
- residual 和 layer normalization 并不会只留下新表示，而是会在不丢掉原始轴线的同时，把结果稳定地送往下一个 block。

## 为什么这种结构会重要

Transformer 看起来像一个大转折点，并不是因为它只是多加了一层新东西。在本节范围里，真正要先看的核心，是下面这些组件被组合成了`一个可重复的 block`。

- 以 attention 为中心的上下文参考
- 再加工每个位置表示的 feed-forward
- 保留原始信息流和数值范围的 residual 与 normalization

也就是说，Transformer 是一种架构：它把`sequence modeling 的核心计算`重新打包成了新的 block 单元。

如果在这里先停一下，短暂固定住`什么时候应该先从 Transformer block 组成的角度来读，而不只是从 attention 本身的角度来读`，下一节关于并行处理的说明就会更稳。

| 先想到的问题 | 为什么要先从 Transformer 基本组成的角度来读 | 下一节会继续接什么 |
| --- | --- | --- |
| 为什么模型不会只有 self-attention 就结束？ | 因为除了上下文读取，还必须有按位置加工和稳定传递装置，block 才能成立 | 当这个 block 被反复重复时，计算感觉会怎样变化 |
| 为什么 residual connection 和 layer normalization 总是一起出现？ | 因为除了强上下文计算，还需要一个稳定化轴线，才能承受深层 block 的反复堆叠 | block 的反复堆叠在并行学习和规模扩展里意味着什么 |
| feed-forward 和 attention 到底哪里不同？ | 因为必须把关系读取和按位置加工分开看，block 里的角色才不会混掉 | 在长上下文与 GPU 计算里，整个 block 是怎样工作的 |

## 案例与示例

在进入案例之前，本节首先要看的不是`它会不会重新参考长上下文`，而是`当前表示在一个 block 里到底怎样变化`。也就是说，读案例时也不能只停在`它重新参考了什么`，还要一起看：`当前这个位置的表示后来是怎样被打磨的`、`原始信息是怎样被保住的`、以及`它是怎样被稳定地送往下一个 block 的`。

| 情况 | 首先要看的当前表示变化 | Transformer block 是怎样帮忙的 |
| --- | --- | --- |
| 工作许可句子 | 当前动作表达必须在`简单重启`和`条件性暂缓`之间被分开 | self-attention 把条件和动作连起来，feed-forward 把当前表示加工成更清楚的动作状态 |
| 一句故障摘要 | 当前摘要表达必须在`模糊异常`和`带原因依据的异常`之间分开 | 先聚合相关线索，再把当前这个位置的表示往`因果摘要`方向加工得更清楚 |
| 一行运行备忘录 | 当前备忘录必须在`一般批准`和`带阻断条件的批准`之间分开 | 通过 residual 保留原始输入语义，再经过 normalization，让条件在下一个 block 里也能保持稳定 |

### 代表案例：解释一句工作许可句

想一想这样一句工作许可句：`在压力尚未释放时，重启应被暂缓。` 人匆忙读这句话时，很容易把`重启`和`暂缓`分开看，或者先只抓住动作词 `重启`。但实际上，为了安全，当前动作表达不应该被读成`批准`，而应该被读成`带条件的暂缓`。这里 self-attention 会先把 `压力未释放`、`重启`、`暂缓` 在同一句子里的关系连起来。接着 feed-forward 会在这些关系已经被聚合的基础上，把当前动作表达进一步加工得更清楚：不再是`一般作业指令`，而更像是`带条件的阻断指令`。residual connection 会把原来动作表达本来带着的基本意义继续留住，不让它完全丢失；layer normalization 则会在把改变后的表示送去下一个 block 时，整理好数值分布，避免过度摇晃。

所以，这个案例里要确认的结果是：当前动作表达是否没有只跟着`重启`这个词走，而是被读成了一个同时反映`压力未释放`和`暂缓`的条件性阻断表达。

同样的视角也会直接延伸到故障摘要句的打磨和运行备忘录的改写里。不过，本节真正要抓住的不是领域名称，而是`当前这个位置的表示，会怎样在一个 block 里被重新加工成更清楚的意义，并被稳定保留下来`。

| 人容易先看的标准 | 从 Transformer block 视角重新读时的标准 |
| --- | --- |
| 容易觉得只要有 attention，Transformer 就已经解释完了 | 只有把读取关系后的再次加工、原始信息保留和稳定性维护这些组件一起看到，block 才算闭合 |
| 容易觉得上下文一混完，最终判断就立刻出现了 | 只有 `上下文读取 -> 按位置加工 -> residual -> normalization` 按顺序连起来，当前表示的变化才真正可解释 |
| 容易觉得任务一变，模型结构就会大变 | 即使是工作许可句、故障摘要句、运行备忘录，也更准确的看法是：同一个 block 在重复，只是`当前表示会被怎样再加工`不同 |

如果再按每个 block 组件各自负责什么，把这三个案例重新拆开，就会更直接地看出：为什么只用`attention 一个部件`来结束整节说明是不够的。

| 案例 | self-attention 先负责什么 | feed-forward 接着负责什么 | residual + normalization 保住什么 |
| --- | --- | --- | --- |
| 工作许可句 | 把`压力未释放`、`重启`、`暂缓`和当前动作表达连接起来 | 把当前表示加工成更明确的`条件性阻断指令`，而不是`一般指令` | 在不丢掉原始动作意义的同时，让阻断条件稳定地延续到下一个 block |
| 故障摘要句 | 把`刚部署后`、`压力波动`、`无异常`这些线索连到当前摘要位置上 | 把当前句子加工成`带原因依据的摘要`，而不是`模糊异常` | 让整体情势感和具体依据之间的平衡在 block 重复中不至于塌掉 |
| 一行运行备忘录 | 把`interlock`、`未解除`、`重启`、`暂缓`连到当前备忘录表达上 | 把当前位置加工成`带阻断条件的暂缓句`，而不是`关于重启的一般句子` | 让重启动作这一原始轴线保留，同时阻断意义也稳定存在 |

## 练习与例子

这个例子的目标，是把构成 Transformer block 的两个核心阶段直接放到一个实际运维句子上来看，也就是`混合上下文的阶段`和`再次加工每个位置表示的阶段`。

在看代码之前，如果先按顺序看下面四个值，这一节的结构轴线就不容易散开。

| 先看的值 | 为什么应该先看它 |
| --- | --- |
| `contextual tokens` | 因为它会立刻显示：self-attention 是怎样先把故障响应日志里的不同线索混在一起的 |
| `feed-forward output` | 因为接着它能让我们看到 attention 混过的表示又会怎样在每个位置被再加工 |
| `after residual` | 因为它能确认：模型并不只用新计算结果，原始输入表示也会被一起保留下来 |
| `after simple layer norm` | 因为最后它能让我们抓住一种感觉：在送去下一个 block 之前，数值范围还会再被整理一次 |

输入：

- 三个 token 的初始表示
- 两种不同运维场景下的 attention 权重
- feed-forward 权重

输出：

- attention 前后 token 表示的变化
- 经过 feed-forward 之后的表示
- 加上 residual 路径之后的表示
- 经过简单 layer normalization 之后的表示
- `rollback confirmed` 与 `rollback not confirmed` 两个场景里，action token 表示是怎样变化的

问题场景：

- 在故障响应运维里，即使`事故征兆`、`部署线索`、`动作确认`写得相隔较远，也还是需要一起被读出来，所以我们要一步一步看：在这种场景里，Transformer block 怎样更新表示

要确认的概念：

- 一个 Transformer block 会把 attention 和 feed-forward 当成一个成套结构反复使用
- 只有把 residual 和 normalization 也放进来，才能理解表示是怎样稳定更新的
- 在一个运维句子场景里，如果我们问`动作确认线索进来之后，action token 表示到底怎么变`，block 内部分工会更清楚

在看代码之前，先猜一猜：在两种运维场景里，哪一个阶段会先开始发生变化，会更有帮助。

| 比较点 | 在 `rollback confirmed` 里先应该预测的变化 | 在 `rollback not confirmed` 里先应该预测的变化 |
| --- | --- | --- |
| `contextual tokens` | action token 会更强地混进动作确认线索 | action token 会更多保留事故征兆 / 部署线索一侧 |
| `feed-forward output` | 混入的动作上下文会更明显地反映到各位置表示里 | 因为确认不足的上下文仍然存在，动作表示就不会那么明显地朝恢复一侧移动 |
| `action token after residual` | 恢复轴会保留得更强 | 事故 / 原因轴会相对保留得更多 |

输入：

这里使用三个 token：`symptom`、`deploy clue`、`action status`，并比较 `rollback confirmed` 与 `rollback not confirmed` 两个场景。

```python
# 这个例子比较 rollback 已确认或未确认时，action token 表示在 Transformer block 内如何变化。
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

def simple_layer_norm(row):
    mean = np.mean(row)
    std = np.std(row)
    return (row - mean) / (std + 1e-6)

for name, attention_weights in attention_cases.items():
    contextual = attention_weights @ tokens
    ff_output = contextual @ ff_weights
    delta_from_input = ff_output - tokens
    residual_added = ff_output + tokens
    normalized = np.vstack([simple_layer_norm(row) for row in residual_added])

    print(f"[{name}]")
    print("contextual tokens =")
    print(np.round(contextual, 3))
    print("feed-forward output =")
    print(np.round(ff_output, 3))
    print("change from input =")
    print(np.round(delta_from_input, 3))
    print("after residual =")
    print(np.round(residual_added, 3))
    print("after simple layer norm =")
    print(np.round(normalized, 3))
    print("action token after residual =", np.round(residual_added[2], 3))
    print("---")
```

在输出里，两种场景都先比较 `action token after residual`，然后再往回追：这个差异其实在 `contextual tokens` 阶段是怎样形成的。

```text
[rollback_confirmed]
contextual tokens =
[[0.87 0.37]
 [0.69 0.59]
 [0.52 0.77]]
feed-forward output =
[[1.031 0.718]
 [0.877 0.866]
 [0.726 0.978]]
change from input =
[[ 0.031  0.518]
 [ 0.077  0.366]
 [ 0.426 -0.022]]
after residual =
[[2.031 0.918]
 [1.677 1.366]
 [1.026 1.978]]
after simple layer norm =
[[ 1. -1.]
 [ 1. -1.]
 [-1.  1.]]
action token after residual = [1.026 1.978]
---
[rollback_not_confirmed]
contextual tokens =
[[0.87 0.37]
 [0.76 0.51]
 [0.76 0.51]]
feed-forward output =
[[1.031 0.718]
 [0.938 0.814]
 [0.938 0.814]]
change from input =
[[ 0.031  0.518]
 [ 0.138  0.314]
 [ 0.638 -0.186]]
after residual =
[[2.031 0.918]
 [1.738 1.314]
 [1.238 1.814]]
after simple layer norm =
[[ 1. -1.]
 [ 1. -1.]
 [-1.  1.]]
action token after residual = [1.238 1.814]
---
```

这个例子里，首先要看的结果，是 action token 在 block 各阶段是往哪里移动的。`rollback confirmed` 和 `rollback not confirmed` 从同一组输入出发，但从 attention 混合上下文的阶段开始就已经分成不同路径，经过 feed-forward 和 residual 之后，最终留下的 action 表示也不一样。

![action token 的阶段性表示移动](/AiBook/assets/part-05/chapter-14/transformer-block-action-stage-trace-zh.png)

第二个结果，是把 residual 之后的 action token 单独拿出来比较。rollback 已确认的场景里，恢复状态轴保留得更强；未确认的场景里，紧急 / 原因轴相对保留得更多。看到这个差异，就更容易明白：为什么 Transformer block 不能只读成 attention，而要读成`上下文混合 -> 按位置加工 -> 保留原始信息`的组合。

![residual 之后的 action token 对比](/AiBook/assets/part-05/chapter-14/transformer-block-action-residual-compare-zh.png)

| 比较点 | rollback confirmed | rollback not confirmed | 为什么重要 |
| --- | --- | --- | --- |
| action token 参考到的上下文 | 动作确认 token 更强地保留了自己和原因线索 | 动作确认变弱后，事故征兆 / 部署线索一侧相对更大 | 因为即使是同一个 block，`更强地绑定哪些线索`也会随运维场景而变化 |
| action token after residual | `[1.026, 1.978]` | `[1.238, 1.814]` | 因为它显示：动作是否被确认，确实会把当前位置表示推向不同方向 |
| 解读方式 | `因为动作已确认，所以更强地反映恢复状态一侧` | `因为确认仍然不足，所以更怀疑警报与部署线索一侧` | 因为它说明：Transformer block 读取运维句子时，依靠的是关系重映射，而不是简单顺序 |

| block 阶段 | 如果只单独看这一阶段，容易出现的误解 | 从整个 block 来读时，需要纠正的点 |
| --- | --- | --- |
| self-attention (`contextual tokens`) | 容易觉得上下文混过一次以后，最终判断就已经完成了 | 这一阶段只是决定`要重新参考什么`，当前位置表示的再加工和稳定传递还没有结束 |
| feed-forward (`feed-forward output`) | 因为只是把数字再变换一次，所以容易被当成次要后处理 | 实际上它会把 attention 聚合来的上下文重新压进各位置表示里，因此即使是同一上下文，也会分出不同的位置解读 |
| residual (`after residual`) | 容易看成只是把前一个值简单加回来 | 它不会只相信新计算，而是把原始输入表示一起留下，因此 action token 原本持有的恢复状态信息不会直接消失 |
| layer normalization (`after simple layer norm`) | 容易被看成只是整理数值大小的次要步骤 | 它会重新对齐送往下一个 block 的表示范围，让 block 叠深以后计算也不那么摇晃 |

- 在 attention 阶段，每个 token 都会接收其他 token 的信息，因此原始表示会发生变化。
- 在 feed-forward 阶段，已经混入上下文的表示会按位置再次被变换。
- `after residual` 说明：模型不是只用新计算结果，而是会把原始 token 表示一起保留下来。
- `after simple layer norm` 说明：每个位置表示在进入下一阶段前，数值范围还会再被整理一次。
- 在运维句子场景里，关键问题是像 `rollback confirmed` 这样的远处线索，是否真的反映到了 action token 表示上。

也就是说，`rollback confirmed` 和 `rollback not confirmed` 的分叉虽然从 attention 阶段开始，但真正把这个差异稳定地送进 block 输出的，是包含 feed-forward、residual、normalization 在内的整套组合。如果只把 Transformer 读成`attention 很强的模型`，这一层分工就会消失。

这个例子说明：即使是同一份故障响应日志，只要出现 `rollback confirmed` 这句话，当前动作表示就可能发生变化。Transformer block 重要，不是因为它只是把 token 混在一起，而是因为它能把`运维判断所需的远处线索`重新反映进当前表示里。

| 先看到的输出信号 | 现在马上可以尝试的变化 | 不应只凭这个例子就仓促下结论的事 |
| --- | --- | --- |
| `action token after residual` 会随场景变化 | 提高或降低动作确认 token 的 attention 比重，比较运维判断表示会怎样变化 | 不要断言只靠一个 attention 数值就能完全决定真实运维优先级 |
| `contextual tokens` 会因场景而混得不同 | 改动事故征兆 token 与部署线索 token 的权重，观察哪类上下文会更强地进入 action token | 不要断言数字变化更大就一定代表表示学习更好 |
| `after simple layer norm` 被整理到相近范围 | 故意放大某个轴值，比较 normalization 前后差异会扩大多少 | 不要用这个简单 normalization 对比，替代真实 layer normalization 的全部实现细节 |

真实的 Transformer 会把 residual connection、layer normalization、multi-head attention 一起使用，但从大方向上看，最容易理解的还是这种 block 的重复。

## 如果从 block 组合视角重新读这个例子

上面的数字并没有实现整个 Transformer，但各组件之间的角色差异已经很清楚。

- `contextual tokens` 是 self-attention 先把其他位置的信息混进来的阶段。
- `feed-forward output` 是对已经混合的表示，再按位置加工一次后的结果。
- `after residual` 展示的是一种安全装置角色：它不会只信任新的计算，而会把原始表示也一起带着走。
- `after simple layer norm` 给出的是一种感觉：在送去下一个 block 之前，数值范围还会再被整理一次。

也就是说，Transformer block 不是`只有 attention`，而是一种把`上下文混合 + 按位置加工 + 保留原始信息 + 稳定化`作为一个整体反复使用的结构。只有这个感觉先固定住，到了下一节 P5-14.2 讨论并行处理与长上下文时，才会更自然地理解：为什么这种 block 容易被大规模重复。

Transformer 是 attention 从辅助装置被提升为核心 block 的代表性案例。这个 block 设计后来也被许多大规模语言模型和多模态模型反复复用，像是一种共同的基本单位。

## 检查清单

- 能否用 self-attention、feed-forward、residual connection、layer normalization 来解释 Transformer block？
- 能否说明 Transformer 不是一个单独想法，而是一种组件打包结构？
- 在理解 Transformer 时，能否把它区分成这样一个 block 组合：self-attention 收集上下文关系，feed-forward 加工表示，residual 与 normalization 稳定深层计算？
- 能否不把 Transformer 只说成`带 attention 的模型`，而是解释成`重复关系读取、按位置加工、稳定传递的 block 结构`？
- 能否把 self-attention 与 feed-forward 的角色差异，分别说成`读取与外部的关系`和`加工当前位置表示`？
- 能否解释 residual 与 normalization 会稳定深层学习？
- 当只讲 attention 仍不足以解释 Transformer 时，能否先想起 block 组成的视角？
- 在读下一节并行处理说明时，是否已经准备好先问`如果这个 block 被重复很多次，计算流为什么会改变`？

## 出处与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017，确认日期：2026-06-29。
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016，确认日期：2026-06-29。[https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Jay Alammar, `The Illustrated Transformer`，确认日期：2026-06-29。[https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/){: target="_blank" rel="noopener noreferrer" }
