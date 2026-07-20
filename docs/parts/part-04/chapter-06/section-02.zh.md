# P4-6.2 按问题类型区分的评价标准

> Section ID: `P4-6.2`
> Version: `v2026.07.19`

在 P4-6.1 里，我们看过评价指标(metric)不只是记分牌，而是会暴露出我们把什么看得更重要的标准。接下来就要进入下一个问题。`为什么问题一变，先看的指标也会跟着变？`

答案很简单。因为 model 产出的 output 不同，而这个 output 接到的判断也不同。classification 是挑选类别的问题，regression 是预测数字的问题，clustering 是把相似东西分组的问题。因此，`做得好` 的意思也不可能完全一样。

## 本节范围

这一节是按 classification、regression、clustering 来整理为什么评价标准会不同的导入节。这里把每种问题类型下应该先想到的问题和代表指标接起来。像 ROC curve、PR curve、log loss、calibration、silhouette coefficient 这类入门说明，会另外在 P4-6.4 补充学习里回收；而聚类质量的解释，会在 P4-17.1 和 P4-17.2 再重新接回来。

正文核心范围先放在下面这些点上：`在分类里哪种错误更痛`、`在回归里平均偏离了多少`、`在聚类里如果没有标准答案该怎么读结构`。像概率分数的可靠性解释、calibration curve、Brier score 这些更细的读取，会先留到 P4-6.4；而实际 threshold 调整与服务政策连接，则会在 P4-15.3 再回来。

这一节回答下面这些问题。

- classification、regression、clustering 在评价上到底有什么不同？
- 为什么 classification 不能只靠 accuracy 就结束？
- 为什么 regression 更关心 `偏了多少`，而不是简单的 `对/错`？
- 为什么 clustering 里 `可能根本没有标准答案` 这件事会变得重要？
- 先把问题类型分开之后，为什么会更容易读后面的算法章节？

## 本节目标

- 能说明：评价问题会随着问题类型而改变。
- 能说明：为什么 classification 的代表指标和 regression 的代表指标不同。
- 能说明：clustering 往往因为没有 label 而必须更谨慎地评价。
- 能为后面学习 linear regression、logistic regression、k-NN、decision tree 等算法时会跟上的评价问题做好准备。

## 学习背景

### 先把问题类型分开

