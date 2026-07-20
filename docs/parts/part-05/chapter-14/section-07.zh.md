# P5-14.7 补充学习：residual connection 为什么要留下原始表示的路径

> Section ID: `P5-14.7`
> Version: `v2026.07.20`

在 P5-14.2 中，我们看到 Transformer block 里的 residual connection 会留下原始信息流。但如果只听到“把原始输入加回来”这个说法，就很容易把 residual connection 误解成简单的加法技巧，或者误解成跳过计算的 shortcut。

在 Transformer block 中，residual connection 不是用来删除新计算的装置。它让新计算结果和原始输入表示一起进入下一阶段。

当术语再次散开时，可以回到概念词汇表中的 [residual connection](../../../reference/concept-glossary.md#residual-connection) 条目，并同时对照 P5-14.2 的四个部件分工。

## 只传递新计算会有什么风险

self-attention 和 feed-forward network 会不断改变当前位置表示。这种改变是必要的。问题在于，block 越深，新计算就越容易盖住原始 token 的基本意义。

例如在 `压力未解除状态下，重启应被保留` 这类句子里，先看 `重启` 位置。attention 和 feed-forward 应该把 `重启` 表示加工成更接近 `有条件被阻止的操作`。但是如果这个过程中 `重启` 这一原始操作轴完全消失，后面的 block 就更难追踪到底是什么被阻止了。

因此 residual connection 回答的是下面这些问题。

| 问题 | residual connection 的回答 |
| --- | --- |
| 新计算需要吗 | 需要。attention 和 feed-forward 会生成新的表示。 |
| 只传递新计算就够吗 | 不一定。原始表示轴可能会被盖住。 |
| 要一起传递什么 | 原始输入表示和新计算结果。 |

## 不是跳过计算，而是一起相加的路径

residual connection 也常被称为 skip connection。这里的 `skip` 不是说不做新计算，而是说原始输入表示有一条绕过新计算路径、再被加回去的通路。

```mermaid
--8<-- "assets/part-05/chapter-14/residual-connection-skip-path-zh.mmd"
```

在这张图中，实线是新计算生成的表示，虚线是原始输入表示绕过后被加回去的路径。关键不是二选一，而是 `原始表示 + 新计算结果` 会成为下一阶段表示的出发点。

可以把差异整理如下。

| 容易误读的说法 | 更合适的读法 |
| --- | --- |
| residual connection 会跳过计算 | 新计算仍然执行，只是留下原始输入表示被一起加回去的路径 |
| 既然保留原始表示，新表示就不重要 | 新表示需要，原始表示也需要 |
| 只是加法，所以只是简单后处理 | 它是让深层重复中信息流不消失的结构性装置 |

## 为什么在深层 block 重复中更重要

Transformer 不会在一个 block 就结束。同类 block 会重复多次，表示也会逐步改变。如果每次都只让新计算通过，前面阶段重要的信息可能在后面阶段变弱。

residual connection 在每个 block 里为原始表示留下通路，让深层重复不至于变成 `不断用新计算覆盖旧表示`。入门阶段可以先这样读。

| 深层重复中可能出现的问题 | residual connection 的帮助方式 |
| --- | --- |
| 原始 token 意义被新计算盖住 | 原始输入表示会一起加到下一阶段 |
| 后面的 block 失去前面 block 的出发点 | 每个 block 的输入都有一条直接连向输出侧的路径 |
| 学习过程中信号难以穿过深层 | 绕行路径让信号流更稳定地继续 |

这里的 `信号` 同时有两层感觉。一层是前向传播中表示信息经过的流动，另一层是学习时根据误差调整参数的流动。本补充学习不先追求公式，而是先抓住结构感：原始表示和新计算结果有一条一起通过的路，所以更容易堆叠深层结构。

## 不要和 layer normalization 混在一起

在 P5-14.2 中，residual connection 和 layer normalization 一起出现。但它们不是同一种稳定化装置。

| 区分 | 先看的问题 | 做的事 |
| --- | --- | --- |
| residual connection | 原始信息是否被新计算盖住 | 把原始输入表示和新计算结果一起传递 |
| layer normalization | 下一个计算是否容易处理这些值 | 整理一个位置表示内部的值基准线 |

residual connection 留下的是 `信息通过的路`。layer normalization 则让经过这条路后得到的表示值范围更容易被下一次计算处理。如果把二者合成一句话，意义就会变模糊。

## 案例与示例

### 案例：工作许可句子中不丢失操作轴

在 `压力未解除状态下，重启应被保留` 中，`重启` 位置会通过 attention 同时看 `压力未解除` 和 `保留`。feed-forward 会在当前位置内部加工这个语境，让意义更接近 `有条件被阻止的操作`。

如果没有 residual connection，后面的 block 可能会强烈接收到 `阻止`、`风险`、`条件` 这类新意义，却弱化这些意义到底附着在哪个原始操作上。residual connection 会把原始的 `重启` 操作轴一起传递，让后面的 block 持续追踪 `到底什么应该被阻止`。

| 当前位置 | 新计算强化的意义 | residual 应一起留下的轴 |
| --- | --- | --- |
| `重启` | 压力未解除条件下被阻止 | 原始操作名称 |
| `批准` | 验证未完成状态下被保留 | 原始批准行为 |
| `部署` | rollback 确认前存在风险 | 原始部署任务 |

这个案例要确认的结果是：residual connection 不是重新判断意义的装置，而是帮助新判断所需的原始表示轴继续留到后面阶段。

## 练习与示例

### 练习：找出要留下的内容，并说明理由

在下面场景中，写出新计算强化的意义，以及 residual connection 应该一起留下的原始表示轴。答案不要停在一个词上，还要说明后面的 block 为什么需要再次使用这个轴。

| 句子 | 当前位置 | 新计算强化的意义 | 应留下的原始表示轴 | 后面 block 需要它的理由 |
| --- | --- | --- | --- | --- |
| `压力未解除状态下，重启应被保留` | `重启` | 有条件阻止 | 重启这个操作名称 | 后面的 block 不只要知道有阻止意义，还要知道阻止的对象是什么。 |
| `验证未完成时，批准不应被最终确定` | `批准` | 保留或未最终确定 | 批准这个行为 | 未确定意义附着的对象必须仍然是批准。 |
| `rollback 确认前，停止部署并维持上一版本` | `部署` | 进行风险或停止对象 | 部署这个任务 | 与 `维持上一版本` 比较时，风险判断必须附着在部署任务上。 |
| `如果故障原因不明确，扩大告警并停止自动恢复` | `自动恢复` | 原因不明情况下的停止对象 | 自动恢复这个操作 | 为了不和 `扩大告警` 混在一起，必须留下停止意义附着在哪个操作上。 |

解说：好的答案不会停在 `保留原来的词`。新计算生成的意义在后面的 block 中再次使用时，这个意义附着的原始对象或行为必须可以追踪。这就是为什么 residual connection 不应被读成简单加法，而应被读成在深层重复中留下信息流的装置。

## 检查清单

- 能否把 residual connection 解释为不是跳过新计算，而是把原始输入表示和新计算结果一起传递的路径？
- 能否用案例说明深层 Transformer block 重复中为什么需要原始表示轴？
- 能否把 residual connection 与 layer normalization 区分为 `信息流` 和 `值范围稳定化`？

## 来源与参考资料

- Kaiming He et al., `Deep Residual Learning for Image Recognition`, CVPR 2016，确认日期：2026-07-19。[https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html](https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html){: target="_blank" rel="noopener noreferrer" }
- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 确认日期：2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
