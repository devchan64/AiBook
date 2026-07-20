# P5-14.4 RNN 的状态传递与 Transformer 的关系计算在并行处理中怎样分开

> Section ID: `P5-14.4`
> Version: `v2026.07.20`

P5-14.1 到 P5-14.3 看的是 Transformer block 内部的角色。现在要比较同样的表示计算在一个序列内部按什么顺序执行。

为什么 RNN 会让人感觉像顺序状态传递，而 Transformer 更适合 token 关系计算和 GPU 并行处理？

比较基准不是 `Transformer 更新` 这种时间顺序印象。核心是两种计算的差异：一种把前一个 step 的状态逐步传给后面，另一种更容易把一层中的多个 token 关系组织成大矩阵运算。

## 计算流与并行处理要处理的问题

- RNN 为什么会被读成把前面 step 的状态传给后面的结构？
- Transformer 为什么会被读成更能一次性计算 token 关系的结构？
- 这种差异为什么会连接到 GPU 并行处理和大规模训练？

## RNN 会按顺序传递状态

RNN 系列让每个 step 接收前一个状态，并生成下一个状态。因此计算感觉自然会像下面这样。

- 先看第一个 token，生成状态。
- 带着这个状态看第二个 token。
- 再把这个状态传给第三个 token。

`RNN 是一边把前面生成的状态传给后面，一边顺序计算的结构。`

这种结构很适合处理顺序重要的数据，但从并行处理角度看会成为负担。如果后面的 step 必须等待前面 step 的结果，即使计算设备很多，也很难随意同时处理一个序列内部的各个 step。

## Transformer 更接近一起计算关系

Transformer 的 self-attention 让每个 token 参考同一序列里的其他 token。所以它的计算感觉，比起把状态沿着一条线传下去，更接近把 token 之间的关系作为大矩阵计算一起处理。

`RNN 按顺序传递状态，而 Transformer 更像一起计算 token 之间的关系。`

| 视角 | RNN 系列 | Transformer |
| --- | --- | --- |
| 计算流 | 前一个 step 的结果是下一个 step 所需的 | 更能一起计算 token 关系 |
| 信息移动感觉 | 状态被依次传递 | 重新比较需要的位置 |
| 并行处理 | 顺序依赖容易成为瓶颈 | 容易打包成大矩阵运算 |
| 规模扩展 | 长序列越多，顺序负担越大 | 更容易通过 batch 和 tensor 计算组织起来 |

GPU 擅长同时处理大量相似计算。Part 5 前面看到的 batch 和 tensor 计算也是同一种感觉。Transformer 的 self-attention 和 feed-forward 容易打包成大矩阵运算，所以和这种计算资源很匹配。

并行处理说明中重要的观察值不是 `速度变快了`，而是哪些计算必须等待、哪些计算可以一起打包。

| 要观察的问题 | RNN 式流程中的负担 | Transformer 式流程中的优势 |
| --- | --- | --- |
| 下一个 token 计算是否必须等待前一个 step 完成 | 顺序依赖容易成为瓶颈 | 一层中的多个 token 关系更容易一起计算 |
| 是否重复大量同类乘法 | 容易被 step 单位的重复切开 | 容易打包成大矩阵运算放到 GPU 上 |
| 是否能一次训练很多句子 | 句子内部的顺序依赖会累积 | 更容易用大 batch 和 tensor 计算组织 |

`Transformer 很适合大规模 GPU 训练，因为 token 之间的关系容易改写成并行矩阵运算。`

## 案例与示例

### 案例：工作许可句子与大规模学习 batch

把工作许可句子按行分开看。

| 行 | 文档内容 | 与最后判断的关系 |
| --- | --- | --- |
| 1 | `压力解除前，不得重启 3 号线。` | 禁止规则 |
| 2 | `传感器校准已在上午完成。` | 中间运营日志 |
| 3 | `包装材料补充作业已另行批准。` | 中间运营日志 |
| 4 | `当前压力尚未回到安全范围。` | 当前状态 |
| 5 | `交接班记录已更新。` | 中间运营日志 |
| 6 | `现在可以批准 3 号线重启吗？` | 最后问题 |

