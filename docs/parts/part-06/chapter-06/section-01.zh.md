# P6-7.1 成为长生成出发点的下一个 token 预测

> Section ID: `P6-7.1`
> Version: `v2026.07.26`

在 P6-5.2 中，我们看过 GPT 基础生成结构如何连接到对话式 LLM 体验。现在该把问题再收窄一些。

那么大的模型在训练时究竟反复做什么？

第一次接触 LLM 时最常听到的回答如下。

LLM 会被训练成预测下一个 token。

这句话是对的，但如果太短，就会引起误解。许多读者听到这句话后会想：`那不就是简单自动补全吗？` 这里我们把这个问题整理到更准确的层位。

理解生成式 LLM 时，第一个标准是 `模型被训练成反复猜中什么`。搜索或工具连接是补强生成结果的装置，alignment 是调节回应习惯的阶段。在那些之前，首先要抓住的感觉是：`在当前上下文中计算下一个 token 分布`，才是长生成的出发点。

## 下一个 token 预测这个基本目标

基本训练目标从下面的问题开始。

- 下一个 token 预测究竟预测什么？
- 为什么这个看似简单的目标能连接到长句、摘要、问答、代码生成？
- 仅靠下一个 token 预测可以说明什么，又不能说明什么？

这里处理的是 `把什么作为学习目标`。实际生成时从候选中选哪个，是输出选择规则的问题；如何调节回应习惯，是 alignment 和后续调节的问题。必须区分这三者，才不会把 `下一个 token 预测` 这一句话拉得过宽。

因此，核心不是 `看起来像自动补全` 的印象，而是 `在当前上下文中反复计算下一个 token 分布` 这个学习目标。本节抓住 LLM 在训练中反复预测什么，以及这种局部预测为什么会成为长生成和多种语言任务的出发点。候选中实际选择什么，留给下一节的 sampling 问题；回应习惯和安全性如何调节，留给后面的 instruction tuning 与 alignment 问题。

目标是建立标准，让自己能够说明 `LLM 的基本学习目标` 是什么。

必须把 `一次拿出完整句子的模型` 这种印象，改读成 `在当前上下文中计算下一个 token 分布，并累积这个选择的结构`。

## 下一个 token 目标与长生成的区分

- 可以用 token 单位说明下一个 token 预测。
- 可以说明句子生成不是一次完成，而是顺序接续。
- 可以说出为什么简单预测目标会连接到复杂语言行为。
- 可以区分仅靠这个标准无法解释 LLM 的全部。

这个标准重要，理由如下。

- 它把 token、embedding、Transformer 重新捆到一个学习目标上
- 它能不过度夸张地说明生成式 AI 的基本动作
- 它让后续 sampling、temperature、prompting、alignment 都能放在这个基础上

## 下一个 token 预测的判断标准

如果不想只把下一个 token 预测读成简单自动补全，就需要分离四个标准。

| 判断标准 | 要确认的问题 |
| --- | --- |
| 预测单位 | 是否不是整句，而是计算下一个 token 候选分布 |
| token 单位 | 是否不是按单词，而是按 token 片段说明 |
| 累积效果 | 当前上下文改变时，下一个候选分布是否也一起改变 |
| 后续连接 | 是否能连接到 sampling、prompting、alignment 的说明出发点 |

## 下一个 token 预测是什么意思

LLM 在训练中阅读长文本，并被反复调节为：根据目前给出的 token，猜中接下来最可能出现的 token。

例如，可以这样看。

- 输入上下文(context)：`今天天气非常`
- 下一个候选 token：`好`、`冷`、`晴朗`、……

这时，模型会基于 `到目前为止的 token`，计算 `紧接着的下一个 token` 的概率分布。

重要的是，模型并不是一开始就把整个句子完整拿出来。

`查看目前为止的上下文，预测下一个片段，再把那个片段贴回上下文` 的过程会反复发生。

## 为什么是 token 单位

LLM 通常不是直接处理字符，而是按 token 单位处理。正如本书前面看过的，token 可以是完整单词，也可以是单词的一部分，也可以是符号片段。

因此，说 `预测下一个单词` 往往不够严密。更安全的表达如下。

`LLM 被训练成预测下一个 token(next token)。`

必须区分这个差异，后面才能一起理解 tokenization、context window、成本计算。

## 为什么简单目标会连接到复杂功能

读者最常在这里停住。

