# P5-14.5 长上下文中顺序状态和直接重参考怎样分开？

> Section ID: `P5-14.5`
> Version: `v2026.07.26`

在 P5-14.4 中，我们看到了 RNN 的顺序状态传递和 Transformer 的关系计算，从并行处理角度有什么不同。P5-14.5 的观察点不是 GPU 效率，而是在长上下文(long context)中，最后判断以什么方式把前面的线索重新接为依据。

长上下文中重要的是长期记住，还是重新参考需要的前面位置？

比较对象不是完整 Transformer 实现，而是长上下文中`把前面规则压缩到一个状态里带着走的方式`和`当前问题重新寻找自己需要的前面句子的方式`。并行处理的计算效率已经在 P5-14.4 中收住，这里只看远处线索重新接到最终判断上的路径。

## 长上下文重参考和实验处理的问题

- 长上下文中，顺序状态传递为什么可能变弱？
- self-attention 为什么会给人更直接参考远处前面位置的感觉？
- 顺序状态方式和直接重参考方式，为什么在同一个长上下文中也可能做出不同最终判断？

## 比较顺序传递和直接重参考

在 RNN 中，远处信息要到达当前点，必须经过多个 step 的状态传递。相比之下，在 self-attention 中，前面的线索不只需要被压缩到一个状态里一路带过来，当前位置还可以重新计算自己和前面位置之间的关系分数。因此，相距很远的线索也会被读成能在当前判断位置被更直接地参考。

这里的关系分数，是最后请求位置和前面线索重新比较后得到的相关度。最后请求位置会用同样方式重新比较前面的规则行、当前状态行和无关日志行。其中和当前请求强烈连接的行会重新浮为判断依据，关系弱的行则会被推到后面。

例如最后问题是`现在可以重启 3 号线吗？`，那么问题位置就需要重新比较前面的`不得重启`规则，以及`压力尚未回到安全范围`这个状态。完成这种比较后，长上下文开头的线索就不是单纯被长期记住，而是在最后判断时重新接成依据。

先看整体概念路径，可以整理如下。前面的线索可以在顺序状态里被压缩后移动，也可以在当前问题位置被重新比较。

```mermaid
--8<-- "assets/part-05/chapter-14/long-context-direct-reference-zh.mmd"
```

接着把同一个请求只按两条计算路径分开看，可以这样比较。这个图不是再次展示整个长上下文结构，而是比较最后请求通过哪条依据路径到达判断。

```mermaid
--8<-- "assets/part-05/chapter-14/sequential-vs-direct-baseline-zh.mmd"
```

| 视角 | 顺序状态传递 | 直接重参考 |
| --- | --- | --- |
| 前面线索移动 | 经过中间状态传递 | 当前位置重新看所需的前面位置 |
| 长上下文风险 | 中间信息越长，线索越可能变弱 | 更可能把相关前面位置重新拉上来 |
| 最后判断 | 依赖状态里剩下的线索强度 | 依赖当前请求和前面依据的关系计算 |

如果只把长上下文问题读成`记忆力`，就只会看模型是否把前面内容长期抓住。但在 Transformer 结构中，更重要的感觉是当前位置能否重新参考自己需要的前面位置。

## 案例与示例

### 案例：压力未恢复状态下的重启请求

看一个较长的工作许可问答。

| 候选线索 | 与最后判断的关系 | 直接重参考视角 |
| --- | --- | --- |
| `压力解除前，不得重启 3 号线` | 重启阻断规则 | 必须重新调用的前面线索 |
| `当前压力尚未回到安全范围` | 规则现在仍适用的状态 | 必须重新调用的前面线索 |
| `传感器校准已在上午完成` | 不表示压力已回到安全范围 | 可能混淆的弱线索 |
| `交接班记录已更新` | 与重启安全判断直接关系弱 | 应从判断中心推开的线索 |
| `现在可以批准 3 号线重启吗？` | 当前问题 | 必须重新接上前面规则和状态的位置 |

人最容易先用的标准是`文档读了很多，所以应该记得前面内容`。但这个案例要确认的结果不是`记住了很多吗`，而是最后判断时是否把禁止规则和当前压力状态重新接为依据。

顺序状态方式试图把前面规则压缩成一个状态并带到最后。中间日志变多时，禁止规则轴可能变弱。直接重参考方式则在最后请求时重新找回规则行和压力状态行。

压缩到一个状态里，并不是说前面的线索会消失。只是每读一行，状态里也会继续混入传感器校准、包装材料补充、交接班记录等其他信息。到达最后请求时，如果禁止规则没有作为单独依据清楚地留下来，模型就可能比起`不得重启`，更容易被最近的日志或“批准”这类词带偏。

这个案例的判断句应该这样收束。

| 方式 | 判断句 |
| --- | --- |
| 只剩下较弱的顺序状态 | 前面的禁止规则可能没有足够强地留到最后请求，因此判断可能变得不确定 |
| 直接重参考找到了所需线索 | 最后请求把禁止规则和当前压力状态重新接为依据，因此判断会偏向阻断重启 |

## 练习与例子

### 练习：区分需要的前面线索和干扰线索

请把下面候选线索分成`需要`、`弱`、`接近干扰`。

