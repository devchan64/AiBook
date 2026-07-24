# P6-6.2 改变回答稳定性与多样性的输出选择规则

> Section ID: `P6-6.2`
> Version: `v2026.07.24`

在 P6-6.1 中，我们看过 LLM 的基本学习目标是 next-token prediction。可是用户体验看起来比 `预测下一个片段` 这句话复杂得多。

问题自然会接上。

那么实际生成按什么流程进行？用户看到的回答，是 `候选分布计算` 和 `候选选择` 多次接续后的结果。

next-token prediction 的基本含义已经抓成 `在当前上下文中计算下一个 token 分布`。这里集中看：从这个分布中实际怎样抽出 token，会如何改变回答的稳定性、多样性、可复现性。

## 输出选择规则会摇动什么

输出选择规则从下面的问题开始。

- 生成如何一个 token 一个 token 接续？
- 为什么同一个输入下结果也可能略有不同？
- temperature、sampling、greedy 选择会制造什么差异？

这里需要的不是再次展开 decoder 内部 attention 公式，而是读懂 `为什么候选的选择方式会改变结果`。即使候选分布相同，只要选择规则不同，用户看到的句子结构和摇动程度也会不同。

因此，核心不是 `模型知道答案`，而是 `候选中按什么规则选择什么，会改变结果`。本节处理的是计算概率分布后，实际选择哪个 token 的过程。beam search、top-p 等细节 decoding 公式比较先放到后面，这里先看 greedy、sampling、temperature 如何改变结果的稳定性和多样性。alignment、政策约束、外部工具连接等会进一步改变生成路径的问题，也在这里先分开。

核心直觉是：`生成是在概率分布中反复选择下一个 token 的过程`。

必须区分 `模型学到了什么` 和 `生成时如何从候选中选择`，才能更准确地阅读同一个回答的摇动。

## 概率分布与输出选择规则的区分

- 可以说明生成是反复选择过程。
- 可以区分 greedy 选择和 sampling。
- 可以说明 temperature 不是 `模型参数`，而是 `生成时改变选择倾向的设置值`。
- 可以说明为什么同一个问题也可能出现不同回答。

## 输出选择规则的判断标准

输出选择规则不是改变模型学到的内容，而是在已经计算出的候选分布中决定实际选择什么。因此，必须分开阅读下面标准。

| 判断标准 | 要确认的问题 |
| --- | --- |
| 反复结构 | 生成是否被说明为概率分布计算与候选选择的反复 |
| 选择方式 | greedy 和 sampling 在同一个分布中选择什么会不同 |
| 设置值的层位 | temperature 是否被说明为生成时改变选择倾向的值，而不是训练参数 |
| 使用目的 | 当前场景更先需要稳定性、多样性、还是可复现性 |

## 生成如何接续

把生成过程说得非常简单，就是反复执行下面顺序。

1. 查看到目前为止的 token
2. 计算下一个 token 候选的概率分布
3. 按某种规则选择一个
4. 把所选 token 接到后面
5. 直到结束条件为止反复执行

看这个过程，生成更接近 `每一步接着做下一个选择`，而不是 `拿出一篇预先完整写好的正确答案句子`。

## 为什么同一个问题也可能回答不同

模型通常不会绝对地只确定一个候选。多个候选都可能合理。

例如，在某个句子后面：

- `很好`
- `可以`
- `我会确认`

这样的候选都可能自然。

如果总是只选择最高候选，结果会更稳定，但表达可能变得单调。相反，如果从概率分布中 sampling，就可能出现更多样的结果，但不稳定性也会变大。

## greedy 和 sampling 有什么不同

最简单的比较如下。

| 方式 | 核心想法 |
| --- | --- |
| greedy | 每一步都选择概率最高的候选 |
| sampling | 反映概率分布来抽取候选 |

greedy 更可预测，sampling 更多样。

可以这样记。

`greedy 是选择最安全的一个点，sampling 是在合理候选之间按概率选择。`

## temperature 会改变什么

这个表达在 Part 1 中也曾小心处理过。许多用户会把 temperature 误解成 `改变模型内部的学习参数`。但在一般服务使用语境中，更安全的说明如下。

`temperature 是生成时调节候选概率分布要被读得多尖锐或多分散的设置值。`

也就是说：

- 低 temperature：更强地推高上位候选
- 高 temperature：低位候选也更常被选择

这个值通常不是改变 `已经学到的知识本身`，而是改变 `生成时的选择方式`。

## 哪种目的先适合哪种选择