人最容易先用的标准是 `文档按顺序写，所以从前往后读就行`。但从计算流角度看，问题要更具体。把第 1 行禁止规则、第 4 行当前状态与第 6 行问题比较时，计算是等待前面 step 的结果，还是能在同一层把多个关系计算打包？

在 RNN 式状态传递感觉中，前面的线索会被压缩到状态里并逐行传下去。要处理第 6 行问题，第 1 行生成的状态必须经过第 2、3、4、5 行计算后才到达。因此即使在同一个句子内部，后面的 step 也要等待前面 step 计算结束。

在 Transformer 式关系计算感觉中，第 6 行问题位置与第 1 行规则、第 4 行状态之间的关系，可以在同一层的 attention 计算中组织起来。P5-14.4 这里的核心不是 `远处线索记得多好`，而是位置对之间的比较更容易被组织成大矩阵运算。远处线索如何在最后判断中被重新调用，会交给 P5-14.5 的长上下文问题。

| 比较场景 | 按 RNN 式状态传递读 | 按 Transformer 式关系计算读 |
| --- | --- | --- |
| 比较第 6 行问题与第 1 行禁止规则 | 线索要经过第 2~5 个 step 传到第 6 行状态 | 第 6 个位置与第 1 个位置的关系分数可以一起计算 |
| 比较第 6 行问题与第 4 行当前压力状态 | 线索要经过第 5 个 step 传到第 6 行状态 | 第 6 个位置与第 4 个位置的关系分数可以一起计算 |
| 比较 batch 中多个句子的各位置关系 | 每个句子内部的 step 依赖会重复出现 | 各句子的关系 score 更容易组织成 tensor |

这个案例要确认的结果不是 `Transformer 因为更新所以更好`。面对同一个最后问题，RNN 式说明会问 `前面 step 的状态是否必须先结束，后面 step 才能开始`，Transformer 式说明会问 `多个位置关系是否能打包成同一层的矩阵计算`。并行处理说明的核心不是模型名字，而是 `哪些计算要等待，哪些计算能打包`。

## 练习与示例

### 示例：比较顺序 trace 与关系 score 矩阵

这个例子不是实际 Transformer 实现，而是用一个小输出确认 P5-14.4 的中心问题。这里不比较执行时间，而是看 `顺序 trace 会按 step 顺序积累`，而 `关系 score 会以矩阵 shape 一次性组织起来`。

| 要操作的值 | 要观察的输出 | 要确认的问题 |
| --- | --- | --- |
| `line_features` 的行顺序 | `recurrent trace` | 前一个 step 状态是否按顺序传给后面的 step |
| `relation_kernel` | `request row`, `top related lines` | 当前问题与哪些前面行有较大的关系 score |
| 放进 `batch` 的句子数 | `score tensor shape` | 多个句子的关系 score 是否被打包成一个 tensor 计算 |

```python
# 这个例子比较 RNN 式 sequential trace 和 Transformer 式 relation-score matrix，观察 step 累积和并行关系计算的差异。
import numpy as np

line_features = np.array([
    [0.0, 1.0, 1.0, 0.0, 0.0],  # rule: pressure + block
    [0.0, 0.0, 0.0, 1.0, 0.0],  # log
    [0.0, 0.0, 0.0, 1.0, 0.0],  # log
    [0.0, 1.0, 0.0, 0.0, 0.0],  # state: pressure
    [0.0, 0.0, 0.0, 1.0, 0.0],  # log
    [1.0, 0.0, 0.0, 0.0, 1.0],  # request: restart + question
])

line_names = [
    "rule",
    "sensor_log",
    "packing_log",
    "pressure_state",
    "shift_log",
    "request",
]

relation_kernel = np.array([
    [1.0, 1.0, 1.0, 0.0, 1.0],
    [0.0, 1.0, 0.3, 0.0, 0.0],
    [0.0, 0.5, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.2, 0.0],
    [1.0, 0.5, 0.5, 0.0, 1.0],
])

state = np.zeros(5)
recurrent_trace = []
for step, (name, features) in enumerate(zip(line_names, line_features), start=1):
    state = 0.55 * state + features
    recurrent_trace.append((step, name, np.round(state, 3)))

relation_scores = line_features @ relation_kernel @ line_features.T
request_scores = relation_scores[-1]
ranked = sorted(zip(request_scores, line_names), reverse=True)

batch = np.stack([
    line_features,
    line_features[[0, 2, 4, 3, 1, 5]],
    line_features[[1, 2, 0, 3, 4, 5]],
])
batch_scores = batch @ relation_kernel @ np.transpose(batch, (0, 2, 1))

print("[recurrent trace]")
for step, name, snapshot in recurrent_trace:
    print(f"step {step}: {name:14s} state={snapshot}")

print("\n[relation score matrix]")
print("shape =", relation_scores.shape)
print("request row =", np.round(request_scores, 1).tolist())
print("top related lines =", [(name, float(score)) for score, name in ranked[:3]])

print("\n[batched relation scores]")
print("batch shape =", batch.shape)
print("score tensor shape =", batch_scores.shape)
```

