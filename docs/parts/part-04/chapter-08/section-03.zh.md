# P4-8.3 补充学习: 按问题类型第一次建立 baseline 的方法

> Section ID: `P4-8.3`
> Version: `v2026.07.20`

如果在 P4-8.2 里已经看过为什么 baseline 必须存在，那么接下来马上会出现一个问题。

那么 baseline 到底该怎么实际建立？

这个补充学习就是在回答这个问题。目标不是去背很多 baseline 名字，而是让读者能看着问题类型，自己选出 `最简单但又有比较意义的标准`。

## 本补充学习的范围

这一节处理的是：在分类、回归、时序问题里，第一次建立代表性 baseline 的方法。

- 在建立 baseline 之前，必须先固定什么？
- 按问题类型，可以先想到哪些 baseline？
- 建好 baseline 之后，应该从什么案例和例子开始比较？
- 看完 baseline 分数之后，下一步应该检查什么？

这一节先收束 `怎样按问题类型建立最简单但仍有比较意义的 baseline`。交叉验证、模型比较流程、更复杂的调优方法，会在 P4-9 之后继续展开。

## 用补充学习: 按问题类型第一次建立 baseline 的方法恢复的概念连接

- 能区分分类、回归、时序里的代表性 baseline 候选。
- 能按 `固定问题类型 -> 选择最简单规则 -> 用同样指标测量 -> 检查错误 -> 决定下一步比较` 的顺序说明 baseline 建立流程。
- 能说明为什么 baseline 解释之后，案例和例子要立刻接上来。
- 能说出看完 baseline 分数之后，应该继续追问什么问题。

## 先固定 baseline 建立流程

baseline 不是靠感觉定下来的临时规则，更安全的做法是把它当成一套程序：在当前问题里，选出 `最简单但仍然有比较意义的标准`。

最短的流程可以先固定成下面这几步。

1. 先固定问题类型。
2. 选一个几乎不使用特征的最简单规则。
3. 用和候选 model 相同的指标来测量 baseline。
4. 不只看分数，也一起看代表错误场景。
5. 只有在解释完“它比 baseline 好了多少”之后，才进入调优或更换候选。

如果把这个顺序再整理成表，会是下面这样。

| baseline 设计顺序 | 现在要问的问题 | 为什么需要 |
| --- | --- | --- |
| 1. 固定问题类型 | 是分类、回归，还是时序？ | 因为 baseline 的形式本身会在这里改变。 |
| 2. 选择最简单规则 | 是多数类、平均值/中位数，还是前一个值？ | 因为必须先立起几乎不使用特征的最低标准。 |
| 3. 用同样指标测量 | 要看 accuracy、recall、MAE，还是 MAPE？ | 因为 baseline 和候选 model 必须用同一个尺子比较。 |
| 4. 检查错误场景 | 它特别遗漏了什么，或者在哪些地方错得很大？ | 因为只看分数差，很难读出改进方向。 |
| 5. 解释后决定下一步 | 是继续调优、换候选，还是回头再看特征？ | 因为不能把连 baseline 都过不了的候选拖太久。 |

也就是说，baseline 方法论的核心，不是 `做一个最容易的规则`，而是 `把最容易的规则放进同一个比较框架里`。

## 按问题类型看的代表 baseline 地图

代表性 baseline 会随着问题类型不同而从不同起点出发。

| 问题类型 | 最先想到的 baseline | 为什么经常最先用它 |
| --- | --- | --- |
| 分类(classification) | 多数类预测 | 因为它最快揭露高 accuracy 幻觉。 |
| 分类(classification) | 基于类别比例的 dummy 预测 | 因为它能区分“只是在跟着分布走”还是“真的学到了东西”。 |
| 回归(regression) | 平均值预测 | 因为它能显示“即使没有输入特征也会产生的默认误差”。 |
| 回归(regression) | 中位数预测 | 因为在极端值很多时，它可能是更稳定的标准。 |
| 时序(time series) | naive 预测 | 因为它是最简单的时间顺序标准，直接沿用上一个值。 |
| 时序(time series) | seasonal naive 预测 | 因为在季节性强时，可以把上一轮同季节的值当作标准。 |