如果只是反复 `猜中下一个片段`，为什么还能摘要、翻译、写代码？

核心如下。

- 语言有顺序结构
- 下一个表达会随上下文大幅改变
- 如果大量阅读长文档和多种体裁
- 为了很好地猜中下一个 token，就必须一起反映语法、表达、关系、格式、部分世界知识

也就是说，学习目标本身看起来是局部(local)的，但要做好这个目标，模型内部必须处理很宽的模式。

这就是为什么很难把 LLM 完全看成简单自动补全。

## 与自动补全到哪里相同，又从哪里不同

自动补全比喻有用，是因为二者都有 `从当前上下文后面选择会出现什么` 这个共同结构。查看目前输入的上下文，预测下一个输出，一片一片接上并形成结果，这一点上自动补全和 LLM 生成相似。

但停在这里就说明不足。LLM 生成可以一起反映更长上下文、多种文档格式、任务指令、对话记录，并因此扩展成摘要、问答、说明、转换、代码生成等任务形式。所以比较核心不是 `是否和自动补全一样`，而是同一个下一个 token 预测结构，在更大上下文和更长输出中开始制造什么负担。

| 比较轴 | 短自动补全比喻 | LLM 生成中更强地显露的点 |
| --- | --- | --- |
| 输入上下文 | 短句的一部分 | 可以一起反映长文档、对话记录、指令 |
| 输出长度 | 下一个一两个词 | 可以接成多句、代码 block、摘要段落 |
| 任务范围 | 续写辅助 | 扩展成摘要、问答、说明、转换、代码生成等多种形式 |
| 失败样态 | 别扭的下一个词 | 可能变成事实错误、结构崩塌、错误中心句等更大层级的失败 |

也就是说，LLM 的出发点也像自动补全，但因为 `输入范围`、`输出长度`、`失败成本` 大得多，所以应把它读成比简单句子辅助更宽的系统。更安全的整理如下。

`LLM 基于下一个 token 预测结构，但经过大规模预训练和追加调节，会执行非常多样的语言工作形式。`

## 极简画出来

```mermaid
--8<-- "assets/part-06/chapter-06/p6-c06-s01-next-token-loop-zh.mmd"
```

这个图示的核心是：生成不是 `一次结束的计算`，而是 `反复发生的顺序计算`。

## 案例与示例

下面的图示不是按 `选择下一个 token`，而是按 `早期选择如何推动后面的整个上下文` 这个共同问题，重新捆起本节的三个案例。

```mermaid
--8<-- "assets/part-06/chapter-06/p6-c06-s01-branch-effects-zh.mmd"
```

这个图示中要确认的是，即使任务不同，生成也都是累积结构。早期一个 token 的选择会连锁影响后面的句子、摘要、代码结构，因此下一个 token 预测比起 `猜一个片段`，更适合读成 `决定后续流程的起始选择`。

### 案例 1. 接续邮件句子

可以想象一封客户邮件草稿以 `您好，关于您咨询的内容` 开始。人看到这种句子时，很容易觉得后面的句子几乎已经有一个固定正确答案，但实际上，说明、道歉、引导等多种表达都可能成为候选。

例如，即使是同一个咨询，`确认结果`、`给您带来不便，我们深表歉意`、`下面说明后续流程` 这类不同开头都可能自然。这里变化的是：从 `是否拿出一个正确句子` 的标准，移动到 `当前上下文中哪个候选更自然` 的标准。

这里重要的不是下一句被固定成一个，而是多个候选中哪个表达在当前上下文中更自然。模型在训练中反复看到这种续写模式，并学习下一个 token 分布。

如果第一句定为道歉中心，后面更容易跟上补偿或处理日程说明；如果定为确认结果中心，后面更可能 接上说明型句子。因此，这个案例中要确认的结果是：同一个输入下，第一表达选择是否真的会改变后面句子的语气和后续指引流程。

这个案例重要，是因为生成结果很容易让人感觉像 `从脑中某处拿出正确句子` 的过程。但实际上，它更接近前几个 token 推动后面句子性格的累积结构。邮件草稿若从 `抱歉` 开始，后面更容易接向补偿和措施说明；若从 `确认结果` 开始，后面更可能接向说明和事实传达。因此，理解下一个 token 预测时，比起 `一次选择整句`，更准确的是 `早期选择决定后续流程方向`。

从续写选择角度重看这个差异，可以得到下表。