输出示例可以这样读。

```text
[recurrent trace]
step 1: rule           state=[0. 1. 1. 0. 0.]
step 2: sensor_log     state=[0.   0.55 0.55 1.   0.  ]
...
step 6: request        state=[1.    0.353 0.05  0.808 1.   ]

[relation score matrix]
shape = (6, 6)
request row = [3.0, 0.0, 0.0, 1.5, 0.0, 4.0]
top related lines = [('request', 4.0), ('rule', 3.0), ('pressure_state', 1.5)]

[batched relation scores]
batch shape = (3, 6, 5)
score tensor shape = (3, 6, 6)
```

第一个输出展示的是 RNN 式状态感觉。第 6 行 request 状态必须经过第 1 到第 5 行的更新之后才生成。第二个输出展示的是关系计算感觉。6 个位置之间的关系 score 被放成 `(6, 6)` 矩阵，request 行中 rule 和 pressure_state 的分数较大。第三个输出 `(3, 6, 6)` 表示如果把 3 个句子作为 batch，每个句子的位置关系矩阵也能以 tensor 形式一起组织。

解说：这个例子要读的结果不是 `哪一边实际快几倍`。P5-14.4 的核心是：顺序状态传递会被读成 step trace，而 Transformer 式关系计算会被读成位置关系矩阵和 batch tensor。因此，并行处理说明应该以计算结构差异来收束，而不是变成硬件炫耀。

### 练习：标出等待的计算和打包的计算

看下面场景，先标出 `等待` 或 `打包`。

| 场景 | 标记 | 解说 |
| --- | --- | --- |
| 句子中第 3 个 token 的计算必须接收第 2 个 token 的 hidden state | 等待 | 前面 step 的结果是后面 step 所需的，所以会出现顺序依赖。 |
| 在同一层计算一个句子中所有 token 对的 attention score | 打包 | 多个 token 关系分数容易组织成矩阵运算。 |
| batch 中多个句子的 feed-forward 计算对各位置使用相同权重 | 打包 | 同类位置计算适合一起作为 tensor 运算处理。 |
| 生成过程中，必须提前知道还没有出现的下一个 token 才能计算 | 等待 | 生成执行阶段仍有顺序约束。要和训练时的并行化感觉区分开。 |
| 把文档前面的规则压缩进一个状态，并一路带到最后 | 更接近等待 | 前面线索要经过多个 step，因此顺序传递负担会变大。 |

解说：这个练习不是实现实际 GPU kernel。P5-14.4 需要学习的是区分 `传递状态的计算`、`重新计算关系的流程`、`可以一次打包的计算`。有了这个区分，才能把 Transformer 的并行处理优势解释为计算结构变化，而不是单纯的速度印象。

## 检查清单

- 能否把 RNN 解释为顺序状态传递结构？
- 能否把 Transformer 解释为 token 关系计算结构？
- 能否从大矩阵运算角度说明 Transformer 为什么适合并行处理？
- 能否从并行处理角度比较 RNN 的顺序依赖和 Transformer 的关系计算？

## 来源与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 确认日期：2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016，确认日期：2026-06-29。[https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