scikit-learn 文档会按问题目标来分评价函数。它把 classification metrics、regression metrics、clustering metrics 分开说明，这本身就是一个重要提示。意思是：在同一个 `performance` 这个词下面，其实藏着不同的问题。

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-2-mermaid-01-zh.mmd"
```

这张图说明：只要先把问题类型选出来，接下来应该读的评价问题也会自然不同。这里先该抓住的，不是指标名字本身，而是 `当前处理的 output 到底是类别、数字，还是分组` 这个区分。

这一节先固定的标准，是下面这张表。

| 问题类型 | model 输出 | 先抛出的评价问题 | 常见代表指标 |
| --- | --- | --- | --- |
| classification | 类别或类别概率 | 哪一类错误要优先减少？ | accuracy, precision, recall, F1 |
| regression | 连续数字 | 预测值离真实值有多远？ | MAE, MSE, RMSE, R² |
| clustering | 分组结构、cluster ID | 真的把相似东西分在一起了吗？ | ARI/FMI 这类比较指标，silhouette |

这里读者最容易混淆的一点是：`只要 output 的形状不同，好结果的含义也会跟着变。`

按问题类型来看的评价顺序，可以先简短固定成下面这样。

| 问题类型 | 先看什么 | 紧接着要问什么 | 和 baseline 连接的地方 |
| --- | --- | --- | --- |
| classification | confusion matrix 和代表错误案例 | 哪种 FP/FN 更痛，precision 和 recall 该先看哪一个？ | 在 P4-8.2 里，会把这种错误结构的改善再和 baseline 比较，看是否真的有意义。 |
| regression | 代表误差大小与大误差区间 | 平均偏了多少，大失败集中在哪些地方？ | 会拿去和 `只说平均值` 的简单 baseline 比较。 |
| clustering | cluster 内部紧密度与 cluster 之间分离度 | 这个分组真的有结构吗，人能不能解释？ | 后面章节会再确认，是否能与人的标准 label 或简单分割相比。 |

| 问题类型 | 输入例子 | 输出例子 | `做得好` 的意思 |
| --- | --- | --- | --- |
| classification | 邮件内容、客户信息、图像像素 | spam/正常、流失/留存、猫/狗 | 选对了类别 |
| regression | 面积、位置、过去价格 | 5.2 亿韩元、37 分钟、21.3 度 | 把数字差距压小了 |
| clustering | 购买记录、点击模式、传感器数据 | 第 1 群、第 2 群、第 3 群 | 把相似东西分到了一起 |

也就是说，classification 更接近 `贴名字标签的问题`，regression 更接近 `对准数字刻度的问题`，clustering 更接近 `寻找人没有预先命名的分组的问题`。

## 主要学习内容

### classification 里先看错误类型

在 classification 里，如果只把预测结果读成 `对了/错了`，往往是不够的。正如 P4-6.1 已经看到的，漏掉真正正类的错误和无端把负类说成正类的错误，成本可能完全不同。

scikit-learn 文档在说明 classification metrics 时，也把 accuracy、F1、confusion matrix、ROC AUC、precision-recall curve 等分开列出来。这就意味着：分类性能并不会被一个数字说完。

classification 更清楚的读取顺序是下面这样。

1. 什么是正类，什么是负类？
2. 是漏掉更痛，还是误报更痛？
3. 所以，先看的应该是 recall，还是 precision？
4. 为了看整体平衡，还需不需要把 F1 score 或其他指标一起看？

即使是同一个 classification 问题，也会出现像下面这样的问题差异。

| 场景 | 先问的问题 | 最容易先看的指标 |
| --- | --- | --- |
| 疾病筛查 | 有没有避免漏掉真正危险案例？ | recall |
| spam 拦截 | 正常邮件是不是被挡太多了？ | precision 和 recall 一起看 |
| 欺诈检测 | 漏掉和误报，到底哪一边成本更大？ | 以 recall 为中心，同时看 precision |
| 推荐点击预测 | 排序结果和 threshold 之后的表现怎样？ | 只看 accuracy 往往不够 |

所以，在 classification 里，首先要读的是 `错误的种类`。

#### 更具体地读 classification

classification 表面上看很简单，因为它只是从几个选项里挑一个。但在实际里，里面混着两层事情。

1. model 认为哪个 class 的可能性更高？
2. 这种可能性在真实服务里，会被变成什么决定？

例如，邮件过滤器可以先生成 `spam 概率 0.82` 这样的内部 score。但用户并不会直接看到概率，而是会经历 `移动到垃圾邮件箱`、`送去复核`、`保留在收件箱` 这样的决定。因此，classification 评价最终不只是读标签表，还会继续读这个决定制造出的错误结构。

读 classification 时，下面这些区分尤其重要。

| 区分 | 问题 | 为什么重要 |
| --- | --- | --- |
| class 本身 | 在预测什么类别？ | 问题定义会变 |
| 正类与负类 | 什么被当成 `必须抓到的对象`？ | precision 和 recall 的解释会变 |
| threshold | 从几分开始算正类？ | 即使同一个 model，结果也会变 |
| 错误成本 | FP 和 FN 哪个更痛？ | 先看的指标会变 |

例如，在医疗筛查里，`把太多案例说成正类` 可能比 `漏掉真正病人` 的问题更小。反过来，在自动批准系统里，`把危险对象错放过去` 可能更严重。因此，classification 既是 `选类别的问题`，也是 `管理错误种类的问题`。

#### classification 的社会现象与工作例子

classification 是现实里最广泛使用的问题类型之一。原因在于，很多制度和服务最终都靠 `通过/保留`、`正常/异常`、`允许/拦截`、`批准/拒绝` 这样的类别判断来运转。

| 场景 | 输入例子 | 输出例子 | 为什么评价敏感 |
| --- | --- | --- | --- |
| 福利对象初筛 | 收入、家庭信息、申请历史 | 支援优先/后序 | 漏掉需要帮助的人会产生社会损失 |
| 招聘简历自动分类 | 简历、经历、资格 | 进入下一阶段/保留 | 错误淘汰会引发公平性问题 |
| 金融异常交易检测 | 支付时间、金额、位置 | 正常/可疑交易 | 漏掉会造成金钱损失，过度拦截会造成用户不便 |
| 内容举报分类 | 帖子文本、图像 | 正常/复核/删除候选 | 既要小心危险表达漏掉，也要小心过度拦截 |

classification 在工作系统里也非常常见。

| 工作场景 | 实际判断 | 先看的指标感觉 |
| --- | --- | --- |
| 运营 alert 分类 | 要不要拉警报 | false alarm 和 missed alert 的平衡 |
| 客户流失预测 | 要不要挑出高风险客户 | 如果 recall 低，漏掉会明显变多 |
| 不良品检验 | 通过/复检/废弃 | 比较漏掉不良与过度复检的成本 |
| spam 与 phishing 拦截 | 拦截/放行/复核 | precision 和 recall 必须一起看 |

从这些例子看，classification 更准确的理解方式，不是单纯的贴 label 技术，而是 `会改变人和组织下一步行为的技术`。

### regression 里先看误差大小

regression 是预测数字的问题。想象房价、配送时间、电力使用量、销售额、温度这些连续值就够了。在这里，重要的不是简单的 `对了/错了`，而是 `错了多少`。

scikit-learn 文档把 mean absolute error、mean squared error、R² score 等放在 regression metrics 下单独说明。这种组织本身就在说明：在 regression 里，误差大小和误差解释方式才是核心。

这里可以这样区分。

| 指标 | 读者问题 | 特点 |
| --- | --- | --- |
| MAE | 平均偏离了多少？ | 很直观 |
| MSE | 想不想对大误差惩罚得更重？ | 对大失败更敏感 |
| RMSE | 想不想把 MSE 换回原本单位来读？ | 更容易解释一点 |
| R² | 相比 baseline，到底多解释了多少？ | 看起来像解释力，但也容易误会 |

这里的重要点是：regression 的指标会和 `数字差距的解释` 连在一起。

- 在配送时间预测里，1 分钟误差和 30 分钟误差不是同一种错误。
- 在电力需求预测里，一个大误差可能会摇动整个运营计划。
- 在房价预测里，平均差多少钱往往更直观。

所以，在 regression 里，关键不是 `有没有误差`，而是 `误差有多大、成本有多高`。

#### 更具体地读 regression

因为 regression 处理的是数字，很多读者会容易把它误会成 `去对准唯一正确答案` 的问题。但实际核心是 `给出的数字离真实值有多近`。

例如，房价应该是 5 亿韩元时，预测成 5.01 亿和预测成 7 亿都算错，但不是同一种错。regression metrics 正是让这种差别被读出来的工具。

读 regression 时，会接着出现下面这些问题。

| 问题 | 为什么需要 | 对应指标 |
| --- | --- | --- |
| 平均偏离了多少？ | 看整体上的日常误差感觉 | MAE |
| 想不想对大误差惩罚得更重？ | 反映大失败特别致命的场景 | MSE, RMSE |
| 比 baseline 真的更有帮助吗？ | 看看是不是比只说平均值更好 | R² |

baseline 感觉在这里也很重要。regression 里的好 model，不是无条件地 `把值猜中了的 model`，而至少应该能说它比 `什么都不想，只说平均值的 model` 更好。R² 能帮助这种比较，但数字高并不总等于实务上已经足够。

另外，regression 也对单位非常敏感。

- 房价预测里的 MAE 100 万韩元
- 配送时间预测里的 MAE 100 万韩元

就算数字看起来一样，含义也完全不同。所以，在 regression 里，必须把 `数值本身` 和 `这是什么单位下的误差` 一起读。

#### regression 的社会现象与工作例子

regression 初学时可能比 classification 更不熟悉，但在实际工作里出现得非常频繁。原因是组织在做决策时，不只处理类别，也不断处理 `多少`、`到什么时候`、`多少个`、`多大成本` 这样的数字。

| 场景 | 输入例子 | 输出例子 | 为什么评价敏感 |
| --- | --- | --- | --- |
| 房价估计 | 面积、地区、交易历史 | 预测价格 | 大误差会扭曲交易判断 |
| 配送时间预测 | 出发地、物流量、交通情况 | 预计到达时间 | 小误差可容忍，但大延迟会打碎服务信任 |
| 电力需求预测 | 气温、时段、过去使用量 | 下一时段需求 | 大误差直接影响供给计划与成本 |
| 医院等候时间预测 | 预约量、医护人数、患者状态 | 预计等待时间 | 会影响实际运营体验与资源排布 |

从工作分析角度，regression 也很常见。

| 工作场景 | 想预测的数字 | 评价时看的感觉 |
| --- | --- | --- |
| 销售计划 | 下周销售额 | 平均偏了多少 |
| 广告运营 | 点击数、转化数、成本 | 大误差会不会摇动预算执行 |
| 制造运营 | 下一批产量 | 低估和高估的成本差多少 |
| 基础设施运营 | CPU 使用量、请求数 | 漏掉尖峰会不会直接变成运营事故 |

读 regression 例子时，不能只想 `把数字猜出来`，还要一起看 `这个数字误差会把计划和运营摇动多少`。regression 的评价既是数学误差，也是运营误差。

### clustering 里可能根本没有标准答案

clustering 会比 classification 和 regression 更陌生一些。原因很简单。clustering 往往从一开始就是在 `没有标准 label` 的状态下出发。

scikit-learn 文档在说明 clustering performance evaluation 时，也明确把 `知道标准 label` 和 `不知道标准 label` 分开解释。它也说明：这件事并不像 supervised learning 里的 precision 与 recall 那样简单。

这个区别非常重要。

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-2-mermaid-02-zh.mmd"
```

