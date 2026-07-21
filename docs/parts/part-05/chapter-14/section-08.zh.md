# P5-14.8 补充学习：layer normalization 为什么要对齐值的基准线

> Section ID: `P5-14.8`
> Version: `v2026.07.20`

在 P5-14.2 中，我们看到 Transformer block 里的 layer normalization 会整理值范围。但 `normalization` 这个词很容易和输入预处理、batch normalization、regularization 混在一起。

在 Transformer block 中，layer normalization 不是重新选择意义的装置。它会在一个位置表示内部重新对齐值的平均和散布，让这些值处在下一次计算更容易处理的基准线上。

当术语再次散开时，可以回到概念词汇表中的 [layer normalization](/AiBook/reference/concept-glossary/#layer-normalization) 条目，并同时对照 P5-14.2 的四个部件分工。

## 值的基准线摇晃是什么意思

Transformer block 里的表示不是一个数字，而是带有多个轴的向量。某个轴可以承载 `重启` 这个操作意义，其他轴可以承载 `保留`、`风险`、`条件` 这样的语境线索。

self-attention 和 feed-forward network 改变表示后，residual connection 又把原始表示加回来，值的大小和散布就可能持续变化。在某个 block 中，一些轴可能过大；在另一个 block 中，值又可能过于集中。如果这种状态持续下去，下一次 attention 或 feed-forward 每次都会在不同基准线上接收输入。

入门阶段可以先这样读。

| 摇晃的状态 | 为什么会成为问题 |
| --- | --- |
| 某个表示轴过大 | 下一次计算可能被这个轴过度牵引 |
| 值过于集中 | 轴之间的差异可能弱到难以读取 |
| 每个 block 的值范围变化很大 | 下一个部件很难在相似基准上继续计算 |

layer normalization 不会用 `哪个意义重要` 来解决这个问题。它整理一个位置表示内部的值范围，创建下一次计算更容易处理的输入状态。

## 在一个位置内部对齐平均和散布

layer normalization 的核心是 `在一个位置表示内部` 整理值。也就是说，它不是把整个句子的 token 混在一起选择意义，而是以当前位置表示向量里的多个数值为基准，对齐平均和散布。

```mermaid
--8<-- "assets/part-05/chapter-14/layer-normalization-value-scale-zh.mmd"
```

在这张图中，前面的表示已经经过 attention、feed-forward、residual connection，所以值范围已经摇晃。layer normalization 会在一个位置内部重新整理这些值，并把它们作为下一次计算可以开始的基准线传递下去。

这里重要的边界如下。

| 问题 | 更直接负责的部件 |
| --- | --- |
| 应该参考哪个其他 token | self-attention |
| 混入语境的当前表示应该怎样改变 | feed-forward network |
| 原始表示是否不该被新计算盖住 | residual connection |
| 下一次计算是否容易处理这些值范围 | layer normalization |

layer normalization 回答的是第四个问题。因此，`整理值` 不是 `抹掉意义`，也不是 `只留下重要意义`，而是对齐基准线，让下一次计算能更稳定地处理同类输入。

## 和 batch normalization 有什么不同

初学者最常见的混淆，是把 layer normalization 和 batch normalization 读成同一件事。二者都叫 normalization，但统计基准不同。

| 区分 | 作为基准看的对象 | 在 Transformer 语境中的读法 |
| --- | --- | --- |
| batch normalization | 多个样本构成的 batch 统计 | 要同时考虑 batch 构成和训练/评估模式差异 |
| layer normalization | 一个样本、一个位置表示内部的多个值 | 把当前位置表示对齐到下一次计算的基准线 |

在 Part 5 前面阅读 batch normalization 时，多个样本一起进入的学习 batch 很重要。相对地，在 Transformer 中，入门阶段更直接的读法是：layer normalization 以一个位置表示内部的值为基准进行整理。

这个差异在实际使用中也重要。语言模型会面对不同的句子长度、batch 构成和生成时点。layer normalization 以当前位置表示本身为基准整理值，因此适合在 Transformer block 中反复使用。

## 为什么常出现在 residual connection 后面

在 Transformer 说明中，residual connection 和 layer normalization 经常一起出现。但它们不是因为做同一件事才放在一起。

residual connection 会把原始输入表示和新计算结果一起留下。这个加法有助于保留信息流，但也可能让值的大小和散布更加摇晃。layer normalization 会把这样合并后的表示重新调整到下一次计算更容易处理的范围。

| 阶段 | 中心问题 | 结果 |
| --- | --- | --- |
| 新计算 | 当前表示应该怎样改变 | 产生反映语境的新表示 |
| residual connection | 是否一起留下原始表示 | 原始轴和新表示一起留下 |
| layer normalization | 下一次计算是否容易处理这些值 | 值基准线被整理 |

因此，把 `residual + normalization` 当成一个词组背下来是不够的。residual connection 处理信息流问题，layer normalization 处理值范围问题。

## 案例与示例

### 案例：工作许可句子中值基准线摇晃

在 `压力未解除状态下，重启应被保留` 中，看 `重启` 位置。attention 会让它同时参考 `压力未解除` 和 `保留`，feed-forward 会把当前表示加工成更接近 `有条件被阻止的操作`。residual connection 又会把原始的 `重启` 操作轴一起留下。

现在传给后面 block 的表示中已经包含多个线索。`重启`、`压力未解除`、`保留`、`风险`、`条件` 等轴可能以不同大小留下。如果某些轴过大，后面的计算可能被它们过度牵引；如果值太小或过于集中，线索之间的差异可能无法被充分读取。

layer normalization 此时不会重新判断 `重启重要还是保留重要`。它会整理已经生成的当前位置表示的值范围，让下一个 block 能在相似基准线上再次开始关系读取和表示加工。

| 表示中一起留下的线索 | layer normalization 直接做的事 | 不直接做的事 |
| --- | --- | --- |
| `重启`、`保留`、`风险` 轴的值大小不一致 | 对齐平均和散布，整理下一次计算的基准线 | 判断哪个线索在规则上更重要 |
| residual 让原始操作轴和新风险轴一起留下 | 稳定合并后表示的值范围 | 新建保留原始操作轴的路径 |
| 下一次 attention 会再次使用这个位置 | 生成下一次计算更容易处理的输入状态 | 选择该重新看哪个 token |

这个案例要确认的结果是：layer normalization 不是意义判断者，而是计算基准线整理者。

### 示例：把值范围摇晃交给实验确认

即使两个表示都承载 `重启应该被保留` 的方向，只要值范围差异很大，下一次计算接收输入时的感觉就可能不同。如果一个轴过大、所有值过于集中，或者 block 之间的值范围变化很大，下一次 attention 和 feed-forward 每次都会在不同基准线上接收输入。

如果只用文字说明，这个差异很容易变模糊。因此下一个例子会直接放入 `risk_axis_spike`、`too_narrow`、`mixed_after_residual` 三个表示，检查 normalization 前后的平均、散布和下一次计算分数如何变化。这里首先要抓住的基准是：`表示意义` 和 `值尺度` 不是同一个问题。

## 练习与示例

### 示例：确认 layer normalization 前后的基准线

这个例子不是为了背 layer normalization 公式。它是一个小实验，用来确认一个位置表示内部的值范围摇晃时，对齐平均和散布之后，下一次计算接收输入的感觉会怎样变化。

| 要操作的值 | 要观察的输出 | 要确认的问题 |
| --- | --- | --- |
| `risk_axis_spike` 的大值 | `raw mean/std`, `norm mean/std` | 一个轴过大时，基准线如何被整理 |
| `too_narrow` 的值差异 | `normalized values` | 过于集中的值是否重新获得可比较的散布 |
| `probe` | `next score before/after` | 下一次计算分数受到原始值尺度多大牵引 |

```python
# 这个例子比较 layer normalization 前后的平均值、标准差和 next score，观察一个位置表示的数值基准如何被整理。
import numpy as np

representations = {
    "risk_axis_spike": np.array([0.6, 8.0, 0.4, 0.5]),
    "too_narrow": np.array([0.48, 0.51, 0.49, 0.50]),
    "mixed_after_residual": np.array([2.0, 4.5, 1.0, 3.5]),
}

probe = np.array([0.2, 1.0, 0.3, 0.7])

def layer_norm(x, eps=1e-6):
    return (x - x.mean()) / (x.std() + eps)

for name, values in representations.items():
    normalized = layer_norm(values)
    raw_score = float(values @ probe)
    normalized_score = float(normalized @ probe)

    print(f"[{name}]")
    print("raw mean/std =", round(values.mean(), 3), round(values.std(), 3))
    print("norm mean/std =", round(normalized.mean(), 3), round(normalized.std(), 3))
    print("next score before/after =", round(raw_score, 3), round(normalized_score, 3))
    print("normalized values =", np.round(normalized, 3).tolist())
    print("---")
```

输出示例可以这样读。

```text
[risk_axis_spike]
raw mean/std = 2.375 3.248
norm mean/std = -0.0 1.0
next score before/after = 8.59 1.036
normalized values = [-0.546, 1.732, -0.608, -0.577]
---
[too_narrow]
raw mean/std = 0.495 0.011
norm mean/std = 0.0 1.0
next score before/after = 1.103 1.252
normalized values = [-1.342, 1.342, -0.447, 0.447]
---
[mixed_after_residual]
raw mean/std = 2.75 1.346
norm mean/std = 0.0 1.0
next score before/after = 7.65 1.188
normalized values = [-0.557, 1.3, -1.3, 0.557]
```

如果只把前两个轴投影到 2D 坐标上，normalization 前后的移动可以这样看。这个图不是完整展示四维表示，而是辅助确认：值尺度被整理后，同一个表示进入下一次计算时，坐标感觉也会改变。

![layer normalization 前后向量移动](/AiBook/assets/part-05/chapter-14/layer-normalization-vector-shift-zh.png)

第一种情况是一个风险轴过大的表示。layer normalization 后，平均接近 0，标准差接近 1，所以下一次计算被原始值大小过度牵引的程度降低。第二种情况是值过于集中的表示。原来的值差异很小，但标准差也很小，所以减去平均值再除以标准差后，轴之间的相对差异会重新展开到可以读取的范围。

解说：这个例子重要的不是把每个 normalized value 当成答案来背。layer normalization 不会重新选择意义，而是把一个位置表示内部的值基准线调整到下一次计算更容易处理的状态。因此 `next score before/after` 的变化不是意义判断变了，而是同一个 probe 在更整理好的输入基准上进行了计算。

### 练习：用语言诊断值范围问题

针对下面情况，用一句话写出为什么需要 layer normalization。

| 情况 | 可能的答案 | 解说 |
| --- | --- | --- |
| residual 之后某个轴值过大 | 需要整理值基准线，避免下一次计算被一个轴过度牵引 | 这是减少值大小不平衡的观点。 |
| 经过多个 block 后，表示值范围持续变化 | 需要对齐值范围，让重复 block 在相似输入基准上继续计算 | 这是深层重复稳定化的观点。 |
| 一个位置表示内部的值过于集中 | 需要重新调整散布，让下一次计算能读出轴之间的差异 | 不只是过大的值会出问题，过窄的值也可能成为问题。 |

解说：这个练习不是计算公式。它用语言确认 layer normalization 不是 `选择答案的阶段`，而是 `让下一次计算能够读取表示的条件整理`。

## 检查清单

- 能否把 layer normalization 解释为对齐一个位置表示内部值的平均和散布？
- 能否说明 layer normalization 与 batch normalization 的基准差异？
- 能否把 residual connection 和 layer normalization 区分为 `信息流保留` 与 `值基准线整理`？
- 能否说明 layer normalization 不直接负责选择意义或 token 关系？

## 来源与参考资料

- Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton, `Layer Normalization`, arXiv, 2016，确认日期：2026-07-19。[https://arxiv.org/abs/1607.06450](https://arxiv.org/abs/1607.06450){: target="_blank" rel="noopener noreferrer" }
- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017，确认日期：2026-07-19。[https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
