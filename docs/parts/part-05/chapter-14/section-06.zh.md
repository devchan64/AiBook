# P5-14.6 补充学习：按位置加工表示

> Section ID: `P5-14.6`
> Version: `v2026.07.26`

_副标题: feed-forward network 如何在 attention 之后再次加工每个位置的表示？_

在 P5-14.2 中，我们看到 Transformer block 里的 feed-forward network 和 self-attention 负责不同工作。不过还会留下一个问题：`attention 已经混入上下文了，为什么还需要 feed-forward？`

在 Transformer block 中，feed-forward network 不是重新选择要参考哪个 token 的装置，而是重新加工每个已经通过 attention 混入上下文的位置表示的装置。

术语再次分散时，可以把概念词汇表里的[前馈网络（feed-forward network）](/AiBook/zh/reference/concept-glossary-pinyin/t/#transformer)和 P5-14.2 的四个部件角色分工一起重读。

## attention 之后为什么还要再加工一次？

self-attention 决定当前位置应该从其他位置带来什么信息。但`参考了什么`和`怎样把这个参考结果变成当前位置的下一个表示`不是同一个问题。

例如，在`压力未解除时保留重启`这类句子里，假设 `restart` 位置通过 attention 同时看到了 `pressure unreleased` 和 `hold`。这时 attention 会混入关系，但要把这个结果更清楚地加工成`简单处置`、`带条件的处置`、`应被阻断的处置`中的哪一类，还需要另外的变换。在 Transformer block 中，feed-forward network 就负责这个角色。

简短拆开如下。

| 问题 | 更直接负责的部件 | 原因 |
| --- | --- | --- |
| 当前位置应该参考哪个其他位置？ | self-attention | 因为它读取 token 之间的关系。 |
| 混入参考上下文后的当前表示要怎样改变？ | feed-forward network | 因为它在同一个位置内部重新做非线性加工。 |

## 把同一个 FFN 应用到多个位置是什么意思？

Transformer 的 feed-forward network 通常对每个位置应用相同权重。这里的`相同`不是说所有位置都会变成相同输出。如果输入表示因位置而不同，即使经过同一个变换，输出也会不同。

```mermaid
--8<-- "assets/part-05/chapter-14/feed-forward-position-update-zh.mmd"
```

这张图中，虚线表示相同权重在多个位置共享，实线表示每个位置表示会在自己的位置内部分别加工。因此 feed-forward network 既不是按顺序传递状态的装置，也不是选择新参考位置的装置。它是把已经混入上下文的各位置表示，用同一套规则再次变换的装置。

使用同一个 FFN，并不意味着把所有 token 变成同一种意义。应该读成`让不同输入表示通过同一套加工标准`。

## 为什么需要非线性加工？

如果把 feed-forward network 读成简单的数字后处理，Transformer block 的一半就消失了。attention 混入上下文之后，表示仍然是多个线索一起进入的状态。feed-forward network 会把这个混合表示进一步分离、压缩成当前位置的下一个表示。

| attention 之后表示中留下的状态 | feed-forward 帮助的事 |
| --- | --- |
| 多个线索已经混入，但当前位置意义仍然模糊 | 在当前位置内部把意义轴加工得更清楚 |
| 只靠简单线性组合时，条件、否定、例外等差异可能较弱 | 通过非线性变换更好地凸显线索组合差异 |
| 每个位置接收了不同混合上下文 | 应用同一个 FFN，但为每个位置产生不同输出表示 |

这里的`非线性`不是要求马上背公式。入门阶段，把它读成`把单纯相加或平均后的表示，变成下一个 block 能使用的、更有区分度的表示的过程`就足够了。下面例子里的 `relu` 也只需要按这个感觉来读。线性计算后，如果把小于 0 的轴折到 0，同样的输入变化就可能让输出方向不是单纯相加，而是出现转折。

## 案例与示例

### 案例：在工作许可句子中加工处置表示

在工作许可句子中，如果只看 `restart` 这个词，人会先想到`重新打开产线`这个动作。但如果句子里同时有 `pressure unreleased` 和 `hold`，当前位置表示就应该从简单动作名，转向`因为带有条件而必须被阻断的处置`。

self-attention 会让 `restart` 同时看到 `pressure unreleased` 和 `hold`。feed-forward network 会在当前位置内部再次加工这个混合表示，帮助 `restart` 表示更接近条件性阻断处置，而不是简单执行请求。

| 人容易先看到的表达 | attention 之后混入的上下文 | feed-forward 之后应更清楚的表示 |
| --- | --- | --- |
| `restart` 是执行动作 | `pressure unreleased`、`hold` 一起混入 | `带条件的阻断对象处置` |
| `approval` 是允许信号 | `verification incomplete`、`no exception` 一起混入 | `还不是最终批准` |
| `deployment` 是作业推进 | `rollback not confirmed`、`symptom continues` 一起混入 | `恢复确认前的风险作业` |

这个案例要确认的结果是：feed-forward network 不是寻找新的依据位置，而是把已经通过 attention 进入的依据，在当前位置表示内部加工成更有区分度的意义。

## 练习与例子

### 例子：确认同一个 FFN 后各位置输出是否不同

这个例子不是实际 Transformer 实现，而是确认 feed-forward network 的按位置加工感觉的小实验。假设 attention 之后已经有三个位置表示混入了上下文，并且相同 FFN 权重会同样应用到各位置。

| 要操作的值 | 要观察的输出 | 要确认的问题 |
| --- | --- | --- |
| `positions` 的每一行 | `hidden`, `output` | 即使经过同一个 FFN，各位置输出是否也不同？ |
| `restart` 位置的输入值 | `restart before/after` | 如果当前位置表示改变，同一个 FFN 是否也会朝不同方向加工？ |
| 只改变 `changed[1]` | `other positions unchanged` | 一个位置的 FFN 计算是否不会重新参考其他位置？ |

```python
# 这个例子确认即使同一个 feed-forward network 被共享应用到各位置表示，各位置的 hidden 和 output 也会如何被不同地加工。
import numpy as np

output_axes = ["action_axis", "block_axis"]

positions = np.array([
    [0.2, 0.1, 0.9, 0.1],  # pressure_state: condition signal high
    [0.8, 0.2, 0.2, 0.1],  # restart: action signal high
    [0.3, 0.9, 0.2, 0.7],  # hold: block/negation signal high
])

position_names = ["pressure_state", "restart", "hold"]

w1 = np.array([
    [1.0, -0.2, 0.8],
    [0.3, 1.2, -0.6],
    [0.8, 0.1, 0.5],
    [-0.4, 0.7, 1.0],
])
b1 = np.array([-0.2, -0.1, 0.0])
w2 = np.array([
    [0.9, 0.2],
    [-0.3, 1.0],
    [0.4, 0.8],
])

def relu(x):
    return np.maximum(x, 0.0)

def ffn(x):
    hidden = relu(x @ w1 + b1)
    output = hidden @ w2
    return hidden, output

hidden, output = ffn(positions)

print("[same FFN, different positions]")
print("output axes =", output_axes)
for name, before, h, after in zip(position_names, positions, hidden, output):
    print(f"{name:15s} input={np.round(before, 2)} hidden={np.round(h, 2)} output={np.round(after, 2)}")

changed = positions.copy()
changed[1] += np.array([0.0, 0.5, 0.0, 0.4])
_, changed_output = ffn(changed)

print("
[change only restart position]")
print("restart before/after =", np.round(output[1], 2), "->", np.round(changed_output[1], 2))
print("other positions unchanged =", np.allclose(output[[0, 2]], changed_output[[0, 2]]))
```

输出示例可以这样读。

```text
[same FFN, different positions]
output axes = ['action_axis', 'block_axis']
pressure_state  input=[0.2 0.1 0.9 0.1] hidden=[0.71 0.14 0.65] output=[0.86 0.8 ]
restart         input=[0.8 0.2 0.2 0.1] hidden=[0.78 0.07 0.72] output=[0.97 0.8 ]
hold            input=[0.3 0.9 0.2 0.7] hidden=[0.25 1.43 0.5 ] output=[-0.    1.88]

[change only restart position]
restart before/after = [0.97 0.8 ] -> [0.74 1.76]
other positions unchanged = True
```

第一个输出表明，即使应用同一个 FFN，只要各位置输入表示不同，hidden 和 output 也会不同。这里 `output` 的第一个值读作 `action_axis`，第二个值读作 `block_axis`。例如 `hold` 位置会留下更大的 `block_axis`；如果给 `restart` 位置混入更多保留线索，第二个输出中 `block_axis` 会从 `0.8` 增大到 `1.76`。第二个输出也表明，只改变 `restart` 位置的输入时，只会改变该位置的输出，其他位置输出保持不变。

解说：这个例子要读出的结果是，feed-forward network 不是选择新 token 的装置。参考其他位置已经在 attention 阶段发生，FFN 会让进入各位置的表示通过同一套加工标准。因此，即使共享同一个 FFN，各位置输出也可能不同。

### 练习：把当前位置表示改写成语言

假设下面场景中，attention 之后已经混入上下文。请用语言写出 feed-forward 之后当前位置表示应该朝什么方向加工。

| 当前位置 | attention 混入的线索 | feed-forward 之后的表示方向 | 解说 |
| --- | --- | --- | --- |
| `restart` | `pressure unreleased`, `hold` | 条件性阻断处置 | 不能只读作动作本身，而应读作因安全条件而被阻断的处置。 |
| `approval` | `verification incomplete`, `no exception` | 最终批准前的保留状态 | 不能只看 approval 这个词，要把未完成条件反映到当前表示中。 |
| `deployment` | `rollback not confirmed`, `symptom continues` | 恢复确认前的风险作业 | deployment 应被加工成仍然留下风险的作业，而不是单纯推进。 |

解说：好的答案不是华丽术语，而是清楚写出`当前位置表示应该朝哪个方向改变`。首先，写出只看当前位置这个词时会想到的基本意义。然后，补上 attention 之后哪些线索一起进入了当前位置。最后，再写出因为这些线索进入了，当前位置表示应该朝哪个方向变得更清楚。

例如，只看 `restart` 时，基本意义是`重新打开产线的执行动作`。但 attention 之后，`pressure unreleased` 和 `hold` 这两个线索一起进入了当前位置。这样一来，feed-forward 之后的表示方向就不是单纯执行动作，而是`因为安全条件而被阻断的处置`。因此答案可以写成：`restart 看起来像执行动作，但压力还没有解除，而且有 hold 线索一起存在，所以当前位置表示应该被加工成条件性阻断处置。`

这样写之后，阅读已经整合到 P5-14.2 的表示移动例子时，就不会把 `feed-forward output` 读成单纯中间数字。输出数字不是没有意义标签的计算残留，而应该读成当前位置表示朝某个意义方向被整理后的痕迹。

## 检查清单

- 能把 feed-forward network 解释成 attention 之后的按位置表示加工，而不是简单后处理吗？
- 能说明即使同一个 FFN 应用到多个位置，输入表示不同也会产生不同输出表示吗？
- 能区分 self-attention 的`关系读取`和 feed-forward network 的`位置内变换`吗？

## 来源与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 确认日期：2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
