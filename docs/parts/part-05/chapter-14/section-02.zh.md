# P5-14.2 并行处理与长上下文

Section ID: `P5-14.2`
Version: `v2026.07.18`

在 P5-14.1 里，我们把 Transformer 解释为 self-attention、feed-forward、residual connection、layer normalization 的组合。接下来还剩下一个问题。

为什么 Transformer 比 RNN 更适合并行处理，并且在长上下文（long context）问题上也显得像一个更强的转折点？

Transformer 更接近这样一种结构：它不是只按顺序逐个 token 传递状态，而是一次性计算 token 之间的关系，因此在并行处理和长上下文引用上都表现出明显优势。

当你需要重新快速对齐这种计算直觉时，最好一起回到英文概念词汇表里的 [Transformer](/AiBook/en/reference/concept-glossary/#transformer)、[self-attention](/AiBook/en/reference/concept-glossary/#self-attention)、[parallel processing](/AiBook/en/reference/concept-glossary/#parallel-processing) 条目。

## 本节范围

- RNN 和 Transformer 的计算流程为什么会给人不同感觉？
- 从并行处理角度看，为什么 Transformer 更有利？
- 在处理长上下文时，self-attention 提供了什么直观优势？
- 为什么这种差异会进一步连到大规模生成模型时代？

本节首先要收住的核心，是`Transformer 不是一个名字更好听的模型，而是一种把顺序传递改造成关系计算、同时抬高 GPU 并行处理与长上下文重参考能力的结构`。

KV cache 会在 P6-3.4 重新解释，sparse attention 与 long-context 会在 P6-3.5 再回收。也就是说，这里先收住的是：为什么`一次性计算 token 关系的结构`会比`顺序状态传递`更适合并行处理和远距离上下文重参考。

这里还有一个必须讲完的点。不能只留下`Transformer 更快`这种印象。读者需要在本节里真正理解：为什么`一次性计算 token 关系的结构`会比`顺序状态传递`更适合并行处理和远距离上下文重参考。像 residual、normalization 这种 block 内部部件说明属于上一节，这里只聚焦计算感觉的差异。

本节不是要把 `RNN vs Transformer` 完整做成数学比较，而是先理解它们在大结构上的差异。

## 本节目标

- 能解释 RNN 与 Transformer 的计算流程差异。
- 能说明为什么 Transformer 更适合并行处理。
- 能直观说明 self-attention 在长上下文引用上的优势。
- 能把这种差异和大规模生成模型训练连接起来。

## 本节的阅读顺序

本节先把 RNN 的顺序传递和 Transformer 的关系计算并排摆出来，然后说明这种差异如何延伸到并行处理和长上下文问题。

1. 先并排看 RNN 的顺序传递与 Transformer 的关系计算。
2. 然后理解为什么这种差异会直接连到 GPU 并行处理。
3. 接着确认：在长上下文里重新参考远处位置时，这两种结构的感觉有什么不同。
4. 最后整理：为什么这种结构差异会成为现代生成模型的基础。

## 为什么 Transformer 看起来不一样

Transformer 的 self-attention 让每个 token 都能同时参考同一序列里的其他 token。这种结构更容易把 token 之间的相关性当作一种偏矩阵式的计算来处理。

也就是说：

- 它不必再严格依赖一次只把状态传给下一个 token
- 而是更强调一次性计算 token 之间的关系

`RNN 是按顺序传递状态，而 Transformer 更像是在一次性计算 token 之间的关系。`

如果说 P5-14.1 讲的是`Transformer block 里面有什么`，那么这一节讲的就是`这种 block 结构怎样改变了真实计算方式和训练规模`。

## 为什么 RNN 会显得更强烈地顺序化

RNN 系列是一种这样的结构：每一步继承前一个状态，再产生下一个状态。所以它的计算感觉自然会变成下面这样。

- 看第一个 token，生成一个状态
- 带着这个状态看第二个 token
- 再把状态传给第三个 token

也就是说，它更像是一种把 token 一个一个往前推的流程。

关键点在于，RNN 是靠把前面生成的状态不断传给后面位置来继续计算的。

`RNN 是一种把前面生成的状态不断往后传、按顺序推进计算的结构。`

## 为什么这对并行处理更有优势

正如 Part 5 前面已经看到的，GPU 最擅长的是同时处理大量相似计算。Transformer 的 self-attention 和大矩阵运算，正好和这种结构高度契合。

也就是说，Transformer：

- 更容易把 token 相关度计算打包成 tensor 运算
- 在 batch 级别也更容易扩展
- 并且展示出非常适合大规模并行训练的方向

核心点在于，Transformer 把 token 相关度计算重构成了并行矩阵运算，因此更适合大规模 GPU 训练。

`Transformer 之所以更适合大规模 GPU 训练，是因为它更容易把 token 之间的关系改写成并行矩阵运算。`

这里读者必须抓住的，不是`Transformer 多加了一个更聪明的规则`，而是`它把计算本身重构成了 GPU 更擅长的形式`。也就是说，本节的问题不是`block 里有什么部件`，而是`当这个 block 被重复时，为什么计算流会改变`。

如果把这个差异再压缩成入门层面的说法，可以先看下面这张表。

| 视角 | RNN 系列 | Transformer |
| --- | --- | --- |
| 计算流程 | 下一步需要前一步的结果 | token 关系更像一次性完成 |
| 与 GPU 的适配 | 顺序依赖很强 | 容易打包成大矩阵运算 |
| 远距离上下文引用 | 高度依赖状态传递 | 更直接地查看需要的位置 |

## 为什么它在长上下文里更有优势

在 RNN 里，如果非常远的信息要到达当前位置，就必须穿过很多中间步骤的状态传递。相比之下，在 self-attention 里，当前 token 可以更直接地参考远处 token。

也就是说，长上下文里的优势在于：远处信息不必只剩下一点淡淡地残留在中间状态里，而是能在当前位置被更直接地重新参考。

- 远处信息不必只作为模糊痕迹留在中间状态里
- 当前位置一旦需要，就能更直接地重新参考相关的前面位置

正因为如此，Transformer 在处理长上下文的问题上形成了很强的转折点。

也就是说，本节真正要读出的变化，是计算感觉从`模型必须长时间记住远处信息`，转向`模型现在可以把那条远处信息重新找回来`。

## 如果把它画得非常简单

```mermaid
--8<-- "assets/part-05/chapter-14/long-context-direct-reference-zh.mmd"
```

这张图同时象征了 RNN 式顺序传递的感觉，以及 self-attention 带来的更直接引用感觉。

如果把同一个长上下文请求再只按两条计算路径来比较，可以看成下面这样。

```mermaid
--8<-- "assets/part-05/chapter-14/sequential-vs-direct-baseline-zh.mmd"
```

从这张比较图里，首先要固定住的是下面几点。

- 顺序传递一侧必须把前面的规则一直装在中间状态里，带到最后的请求位置。
- 直接引用一侧则是让当前请求位置把自己需要的前面规则和状态行重新拉回来。
- 所以差异不只是结果上`重新看到了远处线索`，而是在`怎样到达那条线索的计算路径`上本身就不同。

## 案例与示例

下面这张图把本节的三个案例重新整理成`以顺序传递为中心的阅读`和`以直接引用为中心的阅读`之间的差异。

```mermaid
--8<-- "assets/part-05/chapter-14/long-context-task-flow-zh.mmd"
```

这张图说明：即使任务不同，核心问题其实很相似。它们都需要`把很靠前的线索重新带回当前位置`，而 Transformer 正是通过更直接的引用方式来处理这个问题。

如果把同一个问题拆成这两种计算感觉，差异会更直接。在这里，我们不仅要看`重新参考了什么`，还要看`当前这个位置在重新读这条线索时，到底是在一行一行顺着推进，还是在一次里同时处理多个位置之间的关系`。

| 同一场景 | 如果先按顺序传递思路去读，容易发生什么 | 如果先按直接引用思路去读，会先期待什么 |
| --- | --- | --- |
| 长工作许可问答 | 前面的禁止条件与例外条款，到了后面提问位置时可能已经模糊 | 当前回答位置会重新查找前面的线索，并修正安全判断 |
| 长交接班风险判断 | 很容易丢掉最早的警报和中段检查依据，只剩最后状态报告 | 当前判断位置会把需要的前面日志和中段检查依据重新带回来 |
| 长配置文件审查 | 容易只看当前行附近，漏掉更前面的定义和限制规则 | 当前行会重新参考前面的定义与约束，从而保持配置一致性 |

### 代表案例：长工作许可问答

想象一种情况：读完一份很长的工作许可文档后，最后一行再次问你：`现在可以批准 3 号线重启吗？` 文档前面其实已经写过`在确认压力释放之前不得开始重启`、`在 interlock 解除之前不得打开阀门`之类的条件，但到了提问位置，人很容易只想回看最后几行就给出回答。如果是顺序传递结构，这些条件必须一路从前面带到后面，所以文档越长，核心的禁止重启条件就越可能被削弱。相比之下，Transformer 系列允许当前位置重新直接参考文档开头的禁止条件和例外条款，因此`现在必须回答的位置`和`前面的规则位置`可以被更自然地重新连起来。这里并行计算的感觉也很重要。因为 token 关系会通过大矩阵运算一起处理，所以提问位置不用按顺序一条一条去摸索前面条件，而更容易一次把多个相关位置一起拉进计算里。

所以，这个案例里要确认的结果是：当前回答位置有没有只跟着上一句走，而是确实重新参考了前面的禁止条件和例外条款，从而更安全地判断是否批准重启。

同样的视角也会直接延伸到长交接班风险判断和长配置文件审查。不过，本节真正要抓住的核心不是领域名称，而是`当前位置会不会直接重新参考前面很远的线索，并把这种比较放进并行关系计算里一起处理`。

| 人容易先看到的标准 | 从并行处理与直接重参考视角重新阅读时的标准 |
| --- | --- |
| 容易觉得前面读过的信息只要留在状态里就够了 | 中间上下文越长，单个状态越可能变弱，所以当前位置必须把需要的前面线索重新找回来 |
| 只听到 Transformer 更快，容易觉得只是新模型更强 | 关键在于它把计算从`顺序传递`换成了`关系计算`，同时抬高了 GPU 并行处理和长上下文重参考 |
| 容易觉得长上下文问题只要把内存做大就能解决 | 实际上，只有存在把远处线索重新带回当前位置的结构，解释稳定性才会提高 |

读完这三个案例后，只要能重新说出下面三句话就够了。`如果远处线索只留在状态里，它可能在中途变模糊。若当前位置能重新参考自己需要的前面线索，解释会更稳定。Transformer 正是把这种重参考和并行计算一起抬高的结构。`

也就是说，本节的收尾不是`以后还会再看 long context`。读者应该已经能在当前这一节里说清楚：`只把远处线索留在状态里`和`让当前位置重新直接参考这些线索`之间到底有什么不同。下一 Part 只需要继续讲这种结构如何真正用于生成模型正文即可。

如果在这里停一下，短暂固定住`什么时候应该先想起并行处理和长上下文计算的感觉，而不是 block 内部部件说明`，Part 5 后半段的结构转折会更清楚。

| 先想到的问题 | 为什么要先从并行处理与长上下文视角来读 | 后续 Part 会继续什么 |
| --- | --- | --- |
| 为什么 Transformer 会和 GPU 时代的大规模训练强烈绑定在一起？ | 因为 token 关系计算很容易打包成大矩阵运算并并行处理 | 生成模型的规模扩展与推理成本 |
| 为什么重新读远处线索的感觉会变得重要？ | 因为在长上下文里，让当前位置直接参考所需线索，比只依赖顺序状态传递更自然 | long-context 运用、KV cache、上下文管理 |
| 为什么它和 RNN 的对比不只是旧模型 vs 新模型？ | 因为计算流本身已经从`状态传递`换成了`关系计算` | 后续 LLM 结构与训练管线理解 |

## 练习与例子

这个例子的目标，是确认在长输入里，这两种方式看起来到底有什么差异：一种是`把前面的规则压缩进单个顺序状态里并一路带到后面`，另一种是`让当前问题重新直接查找自己需要的前面句子`。

在读例子前，先把本节真正要看的最小观察点固定下来，会更稳。

| 要确认的点 | 例子里直接要看的值 | 为什么重要 |
| --- | --- | --- |
| 顺序状态会在什么地方变弱 | `history`、`final_state`、`sequential_support` | 它能显示：当中段日志变长时，前面线索只靠一个状态往后传，会多快开始模糊 |
| 直接引用到底重新带回了什么 | `top_matches` | 它能让我们直接看到：当前请求重新把哪些前面句子当成依据 |
| 两种结构最终判断如何分叉 | `sequential_decision` 与 `direct_decision` | 它能显示：即使在同一上下文里，`状态传递`和`直接重参考`也可能给出不同结论 |

输入：

- 一个把前面规则句、中段运维日志、最后运维请求混在一起的长上下文
- 一个会逐渐忘掉规则线索的简单 sequential 状态
- 一个让最后问题重新找回相关前面句子的 direct reference 分数

输出：

- 读每一行时不断更新的 sequential 状态
- 到最后请求位置时的关键线索最小值
- 最后请求重新参考了哪些前面句子
- 两种方式各自给出的最终判断

问题场景：

- 在长上下文处理中，需要比较：只靠顺序状态是否够用，还是必须有能直接重新找回前面线索的结构

要确认的概念：

- Transformer 式直接引用在重新读取远处线索时可能会更强
- 把顺序状态和直接引用判断并排看，结构差异会更明显

在看代码之前，先猜一猜：顺序状态和直接重参考会在什么地方先开始分叉，会更有帮助。

| 比较点 | 在顺序状态里先预期到的结果 | 在直接重参考里先预期到的结果 |
| --- | --- | --- |
| `sequential_support` / `direct_decision` | 规则线索会随着中间日志逐渐变弱 | 到最后请求时，可以重新捞回自己需要的规则行和目标行 |
| `history` / `top_matches` | 会看到前面规则越往后越模糊的过程 | 和请求直接匹配的句子会重新升到最上层依据 |
| 最终判断 | 可能会模糊成 `uncertain` | 更可能直接维持成 `block_restart` |

这个例子里，读者真正要看到的差异还不止于此。面对同一个请求，顺序状态一侧应该更容易倾向于`规则抓不牢，只能先保留或人工复核`，而直接重参考一侧则更容易倾向于`把前面规则和目标信息重新接上，立即阻断`。也就是说，计算差异最终必须连到`模型会选择什么下一步行动`。

输入：

这里使用前面整理的上下文行列表 `context`。

```python
# 这个例子比较重启请求需要重新连接前面压力规则时，sequential state decay 和 direct rereference 的差异。
context = [
    "Rule: unstable pressure state must not be restarted.",
    "Log: sensor calibration completed for line 3.",
    "Log: packaging material restocked this morning.",
    "State: pressure has not fully returned to safe range.",
    "Log: operator schedule updated for tomorrow.",
    "Request: restart line 3 now.",
]

def sequential_reader(lines, decay=0.55):
    state = {"pressure_risk": 0.0, "restart": 0.0, "block": 0.0}
    history = []
    for idx, line in enumerate(lines, start=1):
        lowered = line.lower()
        for key in state:
            state[key] *= decay
        if "pressure" in lowered or "unstable" in lowered:
            state["pressure_risk"] += 1.0
        if "restart" in lowered:
            state["restart"] += 1.0
        if "must not" in lowered:
            state["block"] += 1.0
        snapshot = {key: round(value, 3) for key, value in state.items()}
        history.append((idx, line, snapshot))
    support = round(min(state.values()), 3)
    decision = "block_restart" if support >= 0.8 else "uncertain"
    return history, {key: round(value, 3) for key, value in state.items()}, support, decision

def direct_reference_reader(lines):
    request = lines[-1].lower()
    keywords = {"restart", "pressure", "unstable", "must", "not"}
    scored = []
    for idx, line in enumerate(lines[:-1], start=1):
        words = set(line.lower().replace(".", "").replace(":", "").split())
        score = len(words & keywords)
        scored.append((score, idx, line))
    top_matches = sorted(scored, reverse=True)[:2]
    matched_lines = [line.lower() for _, _, line in top_matches]
    decision = (
        "block_restart"
        if any("must not be restarted" in line for line in matched_lines)
        and any("pressure" in line or "unstable" in line for line in matched_lines)
        and "restart" in request
        else "allow"
    )
    return top_matches, decision

history, final_state, sequential_support, sequential_decision = sequential_reader(context)
top_matches, direct_decision = direct_reference_reader(context)

print("[sequential reader]")
for idx, line, snapshot in history:
    print(f"{idx}. {line}")
    print("   state =", snapshot)
print("final_state =", final_state)
print("sequential_support =", sequential_support)
print("sequential_decision =", sequential_decision)
print()

print("[direct reference reader]")
for score, idx, line in top_matches:
    print(f"matched line {idx} (score={score}): {line}")
print("direct_decision =", direct_decision)
```

在输出里，可以先看 `sequential_support` 变弱了多少，以及 `direct_decision` 是怎样被维持住的。

```text
[sequential reader]
1. Rule: unstable pressure state must not be restarted.
   state = {'pressure_risk': 1.0, 'restart': 1.0, 'block': 1.0}
2. Log: sensor calibration completed for line 3.
   state = {'pressure_risk': 0.55, 'restart': 0.55, 'block': 0.55}
3. Log: packaging material restocked this morning.
   state = {'pressure_risk': 0.303, 'restart': 0.303, 'block': 0.303}
4. State: pressure has not fully returned to safe range.
   state = {'pressure_risk': 1.166, 'restart': 0.166, 'block': 0.166}
5. Log: operator schedule updated for tomorrow.
   state = {'pressure_risk': 0.642, 'restart': 0.092, 'block': 0.092}
6. Request: restart line 3 now.
   state = {'pressure_risk': 0.353, 'restart': 1.05, 'block': 0.05}
final_state = {'pressure_risk': 0.353, 'restart': 1.05, 'block': 0.05}
sequential_support = 0.05
sequential_decision = uncertain

[direct reference reader]
matched line 1 (score=4): Rule: unstable pressure state must not be restarted.
matched line 4 (score=2): State: pressure has not fully returned to safe range.
direct_decision = block_restart
```

第一个结果，是顺序状态在穿过上下文时怎样逐渐减弱。`block` 这一轴在规则行时很强，但到了最后请求位置时，只剩下 `0.05`。

![顺序状态衰减](/AiBook/assets/part-05/chapter-14/sequential-state-decay-zh.png)

第二个结果，是直接重参考方法在最后请求点到底把哪些行重新拉了回来。因为规则行和压力状态行重新升成高依据，所以这个例子真正要读出的变化，不只是两个决策名字不同，而是前面的线索到底是`在状态里变弱了`，还是`在当前请求点被重新调用回来了`。

![直接重参考匹配分数](/AiBook/assets/part-05/chapter-14/direct-reference-match-scores-zh.png)

| 先看的输出 | 这个输出表示什么 | 如果改动它，会看到什么变化 |
| --- | --- | --- |
| `sequential_support` 与 `direct_decision` 的差异 | 说明只靠状态压缩会让前面规则减弱，而直接引用会把需要的句子重新带回来 | 如果改 `decay` 或增加中间日志数量，顺序压缩的弱化会更直观 |

| 运维判断标准 | 只看顺序状态输出时容易做出的判断 | 读完直接重参考输出后会改变的判断 |
| --- | --- | --- |
| 压力尚未回到安全范围时的重启请求处理 | 因为是 `uncertain`，可能会只跟着最后请求推进重启，或需要人工重新翻规则文档 | 因为规则行和状态行重新浮现，`block_restart` 可以立刻成为优先动作 |
| 当日志变得很长时如何应对 | 中间日志越多，前面规则越容易变淡，`为什么要阻断`的依据也会跟着模糊 | 因为请求点能把需要的前面句子重新拉回来，即使日志很长，也能把阻断依据重新贴到当前判断上 |

- 先要把 `sequential_support = 0.05` 和 `direct_decision = block_restart` 一起看。只把前面规则压进状态的一侧，在最后请求点几乎已经失去了禁止依据；而重新参考所需句子的一侧，仍然会阻断同一个请求。
- 在 sequential 方式里，前面规则会在穿过中间日志时逐渐变弱，到最后请求位置已经无法同时强力保住 `pressure risk`、`restart`、`block` 这三个关键信号。
- `sequential_support` 表示在最后请求点，这三个关键信号中最弱的一轴还剩多少；这里可以确认 `block` 轴几乎已经消失。
- 在 direct reference 方式里，最后请求会立即重新找到前面的规则句和包含目标信息的句子。
- 在长上下文里，关键问题不是`模型是不是只读过一次前面的句子还能一直撑住`，而是`模型能不能在当前位置把自己需要的前面句子重新带回来`。

如果把这个结果翻译成运维现场判断，顺序一侧更接近`禁止出货或禁止重启的规则抓不到最后，只能靠人再去翻文档`，而直接引用一侧更接近`在处理当前请求时直接调用禁止依据，并立刻做出阻断判断`。本节真正要读出的结构差异，就是这种`调用依据方式的不同`。

这个输出不应该只停在简单对比上，而更适合继续问：接下来改动什么值，能把结构差异看得更清楚。

| 先出现的输出信号 | 现在马上可以尝试的变化 | 不应只凭这个例子就仓促下结论的事 |
| --- | --- | --- |
| `sequential_support` 很快缩小 | 继续降低 `decay` 或增加中间日志行数，观察顺序压缩会再摇晃多少 | 不要断言所有顺序模型都会失败 |
| `top_matches` 会重新拉回规则行和目标行 | 把规则句放得更远，或改变请求措辞，看看需要的句子是否仍会被重新找回 | 不要断言直接引用就自动保证完整理解 |
| `sequential_decision` 与 `direct_decision` 出现分叉 | 减少或增加规则线索数量，看看两种结构的判断会在什么条件下再次靠近 | 不要用这一个简单例子就推断真实 long-context 优化的全部性能 |

这个例子并没有实现完整的 RNN 和完整的 Transformer，但它确实让我们能动手实验：`把信息压缩进状态里保留`的感觉，和`把当前所需的前面位置重新拉回来`的感觉，到底有什么差别。只要改动 `decay` 数值或增加中间日志数量，就能直接看到为什么顺序压缩会变得更难。

## 如果从长上下文重参考角度重新读这个例子

前面的简单比较代码没有实现整个 Transformer，但比较基准已经很清楚。

- sequential 一侧展示的是`前面规则能不能被压缩进单个状态并长期存活`
- direct reference 一侧展示的是`当前请求一旦需要，前面规则和目标信息能不能被重新带回来`
- 所以最终分叉的不只是`记忆力好不好`这种印象，而是`当前位置能不能重新调用禁止依据并立即阻断`

也就是说，如果只把长上下文问题看成`记忆维持`，顺序状态的限制会先显现；如果把它看成`重新参考当前位置需要的前面位置`，Transformer 系列的优势就会更直接显现。只有先固定住这种感觉，后面再读长上下文限制时，才会自然理解成`把需要的上下文重新带回当前窗口再读`，而不是`它无条件记得更久`。

当 Transformer 把 attention 中心结构和并行计算优势结合起来以后，自然语言处理的基础计算结构发生了很大变化。此后，大规模预训练（pretraining）、长上下文处理，以及各种生成模型的扩展，都和这种结构转折紧密相关。

- 为什么 Transformer 不是又一个普通顺序模型
- 为什么 GPU 时代的大规模语言模型因此成为可能
- 为什么长上下文和大规模学习的标准会一起改变

会在同一节里被绑在一起，原因就在这里。

## 检查清单

- 能解释为什么 Transformer 比 RNN 更适合并行处理吗？
- 能说明 self-attention 在长上下文引用中的优势吗？
- 能解释 Transformer 不是只靠顺序状态传 token，而是更并行地计算关系吗？
- 能说明这种结构为什么和 GPU 并行处理很契合吗？
- 能解释 self-attention 会带来更直接参考远处位置的感觉吗？
- 能把 Transformer 的优势解释成`把计算流改造成 GPU 友好的关系计算`，而不是只说成`性能更好`吗？
- 能把长上下文问题解释成`当前位置重新查看所需前面线索`，而不是只说成`记得更久`吗？
- 在阅读后续 LLM 章节时，是否已经准备好先问`这种结构究竟让哪些计算变得可能`？

## 出处与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017，确认日期：2026-06-29。
- Colin Raffel et al., `Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer`, JMLR, 2020，确认日期：2026-06-29。
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016，确认日期：2026-06-29。[https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