| 第一表达选择 | 在人眼中都自然的点 | 后面句子中实际容易变化的流程 |
| --- | --- | --- |
| `给您带来不便，我们深表歉意` | 作为客户回应看起来稳妥 | 道歉、补偿、后续处理说明更容易接上 |
| `确认结果` | 作为事实传达开头看起来稳妥 | 说明型句子和原因整理更容易跟随 |
| `下面说明后续流程` | 看起来像友好的指引 | 分步骤行动指引和链接/方法说明更容易 接上 |

这个表要纠正的误解是 `反正句子相似，后面也差不多`。实际上，前几个 token 的选择会持续拉动后面的语气和 指引结构。

### 案例 2. 摘要

可以想象把会议记录变成三行摘要的场景。只看结果时，人很容易觉得 `摘要` 是一种单独能力，并想象模型一次拿出了压缩后的正确答案。

但在实际生成过程中，会反复执行一种结构：在目前已经做出的摘要句后面，继续接上自然的表达。例如，如果第一行选择 `部署日程被推迟`，下一行更自然地会接续理由或后续措施。

这里变化的是，从 `一次拿出摘要答案` 的感觉，移动到 `第一句选择会持续推动后续摘要流程` 的感觉。当然，此时必须在内部反映输入文档的核心，才不会选择奇怪的下一表达。

如果第一行错误开始，后面句子也会沿着那个流程走，因此早期抓错中心句的成本很大。也就是说，摘要并不是特殊魔法，也可以读成反映上下文的下一个 token 选择的连续过程。所以，这个案例中要确认的结果是：第一摘要句如何开始，是否真的会一起改变后面句子的理由、措施、强调顺序。

这个场景也直接触碰实践中常见的误解。人看到完整摘要后，很容易想象 `它从一开始就知道这整段摘要`。但实际上，第一行把什么选为中心，会持续推动第二行、第三行方向。以 `部署日程被推迟` 开始，后面更容易贴上理由和后续措施；以 `需要法务审查` 开始，风险和审批流程更容易成为中心。也就是说，摘要与其说是一次拿出完成的压缩答案，不如说是中心句如何被抓住会规定后续流程的累积生成结构。

同一份会议记录，也会因第一行选择而改变后续摘要结构。

| 第一摘要句选择 | 容易先想到的印象 | 后面实际容易强调的内容 |
| --- | --- | --- |
| `部署日程被推迟` | 像先抓住核心结论的摘要 | 推迟理由、下一步措施 |
| `需要法务审查` | 像风险中心摘要 | 审批流程、保留事项 |
| `负责人已变更` | 像交接中心摘要 | 角色转换、后续责任 |

这个案例的重要标准，不是 `摘要是一次压缩的结果` 这种印象，而是 `第一个中心句推动后面句子的强调顺序` 这一结构。下一个 token 预测视角正是为了说明这种累积效果。

### 案例 3. 代码生成

可以想象在代码生成中已经写到 `def calculate_total` 的场景。人看到这个位置时，会期待后面接上括号、冒号、缩进 block 等结构。

同时，代码比自由叙述严格得多，只要进入一个不符合当前上下文的 token，就很容易直接变成语法错误或流程错误。例如，函数名是计算总额，但下一行漏掉折扣变量，或忘了需要关闭的括号，后面整体都可能崩掉。

条件语句缩进一旦错位，返回语句位置也会连锁偏移，这一点也展示同一结构。这里变化的是，从 `一次完成代码 block` 的感觉，移动到 `早期 token 选择会持续拉动后面整个结构` 的感觉。

LLM 像处理自然语言一样，也在 `当前上下文后面什么最像会出现` 的反复选择结构中处理这些代码 token 模式。因此，这个案例中要确认的结果是：早期一个 token 的选择是否会连锁摇晃后续代码的变量名、缩进、返回结构。

把三个案例从下一个 token 选择视角重新捆起，可以得到下表。

| 情况 | 当前上下文先决定的内容 | 下一阶段马上改变的候选 |
| --- | --- | --- |
| 邮件续写 | 道歉型、说明型、指引型等语气 | 后面句子的语气和指引流程 |
| 摘要 | 第一摘要句的中心信息 | 理由、措施、强调顺序 |
| 代码生成 | 函数结构和当前 block 上下文 | 括号、缩进、返回模式 |

## 下一个 token 预测显露出来的场景