这张图的核心是：clustering 评价从一开始就分成两条路。如果有人类标准 label，就问 `和人的分法像不像`；如果没有，就问 `这个分组本身看起来合不合理`。

| 情况 | 先问的问题 | 代表性的读法 |
| --- | --- | --- |
| 有标准 label | 和人已知的区分方式像吗？ | ARI、FMI 这类比较指标 |
| 没有标准 label | 同一 cluster 内部是不是更近，不同 cluster 之间是不是更开？ | silhouette 这类内部标准 |

所以，在 clustering 里，`这是没有标准答案的评价` 本身就是核心学习点。

#### 更具体地读 clustering

clustering 可能是最抽象的。classification 有答案类别，regression 有要对准的数字，但 clustering 从一开始就需要人重新解释 `什么样的分组才算好分组`。

因此，读 clustering 时，必须把 model 做的事情分成两层。

1. 它在数据里形成了怎样的分组结构？
2. 这个分组是否也符合人能理解的区分？

例如，把客户数据拿去 clustering 之后，model 可能只会吐出 `第 1 群`、`第 2 群`、`第 3 群` 这种 ID。但这些数字本身并不会自动等于 `忠诚客户`、`流失风险客户`、`偶尔来访客户`。这些意义必须再由人去读取和解释。

下面这些区分很重要。

| 区分 | 问题 | 为什么重要 |
| --- | --- | --- |
| 无 label 的评价 | cluster 内部是否紧密，cluster 之间是否分离？ | 人不知道答案时使用的视角 |
| 有 label 的评价 | 是否接近人原本知道的区分？ | 有可比较标准时使用的视角 |
| cluster 数量的解释 | cluster 会不会太多或太少？ | 结果的可解释性会改变 |
| 给 cluster 赋意义 | cluster ID 能不能接到真实业务群体？ | 分析结果必须能转成行动 |

所以，clustering 评价必须同时考虑 `形状看起来合理吗` 和 `能解释吗`。在这一点上，clustering 比单纯读分数更像是在做 `看结构、做比较、再命名` 的解释工作。

#### clustering 的社会现象与工作例子

clustering 比起 `答对既有答案`，更接近 `找出隐藏结构`。因此，它很常出现在分析、政策规划、服务运营的前期。

| 场景 | 输入例子 | 输出例子 | 为什么评价敏感 |
| --- | --- | --- | --- |
| 客户细分 | 购买周期、客单价、到访频率 | 客户群 A/B/C | 即使分组出来了，如果人无法解释，实用性也很弱 |
| 地区政策分析 | 人口、收入、交通、医疗可达性 | 相似地区分组 | clustering 能帮助行政判断，但必须警惕污名效果 |
| 新闻与帖子主题探索 | 词分布、embedding | 相似文档群 | 只要 cluster 数与解释方式变了，结论就可能完全不同 |
| 设备异常模式探索 | 振动、温度、压力变化 | 相似行为群 | 后面要有依据，才能解释成异常 cluster |