生成设置与其说是 `无条件提高或降低 creativity 的按钮`，不如说是决定当前优先什么的选择。

| 场景 | 更先想要的东西 | 先想到的选择感觉 |
| --- | --- | --- |
| 客户支持草稿 | 一致性、政策遵守 | 低 temperature、保守选择 |
| 代码生成 | 可复现性、结构稳定性 | 低 temperature、接近 greedy 的选择 |
| 营销文案草稿 | 候选多样性、表达宽度 | sampling、略高 temperature |
| 头脑风暴 | 新组合、探索 | sampling 中心选择 |

也就是说，即使模型相同，也会因更先需要 `准确且不摇动的回答`，还是想要 `宽泛查看多个候选`，而改变生成设置的优先顺序。

## 选择规则改变的稳定性与多样性

把到这里为止的内容压到最短，如下。

- 学习处理 `把什么预测成下一个 token`。
- 生成处理 `从那些候选中实际抽出什么`。
- temperature、greedy、sampling 属于第二个问题。

这个区分先立住，才不会把 `模型知道什么` 和 `实际拿出了什么回答` 混在一起说明。

## 极简画出来

```mermaid
--8<-- "assets/part-06/chapter-06/p6-c06-s02-decoding-loop-zh.mmd"
```

这个图示的核心是：生成是 `概率分布计算` 和 `选择规则` 的结合。

## 案例与示例

下面的图示不是按 `随机选择`，而是按 `为了什么目的，要多保守或多多样地选择` 这个共同问题，重新捆起本节的三个案例。

```mermaid
--8<-- "assets/part-06/chapter-06/p6-c06-s02-selection-criteria-zh.mmd"
```

这个图示中要确认的是，生成设置并不是一个 `创意按钮`。即使模型相同，客户回应、营销文案、代码生成等目的不同，`稳定性`、`多样性`、`可复现性` 的优先顺序也会不同，因此阅读 greedy、sampling、temperature 的标准也会随之改变。

### 案例 1. 客户回应草稿

可以想象自动制作客户支持草稿的场景。人在这个场景中通常首先以 `是否出现符合政策的稳定句子` 为标准。

例如，面对退款咨询，一个回答先道歉，另一个回答立刻说政策，即使内容都对，服务语气也会显得不一致。又比如，一个回答先说退款条件，另一个回答先长篇说明提交材料，客户可能会混淆下一步行动。

这时，如果 sampling 范围太宽，同一个问题下语气和引导顺序也容易摇动。相反，低 temperature 和保守选择规则，会更常维持类似 `政策说明 -> 必要材料 -> 下一步` 的引导流程。

所以，这个案例中要确认的结果是：同一个问题下语气和引导顺序是否不会大幅摇动。

在这个场景中，`多样表达` 不一定是优点。客户想要的不是多种风格的回答，而是在相同条件下，以相似结构和相同政策顺序获得引导的体验。也就是说，比起拓宽表达幅度，更应先检查 `政策句是否遗漏`、`下一行动是否总是在同一个位置出现`。

| 这个场景先看的内容 | 一旦摇动会出现的问题 |
| --- | --- |
| 道歉、政策说明、下一步的顺序 | 每个回答的引导流程不同，客户会混淆 |
| 相同条件下维持相似语气 | 咨询质量看起来忽高忽低 |
| 必要信息请求位置固定 | 订单号、收货日等下一行动不够显眼 |

### 案例 2. 营销文案草稿

营销文案草稿或创意头脑风暴就不同。人在这个阶段通常先看 `是否出现多个值得比较的候选`，而不是 `最安全的一句话`。如果总是收到同一表达，就会觉得候选范围太窄。

例如，请求三个方案时，如果全都以 `简单又快速` 开头，语法上可能没错，但团队很难比较方向。相反，如果强调点分成 `快速处理`、`安心配送`、`没有复杂流程的开始`，团队就有材料讨论哪个信息更合适。

这个场景中，比起总是只选择最高候选的保守选择，允许更多合理候选的 sampling 系列设置可能更合适。也就是说，重要变化是标准从寻找 `一句正确答案`，转为制作 `可比较的候选集合`。

所以，这个案例中要确认的结果是：是否真的出现多个强调点不同的候选。

这里反而可能是输出太稳定出了问题。如果所有方案都只用同一结构和词汇，团队就拿不到判断比较对象的材料。因此在这个场景中，更适合先看 `即使稍微不那么安全，是否出现不同角度候选`、`强调点是否真的分开`。

