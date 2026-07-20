# P3-2.2 数据集候选里要放进哪些结构

> Section ID: `P3-2.2`
> Version: `v2026.07.20`

正如前一节所看到的，已存的记录还不一定就是数据集。那么下一个问题就会立刻接上来：如果要重新做出一个数据集候选，里面到底应该放进哪些结构？为了回答这个问题，Part 3 会把 [sample](/AiBook/en/reference/concept-glossary/#glossary-sample)、[feature](/AiBook/en/reference/concept-glossary/#glossary-feature)、[baseline](/AiBook/en/reference/concept-glossary/#glossary-baseline)、[output structure](/AiBook/en/reference/concept-glossary/#glossary-output-structure) 放在一起看。与其把这些词当成彼此分开的记忆清单，不如把它们读成一个数据集设计结构。只有先决定什么算一条样本，才能做出特征；只有有了特征，才能决定该拿什么和基准线比较；只有这层比较先成立，才能决定最后要做成什么输出结构。

这一节尤其重要的一点，是在它还没有直接凝固成 [target](/AiBook/en/reference/concept-glossary/#glossary-target) 之前，先把 `输出结构` 读成一种问题设计轴：它负责区分面向复核的结果和面向预测的目标候选。这也是为什么数据集候选不能被读成单一表名，而要读成几种互相连接的结构。只有“什么算样本、保留哪些特征、和什么基准线比较、最后以什么输出结构收口”这些判断一起定下来，数据集候选的含义才会清楚。

以一次自动执行的动作为例。样本可以是 `把这一次完整动作看成一条案例`。特征可以是从这次动作里计算并留下来的值，例如 `总时长`、`中段均值`、`后段下降率`、`跟踪误差`。基准线可以是非近期区段的代表值，或者平常状态的比较群体。输出结构则是人或模型最后要读到的结果形式，例如 `需要复核`、`注意`、`正常范围`，或者 `预测标签候选`。

这层关系可以先整理成下面这张表。

| 组成要素 | 这里表示什么 | 当前阶段在问的问题 |
| --- | --- | --- |
| 样本 | 作为比较或学习基本单位的一条案例 | 什么算一行？ |
| 特征 | 为了描述样本而计算并保留下来的值 | 哪些值该留下，比较才会更容易？ |
| 基准线 | 用来和近期状态比较的平常结构或参考群体 | 和什么比较，变化才会显现？ |
| 输出结构 | 人要读、或模型下一步要接收的结果形式 | 最终想做出什么判断？ |

把这四个要素放在一起，就能看出为什么数据建模不是单纯整理。比如说，如果还没决定样本是 `一个时点测量` 还是 `一次完整动作`，就不可能稳定地定特征，因为适合时点表的特征，和适合动作级表的特征并不一样。同样地，如果不先定好基准线，近期区段的变化也很难读出来。再进一步，如果输出结构还没定清楚是 `生成复核候选` 还是 `输出预测标签`，连需要什么比较也会变得模糊。

也就是说，这四个要素并不是要分开背的术语表，而是构造数据集候选时从前到后连起来的一套设计顺序。样本一晃，特征也会晃；特征一晃，基准线比较也会晃；比较一晃，输出结构也会跟着晃。所以这一节先固定的是：它们应该按照怎样的问题顺序连接起来。

在实际里，问题通常按下面这个顺序接起来。

1. 现在要比较的对象，是一个时点、一次完整动作，还是一个近期区段？
2. 要描述这个对象，应该留下哪些数字？
3. 这些数字要和什么比较，才会产生意义？
4. 最后的结果，是要输出成人能读的判断语句，还是输出成模型会接收的标签候选？

这四个问题分别对应样本、特征、基准线、输出结构。所以，即使术语本身还有些模糊，只要顺着这套问题顺序往下读，也能重新确认自己现在站在哪一步的数据集设计阶段。

下面这张表更具体地展示了：这四个要素是怎么在同一行里接起来的。哪怕同样是一条“完整动作”，也是先把样本立成一条案例，再在上面写入特征，再把这些特征和基准线比较，最后再收口为一个人能读的输出。

| sample_id | mean_flow | late_drop_rate | baseline_mean_flow | baseline_late_drop_rate | baseline_gap | output |
| --- | --- | --- | --- | --- | --- | --- |
| A | 0.74 | -0.32 | 0.92 | -0.05 | -0.27 | `需要复核` |
| B | 0.89 | -0.08 | 0.92 | -0.05 | -0.03 | `正常范围` |

读这张表的顺序，会自然地从左往右走。`sample_id` 固定了什么被算成一条样本。`mean_flow` 和 `late_drop_rate` 是描述这条样本的特征。`baseline_mean_flow` 和 `baseline_late_drop_rate` 是平常状态的基准线。`baseline_gap` 写下比较结果，说明当前样本的后段下降率比基准线多下降了多少。只要这个比较结果足够大，`output` 列里就会形成像 `需要复核` 这样的运营判断。

换句话说，`需要复核` 这样的输出，并不是在表最末尾突然贴上的一句话。只有前面的列已经把 `比较什么` 和 `什么地方偏离平常` 整理清楚，最后那一列输出才能被解释。所以，样本、特征、基准线、输出结构即使都放在同一张表里，也不是彼此独立的清单，而是一条从前往后串起来的设计流。

## 用一个小图来看

如果把数据集候选里的四种结构压成 `样本 -> 特征 -> 基准线比较 -> 输出结构` 这条顺序，就能一眼看清它们是怎样咬合的。

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-2-mermaid-01-zh.mmd"
```

问题情境：确认把一次动作当作一条样本之后，如何写入特征、和平常基准线比较，并最终生成运营输出。

输入(input)：同时包含 `baseline` 区段和 `recent` 区段的逐时刻流量日志 [p3_2_2_event_flow_log.csv](/AiBook/assets/part-03/chapter-02/p3_2_2_event_flow_log.csv)，以及决定是否送去复核的候选阈值 `review_gap_thresholds`

输入文件的一行表示某个样本在特定秒(`second`)测得的流量(`flow`)。`sample_id` 指向一次动作，`period` 区分这个样本属于用来建立平常参考的 `baseline` 区段，还是属于要被比较的 `recent` 区段。

期望输出(output)：原始日志会依次生成 `样本行 -> 特征表 -> 基准线生成 -> recent 样本比较表 -> 运营输出`，并且当 `review_gap_thresholds` 取不同值时，复核候选数量会改变。

要确认的概念：输出结构和基准线不是事先写好的结果列，而是在原始日志按样本单位重组、计算特征、区分 period 角色之后生成的。用多个输出标准比较，才能看出运营判断对阈值有多敏感。

```python
# 这个例子检查数据集候选中样本、特征、标签和基准列的作用。
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

event_log_path = "docs/assets/part-03/chapter-02/p3_2_2_event_flow_log.csv"
selected_review_gap_threshold = -0.20
review_gap_thresholds = [-0.36, selected_review_gap_threshold, 0.0]

event_log = pd.read_csv(event_log_path)

print("1) raw input shape and first rows")
print("shape:", event_log.shape)
print(event_log.head())
print()

sample_rows = event_log[["sample_id", "period"]].drop_duplicates().reset_index(drop=True)
print("2) sample rows")
print(sample_rows)
print()

feature_table = (
    event_log.sort_values(["sample_id", "second"])
    .groupby(["sample_id", "period"], as_index=False)
    .agg(
        mean_flow=("flow", "mean"),
        late_drop_rate=("flow", lambda values: values.iloc[-1] - values.iloc[-2]),
    )
)
print("3) add features")
print(feature_table.round(2))
print()

baseline = (
    pd.DataFrame(
        [
            {
                "baseline_mean_flow": feature_table.loc[
                    feature_table["period"] == "baseline", "mean_flow"
                ].mean(),
                "baseline_late_drop_rate": feature_table.loc[
                    feature_table["period"] == "baseline", "late_drop_rate"
                ].mean(),
            }
        ]
    )
)
print("4) build baseline from baseline samples")
print(baseline.round(2))
print()

comparison_table = feature_table[feature_table["period"] == "recent"].copy()
comparison_table["baseline_mean_flow"] = baseline.loc[0, "baseline_mean_flow"]
comparison_table["baseline_late_drop_rate"] = baseline.loc[0, "baseline_late_drop_rate"]
comparison_table["baseline_gap"] = (
    comparison_table["late_drop_rate"] - comparison_table["baseline_late_drop_rate"]
)
print("5) compare recent samples with baseline")
print(comparison_table.round(2))
print()

selected_output_table = None
threshold_results = []
for threshold in review_gap_thresholds:
    output_table = comparison_table.copy()
    output_table["output"] = output_table["baseline_gap"].apply(
        lambda gap: "needs review" if gap <= threshold else "normal range"
    )
    if threshold == selected_review_gap_threshold:
        selected_output_table = output_table.copy()
    threshold_results.append(
        {
            "review_gap_threshold": threshold,
            "review_count": int((output_table["output"] == "needs review").sum()),
            "review_samples": ",".join(
                output_table.loc[output_table["output"] == "needs review", "sample_id"]
            )
            or "none",
        }
    )

print("6) final output structure when review_gap_threshold = -0.20")
print(selected_output_table.round(2))
print()
print("7) threshold sensitivity")
print(pd.DataFrame(threshold_results))
```

期望输出：

```text
1) raw input shape and first rows
shape: (36, 4)
  sample_id    period  second  flow
0        B1  baseline       0  0.80
1        B1  baseline       1  0.92
2        B1  baseline       2  1.02
3        B1  baseline       3  1.04
4        B1  baseline       4  1.00

2) sample rows
  sample_id    period
