# P1-7.1 搜索空间与计算极限

> Section ID: `P1-7.1`
> Version: `v2026.07.26`

第 6 章讨论了信息不完整与概率性判断。现在要转向另一类困难。有些问题之所以难，是因为信息不足；但还有些问题之所以难，是因为可能的选择实在太多。

这里的核心问题是：

> 当可能解太多时，  
> AI 到底会先失去“把所有情况都看完”的能力中的哪一部分？

要理解 `heuristic`，必须先建立 `search` 和 `search space` 的基本感觉。

在 Part 1 里，`search`、`search space`、`computational limit` 和 `exhaustive search` 的基础区分先在这一节固定。第 6 章先处理了不确定性和概率，这里则转向另一种困难：候选项多到无法现实地全部检查。启发式的具体作用会在 7.2 紧接着展开。

在同一个服务里，这两种困难甚至可能并排出现：

| 同一服务里的场景 | 核心困难 | 最先该想到的方法 |
| --- | --- | --- |
| 估计配送延迟的原因 | 信息不完整，可能原因不止一个 | 不确定性、概率、证据更新 |
| 决定今天的配送路线 | 路径候选太多，难以全部比较 | 搜索、剪枝、启发式 |

关键是要把“因为不知道什么是真的而难”和“因为候选太多而难”先拆开。

> 一旦候选数爆炸，问题就不只是定义正确答案，  
> 还变成了如何找到通向答案的路径。

这一节不会实现具体搜索算法。这里不去计算 breadth-first search、depth-first search 或 A*。

也不会在这里完整解释 heuristic function。启发式本身会在 7.2 继续。

这里先固定一个更窄的观点：

> 当可能的状态和选择变得太多时，  
> 想把每一种情况都看完的方法，很快就会碰到极限。

## 搜索空间如何造成计算极限

- 把 `search` 理解成“查看可能候选并寻找解”的过程。
- 在入门层面区分 `state`、`action`、`goal`、`path` 和 `cost`。
- 理解为什么搜索空间一旦变大，就会出现 `computational limit`。
- 说明为什么 `exhaustive search` 在很多现实问题里会变得不现实。
- 为 7.2 中为什么需要启发式做准备。

## 三个基准

| 基准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 搜索是沿着候选不断前进以寻找解的过程 | 这能让我们把 AI 问题看成“结构化选择”，而不只是计算。 | 先保留“像找路一样，一步步决定往哪走”的直觉。 |
| 搜索空间是所有可能状态与选择的整体 | 这能解释为什么候选数会突然变得很大。 | 理解步骤一多，可能情况会迅速增长。 |
| 计算极限意味着我们无法现实地看完所有情况 | 这会直接连到下一节为什么需要启发式。 | 理解完全搜索在理论上可行，但在实践中可能太慢。 |

先做一个简短的角色分拆：

| 术语 | 极短含义 | 本节里的作用 |
| --- | --- | --- |
| search | 沿着可能候选寻找解的过程 | 问题求解的大框架 |
| search space | 所有可能状态与选择的整体 | 解释候选数为何增长的框架 |
| state | 问题当前的一种样子 | 表示搜索现在走到哪里 |
| action | 改变状态的一个选择 | 生成下一个候选的单位 |
| path | 一串相连状态形成的轨迹 | 通向解的实际路径 |
| cost | 比较哪条路径更好的标准 | 距离、时间、资源等比较依据 |
| computational limit | 现实中无法把所有候选都看完的状态 | 启发式之所以必要的原因 |

## 搜索是一种查看候选的求解方式

Poole 和 Mackworth 说明，智能体为了达到目标而寻找方法的问题，可以抽象成：在图(graph)里从起点节点到目标节点寻找路径。AIMA 也把问题求解和搜索放在 AI 导论前部的核心位置。

Poole 和 Mackworth 直接写过一句话：

> “Search underlies much of AI.”  
> — David L. Poole, Alan K. Mackworth

这里先把搜索理解成：

> 从当前状态出发，  
> 沿着可选路径前进，直到找到通向目标的路径。

拿路径规划来说：