| 这个场景先看的内容 | 不足时会出现的问题 |
| --- | --- |
| 强调点不同的候选数量 | 没有可比较方案，只能反复检查一句话 |
| 不脱离品牌语气的多样性 | 候选增加了，但质量线可能崩塌 |
| 句子开头和核心信息的变体 | 所有文案都以相似表达开头，选择范围变窄 |

### 案例 3. 代码生成

代码生成中特别重要的是语法稳定性和可复现性。人在这里首先看的标准，不是 `每次略有不同的代码`，而是 `同一要求下是否用相似结构稳定回答`。

例如，同一个函数修改请求中，一次加入 `try/except`，下一次又省略它，比较和回归确认都会困难得多。第一次结果已经配好测试后，再生成时结构大幅改变，追踪生成变动的时间可能比追踪真实 bug 还多。

这时，如果 sampling 范围太宽，异常处理方式、变量结构、返回顺序都可能不必要地摇动。相反，更保守的设置会更常维持 `同一要求 -> 相似结构`，更容易建立调试基准线。

所以，这个案例中要确认的结果是：重复同一请求时，代码结构和异常处理方式是否不会大幅摇动。

把三个案例按 decoding 选择标准重新捆起，可以得到下表。

| 情况 | 越保守越好的内容 | 允许更多样候选时更好的内容 |
| --- | --- | --- |
| 客户回应草稿 | 语气一致性、引导顺序稳定性 | 几乎没有，摇动反而是问题 |
| 营销文案草稿 | 维持最低质量线 | 强调点不同的多个方案 |
| 代码生成 | 结构稳定性、可复现性 | 过度多样会增加调试成本 |

把三个案例合起来看，生成设置应读成 `允许结构摇动到什么程度` 的选择，而不是 `创意按钮`。

## 选择规则显露出来的场景

即使还不知道 beam search 或 top-p 这类细节公式，也可以先区分眼前场景是 `模型不知道` 的问题，还是 `从已有候选中抽出什么` 的问题。同一个咨询下回答语气和引导顺序每次都摇动时，不要立刻只看成知识不足，而要问：候选其实知道，但 sampling 范围或 temperature 是否让结构摇动变大了。营销方案太相似而没有比较材料时，比起说创意不足，应看是否需要允许更多样候选的选择规则。同一个代码修改请求中，每次异常处理方式不同，那么在增加知识之前，更保守的选择规则可能才是先需要的。

这里重要的不是机械背诵 `temperature 要升还是降`，而是先把 `学到了什么` 和 `实际从中抽出了什么` 读成不同问题。

这里经常混在一起的内容如下。

- 容易把模型知识不足和输出选择摇动捆成同一个原因。
- 容易用同一个评价标准看需要多样性的场景和需要一致性的场景。
- 容易把 temperature 感觉成 `改变模型内部的值`，而错过它实际上是改变输出选择倾向的设置值。

因此，`生成是从候选分布中决定实际抽出什么的过程` 这句话，应成为阅读实际服务场景的标准。

这个区分的目的不是一次确定原因。它是为了不把 `生成很奇怪` 压成一句话，而是短暂区分当前问题先显露在 `选择规则`、`候选多样性`、`结构摇动` 中的哪一处，而不是先归为 `知识不足`。

## 练习与示例

这个例子的目标，是直接看到 `greedy`、`sampling`、`temperature`、`seed` 如何改变从概率候选中选择下一个 token。这里不拿真实 LLM 内部巨大的词汇表，而是在每个位置放置 `下一个 token 候选` 和基础概率，一次抽取一个 token 来完成句子。因此，核心不是组合回答模板，而是 `当前位置实际选择了哪个候选片段`。

输入 CSV 是 [p6-6-2-next-token-candidates-zh.csv](/AiBook/assets/part-06/chapter-06/p6-6-2-next-token-candidates-zh.csv){ .csv-preview }。一行表示某个位置的一个候选 token。例如，1 号位置有 `退款`、`订单`、`确认`、`引导` 作为候选，6 号位置有 `7天`、`3天`、`14天`、`2个工作日` 这类时间表达候选。读者可以直接改动的值是 `base_probability`、`temperatures`、`seeds`。

要确认的核心有三点。

- greedy 在每个位置只选最高概率 token，因此输出固定。
- sampling 即使面对同一个候选分布，实际抽出的 token 也可能不同，因此产生输出多样性。
- 固定 seed 后可以重新做出同一 sampling 结果，因此可以确认可复现性。