即使还不知道 sampling 或 temperature 的细节，也可以简短区分眼前现象如何连接到下一个 token 预测这个学习目标。同一句前文后面，若道歉型、说明型、指引型候选都自然，就应先问 `当前上下文是否打开了多个下一个 token 候选分布`，而不是 `是否存着一个正确句子`。如果摘要第一行抓错后，后面句子也被推向同一方向，就应看 `这是第一选择持续改变后续生成路径的顺序结构吗`，而不是 `是否一次拿出整个摘要`。如果代码中括号一错后整个 block 崩掉，就应问 `当前 token 选择是否连锁改变后面上下文条件`，而不是 `一个小 token 后面会恢复吧`。

这个区分中重要的不是追问 `是否和自动补全完全一样`，而是把长生成也位于 `当前上下文后面会来什么` 的反复预测结构之上这一点，套回实际案例。

这里经常混在一起的内容如下。

- 容易把学习目标 `下一个 token 预测` 和实际服务回应整体捆到同一层位。
- 容易把摘要、说明、代码生成看成不同魔法，却错过它们都位于同一个顺序预测结构之上。
- 容易低估下一个 token 一个选择会多强地推动后面整个结构。

因此，`LLM 会被训练成预测下一个 token` 这句话不应只是背诵定义，而应成为阅读实际生成场景的标准。

这个区分的目的不是一次确定原因。它是为了不把 `下一个 token 预测` 只背成一句定义，而是短暂区分眼前现象先显露在 `候选分布`、`累积生成`、`连锁错误` 中的哪一处。

## 练习与示例

这个例子的目标不是实现真实 LLM 的全部，而是用眼睛确认 `训练数据如何形成下一个 token 候选`，以及 `被选择的 token 是否再次成为下一阶段输入`。这里不手动放入固定分数字典，而是直接从一组小句子中数 `前三个 token -> 下一个 token` 的频率，并用结果接着生成几个 prompt。

下面代码使用几条短训练句、几个生成起始 prompt、最大生成长度。结果中会一起看到每个上下文的下一个 token 候选分布、每一步选择的 token、第一分支中存在什么候选竞争、累积生成的最终序列。若候选同分，为了让执行过程简单可见，就选择先观察到的候选。这个选择规则不是为了模仿真实 LLM 的 decoding 策略，而是为了看见 `候选分布出现，选择一个后，下一上下文改变` 这一流程。

要确认的核心是：下一个 token 分布，是训练句子中反复出现的连接模式累积出来的结果。

先看作为输入的小训练句子组。这个输入不是真实 LLM 训练数据，而是为了展示 `即使前面上下文相同，下一候选也可能打开成多个分支` 这一感觉的缩小语料。每组由共享相同前半部分的两句话构成，让第一分支中候选分成两条。

| 输入组 | 训练句子 | 第一分支中形成的候选 |
| --- | --- | --- |
| 会议结果 | `会议 结果 部署 日程 推迟 到 下周`<br>`会议 结果 优先 修改 项目 先 处理` | `部署`、`优先` |
| 客户咨询确认结果 | `客户 咨询 确认 结果 退款 流程 将 引导`<br>`客户 咨询 确认 结果 配送 日程 将 再次 引导` | `退款`、`配送` |
| 部署错误确认结果 | `部署 错误 确认 结果 配置 文件 路径 错误`<br>`部署 错误 确认 结果 日志 收集 范围 先 确认` | `配置`、`日志` |

代码会把这些句子按空格切成 token，并计算 `前三个 token -> 下一个 token` 的频率。真实 LLM 并不是查找这种精确三 token 表的结构，但这个缩小例子的目的是确认 `当前上下文会形成候选分布，所选 token 会再接回下一上下文` 这种顺序生成感。