在工作现场里，clustering 通常会接到下面这些问题。

| 工作问题 | clustering 做什么 | 后面人的工作 |
| --- | --- | --- |
| 客户到底会分成哪些类型？ | 把相似购买模式先分组 | 人去读每个 cluster 的特点并给它命名 |
| 异常案例集中在哪里？ | 找出和一般模式不同的分组 | 人再确认那个分组是否真的危险 |
| 运营日志里有没有隐藏模式？ | 把相似序列分组 | 人再把它和事故、发布、用户行为接起来 |
| 文档集合会分裂成哪些主题？ | 把相似文档分组 | 人再把 cluster 解释成主题或业务分类 |

所以，clustering 更应该理解成：它不是 `model 一路把答案给完的问题`，而是 `先把结构暴露出来，好让人继续解释的问题`。

## 细部学习内容

### 如果期待同一种数字，会产生误解

有时会这样想。

- classification 也有 score
- regression 也有 score
- clustering 也有 score
- 那是不是反正数字大就代表更好？

如果这样读，就会漏掉关键差异。

| 问题类型 | 数字在说什么 | 容易误解的点 |
| --- | --- | --- |
| classification | 制造了多少种预测错误 | 很容易误以为高 accuracy 就够了 |
| regression | 数字误差平均有多大 | 很容易忽略单位和成本差异 |
| clustering | 分组结构看起来有多合理 | 很容易假定一定存在标准答案 |

所以，在看 metric 之前，第一件事应该是先确认 `这个 model 在预测什么？`

按问题类型来看的评价，首先抛出的评价问题，会由 `当前这个 model 在预测什么` 决定。

| 当前问题类型 | 先抛出的评价问题 | 代表性出发指标 |
| --- | --- | --- |
| classification | 哪一种错误更该优先减少？ | accuracy, precision, recall, F1 |
| regression | 数字平均偏离了多少？ | MAE, RMSE |
| clustering | 分组是否紧密而且分离？ | silhouette 或 label 比较指标 |

## 案例与示例

### 案例 1. 即使是同一份客户数据，只要问题变了，评价标准就会变

服务团队正拿着同一份客户数据讨论几项任务。人首先会把业务问题分开，比如 `要不要找出会流失的客户`、`要不要预测下个月购买额`、`要不要把相似客户群分出来`。

