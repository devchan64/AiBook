# P3-4.5 现在收集到的样本，在多大程度上代表了整体运行情况

> Section ID: `P3-4.5`
> Version: `v2026.09.19`

即使正确地把一次动作计为一条样本，这批资料是否充分覆盖目标运行环境，仍是另一个问题。**代表性关注目标环境的分布和采集过程如何反映在资料中，而不只是各条件的数量是否相等。** 总样本数、最低数量要求和模型准确率提供不同的信息。

## 并列读取运行比例与采集比例 {#_4}

[虚构动作样本 CSV](/AiBook/assets/part-03/chapter-04/p3_4_5_sample_coverage.csv) 包含 E01～E36 共 36 次动作。一行代表一次动作，`shift` 为日间或夜间，`load_mode` 为负载模式，`machine_id` 为设备，`maintenance_phase` 区分稳定运行与维护后状态。这是检查采集覆盖和评估的自制案例，并非实际运行统计。

**假设**目标运行中日间占 80%、夜间占 20%。这个比例是另外规定的比较目标，并非从 CSV 推算得到。

| shift | 假设的运行比例 | 采集动作数 | 采集比例 |
| --- | ---: | ---: | ---: |
| day | 80% | 26 | 26/36 ≈ 72.2% |
| night | 20% | 10 | 10/36 ≈ 27.8% |

仅凭日间记录更多，不能判定存在偏差。在这个假设下，夜间的采集比例反而比目标高约 7.8 个百分点。但也不能只根据这个小表的比例差异，判定代表性合格或不合格。还要检查记录如何选取，以及遗漏了哪些期间、设备和条件。

如果需要单独评估夜间表现，可以有意多收集夜间资料。这可能有助于分条件评估，但不能把改变后的采集比例直接报告为整体运行比例。CSV 没有采集时间，因此当前列无法确认季节或期间的代表性。

## 最低 9 条规则实际统计什么

将 `minimum_count = 9` 设为说明用的观察规则，标出**少于 9 次动作的条件**。9 不是标准的充分样本数，也不是认证代表性的阈值。

| 分组列 | 各条件动作数 | 已出现的条件种类数 | 少于 9 条的条件 |
| --- | --- | ---: | --- |
| shift | day 26, night 10 | 2 | 无：0 个 |
| load_mode | normal 25, high 6, low 5 | 3 | high, low：2 个 |
| machine_id | M1 22, M2 7, M3 7 | 3 | M2, M3：2 个 |
| maintenance_phase | stable 28, after-maintenance 8 | 2 | after-maintenance：1 个 |

`shift` 的不足条件数为 0，是因为 `26 < 9` 与 `10 < 9` 都不成立。“两个条件都超过规则要求”不等于“代表目标运行”。表中的 2、3 等条件种类数，也不是动作数或模型预测正确的数量。

把最低要求提高到 10，夜间 10 条仍不算不足；提高到 11 才会被标出。反过来，降低到 5 后，上述四列的不足条件数都变为 0。这个操作只改变显示规则，并未增加资料。

## 零记录与条件组合要另行检查

上表只统计 CSV 中出现过的值。如果另行确定目标范围包含 M4，就应加入 M4 并标为 **0 条**。未确认 M4 属于目标范围前，不能随意把它当作缺失设备。这就是要将目标条件清单与实际采集值对照的原因。

即使每个单独条件都有记录，组合仍可能为空。下表从同一 CSV 中只选 `night` 动作，再同时按设备与负载统计。

| 夜间动作 | normal | high | low |
| --- | ---: | ---: | ---: |
| M1 | 3 | 1 | 0 |
| M2 | 1 | 0 | 1 |
| M3 | 2 | 1 | 1 |

全部资料中有夜间 10 条、M2 7 条、高负载 6 条，但**夜间＋M2＋高负载组合为 0 条**。如果这个组合在运行中可能发生，并属于评估范围，就应记录为空白。如果本来不可能发生，则不是补充采集对象。目标不是无条件把所有组合填成相同数量。

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-5-mermaid-01-zh.mmd"
```

## 模型分数也要结合各条件的分母读取 {#_6}

用同一 CSV 运行模型，但按虚构规则生成 `needs_review`：**负载为 `high` 或状态为 `after-maintenance` 时取 1，否则取 0**。标签由输入条件生成，因此没有测量真实故障预测能力。这个实验检查模型能从训练资料中多大程度地复现已知规则。

固定 E01～E24 为训练集，E25～E36 为评估集。这里按 ID 范围划分，并不假定它代表真实时间顺序。各负载的数量如下。

| load_mode | 训练动作数 | 评估动作数 |
| --- | ---: | ---: |
| high | 4 | 2 |
| low | 0 | 5 |
| normal | 20 | 5 |
| 合计 | 24 | 12 |

`dummy` 总是输出训练中更常见的标签 0，作为比较基准。`tree` 是根据输入条件分支预测的决策树。`OneHotEncoder` 将类别转换为 0/1 列；遇到训练中未见过的类别时，将该特征对应的编码列全部设为 0。能够执行预测，不代表已经学过这个条件。

从仓库根目录运行以下代码。通过 `features` 改变输入列，同时观察总正确数与各负载的 `test_events`、`errors`。类别转换和模型拟合都只使用训练资料。

```python
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