不过，这里的 seed 可复现性，是在固定本地 Python 随机数生成器的例子中的可复现性。实际 API 服务中，即使使用同一 seed 和同一生成设置，也可能因模型提供环境、后端设置、系统指纹(system fingerprint) 等条件而不能保证完全决定性。本节关注的不是运营 API 的可复现性保证范围，而是固定或改变选择规则时，观测到的输出如何变化。

```python
# 比较从下一个 token 候选分布中实际抽出什么 token。
import csv
import random
from collections import Counter, defaultdict
from pathlib import Path

candidate_path = Path("docs/assets/part-06/chapter-06/p6-6-2-next-token-candidates-zh.csv")
temperatures = [0.3, 1.0, 1.7]
seeds = range(1, 13)

def load_candidates(path):
    candidates_by_step = defaultdict(list)
    with path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            row["step"] = int(row["step"])
            row["base_probability"] = float(row["base_probability"])
            candidates_by_step[row["step"]].append(row)
    return dict(sorted(candidates_by_step.items()))

def apply_temperature(candidates, temperature):
    adjusted = [
        row["base_probability"] ** (1.0 / temperature)
        for row in candidates
    ]
    total = sum(adjusted)
    return [value / total for value in adjusted]

def pick_top_token(candidates, probabilities):
    top_index = max(range(len(candidates)), key=lambda index: probabilities[index])
    return top_index, candidates[top_index]["candidate_token"]

def greedy_decode(candidates_by_step, temperature):
    tokens = []
    for candidates in candidates_by_step.values():
        probabilities = apply_temperature(candidates, temperature)
        _, token = pick_top_token(candidates, probabilities)
        tokens.append(token)
    return "".join(tokens)

def sample_decode(candidates_by_step, temperature, seed):
    rng = random.Random(seed)
    tokens = []
    top_hits = 0
    trace = []
    for step, candidates in candidates_by_step.items():
        probabilities = apply_temperature(candidates, temperature)
        top_index, top_token = pick_top_token(candidates, probabilities)
        picked_index = rng.choices(
            range(len(candidates)),
            weights=probabilities,
            k=1,
        )[0]
        picked_token = candidates[picked_index]["candidate_token"]
        if picked_index == top_index:
            top_hits += 1
        tokens.append(picked_token)
        trace.append({
            "step": step,
            "picked_token": picked_token,
            "top_token": top_token,
        })
    return "".join(tokens), top_hits, trace

candidates_by_step = load_candidates(candidate_path)
print("candidate_rows =", sum(len(rows) for rows in candidates_by_step.values()))
same_seed_output_1 = sample_decode(candidates_by_step, temperature=1.0, seed=7)[0]
same_seed_output_2 = sample_decode(candidates_by_step, temperature=1.0, seed=7)[0]
different_seed_output = sample_decode(candidates_by_step, temperature=1.0, seed=8)[0]

print("same_seed_reproducible =", same_seed_output_1 == same_seed_output_2)
print("same_seed_output =", same_seed_output_1)
print("different_seed_output =", different_seed_output)

print("\ngreedy outputs by temperature")
for temperature in temperatures:
    print(temperature, greedy_decode(candidates_by_step, temperature))

print("\nsampling summary")
token_positions = len(candidates_by_step)
for temperature in temperatures:
    greedy_output = greedy_decode(candidates_by_step, temperature)
    outputs = []
    top_hits = 0
    first_tokens = []
    for seed in seeds:
        output, hits, trace = sample_decode(candidates_by_step, temperature, seed)
        outputs.append(output)
        top_hits += hits
        first_tokens.append(trace[0]["picked_token"])
    print(
        "temperature =",
        temperature,
        "exact_greedy_matches =",
        f"{sum(output == greedy_output for output in outputs)}/{len(seeds)}",
        "unique_outputs =",
        len(set(outputs)),
        "top_token_rate =",
        round(top_hits / (len(seeds) * token_positions), 2),
    )

print("\nfirst token counts")
for temperature in temperatures:
    first_token_counter = Counter(
        sample_decode(candidates_by_step, temperature, seed)[2][0]["picked_token"]
        for seed in seeds
    )
    print("temperature =", temperature, dict(first_token_counter))

print("\nhigh temperature preview")
for seed in [1, 2, 3]:
    print("seed =", seed, sample_decode(candidates_by_step, temperature=1.7, seed=seed)[0])
```

这个例子已用本地 `.venv` 的 Python 执行，并确认与正文输出一致。

执行结果示例可以这样阅读。