问题出在：因为数据集相同，就期待同一种性能数字。流失预测是 classification，所以要看漏掉和误报；购买额预测是 regression，所以要看偏离了多少；客户细分是 clustering，所以要看在没有标准 label 的情况下，这种分组是否还能被解释。如果都被放进同一个 `score` 词里，判断标准就会变模糊。

这里，区分问题类型，就是改变评价标准的起点。如果是 classification，就先看 precision/recall/F1 方向的问题；如果是 regression，就看 MAE、RMSE 这类误差大小；如果是 clustering，就要把 silhouette 和人的解释可能性一起看。

可检验的结果也会读得不同。即使面对同一份客户数据，classification 要检查漏掉的正类数量，regression 要检查平均误差大小，clustering 要检查 cluster 内部紧密度和 cluster 之间分离度。换句话说，最先要变的不是数据，而是问题。

把同一张客户表分成不同评价问题的场景画出来，会更清楚。

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-2-mermaid-03-zh.mmd"
```

## 案例与示例

### 再用很短的场景对比来读一次

即使是同一份数据任务，只要问题类型变了，读者会先问的问题也会完全不同。

| 同一个工作场景 | 作为 classification 来看 | 作为 regression 来看 | 作为 clustering 来看 |
| --- | --- | --- | --- |
| 客户数据 | 能不能分成流失/留存？ | 能不能预测下个月购买额？ | 能不能分成相似客户群？ |
| 邮件数据 | 能不能分成 spam/正常？ | spam 分数能打多高？ | 相似邮件类型会不会聚在一起？ |
| 传感器数据 | 能不能分成故障/正常？ | 温度或振动值能不能更准确地预测？ | 相似行为模式会不会聚在一起？ |

这张表说明：`在算法之前，必须先把问题句子改写清楚。` 同一份数据集，只要问题改变，问题类型就改变，而评价标准也会一起改变。

## 练习与示例

### 用 Python 试一试 classification

在 classification 里，只要 threshold 稍微变化一点，precision 和 recall 就可能变化。下面这个例子说明：即使是同一组 score，只要 `从几分开始算正类` 变了，结果就会变。

下面的例子使用实际标签 `y_true`、预测分数 `scores` 和多个 `threshold` 值。结果里同时确认各 threshold 下的预测结果、TP/TN/FP/FN、accuracy、precision、recall。

要确认的核心是，classification 评价不能只读 model score，还要读经过 threshold 之后的最终判断。precision 和 recall 的平衡会随着 threshold 改变。

```python
# 这个例子分别计算并比较分类、回归和聚类问题中的不同评价标准。
y_true = [1, 1, 1, 0, 0, 0, 1, 0]
scores = [0.95, 0.80, 0.55, 0.70, 0.40, 0.20, 0.45, 0.60]

def classification_metrics(y_true, scores, threshold):
    y_pred = [1 if s >= threshold else 0 for s in scores]

    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)

    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0

    return {
        "threshold": threshold,
        "pred": y_pred,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "accuracy": round(accuracy, 3),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
    }

for threshold in [0.4, 0.6, 0.8]:
    result = classification_metrics(y_true, scores, threshold)
    print("threshold =", result["threshold"])
    print("  pred      =", result["pred"])
    print("  TP TN FP FN =", result["tp"], result["tn"], result["fp"], result["fn"])
    print("  accuracy  =", result["accuracy"])
    print("  precision =", result["precision"])
    print("  recall    =", result["recall"])
```

执行结果如下。

```text
threshold = 0.4
  pred      = [1, 1, 1, 1, 1, 0, 1, 1]
  TP TN FP FN = 4 1 3 0
  accuracy  = 0.625
  precision = 0.571
  recall    = 1.0
threshold = 0.6
  pred      = [1, 1, 0, 1, 0, 0, 0, 1]
  TP TN FP FN = 2 2 2 2
  accuracy  = 0.5
  precision = 0.5
  recall    = 0.5