samples = pd.read_csv("docs/assets/part-03/chapter-04/p3_4_5_sample_coverage.csv")
samples["needs_review"] = (
    samples["load_mode"].eq("high")
    | samples["maintenance_phase"].eq("after-maintenance")
).astype(int)
train = samples[samples["event_id"].between("E01", "E24")]
test = samples[samples["event_id"].between("E25", "E36")]
# 改变输入列，同时检查评估数量与错误数。
features = ["shift", "load_mode", "machine_id", "maintenance_phase"]
models = {
    "dummy": DummyClassifier(strategy="most_frequent"),
    "tree": DecisionTreeClassifier(random_state=0, max_depth=3),
}
results = {}
for name, estimator in models.items():
    model = make_pipeline(OneHotEncoder(handle_unknown="ignore"), estimator)
    model.fit(train[features], train["needs_review"])
    result = test[["event_id", "load_mode", "needs_review"]].copy()
    result["prediction"] = model.predict(test[features])
    result["error"] = result["prediction"].ne(result["needs_review"])
    correct = int((~result["error"]).sum())
    print(f"{name}: correct={correct}/{len(result)}, accuracy={correct / len(result):.3f}")
    print(result.groupby("load_mode").agg(
        test_events=("error", "size"), errors=("error", "sum")
    ).to_string())
    results[name] = result
```

```text
dummy: correct=5/12, accuracy=0.417
           test_events  errors
load_mode
high                 2       2
low                  5       2
normal               5       3
tree: correct=9/12, accuracy=0.750
           test_events  errors
load_mode
high                 2       0
low                  5       3
normal               5       0
```

基准模型在 12 次动作中答对 5 次，`5/12 ≈ 41.7%`；决策树答对 9 次，`9/12 = 75%`。后者的三个错误全在 `low`，因此低负载准确率为 `(5−3)/5 = 2/5 = 40%`。高负载为 2/2，正常负载为 5/5，但这些只是小型评估集上的结果，并不保证未来表现。

本次运行的低负载错误是 E27、E28、E29。三次动作均为 `stable`，所以虚构目标为 0，但模型输出 1。需要注意训练中没有 `low`，但不能推广为“未见条件必然预测错误”或“未见条件是唯一错误原因”。输入表示与学到的分支也会影响结果。

试着改成 `features = ["load_mode"]`，去掉维护信息。决策树准确率变为 `6/12 = 50%`，各负载的错误数为 high 0/2、low 3/5、normal 3/5。此时输入无法区分维护后的正常负载动作 E25、E26、E34 的标签。采集范围与输入信息会共同影响结果。根据本练习的评估分数选择输入后，应避免再次使用同一集合进行最终性能验证。

## 用文字记录适用范围与剩余空白

请改写“最低数量达标且准确率为 75%，所以足以用于整体运行”。参考答案是：“日间与夜间超过了说明用的 9 条要求，但仍需检查目标比例、采集方式和其他条件。该虚构规则实验在 12 次动作中答对 9 次；训练中没有的低负载在 5 次中答对 2 次。夜间＋M2＋高负载以及采集期间的覆盖仍缺少依据。”

实际资料应记录采集期间与方式、目标条件清单、重要的零记录或少量记录组合，以及需要补充采集或暂缓应用的范围。总数量或单一准确率都不能代替这些记录。

## 检查清单

- 是否区分假设的目标比例 80/20 与实际采集比例 26/36、10/36？
- 是否算出了 9 条要求下 shift 的不足条件数为何为 0？
- 能否解释降低要求会消除警告，却没有增加资料？
- 是否检查了目标清单中的零记录条件，以及夜间＋M2＋高负载等交叉空白？
- 是否同时读取整体 9/12 与低负载 2/5，并说明虚构标签的局限？
- 是否记录了当前 CSV 无法确认的范围，例如观测期间？

## 来源与参考资料

- Google for Developers，[Deep Learning Tuning Playbook: Additional guidance](https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook/additional-guidance){: target="_blank" rel="noopener noreferrer" }。为在代表实际运行的资料上评估提供一般依据。80/20 比例与最低 9 条要求是本节的虚构设定。 / 查阅日期：2026-09-19
- scikit-learn developers，[OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html){: target="_blank" rel="noopener noreferrer" }。说明类别编码以及 `handle_unknown="ignore"` 如何处理未见类别。 / 查阅日期：2026-09-19
