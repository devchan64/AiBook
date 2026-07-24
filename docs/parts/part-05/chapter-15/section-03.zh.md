# P5-15.3 采样（sampling）怎样从候选分布中取出实际输出

> Section ID: `P5-15.3`
> Version: `v2026.07.24`

在 P5-15.2 中，我们已经看到：生成模型（generative model）不是背下一个正确答案再取出来，而是把可能输出候选的相对可信度保留成候选分布。接下来就会自然出现一个问题。

如果生成模型能给出多个可信答案，那它实际会选出哪一个？

sampling 是模型从多个它认为可信的候选里，一次取出一个实际输出的过程，而这种方式会直接影响结果的多样性与稳定性。

当你需要重新区分“模型分数”和“实际输出选择”时，可以回到概念词汇表里的 [sampling](/AiBook/reference/concept-glossary/#sampling) 条目。

## 候选分布和实际输出选择不同

本节首先要抓住的核心，是`生成模型的质量，不只取决于它学到了什么，还非常取决于它实际取出了哪些候选`。如果说 P5-15.2 看的是模型怎样保留候选之间的相对可信度，那么 P5-15.3 看的是：在这些已经算出来的候选里，实际输出是按什么步骤被取出来的。

| 这一节现在要读的内容 | 后面 Part 里会继续读的内容 |
| --- | --- |
| 在候选分布算出来之后，实际输出是凭什么感觉被选中的 | top-k、top-p、temperature 怎样作为产品设置语言被更细地处理 |
| 为什么多样性与稳定性之间的取舍会改变结果 | 生成设置怎样调整回答风格、长度和变化宽度 |

top-k、top-p、temperature 的细节差异，会在 P6-5.2 里再具体化。这里先固定住：`计算候选分布的阶段`和`实际选择输出的阶段`是两个不同步骤，而输出质量同时受这两步影响。

例如，再想一想一个运维提示语的开头：

- `Batch inspection result`

在它后面，自然可能接上的短语不只一种，例如 `需要重新确认`、`经主管确认后恢复`、`10 分钟后重新测量`、`按当前标准保持正常`。

计算这组候选分布，和从里面取出一句真正的提示语，并不是同一件事。sampling 正是第二个阶段。

## sampling 在做什么

sampling 的核心，是一种选择步骤：它优先更高的候选，但也给其他候选留下成为实际输出的空间。

`sampling 是一种步骤：模型会更常选择它认为更可信的候选，但在某些情况下，也允许其他候选真正成为输出。`

也就是说，sampling 处理的是下面两个极端之间的问题。

- 永远只选分数最高的候选
- 把所有可能候选混得过于随机

在生成式 AI 里，这两者之间的平衡很重要。

在入门阶段，先区分下面三种方式就已经足够。

| 方式 | 先要抓住的直觉 |
| --- | --- |
| argmax | 永远只选分数最高的候选 |
| sampling | 更常选高候选，但也允许其他候选 |
| temperature 调整 | 让候选分布被读得更保守或更多样 |

如果把候选分布和实际被选中的频率并排看，这种差异会更清楚。先看模型给每个候选分配了多少权重时，会发现最高候选很明确，但其他候选并不全是 0。

![候选短语相对权重](/AiBook/assets/part-05/chapter-15/sampling-candidate-weights-zh.svg)

再看实际进行 20 次 sampling 后的选择频率时，就会发现：最高候选虽然出现最多，但较低候选也不会完全消失，而是能实际留在部分结果里。

![20 次 sampling 的选择频率](/AiBook/assets/part-05/chapter-15/sampling-choice-counts-zh.svg)

这张图里最关键的一点是：sampling 不是`随便乱抽`。它应该被读成一种选择步骤：基于模型给各候选分配的权重去采样实际输出，但不像 argmax 那样把结果固定成唯一一个候选。

## 为什么必须把多样性和稳定性一起看

如果完全不做 sampling，而是反复只选最高候选，输出看起来会很稳定。但它也可能显得太单调、太重复。

反过来，如果候选被放得太宽，输出多样性会变大，但句子可能突然不自然，或者意思开始漂移。

`生成质量不只是“答对没有”，它同时也是一个多样性与稳定性平衡的问题。`

## 在什么场景里，先看哪种平衡

读 sampling 时，最安全的不是一上来就说`一定要更有变化`或`一定要更保守`，而是先问：此刻到底该优先哪一边。

| 情况 | 先看的标准 | 更先要想起的选择感觉 |
| --- | --- | --- |
| 点检结果提示语 | 可重复性、尽量少抖动 | 以高概率候选为中心选择 |
| 解释型现场支援回答 | 正确性、结构稳定性 | 相对保守的 sampling |
| 运维文案草稿、应对消息草案 | 候选宽度、表达多样性 | 允许更多候选 |
| 图像概念探索 | 场景变化、风格范围 | 允许更宽的 sampling |

也就是说，sampling 最安全的读法，不只是把它当成`增加趣味`的工具，而是把它当成一种取舍：在输出一致性和多样性之间，此刻到底更优先哪一边。

## 为什么即使是同一个模型，也会产生不同结果

即使是同一个模型，只要下面这些条件变化，结果也会变化。

- 保留到哪一层候选为止
- 概率分布被读得有多尖锐
- 是只取最高候选，还是允许多个候选

正因为如此，用户有时会觉得`模型变了`，但实际上变化的可能只是输出选择策略。

这个视角在后面阅读 token 级生成和 prompt 实验时会非常重要。

## 如果把流程画得非常简单

```mermaid
--8<-- "assets/part-05/chapter-15/sampling-selection-flow-zh.mmd"
```

这张图里要确认的结果，是`模型分数计算`和`实际决定取出哪个候选`这两个步骤并不相同。

即使给出的是同一组候选分数，最后采用什么选择规则，用户体验也会立刻发生变化。

| 同样的前缀和候选分数 | 只选最高候选时先出现的结果 | 允许多个候选时先出现的结果 |
| --- | --- | --- |
| `Batch inspection result` 后面，`需要重新确认`、`经主管确认后恢复`、`10 分钟后重新测量` 都有可能 | 很容易反复只出现一条最保守的句子 | 在保留点检语境的同时，动作措辞和句子长度会有轻微变化 |
| 现场支援回答解释 `因压力异常停机后的重启顺序` | 很容易反复只出现同样的步骤句 | 核心安全流程可以保持，但警告语位置和解释长度会变化 |
| 按提示词 `stainless mixing tank with side valve and warning beacon` 生成图像 | 很容易反复出现相似的罐体构图和警示灯位置 | 核心设备场景会保留，但光线、视角、管路布局会变化 |

也就是说，`模型把哪个候选看得更高`，和`最后实际取出了哪个候选`，并不是同一个问题。

## 案例与示例

### 代表案例：点检结果提示语

`Batch inspection result`

人通常会先想到`一条最稳妥的回应短语`。所以也很容易觉得，生成提示语时，只要永远取最高候选就够了。但真实运维句子里，`需要重新确认`、`经主管确认后恢复`、`10 分钟后重新测量` 等候选都可能自然成立，而哪一个更合适，又会随着点检状态变化。比如警报反复出现时，`需要重新确认` 更自然；而如果现场处置已经开始，`经主管确认后恢复` 可能更自然。若总是只取最高候选，提示语会每次都冻成同一种语气；反过来，如果放得太宽，又可能跳出不那么贴合现场语境的动作短语。sampling 正是夹在这两者之间，控制实际取出哪个候选的步骤。

所以，这个案例里要确认的结果是：即使前缀 `Batch inspection result` 不变，真实运维情境不同，实际提示语也可能略有变化，而 sampling 正是控制这种选择宽度的步骤。

同样的视角也会直接延伸到现场支援回答和图像生成提示词。不过，本节真正要抓住的核心不是领域名称，而是`面对同一组候选分布，实际取出的输出会不会改变结果变化的宽度`。

| 案例 | 模型可能持有的候选 | 选得太窄时会发生什么 | 放得更宽时要确认什么结果 |
| --- | --- | --- | --- |
| 点检结果提示语 | `需要重新确认`、`经主管确认后恢复`、`10 分钟后重新测量` 等回应候选 | 每次都反复出现同一句动作短语 | 在保持运维语境的同时，回应措辞是否出现变化 |
| 现场支援回答 | 简短步骤型、警告先行型、解释扩展型回答候选 | 每次都出现差不多的长度和结构 | 在保持核心安全步骤时，解释格式是否会变化 |
| 图像生成 | 罐体角度、管路布局、警示灯强调、视点候选 | 结果场景会变得过于相似 | 在保留核心 prompt 的同时，是否会出现画面变化 |

| 人容易先看到的标准 | 从 sampling 视角重新阅读时的标准 |
| --- | --- |
| 容易觉得模型给最高分的那个候选，会立刻直接变成最终输出 | 打分和实际选择是两个不同步骤，所以即使分布相同，采用什么规则也会让结果不同 |
| 如果结果每次都不一样，容易只觉得模型不稳定 | 它也可能只是候选分布里允许了不同选择，所以必须把多样性和稳定性一起看 |
| 容易把 sampling 理解成单纯增加随机性 | 真正核心是：在允许其他候选的同时，到底要多强地优先高候选 |

把这三个案例放在一起时，sampling 的核心并不在于重新解释`模型学到了什么`，而在于：怎样按运维语境调节`多个候选里，实际要取出哪一个输出`。

如果在这里停一下，短暂固定住`什么时候只说模型学会了候选分布还不够，而必须把实际输出选择步骤单独拿出来`，那么后面 temperature、top-k、top-p 的说明就不会显得那么突然。

| 先想到的问题 | 为什么必须先从 sampling 视角来读 | 后续 Part 会继续什么 |
| --- | --- | --- |
| 为什么即使是同一个模型，每次结果也会略有不同？ | 因为除了学习到的候选分布外，还存在一个单独的实际输出采样步骤 | temperature、top-k、top-p 调节 |
| 为什么不能永远只选最高分候选？ | 因为稳定性会提高，但表达多样性和情境贴合度会缩得过窄 | 产品设置与用户体验控制 |
| 为什么输出质量不只是模型本身的问题？ | 因为“学到了什么”和“实际选了什么”会一起决定结果 | 回答风格、长度和变化宽度设计 |

## 练习与例子

### 例子 1：用固定 logits 确认 temperature 和 top-k

这个例子的目标，是在运行真实 LLM 之前，先用已经算好的候选分数（logits）确认 temperature 和 top-k 会怎样改变实际选择分布。真实 LLM 内部会处理多得多的 token 候选，但在入门阶段，小候选集合已经足够用来区分`分数 -> 概率 -> 实际选择`。

```python
# 在固定 logits 上只改变 sampling 设置，比较候选概率、选择频率和 entropy。
import math
import random

import numpy as np

candidates = [
    "需要重新确认。",
    "经主管确认后恢复。",
    "10 分钟后重新测量。",
    "按当前标准保持正常。",
    "立即重新启动。",
]
logits = np.array([3.2, 2.4, 1.7, 0.6, -0.4])

experiments = [
    ("argmax", 0.0, None),
    ("temperature_0.7", 0.7, None),
    ("temperature_1.4", 1.4, None),
    ("top_k_3_temperature_1.0", 1.0, 3),
]


def softmax(values, temperature):
    scaled = values / temperature
    shifted = scaled - np.max(scaled)
    exp_scores = np.exp(shifted)
    return exp_scores / exp_scores.sum()


def apply_top_k(probabilities, k):
    if k is None:
        return probabilities
    kept_indices = np.argsort(probabilities)[-k:]
    filtered = np.zeros_like(probabilities)
    filtered[kept_indices] = probabilities[kept_indices]
    return filtered / filtered.sum()


def probabilities_for(temperature, top_k):
    if temperature == 0.0:
        probabilities = np.zeros_like(logits, dtype=float)
        probabilities[int(np.argmax(logits))] = 1.0
        return probabilities
    return apply_top_k(softmax(logits, temperature), top_k)


def entropy_bits(probabilities):
    non_zero = probabilities[probabilities > 0]
    if len(non_zero) <= 1:
        return 0.0
    return -sum(p * math.log2(p) for p in non_zero)


for label, temperature, top_k in experiments:
    probabilities = probabilities_for(temperature, top_k)
    random.seed(15)
    choices = random.choices(
        range(len(candidates)),
        weights=probabilities,
        k=40,
    )
    counts = [choices.count(index) for index in range(len(candidates))]

    print(f"[{label}]")
    print("probabilities =", [round(float(value), 3) for value in probabilities])
    print("counts =", counts)
    print("entropy_bits =", round(entropy_bits(probabilities), 3))
    print("top_choice =", candidates[int(np.argmax(probabilities))])
    print()
```

```text
[argmax]
probabilities = [1.0, 0.0, 0.0, 0.0, 0.0]
counts = [40, 0, 0, 0, 0]
entropy_bits = 0.0
top_choice = 需要重新确认。

[temperature_0.7]
probabilities = [0.682, 0.217, 0.08, 0.017, 0.004]
counts = [24, 8, 5, 2, 1]
entropy_bits = 1.277
top_choice = 需要重新确认。

[temperature_1.4]
probabilities = [0.467, 0.264, 0.16, 0.073, 0.036]
counts = [18, 7, 7, 4, 4]
entropy_bits = 1.89
top_choice = 需要重新确认。

[top_k_3_temperature_1.0]
probabilities = [0.598, 0.269, 0.133, 0.0, 0.0]
counts = [22, 8, 10, 0, 0]
entropy_bits = 1.341
top_choice = 需要重新确认。
```

这里首先要看的，是四种设置里的 `top_choice` 都相同。最高候选始终是`需要重新确认。`，但实际选择分布已经明显不同。`argmax` 会 40 次都选择同一个候选，`temperature_1.4` 会给较低候选留下更大空间，而 `top_k_3_temperature_1.0` 会把后两个候选直接排除在可选集合之外。

![不同 sampling 设置下的候选概率](/AiBook/assets/part-05/chapter-15/sampling-control-probabilities-zh.png)

![40 次 sampling 的选择频率](/AiBook/assets/part-05/chapter-15/sampling-control-counts-zh.png)

因此，这个例子的结论不是`temperature 越高越好`。在同一组 logits 下，只要选择规则改变，候选分布的展开程度和实际选择频率就会改变。生成设置应该被读成`从模型知道的内容里实际取出什么`的控制阶段，而不是模型知识本身。

### 可选例子：用 Ollama 观察真实 LLM 输出变化

前一个例子用固定 logits 确认可复现的选择规则。如果本地已经准备好 Ollama 和模型，就可以继续观察：即使是同一个 prompt，只要改变生成设置，实际输出的稳定性和变化宽度也可能不同。Part 1 没有要求读者用 Python 调用 LLM，但到了这里，我们已经讨论过生成模型和 sampling，所以可以用真实输出来确认这一点。

这个例子不是为了熟练掌握 API 用法。核心是看到：`模型计算候选`和`从候选中取出实际句子`是分开的步骤，而生成设置会改变第二个步骤带来的用户体验。

要运行这个例子，Ollama 必须已经在本地运行，代码里的 `MODEL` 值也要换成自己环境中已经安装的模型名。Ollama 默认在 `http://localhost:11434/api` 提供本地 API，`/api/generate` 是根据 prompt 生成回答的端点。

看代码前，先抓住下面四个值就够了。

| 要确认的点 | 例子里直接要看的值 | 为什么重要 |
| --- | --- | --- |
| 同一个 prompt 执行几次 | `RUNS_PER_SETTING` | 避免只看一次输出就断定模型倾向 |
| 生成设置怎样改变 | `temperature` | 用低值和高值比较表达稳定性与变化宽度 |
| 回答长度怎样限制 | `num_predict` | 防止输出过长，使观察重点变模糊 |
| 实际输出里看什么 | `response` | 确认同一个请求下，句子顺序、警告位置、表达宽度是否会变化 |

看代码前，可以先猜一猜：同一个 prompt 下，设置不同会先在哪里产生差异。

| 比较点 | 低 temperature 下先预期到的结果 | 高 temperature 下先预期到的结果 |
| --- | --- | --- |
| 句子结构 | 更可能重复相近的顺序和表达 | 核心可能保留，但表达顺序或句子长度会变化 |
| 警告语 | 安全确认语句可能更稳定地重复 | 警告位置或表达方式可能变化 |
| 复核负担 | 更容易比较，但可能显得单调 | 能得到更多样的草稿，但也增加要复核的差异 |

prompt 故意保持为一个简短的运维提示语生成场景。模型名要改成自己 Ollama 环境里已经安装的名称。`temperature` 和 `RUNS_PER_SETTING` 是读者可以直接改动的操作变量。

```python
# 通过 Ollama 本地 API 多次运行同一个 prompt，观察生成设置怎样改变输出。
import json
import textwrap
import urllib.error
import urllib.request

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3"  # 改成自己 Ollama 环境中已经安装的模型名。
RUNS_PER_SETTING = 2

PROMPT = """
请为现场作业人员写一段不超过两句话的运维提示语。

情况：
批次检查结果显示压力波动已经减小，但重新启动前仍需再次确认 interlock 和传感器状态。

条件：
- 不要断定看不见的原因。
- 包含重新启动前需要确认的行动。
- 避免夸张表达，写成可以复核的句子。
""".strip()

experiments = [
    {
        "label": "stable_temperature",
        "options": {
            "temperature": 0.1,
            "num_predict": 80,
        },
    },
    {
        "label": "wider_temperature",
        "options": {
            "temperature": 0.9,
            "num_predict": 80,
        },
    },
]

def generate_with_ollama(label, options, run_index):
    payload = {
        "model": MODEL,
        "prompt": PROMPT,
        "stream": False,
        # 这是本例中的操作变量。改变 temperature 后，输出选择宽度可能会变化。
        "options": options,
    }
    request = urllib.request.Request(
        OLLAMA_GENERATE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        print("无法连接到 Ollama。")
        print("请确认 Ollama 是否正在运行，以及 MODEL 是否是已安装的模型名。")
        print("error =", error)
        return

    generated = data.get("response", "").strip()
    one_line = " ".join(generated.split())

    print(f"[{label} / run {run_index}]")
    print("options =", options)
    print(textwrap.shorten(one_line, width=220, placeholder=" ..."))
    print()

for experiment in experiments:
    for run_index in range(1, RUNS_PER_SETTING + 1):
        generate_with_ollama(
            experiment["label"],
            experiment["options"],
            run_index,
        )
```

执行结果会因模型、版本、本地环境和执行时点而变化。这里重要的不是把某一句话当成标准答案，而是观察：即使 prompt 和模型相同，生成设置也可能改变输出体验。

| 先看的输出 | 这个输出表示什么 | 改动它时会看到什么变化 |
| --- | --- | --- |
| `stable_temperature` 的回答 | 显示低 temperature 下是否出现相对稳定的句子结构 | 如果把 `temperature` 再调低，重复性可能增加，但表达宽度也可能变窄 |
| `wider_temperature` 的回答 | 显示高 temperature 下表达顺序、句子长度、词语选择是否更容易波动 | 如果把 `temperature` 再调高，变化可能变大，但复核负担也会增加 |
| 同一设置下的两次执行结果 | 显示不能只凭一次输出判断生成设置的性质 | 增加 `RUNS_PER_SETTING` 后，更容易比较重复性和变化宽度 |

- 如果低 temperature 下两次回答几乎是同一种结构，可以把它读成候选选择宽度变窄、稳定性变高的场景。
- 如果高 temperature 下句子顺序或表达更不一样，可以把它读成候选选择宽度变宽、草稿多样性变大的场景。
- 但是，高 temperature 并不总是表示回答更好。现场提示语里，安全确认、不随意断定原因、重新启动前行动是否保留，仍然需要人重新复核。
- 因此，这个例子的结论不是`设置调高就更有创造力`，而是`输出选择步骤会改变实际句子体验，而结果必须再次复核`。

这个结果也不应该只停在`它们不同`。还要能继续确认：改动什么值，会让多样性与稳定性的平衡开始摇动。

| 先看到的输出信号 | 现在马上可以尝试的变化 | 不应只凭这个例子就仓促下结论的事 |
| --- | --- | --- |
| 低 temperature 下句子几乎重复 | 逐步提高 `temperature`，看表达宽度从什么时候开始变宽 | 不要断定重复性高就一定是质量好 |
| 高 temperature 下句子更多样 | 在同一条件下增加 `RUNS_PER_SETTING`，继续观察变化宽度 | 不要断定多样性就直接等于正确性或安全性 |
| 某个输出漏掉了重要确认行动 | 把 prompt 条件写得更明确，或降低 temperature | 不要认为只靠 prompt 和设置就能免除复核责任 |

如果在这里再往前走一步，最好把这一节的例子读成`真实 LLM 输出选择敏感度实验`。

| 先改哪个值 | 会看到什么开始摇动 | 本节里先要确认的结果 |
| --- | --- | --- |
| 把 `temperature` 从 0.1 提高到 0.9 | 同一个 prompt 的表达顺序和词语选择会变得多不一样 | 即使变化宽度变大，核心安全条件是否仍然保留 |
| 缩短或增加 `num_predict` | 输出长度和被省略的信息是否变化 | 短输出是否更容易复核，同时又没有漏掉重要条件 |
| 从 prompt 条件里删掉`不要断定看不见的原因` | 模型是否更容易断定原因 | 不只要看输出多样性，也要一起复核危险断定 |

也就是说，这一节的例子不应停留在`argmax 和 sampling 不一样`这种手算直觉上，而应让我们在本地 LLM 的真实输出里看到：生成设置和 prompt 条件会怎样摇动运维消息与后续行动措辞。

语言模型（language model）通常会计算下一个 token 的可信度，而图像生成模型会逐步构造可能的视觉模式。实际输出则会通过“算出来的分布”和“选择策略”这两步一起出现。

- token 与 tokenization
- next-token prediction
- temperature、top-k、top-p 等生成设置
- 为什么 prompt 一变，输出也会跟着改变

## 检查清单

- 能解释 sampling 是在已学习候选中选择实际输出的过程吗？
- 能解释多样性与稳定性的取舍会怎样影响结果吗？
- 能说明生成模型先计算候选可信度，而 sampling 再从中选出实际输出吗？
- 能说清生成问题未必只有一个正确答案吗？
- 能解释为什么多样性和稳定性的平衡对生成质量很重要吗？
- 能否不只把 sampling 说成“加点随机性”，而是解释成“从候选分布里选择实际输出的步骤”？
- 能否把 argmax 和 sampling 分别说成“固定最高候选”与“更常选高候选但仍允许其他候选”？
- 在阅读后面 Part 的生成设置时，是否已经准备好先把`模型打分`和`实际输出选择`看成两个不同阶段？

## 出处与参考资料

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016，确认日期：2026-06-29。[https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Christopher D. Manning, Hinrich Schutze, `Foundations of Statistical Natural Language Processing`, MIT Press, 1999，确认日期：2026-07-19。[https://mitpress.mit.edu/9780262133609/foundations-of-statistical-natural-language-processing/](https://mitpress.mit.edu/9780262133609/foundations-of-statistical-natural-language-processing/){: target="_blank" rel="noopener noreferrer" }
- Daniel Jurafsky, James H. Martin, `Speech and Language Processing` draft materials，确认日期：2026-07-19。[https://web.stanford.edu/~jurafsky/slp3/](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }
- Ollama, [Introduction](https://docs.ollama.com/api/introduction){: target="_blank" rel="noopener noreferrer" }, Ollama API documentation，确认日期：2026-07-22。
- Ollama, [Generate a response](https://docs.ollama.com/api/generate){: target="_blank" rel="noopener noreferrer" }, Ollama API documentation，确认日期：2026-07-22。