```text
candidate_rows = 36
same_seed_reproducible = True
same_seed_output = 退款可以订单完成为准7天以内提交申请。
different_seed_output = 退款申请配送受理后7天之后办理需要订单号。

greedy outputs by temperature
0.3 退款可以配送完成后7天以内办理。
1.0 退款可以配送完成后7天以内办理。
1.7 退款可以配送完成后7天以内办理。

sampling summary
temperature = 0.3 exact_greedy_matches = 3/12 unique_outputs = 8 top_token_rate = 0.88
temperature = 1.0 exact_greedy_matches = 0/12 unique_outputs = 12 top_token_rate = 0.48
temperature = 1.7 exact_greedy_matches = 0/12 unique_outputs = 12 top_token_rate = 0.37

first token counts
temperature = 0.3 {'退款': 11, '订单': 1}
temperature = 1.0 {'退款': 8, '引导': 1, '订单': 2, '确认': 1}
temperature = 1.7 {'退款': 5, '引导': 1, '订单': 5, '确认': 1}

high temperature preview
seed = 1 退款资格客户完成为准3天为止需要确认。
seed = 2 引导申请配送完成时点14天为止办理需要订单号。
seed = 3 退款相关咨询配送状态为准7天以内需要确认。
```

先压缩长执行结果，可以得到下表。第一张表展示 greedy 为什么在 temperature 变化时也可能固定。

| temperature | greedy 输出 | 应读取的含义 |
| --- | --- | --- |
| 0.3 | `退款可以配送完成后7天以内办理。` | 每个位置只选第 1 位 token，因此输出固定 |
| 1.0 | `退款可以配送完成后7天以内办理。` | 即使按原始概率分布阅读，第 1 位顺序也不变 |
| 1.7 | `退款可以配送完成后7天以内办理。` | 分布更分散时，greedy 仍然只选第 1 位 token |

这个表中重要的是 greedy 为什么看起来 `稳定`。这不是因为模型更聪明，而是因为实际选择规则在每个位置只选第 1 位 token。

第二张表是按预设 seed 列表反复 sampling 12 次的结果。这里看的不是句子质量，而是 `上位 token 维持得多频繁`、`出现多少个不同输出`、`同一 seed 是否能重新做出同一结果`。

| temperature | 与 greedy 完全相同的输出 | 不同输出数 | 上位 token 选择比例 | 应读取的含义 |
| --- | ---: | ---: | ---: | --- |
| 0.3 | 3/12 | 8 | 0.88 | 低 temperature 下，上位 token 维持更强，因此相对稳定 |
| 1.0 | 0/12 | 12 | 0.48 | 即使是基础分布，sampling 也可能每次抽出不同 token |
| 1.7 | 0/12 | 12 | 0.37 | 高 temperature 下，低位候选更常被选中，选择范围变宽 |

这些数字并不表示 `提高 temperature 就会得到好回答`。在这次运行中，从 0.3 到 1.0 时不同输出数大幅增加；到 1.7 时，比起输出数量，上位 token 选择比例下降和第一 token 分布扩张更明显。在客户支持或代码生成这类稳定性重要的场景中，这种多样性可能表现为摇动；在草稿生成这类需要候选宽度的场景中，它可能成为比较材料。

这个例子中要读的核心如下。

- greedy 在三种情况下都生成同一个 token 序列。
- sampling 即使面对同一候选分布，也会改变实际抽出的 token 序列。
- 低 temperature 下第 1 位 token 选择比例更高，稳定性更强；高 temperature 下从第一 token 开始分布变宽，选择范围变大。
- `same_seed_output` 和 `different_seed_output` 的差异显示，即使使用 sampling，固定 seed 也可以重新做出同一输出；seed 改变时，同一设置下也可能出现不同 token 序列。
- 也就是说，temperature 与其说是 `增加随机性的按钮`，不如说是通过调节 `下一个 token 候选分布要压着看还是展开看`，改变稳定性、多样性、可复现性平衡的设置值。

把这个变化画成图，会如下所示。左侧显示所有 token 位置中上位候选维持得多频繁，中间显示不同输出数在哪个设置上饱和，右侧显示第一 token 分布如何变宽。这个图不表示回答质量提高，而应读成同一候选分布中实际 token 选择范围变宽。

![按 temperature 区分的 token 选择稳定性与输出多样性](/AiBook/assets/part-06/chapter-06/temperature-unique-reply-count-zh.png)