| 候选线索 | 分类 | 解说 |
| --- | --- | --- |
| `压力解除前，不得重启 3 号线` | 需要 | 这是直接阻止最后重启批准问题的规则。 |
| `当前压力尚未回到安全范围` | 需要 | 它确认禁止规则现在是否仍然适用。 |
| `传感器校准已在上午完成` | 弱 | 传感器校准不等于压力回到安全范围。 |
| `包装材料补充作业已另行批准` | 接近干扰 | 即使有“批准”这个词，也和 3 号线重启批准的直接关系较弱。 |

解说：长上下文问题的学习点不是`读了很多`，而是`把最后判断所需依据重新接上`。不仅要选出需要的线索，也要把直接关系弱的线索从判断中心推开。

### 例子：比较 sequential reader 和 direct reference reader

这个例子不是 Transformer 实现，而是比较两种参考方式在长上下文判断中留下什么观察值。`direct_reference_reader` 不是实际 attention 计算，而是用关键词分数重新排列前面行的压缩模型。这里要确认的不是代码是否命中预先定好的答案，而是`状态里变弱的线索`和`当前请求中重新浮上来的线索`在输出上的差异。

| 要操作的值 | 要观察的输出 | 要确认的问题 |
| --- | --- | --- |
| `decay` | `sequential_support`, `final_state` | 前面规则在顺序状态里多快变弱？ |
| 中间 `Log:` 行数 | `block` 轴的最后值 | 不相关的中间句子越多，顺序状态是否越容易摇晃？ |
| 最后 `Request:` 句子 | 上位 matched line, score | 当前请求和哪些前面行的词语轴重叠更强？ |

```python
# 这个例子比较长上下文中顺序状态变弱的过程，以及 direct reference 重新找到前面规则的过程。
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
    return history, {key: round(value, 3) for key, value in state.items()}, support

def direct_reference_reader(lines):
    request = lines[-1].lower()
    keywords = set(request.replace(".", "").replace(":", "").split())
    keywords |= {"pressure", "unstable", "must", "not"}
    scored = []
    for idx, line in enumerate(lines[:-1], start=1):
        words = set(line.lower().replace(".", "").replace(":", "").split())
        score = len(words & keywords)
        scored.append((score, idx, line))
    top_matches = sorted(scored, reverse=True)[:2]
    return top_matches

history, final_state, sequential_support = sequential_reader(context)
top_matches = direct_reference_reader(context)

print("[sequential reader]")
for idx, line, snapshot in history:
    print(f"{idx}. {line}")
    print("   state =", snapshot)
print("final_state =", final_state)
print("sequential_support =", sequential_support)
print()

print("[direct reference reader]")
for score, idx, line in top_matches:
    print(f"matched line {idx} (score={score}): {line}")
```

输出示例可以这样读。

```text
final_state = {'pressure_risk': 0.353, 'restart': 1.05, 'block': 0.05}
sequential_support = 0.05

matched line 1 (score=4): Rule: unstable pressure state must not be restarted.
matched line 4 (score=2): State: pressure has not fully returned to safe range.
```

第一个产物展示顺序状态怎样穿过上下文而变弱。`block` 轴在规则行很强，但经过中间日志后，到最后请求时只剩下 `0.05`。

![顺序状态弱化](/AiBook/assets/part-05/chapter-14/sequential-state-decay-zh.png)

第二个产物展示直接重参考方式在最后请求时重新拉回哪些行。这段代码并不判定`应该阻止重启`这个固定答案，而是比较最后请求的词语轴和前面行的词语轴，观察规则行和压力状态行是否重新浮为上位依据。这个例子要读出的变化不是决策标签，而是前面线索是在`状态里变弱`，还是在`和当前请求的比较中重新浮上来`。

![直接重参考分数](/AiBook/assets/part-05/chapter-14/direct-reference-match-scores-zh.png)

### 练习：改变数值确认差异

| 要改变的值 | 预期输出变化 | 解说 |
| --- | --- | --- |
| 把 `decay` 从 `0.55` 提高到 `0.8` | `sequential_support` 可能变大 | 顺序状态会更久保留前面线索，因此规则行产生的 `block` 轴到最后请求时弱化得更少。 |
| 再增加 3 行中间日志 | 顺序状态一侧更容易摇晃 | 中间行越多，状态里的前面线索会继续衰减；但直接重参考只要能找到关键词匹配的前面行，就可能保持判断。 |
| 从最后请求中去掉 `restart` 一词 | 上位 matched line 的排序可能改变 | 如果当前请求缺少连接前面规则的核心词，直接重参考一侧也会改变哪些前面线索更强地浮上来。 |

解说：这个练习不是说直接重参考总能保证正确答案。核心是通过输出变化区分，长上下文中的前面线索是在`状态里变弱`，还是在`和当前请求的比较中重新浮上来`。

## 检查清单

- 能把长上下文问题解释成顺序状态传递和直接重参考的差异吗？
- 能说明 self-attention 给人更直接参考远处位置的感觉吗？
- 能解释 `sequential_support` 和上位 matched line 的差异吗？
- 能说明长上下文中最终判断可能随依据调用方式而改变吗？

## 来源与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 确认日期：2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016，确认日期：2026-06-29。[https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