```python
# 这个例子从小训练句子组中统计前三个 token 对应的下一个 token 频率，并用该分布接着生成 prompt。
from collections import Counter, defaultdict

training_sentences = [
    "会议 结果 部署 日程 推迟 到 下周",
    "会议 结果 优先 修改 项目 先 处理",
    "客户 咨询 确认 结果 退款 流程 将 引导",
    "客户 咨询 确认 结果 配送 日程 将 再次 引导",
    "部署 错误 确认 结果 配置 文件 路径 错误",
    "部署 错误 确认 结果 日志 收集 范围 先 确认",
]

def tokenize(sentence):
    return sentence.split()

def build_ngram_counts(sentences):
    ngram_counts = defaultdict(Counter)
    for sentence in sentences:
        tokens = ["<BOS1>", "<BOS2>", "<BOS3>"] + tokenize(sentence) + ["<EOS>"]
        for i in range(len(tokens) - 3):
            context = (tokens[i], tokens[i + 1], tokens[i + 2])
            next_token = tokens[i + 3]
            ngram_counts[context][next_token] += 1
    return ngram_counts

def next_token_distribution(ngram_counts, context_tokens):
    context = tuple(context_tokens[-3:])
    counter = ngram_counts.get(context, Counter())
    total = sum(counter.values())
    if total == 0:
        return {}
    return {
        token: round(count / total, 2)
        for token, count in counter.most_common()
    }

def generate_tokens(ngram_counts, prompt, max_steps=5):
    generated = ["<BOS1>", "<BOS2>", "<BOS3>"] + tokenize(prompt)
    trace = []

    for _ in range(max_steps):
        context = generated[-3:]
        distribution = next_token_distribution(ngram_counts, context)
        if not distribution:
            trace.append(
                {
                    "context": tuple(context),
                    "distribution": {},
                    "selected": "<STOP:no-known-next-token>",
                }
            )
            break

        selected = max(distribution, key=distribution.get)
        trace.append(
            {
                "context": tuple(context),
                "distribution": distribution,
                "selected": selected,
            }
        )
        if selected == "<EOS>":
            break
        generated.append(selected)

    visible_tokens = [token for token in generated if not token.startswith("<BOS")]
    return visible_tokens, trace

ngram_counts = build_ngram_counts(training_sentences)
prompts = ["会议 结果", "客户 咨询 确认 结果", "部署 错误 确认 结果"]

for prompt in prompts:
    generated, trace = generate_tokens(ngram_counts, prompt, max_steps=5)
    print("=" * 80)
    print("prompt =", prompt)
    if trace:
        first_distribution = trace[0]["distribution"]
        print("first_branch_candidates =", first_distribution)
    for step_index, step in enumerate(trace, start=1):
        print(f"[step {step_index}] context =", step["context"])
        print("distribution =", step["distribution"])
        print("selected =", step["selected"])
    print("generated =", generated)
```

这个例子已用本地 `.venv` 的 Python 执行，并确认与正文输出一致。

执行结果示例可以这样阅读。

```text
================================================================================
prompt = 会议 结果
first_branch_candidates = {'部署': 0.5, '优先': 0.5}
[step 1] context = ('<BOS3>', '会议', '结果')
distribution = {'部署': 0.5, '优先': 0.5}
selected = 部署
[step 2] context = ('会议', '结果', '部署')
distribution = {'日程': 1.0}
selected = 日程
[step 3] context = ('结果', '部署', '日程')
distribution = {'推迟': 1.0}
selected = 推迟
[step 4] context = ('部署', '日程', '推迟')
distribution = {'到': 1.0}
selected = 到
[step 5] context = ('日程', '推迟', '到')
distribution = {'下周': 1.0}
selected = 下周
generated = ['会议', '结果', '部署', '日程', '推迟', '到', '下周']
================================================================================
prompt = 客户 咨询 确认 结果
first_branch_candidates = {'退款': 0.5, '配送': 0.5}
[step 1] context = ('咨询', '确认', '结果')
distribution = {'退款': 0.5, '配送': 0.5}
selected = 退款
[step 2] context = ('确认', '结果', '退款')
distribution = {'流程': 1.0}
selected = 流程
[step 3] context = ('结果', '退款', '流程')
distribution = {'将': 1.0}
selected = 将
[step 4] context = ('退款', '流程', '将')
distribution = {'引导': 1.0}
selected = 引导
[step 5] context = ('流程', '将', '引导')
distribution = {'<EOS>': 1.0}
selected = <EOS>
generated = ['客户', '咨询', '确认', '结果', '退款', '流程', '将', '引导']
================================================================================
prompt = 部署 错误 确认 结果
first_branch_candidates = {'配置': 0.5, '日志': 0.5}
[step 1] context = ('错误', '确认', '结果')
distribution = {'配置': 0.5, '日志': 0.5}
selected = 配置
[step 2] context = ('确认', '结果', '配置')
distribution = {'文件': 1.0}
selected = 文件
[step 3] context = ('结果', '配置', '文件')
distribution = {'路径': 1.0}
selected = 路径
[step 4] context = ('配置', '文件', '路径')
distribution = {'错误': 1.0}
selected = 错误
[step 5] context = ('文件', '路径', '错误')
distribution = {'<EOS>': 1.0}
selected = <EOS>
generated = ['部署', '错误', '确认', '结果', '配置', '文件', '路径', '错误']
```

先压缩长执行结果，可以得到下表。

| prompt | 第一候选分布 | 被选择的第一 token | 后续生成路径 |
| --- | --- | --- | --- |
| `会议 结果` | `部署`: 0.5, `优先`: 0.5 | `部署` | `日程 -> 推迟 -> 到 -> 下周` |
| `客户 咨询 确认 结果` | `退款`: 0.5, `配送`: 0.5 | `退款` | `流程 -> 将 -> 引导` |
| `部署 错误 确认 结果` | `配置`: 0.5, `日志`: 0.5 | `配置` | `文件 -> 路径 -> 错误` |

这张摘要表中首先要看的是，第一候选并没有固定成一个。即使是同样方式制作的小语料，当前 prompt 改变时第一候选分布也会改变；先选中一个 token 后，该 token 又会贴回下一阶段上下文，改变后续生成路径。

这个例子中要确认的结果是：训练数据会形成按上下文区分的下一候选分布，当前上下文改变时候选分布也会改变，而被选择的 token 又会成为更长上下文，继续作为下一选择条件。尤其查看 `first_branch_candidates` 时，可以直接看出三个 prompt 从第一次候选竞争开始就已经不同。

- 训练句子中会按上下文聚合下一候选
- 当前上下文会改变下一候选分布
- 选中一个 token 后，该 token 会贴回下一阶段上下文
- 早期选择会推动后续生成流程整体

## 顺序生成中累积的候选分布

这个例子不应读成一次拿出生成结果的盒子，而应读成 `到目前为止形成的上下文` 持续回到下一选择条件中的循环结构。在 `会议 结果` 后面，会出现 `部署`、`优先` 这样的候选；在 `客户 咨询 确认 结果` 后面，候选会变成 `退款`、`配送`；在 `部署 错误 确认 结果` 后面，候选又变成 `配置`、`日志`。一旦选择 `退款`，后面就会接上 `流程`、`将`、`引导` 这类符合该流程的 token；如果选择 `配置`，则会接上 `文件`、`路径`、`错误` 这样完全不同的路径。因此，后面阅读 sampling、prompting、alignment 时，也应持续保持 `下一个 token 选择不断累积，最终形成整个回应` 这一视角。

如果把这个例子重新缩成判断标准，下面三个问题应该先浮现出来。

| 场景 | 要先回答的问题 |
| --- | --- |
| 为什么同一个前文后面候选不是固定一个 | 当前上下文是否制造了多个下一个 token 候选分布 |
| 为什么第一行选择会摇晃后续摘要和代码结构 | 被选择的 token 是否重新进入下一阶段上下文的顺序结构 |
| 为什么摘要、说明、代码生成能从一个学习目标出发 | 不同任务是否也位于预测 `现在这里后面什么自然` 的能力之上 |

## 检查清单

- 能否把下一个 token 预测说明为 `下一个片段分布` 的反复，而不是 `整个长回答`？
- 能否同时说明自动补全和 LLM 相同的地方与不同的地方？
- 是否准备好把接下来的生成选择说明，读成 `候选中选择什么` 的问题，而不是 `学到了什么` 的问题？

## 来源与参考资料

- Yoshua Bengio et al., `A Neural Probabilistic Language Model`, JMLR, 2003, 确认日期：2026-07-19. [https://jmlr.csail.mit.edu/papers/v3/bengio03a](https://jmlr.csail.mit.edu/papers/v3/bengio03a){: target="_blank" rel="noopener noreferrer" }
- Tomas Mikolov et al., `Recurrent Neural Network Based Language Model`, Interspeech, 2010, 确认日期：2026-07-19. [https://www.isca-archive.org/interspeech_2010/mikolov10_interspeech.html](https://www.isca-archive.org/interspeech_2010/mikolov10_interspeech.html){: target="_blank" rel="noopener noreferrer" }
- Alec Radford et al., `Improving Language Understanding by Generative Pre-Training`, OpenAI, 2018, 确认日期：2026-07-19. [https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf){: target="_blank" rel="noopener noreferrer" }
- Tom B. Brown et al., `Language Models are Few-Shot Learners`, arXiv, 2020, 确认日期：2026-07-19. [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }
