# P4-10.2 线性回归(linear regression)的评价与局限

> Section ID: `P4-10.2`
> Version: `v2026.07.11`

P4-10.1 把 linear regression 介绍成 `先用直线来读取关系的模型`。现在要进入下一个问题。

那条直线到底拟合得有多好？又会从哪里开始变得容易出错？

这正是 evaluation 与 limit 的出发点。

学完 linear regression 之后，读者常常停在 `系数看起来挺合理`、`预测值看起来差不多` 这样的层次。但在算法章节里，必须再往前走一步。要一起看 prediction 与 reality 的差该怎样读、该用什么 metric 来总结、以及直线假设会在什么时候变得吃力。

所以，这一节不是停在 `画出了一条直线`，而是进入 `那条直线到底解释了多少数据`。

本节不会长篇重复 linear regression 的基本定义。`用直线读取关系的模型` 这个核心直觉，继续通过 P4-10.1 和 [概念词汇表](../../../reference/concept-glossary.md) 接回来；这里则把焦点放在评价与局限上。

## 本节范围

这一节回答下面这些问题。

- residual 和 error 应该怎样理解？
- 说 linear regression 的 prediction `拟合得好`，到底是什么意思？
- 在入门层面，MAE、MSE、RMSE、R² 应该怎样区分？
- 当直线假设失效时，会出现什么局限？
- linear regression 的结果应该信到什么程度，又该从哪里开始更谨慎？

这一节不会深入讲下面这些内容。

- statistical significance test
- residual normality 与 homoscedasticity 的严格检验
- multicollinearity 诊断
- 更深入的 regularization 与 feature engineering

regression diagnostics、significance 和 multicollinearity 的基础阅读，会在 P4-10.3 补充学习里再整理。regularization 与相关 hyperparameter 的更大视角，也会通过 P4-9.1 和 P4-9.2 再接回来。feature engineering 的更大 흐름，则会通过 P4-7.1、P4-7.2、P4-18.1、P4-18.2 再连回去。

## 本节目标

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

这里再固定住一点，classification 章节学过的比较框架，在 regression 里也会 그대로 이어집니다. 在 regression 里，baseline 可以是像简单平均预测这样的 `参考 model`，也可以是把最近 prediction error 和平时的 error distribution 摆在一起的 `比较基准线`。所以 regression evaluation 也不是只看一个绝对误差数字，而是要一起读 `现在的误差是不是比平时更大`、`是不是只在某个区间反复出现`。这里同样，首先把大误差读成变化信号，原因解释则要在回头检查缺失 feature 或区间差异之后再 붙입니다。

所以，在 regression evaluation 里，比较框架也必须保持统一。如果把 baseline error、当前 model error、最近区间的 error distribution 分别放在不同单位、不同区间下去读，就很难说清 `到底是什么真的变好了`。

## 主要学习内容

### residual 和 error 有什么不同

这两个词第一次看时会很像，但在这本书里会这样区分。

- residual：某一个数据点上的 `actual - prediction`
- error：泛指 model 留下来的差

例如，真实分数是 72，而 prediction 是 68，那么 residual 就是 `72 - 68 = 4`。反过来，真实分数是 64，而 prediction 是 67，那么 residual 就是 `64 - 67 = -3`。

这里重要的是 sign 和 size。

- 正 residual：model 预测得偏低
- 负 residual：model 预测得偏高
- 绝对值大：在那个数据点上 miss 得更多

