# P5-13.3 补充学习：查询-键-值（QKV）与多头注意力（multi-head attention）

Section ID: `P5-13.3`
Version: `v2026.07.18`

在 P5-13.1 和 P5-13.2 里，我们已经先固定了 attention 与 self-attention 的直觉。读到这里，自然会出现下一个问题。

那么，为什么在实际计算里，attention 会被解释成 query、key、value，而 multi-head attention 又为什么会被单独拿出来命名？

当这些术语又开始散开时，可以一起回到英文概念词汇表里的 [query-key-value (QKV)](/AiBook/en/reference/concept-glossary/#-query-key-value-qkv) 和 [multi-head attention](/AiBook/en/reference/concept-glossary/#multi-head-attention) 条目重新对齐。

## 本补充学习的范围

- query、key、value 分别是什么意思？
- 为什么 self-attention 的计算要拆成这三个名字来解释？
- multi-head attention 所说的“看很多次”到底是什么意思？
- 在阅读 Transformer 时，对这些概念理解到什么程度就够了？

这篇补充学习集中抓住的是`为什么要用这些名字`，以及`应该怎样直观地读一头和多头之间的差别`。这里的核心不是`要不要再背更多公式`，而是`能不能把已经抓住的 attention 直觉，用 QKV 和 multi-head 这些反复出现的名字重新读一遍`。

## 本补充学习的目标

- 能在入门层次解释 query、key、value。
- 能把 self-attention 读成一种`先发问、再找匹配位置、再把信息带回来`的计算。
- 能把 multi-head attention 解释成`不是只从一种关系看，而是把关系分成多个视角来读`。
- 在回头阅读 Transformer 小节时，能想起 QKV 和 multi-head 分别放在什么位置。

## 如果先用一个很短的比喻来看

query、key、value 可以先这样类比。

| 名称 | 入门直觉 |
| --- | --- |
| query | 我现在想找什么？ |
| key | 每个位置贴着什么样的标签？ |
| value | 真正会被带回来的内容是什么？ |

如果把它改写成图书馆比喻，就是下面这样。

- query：`我现在想找一本历史书`
- key：`每张书卡上都写着历史、科学、小说之类的标签`
- value：`真正会被拿来阅读和带回去的书的内容`

也就是说，attention 就是一种计算：按照`当前真正需要的问题（query）`，去找拥有匹配`标签（key）`的位置，然后从那里多带回一些`实际内容（value）`。

如果立刻放到运维备忘录语境里读，会更清楚。

| 同一运维备忘录场景 | 像 query 一样读的东西 | 像 key 一样读的东西 | 像 value 一样读的东西 |
| --- | --- | --- | --- |
| `已提出解除停机请求。但压力恢复仍未完成。` | 当前表示重新发出的提问：`到底还有什么没有完成？` | `解除停机`、`压力恢复`、`尚未完成` 这些显示各位置属于什么信息类型的标签 | 真正需要重新混回当前表示里的`请求解除`与`恢复未完成`这些语义内容 |
| 交接班摘要 | 当前摘要表达在问：`这是最终决定、依据，还是条件？` | 每句话更接近`结论`、`异常征兆`还是`安全条件`的标签 | 最终摘要里真正需要保留下来的决定、依据与条件内容 |
| 阅读维修代码 | 当前代码行重新问：`这个值到底来自哪里？` | 变量定义、条件表达式、函数调用分别扮演什么角色的标签 | 真正需要重新混回当前代码解释里的定义-使用关系与调用上下文 |

也就是说，把 QKV 单独叫出来的原因，就是为了把`现在在找什么`、`每个位置是什么类型的信息`、`真正会带回什么来改变表示`这三种角色分开来读。本节是为了抓住这些角色名字为什么需要，而不是为了展开矩阵维度或实现优化。

## 在 self-attention 里面，什么发生了变化

在 P5-13.2 里，我们把 self-attention 解释成了`同一序列里的 token 会彼此参考并重新计算自己的表示`。如果把 QKV 接上去，这同一句话就会被改写成一种更贴近计算的说法。

- 当前 token 会发出一个 query，意思是`我现在需要什么？`
- 每个 token 都带着一个 key，意思是`我是什么类型的信息？`
- 每个 token 也都有一个 value，意思是`我真正能提供回去的内容是什么？`

也就是说，当前 token 会拿自己的 query 去和其他 token 的 key 比较，决定`我应该更强地参考谁`；然后再把那些 token 的 value 按权重做加权平均，形成新的表示。

把这条流程画得很简单，会是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-13/qkv-flow-zh.mmd"
```

这张图压缩的是下面这串计算顺序。

1. 当前 token 先发出一个问题。
2. 它比较：哪个 token 的标签和这个问题更匹配。
3. 对更匹配的位置分配更大权重。
4. 从那些位置多带回一些真正的内容（value），形成新表示。

## 为什么还要把 key 和 value 分开

入门读者在这里很自然会问：`反正都是同一个 token，为什么还要把 key 和 value 分开叫？`

核心原因在于，`用来寻找的标准`和`真正要带回来的内容`，可以扮演不同角色。

例如，假设我们想在交接班记录里找到`这次交接的最终决定`。

- `决定`、`批准`、`暂缓` 这些词，更像是帮助搜索的标签
- 而模型真正需要带回来的，是整句话里面的语义表示

也就是说，key 更接近`决定这个位置要被参考多少的标签`，而 value 更接近`真正会被混进来形成新表示的内容`。

把这个区分缩成一句话，就是下面这样。

`key 更接近决定该看哪里，value 更接近决定真正要带回什么。`

## 再用一个小句子回头看

```text
已提出解除停机请求。但压力恢复仍未完成。
```

如果当前 token 正在理解 `但是` 后面的语境，那么 query 就可以像一个问题：`这里现在形成对比的到底是什么？` 在这种情况下，`提出解除停机请求` 和 `压力恢复未完成` 这两段表达会各自给出不同的 key，而与当前 query 更匹配的位置就会得到更大的权重。然后那个位置的 value 会被更多地混进来，于是当前表示被更新。

也就是说，在 self-attention 里，一个 token 的工作方式是：`重新扫整句话，再把此刻我解释所需要的线索挑出来并混回来。`

## multi-head attention 所说的“看很多次”是什么意思

接着就会出现下一个问题。

如果一次 attention 已经够了，为什么还要有 `multi-head`？

核心点在于，模型并不是只看一种关系，而是把 token 之间的关系分成不同视角去读。

`不要只看一种关系，而是从不同视角把这些关系读很多遍。`

例如，在一句话里，即使是同一个 token，也可能同时参加多种重要关系。

- 某个 head 可能更擅长看主语-动词关系
- 某个 head 可能更擅长看修饰语-被修饰对象或指代关系
- 某个 head 可能更擅长看近距离 token 组合，另一个则更擅长看远距离连接

也就是说，multi-head attention 是一种装置：它不会只看一个“正确关系”，而是把多种相关性拆开来读。

下面这张表，会直接比较 single-head 和 multi-head 在同一场景里分别更容易留下什么关系信息。

| 同一场景 | 像 single-head 那样只读一次时更容易先留下什么 | 像 multi-head 那样从多个视角去读时更容易先留下什么 |
| --- | --- | --- |
| 步骤文档转换 | 最显眼的一种关系会先留下，修饰范围或例外条件更容易变弱 | 主体-动作、修饰范围、对比关系可以被分开同时保留 |
| 交接班摘要 | 可能只剩下一句结论，而依据和条件一起被削弱 | 结论、依据、条件更容易以不同相关性模式被分别保留 |
| 维修代码理解 | 容易偏向一种信号，例如重复变量名 | 定义-使用、条件-结果、调用流更容易从不同视角一起被读出 |

## 如果用图来读

```mermaid
--8<-- "assets/part-05/chapter-13/multihead-flow-zh.mmd"
```

这张图真正要抓住的，不是`输入被切成了好几块`，而是`同一份输入从不同视角被读过后，再把结果重新合起来`。

如果把同一句判断句放进 single-head 和 multi-head 的感觉里并排看，很短地说会是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-13/single-vs-multihead-baseline-zh.mmd"
```

这张比较图首先要抓住的是下面几点。

- single-head 容易把`决定`、`依据`、`条件`压成一个折中的上下文。
- multi-head 则能把同一输入拆成不同相关性模式，例如`决定-依据关系`和`决定-条件关系`。
- 只有先抓住这个感觉，multi-head 才不会被读成`attention 重复很多次`，而会被读成`把不同类型的关系分别保留下来的结构`。

## 案例与示例

这一节的案例，首先该看的不只是`重新回头看远处位置`，而是`哪些类型的关系必须被分开带着走`。也就是说，即使是同一句话，我们也需要区分：`决定`、`依据`、`条件`、`定义-使用`这些关系，到底是被压进一个平均上下文里，还是能被不同视角分别保留。

### 代表案例：步骤文档转换

把一份很长的步骤文档转成作业指令时，人很容易觉得只要把每个词的意思一一对应就够了。但实际上，主体-动作关系、修饰范围、否定、例外条件，可能会同时重要。比如有些场景里，如果想把作业指令真正写对，就必须同时看到`谁修饰谁`，以及`谁和谁形成对比`。如果只有一次 attention 把所有关系都读成同一种类型，这些关键差异就可能被混在一起。multi-head attention 给出的直觉，是把不同关系分开来读，所以它很适合解释步骤文档里多个语法线索都要被同时反映的场景。

所以，这个案例里要确认的结果是：当前这句指令并不是只跟着一种关系走，而是把主体-动作关系和例外条件范围当成不同视角一起保留下来，从而让实际作业顺序不那么容易被扭曲。

同样的视角也会直接延伸到交接班判断句整理和维修代码阅读。不过，本节真正要抓住的不是领域名称，而是`那些很容易被折成一个上下文的关系，是否能在不同 head 里被分别保留下来`。

```mermaid
--8<-- "assets/part-05/chapter-13/multihead-decision-condition-case-flow-zh.mmd"
```

这张图压缩的是：同一句判断句在 single-head 里容易被折中，而在 multi-head 里则会重新拆成决定、依据、条件几种关系。

| 人容易先看的标准 | 从 single-head 视角重新读时的标准 | 从 multi-head 视角重新读时的标准 |
| --- | --- | --- |
| 觉得步骤文档只要抓住几个关键词就够了 | 最强的一种关系会先留下，修饰范围和例外条件可能被折进同一个上下文 | 不同 head 可以分别保留主体-动作、修饰范围和对比关系 |
| 觉得交接班判断句只要抓住结论词就够了 | 一个以结论为中心的信号可能拖着平均上下文走，依据和条件会被削弱 | 结论、依据、条件可以拆成不同相关性模式被保留更久 |
| 觉得代码只要变量名接得上就算读懂了 | 定义-使用、条件-结果、调用流容易被混成一个折中表示 | 不同 head 会把不同连接模式拆开来看，从而不只被一种信号牵着走 |

这三个案例里共同要确认的结果，是：关系不会只被读成一条线，而会从多个视角分开来看。在步骤文档转换里，只要看主体-动作关系和例外条件是否一起保留下来；在交接判断句里，只要看结论、依据、条件是否都在；在代码里，只要看定义-使用和条件-结果关系是否都继续存在，就够了。

这些案例里最终要确认的结果也很明确。multi-head 的差别，不在于`attention 跑了很多次`，而在于：那些在 single-head 里很容易被压成一个上下文的不同关系，会被分到不同 head 里保留得更久。

## 练习与例子

这个例子的目标，是直接实验：即使在同一串 token 上，不同 head 会怎样读出不同关系，而这种差异又会怎样随着 head 权重变化而放大或缩小。

这一次我们不用抽象 token，而是把一段很短的运行报告片段放成简单向量来看。当前有三块内容：`停机决定`、`压力异常依据`、`复归条件`。核心问题是：single-head 会不会倾向于把它们折成一个折中上下文，而 multi-head 能不能把`决定侧`和`条件侧`这样的视角分开保留。

输入：

- 三个 token 表示
- 三种 head 权重场景
- 一个用作对照基线的 single-head 权重

输出：

- 每个场景里的 single-head 上下文
- 每个场景里的 head1、head2 上下文
- 每个 head 相对 single-head 基线的差值
- 一个显示两头读关系差得有多开的 separation 指标

问题场景：

- 如果只用语言解释，multi-head attention 很容易显得抽象，所以直接比较：当不同 head 被设得更不同时，关系分离到底会放大多少，会更有帮助

要确认的概念：

- 即使面对同一串 token，不同 head 也能强调不同关系
- 如果各 head 权重很像，multi-head 也会更接近折中；如果差得更开，关系分离就会更明显
- 把几个 head 的结果重新合起来时，可以形成比 single-head 更丰富的表示

输入：

这里使用上面整理好的三个报告片段表示和三种 head 权重场景。

在看代码之前，先猜一猜每种场景会留下多大的关系分离，会更容易看出`一个折中的上下文`和`几种被拆开的关系`之间的差别。

| 比较项 | 先应该预测的输出 | 这样预测的理由 |
| --- | --- | --- |
| `balanced_heads` | `head1_context` 和 `head2_context` 的差距可能比较小 | 因为两个 head 都会以相近比例混合`停机决定`、`压力异常依据`、`复归条件` |
| `decision_vs_condition_split` | `head1_context` 和 `head2_context` 的差距可能最大 | 因为一个 head 会更强地推向决定侧，另一个会更强地推向条件侧，从而把 single-head 会压平的差异重新拉开 |
| `condition_heavy_both_heads` | 两个 head 可能都会往后侧偏，和 single-head 的差异也许更小 | 因为两个 head 强调的不是不同视角，而是同一类条件侧关系 |
| `head_separation` | `decision_vs_condition_split` 最可能最大 | 因为当不同 head 真正在读不同关系时，分离程度就会更大 |

这张表的目的，并不是让人预先算准向量值，而是让人在读代码前先抓住：multi-head 不是简单重复，而是`关系分离`会随着 head 的设计而放大或回缩。

```python
import numpy as np

tokens = np.array([
    [1.0, 0.0],   # shutdown decision
    [0.0, 2.0],   # pressure-anomaly basis
    [3.0, 1.0],   # restart condition
])

single_head_weights = np.array([0.4, 0.3, 0.3])

scenarios = {
    "balanced_heads": {
        "head1": np.array([0.45, 0.30, 0.25]),
        "head2": np.array([0.30, 0.30, 0.40]),
    },
    "decision_vs_condition_split": {
        "head1": np.array([0.70, 0.20, 0.10]),
        "head2": np.array([0.10, 0.30, 0.60]),
    },
    "condition_heavy_both_heads": {
        "head1": np.array([0.20, 0.25, 0.55]),
        "head2": np.array([0.15, 0.20, 0.65]),
    },
}


def summarize_scenario(name, head1_weights, head2_weights):
    single_head_context = single_head_weights @ tokens
    head1_context = head1_weights @ tokens
    head2_context = head2_weights @ tokens
    combined = np.concatenate([head1_context, head2_context])
    difference_from_single = combined - np.concatenate(
        [single_head_context, single_head_context]
    )
    head_separation = np.linalg.norm(head1_context - head2_context)

    print(f"[{name}]")
    print("single_head_context =", np.round(single_head_context, 3).tolist())
    print("head1_context       =", np.round(head1_context, 3).tolist())
    print("head2_context       =", np.round(head2_context, 3).tolist())
    print("difference_from_single =", np.round(difference_from_single, 3).tolist())
    print("head_separation =", round(float(head_separation), 3))
    print()


print("tokens =")
print(tokens)
print()

for scenario_name, heads in scenarios.items():
    summarize_scenario(scenario_name, heads["head1"], heads["head2"])
```

在输出里，可以先看不同场景下 `head_separation` 和 `difference_from_single` 会怎样变化。

```text
tokens =
[[1. 0.]
 [0. 2.]
 [3. 1.]]

[balanced_heads]
single_head_context = [1.3, 0.9]
head1_context       = [1.2, 0.85]
head2_context       = [1.5, 1.0]
difference_from_single = [-0.1, -0.05, 0.2, 0.1]
head_separation = 0.335

[decision_vs_condition_split]
single_head_context = [1.3, 0.9]
head1_context       = [1.0, 0.5]
head2_context       = [1.9, 1.2]
difference_from_single = [-0.3, -0.4, 0.6, 0.3]
head_separation = 1.14

[condition_heavy_both_heads]
single_head_context = [1.3, 0.9]
head1_context       = [1.85, 1.05]
head2_context       = [2.1, 1.05]
difference_from_single = [0.55, 0.15, 0.8, 0.15]
head_separation = 0.25
```

这个例子里第一眼最该看的，是不同场景下的 `head_separation`。在 `decision_vs_condition_split` 里，两头真的分别朝决定侧和条件侧分开，所以 separation 最大；而在 `condition_heavy_both_heads` 里，虽然也有两个 head，但它们都看向同一边的条件侧，所以分离程度就小。

![不同场景下的 head separation](/AiBook/assets/part-05/chapter-13/qkv-head-separation-zh.png)

第二个要看的，是 single-head 上下文和 head1 / head2 上下文在坐标空间里会分开到什么程度。灰点是同一个 single-head 基线，蓝三角和橙方块之间越远，就越能看见两个 head 正在读取不同关系。

![single head 与两个 head 的上下文位置](/AiBook/assets/part-05/chapter-13/qkv-head-context-space-zh.png)

| 先看的输出 | 这个输出意味着什么 | 如果改动它，会跟着改变什么 |
| --- | --- | --- |
| `head_separation` 很大 | 说明两个 head 确实在读不同关系 | 如果让各 head 权重更相似，分离程度会变小；如果让它们更不同，分离程度会变大 |
| `difference_from_single` 向两个方向散开 | 说明 single-head 里被平均掉的差异，在 multi-head 里又被拆了出来 | 如果改动 single-head 基线权重，就能比较哪些差异已经先被`折中结果`吸收掉了 |
| 两个 head 一起朝同一方向变大 | 说明即使有两个 head，也可能只是在重复看同一种关系 | 像 `condition_heavy_both_heads` 那样让两个 head 都偏向同一侧时，multi-head 的分离优势会缩小 |

| 阅读标准 | 如果只看 single-head 输出，容易得到的判断 | 看过场景比较之后会改变的判断 |
| --- | --- | --- |
| 运行报告摘要 | `停机决定`、`压力异常`、`复归条件` 可能只剩下一个整体平均，结论和条件分别是什么会变弱 | 如果像 `decision_vs_condition_split` 那样把 head 分开，结论和条件就能作为不同上下文保留更久 |
| 步骤文档解释 | 很容易觉得 head 只要有多个，关系自然就会多样化 | `condition_heavy_both_heads` 会提醒我们：即使有两个 head，如果它们都强调同一类条件侧关系，分离也仍然不大 |
| 实验设计 | 很容易觉得只看一个数值就已经理解了 multi-head | 只有把 `balanced_heads`、`decision_vs_condition_split`、`condition_heavy_both_heads` 并排看，才会更清楚：关键在于`各 head 被设得有多不同` |

也就是说，如果说 single-head 会把多种关系折成一个折中表示，那么 multi-head 就会把不同关系读取结果并排保留下来，让那些在单一平均里消失的差别活得更久。不过，这种效果更依赖于`不同 head 真实读取的关系差得有多开`，而不是单纯依赖`head 的数量`。

如果把这些数字翻回运行报告阅读，`balanced_heads` 还比较接近折中式摘要，而 `decision_vs_condition_split` 更接近于把`决定侧上下文`和`条件侧上下文`分开保留下来的阅读。相反，`condition_heavy_both_heads` 则是一个场景：虽然有两个 head，但它们都被拉向条件侧，所以 multi-head 的优势被削弱了。真正重要的，不是向量值本身，而是`不同 head 会把哪些判断单独留下来`。

真实的 multi-head attention 后面还会包含线性变换等更细的组合过程，但在入门阶段，只要先抓住两种感觉就够了：`不同关系读取结果会被并排保留`，以及`head 是怎么分开的，这件事本身很重要`。

这个例子也更适合被当成一个可以继续改动的实验，而不是跑一次就结束。下面三种改动，会很适合继续观察`关系分离`什么时候变大、什么时候又缩回去。

| 现在马上可以改的值 | 要观察的输出 | 要解释的问题 |
| --- | --- | --- |
| 让 `head1`、`head2` 的权重更相似 | `head_separation` | 如果不同 head 最后读得几乎是同一种关系，multi-head 的优势到底会缩小多少？ |
| 让 `single_head_weights` 更偏向 `head1` 或更偏向 `head2` | `difference_from_single` | 如果 single-head 本来就已经强烈反映某一种关系，那么它和 multi-head 的差距会缩小多少？ |
| 把 `tokens` 里的`复归条件`值调大或调小 | `head2_context`、`head_separation` | 如果 token 自身语义强度变化了，哪个 head 会对这种变化更敏感？ |

前面的数字并没有实现真实大规模 multi-head attention 的全部，但它已经足够清楚地展示两条比较标准。第一，single-head 倾向于把多种关系一次平均成一个折中上下文，而 multi-head 会把不同关系读取结果并排保留下来再一起使用。第二，head 的设计本身会放大或缩小这种差异。也就是说，multi-head attention 并不只是`attention 重复很多次`，而更像是一种结构：通过把 head 分开，让不同类型的相关性模式可以同时被保留下来而不轻易丢失。

这一节最后读者真正该抓住的结论也是一样的。QKV 是一组名字，它让我们把`正在找什么`、`和什么标签匹配`、`真正会带回什么`分开来读；而 multi-head 则是一种结构：它不会把这些关系一次平均掉，而是让`决定`、`依据`、`条件`这样的不同视角活得更久。

## 为什么它在 Part 5 的流程里重要

这篇补充学习，并不是夹在 attention 小节和 Transformer 小节之间的一张实现细节备忘录。相反，它更像是一个回收位置：把本篇正文里已经固定好的直觉，接回到`为什么这些名字和结构会出现`。attention 和 self-attention 的核心直觉，已经在正文里收住了；但因为 QKV 和 multi-head 这些名字会在 Transformer 本文里一再出现，所以这一节更适合被保留成`重新读这些名字的入门回收点`，而不是一份公式备忘录。下一章 P5-14.1 会继续解释：这些名字在 Transformer block 里到底放在什么位置。

## 检查清单

- 能解释 QKV 是一组用来描述 attention 计算的名字吗？
- 能说明为什么 multi-head attention 应该被读成从多个视角进行参考计算吗？
- 能把 query、key、value 解释成`问题`、`标签`、`带回来的内容`这三种不同角色吗？
- 能说明 multi-head attention 不是只看一种关系，而是把几类相关性一起读出来的方法吗？
- 能把 single-head 和 multi-head 的差别，解释成`一个折中的关系`和`多个关系视角同时被保留`吗？
- 当 query、key、value 这些名字突然看起来和 attention 直觉脱节时，能先想到 QKV 回收视角吗？
- 当需要解释为什么要有多个 head 时，能回到 single-head 折中和 multi-head 多视角保留的差别吗？
- 在读下一节 Transformer 时，是否已经准备好先问：`为什么这些名字会在 block 里反复出现，成为关键部件？`

## 来源与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 确认日期：2026-06-30。
- Jay Alammar, `The Illustrated Transformer`, 确认日期：2026-06-30。 [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-30。 [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }

