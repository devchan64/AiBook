# P4-6.3 补充学习：在站点可靠性工程里如何读指标(metrics)

> Section ID: `P4-6.3`
> Version: `v2026.07.12`

在 P4-6.1 和 P4-6.2 里，我们看过 model evaluation metric。现在把视线稍微往外移一点。model 拟合得好，和服务运营得好，并不是同一句话。要理解这个差别，就有必要看一看在 SRE(site reliability engineering) 里，`metric` 这个词到底是怎么被使用的。

这一节不会代替 SRE 入门书。目的只有一个：把 `读取 model 质量的数字` 和 `读取服务状态的数字` 到底在哪里相似、又在哪里分开，作为补充学习整理出来。

## 本补充学习的范围

这一节是把 machine-learning evaluation metric 和运营 metric 区分开的补充学习节。它会把 SLI(service level indicator)、SLO(service level objective)、SLA(service level agreement)、error budget，以及运营里常看的 latency、traffic、errors、saturation，用入门层次接起来。

这一节回答下面这些问题。

- 为什么好的 model 和好的 service 不是同一句话？
- machine-learning metric 和 SRE metric 有什么不同？
- SLI、SLO、SLA 是什么关系？
- 为什么在运营里，比起只看 mean，更会一起看 distribution、percentile、error rate？
- 为什么在 AI service 里，model 评价和 service 运营评价必须同时存在？

## 本补充学习的目标

- 能说明 model metric 与运营 metric 是不同层位(level)上的数字。
- 能在入门层次区分 SLI、SLO、SLA 的差别。
- 能说明为什么 latency、traffic、errors、saturation 是运营的基本信号。
- 能说明在 AI service 里，`回答质量` 和 `服务可靠性` 必须分开来看。

## 学习背景

### model metric 和运营 metric 到底哪里不同

在 machine learning 里，metric 主要是用来读取 prediction 结果的数字。比如 accuracy、precision、recall、MAE、RMSE 这些值，会显示 model 拟合得怎样、正在制造什么样的误差。

在 SRE 里，metric 主要是用来读取 service 真实运行状态的数字。比如 latency、error rate、throughput、availability 这些值，会显示用户现在到底在经历什么样的服务。

两者都很像的一点在于：它们都在决定 `什么被当成重要去测量`。但目标对象不同。

| 区分 | 主要在问什么 | 代表例子 |
| --- | --- | --- |
| model metric | prediction 到底有多准？哪种误差重要？ | accuracy, precision, recall, F1, MAE, RMSE |
| 运营 metric | service 跑得有多快、多稳？ | latency, error rate, throughput, availability |

model metric 更接近答案质量，运营 metric 更接近服务状态。

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-3-mermaid-01-zh.mmd"
```

这张图的核心是：即使在同一个 AI service 里，也会同时存在两种 metric。

## 主要学习内容

### 好的 model 不等于好的 service

这个区分在 AI service 里尤其重要。

例如，一个 chatbot service 会同时收到下面两个问题。

1. 回答是否合适？
2. 回答是否按时到达？

第一个是 model 质量问题，第二个是 service 运营问题。

| 情况 | model 视角的问题 | 运营视角的问题 |
| --- | --- | --- |
| chatbot | 回答是否接近事实、是否有用？ | 响应时间是不是太长？ |
| spam classification API | 有没有把 spam 抓对？ | 失败率和处理时间是否稳定？ |
| recommendation service | 推荐结果是否贴近用户行为？ | 即使流量涌入，也能无延迟响应吗？ |
| search service | 有没有展示相关结果？ | 能否在没有故障的情况下持续搜索？ |

也就是说，就算 model 表现很好，只要 latency 很长或者失败率很高，service 质量仍然可能很低。反过来，就算 service 很快很稳，只要 prediction 一直错，产品目标还是达不成。

#### 把同一个 service 分成两个层位来读的例子

关键点在于：即使是同一个 service，问题也会分成两类。哪怕只看一个 chatbot，也可以这样读。

| 同一个 chatbot service | model 团队先看的问题 | 运营团队先看的问题 |
| --- | --- | --- |
| 一般咨询回答 | 回答是否符合语境、是否有用？ | 即使负载拥挤时也还稳定吗？ |
| 危险问题应对 | 对危险回答的拦截做得好吗？ | 加上安全过滤后 timeout 会不会增加？ |
| 多语言支持 | 不同语言之间的质量差距大吗？ | 某个地区流量暴增时还不会出故障吗？ |
| 工具调用 | 有没有选对合适的工具？ | 外部 API 失败会不会扩散成整体响应失败？ |

所以，即使面对同一个产品，`它回答得好不好` 和 `用户实际体验是不是还能忍受` 也是不同的评价问题。

把两种情况对照起来，差别会更直观。

| 情况 | model metric 的样子 | 运营 metric 的样子 | 解读 |
| --- | --- | --- | --- |
| A | 回答质量高 | latency 高，timeout 增加 | 可能是好 model，但会变成坏 service |
| B | 回答质量低 | latency 低，availability 高 | 可能是稳定 service，但达不到产品目标 |

这个对照会给出一种感觉：`AI service 质量 = model 质量 + 运营质量`。

只要先确认 `当前问题是 prediction 质量问题，还是 service 状态问题`，model metric 和运营 metric 的区分就会更容易整理。

| 当前在看的问题 | 先抛出的提问 | 更接近的 metric 层位 |
| --- | --- | --- |
| 回答对不对、分类准不准 | prediction 质量够不够？ | model metric |
| 响应变慢了、失败变多了 | service 状态是不是用户还能忍受？ | 运营 metric |
| 回答明明不错，但用户不满很高 | 是质量问题，还是运营问题？ | 两边都要一起看 |

### SLI、SLO、SLA 到底怎么不同

Google SRE Book 会把 SLI、SLO、SLA 分开定义。这个区分很重要。三个词看起来相似，但问的问题不同。

- SLI(service level indicator): 要测量什么？
- SLO(service level objective): 想把这个测量值维持在什么水平？
- SLA(service level agreement): 如果这个承诺没做到，会有什么后果？

如果拿同一个 service 来举例，可以这样读。

| 术语 | 读者问题 | 例子 |
| --- | --- | --- |
| SLI | 到底看哪个数字？ | 请求延迟、错误率、可用性 |
| SLO | 想把这个数字维持在什么水平？ | p95 latency 低于 300ms，成功率高于 99.9% |
| SLA | 做不到会发生什么？ | 退款、credit、合同补偿 |

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-3-mermaid-02-zh.mmd"
```

看这条流程，就能知道：在运营里读数字，不只是观察，它还会接到 `要承诺什么、没做到时要怎样反应` 的结构上。

### error budget 又多了什么

只要定了 SLO，error budget 的概念就会自然跟上来。非常简单地说，它是把 `不必完美也可以的范围` 用数字先定出来。

例如，可用性目标如果是 99.9%，那么剩下的 0.1% 就是允许失败的范围。这个概念会同时带来两件事。

1. 它不会强迫人去追求不现实的 100% 完美。
2. 但它也不会让人直接忽视失败。

| 问题 | error budget 在做什么 |
| --- | --- |
| 到底允许多少失败？ | 它把允许范围用数字显示出来 |
| 现在是不是运营得太危险？ | 它让人去看剩余失败空间还有多少 |
| 还能不能更激进地部署？ | 它帮助平衡 service 可靠性与开发速度 |

所以，error budget 不是 `允许失败的概念`，而是 `把失败控制在可管理范围里的概念`。

#### 用工作感觉来读 error budget

error budget 听起来很抽象。但实际上，它可以被读成一种标准：`现在还能继续激进地改，还是该先把稳定化放在前面？`

| 情况 | 当 error budget 还很宽裕时 | 当 error budget 几乎没有时 |
| --- | --- | --- |
| 新功能部署 | 可以尝试更多实验和部署 | 应该更保守地运营 |
| model 替换 | 还有测试新 model 的空间 | 可能要把稳定化排在质量改进前面 |
| 基础设施变更 | 可以推进结构改进工作 | 可能要推迟故障风险大的变更 |

所以，error budget 不只是运营团队的数字，它也是产品团队和开发团队一起读的 `变更速度信号`。

### 为什么运营里会比平均值更看分布和百分位

Google SRE Book 说明，在运营里，简单的 mean 很可能会把重要事实盖住。特别是 latency，只看平均值，很容易把长尾区间藏起来。

例如，平均响应时间即使是 100ms，只要有一部分请求会拖到 5 秒，用户仍然会觉得服务很慢。所以在运营里，经常会看 p95、p99 这样的 percentile。

可以先整理成下面这样。

| 读取数字的方式 | 它显示什么 | 为什么重要 |
| --- | --- | --- |
| 平均值(mean) | 整体中心感 | 可以快速做简单概括 |
| 中位数(median, p50) | 一般用户的体验 | 不容易被极端值拉动 |
| p95, p99 | 缓慢长尾区间 | 能暴露部分用户的糟糕体验 |

也就是说，在运营里读数字，并不只是在问 `平均上还好吗？`，而是在同时问 `最难受的那一段到底有多严重？`

### SRE 的四个基本信号

Google SRE Book 把 latency、traffic、errors、saturation 提出为面向用户系统里特别重要的四个基本信号。

| 信号 | 读者问题 | 直觉 |
| --- | --- | --- |
| latency | 响应要花多久？ | 一旦变慢，用户会立刻感觉到 |
| traffic | 现在进来了多少请求？ | 看需求到底有多大 |
| errors | 失败了多少？ | 看服务错了多少、停了多少 |
| saturation | 系统有多满？ | 看是不是快碰到极限了 |

这四个信号可以当成运营视角里的基本坐标。

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-3-mermaid-03-zh.mmd"
```

这张图不是把四个信号当成并列列表来背，而是按运营团队真实读取的顺序来呈现。先通过 traffic 看 `现在进来了多少请求`，再通过 saturation 看 `系统是不是逼近极限`。只要逼近极限，latency 和 errors 就会作为用户可感知的问题冒出来，最后把服务可靠性一起摇动。反过来，如果 saturation 不高，就可以通过 latency 是否保持稳定来确认正常状态。

这四个信号并不会代替 machine-learning metric。它们是在帮助确认：`好的 model 是否真的被传递成了好的用户体验。`

#### 把四个信号代入 AI service 场景

四个信号与其抽象记忆，不如代入场景会更容易留下来。

| 信号 | 在 chatbot service 里的读取例子 | 在 classification API 里的读取例子 |
| --- | --- | --- |
| latency | 回答是在 1 秒内回来，还是经常拖到 8 秒？ | 分类结果能不能在实时请求里返回？ |
| traffic | 现在同时有多少人在发问？ | 每秒进来多少分类请求？ |
| errors | timeout、5xx、工具调用失败是不是在增加？ | 请求失败、响应格式错误是不是在增加？ |
| saturation | GPU、CPU、内存、连接池是不是快满了？ | worker 数、队列长度、网络是不是快到极限？ |

看完这张表，会更清楚地感觉到：运营 metric 读的是 `系统撑不撑得住`。

## 细部学习内容

### 了解 SRE metric，也会让 machine-learning metric 没那么陌生

如果 software engineer 已经熟悉 SRE metric，那么 machine-learning metric 也会更容易被接受成另一类判断数字。

- 看 latency 时，会问 `什么东西慢了？`
- 看 error rate 时，会问 `什么东西经常失败？`
- 看 precision 和 recall 时，会问 `哪一类 prediction 错误更成问题？`

也就是说，两个世界最终都在决定：`要测量什么`、`要减少哪种失败`、`要按什么标准反应`。差别只是在于，对象到底是 model 还是 service。

## 案例与示例

### 案例 1. 回答质量变好了，但 chatbot 投诉还是不降

运营团队改进了一个咨询 chatbot。按人的判断，回答内容更丰富了，内部离线评价里，分类准确度和回答适切性也都更好了。

但是，真实用户投诉并没有下降。原因一查，发现高峰时段响应延迟拉长，timeout 也变多，所以即使有好回答，也经常来得太晚。这个场景说明：model metric 和运营 metric 看的是不同层位。

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-3-mermaid-04-zh.mmd"
```

这里，model metric 读的是 `答案质量`，运营 metric 读的是 `服务体验`。即使回答适切性很高，只要 latency 和 error rate 很差，服务质量仍会被感受到很低。反过来，就算服务很快，如果答案不准确，目标同样达不成。

真正可检查的结果，会在把两类数字并排放时出现。只要把 p95 latency、timeout rate、availability 和离线评价分数放在一起看，就能解释为什么 `好 model` 并不直接等于 `好 service`。

## 案例与示例

### 再用社会现象与工作例子来读一次

从 SRE 视角来的 metric，不只是服务器数字，它们会接到真实服务体验上。

| 场景 | model metric 主要在问什么 | 运营 metric 主要在问什么 |
| --- | --- | --- |
| 医疗咨询 chatbot | 回答是否合适？有没有漏掉危险症状？ | 响应延迟会不会太长？故障会不会太频繁？ |
| 福利咨询系统 | 分类和推荐是否合适？ | 即使在申请高峰时段，也还能撑住吗？ |
| 金融欺诈检测 API | 有没有尽量不漏掉欺诈？ | 能不能在没有延迟的情况下处理实时交易流？ |
| 公共民愿分类服务 | 有没有把民愿送到正确部门？ | 接入高峰时失败率会不会飙升？ |

在工作现场里，可以这样来读。

| 工作问题 | 用 model metric 来看什么 | 用运营 metric 来看什么 |
| --- | --- | --- |
| 结果对不对？ | precision, recall, F1, RMSE | 不能直接回答 |
| 用户会不会一直等？ | 不能直接回答 | latency, timeout rate |
| 故障是不是常常发生？ | 不能直接回答 | error rate, availability |
| 能不能扛住流量暴增？ | 不能直接回答 | traffic, saturation |

这张表想说明的核心很简单。

`model metric 和运营 metric 不是竞争关系，而是回答不同问题的互补关系。`

#### 把社会现象例子读得再具体一点

越是带有社会影响的服务，就越能清楚看出为什么两层 metric 必须一起读。

| 场景 | 如果只看 model 质量，容易漏掉什么 | 如果只看运营质量，容易漏掉什么 |
| --- | --- | --- |
| 医疗咨询 chatbot | 对危险症状的回答仍可能不准确 | 服务就算很快，也可能给出错误引导 |
| 福利咨询系统 | 需要支持的人可能被错误分类 | 服务再稳定，也可能不断重复错误引导 |
| 金融欺诈检测 | 可能漏掉欺诈，也可能过度封锁正常交易 | 如果实时 API 太慢，整条交易流都会被拖慢 |
| 公共民愿分类 | 民愿可能被送错，造成行政延迟 | 分类就算对了，接入高峰时一旦故障，市民体验仍会变差 |

也就是说，在和社会现象连接的系统里，`判断正确` 和 `运营撑得住` 必须一起存在。

#### 换成技术现场里更容易直接想到的例子

如果改写成更靠近技术现场的例子，可以这样读。

| 系统 | model metric 例子 | 运营 metric 例子 | 实际判断 |
| --- | --- | --- | --- |
| spam classification API | precision, recall, F1 | p95 latency, error rate | 就算抓得准，如果太慢也会阻碍邮件流 |
| recommendation system | 和点击率、转化率相关的离线质量 | throughput, availability | 推荐质量再好，峰值时段一出故障，意义也会变弱 |
| search ranking service | relevance、NDCG 这类质量指标 | tail latency, saturation | 结果质量和响应速度必须一起看 |
| anomaly detection system | 是否减少了 false negative | alert noise, queue delay | 探测得再好，如果警报太慢或太多，运营团队也撑不住 |

## 练习与示例

### 用 Python 读 p95 latency

只看平均值，会漏掉什么，在运营里会非常直观。下面这个例子说明：只要有几个请求特别慢，mean 和 p95 的读法就会分开。