正文代码中，读者可以直接修改 CSV 的 `base_probability`、`temperatures`、`seeds`。例如，如果降低 6 号位置 `7天` 的概率、提高 `14天` 的概率，greedy 输出本身也可能改变。把 `temperature` 改成 0.2 或 2.0，上位 token 固定程度和第一 token 分布也会更极端地移动。增加 `seeds`，则能更清楚地看到同一设置下输出会多样到什么程度。

## temperature 改变的选择宽度

下面这种比喻有用。

- 低 temperature：`几乎只选择最有力的候选`
- 高 temperature：`不那么有力的候选也会相当频繁地被考虑`

不过，这个比喻也不是全部。实际实现中，概率分布的形状本身会被调节。因此，仅说 `temperature 是 randomness 按钮` 仍然不足。

## 选择规则制造的输出差异

这个例子中重要的，不只是存在候选概率，而是从该分布中 `如何选择` 会改变实际用户体验。同一模型中，是保守抽取，还是允许更多样候选，会改变回应的稳定性、创意性、可复现性，因此后续设置讨论都建立在这个选择规则视角之上。

要把语言模型理解成实际用户工具，就需要养成习惯，把 `学到了什么` 和 `如何用该学习结果抽出实际输出` 分开看。

- 学习目标：next-token prediction
- 生成过程：从候选分布中反复选择实际 token

有了这个区分，后续的：

- prompting
- decoding 设置
- hallucination 检查
- evaluation

才能被分成不同问题。

如果把这个例子重新压缩成判断标准，下面三个问题应该先浮现出来。

| 场景 | 要先回答的问题 |
| --- | --- |
| 为什么同一个问题下回答也略有不同 | 候选分布相似，但实际选择规则是否在变化 |
| 为什么客户回应和代码生成中摇动更是问题 | 这个任务是否比多样性更先需要一致性和可复现性 |
| 为什么营销文案草稿中回答太相似反而是问题 | 是否需要允许更宽候选的选择规则 |

## 检查清单

- 能否把 `学到了什么` 和 `实际抽出了什么` 分开说明？
- 能否从稳定性、多样性、可复现性角度区分 greedy、sampling、temperature？
- 读后续章节时，是否准备好不把模型知识和输出选择规则混在一起？

## 来源与参考资料

- Tom B. Brown et al., `Language Models are Few-Shot Learners`, arXiv, 2020, 确认日期：2026-07-19. [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }
- Ari Holtzman et al., `The Curious Case of Neural Text Degeneration`, ICLR, 2020, 确认日期：2026-07-19. [https://iclr.cc/virtual_2020/poster_rygGQyrFvH.html](https://iclr.cc/virtual_2020/poster_rygGQyrFvH.html){: target="_blank" rel="noopener noreferrer" }
- OpenAI API Reference, `Create a model response`, 生成设置示例，确认日期：2026-07-19. [https://developers.openai.com/api/reference/resources/responses/methods/create](https://developers.openai.com/api/reference/resources/responses/methods/create){: target="_blank" rel="noopener noreferrer" }
- Clara Meister et al., `Language Model Behavior: A Comprehensive Survey`, Computational Linguistics, 2024, 确认日期：2026-07-24. [https://direct.mit.edu/coli/article/50/1/293/118131/Language-Model-Behavior-A-Comprehensive-Survey](https://direct.mit.edu/coli/article/50/1/293/118131/Language-Model-Behavior-A-Comprehensive-Survey){: target="_blank" rel="noopener noreferrer" }. 用于确认 autoregressive language model 会计算下一个 token 概率分布，并在 open-ended generation 中使用 greedy、temperature sampling、top-k、nucleus sampling 等选择方式。
- OpenAI Help Center, `Best practices for prompt engineering with the OpenAI API`, 确认日期：2026-07-24. [https://help.openai.com/en/articles/6654000-how-to-prompt-the-models](https://help.openai.com/en/articles/6654000-how-to-prompt-the-models){: target="_blank" rel="noopener noreferrer" }. 用于确认 temperature 与低概率 token 选择频率、随机性、事实性 use case 中的保守设置有关。
- OpenAI Cookbook, `How to make your completions outputs consistent with the seed parameter`, 确认日期：2026-07-24. [https://developers.openai.com/cookbook/examples/reproducible_outputs_with_the_seed_parameter](https://developers.openai.com/cookbook/examples/reproducible_outputs_with_the_seed_parameter){: target="_blank" rel="noopener noreferrer" }. 用于确认 seed 是在同一设置下获得大体一致输出的装置，但并不保证完全决定性。