这张表不是 baseline 的答案清单，而是一张快速整理 `应该先把什么放成比较线` 的地图。时序里的 naive、seasonal naive，在 Hyndman 等公开教材中也被直接说明为代表性的 `simple forecasting methods`。

## 在分类里怎么建立 baseline

在分类里，首先可以想到下面这些 baseline。

| baseline 形式 | 意义 | 适合先用的场景 |
| --- | --- | --- |
| 永远预测最常见的类别 | 多数类标准 | 类不平衡很强的问题 |
| 按类别比例随机预测 | 分布层面的标准 | 想区分“跟着分布走”和“真的学到”时 |
| 永远预测同一个类别 | 绝对最低地板线 | 当读者第一次固定指标解释方式时 |

想象一个客户流失预测场景，其中流失很少。如果 baseline 说 `永远不流失`，accuracy 可能会很高。但流失 recall 会变成 0。所以，分类 baseline 的第一角色不是先回答 `分数高不高`，而是先暴露 `这里到底有什么幻觉`。

## 案例及示例

### 案例 1. 为什么在客户流失预测里要先放多数类 baseline

一个订阅服务团队想预测客户下个月是否流失。假设数据里非流失客户占 90%，流失客户占 10%。

这时如果 baseline 一律预测 `非流失`，accuracy 就可能达到 90%。但真正重要的是：它完全抓不到流失客户。所以，如果没有 baseline，只看实际 model 的 accuracy 91%，就很容易说成 `提高了 1 个百分点`。而一旦把 baseline 放在一起，读者首先就会问：`它是不是仍然几乎抓不到那些重要客户？`