问题场景：

- 在运营指标里，只看平均值会把少数特别慢的请求藏起来

输入(input)：

- 请求延迟时间列表 `latencies_ms`

期望输出(output)：

- 排序后的延迟时间列表
- 平均 latency
- p95 latency

确认概念：

- 平均值和百分位数显示的是不同的用户体验
- 要读 tail latency，就需要 p95 这类指标

```python
latencies_ms = [95, 100, 98, 102, 97, 105, 99, 101, 96, 110, 480, 520]

sorted_latencies = sorted(latencies_ms)
mean_latency = sum(sorted_latencies) / len(sorted_latencies)

index_95 = int(len(sorted_latencies) * 0.95) - 1
index_95 = max(0, min(index_95, len(sorted_latencies) - 1))
p95_latency = sorted_latencies[index_95]

print("sorted latencies:", sorted_latencies)
print("mean latency    :", round(mean_latency, 2), "ms")
print("p95 latency     :", p95_latency, "ms")
```

执行结果如下。

```text
sorted latencies: [95, 96, 97, 98, 99, 100, 101, 102, 105, 110, 480, 520]
mean latency    : 158.58 ms
p95 latency     : 480 ms
```

这个例子会自然抛出下面这些问题。

- 平均只有 158ms 左右，为什么用户仍然可能觉得特别慢？
- 少数慢请求到底会把用户体验摇成什么样？

可以直接这样实验。

- 把 `480`、`520` 改成 `180`、`220`
- 再多加一个慢请求
- 看看是平均值先明显变化，还是 p95 先明显变化

也就是说，运营里之所以要看 percentile，是因为它能把 `看起来多数时候都还行的平均值` 背后藏着的慢尾巴揭出来。

### 用 Python 读 error budget

如果只把 error budget 当概念来听，它会很抽象。下面这个例子，是把非常简单的成功/失败记录拿来，练习计算 SLO 和剩余 budget。

问题场景：

- 只读定义时，error budget 太抽象，所以最好从成功/失败记录里直接算一次允许失败率和实际失败率

输入(input)：

- 请求成功/失败记录 `requests`
- 目标 SLO `slo_target`

期望输出(output)：

- 总请求数
- availability
- 允许失败率
- 实际失败率
- 剩余 budget

确认概念：

- error budget 能把允许失败范围用数字读出来
- 如果 remaining budget 变成负数，就说明失败已经超过目标

```python
requests = [
    "ok", "ok", "ok", "ok", "ok",
    "ok", "ok", "fail", "ok", "ok",
    "ok", "fail", "ok", "ok", "ok",
    "ok", "ok", "ok", "ok", "ok",
]

slo_target = 0.95

total_requests = len(requests)
successful_requests = sum(1 for item in requests if item == "ok")
availability = successful_requests / total_requests
error_budget = 1 - slo_target
actual_failure_rate = 1 - availability
remaining_budget = error_budget - actual_failure_rate

print("total requests      :", total_requests)
print("successful requests :", successful_requests)
print("availability        :", round(availability, 3))
print("slo target          :", slo_target)
print("allowed failure rate:", round(error_budget, 3))
print("actual failure rate :", round(actual_failure_rate, 3))
print("remaining budget    :", round(remaining_budget, 3))
```

执行结果如下。

```text
total requests      : 20
successful requests : 18
availability        : 0.9
slo target          : 0.95
allowed failure rate: 0.05
actual failure rate : 0.1
remaining budget    : -0.05
```

这个结果可以读成：`当前失败率已经超过了允许范围。`

可以直接这样实验。

- 少掉一个 `"fail"`
- 把 `slo_target` 改成 `0.99`
- 在请求数不变、失败数略微变化时，看看 remaining budget 会怎样变

所以，error budget 不是模糊的不安，而是一种能把 `允许范围还剩没剩` 用数字读出来的方法。

### 用 Python 把 model 质量和运营质量放在一起读

现在，把同一个服务里的两类数字放到一起读。

问题场景：

- 在 AI service 里，model 质量和运营状态都很重要，所以需要练习把两类数字一起读

输入(input)：

- 各案例的 precision、recall
- 各案例的 p95 latency、error rate

输出(output)：

- 各案例的 model 质量判断
- 各案例的 service 状态判断
- 把两类数字一起读后的解释句子

确认概念：

- 好的 model 并不会立刻变成好的 service
- model metric 和运营 metric 是不同层位的判断标准

```python
service_cases = [
    {
        "name": "case_A",
        "precision": 0.91,
        "recall": 0.88,
        "p95_latency_ms": 420,
        "error_rate": 0.06,
    },
    {
        "name": "case_B",
        "precision": 0.72,
        "recall": 0.68,
        "p95_latency_ms": 180,
        "error_rate": 0.01,
    },
]

model_precision_threshold = 0.85
model_recall_threshold = 0.85
latency_threshold_ms = 250
error_rate_threshold = 0.02

for case in service_cases:
    model_ok = (
        case["precision"] >= model_precision_threshold
        and case["recall"] >= model_recall_threshold
    )
    service_ok = (
        case["p95_latency_ms"] <= latency_threshold_ms
        and case["error_rate"] <= error_rate_threshold
    )

    if model_ok and not service_ok:
        interpretation = "model is strong, but service reliability is weak"
    elif not model_ok and service_ok:
        interpretation = "service is stable, but model quality is weak"
    elif model_ok and service_ok:
        interpretation = "model quality and service reliability are both acceptable"
    else:
        interpretation = "both model quality and service reliability need work"

    print(case["name"])
    print(
        "  model quality :",
        "good" if model_ok else "needs work",
        f"(precision={case['precision']}, recall={case['recall']})",
    )
    print(
        "  service state :",
        "stable" if service_ok else "unstable",
        f"(p95 latency={case['p95_latency_ms']}ms, error rate={case['error_rate']})",
    )
    print("  interpretation :", interpretation)
```

执行结果如下。

```text
case_A
  model quality : good (precision=0.91, recall=0.88)
  service state : unstable (p95 latency=420ms, error rate=0.06)
  interpretation : model is strong, but service reliability is weak
case_B
  model quality : needs work (precision=0.72, recall=0.68)
  service state : stable (p95 latency=180ms, error rate=0.01)
  interpretation : service is stable, but model quality is weak
```

这个例子的关键，是不要把两个案例压成一个分数。`case_A` 的 model 质量不错，但运营状态不稳；`case_B` 的 service 很稳，但 model 质量不足。也就是说，只要坏掉的是不同数字，下一步行动也应该不同。

- 在 `case_A` 里，比起 precision 和 recall，更该先修 p95 latency 和 error rate。
- 在 `case_B` 里，比起基础设施，更可能要先做 model 改进或数据质量检查。
- 最终，在 AI service 运营里，只有把 `是 model 弱了` 还是 `是 service 弱了` 分开来读，下一步措施才会更清楚。

## 检查清单

- 能不能说明为什么 `好 model` 和 `好 service` 不是同一句话？
- 能不能区分当前遇到的问题是 precision/recall 问题，还是 latency/error-rate 问题？
- 能不能用入门层次说明 SLI、SLO、SLA 各自在问什么？
- 能不能说明 model metric 读 prediction 质量，而运营 metric 读 service 状态？
- 能不能说明好的 model 不等于好的 service，好的 service 也不等于好的 model？
- 能不能说明在运营里，不能只看一个平均值，而要一起看 percentile、error rate、availability、saturation 等多个信号？

## 出处与参考资料

- Google SRE, `Service Level Objectives`, Site Reliability Engineering Book, 确认日期: 2026-06-26. [https://sre.google/sre-book/service-level-objectives/](https://sre.google/sre-book/service-level-objectives/){: target="_blank" rel="noopener noreferrer" }
- Google SRE, `Monitoring Distributed Systems`, Site Reliability Engineering Book, 确认日期: 2026-06-26. [https://sre.google/sre-book/monitoring-distributed-systems/](https://sre.google/sre-book/monitoring-distributed-systems/){: target="_blank" rel="noopener noreferrer" }
