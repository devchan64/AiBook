# P5-14.1 不能只靠 attention 解释的 Transformer

> Section ID: `P5-14.1`
> Version: `v2026.07.31`

本章的起点不是一个 `attention_score`，而是 `token_representation` 经过 block 时如何进入下一个表示。因此从 P5-14.1 开始，要把 `relation_reading`、`position_update`、`stable_passage`、`next_block_input` 作为一个 流程 来读。

_副标题: 为什么 Transformer 应该读成 block 结构，而不是只有 self-attention？_

在 P5-13.2 里，我们已经看到 self-attention 是同一序列里的 token 彼此重新参考并更新表示的方式。这里马上会出现下一个问题。

只说 Transformer 是使用 self-attention 的模型，这样够吗？

不够。Transformer 是一种 block 结构：它用 self-attention 读取关系，用 feed-forward network 重新加工各位置的表示，并用 residual connection 与 layer normalization 稳定深层重复计算。只有抓住这个差别，后面读并行处理、长上下文、LLM 结构时，才不会只用`有 attention`这句话就结束说明。

## Transformer 基本问题处理的提问

- 如果 self-attention 是 Transformer 的核心，为什么不能只用它解释完？
- Transformer block 应该被读成哪几种角色的组合？
- Part 5 应该把 Transformer 讲到哪里，又把什么交给下一节？

这里首先要抓住的问题，不是`Transformer 有哪些部件`，而是`为什么 self-attention 和 feed-forward 必须被捆成可以重复的 block`。

| 本节现在要读的内容 | 交给后续小节的内容 |
| --- | --- |
| 把 Transformer 读成 block 结构，而不是只读成 self-attention 的标准 | 各部件的细部角色和表示更新过程 |
| 关系读取、按位置加工、稳定传递必须一起存在的感觉 | 并行处理、长上下文直接再参考、生成模型连接 |

## 只有 self-attention 时会缺什么

self-attention 擅长决定当前 token 应该更强地参考其他 token 中的哪些位置。但模型一旦变深，后面的问题会立刻接上来。

- 带回来的上下文信息，要在当前位置怎样重新加工？
- 新计算怎样避免把原来的信息覆盖得太厉害？
- 多层反复计算时，数值大小和分布怎样避免过度摇晃？

如果这些问题空着，Transformer 就只会被理解成`有 attention 的模型`。更稳妥的标准是下面这句。

`Transformer 是一种结构：它把 self-attention 的关系读取、feed-forward 的按位置表示加工、以及稳定传递捆成一个可以重复的 block。`

## 先从大图看基本 block

入门层次读 Transformer block 时，可以先区分四个元素。

| 组成元素 | 首先要抓住的角色 |
| --- | --- |
| self-attention | 读取与其他 token 的关系 |
| feed-forward network | 重新加工各位置表示 |
| residual connection | 把原始信息流也一起留下 |
| layer normalization | 整理数值范围，让计算不那么摇晃 |

这四个并不是彼此散开的部件清单。通常它们会被捆成一个重复单元：`读取上下文关系 -> 加工当前位置表示 -> 保留原始信息与稳定性 -> 传给下一个 block`。

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-block-repeat-zh.mmd"
```

这张图里重要的，不是一次 attention 计算，而是同一组结构会在下一个 block 里再次重复。所以 P5-14.1 先不急着展开细部计算，而是先抓住一个标准：`关系读取`、`表示加工`、`稳定传递`会被捆成一个重复单元。

## 案例与示例

### 案例：只靠 attention 无法抓住处置判断的情况

想一想这样一句工作许可句：`Restart is held while the pressure remains unreleased.` self-attention 对于读取 `pressure unreleased`、`restart`、`held` 彼此相关这一点很重要。但如果说明到这里就结束，那么当前动作表达怎样从`单纯重启`变得更明确地指向`条件性暂缓`，以及这个意义怎样保持到下一层，都会空着。

人一开始容易使用的标准是：`restart 这个词是否参考了 pressure unreleased 和 held？` 这个标准足以说明 attention 的作用。但要解释整个 Transformer，还会剩下一个问题。

读完这个关系之后，当前动作表示应该以什么状态进入下一个 block？

只要这个问题还在，attention-only 说明就会断掉。`restart` token 参考了前面的条件，这件事本身还不能说明当前表示怎样从`可批准的动作`被加工成`有条件的阻断动作`，也不能说明它怎样在不丢失原始动作意义的情况下，被整理成下一步计算容易处理的范围。

把同一句话分成两种读法，差别会更清楚。

| 读法 | 能解释的内容 | 说明断开的地方 |
| --- | --- | --- |
| attention-only 说明 | `restart` 与 `pressure unreleased`、`held` 相关 | 读完关系之后，当前表示会变成什么动作状态 |
| Transformer block 说明 | 读取关系、加工当前位置表示、保留原始动作意义与稳定性，并把结果传给下一个 block 的流程 | 细部角色分工与表示移动会在 P5-14.2 中一起处理 |

这个案例的确认结果可以这样抓住。

| 读取当前表示时的问题 | 只靠 attention 能回答吗 | block 视角需要补充什么 |
| --- | --- | --- |
| 这个动作和什么条件相连？ | 可以 | self-attention 负责的关系读取 |
| 因为连接了那个条件，动作表示会怎样改变？ | 不足 | feed-forward 重新加工当前位置表示 |
| 新表示会不会不丢掉原始动作意义，并进入下一步计算？ | 不足 | residual connection 与 layer normalization 辅助稳定传递 |

这个案例要确认的结果不是`attention 很重要`。更准确的结果是：`attention 是读取关系的核心，但 Transformer 的说明必须包含这个关系怎样改变当前表示，并怎样稳定进入下一个 block，才算抓住。`

## 练习与例子

### 练习：把 attention-only 说明改成 block 说明

看下面的输入句子，先从三个说明里选出哪一个最能抓住 P5-14.1 的中心问题。

输入句子：

`Restart is held while the pressure remains unreleased.`

| 候选说明 | 判定 |
| --- | --- |
| A. `Restart` 参考了 `pressure unreleased` 和 `held`，所以 Transformer 说明已经结束。 | 不足 |
| B. `Restart` 参考了 `pressure unreleased` 和 `held`，并且因为这个关系，当前动作表示应该被加工到 `conditional hold` 一侧。 | 中间 |
| C. `Restart` 参考相关条件，这个关系会改变当前动作表示，并且结果要在保留原始动作意义与稳定性的情况下进入下一个 block。 | 更合适 |

解说：A 只说了 self-attention 负责的`关系读取`。它能回答`参考了什么`，但不能解释`参考之后当前表示怎样改变`。B 更接近 feed-forward network 为什么需要出现。但在深层 block 反复中，改变后的表示还需要稳定性，不能在进入下一步计算时完全丢掉原始动作意义。C 最接近本节中心。P5-14.1 要抓住的不是`attention 很重要`，而是`attention + 按位置加工 + 稳定传递必须被捆成一个 block，Transformer 说明才会确认`。

接下来，直接改写下面的短说明。

| 改写前说明 | 改写后的说明示例 | 为什么这样改 |
| --- | --- | --- |
| Transformer 通过 self-attention 参考需要的词。 | Transformer 通过 self-attention 读取需要的词之间的关系，再重新加工混入这种关系后的当前表示，并稳定地传给下一个 block。 | 停在`参考`就是 attention 说明；到了`加工表示并稳定传递`，才是 block 说明。 |
| 因为 `restart` 参考了 `pressure unreleased`，所以可以判断暂缓。 | `restart` 参考 `pressure unreleased` 之后，当前动作表示必须转向 `conditional hold`，并且这个意义要在下一步计算中继续保留。 | 只确认关系，还不能说明当前表示的变化和传递。 |

解说：好的答案不是背了很多部件名称的句子。只要包含`关系读取`、`当前表示加工`、`稳定传给下一个 block`，就通过 P5-14.1 的标准。self-attention、feed-forward、residual connection、layer normalization 各自负责什么，会在 P5-14.2 中再分开确认。

## 检查清单

- 能说明为什么只用 self-attention 解释 Transformer 会缺东西吗？
- 能说明 self-attention 的关系读取和 feed-forward 的按位置加工，必须在重复 block 里一起出现吗？
- 是否已经准备好把下一节读成对各部件角色分担的进一步说明？

## 来源与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 确认日期：2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Jay Alammar, `The Illustrated Transformer`, 确认日期：2026-06-29. [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/){: target="_blank" rel="noopener noreferrer" }
