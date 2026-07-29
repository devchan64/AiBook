# P4-10.2 线性回归(linear regression)的评价与局限

> Section ID: `P4-10.2`
> Version: `v2026.07.26`

P4-10.1 把 linear regression 介绍成 `先用直线来读取关系的模型`。现在要进入下一个问题。

那条直线到底拟合得有多好？又会从哪里开始变得容易出错？

这正是 evaluation 与 limit 的出发点。

学完 linear regression 之后，读者常常停在 `系数看起来挺合理`、`预测值看起来差不多` 这样的层次。但在算法章节里，必须再往前走一步。要一起看 prediction 与 reality 的差该怎样读、该用什么 [metric](/AiBook/zh/reference/concept-glossary-pinyin/m/#metric) 来总结、以及直线假设会在什么时候变得吃力。

所以，这一节不是停在 `画出了一条直线`，而是进入 `那条直线到底解释了多少数据`。

本节不会长篇重复 linear regression 的基本定义。`用直线读取关系的模型` 这个核心直觉，继续通过 P4-10.1 和 [linear regression](/AiBook/zh/reference/concept-glossary-pinyin/l/#linear-regression) 条目接回来；这里则把焦点放在评价与局限上。

## 线性回归评价与局限先收束的问题

这一节回答下面这些问题。

- residual 和 [error](/AiBook/zh/reference/concept-glossary-pinyin/e/#error) 应该怎样理解？
- 说 linear regression 的 prediction `拟合得好`，到底是什么意思？
- 在入门层面，MAE、MSE、RMSE、R² 应该怎样区分？
- 当直线假设失效时，会出现什么局限？
- linear regression 的结果应该信到什么程度，又该从哪里开始更谨慎？

这一节先用 `拟合得有多好` 和 `从哪里开始容易出错` 这两个问题收束 linear regression 的结果，并集中把 residual 和评价指标抓成判断手柄。

不过，这一节不会立刻扩展的问题也很明确。regression diagnostics、significance 和 multicollinearity 的基础阅读，会在 P4-10.3 补充学习里再整理。regularization 与相关 hyperparameter 的更大视角，也会通过 P4-9.1 和 P4-9.2 再接回来。feature engineering 的更大流程，则会通过 P4-7.1、P4-7.2、P4-18.1、P4-18.2 再连回去。

statistical significance test、residual normality 与 homoscedasticity 的严格检验、multicollinearity 诊断、更深入的 regularization 与 feature engineering，超出了当前这一节的直接范围，所以这里不会详细处理。

## 线性回归评价与局限要留下的判断标准

- 能把 residual 解释成 `真实值和预测值之间的差`。
- 能说明 MAE、MSE、RMSE、R² 分别是从什么角度看 model。
- 能区分对大误差更敏感和不那么敏感的 metric。
- 能说明 linear regression 不容易拟合好的典型场景。
- 能理解为什么不能只看一个漂亮数字就过度相信 linear regression。

## 学习背景

P4-10.1 把 linear regression 介绍成 `总结关系的第一个 model`。但只要 model 立起来，接下来就必须读取 `它到底拟合了多少`。

- 即使有一条直线，prediction error 仍然会留下。
- 只要 error 留下，就要决定怎样去总结它的大小。
- 即使 metric 看起来不错，只要直线漏掉了重要模式，model 就应该再被怀疑一次。

因此，这一节在算法章节里承担下面这些作用。

| 课程位置 | 本节作用 |
| --- | --- |
| 在 P4-10.1 之后 | 把直觉解释接到数值评价上 |
| 在 P4-6 评价指标之后 | 把 regression metric 放回真实 model 的语境里复用 |
| 在 P4-11 之后其他算法之前 | 提供 `prediction 对了吗` 和 `model 解释得好吗` 之间的区分标准 |

如果说 P4-10.1 看的还是 `model 的形状`，那 P4-10.2 就是在看 `model 留下来的差`。

在 regression evaluation 里，下面四项最好一起留下。

| 先检查什么 | 为什么要一起看 |
| --- | --- |
| baseline error | 因为必须知道这条直线是否真的比简单平均预测更好 |
| 平均误差(MAE, RMSE) | 因为必须知道整体上到底错得有多远 |
| 大失败出现的区间 | 因为平均值后面可能藏着很大的误差 |
| 代表性错误案例 | 因为必须说明 model 会在什么输入条件下反复用同一种方式失败 |

也就是说，好的 regression evaluation 不是读完一个 metric 就结束，而是要把 `有没有超过 baseline`、`平均错多少`、`哪里错得特别大`、`那种失败在什么场景里反复出现` 一起确认。

这里再固定住一点，classification 章节学过的比较框架，在 regression 里也会直接延续。 在 regression 里，baseline 可以是像简单平均预测这样的 `参考 model`，也可以是把最近 prediction error 和平时的 error distribution 摆在一起的 `比较基准线`。所以 regression evaluation 也不是只看一个绝对误差数字，而是要一起读 `现在的误差是不是比平时更大`、`是不是只在某个区间反复出现`。这里同样，首先把大误差读成变化信号，原因解释则要在回头检查缺失 feature 或区间差异之后再补上。

所以，在 regression evaluation 里，比较框架也必须保持统一。如果把 baseline error、当前 model error、最近区间的 error distribution 分别放在不同单位、不同区间下去读，就很难说清 `到底是什么真的变好了`。

| 在 regression evaluation 之前一起留下的内容 | 为什么需要 |
| --- | --- |
| baseline error | 为了先确认模型是否真的比平均预测更好 |
| 大误差聚集的区间 | 为了把藏在平均值后面的失败区间直接暴露出来 |
| 解释边界句子 | 为了避免一看到大误差就立刻把原因定死 |
| 下一步检查优先级 | 为了决定该回头查看哪个区间、补强哪个 feature |

## 主要学习内容

### residual 和 error 有什么不同

第一次看到这两个词时，它们很容易显得差不多。但在这本书里，会把它们区分成下面这样。

- residual：某一个数据点上的 `actual - prediction`
- error：泛指 model 留下来的差

例如，真实分数是 72，而 prediction 是 68，那么 residual 就是 `72 - 68 = 4`。反过来，如果真实分数是 64，而 prediction 是 67，那么 residual 就是 `64 - 67 = -3`。

这里重要的是 sign 和 size。

- 正 residual：model 预测偏低
- 负 residual：model 预测偏高
- 绝对值很大：在那个数据点上 miss 得更多

只盯着一个点看时，residual 就是 `真实点` 和 `回归线上的预测点` 之间的垂直距离。所以要读 residual，与其只盯着数字表，不如连着看 `它离那条线到底在上面还是下面、有多远`。

![用实际点与回归线之间的垂直间隔来展示残差的图](/AiBook/assets/part-04/chapter-10/p4-10-2-residual-gap-zh.svg)

把这个差简单画出来，就是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-2-mermaid-01-zh.mmd"
```

这张图让 residual 不再只是一个平面的 `失败标记`，而是一个 `带方向的差`。只有把 prediction 比 reality 低还是高一起看，读者以后才能怀疑：model 是否在某个区间里系统性地偏向某一边。

关键点是：residual 不只是 `错了`，而是在展示 `往哪个方向错了多少`。

### 说 linear regression 的 prediction 拟合得好，到底是什么意思

在 regression 里，不像 classification 那样容易直接分成 `对/错`。数值预测往往都会留下一点偏差。所以读取 regression model 时，首先看的通常不是 `它有多常正好猜中`，而是 `它平均偏离了多远`。

假设有两个 model。

| model | 误差特点 |
| --- | --- |
| Model A | 大多数时候偏 2 到 3 分 |
| Model B | 平时差不多，但偶尔会一下错 20 分 |

两者在平均上都可能看起来还可以，但在实际使用里，B 可能更危险。所以 regression evaluation 的核心，就是 `怎样去总结误差`。

也就是说，在 regression 里，`拟合得好` 往往要重新拆成下面这些问题。

- 平均偏多少？
- 大误差常不常出现？
- 它真的比 baseline 更好吗？
- 这条直线有没有漏掉结构性的模式？

### MAE、MSE、RMSE 应该怎样区分

scikit-learn 的 regression metric 文档提供了 mean absolute error、mean squared error、R² 等指标。入门时，读者比起背公式，更容易先从 `它会更重处罚哪种错误` 这个角度来理解。

#### MAE

MAE 是把 residual 的绝对值取平均。

- 它最直观。
- 很容易直接读成 `平均大概错了几分、几分钟、几单位`。
- 它不会特别夸大大误差。

所以，MAE 最朴素地展示的是 `平均错了多少`。

#### [MSE](/AiBook/zh/reference/concept-glossary-pinyin/m/#mean-squared-error-mse)

MSE 是把 residual 平方之后再平均。

- 它对大误差更敏感。
- 它会把少数大失败看得比许多小失败更重。
- 因为单位被平方了，所以解释不够直观。

所以，MSE 适合用在 `想更重地惩罚大失败` 的场景。

#### RMSE

RMSE 是在 MSE 上再开平方。

- 它保留了对大误差更敏感的优点。
- 同时又回到原本单位，解释起来更方便。

所以，RMSE 常用在 `既想对大误差敏感，又想继续用原单位解释` 的场景。

三者可以很短地整理成下面这样。

| metric | 入门式读取 |
| --- | --- |
| MAE | 平均错了多少 |
| MSE | 更重惩罚大误差的平均误差 |
| RMSE | 对大误差更敏感、但回到原单位来读的误差 |

换到工作场景里，这种差别会更清楚。

| 工作场景 | 更先看的 metric | 理由 |
| --- | --- | --- |
| 预测快递送达时间 | MAE | 因为想直接读出平均大概错几分钟 |
| 预测医院等待时间 | RMSE | 因为少数病人如果遇到特别大的延迟，需要更敏感地看见 |
| 销售额预测 | MAE + RMSE | 因为想同时看到平均偏差和大失败 |
| 设备故障时点预测 | RMSE | 因为少见的大误差会直接变成运营风险 |

所以，metric 的选择不是数学偏好问题，而是直接连接到 `哪一种错误更痛`。

### R² 展示的是什么

R² 是 linear regression 入门里经常出现的数字，但也很容易被误读。

`R² 是一个 summary value，它展示的是：这个 model 比简单平均预测多解释了多少数据。`

入门层面可以先这样读。

- 接近 1：这条直线在当前数据里解释了相当多的变动
- 接近 0：它和用平均值来预测差不多
- 也可能是负数：甚至会比平均预测更差

重要的是，R² 很容易被当成 `越高越好` 的单一分数来读。但光靠 R²，读者看不出来后面是否藏着几个大失败。所以它必须和 MAE、RMSE 这类误差 metric 一起读。

在实务里，这样的场景也很常见。比如销售额预测里，大多数普通工作日都预测得不错，但少数大型活动日会错得很大。这时，整体现象仍可能被解释得不少，所以 R² 还是很高；但运营方依然会因为那几次大失败而很难真正信任 model。

所以，R² 很擅长展示 `整体解释力`，但它不能替代 `少数大失败带来的实际体感`。

### metric 应该怎样一起读

如果 linear regression 只用一个 metric 来看，解释很容易摇晃。典型场景如下。

| 场景 | 解释风险 |
| --- | --- |
| R² 很高 | 后面可能藏着几个大误差 |
| MAE 很低 | model 仍然可能在某个区间结构性失效 |
| RMSE 很高 | 这可能是在提醒有一些大失败存在 |

把 regression evaluation 按下面这个顺序来读，会更清楚。

1. 它有没有超过 baseline？
2. 平均误差大概有多大？
3. 有没有异常大的误差？
4. residual 是否反复往同一方向偏？

把这个顺序简单画出来，就是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-2-mermaid-02-zh.mmd"
```

这张图整理的是 regression metric 的阅读顺序。好的 regression evaluation 不是看完一个数字就结束，而是要按顺序确认：它有没有超过 baseline、平均误差有多大、以及后面有没有藏着大失败。

核心就是不要停在 `有一个数字看起来不错`。

在 regression evaluation 记录里，还要把下面三句话一起留下。

- 变化已经看到了，但原因还没有定死。
- 大误差区间是一个要提高 review 优先级的信号。
- 在样本很少的区间里出现的大误差，应该更保守地解释。

这三句话其实指向同一个总原则。regression evaluation 也只有在把 `同一个 baseline、同一个区间、同一个代表失败` 摆在一起读的时候，才会变得更可解释。

### 应该先读哪个 metric

比起把所有 regression metric 一次性列出来，更重要的是根据当前最警惕哪种失败，明确阅读顺序。

| 当前关心点 | 优先看的 metric / 标准 | 理由 |
| --- | --- | --- |
| 想知道平均大概错多少 | MAE | 因为它最容易用真实单位直接读 |
| 想更敏感地看到大失败 | RMSE 或 MSE | 因为它们对大误差更重 |
| 想确认是否真的超过平均预测 | baseline error + R² | 因为要一起看改善和解释力 |
| 怀疑只在某个区间里特别容易错 | 代表错误案例 + 大误差区间 | 因为平均值看不出来隐藏失败 |
| 想看最近表现是不是在摇晃 | 最近误差 vs 平时基准线 | 因为需要一个比较框架来看 error distribution 是否变化 |

这个表的目的，不是把读者锁死在某一个 metric 上，而是根据 `现在究竟在读哪种失败`，把评价顺序讲清楚。

## 细化学习内容

### linear regression 不容易拟合好的典型场景是什么

linear regression 的局限，大多会在 `一条直线根本不够，但还是硬要拿一条直线去解释` 的场景里暴露出来。

典型场景包括：

#### 1. 关系是 nonlinear 的时候

输入变大时，输出可能一开始增加得很快，但过了某个点之后就变缓。这个时候，一条线很难同时照顾前半段和后半段。

例如，学习时间增加时，分数会上升，但超过一定学习时间之后，上升幅度可能会下降。

#### 2. 关系会随区间改变的时候

有些数据在不同区间里会换一种性质。

- 小户型和大户型的价格结构可能不同
- 短距离配送和长距离配送的时间模式可能不同

这时，把全部数据压成一条直线，平均上也许看起来还行，但在各区间里却会不断失误。

#### 3. 缺了重要 feature 的时候

有时问题不在于那条线，而在于真正需要的 feature 没有放进来。

例如，房价预测只放面积而不放位置，model 看起来像是在读面积和价格的关系，实际上却漏掉了关键结构。

#### 4. [outlier](/AiBook/zh/reference/concept-glossary-pinyin/y/#outlier) 很强的时候

linear regression 无法直接无视大误差。如果少数数据点离得特别远，整条线就可能被它们拉走，导致整体解释都摇晃起来。

实际场景里，经常会像下面这样。

- 平时配送时间都在 5 到 20 分钟之间，但某个暴雨天冲到了 90 分钟
- 大多数销售额都在 2000 万到 6000 万韩元之间，但某一次活动冲到了 20 亿韩元
- 普通房价带里混进了几套超高价顶层公寓

这些点在现实里可能是重要事件，但当读者试图用一条直线去总结整份数据时，它们也会把 model 拉得过头。

所以，linear regression 的局限，与其读成 `算法不好`，不如读成 `当前问题可能根本不适合只用一条直线来总结`。

最典型要先怀疑的，是 `真实关系本来就是弯的`，以及 `少数极端值把整条线拉偏了` 这两种情况。

![比较非线性关系与异常值拉扯，让一条直线变得吃力的两种场景的图](/AiBook/assets/part-04/chapter-10/p4-10-2-line-limit-comparison-zh.svg)

如果把这种信号压缩成实务型回顾记录，可以写成下面这样。

| 回顾中应留下的项 | 例子 |
| --- | --- |
| 相对 baseline 的变化 | `MAE 下降了，但大误差区间还在` |
| 重复出现的失败场景 | `在高值区间里持续发生低估` |
| 解释边界 | `看到了 nonlinear 可能性，但原因还需要继续检查 feature` |
| 下一步问题 | `是否该分区间建模，或者补充 feature，而不是继续强压一条线` |

## 细节补充

### 学术背景与历史

在看完评价与局限之后，读者会更清楚地理解：为什么 linear regression 会用这种方式来处理误差。它背后其实有两条历史线索。

第一条是 `least squares` 的线索。如何选择一条线或一个公式，去最好地解释带有观测误差的观测值，这在 19 世纪初的 astronomy 和 geodesy 里都非常重要。least squares 正是在这个语境里，作为系统化减小观测差异的方法快速站稳。

第二条是 `regression` 这个名字本身的线索。`regression` 这个词在 19 世纪后半，由 Francis Galton 的遗传与身高研究广泛传播。它当时用来描述极端数值会在下一代向平均值回归的倾向，后来才扩展成统计学里更一般的线性关系估计名称。

- least squares 来自 `如何减少误差的计算方法` 这条历史
- regression 来自 `如何量化关系的统计解释` 这条历史
- 今天的 linear regression，就是这两条线索合到一起的结果

知道这个背景之后，会更清楚地看到：linear regression 不只是教材里的第一个算法，而是 `处理观测误差的方法` 和 `解释关系的方法` 相遇的地方。

### 主要争议在哪里产生

只有在看完 metric 和局限之后，围绕 linear regression 的争议也才能更准确地读出来。linear regression 本身是经典工具，但围绕它的解释争议今天仍会反复出现。重要的争议主要有四类。

#### 1. 把 prediction 和 explanation 当成同一句话

即使某个 regression 式子预测得不错，也不能直接断定那个 coefficient 就在解释现实原因。具有 prediction performance，和解释 causality，是不同的问题。

这种争议在数据驱动服务里非常常见。

- 销售额预测做得不错，不等于广告费 coefficient 就证明了原因效果
- 房价预测做得不错，不等于某一个变量就决定了价格

也就是说，linear regression 能帮助解释，但不会自动证明因果。

#### 2. 把 coefficient 直接读成 importance

coefficient 的数字大，并不等于这个 feature 就更本质。scale、preprocessing、变量选择方式都会一起影响它。

这种争议在多变量回归里尤其常见。读者看线性回归系数时，比起先问 `大不大`，更应该先问 `它是按什么单位测量的`。

#### 3. 过度相信高 R²

R² 高时，model 看起来像是“解释得很好”。但几个大失败、某个区间的结构性误差、重要变量的缺失，都可能藏在高 R² 后面。

所以，R² 是有用的 summary value，但不是最后判决值。

#### 4. regression 的历史出发点与社会解释之间的问题

`regression` 这个词是和 Galton 的遗传研究一起广泛传播的，而其周边也连着今天会被批判性重看的 determinism 与 eugenics 历史。今天在统计学和机器学习里学习 linear regression 时，需要把数学工具本身，与当时的社会解释分开来读。

这虽然不是技术局限本身，但它提醒读者：`用数字解释关系` 这件事，不会自动为社会含义背书。

### 好的 linear regression 解读与坏的 linear regression 解读

linear regression 的优点之一是解释性高，但正因为如此，草率解释也更容易出现。

| 不好的解读 | 更好的解读 |
| --- | --- |
| 斜率是正的，所以它就是原因 | 看到了正向关系，但原因仍需另行检查 |
| R² 很高，所以已经足够好 | R² 虽高，但仍要一起看大误差和 residual pattern |
| coefficient 大，所以它最重要 | coefficient 必须连同单位和 preprocessing 一起读 |
| prediction 是 76.4，所以现实也会在那附近 | 当前 model 会这样估计，但误差可能性仍然存在 |

其中最重要的一句话是：

`linear regression 让解释得以开始，但不会替解释画上句号。`

## 案例及示例

### 案例 1. 平均上看起来不错，但在特定客户区间里明显失败的配送时间预测

一个物流团队正在根据配送距离和下单时间段预测到达时间。人们最先看的关系是 `距离更远时是不是更久`、`下班时段下单是不是会更晚`。

把 linear regression 跑出来之后，整体 R² 不低，MAE 看起来也还可以。表面上，model 似乎能用。但仔细看时，在长距离配送或暴雨天里 prediction 会明显偏掉，而 RMSE 也因为这些大失败而比预想更高。

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-2-mermaid-03-zh.mmd"
```

在这个场景里，regression evaluation 不是一个数字就能结束。MAE 展示的是平均偏了多少，RMSE 对少数大失败更敏感，而 R² 只是总结整体解释力有多大。因此，单看 `R² 很高` 还远远不够说明实际运营风险。

可确认的结果只有在把 residual 和 metric 一起看时才会显现出来。即使平均误差不大，只要某个区间里的 residual 明显朝一边聚集，或者大失败反复出现，就应该把它读成一个信号：linear regression 还没有把那个区间的结构解释清楚。即使是这种差异，也应先被读成 `下一个该优先检查哪个区间` 的 review 信号，而不是立刻固定原因的句子。

### 实证示例 1. 配送时间预测

假设现在要预测同一区域内的配送时间。

| model | MAE | RMSE | 解读 |
| --- | --- | --- | --- |
| Model A | 8 分钟 | 9 分钟 | 整体上比较均匀地出错 |
| Model B | 7 分钟 | 18 分钟 | 平均看起来更好，但混着一些大失败 |

这时，如果只看平均数字，B 可能看起来更好。但如果部分客户会遇到 30 分钟、40 分钟的延迟，那实际服务体感反而可能更差。

这说明：MAE 和 RMSE 必须一起读。

### 实证示例 2. 房价预测

在房价预测里，model 可能对大多数中间价位房屋预测得不错，但在极高价房屋上错得很大。

- MAE 仍然可能比较低
- RMSE 会因为那些高价房大误差而更高
- R² 也可能因为整体波动解释得不少而看起来很高

这个场景里，真正重要的问题不是 `平均上还行吗`，而是 `哪一个区间尤其危险`。

也就是说，metric 展示的是总体平均，而实务解读只有把区间级失败模式也一起看，才算完整。

## 练习与示例

### 用 Python 一起看 residual 和 metric

下面这个例子重新使用 10.1 的学习时间数据，一起查看 prediction、residual、MAE、RMSE、R²。

- 问题场景：根据学习时间预测考试成绩后，检查到底偏了多少
- 输入(input)：学习时间
- 标签(label)：真实考试分数
- 要检查的概念：
  - 每个数据点都会各自产生 residual
  - MAE 和 RMSE 用来总结 error
  - R² 展示的是：比平均预测多解释了多少

可以改动的值：

- 把 `exam_score` 的最后一个值改成 `80` 或 `90`，可以观察 residual 数组和 RMSE 会怎样变化。
- 给 `study_hours` 和 `exam_score` 各加一个新点，可以确认小数据集里的 R² 多容易晃动。

```python
# 这个例子计算线性回归预测的残差以及 MAE、MSE、RMSE 等评价指标。
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

study_hours = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
exam_score = np.array([52, 55, 61, 64, 68, 72])

model = LinearRegression()
model.fit(study_hours, exam_score)

pred = model.predict(study_hours)
residuals = exam_score - pred

print("predictions :", np.round(pred, 3))
print("residuals   :", np.round(residuals, 3))
print("MAE         :", round(mean_absolute_error(exam_score, pred), 3))
print("RMSE        :", round(mean_squared_error(exam_score, pred) ** 0.5, 3))
print("R2          :", round(r2_score(exam_score, pred), 3))
```

一个可能的输出如下。

```text
predictions : [51.714 55.829 59.943 64.057 68.171 72.286]
residuals   : [ 0.286 -0.829  1.057 -0.057 -0.171 -0.286]
MAE         : 0.448
RMSE        : 0.608
R2          : 0.992
```

这个输出可以这样读。

- residual 同时包含正值和负值，所以 model 并没有明显只朝一个方向连续失误。
- MAE 大约 `0.448`，表示平均大概偏了 0.45 分。
- RMSE 大约 `0.608`，表示对较大误差稍微更敏感的一种平均误差。
- R² 大约 `0.992`，说明在这个小例子里，这条直线对数据变动解释得相当多。

不过，即使这里也有几件事要小心。

- 这个数据集很小，也很简单。
- 它是在学习过的同一批点上再次评估的，所以和真实 generalization performance 不一样。
- 数字看起来漂亮，并不代表 linear regression 对所有 regression 问题都够用。

所以，metric 是帮助解释的工具，而不是一次就给出最终判决的工具。

### 用 Python 看 outlier 怎样摇动 metric

下面这个例子在相似模式的数据里，故意给最后一个点加上一个大错误，用来展示 MAE 和 RMSE 会怎样不同地反应。

问题场景：

- 假设大多数数据都差不多，但其中一个点特别失败

输入(input)：

- 实际值数组 `actual`
- 普通预测 `pred_good`
- 在最后一点放入大误差的预测 `pred_outlier`

期望输出(output)：

- 两种情况下的 MAE
- 两种情况下的 RMSE

要检查的概念：

- MAE 展示平均偏差
- RMSE 会对单个大失败更敏感

可以改动的值：

- 把 `pred_outlier` 的最后一个值改成 `80`、`90` 或 `100`，可以比较 MAE 和 RMSE 增长的速度。
- 把 `pred_good` 的所有值都改成比 actual 大 `+2`，可以观察没有大失败时两个 metric 会多接近。

```python
# 这个例子计算线性回归预测的残差以及 MAE、MSE、RMSE 等评价指标。
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

actual = np.array([52, 55, 61, 64, 68, 72])
pred_good = np.array([51, 56, 60, 65, 67, 73])
pred_outlier = np.array([51, 56, 60, 65, 67, 90])

print("good MAE    :", round(mean_absolute_error(actual, pred_good), 3))
print("good RMSE   :", round(mean_squared_error(actual, pred_good) ** 0.5, 3))
print("outlier MAE :", round(mean_absolute_error(actual, pred_outlier), 3))
print("outlier RMSE:", round(mean_squared_error(actual, pred_outlier) ** 0.5, 3))
```

一个可能的输出如下。

```text
good MAE    : 1.0
good RMSE   : 1.0
outlier MAE : 3.833
outlier RMSE: 7.431
```

这个输出对解释训练非常有用。

- 在 `good` prediction 里，MAE 和 RMSE 几乎一样。
- 在 `outlier` prediction 里，MAE 也变大了，但 RMSE 的反应要尖锐得多。

从实证角度看，这就把 `RMSE 更讨厌大失败` 这句话直接变成了数字。

### 再改一个值试试：如果大失败从一个点扩大到两个点，什么保持不变，什么发生变化

这次不再只让最后一个点明显失败，而是把最后两个点都改成大失败。

可以改动的值：

- 把 `pred_two_outliers` 的第五个值改成 `76`、`84` 或 `92`，可以比较单点失败和重复失败的差异。
- 也可以让前四个点中的某一个明显失败，然后记录大误差是集中在一个区间还是分散出现。

```python
# 这个例子计算线性回归预测的残差以及 MAE、MSE、RMSE 等评价指标。
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

actual = np.array([52, 55, 61, 64, 68, 72])
pred_outlier = np.array([51, 56, 60, 65, 67, 90])
pred_two_outliers = np.array([51, 56, 60, 65, 84, 90])

print("one-outlier MAE :", round(mean_absolute_error(actual, pred_outlier), 3))
print("one-outlier RMSE:", round(mean_squared_error(actual, pred_outlier) ** 0.5, 3))
print("two-outlier MAE :", round(mean_absolute_error(actual, pred_two_outliers), 3))
print("two-outlier RMSE:", round(mean_squared_error(actual, pred_two_outliers) ** 0.5, 3))
```

一个可能的输出如下。

```text
one-outlier MAE : 3.833
one-outlier RMSE: 7.431
two-outlier MAE : 6.5
two-outlier RMSE: 8.91
```

### 什么保持不变，什么发生变化

- 保持不变的点：两种情况下，RMSE 都仍然比 MAE 反应更强。`它对大失败更敏感` 这个解释保持成立。
- 发生变化的点：当大失败从一个点扩大到两个点时，MAE 也开始更快变大。这意味着 `现在平均上也错得很多` 的信号变强了。
- 最先应留下的判断：同样都是误差上升，但如果是单点事故，和如果是跨多个点重复失败，会导向完全不同的运营问题。

这个练习把 regression evaluation 从 `读数字` 重新拉回到 `读失败结构`。真正的问题，不只是误差有没有变大，而是 `在哪里`、`在几个点上`、`朝哪个方向` 变大了。比起只背 MAE 和 RMSE 的差别，更重要的是训练自己区分 `一个大失败` 和 `反复出现的失败区间`。

| 共通记录语言 | 这次练习里应该立刻留下的内容 |
| --- | --- |
| 显示出来的结构 | 单点大失败和扩散到多个点的大失败，会让 MAE 和 RMSE 以不同速度上升 |
| 解释边界 | 仅凭 RMSE 明显跳高，还不能立刻断定原因到底是一个 outlier 还是结构性缺漏 |
| 下一步问题 | 是否应该先回头检查大误差是否集中在某个区间，或缺失 feature / nonlinear pattern 是否在重复出现 |

这一节的核心不是继续背更多 regression metric 名称，而是固定 regression evaluation 到底要一起看到哪里。

| 应该一起看的内容 | 这一节先读取的问题 | 后面会再连接到哪里 |
| --- | --- | --- |
| baseline error | 直线 model 是否真的比简单平均预测更好 | P4-8 baseline 比较 |
| 平均误差与大失败区间 | 整体上错多少，哪里错得特别大 | P4-6 regression metric |
| 代表性错误案例 | 在什么输入条件下会反复用同一种方式失败 | P4-18 feature engineering，后续 regression model 比较 |

## 检查清单

- 在确认超过 baseline 之前，你是不是还在因为一个误差数字就先下结论？
- 你能说明 residual 是真实值和预测值之间的差吗？
- 你能解释 residual 的符号是什么意思吗？
- 你能把 MAE 和 RMSE 的差别说明成 `对大误差的敏感度` 吗？
- 你有没有把 R² 理解成相对于 baseline 的解释力，而不是单纯分数？
- 你有没有把平均误差和大失败区分开来读？
- 你有没有理解：如果只看一个 metric，解释会变得摇晃，所以 baseline、平均误差、大误差、residual pattern 必须一起看？
- 当大误差区间出现时，你有没有避免立刻把原因定死，而是重新检查缺失 feature 或 nonlinear 可能性？
- 你有没有理解 linear regression 的局限通常会出现在 `问题无法只用一条直线来概括` 的场景里？
- 你能举出一两个直线假设失效的场景吗？
- 你能解释为什么即使数字好看，也不应该立刻过度相信吗？

## 出处与参考资料

- scikit-learn, `1.1. Linear Models`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/linear_model.html](https://scikit-learn.org/stable/modules/linear_model.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `3.4. Metrics and scoring: quantifying the quality of predictions`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/model_evaluation.html](https://scikit-learn.org/stable/modules/model_evaluation.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `mean_absolute_error`, scikit-learn API Reference, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `mean_squared_error`, scikit-learn API Reference, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `r2_score`, scikit-learn API Reference, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html){: target="_blank" rel="noopener noreferrer" }
- NIST/SEMATECH, `4.1.4.1. Linear Least Squares Regression`, Engineering Statistics Handbook, 确认日期: 2026-07-26. [https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm){: target="_blank" rel="noopener noreferrer" }
- J. M. Bland, D. G. Altman, `Statistic Notes: Regression towards the mean`, BMJ 1994;308:1499, 确认日期: 2026-07-26. [https://www.bmj.com/content/308/6942/1499](https://www.bmj.com/content/308/6942/1499){: target="_blank" rel="noopener noreferrer" }
- National Human Genome Research Institute, `Eugenics and Scientific Racism`, 确认日期: 2026-07-26. [https://www.genome.gov/about-genomics/fact-sheets/Eugenics-and-Scientific-Racism](https://www.genome.gov/about-genomics/fact-sheets/Eugenics-and-Scientific-Racism){: target="_blank" rel="noopener noreferrer" }