0        B1  baseline
1        B2  baseline
2        B3  baseline
3        R1    recent
4        R2    recent
5        R3    recent

3) add features
  sample_id    period  mean_flow  late_drop_rate
0        B1  baseline       0.96           -0.04
1        B2  baseline       0.94           -0.06
2        B3  baseline       0.92           -0.04
3        R1    recent       0.83           -0.32
4        R2    recent       0.90           -0.08
5        R3    recent       0.94           -0.40

4) build baseline from baseline samples
   baseline_mean_flow  baseline_late_drop_rate
0                0.94                    -0.05

5) compare recent samples with baseline
  sample_id  period  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap
3        R1  recent       0.83           -0.32                0.94                    -0.05         -0.27
4        R2  recent       0.90           -0.08                0.94                    -0.05         -0.03
5        R3  recent       0.94           -0.40                0.94                    -0.05         -0.35

6) final output structure when review_gap_threshold = -0.20
  sample_id  period  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap        output
3        R1  recent       0.83           -0.32                0.94                    -0.05         -0.27  needs review
4        R2  recent       0.90           -0.08                0.94                    -0.05         -0.03  normal range
5        R3  recent       0.94           -0.40                0.94                    -0.05         -0.35  needs review

7) threshold sensitivity
   review_gap_threshold  review_count review_samples
