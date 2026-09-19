# P3-6.1 应该用什么特征把可比较的结构留下来

> Section ID: `P3-6.1`
> Version: `v2026.09.19`

第一次学习[特征(feature)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)时，人们常常会把它理解成 `列越多越好吗？` 但特征并不是简单地往里塞更多数值。特征是把样本所具有的结构，重新表达成可以用于比较和预测的值。所以，好的特征与其说是“更多”，不如说应该先让 `它到底想展示什么` 变得清楚。如果前一节已经把原始日志变成了[汇总表(summary table)](/AiBook/zh/reference/concept-glossary-pinyin/d/#data-modeling)，那么现在就要决定：这张汇总表里到底该留下什么结构。

所谓“设计特征”，不是把汇总表里的数字原样照用，而是重新选择：要用什么数字表达，来保留我们想比较的结构。所以，只有先决定想保留什么结构，平均值、斜率、波动性这样的特征候选才会真正有意义。这里还会再分出一个判断。把同一个结构转换成平均值、差值、斜率、token、比率这样的不同表达，是[变量变换(variable transformation)](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-variable-transformation)；而从这些已经变换出来的表达里，再决定究竟保留哪些项目，则是[特征选择(feature selection)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature-selection)。


原始测量值本身也可以直接作为特征。这里讨论从汇总值中选择并表达比较信息的情况。

## 这些特征的计算对象与单位

以下是虚构动作 A、B 的区间均值，单位为 L/min。**计算对象是前段、中段、后段三个均值，而非全部原始测量值。** 如果各区间的观测数或时长不同，这三个均值的简单平均可能不同于全部观测的平均或时间平均。

| 动作 | 前段均值 | 中段均值 | 后段均值 |
| --- | ---: | ---: | ---: |
| A | 1.8 | 2.2 | 2.6 |
| B | 2.1 | 2.2 | 2.3 |

给前段、中段、后段分配索引 0、1、2。前段到后段的索引间隔为 `2−0=2`。因此把 A 的差值 `2.6−1.8=0.8 L/min` 除以 2，得到的斜率是**每索引间隔 0.4 L/min**，不是每秒变化量。如果代表时刻相隔 20 秒，时间斜率才是 `0.8/20=0.04 L/min/s`。没有时刻资料就不能假设相隔 20 秒。

| 动作 | 三个区间均值的平均：L/min | 后段−前段：L/min | 每索引间隔的斜率 | 三个区间均值的标准差：L/min |
| --- | ---: | ---: | ---: | ---: |
| A | 2.2 | 0.8 | 0.4 | 0.4 |
| B | 2.2 | 0.2 | 0.1 | 0.1 |

标准差概括数值偏离平均值的程度。这里采用样本标准差：把三个值的离差平方和除以 `3−1=2`，再开平方根。A 相对 2.2 的差为 −0.4、0、0.4，因此 `sqrt((0.16+0+0.16)/2)=0.4`；B 用同样方法得到 0.1。采用这一计算规则并不保证三个均值在统计上独立。

## 区间均值之间的离散与区间内部波动不同

假设每个区间中，X 的测量为 `[2, 2]`，Y 为 `[0, 4]`。两个动作的区间均值都是 `[2, 2, 2]`，**这三个均值的标准差都为 0**。但每个区间内部的最大值减最小值，X 为 0，Y 为 4。只保留区间均值就无法恢复这个差异。

因此，表中 A 的标准差较大，只说明区间均值彼此更分散，并不意味着传感器噪声更大或运行不稳定。把前段和后段交换，标准差也不变；要区分上升与下降，还应读取带符号的差值。

问题是“三个区间的水平是否相似”时选择均值，问题是“从前段到后段改变了多少”时选择后段减前段。前一问题中 A、B 都为 2.2，后一问题中 A 为 0.8、B 为 0.2。索引间隔固定为 2 时，斜率就是差值的一半，同时保留两列不会增加独立的新信息。若关心区间内部波动，则需要原始值或额外的区间内部离散指标。

## 改变特征组合的小型预测实验

把动作 A～H 的区间均值转换成不同特征组合，输入同一种决策树算法。这里 `overall_mean` 是三个区间均值的简单平均，`segment_variability` 是上面计算的样本标准差。在安装了 pandas 与 scikit-learn 的 Python 环境中运行。

这是为展示输入信息损失而设计的 8 个虚构事件。`review_needed` 是例子赋予的值，不是经过验证的实际检查标准。训练事件 A～F 共 6 个，三个区间均值的平均都为 2.2，因此仅凭均值难以区分不同标签。测试只有 G、H 两个事件，准确率 0.5 与 1.0 分别表示答对 1/2 和 2/2，不能据此断言增加特征通常会提高性能。

把输入改成仅有 `overall_mean` 与 `late_minus_early` 两列，再运行实验。这一设置也能正确预测两个测试事件，但更多资料上的性能仍需要单独评估。要区分区间内部波动，仍需这些特征无法恢复的原始信息。

```python
# 这个例子比较只保留平均值的模型，以及加入变化/变动性特征的模型预测差异。
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

events = pd.DataFrame(
    [
        {"event_id": "A", "early": 1.8, "mid": 2.2, "late": 2.6, "review_needed": 1},
        {"event_id": "B", "early": 2.1, "mid": 2.2, "late": 2.3, "review_needed": 0},
        {"event_id": "C", "early": 2.5, "mid": 2.2, "late": 1.9, "review_needed": 1},
        {"event_id": "D", "early": 2.0, "mid": 2.2, "late": 2.4, "review_needed": 0},
        {"event_id": "E", "early": 1.7, "mid": 2.2, "late": 2.7, "review_needed": 1},
        {"event_id": "F", "early": 2.2, "mid": 2.2, "late": 2.2, "review_needed": 0},
        {"event_id": "G", "early": 2.6, "mid": 2.2, "late": 1.8, "review_needed": 1},
        {"event_id": "H", "early": 2.0, "mid": 2.1, "late": 2.3, "review_needed": 0},
    ]
)

segment_values = events[["early", "mid", "late"]]
events["overall_mean"] = segment_values.mean(axis=1)
events["late_minus_early"] = events["late"] - events["early"]
events["segment_variability"] = segment_values.std(axis=1)

train = events[events["event_id"].isin(["A", "B", "C", "D", "E", "F"])]
test = events[events["event_id"].isin(["G", "H"])]
feature_sets = {
    "mean_only": ["overall_mean"],
    "structure_features": ["overall_mean", "late_minus_early", "segment_variability"],
}

for name, columns in feature_sets.items():
    model = DecisionTreeClassifier(random_state=0, max_depth=2)
    model.fit(train[columns], train["review_needed"])
    predicted = model.predict(test[columns])
    comparison = [
        (event_id, int(prediction), int(actual))
        for event_id, prediction, actual in zip(test["event_id"], predicted, test["review_needed"])
    ]
    print(name, "accuracy:", accuracy_score(test["review_needed"], predicted))
    print(name, "predictions:", comparison)
```

```text
mean_only accuracy: 0.5
mean_only predictions: [('G', 0, 1), ('H', 0, 0)]
structure_features accuracy: 1.0
structure_features predictions: [('G', 1, 1), ('H', 0, 0)]
```

## 保留符合比较问题的特征 {#_1}

```mermaid
--8<-- "assets/part-03/chapter-06/p3-6-1-mermaid-01-zh.mmd"
```

## 检查清单

- 能否区分斜率分母 2 与实际时间间隔？
- 能否指出标准差的三个计算值及其单位？
- 能否解释均值 [2, 2, 2] 为何不能恢复区间内部波动？
- 能否避免把两个测试事件的准确率推广为一般性能？

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `feature`。它把 feature 解释为用于预测的输入变量，因此支持这样一点：应该先决定想展示什么结构，再把这个结构转成输入变量。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-09-19
- Google for Developers, `Machine Learning Glossary` 中的 `feature engineering`。它把 feature engineering 解释为决定哪些变换有助于模型训练的过程，因此强化了这一点：特征设计不是保留原始值不动，而是把结构转换成可比较的数字表达。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-09-19
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Location`. 该资料把平均值、中位数、众数作为代表性位置尺度来说明，并展示在偏斜分布或厚尾分布中平均值和中位数可能提供不同信息。因此，它强化了这一节的说明：即使要把整体水平留下成一个数字，也应先决定想看的结构。 [https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-09-19
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Scale`. 该资料说明了多种用于描述变动性(variability)或分散程度(spread)的数值尺度，并指出选择哪种尺度估计量取决于想强调哪一部分分散。因此，它支持这一节的说明：稳定性特征应作为不同于平均值的结构被保留下来。 [https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-09-19