| 元素 | 找路例子 |
| --- | --- |
| state | 当前位置 |
| action | 走向下一条道路 |
| goal | 到达目的地 |
| path | 经过的道路与路口顺序 |
| cost | 距离、时间、过路费或能耗 |

这种结构并不只属于找路。排程、解谜、博弈、代码修改顺序，甚至文档目录候选的比较，都可以用类似视角来看。

## 搜索空间是所有可能状态与选择的整体

`search space` 指的是：在解决问题时，所有可以考虑的状态和动作所构成的整体结构。

先看一个简单例子：

> 决定早上要做什么  
> 第一层候选：运动、阅读、查邮件  
> 第二层候选：通勤、准备会议、买菜

如果第一步有 3 个选择，下一步也有 3 个，那么就已经有 9 种组合。阶段一多，候选数会迅速膨胀。

| 阶段数 | 每阶段有 3 个选择时的组合数 |
| ---: | ---: |
| 1 | 3 |
| 2 | 9 |
| 3 | 27 |
| 4 | 81 |
| 5 | 243 |
| 10 | 59,049 |

下面的图把同一组数字重新放到坐标位置上看。即使每个阶段都固定只有 3 个选择，候选组合也不是沿直线一点点增加，而是随着阶段增加迅速向上弯起。

![每阶段有 3 个选择时，阶段数增加会让可能组合数迅速变大的图](/AiBook/assets/part-01/chapter-07/search-space-growth-zh.png)

这里最重要的直觉是：

> 即使每一步只多出少量选择，  
> 组合总数也会很快变得巨大。

这也是为什么“那就全部看一遍不就好了？”很快会变得困难。

## 为什么完全搜索会变难

`exhaustive search` 指的是不遗漏地检查所有可能情况。对于很小的问题，它可以是很好的基准。但候选一多，时间和内存都会迅速不够。

想一想这些问题：

| 问题 | 候选数为什么会变大 |
| --- | --- |
| 配送路线 | 访问站点的顺序非常多 |
| 会议排程 | 人员、时间段和会议室条件交织 |
| 象棋或围棋 | 每一步都会打开大量下一步选择 |
| 文档写作 | 目录、句子、例子、证据安排有很多候选 |
| 模型调参 | 模型种类、特征、超参数组合很多 |

Poole 和 Mackworth 也强调，问题求解的难点常常就在搜索本身。有些问题里，验证一个答案是不是正确并不难，但高效地找到那个答案却很难。

> 认出一个解可能很容易。  
> 但找到通向它的路径，仍然可能很难。

## 计算极限不只是“电脑太慢”

`computational limit` 并不只是硬件差或程序写得慢。如果问题结构让候选数增长得太快，那么即使计算机很快，也可能无法在现实时间里把所有情况都看完。

| 区分 | 含义 |
| --- | --- |
| 实现太慢 | 也许优化代码可以改善 |
| 数据太大 | 也许存储、传输或并行化可以缓解 |
| 搜索空间爆炸 | 候选本身增长得太快 |
| 目标标准复杂 | 连评估“什么更好”都变难 |

更快的 CPU、GPU、更大的内存和并行处理当然重要，但它们并不会消除所有搜索问题，因为问题规模可能比计算资源增长得更快。

> 更快的电脑能让我们看得更远，  
> 但不能让我们看见每一条路。

## 现代例子：AlphaDev 与 FunSearch

`search space` 和 `computational limit` 不是只存在于老教材里的词，它们在现代 AI 研究中仍然不断出现。

AlphaDev 是一个很直观的现代例子。它通过搜索汇编指令组合来发现更快的排序算法。DeepMind 用这样一句话描述它的难点：

> “enormous number of possible combinations of instructions”

这正好对应 7.1 的直觉：当可能组合太多时，把所有候选都检查一遍会变得不现实。

FunSearch 则展示了另一种情况。它并不是直接搜索最终答案，而是搜索能够产生答案的函数或程序：

> “functions written in computer code”

这说明搜索对象本身也可以变化。问题有时不是直接枚举答案，而是枚举会生成答案的程序或函数。

这里需要保持边界：

