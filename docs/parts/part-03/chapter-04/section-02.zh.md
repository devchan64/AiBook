# P3-4.2 一旦样本单位摇摆，哪些东西会一起摇摆

> Section ID: `P3-4.2`
> Version: `v2026.09.19`

如果把一次动作定为一个[样本](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)，其观测、特征与结果必须指向同一动作。但**按事件划分训练与评估**和**每个事件只评分一次**是两个决定。本节用预测动作复核结果的虚构实验说明区别。

## 观测行、分析对象、划分组与评分单位

| 区分 | 本实验中的含义 |
| --- | --- |
| 观测行 | 动作内某一时点的流量记录 |
| 分析对象 | 带有复核结果的一次动作 |
| 一条模型输入 | 一个时点的 `flow` 值 |
| 划分组 | 一起放入训练或评估的 `event_id` |
| 评分单位 | 将预测与目标对照的一条时点记录 |

模型逐时点预测，而目标 `review_needed` 是把动作的 0 或 1 重复到各行。这是输入与目标设计实验，并非已确认故障的资料。把 1 填入一个动作的 18 行，仍然只代表一个被标记为需复核的动作，不是 18 个动作。

还要明确特征的计算范围。下面 CSV 中 A 在 16 秒的流量为 10.2，17 秒为 9.9。`late_drop = 前值−后值 = 0.3 L/min` 是该区间的下降量，斜率则为 `(9.9−10.2)/(17−16) = −0.3 L/min/s`。两者符号与单位不同，都无法仅凭一个时点值计算。也可以给时点输入添加区间特征，但必须说明使用了哪个观测区间。

## 先读准确率的分母

本实验的**准确率是预测正确的评估行数除以全部评估行数**。例如，12 行中答对 6 行，得到 `6/12 = 0.5`，即 50%。一个事件有多行时，会在此计算中被评分多次。

| 划分方式 | 训练记录 | 评估记录 | 两侧有相同事件吗 |
| --- | --- | --- | --- |
| 按行划分 | A~H 每个事件的 0~11 秒 | A~H 每个事件的 12~17 秒 | 有：A~H |
| 按事件划分 | A~D 的所有时点 | E~H 的所有时点 | 没有 |

第一种评估已见事件的其他时点，第二种评估未见事件的记录。两者都不会自动变成每个事件只评分一次。如果问题关心新事件性能，第一种划分的高分本身不能回答。

## 改变划分并检查模型输出

输入是[虚构日志 CSV](/AiBook/assets/part-03/chapter-04/p3_4_2_split_log.csv)。A~H 八个事件各有 18 个观测点，共 144 行，流量按 L/min 读取。以事件中心值 10、30、…、150 为基准，重复小变化 `0.0, +0.2, −0.1`。同一事件内的值非常相近，重复观测不会增加独立事件。[生成代码](/AiBook/assets/part-03/chapter-04/p3_4_2_make_split_log.py)可重现该文件。

决策树 `DecisionTreeClassifier` 根据输入值作划分并预测 0/1。这里关注同一模型采用不同划分时评估对象如何变化，而非如何提高性能。`features` 是输入列，`train_event_ids` 是事件划分中的训练事件。修改它们，观察重叠事件、正确行数与分母。

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

raw = pd.read_csv("docs/assets/part-03/chapter-04/p3_4_2_split_log.csv")
# 修改输入列与训练事件，同时检查正确行数和评估行数。
features = ["flow"]
train_event_ids = ["A", "B", "C", "D"]
row_train_end = 12

row_train = raw[raw["second"] < row_train_end]
row_test = raw[raw["second"] >= row_train_end]
event_train = raw[raw["event_id"].isin(train_event_ids)]
event_test = raw[~raw["event_id"].isin(train_event_ids)]


def evaluate(name, train, test):
    if train.empty or test.empty:
        raise ValueError("Both training and evaluation need records.")
    model = DecisionTreeClassifier(random_state=0)
    model.fit(train[features], train["review_needed"])
    result = test[["event_id", "review_needed"]].copy()
    result["prediction"] = model.predict(test[features])
    result["correct"] = result["prediction"].eq(result["review_needed"])
    overlap = sorted(set(train["event_id"]) & set(test["event_id"]))
    correct = int(result["correct"].sum())
    total = len(result)
    print(f"{name}: train_rows={len(train)}, test_rows={total}, overlap={overlap}")
    print(f"row_accuracy: {correct}/{total} = {correct / total:.3f}")
    print(result.groupby("event_id").agg(
        test_rows=("correct", "size"), correct_rows=("correct", "sum")
    ).to_string())
    return result


row_result = evaluate("row_split", row_train, row_test)
print()
event_result = evaluate("event_split", event_train, event_test)
```

```text
row_split: train_rows=96, test_rows=48, overlap=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
row_accuracy: 48/48 = 1.000
          test_rows  correct_rows
event_id
A                 6             6
B                 6             6
C                 6             6
D                 6             6
E                 6             6
F                 6             6
G                 6             6
H                 6             6

event_split: train_rows=72, test_rows=72, overlap=[]
row_accuracy: 36/72 = 0.500
          test_rows  correct_rows
event_id
E                18             0
F                18            18
G                18            18
H                18             0
```

默认按行划分得到 **48/48 = 1.0**，按事件划分得到 **36/72 = 0.5**。后者错判 E、H 的 36 行，正确预测 F、G 的 36 行。分母 72 是四个事件的时点行数，不是事件数 4。

按行划分时，同一事件的相近值在两侧重复，模型容易学到彼此分离的事件取值区间。按事件划分时，评估流量在 90 以上，超出训练约 10~70 的范围，模型全部预测为 0。两种实验的训练、评估行数及数值分布也不同，因此**不能把分数差全部归因于事件重叠这一项因素**。事件分开后，分数并不必然降低。

将 `train_event_ids` 改为 `['A', 'B', 'C', 'E']`，评估事件变为 D、F、G、H。对这些数据与模型，只有 H 的 18 行预测正确，得到 `18/72 = 0.25`。也可尝试 `features = ['flow', 'second']`，默认事件划分下准确率仍为 0.5。增加列不一定改变或提高分数。这些是探索性检查，不能挑选评估得分最高的划分来报告性能。

## 事件级评分需要另定规则 {#_1}

每个事件只评分一次，需要规定如何把逐时点预测合成一个事件结果。例如，对 18 个预测作多数表决，平票时暂缓判定。默认事件划分中每个事件的预测全为 0，因此仅 F、G 正确，得到 `2/4 = 0.5`。虽然与行准确率数值相同，分母却不同。若事件记录数不同或内部预测混合，两种分数就可能不同。

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-2-mermaid-01-zh.mmd"
```

请把“事件划分准确率为 0.5”改写得更准确。答案是：“用 A~D 训练后，对新事件 E~H 的 72 个时点行预测正确了 36 行。”若每个事件只评分一次，则要另写多数表决等合成规则，并单独报告 `2/4`。

## 检查清单

- 能否分别指出观测行、分析对象、划分组与评分单位？
- 是否避免把重复的事件标签计作新的独立事件？
- 能否区分下降量 0.3 L/min 与斜率 −0.3 L/min/s？
- 是否把 1.0 与 0.5 展开为正确行数除以评估行数？
- 能否区分保留新事件作评估与每个事件评分一次？

## 来源与参考资料

这些资料支持按组划分及准确率的定义。

- scikit-learn developers, `Cross-validation: evaluating estimator performance`, grouped data. [官方文档](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 查阅日期: 2026-09-19
- scikit-learn developers, `accuracy_score`. [官方文档](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html){: target="_blank" rel="noopener noreferrer" } / 查阅日期: 2026-09-19