0                 -0.36             0           none
1                 -0.20             2          R1,R3
2                  0.00             3       R1,R2,R3
```

这个例子展示的是：原始日志里的同一批行如何逐步变成数据集候选结构。最开始，`event_log` 先用 `sample_id` 和 `period` 抓出样本行，然后从逐时刻流量中计算 `mean_flow` 和 `late_drop_rate`。接着，只用 `baseline` 区段的样本生成基准线，再把 `recent` 区段的样本拿来和它比较。最后的运营输出不是原本就存在的列，而是从 `baseline_gap` 和 `review_gap_thresholds` 生成的。阈值设为 `-0.36` 时，没有复核候选；设为 `-0.20` 时，R1 和 R3 会成为复核候选；设为 `0.0` 时，三个 recent 样本都会成为复核候选。也就是说，输出列不是单独存在的，而是承接 `样本设定 -> 特征计算 -> 基准线生成 -> 基准线比较 -> 运营判断标准` 这些阶段的结果之后才生成的。

如果再把同一张表拆解得更细一些，就能更清楚地看到：四种结构分别落在表里的哪些格子上。

| 列名 | 这里承担的角色 | 为什么要这样读 |
| --- | --- | --- |
| `sample_id` | 样本标识符 | 因为它指向什么被算成一条案例 |
| `mean_flow`, `late_drop_rate` | 特征 | 因为它们描述的是样本的状态 |
| `baseline_mean_flow`, `baseline_late_drop_rate` | 基准线列 | 因为它们单独写下了平常区段的代表值 |
| `baseline_gap` | 基准线比较列 | 因为它直接写下当前样本和基准线之间的差值 |
| `output` | 输出结构 | 因为它是人要读、或下一阶段要接收的结果形式 |

这张表说明，`数据集候选` 并不是单纯指“列很多的表”，而是指同一行里放着 `样本`、`描述值`、`比较结果`、`结果形式`，并且这些部分彼此分工的结构。

这里还要再固定一个重要差别。输出结构并不一定意味着 `已经有正确标签的训练数据`。`需要复核`、`正常范围` 这样的输出，看起来可能和 `yes/no` 这样的监督学习标签很像，但在实际里它们并不一定相同。

| 输出结构表示什么 | 在当前阶段应该怎么读 |
| --- | --- |
| `需要复核`、`注意`、`正常范围` | 人要先检查的运营结果 |
| `正常/异常` 这类固定标签 | 以后可以送进预测问题的目标标签候选 |

只要先把这个区分放好，后面再谈 `输出结构` 时，就不容易误解成 `标签已经完全做好了`。

把这条流程再压短一点，可以记成下面这个顺序。

1. 先决定什么算一条样本。
2. 留下描述这条样本的特征。
3. 建立比较近期与平常状态的基准线。
4. 决定人要读、或模型要接收的输出结构。

这四个阶段在后面会分别展开成不同章节，但在实际里，它们是一条连续判断。所以无论读到哪一章，只要一起追问 `现在这段说明属于样本、特征、基准线、输出结构里的哪一步`，就不容易迷失。一旦抓住 `先定样本才有特征，先定特征才有比较结构，有了比较结构输出结构才会整理出来` 这层关系，就会更清楚：数据集候选不是某一个文件名，而是一张让这四种结构彼此咬合的设计表。从更宽一点的角度看，这一节建立的是一个最小契约：它整理了 `example 单位`、`描述变量`、`比较基准`、`结果形式` 在同一个数据问题里按什么顺序咬合。因此，数据集候选不该被读成 `列很多的表`，而该被读成：在同一个 example 里，描述值、比较基准、结果形式各自分工的结构。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `example`、`labeled example`、`feature`、`label`。它分开说明 feature 和 label 在一个 example 里的角色，因此支持本节把样本、特征、基准线、输出结构读成同一张表里的分工结构。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 它提供了“比较用参考区段”的一般概念，因此强化了本节的说明：当前样本的值只有在和基准线比较之后，才真正产生意义。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. 它说明 derivation 和 activity context 应当一起保留，因此强化了本节的上位框架：输出结构是前面的样本设定、特征计算、基准线比较之后才生成的结果。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