| 项目 | 内容 |
| --- | --- |
| 问题 | 预测客户下个月是否流失 |
| 类别分布 | 非流失 90%，流失 10% |
| baseline | 永远预测 `非流失` |
| 先看的指标 | accuracy、recall、F1 |
| 马上检查的错误 | 漏掉真实流失客户的案例 |

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-3-mermaid-01-zh.mmd"
```

这个案例的关键点是：baseline 之所以重要，不是因为它是一个低水平模型，而是因为它是 `能立刻揭露 accuracy 幻觉的标准`。

### 小例子: 用数字读分类 baseline

当 baseline 和实际 model 在同一份数据上并排放在一起时，baseline 的作用会更清楚。

| 模型 | accuracy | recall | F1 | 读法 |
| --- | ---: | ---: | ---: | --- |
| baseline: 永远非流失 | 0.90 | 0.00 | 0.00 | accuracy 看起来很高，但一个重要客户也没抓到。 |
| 候选模型 | 0.94 | 0.50 | 0.63 | 可以读出它是否真的比 baseline 更开始抓到流失。 |

读这张表时要问的问题很简单。

- accuracy 的差异真的有意义吗？
- recall 和 F1 比 baseline 改变了多少？
- 仍然漏掉的流失客户是什么样的案例？

## 在回归里怎么建立 baseline

在回归里，首先可以放上下面这些 baseline。

| baseline 形式 | 意义 | 适合先用的场景 |
| --- | --- | --- |
| 对所有样本都预测平均值 | 最基础的中心值标准 | 当第一次检查输入特征是否真的有帮助时 |
| 对所有样本都预测中位数 | 对极端值不那么敏感的标准 | 当异常值很多时 |
| 预测某个固定常数值 | 领域固定标准 | 当业务里已经有一个既存基准时 |

回归 baseline 的核心，是先建立一个起点：`即使没有输入，也会出现这么多误差`。

### 案例 2. 为什么在配送时间预测里先放平均值 baseline

一个物流团队想预测配送时间。在建立一个使用地区、距离、货量、天气信息的 model 之前，它先放一个 `对所有订单都预测平均配送时间` 的 baseline。

这个 baseline 的目的，并不是说平均预测很优秀，而是为了检查：用了输入特征的 model，到底比平均标准真实减少了多少误差。

| 项目 | 内容 |
| --- | --- |
| 问题 | 配送时间预测 |
| baseline | 对所有订单预测平均配送时间 |
| 先看的指标 | MAE、RMSE |
| 马上检查的错误 | 长途配送、恶劣天气配送等大误差区间 |

例如，如果平均 baseline 的 MAE 是 18 分钟，而候选 model 的 MAE 是 15 分钟，那么下一个问题就是 `减少了 3 分钟，这在运营上有没有意义`。要回答这个问题，就不能只看整体平均，还得一起看：到底是哪些订单群的误差真的减少了。

### 小例子: 用数字读回归 baseline

| 模型 | MAE | RMSE | 读法 |
| --- | ---: | ---: | --- |
| baseline: 平均配送时间 | 18.0 | 24.5 | 这是不看输入时的出发点。 |
| 候选模型 | 15.0 | 20.8 | 它比 baseline 降低了误差，但还要继续看到底是在什么订单群里降下来的。 |

读这张表时，最好再一起写下下面这些东西。

- 哪些订单群的大误差减少了？
- 它是不是不只在整体平均上更好，也在重要区间里更好？
- 相比 baseline 降下来的误差，是否会转化成运营成本降低？

## 在时序里怎么建立 baseline

在时序问题里，与其完全抹掉时间顺序，不如先放一个至少最小程度反映时间结构的简单标准，往往更自然。

| baseline 形式 | 意义 | 适合先用的场景 |
| --- | --- | --- |
| naive | 用前一个值预测下一个值 | 变化缓慢的时序 |
| seasonal naive | 使用上一周同一天或去年同月的值 | 存在季节性、周期性的时序 |
| mean method | 用整体平均作为下一个值的标准 | 当时间结构较弱，只需要一个简单比较起点时 |

### 案例 3. 为什么在日访问量预测里先放 seasonal naive

一个电商团队想预测每日访问人数。如果周一和周末的模式差异很大，那么比起简单平均值，用 `上周同一天的值` 作为下一次标准，会更自然。

| 项目 | 内容 |
| --- | --- |
| 问题 | 预测明天访问人数 |
| baseline 候选 | naive、seasonal naive |
| 先看的指标 | MAE、MAPE |
| 马上检查的错误 | 节假日、活动日、促销期 |

例如，如果直接使用昨天访问人数的 naive baseline，比起使用上周同一天数值的 seasonal naive 误差更大，就说明在这个时序里，`星期周期` 必须进入最低标准。

### 小例子: 比较读取时序 baseline

| 模型 | MAE | 读法 |
| --- | ---: | --- |
| naive | 320 | 这是只跟着前一个值走的标准。 |
| seasonal naive | 180 | 反映星期模式的最低标准更好。 |
| 候选模型 | 150 | 可以读出它是否在季节性标准之上还有额外改进。 |

在这个场景里，baseline 本身可能不止一个。对于时序来说，更自然的顺序往往是：先比较 `前一个值标准` 和 `周期标准` 哪一个更适合作为地板线，然后再把复杂 model 放到它上面。

## 练习与示例

### 用 Python 例子比较分类 baseline 和候选模型

下面这个例子是一个很小的练习，用来比较 scikit-learn 的 `DummyClassifier` 和一个简单分类模型。

问题场景:

- 如果要确认新 model 是否真的有帮助，就必须把它和最低标准并排比较

输入:

- 用 `make_classification` 生成的不平衡分类数据
- `DummyClassifier`
- `LogisticRegression`

期待输出:

- baseline 和实际模型的 accuracy、recall、F1

要确认的概念:

- baseline 是复杂 model 至少必须赢过的比较标准
- 对于不平衡数据，不能只看 accuracy，还要一起看 recall 和 F1

```python
# 这个例子按问题类型建立 baseline，并把候选模型性能与它们进行比较。
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=400,
    n_features=6,
    n_informative=3,
    n_redundant=0,
    weights=[0.9, 0.1],
    random_state=42,
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)
baseline_pred = baseline.predict(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
model_pred = model.predict(X_test)

print("baseline accuracy :", round(accuracy_score(y_test, baseline_pred), 3))
print("baseline recall   :", round(recall_score(y_test, baseline_pred), 3))
print("baseline f1       :", round(f1_score(y_test, baseline_pred), 3))
print()
print("model accuracy    :", round(accuracy_score(y_test, model_pred), 3))
print("model recall      :", round(recall_score(y_test, model_pred), 3))
print("model f1          :", round(f1_score(y_test, model_pred), 3))
```

执行结果示例如下。

```text
baseline accuracy : 0.9
baseline recall   : 0.0
baseline f1       : 0.0

model accuracy    : 0.942
model recall      : 0.5
model f1          : 0.632
```

在这个例子里，真正必须读的不是某一个数字。

- accuracy 即使在 baseline 上也可能已经很高
- recall 和 F1 更能显示是否真的抓到了重要的少数 class
- 所以 baseline 比较会迫使读者同时看 `到底在哪个指标上改进了` 和 `还留下了什么错误`

### 用 Python 例子实际比较回归 baseline

下面这个例子用一个很小的目标值数组，直接比较平均值 baseline 和中位数 baseline。

问题场景:

- 在配送时间预测里，想看看平均值 baseline 和中位数 baseline 哪一个才是更自然的出发点

输入:

- 简单的训练目标值和评估目标值
- 平均值 baseline、中位数 baseline

期待输出:

- 平均值 baseline 和中位数 baseline 的预测值与 MAE

要确认的概念:

- 即使是 baseline，随着真实数据场景不同，更自然的出发点也可能不同

```python
# 这个例子按问题类型建立 baseline，并把候选模型性能与它们进行比较。
y_train = [32, 35, 31, 120, 33]
y_test = [34, 36, 30, 90]

mean_value = sum(y_train) / len(y_train)
median_value = sorted(y_train)[len(y_train) // 2]

mean_pred = [mean_value] * len(y_test)
median_pred = [median_value] * len(y_test)

def mae(y_true, y_pred):
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)

print("mean baseline")
print("  prediction :", [round(v, 1) for v in mean_pred])
print("  MAE        :", round(mae(y_test, mean_pred), 2))
print()
print("median baseline")
print("  prediction :", [round(v, 1) for v in median_pred])
print("  MAE        :", round(mae(y_test, median_pred), 2))
```

执行结果示例如下。

```text
mean baseline
  prediction : [50.2, 50.2, 50.2, 50.2]
  MAE        : 22.6

median baseline
  prediction : [33, 33, 33, 33]
  MAE        : 16.0
```

这个例子说明了为什么平均值 baseline 和中位数 baseline 都要一起想到。只要训练目标值里有一个很大的值 `120`，平均值就会被强烈拉走，而中位数会更稳定地留下来。也就是说，在这种场景里，更安全的做法是先用真实数字确认：`平均值是不是默认基准线`，还是 `中位数才是更自然的基准线`。

## 检查清单

- 你有没有至少写下一个符合当前问题类型的代表性 baseline 候选？
- 你是不是在用同一个指标比较 baseline 和候选 model？
- 你看的是否不只分数差，也包括代表错误场景？
- 你有没有避免把一个过不了 baseline 的候选拖进很长的调优？
- 你能不能说明 baseline 不是 `先输掉的模型`，而是 `必须先比较的标准`？
- 你能不能说明代表性 baseline 方法必须按问题类型不同来设置？
- 你能不能说明只有确认出现了比 baseline 更好的候选，才更安全地进入调优？

## 出处与参考资料

- scikit-learn developers, [`DummyClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, 确认日期: 2026-07-09.
- scikit-learn developers, [`DummyRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, 确认日期: 2026-07-09.
- scikit-learn developers, [`Cross-validation: evaluating estimator performance`](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn User Guide, 确认日期: 2026-07-09.
- Rob J Hyndman, George Athanasopoulos, [`Forecasting: Principles and Practice (3rd ed), 5.2 Some simple forecasting methods`](https://otexts.com/fpp3/simple-methods.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
- Trevor Hastie, Robert Tibshirani, Jerome Friedman, [*The Elements of Statistical Learning*](https://hastie.su.domains/ElemStatLearn/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
- Sebastian Raschka, [`Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning`](https://arxiv.org/abs/1811.12808){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, 确认日期: 2026-07-09.