threshold = 0.8
  pred      = [1, 1, 0, 0, 0, 0, 0, 0]
  TP TN FP FN = 2 4 0 2
  accuracy  = 0.75
  precision = 1.0
  recall    = 0.5
```

可以这样继续做小实验。

- 把 threshold 改成 `0.5`、`0.7`、`0.9`
- 把某一个 score 稍微上调或下调
- 看看在哪些情况下 recall 会升，而 precision 会降

所以，在 classification 里，重要的是用 `model score -> threshold -> 最终判断` 这条流程来读。

### 用 Python 试一试 regression

在 regression 里，最重要的是培养一种感觉：数字到底偏了多大。特别是要亲眼看到 `一个大误差` 会把指标摇成什么样。

下面的例子使用真实值 `y_true` 和预测值 `y_pred`，输出 `absolute_errors`、`squared_errors`、MAE、MSE、RMSE。

要确认的核心是，regression metrics 是读取数字偏离程度的标准。MAE 与 MSE/RMSE 会用不同强调方式去看同一组误差。

```python
# 这个例子分别计算并比较分类、回归和聚类问题中的不同评价标准。
y_true = [10, 12, 9, 15]
y_pred = [11, 10, 8, 18]

absolute_errors = [abs(a - b) for a, b in zip(y_true, y_pred)]
squared_errors = [(a - b) ** 2 for a, b in zip(y_true, y_pred)]

mae = sum(absolute_errors) / len(absolute_errors)
mse = sum(squared_errors) / len(squared_errors)
rmse = mse ** 0.5

print("absolute_errors:", absolute_errors)
print("squared_errors :", squared_errors)
print("mae            :", round(mae, 2))
print("mse            :", round(mse, 2))
print("rmse           :", round(rmse, 2))
```

执行结果如下。

```text
absolute_errors: [1, 2, 1, 3]
squared_errors : [1, 4, 1, 9]
mae            : 1.75
mse            : 3.75
rmse           : 1.94
```

这些数字可以这样来读。

- MAE 表示平均偏了 1.75。
- MSE 会更强地反映大误差。
- RMSE 会帮助把 MSE 换回原来单位的感觉。

也就是说，在 regression 里，metric 的中心是 `错了多少`。

这一次，再塞进一个大误差。

下面的例子比较小误差预测 `y_pred_small_error` 和包含大误差的预测 `y_pred_big_error`。结果里看两种情况下的绝对误差、平方误差、MAE、MSE、RMSE 会怎样变化。

要确认的核心是，如果想对大失败惩罚得更重，MSE 和 RMSE 会反应得更敏感。即使是同一个 regression 问题，也仍然需要选择到底哪一种误差更该被重看。

```python
# 这个例子分别计算并比较分类、回归和聚类问题中的不同评价标准。
y_true = [10, 12, 9, 15]
y_pred_small_error = [11, 10, 8, 18]
y_pred_big_error = [11, 10, 8, 30]

def regression_metrics(y_true, y_pred):
    absolute_errors = [abs(a - b) for a, b in zip(y_true, y_pred)]
    squared_errors = [(a - b) ** 2 for a, b in zip(y_true, y_pred)]
    mae = sum(absolute_errors) / len(absolute_errors)
    mse = sum(squared_errors) / len(squared_errors)
    rmse = mse ** 0.5
    return absolute_errors, squared_errors, round(mae, 2), round(mse, 2), round(rmse, 2)

for name, pred in [
    ("small_error_case", y_pred_small_error),
    ("big_error_case", y_pred_big_error),
]:
    absolute_errors, squared_errors, mae, mse, rmse = regression_metrics(y_true, pred)
    print(name)
    print("  pred           =", pred)
    print("  absolute_error =", absolute_errors)
    print("  squared_error  =", squared_errors)
    print("  mae            =", mae)
    print("  mse            =", mse)
    print("  rmse           =", rmse)
