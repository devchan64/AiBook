# P3-5.5 数值缺失或区间为空的样本应该怎样处理

> Section ID: `P3-5.5`
> Version: `v2026.07.25`

当我们已经来到“把源日志变成[汇总表(summary table)](/AiBook/zh/reference/concept-glossary-pinyin/h/#glossary-summary-table)”的阶段后，像 `动作是有的，但部分传感器值为空怎么办？`、`中间区间记录缺了，这条样本该丢掉，还是部分使用？` 这样的问题就会立刻出现。这时首先要看的，不是怎么填值，而是这些[缺失值(missing value)](/AiBook/zh/reference/concept-glossary-pinyin/q/#glossary-missing-value)会在多大程度上动摇[样本(sample)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)边界和[特征(feature)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)含义。

“值缺了”这件事，不只是一个清洗问题，它更像是一个数据建模信号，要求我们重新问一次：`这条样本还能不能被看成同一种案例？`

## 缺失如何动摇样本结构

如果只看到空值，就立刻觉得 `把 NaN 补上就行`，就很容易漏掉：样本边界是不是已经塌掉了，以及哪些特征的含义是不是已经丢失了。实际上，更早就必须问清下面这些问题。

| 现在看到的现象 | 在 Part 3 里更应该先问的问题 |
| --- | --- |
| 整个后段传感器区间都空了 | 这条样本还能作为一次动作级比较单位来使用吗？ |
| 只有少数时点缺失 | 做出汇总值后，还能保持同样的结构比较吗？ |
| 只有某一个传感器经常缺失 | 缺失本身是不是一种运行信号？ |

所以，带有缺失值的样本，不只是 `一张等着填值的表`，而是 `需要重新检查样本边界和特征含义的案例`。对于第一次看这张表的读者来说，先区分 `部分缺失`、`区间缺失`、`样本边界坍塌`，理解通常会更快。

## 先要区分的三种情况

有空值时，与其先谈复杂方法，不如先区分下面三种情况。

| 先区分什么 | 换成问题就是 |
| --- | --- |
| 只是部分值缺失吗 | 是某个区间平均值的一部分缺了，还是某个传感器的一部分缺了？ |
| 是不是整段区间都缺了 | 前段/中段/后段里，有没有一整个块消失了？ |
| 样本本身的意义是不是已经坏掉了 | 整次动作还容易被当作同一种案例吗？ |

之所以需要这种区分，是因为 `什么算缺失` 的定义不同，后面的判断就会完全不同。`只是缺了一部分值` 和 `动作的结尾已经没了`，表面上都像空白，但真正要做的决定并不一样。

## 看起来都像缺失，其实可能是不同问题

例如，下面三种情况都看起来像是 `没有值`，但实际含义并不相同。

| 看见的问题 | 更接近的解释 |
| --- | --- |
| 缺了 1 到 2 个时点 | 局部测量缺失 |
| 后 20% 区间整段都缺了 | 会动摇结构比较的区间缺失 |
| 没有 `event_end`，连结束时点都不知道 | 样本边界坍塌 |

第一种情况，可能仍然是在同一条样本结构里丢掉了部分信息。第二种情况则会直接动摇“后段下降率”这类特征的含义。第三种情况则更严重，因为整次动作的开始和结束都没有闭合，样本本身可能都要重新判断。

## 所以，在这个阶段最先要决定什么

比起复杂的缺失值补全技术，更重要的是先把下面四个判断写下来。

| 先要写下来的判断 | 为什么需要 |
| --- | --- |
| 这条样本是否保留 | 为了判断它还能不能作为同一种可比较案例 |
| 哪些特征不应该生成 | 为了阻止那些因为区间缺失而失去意义的特征 |
| 缺失本身要不要保留成标记列 | 因为缺失本身可能就是运行信号 |
| 是否需要重新查看原始日志 | 因为这可能不是单纯空值，而是样本边界问题 |

所以，这里真正关心的，与其说是 `怎么补`，不如说更接近 `这条样本现在应该被归到什么状态`。常见的判断顺序通常是 `是否保留样本 -> 哪些特征不能做 -> 缺失本身要不要作为标记列保留`。

## 用一个小图来看

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-5-mermaid-01-zh.mmd"
```

这张图说明：我们并不把 `为空` 看成单一状态。判断会随着缺失发生的位置和样本边界状态而分叉。也就是说，这一节的例子重点，与其说是在展示数值本身，不如说是在先展示一个判断结构：它会分成 `保留`、`排除特征`、`结构坍塌` 三条路。

## 为什么缺失本身也可以保留成一列

人们常常只会想到 `空白应该去掉`。但在实际场景里，缺失本身也可能带有含义。

| 缺失状态 | 为什么可以保留成标记列 |
| --- | --- |
| 某个传感器只在特定条件下经常缺失 | 它可能是运行模式或通信状态的信号 |
| 临近结束前的区间经常缺失 | 它可能和事件结束识别失败有关 |
| 只在某一段时期缺失 | 它可能和系统变更或维护状态有关 |

所以，在 Part 3 里，也有必要判断像 `missing_sensor_flag`、`late_segment_missing` 这样的标记列是否值得留下来。这并不是说它们已经被固定成模型输入，而是说：在立刻删掉缺失之前，先判断缺失本身是否应该作为结构信息留下来。

只要先做了这个判断，就不会把 `可以补的值` 和 `已经破坏样本结构的缺失` 混在一起。关键不在于某种处理技术的名字，而在于更早地分清：这条样本是否仍然是同一种比较单位，以及缺失本身是否应作为结构信息留下。

## 小型代码示例

问题情境：确认带有缺失值的样本并不都处于同一种状态；有些只是需要避开特定特征，有些则是样本结构本身已经坏掉了。

输入(input)：[`p3_5_5_missing_segments.csv`](/AiBook/assets/part-03/chapter-05/p3_5_5_missing_segments.csv){: target="_blank" rel="noopener noreferrer" } 文件。一行是一条动作汇总行，空值表示该区间平均值没有生成出来。部分缺失样本是否保留，由 `keep_partial_samples` 控制。

期望输出(output)：把 `late_segment_missing`、`sample_structure_broken`、`keep_sample`、`avoid_features` 一起整理出来的输出。改变 `keep_partial_samples` 时，只存在部分区间缺失的样本是否保留也会改变。

要确认的概念：在补缺失之前，应先把情况分类成 `保留样本`、`排除特征`、`结构坍塌`。是否允许部分缺失，应该作为明确的策略留下来。

```python
# 这个例子在聚合前检查并标记数值缺失或区间为空的样本。
import csv
from collections import Counter
from pathlib import Path

keep_partial_samples = True
preview_count = 9

data_path = Path("docs/assets/part-03/chapter-05/p3_5_5_missing_segments.csv")

def parse_optional_float(value):
    return None if value == "" else float(value)

with data_path.open(newline="", encoding="utf-8") as file:
    summary = []
    for row in csv.DictReader(file):
        early = parse_optional_float(row["early_flow_mean"])
        mid = parse_optional_float(row["mid_flow_mean"])
        late = parse_optional_float(row["late_flow_mean"])
        end_detected = int(row["end_detected"])
        late_segment_missing = int(late is None)
        sample_structure_broken = int(end_detected == 0)

        if sample_structure_broken:
            keep_sample = "no"
            avoid_features = "all event-level features"
        elif late_segment_missing and not keep_partial_samples:
            keep_sample = "no"
            avoid_features = "late_drop features"
        elif late_segment_missing:
            keep_sample = "yes"
            avoid_features = "late_drop features"
        else:
            keep_sample = "yes"
            avoid_features = "none"

        summary.append(
            {
                "event_id": row["event_id"],
                "early_flow_mean": early,
                "mid_flow_mean": mid,
                "late_flow_mean": late,
                "late_segment_missing": late_segment_missing,
                "sample_structure_broken": sample_structure_broken,
                "keep_sample": keep_sample,
                "avoid_features": avoid_features,
            }
        )

def fmt(value):
    return "missing" if value is None else f"{value:.2f}"

print("1) missingness flags")
for row in summary[:preview_count]:
    print(
        f'{row["event_id"]}: '
        f'late={fmt(row["late_flow_mean"]):<7} '
        f'late_missing={row["late_segment_missing"]} '
        f'boundary_broken={row["sample_structure_broken"]}'
    )
print(f"... {len(summary) - preview_count} more event summaries")
print()
print("2) sample decision")
for row in summary[:preview_count]:
    print(
        f'{row["event_id"]}: keep={row["keep_sample"]:<3} '
        f'avoid={row["avoid_features"]}'
    )
print()
print("3) decision counts")
for decision, count in sorted(Counter(row["keep_sample"] for row in summary).items()):
    print(f"keep_sample={decision}: {count}")
for feature_group, count in sorted(Counter(row["avoid_features"] for row in summary).items()):
    print(f"avoid={feature_group}: {count}")
```

期望输出：

```text
1) missingness flags
E01: late=1.80    late_missing=0 boundary_broken=0
E02: late=missing late_missing=1 boundary_broken=0
E03: late=missing late_missing=1 boundary_broken=1
E04: late=1.75    late_missing=0 boundary_broken=0
E05: late=missing late_missing=1 boundary_broken=0
E06: late=missing late_missing=1 boundary_broken=1
E07: late=1.82    late_missing=0 boundary_broken=0
E08: late=missing late_missing=1 boundary_broken=0
E09: late=missing late_missing=1 boundary_broken=1
... 27 more event summaries