把这个差简单画出来，就是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-2-mermaid-01-en.mmd"
```

这张图让 residual 不再只是一个扁平的 `失败标记`，而是一个 `有方向的差`。只有把 prediction 比 reality 低还是高一起看，读者以后才能怀疑 model 是否在某个区间里系统性地偏向一边。

关键点是：residual 不只是 `错了`，而是在展示 `往哪个方向错了多少`。

### 说线性回归预测得好，到底是什么意思

在 regression 里，不像 classification 那样很容易直接分成 `对/错`。数值预测大多都会有一点点偏差。所以读 regression model 时，首先看的通常不是 `它有多常正好猜中`，而是 `它平均偏离了多远`。

假设有两个 model。

| model | 误差特点 |
| --- | --- |
| Model A | 大多数时候偏 2 到 3 分 |
| Model B | 平时差不多，但偶尔会一下错 20 分 |

两者在平均上都可能看起来还行，但在实际使用里，B 可能更危险。所以 regression evaluation 的核心就是 `怎样总结误差`。

也就是说，在 regression 里，`拟合得好` 往往要再拆回下面这些问题。

- 平均偏多少？
- 大误差常不常出现？
- 它真的比 baseline 更好吗？
- 这条直线有没有漏掉结构性的模式？

### MAE、MSE、RMSE 应该怎样区分

scikit-learn 的 regression metric 文档提供了 mean absolute error、mean squared error、R² 等指标。入门时，读者比起记公式，更容易先从 `它会更重地处罚哪种错误` 来理解。

#### MAE

MAE 是把 residual 的绝对值取平均。

- 它解释起来最直观。
- 很容易直接读成 `平均大概错了几分、几分钟、几单位`。
- 它不会特别夸大大误差。

所以，MAE 最朴素地展示的是 `平均错了多少`。

#### MSE

MSE 是把 residual 平方之后再平均。

- 它对大误差更敏感。
- 它会把少数大失败看得比许多小失败更重。
- 因为单位被平方了，所以解释起来不够直观。

所以，MSE 适合用在 `想更重地惩罚大失败` 的场景。

#### RMSE

RMSE 是在 MSE 上再开平方。

- 它保留了对大误差更敏感的优点。
- 同时又回到原本的单位，解释起来更方便。

所以，RMSE 常用在 `既想对大误差敏感，又想继续用原单位来解释` 的场景。

三者可以很短地整理成下面这样。

| metric | 入门式读取 |
| --- | --- |
| MAE | 平均错了多少 |
| MSE | 更重惩罚大误差的平均误差 |
| RMSE | 对大误差更敏感、但回到原单位来读的误差 |

### R² 보여주는 것은 무엇인가

R² 是 linear regression 入门里经常出现的数字，但也很容易被误读。

`R² 是一个 summary value，它展示的是：这个 model 比简单平均预测多解释了多少数据。`

入门层面上，可以先这样读。

- 接近 1：这条直线在当前数据里解释了相当多的变动
- 接近 0：它和用平均值来预测没多大差别
- 也可能是负数：甚至会比平均预测更差

重要的是，R² 很容易被当成 `越高越好` 的单一分数来读。但光靠 R²，读者看不出来后面是否藏着几个很大的失败。所以它必须和 MAE、RMSE 这类误差 metric 一起读。

### metric 应该怎样一起读

只看一个 metric 时，linear regression 的解释很容易摇晃。典型场景如下。

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
--8<-- "assets/part-04/chapter-10/p4-10-2-mermaid-02-en.mmd"
```

这张图整理的是 regression metric 的阅读顺序。好的 regression evaluation 不是看完一个数字就结束，而是要按顺序去确认：它有没有超过 baseline、平均误差有多大、以及后面有没有藏着大失败。

核心就是不要停在 `有一个数字看起来不错`。

### linear regression 不容易拟合好的典型场景是什么

linear regression 的局限，大多会在 `一条直线根本不够，但还是硬要拿一条直线去解释` 的场景里暴露出来。

典型场景包括：

#### 1. 关系是 nonlinear 的时候

输入变大时，输出可能一开始增加得很快，但过了某个点之后就变缓。这个时候，一条线很难同时照顾前半段和后半段。

#### 2. 关系会随区间改变的时候

有些数据在不同区间里会换一种性格。

- 小户型和大户型的价格结构可能不同
- 短距离配送和长距离配送的时间模式可能不同

这时，把全部数据压成一条直线，平均上也许看起来还行，但在各区间里却会不断失误。

#### 3. 缺了重要 feature 的时候

有时问题不在于那条线，而在于真正需要的 feature 没有放进来。

例如，房价预测只放面积而不放位置，model 看起来像是在读面积和价格的关系，实际上却漏掉了一个关键结构。

#### 4. outlier 很强的时候

linear regression 无法直接无视大误差。如果少数数据点离得特别远，整条线就可能被它们拉走，导致整体解释都摇晃起来。

因此，linear regression 的局限，应该更少读成 `这个算法不好`，而更多读成 `现在这个问题可能无法只用一条直线来总结`。

## 案例及示例

### 案例 1. 平均上看起来不错，但在特定客户区间里 크게 실패하는 배송时间预测

一个物流团队正在根据配送距离和下单时间段预测到达时间。人们最先看的关系是 `距离更远时是不是会更久`、`下班时段下单是不是会更晚`。

把 linear regression 跑出来之后，整体 R² 不低，MAE 看起来也还可以。表面上，model 似乎能用。但仔细看时，在长距离配送或暴雨天里 prediction 会 크게 빗나가고，RMSE 也因为这些大失败而高得比预想更明显。

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-2-mermaid-03-en.mmd"
```

在这个场景里，regression evaluation 不是一个数字就能结束。MAE 展示的是平均偏了多少，RMSE 对少数大失败更敏感，而 R² 只是总结整体解释力有多大。因此，单看 `R² 很高` 还远远不够说明实际运营风险。

## 本节要记住的观念

- residual 是真实值与预测值之间的差。
- MAE 보여주는 것은 평균적으로错多少，RMSE 则是对大误差更敏感的平均误差。
- R² 是显示 model 比平均预测多解释了多少的 summary value。
- 只看一个 metric 很容易让解释摇晃，所以 baseline、平均误差、大误差和 residual pattern 必须一起看。
- linear regression 的局限通常出现在 `问题无法只用一条直线来概括` 的场景里。

## 出处与参考资料

- scikit-learn, `1.1. Linear Models`, scikit-learn User Guide, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/modules/linear_model.html](https://scikit-learn.org/stable/modules/linear_model.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `3.4. Metrics and scoring: quantifying the quality of predictions`, scikit-learn User Guide, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/modules/model_evaluation.html](https://scikit-learn.org/stable/modules/model_evaluation.html){: target="_blank" rel="noopener noreferrer" }