| 例子 | 本节拿来说明的意义 | 不应过度泛化的地方 |
| --- | --- | --- |
| AlphaDev | 搜索空间可能非常大，候选无法全部检查 | 不表示所有 AI 问题都等于用强化学习找算法 |
| FunSearch | 搜索对象可以从“答案本身”变成“产生答案的程序” | 不表示 LLM 只是把训练数据中的答案直接搜出来 |

## 搜索处理的是和概率不同的一类困难

第 6 章聚焦于不确定性和概率。搜索处理的是另一类困难。

| 困难 | 核心问题 | 代表方法 |
| --- | --- | --- |
| uncertainty | 我们不知道什么是真的 | 概率、证据更新、校准 |
| search space | 候选太多 | 搜索、剪枝、启发式 |
| learning | 人很难把所有判断标准都写出来 | 数据驱动模型 |

现实问题里，这三者当然可能同时出现。但在入门阶段，先把它们区分开会更安全：

> 不知道什么是真的，  
> 候选太多，  
> 以及必须学习判断标准，  
> 彼此相关，但并不是同一种困难。

## 用文档结构整理来类比

搜索问题并不只在找路和游戏里出现。整理文档结构时也会出现类似感觉。

| 元素 | 文档结构整理例子 |
| --- | --- |
| state | 当前的目录与小节排布 |
| action | 增加小节、调整顺序、补强证据、改写表述 |
| goal | 让读者容易跟上的结构 |
| cost | 读者混乱、证据不足、篇幅过长、写作时间 |
| constraint | 以证据为中心、保持小节边界、术语一致 |

可能的目录组合会非常多。由于不可能把所有候选都完整生成并比较，通常会先固定大的结构，再通过中心问题和范围约束缩小候选。

这并不是完整的搜索算法，但作为比喻，它很适合说明：为什么在候选数很大时，候选缩减会成为必须。

## 为什么下一步会需要启发式

一旦搜索空间太大，就不可能把所有候选都看完。接下来就会自然出现三个问题：

> 哪些候选应该先看？  
> 哪些候选可以尽早放弃？  
> 到哪里可以停下来，把当前答案视为“已经够好”？

这正是启发式要回答的问题。Poole 和 Mackworth 说明，搜索的困难加上人类能高效解决部分搜索问题这一事实，提示我们：计算机智能体也应当利用关于特殊情况的额外知识来引导搜索。他们把这种额外引导称为 `heuristic knowledge`。

所以，下一节会把启发式理解成：

> 它不保证唯一正确答案，  
> 但能减少搜索量的经验性标准。

## 检查清单

- 能把 `search` 说明成查看可能候选并寻找解的过程。
- 能用找路例子说明 `state`、`action`、`goal`、`path` 和 `cost`。
- 能说明搜索空间一旦变大，组合数会迅速增长。
- 能说明 `exhaustive search` 在小问题上可行，但在大问题上会碰到计算极限。
- 能区分 `uncertainty`、`search space` 和 `learning` 三类不同困难。
- 能说明搜索空间一旦变大，为什么会需要 `heuristic`。

## 来源与参考资料

- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed., Chapter 3 Searching for Solutions](https://artint.info/3e/html/ArtInt3e.Ch3.html){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-23.
- David L. Poole, Alan K. Mackworth, [3.1 Problem Solving as Search](https://artint.info/3e/html/ArtInt3e.Ch3.S1.html){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-23.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents](https://aima.cs.berkeley.edu/contents.html){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-06-22.
- Google DeepMind, Daniel J. Mankowitz and Andrea Michi, [AlphaDev discovers faster sorting algorithms](https://deepmind.google/discover/blog/alphadev-discovers-faster-sorting-algorithms/){: target="_blank" rel="noopener noreferrer" }, 2023-06-07, 确认日期：2026-06-23.
- Google DeepMind, Alhussein Fawzi and Bernardino Romera-Paredes, [FunSearch: Making new discoveries in mathematical sciences using Large Language Models](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/){: target="_blank" rel="noopener noreferrer" }, 2023-12-14, 确认日期：2026-06-23.