2) sample decision
E01: keep=yes avoid=none
E02: keep=yes avoid=late_drop features
E03: keep=no  avoid=all event-level features
E04: keep=yes avoid=none
E05: keep=yes avoid=late_drop features
E06: keep=no  avoid=all event-level features
E07: keep=yes avoid=none
E08: keep=yes avoid=late_drop features
E09: keep=no  avoid=all event-level features

3) decision counts
keep_sample=no: 12
keep_sample=yes: 24
avoid=all event-level features: 12
avoid=late_drop features: 12
avoid=none: 12
```

这个例子的核心，不是如何填值，而是 `局部区间缺失` 和 `样本结构坍塌` 不能被当成同一种空白来处理。这里可以操作的值是 `keep_partial_samples`。如果它是 `True`，像 `E02` 这样的行会作为样本保留，但后段下降特征会被保守地排除。改成 `False` 时，存在部分区间缺失的 12 行也会从比较候选中排除。相反，像 `E03` 这样的行，样本边界本身已经不稳定，因此不管采用哪种策略，都很难立刻作为动作级比较样本使用。第 1 步里，我们先区分缺失发生在什么位置；第 2 步里，这种区分又会直接通向 `样本是否保留` 和 `哪些特征不应继续生成` 的判断。

这里最后要确认的是三件事：这条样本是否仍然是同一种比较单位；因缺失而不该生成的特征是否已经区分出来；缺失本身要不要作为标记列保留。只有这三点一起成立，空白才不只是 `待清洗对象`，而会变成一个夹带着样本结构判断的数据建模项。

值缺失这件事，不只是[预处理(preprocessing)](/AiBook/zh/reference/concept-glossary-pinyin/y/#preprocessing)问题。它更像一个数据建模信号，要求我们重新问：这条样本是否仍然是同一种比较单位，以及缺失本身是否应被保留成结构信息。所以，说“处理缺失”，与其说是补空白，不如说更接近重新划定边界：哪些样本还应继续比较，哪些样本应从比较中撤回。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。因为 example 预设的是特征和标签附着在同一个单位上，所以它支持这一点：当缺失已经动摇样本边界时，应该先判断这条样本是否仍然是同一种比较单位，而不是先急着补值。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `feature engineering`。它把 feature engineering 解释为把原始数据变成更适合学习和比较的形式，因此强化了这一节的判断：那些因为区间缺失而失去意义的特征，不应该继续生成。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. provenance framework 说明派生关系和处理步骤应当可解释，因此它提供了一个更高层的框架：缺失发生的位置，以及样本结构是否已经坍塌，都应作为独立信息保留下来，后面才能再次判断质量和可复现性。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- scikit-learn developers, `Imputation of missing values`. 它说明删除含缺失值的行或列可能造成有价值数据的损失，`MissingIndicator` 可以保留哪些值曾经缺失的信息，因此支持这一节的说明：应先判断缺失本身是否需要作为标记列留下来。 [https://scikit-learn.org/stable/modules/impute.html#marking-imputed-values](https://scikit-learn.org/stable/modules/impute.html#marking-imputed-values){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