```

执行结果如下。

```text
small_error_case
  pred           = [11, 10, 8, 18]
  absolute_error = [1, 2, 1, 3]
  squared_error  = [1, 4, 1, 9]
  mae            = 1.75
  mse            = 3.75
  rmse           = 1.94
big_error_case
  pred           = [11, 10, 8, 30]
  absolute_error = [1, 2, 1, 15]
  squared_error  = [1, 4, 1, 225]
  mae            = 4.75
  mse            = 57.75
  rmse           = 7.6
```

这个例子会直接抛出下面这些问题。

- 一旦放进一个大误差，哪个指标会被摇得更多？
- 想看的是平均误差，还是想更强地惩罚大失败？

所以，regression metrics 不只是告诉你 `数字错了多少`，也会帮助你选择 `哪一类错误要被看得更重`。

### 用 Python 试一试 clustering

clustering 最好是读者亲手做一遍，会更快理解。下面这个例子，是一个非常简单的实验：用距离标准把一维数值分组。

下面的例子使用一维数值列表 `points` 和多个 `gap` 值，确认 clustering 结果会怎样随着距离标准而变化。

要确认的核心是，cluster 数量和 cluster 组成会随着距离标准改变。clustering 评价必须和后面由人重新解释结果的步骤一起读。

```python
# 这个例子分别计算并比较分类、回归和聚类问题中的不同评价标准。
points = [1.0, 1.2, 1.4, 4.8, 5.0, 8.5]

def cluster_by_gap(points, gap):
    clusters = [[points[0]]]

    for value in points[1:]:
        if value - clusters[-1][-1] <= gap:
            clusters[-1].append(value)
        else:
            clusters.append([value])

    return clusters

for gap in [0.3, 0.6, 1.5]:
    print("gap =", gap)
    print("  clusters =", cluster_by_gap(points, gap))
```

执行结果如下。

```text
gap = 0.3
  clusters = [[1.0, 1.2, 1.4], [4.8, 5.0], [8.5]]
gap = 0.6
  clusters = [[1.0, 1.2, 1.4], [4.8, 5.0], [8.5]]
gap = 1.5
  clusters = [[1.0, 1.2, 1.4], [4.8, 5.0], [8.5]]
```

接下来，可以稍微改一改数值，看看 clustering 标准怎么变化。

- 在 `points` 里加入 `6.1`
- 把 `gap` 改成 `2.0`
- 看看在什么时刻 cluster 数量会突然减少

例如，如果加入 `6.1`，同时把 `gap = 1.5`，那么 `[4.8, 5.0, 6.1]` 就可能被读成一个 cluster。也就是说，clustering 更接近的不是 `把标准答案算对`，而是 `实验相似性的标准应该放在哪里`。

## 检查清单

- 能不能说明为什么 classification、regression、clustering 对 `好结果` 的定义不可能一样？
- 能不能说明为什么在 regression 里，比起对错，更应该先读 `偏了多少`？
- 能不能说明为什么在 clustering 里，评价必须同时放进可解释性和结构读取，而不只是分数？
- 能不能说明只要问题类型改变，`好性能` 的含义也会跟着改变？
- 能不能说明为什么 classification 要先读错误种类，regression 要先读误差大小与成本，clustering 要先读结构解释？
- 能不能说明在挑 metric 之前，必须先检查 model 的输出和使用场景？

## 出处与参考资料

- scikit-learn developers, `Metrics and scoring: quantifying the quality of predictions`, scikit-learn User Guide, 确认日期: 2026-07-19. [https://scikit-learn.org/stable/modules/model_evaluation.html](https://scikit-learn.org/stable/modules/model_evaluation.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Clustering performance evaluation`, scikit-learn User Guide, 确认日期: 2026-07-19. [https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation](https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation){: target="_blank" rel="noopener noreferrer" }
