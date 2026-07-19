# P5-5.2 计算图（computation graph）与自动微分（automatic differentiation）

> Section ID: `P5-5.2`
> Version: `v2026.07.19`

在 P5-5.1 里，我们已经说明：损失（loss）本身并不是更新，它必须先被重新拆成按参数分开的梯度（gradient）信号。理解到这里之后，接下来还会留下一个问题：

当层数变多、运算变复杂时，框架到底记录了哪些计算，才能自动把梯度算出来？

回答这个问题的视角，就是计算图（computation graph）与自动微分（automatic differentiation）。

计算图，是把模型里的运算展开成节点（node）与连接（edge）的表示方式。这样我们就能看见：顺向传播里值是在哪里生成的，而自动微分又会在反向阶段沿着哪条路径把梯度送回来。

如果之后需要把这种运算关系再拆小来读，更适合回到[英文概念词汇表里的 computation graph 条目](/AiBook/en/reference/concept-glossary/#computation-graph)。

## 本节范围

- 计算图到底在表示什么？
- 为什么深度学习里的运算需要按图来阅读？
- 顺向传播（forward pass）与反向传播（backward pass）在图上该怎样读？
- 它和自动微分之间是什么关系？

这一节不会去教图论本身，而是先解释：`为什么只有当深度学习的计算被像图一样记录下来时，自动微分才会真正变得可行。`

从 Part 5 的位置来看，到这一节为止，理解梯度计算所需要的正文责任其实已经闭合了。与其再单独补一节`反向传播数学补充`，不如在这里把`损失到梯度`、`链式法则`、`计算图`、`自动微分`这些感觉真正串起来，然后再进入优化器章节。所以，这一节不是要介绍新的模型结构，而是要读清：`已经见过的结构，到底怎样被记录下来，又怎样把梯度送回去。`

| 这一节正在阅读什么 | 为什么这里必须读它 |
| --- | --- |
| 计算结构的连接关系 | 因为它会显示中间值在哪里生成、又被传到哪里去 |
| 学习过程里的 backward 流 | 因为它让我们一步步看到：损失是怎样把责任分配给各个运算的 |
| 与后面优化器章节的衔接 | 因为梯度算完之后，参数如何真正改变，会在 P5-7 继续展开 |

## 本节目标

- 能把计算图解释成`把运算依赖关系展开保存的记录结构`。
- 能在图上读出：顺向传播负责算值，反向传播负责传梯度。
- 能理解：计算图会把复杂的微分拆成很多个小步骤。
- 能解释：自动微分是怎样利用计算图和局部微分规则，自动组织梯度计算的。
- 能通过一个可运行的 Python 例子确认：中间值保存与梯度计算的流程到底怎样连在一起。

## 计算图到底画出了什么

神经网络并不是那种把输入一下子变成答案的魔法盒子。它更像是一张由许多小运算串起来的网。

例如：

- 接收输入 \(x\)
- 乘上权重 \(w\)
- 加上偏置 \(b\)
- 通过激活函数
- 再计算损失

如果只把这整个流程写成一段文字，很快就会变复杂。计算图就是一种`把这些运算拆成小阶段，再把小阶段连接起来的图`。

也就是说，计算图会同时让下面两件事显露出来：

1. 值（value）到底在哪里生成；
2. 依赖关系（dependency）到底怎样接下去。

## 为什么必须按图来读

当式子越来越长时，反向传播常常会开始显得抽象。原因不是它真的神秘，而是因为我们把整个表达式看成了一个大块。

但一旦改成计算图：

- 大公式会被拆成很多小运算；
- 每个节点到底依赖谁，会直接看见；
- 梯度在 backward 时，其实也是沿着同一条路径反向走回来，这一点也会变明显。

也就是说，计算图并不是发明了新的微分方法，而是把原本已经存在的计算流程重新显形出来。

先这样理解就够：

`计算图把一条很大的公式拆成很多个小盒子，好让 forward 算值，backward 把影响再送回去。`

## 从最小的例子开始看

先看下面这个式子：

\[
z = wx + b
\]

\[
a = ReLU(z)
\]

\[
L = (a - t)^2
\]

如果只把它看成一行公式，好像并不算复杂。但在神经网络里，这种结构会重复成千上万次。因此，先学会把它按小运算节点拆开看，会更重要。

把它画得最简单，大致就是下面这样：

```mermaid
--8<-- "assets/part-05/chapter-05/computation-graph-flow-zh.mmd"
```

这张图会同时展示两件事：

- 在顺向传播里，值是从左往右被算出来的；
- 在反向传播里，梯度是从损失出发，由右往左传回去的。

## 在图上怎样读顺向传播

顺向传播（forward pass）就是在图上的每个节点里，真正算出具体数值的阶段。

例如：

1. `multiply` 节点接收 \(w\) 和 \(x\)，算出 \(wx\)
2. `add` 节点把 \(b\) 加进去，得到 \(z\)
3. `ReLU` 节点接收 \(z\)，得到 \(a\)
4. `loss` 节点拿 \(a\) 和目标 \(t\) 做比较，算出损失

也就是说，顺向传播就是沿着图一路走，把中间值（intermediate value）逐个填出来。

这些中间值之所以重要，是因为反向传播时还会再次用到它们。

## 在图上怎样读反向传播

反向传播（backward pass）则是从损失节点出发，一边往前回走，一边计算每个更早节点到底对损失贡献了多少梯度。

例如：

- 先看损失对 \(a\) 有多敏感；
- 再看 \(a\) 对 \(z\) 有多敏感；
- 再继续拆成 \(z\) 对 \(w\)、\(x\)、\(b\) 各自有多敏感。

因此，图其实是在一步步拆开下面这个问题：

`如果这个值稍微变一点，最终损失会变多少？`

把这个问题拆开以后，链式法则（chain rule）才真正变成了可以执行的计算过程。

## 计算图怎样让链式法则更容易读

在 P5-5.1 里，我们把链式法则解释成`把影响一层层串起来的规则`。计算图则会让这些层真的可见。

例如，如果损失 \(L\) 依赖于 \(a\)，\(a\) 又依赖于 \(z\)，\(z\) 再依赖于 \(w\)，那么与其一次性记住

\[
\frac{\partial L}{\partial w}
\]

不如按顺序读成：

- \(L\) 对 \(a\) 有多敏感；
- \(a\) 对 \(z\) 有多敏感；
- \(z\) 对 \(w\) 有多敏感。

把它记成一句话就够：

`计算图不会把微分当成一个巨大公式，而是把它拆成每个节点上的局部规则（local rule）。`

## 它和自动微分到底是什么关系

在现代深度学习框架里，我们很多时候不会自己手写全部反向传播公式。像 PyTorch、TensorFlow、JAX 这样的工具，会利用计算图自动算出梯度。

这里最重要的一点是：

`自动微分并不是像魔法一样凭空生成梯度，而是沿着计算图，把局部微分规则有组织地套起来。`

所以，想理解自动微分时，先理解计算图反而更自然。

这一层先记住就足够：

- forward：把值算出来并记住；
- backward：沿着记住的路径，把梯度算回来；
- 自动微分：框架替我们组织好这两件事。

```mermaid
--8<-- "assets/part-05/chapter-05/forward-loss-backward-flow-zh.mmd"
```

## 案例与示例

### 案例 1. 只看最终阻断分数时，计算路径会消失

先想象一个很小的计算：它读取压力未恢复程度，然后生成一个`再启动阻断分数`。人在看这个场景时，通常会先盯着最后那个阻断分数，然后直接判断：`分数高`、`分数低`、`和目标不一样`。但从计算图的角度，更重要的是把这个分数究竟经过了哪些中间计算重新展开。

例如，可以设想输入信号 `pressure_signal` 先乘上风险权重 `risk_weight`，生成 `weighted_pressure`；然后再加上基线偏置 `base_block_bias`，得到 `block_logit`；再经过 ReLU，得到 `block_activation`。最后损失（loss）则是比较这个输出与目标阻断分数 `target_block_score` 之间的差距。如果只用一行公式去读它，容易只剩下一句“最后算出了损失”。但一旦展开成计算图，每个节点都会分开出现。

初学者最容易漏掉的，就是把`最后那个分数`和`产生那个分数的整条路径`看成同一件事。比如当阻断分数是 0.8 时，人很容易立刻把它读成“风险被判断得较高”。但计算图会再多问一步：这个 0.8 到底是因为 `pressure_signal` 本身很大，还是 `risk_weight` 把它放大了，还是 `base_block_bias` 先把基线抬高了，还是因为 ReLU 前的 `block_logit` 本来就是正的，所以被直接放了过去？这些都必须先拆开。

换句话说，最终阻断分数是`结果`，但在计算图上更重要的是它经过的`路径`。在 `pressure_signal -> weighted_pressure` 里，输入和权重第一次相遇；在 `weighted_pressure -> block_logit` 里，偏置把基线又挪了一次；在 `block_logit -> block_activation` 里，ReLU 决定这个值到底是被放过去，还是被截住。一旦把这些阶段分开看，就会发现：同样一个 `block score 0.8`，可能来自完全不同的原因。有时是因为输入本身大，有时则是因为输入不算大，但权重与偏置把它推高了。

之所以必须做这个区分，是因为后面在读梯度时，我们必须一层层追问：`到底是谁承担了多少责任？` 如果只盯着最终分数，就只会剩下“分数很大”这个结果，而让它变大的那条计算路径会直接消失。相反，如果把它展开成计算图，就能分别读出：`哪个中间值成了后续计算的材料`、`哪个节点改变了值的符号与大小`、`哪个参数真的影响了最后的输出。`

```mermaid
--8<-- "assets/part-05/chapter-05/computation-graph-case1-path-vs-score-zh.mmd"
```

因此，这个案例里真正要确认的结果，并不是最后阻断分数本身，而是 `weighted_pressure -> block_logit -> block_activation -> loss` 这条路径里的中间产物是否真的被拆开显现出来。只有先做出这个区分，后面才看得见梯度究竟能沿着哪条路传回来。

| 人最容易先看的标准 | 用计算图重新阅读后的标准 |
| --- | --- |
| 觉得只看最终阻断分数就够了 | 必须先拆开：这个分数到底由哪些中间值生成 |
| 觉得损失大，前面权重也一定会改很多 | 损失大小与梯度能不能沿着路径传回去，要分开确认 |
| 觉得只盯着 ReLU 之后的输出就够了 | ReLU 之前的 `block_logit` 符号，本身就会改变 backward 路径 |

### 案例 2. 损失很大，但梯度并不一定能回到前面

即使在同一个计算网络里，只要 `block_logit` 是正还是负不同，反向传播的解释就会跟着改变。如果 `block_logit > 0`，ReLU 会把这个值放行，因此从损失出发的梯度可以继续沿着 `block_activation -> block_logit -> risk_weight, base_block_bias` 传回去。反过来，如果 `block_logit <= 0`，那么在 forward 里输出会被截成 0，而在 backward 里，梯度也不会再被送回到 ReLU 前面的部分。

这里最容易让初学者混淆的一点，是把`损失很大`和`前面参数应该被大幅修改`自动连成一件事。例如，假设目标阻断分数是 1.0，但实际 `block_activation` 变成了 0，因此损失很大。人很自然会想：`既然错得这么厉害，前面的 risk_weight 不也该大幅修吗？` 但计算图并不是只看损失大小，它还会继续问：从损失出发的梯度，沿着这条路径到底能不能真的走回到前面的节点？

把 ReLU 门被关上的情况一步步拆开，会更容易看清。首先，在 forward 里，如果 `block_logit` 被算成 0 或更小，那么经过 ReLU 之后的 `block_activation` 就会变成 0。这时，输出依然可能和目标差很远，所以损失仍然会很大。但一旦进入 backward，ReLU 对那些`输入小于等于 0 的路径`会返回 0 的梯度。这样一来，从损失出发的信号虽然还存在于 `block_activation`，却不会继续穿过 `block_logit` 走到 `risk_weight` 和 `base_block_bias`。也就是说，会出现这样一种情形：`结果错得很厉害`，但这条路径上的前面参数并不会因为这次错误而收到更新信号。

如果用更贴近初学者的话来说，就是：`输出偏得很大`这件事，与`这条路径可以被往前修正`这件事，是两码事。损失负责展示结果的偏差，而梯度负责展示：这个偏差在计算图里到底有没有一条真实存在的回传路径。如果 ReLU 门关着，即便损失很大，那条路也可能断掉。因此，读计算图时，除了问`它错得有多厉害`之外，还必须继续问`这个错误的责任到底能回传到哪里。`

```mermaid
--8<-- "assets/part-05/chapter-05/computation-graph-case2-loss-vs-gradient-zh.mmd"
```

因此，这个案例里最重要的学习点不是`大损失 = 大更新`，而是`大损失 + backward 路径仍然活着`，前面的参数才会真的因此被更新。即使损失数字一样大，只要 ReLU 前值的符号不同，backward 的解读就会完全改变。`block_logit > 0` 时，责任会传回 `risk_weight` 与 `base_block_bias`；而 `block_logit <= 0` 时，梯度可能就在这里停住。能让这种差别被肉眼看见的工具，正是计算图。

在这个场景里，人最容易只盯着损失数字，然后觉得：`损失更大的那边，应该被修得更猛。` 但计算图不会这样读。即使损失大，只要路径断了，前面的参数也不会沿这条路被更新。所以，计算图视角会强迫我们把`错得多严重`和`责任到底能回传到哪里`拆开来看。

因此，这个案例里必须确认两件事。第一，forward 阶段里，值到底是在哪些节点生成的。第二，backward 阶段里，从损失出发的梯度到底有没有活着传到 ReLU 前面的节点与参数。只有把这两个问题分开，计算图才不只是“计算顺序示意图”，而是真正变成阅读反向传播的工具。

把这两个案例放在一起之后，就更容易看清为什么必须需要计算图。

| 场景 | 人最容易先看到的结果 | 计算图会更清楚留下什么解释 | 接下来要立刻确认什么 |
| --- | --- | --- | --- |
| 计算再启动阻断分数 | 容易觉得只看最终输出分数和损失就够了 | 要读 backward，必须先分开：每个中间值到底是在什么节点生成的 | 分别看 `weighted_pressure`、`block_logit`、`block_activation`、`loss` |
| ReLU 门关闭的路径 | 容易觉得损失大，前面的权重也会大改 | 即使损失大，梯度仍然可能在 ReLU 前面就变成 0 | 去看 `d_loss_d_logit`、`d_loss_d_weight`、`d_loss_d_bias` 是否真的还活着 |

```mermaid
--8<-- "assets/part-05/chapter-05/backprop-direction-and-responsibility-flow-zh.mmd"
```

## 练习与示例

这次示例的目标，并不是借助自动微分库，而是直接在一个极小的式子里确认：`forward 里到底生成了哪些中间值`，以及`backward 里到底算出了哪些梯度`。这个例子的角色，不是写出一段“能把模型训好”的代码，而是帮助读者建立：怎样像手工追踪一样，一步步读计算图里的节点。

所以，这里的代码只承担三件事：

- 沿着同一张计算图，把 forward 的值和 backward 的梯度并排展示出来；
- 让读者不会再把`损失很大`与`梯度路径还活着`读成同一句话；
- 用一个很小的网络，把自动微分框架内部真正做的事压缩出来。

输入：

- 压力未恢复程度 `pressure_signal`
- 压力风险权重 `risk_weight`
- 基线偏置 `base_block_bias`
- 目标阻断分数 `target_block_score`

输出：

- forward 中间值 `weighted_pressure`、`block_logit`、`block_activation`、`loss`
- backward 梯度 `d_loss_d_activation`、`d_loss_d_logit`、`d_loss_d_weighted_pressure`、`d_loss_d_weight`、`d_loss_d_bias`
- 哪个中间值在后面的梯度计算里再次被利用的连接
- ReLU 门打开与关闭时 backward 路径的差异

问题场景：

- 因为反向传播是从最终损失出发、沿着中间值一路倒回去，所以把 forward 值和 backward 值并排看会更容易理解；
- 即使公式一样，只要 ReLU 前值 `block_logit` 的符号不同，梯度路径就可能断掉，因此必须比较。

要确认的概念：

- 反向传播里的梯度，必须重新利用顺向传播中的中间值来计算；
- 把各阶段的中间值和梯度一起打印出来，会更容易追踪计算连接；
- 像 ReLU 这样的节点，是否让 backward 继续传回去，会取决于 forward 阶段保留下来的符号信息。

这里尤其要确认的是：这个示例的“答案”，并不是单独某一个损失数字。真正的答案是：能不能按节点（node-by-node）读出来，`每个节点生成了什么值`，以及`梯度到底是在哪里活着、又是在哪里被截断的。`

输入（input）：

使用上面整理过的两个案例：`pressure_signal`、`risk_weight`、`base_block_bias`、`target_block_score`。

在看代码之前，先猜一猜哪一种情况会让梯度传得更远，会更好。

| 案例 | 可以先猜的比较结果 | 这样猜的原因 |
| --- | --- | --- |
| `block_gate_open` | `d_loss_d_logit`、`d_loss_d_weight`、`d_loss_d_bias` 都可能还活着 | 因为 `block_logit > 0` 时，ReLU 会把输入放过去，backward 也能继续走。 |
| `block_gate_closed` | `d_loss_d_logit`、`d_loss_d_weight`、`d_loss_d_bias` 很可能变成 0 | 因为 `block_logit <= 0` 时，ReLU 会把输出截成 0，backward 也可能在这里断掉。 |

这种比较之所以在计算图里特别重要，是因为 forward 里看到的`门是开着还是关着`，会直接改变 backward 的路径。

```mermaid
--8<-- "assets/part-05/chapter-05/computation-graph-relu-gate-comparison-zh.mmd"
```

这张图的作用，是在真正看输出数字之前，先把`损失更大吗？`和`梯度真的会回到前面吗？`分开来读。`block_gate_closed` 的损失更大，但在计算图里路径会在 ReLU 前被截断，因此梯度不会再传到 `risk_weight` 与 `base_block_bias`。

```python
def relu(value):
    return max(0.0, value)

cases = [
    {"name": "block_gate_open", "pressure_signal": 2.0, "risk_weight": 1.5, "base_block_bias": -0.5, "target_block_score": 4.0},
    {"name": "block_gate_closed", "pressure_signal": 2.0, "risk_weight": 0.1, "base_block_bias": -0.5, "target_block_score": 4.0},
]

for case in cases:
    pressure_signal = case["pressure_signal"]
    risk_weight = case["risk_weight"]
    base_block_bias = case["base_block_bias"]
    target_block_score = case["target_block_score"]

    # forward
    weighted_pressure = risk_weight * pressure_signal
    block_logit = weighted_pressure + base_block_bias
    block_activation = relu(block_logit)
    loss = (block_activation - target_block_score) ** 2

    # backward
    d_loss_d_activation = 2 * (block_activation - target_block_score)
    d_activation_d_logit = 1.0 if block_logit > 0 else 0.0
    d_loss_d_logit = d_loss_d_activation * d_activation_d_logit
    d_logit_d_weighted_pressure = 1.0
    d_loss_d_weighted_pressure = d_loss_d_logit * d_logit_d_weighted_pressure
    d_logit_d_weight = pressure_signal
    d_logit_d_bias = 1.0
    d_loss_d_weight = d_loss_d_logit * d_logit_d_weight
    d_loss_d_bias = d_loss_d_logit * d_logit_d_bias

    node_trace = [
        {
            "node": "weighted_pressure = risk_weight * pressure_signal",
            "forward_value": round(weighted_pressure, 3),
            "backward_signal": round(d_loss_d_weighted_pressure, 3),
            "read_as": "回到 weighted_pressure 输出处的梯度",
        },
        {
            "node": "block_logit = weighted_pressure + base_block_bias",
            "forward_value": round(block_logit, 3),
            "backward_signal": round(d_loss_d_logit, 3),
            "read_as": "在 ReLU 前面仍然活着或已经断掉的梯度",
        },
        {
            "node": "block_activation = ReLU(block_logit)",
            "forward_value": round(block_activation, 3),
            "backward_signal": round(d_loss_d_activation, 3),
            "read_as": "loss 直接对着看的输出节点",
        },
        {
            "node": "loss = (block_activation - target_block_score) ** 2",
            "forward_value": round(loss, 3),
            "backward_signal": "start",
            "read_as": "backward 出发的损失节点",
        },
    ]

    print(f"[{case['name']}]")
    print("forward:", {
        "weighted_pressure": round(weighted_pressure, 3),
        "block_logit": round(block_logit, 3),
        "block_activation": round(block_activation, 3),
        "loss": round(loss, 3),
    })
    print("backward:", {
        "d_loss_d_activation": round(d_loss_d_activation, 3),
        "d_loss_d_logit": round(d_loss_d_logit, 3),
        "d_loss_d_weighted_pressure": round(d_loss_d_weighted_pressure, 3),
        "d_loss_d_weight": round(d_loss_d_weight, 3),
        "d_loss_d_bias": round(d_loss_d_bias, 3),
    })
    print("node_trace:")
    for row in node_trace:
        print(" ", row)
    print("---")
```

读这组输出时，不要只看`损失数字`，而是必须按 `forward 摘要 -> backward 摘要 -> node_trace` 这个顺序去看。前两行只是值的总结，真正关键的是 `node_trace`，因为只有在那一段里，读者才能沿着计算图的节点重新读出：`值是在哪里生成的`，以及`梯度是在哪里活着、在哪里被截断的。`

```text
[block_gate_open]
forward: {'weighted_pressure': 3.0, 'block_logit': 2.5, 'block_activation': 2.5, 'loss': 2.25}
backward: {'d_loss_d_activation': -3.0, 'd_loss_d_logit': -3.0, 'd_loss_d_weighted_pressure': -3.0, 'd_loss_d_weight': -6.0, 'd_loss_d_bias': -3.0}
node_trace:
  {'node': 'weighted_pressure = risk_weight * pressure_signal', 'forward_value': 3.0, 'backward_signal': -3.0, 'read_as': '回到 weighted_pressure 输出处的梯度'}
  {'node': 'block_logit = weighted_pressure + base_block_bias', 'forward_value': 2.5, 'backward_signal': -3.0, 'read_as': '在 ReLU 前面仍然活着或已经断掉的梯度'}
  {'node': 'block_activation = ReLU(block_logit)', 'forward_value': 2.5, 'backward_signal': -3.0, 'read_as': 'loss 直接对着看的输出节点'}
  {'node': 'loss = (block_activation - target_block_score) ** 2', 'forward_value': 2.25, 'backward_signal': 'start', 'read_as': 'backward 出发的损失节点'}
---
[block_gate_closed]
forward: {'weighted_pressure': 0.2, 'block_logit': -0.3, 'block_activation': 0.0, 'loss': 16.0}
backward: {'d_loss_d_activation': -8.0, 'd_loss_d_logit': -0.0, 'd_loss_d_weighted_pressure': -0.0, 'd_loss_d_weight': -0.0, 'd_loss_d_bias': -0.0}
node_trace:
  {'node': 'weighted_pressure = risk_weight * pressure_signal', 'forward_value': 0.2, 'backward_signal': -0.0, 'read_as': '回到 weighted_pressure 输出处的梯度'}
  {'node': 'block_logit = weighted_pressure + base_block_bias', 'forward_value': -0.3, 'backward_signal': -0.0, 'read_as': '在 ReLU 前面仍然活着或已经断掉的梯度'}
  {'node': 'block_activation = ReLU(block_logit)', 'forward_value': 0.0, 'backward_signal': -8.0, 'read_as': 'loss 直接对着看的输出节点'}
  {'node': 'loss = (block_activation - target_block_score) ** 2', 'forward_value': 16.0, 'backward_signal': 'start', 'read_as': 'backward 出发的损失节点'}
---
```

如果把这组输出像表一样读当然也可以，但如果进一步拆成图，就会更容易把`forward 值的大小`和`backward 梯度是否活着`区分开。

![计算图中各 forward 节点的值对比](/AiBook/assets/part-05/chapter-05/computation-graph-forward-trace-zh.png)

在 forward 图里，最先会看到的是：`block_gate_closed` 的损失要大得多。但如果只看这张图，很容易误读成“损失越大，前面的参数更新就一定越大”。所以必须再把同一个例子的 backward 图分开看一次。

![计算图中各 backward 节点的梯度对比](/AiBook/assets/part-05/chapter-05/computation-graph-backward-trace-zh.png)

在 backward 图里，差别会反过来显露出来。`block_gate_open` 时，`dL/d_logit`、`dL/d_weight`、`dL/d_bias` 都还活着；而 `block_gate_closed` 时，虽然 `dL/d_activation` 很大，但 ReLU 前面的梯度已经被截成 0。也就是说，读计算图时，必须把损失柱状图和梯度柱状图分开来解读。

这个例子里真正重要的是下面几点：

- 在 forward 里，中间值会一步步生成；
- 在 backward 里，从最终损失出发的变化量会被一步步拆回前面的参数；
- 每个节点只要知道自己前后依赖的关系，就能参与梯度计算；
- 顺着 `node_trace` 去读，就会更清楚：这个例子不是“又一个损失计算例子”，而是“逐节点阅读计算图的例子”。

也就是说，这段 Python 代码的作用，并不是让人多背一套反向传播公式，而是把计算图这一节里讲到的`节点`、`中间值`、`局部规则`、`路径被截断`重新收在一组输出里。

这里必须把两个案例并排来读，计算图的感觉才会更清楚。

| 案例 | 现在要抓住的核心 |
| --- | --- |
| `block_gate_open` | 因为 `block_logit > 0`，ReLU 门是开着的，所以梯度会继续沿着 `block_activation -> block_logit -> risk_weight, base_block_bias` 传回去。 |
| `block_gate_closed` | 虽然损失更大，但因为 `block_logit <= 0`，ReLU 会把路径截断，因此 `d_loss_d_logit`、`d_loss_d_weight`、`d_loss_d_bias` 都变成 0。 |

也就是说，计算图并不只是在告诉我们`损失是不是很大`，而是在进一步让我们看清：`梯度到底在哪些节点上仍然活着，又是在哪里被截断的。`

在读输出数字时，也必须把`损失大小`和`梯度路径`分开来看。

| 案例 | 输出里最先看到的东西 | 只看损失时容易留下的解释 | 连计算图一起看时会变成什么 |
| --- | --- | --- | --- |
| `block_gate_open` | 损失是 2.25，而且 `d_loss_d_weight`、`d_loss_d_bias` 都不是 0 | 容易只觉得“损失还在，所以继续减就行” | 更准确的读法是：ReLU 门开着，梯度确实能回到前面的参数，因此存在真实可更新的路径 |
| `block_gate_closed` | 损失是 16.0，更大，但 `d_loss_d_logit`、`d_loss_d_weight`、`d_loss_d_bias` 都是 0 | 容易觉得“损失更大，所以应该更新得更猛” | 更准确的读法是：虽然损失更大，但 ReLU 前面路径已经断掉，这条路上的前面参数这次并不会被更新 |

也就是说，计算图真正做的事，是把“大问题”拆成很多“小的局部计算”。

计算图视角并不只是教学用图，而是理解现代深度学习框架里的自动微分和训练系统时，一个非常实用的入口。

随着深度学习越来越普及，网络结构也变得越来越复杂。此时，如果还坚持靠人手把整个微分全部展开，已经很不现实。把运算按图来读，再利用局部微分规则去组合，就会成为更实用的解释方式。

从课程结构来看，这一节真正要确认的结果是：能不能把上一节 P5-5.1 里的反向传播直觉，不再只当成公式记忆，而是进一步读成“运算块连接 + 局部微分规则组合”的过程。

- 如果只有反向传播直觉，计算流程仍然可能很模糊；
- 在进入优化器之前，必须更清楚梯度到底是从哪里来的；
- 而之后的 CNN、RNN、Attention 等结构，其实也更自然地适合按“运算块怎样连接”来阅读。

也就是说，计算图可以看成是 Part 5 整体的一个共通阅读工具。

## 什么时候要把问题抬到计算图来读

真正需要拿出计算图这一节的时机，是当反向传播的直觉已经有了，但随着运算步骤变多，`值到底在哪里生成、梯度到底沿哪条路传回去`开始模糊的时候。

| 先出现的问题场景 | 为什么这时计算图视角更有用 | 紧接着会连到哪里 |
| --- | --- | --- |
| 公式变长后像一个整体大块 | 可以把大计算拆成小运算块和依赖关系 | 接着去看优化器怎样使用这些梯度 |
| 不明白中间值为什么要保存 | 可以看出 forward 的值会在 backward 时再次被利用 | 接着会连到训练 / 推理区分与优化器章节 |
| 自动微分看起来像魔法 | 可以看出：它其实是在图上组织局部微分规则 | 接着会连到框架使用感与优化器章节 |
| 想把 CNN、RNN、Attention 也放进同一套阅读框架里 | 可以提供一个“按运算块连接来读”的共通工具 | 后面的结构章节都能复用这一套视角 |

## 检查清单

- 能说明：计算图（computation graph）到底怎样把顺向传播与反向传播展开出来吗？
- 能把一个大公式拆成许多小运算块来读吗？
- 能说明：计算图本质上是在展开运算依赖关系吗？
- 能说明：顺向传播是在图上算值，而反向传播是在图上把从损失出发的梯度送回去吗？
- 能解释为什么 forward 阶段保存的中间值，在 backward 里还会再次需要吗？
- 能在读计算图时，不再直接面对一个巨大微分式，而是按每个局部运算块的规则去跟梯度路径吗？
- 当自动微分看起来像魔法时，能重新拿出“它是在图上组织局部微分规则”的视角吗？
- 能理解这一节之后为什么会继续连到优化器，以及训练 / 推理区分吗？

## 出处与参考资料

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Christopher M. Bishop, `Pattern Recognition and Machine Learning`, Springer, 2006, 确认日期: 2026-07-19. [https://link.springer.com/book/9780387310732](https://link.springer.com/book/9780387310732){: target="_blank" rel="noopener noreferrer" }
- Andrej Karpathy, `micrograd`, GitHub, 确认日期：2026-06-29. [https://github.com/karpathy/micrograd](https://github.com/karpathy/micrograd){: target="_blank" rel="noopener noreferrer" }
