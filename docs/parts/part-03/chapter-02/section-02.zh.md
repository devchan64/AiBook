# P3-2.2 数据集候选里要放进哪些结构

> Section ID: `P3-2.2`
> Version: `v2026.09.19`

如前一节所示，即使已经存储了数据集，也可能需要按照当前问题重新组织。接下来的问题自然是：重新构建[候选数据集](/AiBook/zh/reference/concept-glossary-pinyin/d/#dataset)时，里面应包含哪些结构？Part 3 为回答这个问题，会一起看[样本](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)、[特征](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)、[基准线](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-baseline)和[输出结构](/AiBook/zh/reference/concept-glossary-pinyin/s/#output-structure)。把这些词理解为相互连接的数据集设计，比逐项背诵更准确。先确定什么算一条样本，才能构造特征；有了特征，才能决定拿什么与基准线比较；有了比较，才能决定构造什么输出结构。

这一节尤其重要的一点，是在它还没有直接凝固成 [target](/AiBook/zh/reference/concept-glossary-pinyin/m/#target) 之前，先把 `输出结构` 读成一种问题设计轴：它负责区分面向复核的结果和面向预测的目标候选。这也是为什么数据集候选不能被读成单一表名，而要读成几种互相连接的结构。只有“什么算样本、保留哪些特征、和什么基准线比较、最后以什么输出结构收口”这些判断一起定下来，数据集候选的含义才会清楚。

下面四个要素是本书状态比较案例的设计框架，并不是说每个数据集都必须包含基准线列和输出列。例如，无标签图像集合也叫数据集；特征可以是直接测量的值或类别，并不一定要通过汇总计算得到。

以一次动作为样本时，测得的流量或运行模式可以直接来自原始记录，均值和斜率则可以计算得到。本节把平均流量和最后区间斜率作为特征，以相同条件下的历史动作作为基准线。输出是指定规则产生的 `review` 或 `no_flag`，并非确认实际故障的标签。

这层关系可以先整理成下面这张表。

| 组成要素 | 这里表示什么 | 当前阶段在问的问题 |
| --- | --- | --- |
| 样本 | 作为比较或学习基本单位的一条案例 | 什么算一行？ |
| 特征 | 表示样本的观测值、类别或计算值 | 哪些值该留下，比较才会更容易？ |
| 基准线 | 用来和近期状态比较的平常结构或参考群体 | 和什么比较，变化才会显现？ |
| 输出结构 | 人要读、或模型下一步要接收的结果形式 | 最终想做出什么判断？ |

把这四个要素放在一起，就能看出为什么数据建模不是单纯整理。比如说，如果还没决定样本是 `一个时点测量` 还是 `一次完整动作`，就不可能稳定地定特征，因为适合时点表的特征，和适合动作级表的特征并不一样。同样地，如果不先定好基准线，近期区段的变化也很难读出来。再进一步，如果输出结构还没定清楚是 `生成复核候选` 还是 `输出预测标签`，连需要什么比较也会变得模糊。

也就是说，这四个要素并不是要分开背的术语表，而是构造数据集候选时从前到后连起来的一套设计顺序。样本一晃，特征也会晃；特征一晃，基准线比较也会晃；比较一晃，输出结构也会跟着晃。所以这一节先固定的是：它们应该按照怎样的问题顺序连接起来。

在实际里，问题通常按下面这个顺序接起来。

1. 现在要比较的对象，是一个时点、一次完整动作，还是一个近期区段？
2. 要描述这个对象，应该留下哪些值或类别？
3. 在本例中，要把这些值与什么比较才能看出变化？
4. 最后的结果，是要输出成人能读的判断语句，还是输出成模型会接收的标签候选？

这四个问题分别对应样本、特征、基准线、输出结构。所以，即使术语本身还有些模糊，只要顺着这套问题顺序往下读，也能重新确认自己现在站在哪一步的数据集设计阶段。

下表使用与后面的 Python 示例相同的虚构 CSV，展示计算得到的近期动作 R1、R2、R3。每次动作在 0~5 秒有六条流量记录，最后区间均为 4~5 秒。流量和均值单位为 L/min，斜率和斜率差值单位为 L/min/s。显示值保留两位小数，但计算和规则应用使用未四舍五入的值。

| sample_id | mean_flow | late_drop_rate | baseline_mean_flow | baseline_late_drop_rate | baseline_gap | output |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| R1 | 0.83 | -0.32 | 0.94 | -0.05 | -0.27 | `review` |
| R2 | 0.90 | -0.08 | 0.94 | -0.05 | -0.03 | `no_flag` |
| R3 | 0.94 | -0.40 | 0.94 | -0.05 | -0.35 | `review` |

基准动作 B1、B2、B3 的最后斜率分别为 −0.04、−0.06、−0.04 L/min/s。假定这三次动作代表相同条件下的平常状态，其均值为 `(-0.04−0.06−0.04)/3 = −0.046666… L/min/s`，表中显示为 −0.05。基准平均流量同样是三个动作平均流量的均值，四舍五入后为 0.94 L/min。

R1 从第 4 秒的 0.92 L/min 变为第 5 秒的 0.60 L/min，所以斜率为 `(0.60−0.92)/(5−4) = −0.32 L/min/s`。基准线差值是**当前斜率减去基准线斜率**。

- 按显示值阅读：`−0.32−(−0.05) = −0.27 L/min/s`。
- 四舍五入前的计算：`−0.32−(−0.046666…) = −0.273333… L/min/s`。
- 解释：两个斜率都表示下降，但 R1 比平常基准下降得更陡，差约 0.27 L/min/s。这不表示流量本身为负数。

应用虚构复核规则 `baseline_gap <= −0.20 L/min/s`，R1、R3 得到 `review`，R2 得到 `no_flag`。恰好 −0.20 也包含在内，因此 −0.21、−0.20、−0.19 中只有前两个符合规则。`no_flag` 只表示没有触发该规则，不表示确认正常，也不是无故障标签。

`sample_id` 标识对象，`mean_flow`、`late_drop_rate` 是对象特征，`baseline_gap` 是比较结果，`output` 是复核规则的结果。改变阈值不会改变观测值、斜率或基准线差值，而是改变人根据同一组数字优先检查什么的策略。本节通过角色表和计算区分这些概念，斜率在时间轴上的形状可结合前一节图表阅读。

## 样本、特征、基准线与输出的连接 {#_1}

如果把数据集候选里的四种结构压成 `样本 -> 特征 -> 基准线比较 -> 输出结构` 这条顺序，就能一眼看清它们是怎样咬合的。

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-2-mermaid-01-zh.mmd"
```

问题情境：确认把一次动作当作一条样本之后，如何写入特征、和平常基准线比较，并最终生成运营输出。

输入(input)：同时包含 `baseline` 区段和 `recent` 区段的逐时刻流量日志 [p3_2_2_event_flow_log.csv](/AiBook/assets/part-03/chapter-02/p3_2_2_event_flow_log.csv)，以及决定是否送去复核的候选阈值 `review_gap_thresholds`

输入文件的一行表示某个样本在特定秒(`second`)测得的流量(`flow`)。`sample_id` 指向一次动作，`period` 区分这个样本属于用来建立平常参考的 `baseline` 区段，还是属于要被比较的 `recent` 区段。

期望输出(output)：原始日志会依次生成 `样本行 -> 特征表 -> 基准线生成 -> recent 样本比较表 -> 运营输出`，并且当 `review_gap_thresholds` 取不同值时，复核候选数量会改变。

要确认的概念：输出结构和基准线不是事先写好的结果列，而是在原始日志按样本单位重组、计算特征、区分 period 角色之后生成的。用多个输出标准比较，才能看出运营判断对阈值有多敏感。

该 CSV 中每次动作都以 1 秒间隔测量且无缺失，并假定基准动作与近期动作的运行条件相同。代码先检查时间间隔，再把最后两个流量值之差作为每秒斜率。CSV 本身不含验证运行条件一致的资料，实际数据还需另行确认。

```python
# 区分样本特征、基准线差值和复核规则结果；这里没有实际故障标签。
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

event_log_path = "docs/assets/part-03/chapter-02/p3_2_2_event_flow_log.csv"
selected_review_gap_threshold = -0.20
review_gap_thresholds = [-0.36, selected_review_gap_threshold, 0.0]

event_log = pd.read_csv(event_log_path)
event_log = event_log.sort_values(["sample_id", "second"])
intervals = event_log.groupby("sample_id")["second"].diff().dropna()
if not intervals.eq(1).all():
    raise ValueError("This example requires 1-second observation intervals.")

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
        lambda gap: "review" if gap <= threshold else "no_flag"
    )
    if threshold == selected_review_gap_threshold:
        selected_output_table = output_table.copy()
    threshold_results.append(
        {
            "review_gap_threshold": threshold,
            "review_count": int((output_table["output"] == "review").sum()),
            "review_samples": ",".join(
                output_table.loc[output_table["output"] == "review", "sample_id"]
            )
            or "none",
        }
    )

print(f"6) final output structure when review_gap_threshold = {selected_review_gap_threshold:.2f}")
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
  sample_id  period  mean_flow  late_drop_rate  baseline_mean_flow  baseline_late_drop_rate  baseline_gap   output
3        R1  recent       0.83           -0.32                0.94                    -0.05         -0.27   review
4        R2  recent       0.90           -0.08                0.94                    -0.05         -0.03  no_flag
5        R3  recent       0.94           -0.40                0.94                    -0.05         -0.35   review

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

`review` 和 `no_flag` 是本例规则产生的结果。若要把它们当作真实故障标签，还需要检查记录、故障判定标准等独立依据。这份 CSV 不包含这些依据。

| 区分 | 本例中能够确认的内容 |
| --- | --- |
| 规则结果 | 是否按设定的阈值选为待检查样本 |
| 真实故障标签 | 是否通过独立检查确认了故障；仅凭当前 CSV 无法得知 |

列的作用也会随用途改变。例如，后续模型可以把 `baseline_gap` 用作输入特征。这里为了理解计算过程，将原有特征、与基准线的比较结果、检查规则的结果分开说明。并不是所有数值列都承担相同的作用。

确定样本、选择描述值、设定比较基准与输出规则之后，请把一行数据追溯到原始记录。如果能用 R1 的两个测量值计算斜率，再结合由 B1、B2、B3 得出的基准斜率和复核阈值，重现差值与 `review` 结果，就读懂了本例的结构。

## 检查清单

- 能否解释测量值或运行模式等原始值也可以作为特征？
- 能否从 CSV 找到 R1 第 4、5 秒的值，算出斜率 −0.32，再减去基准斜率重现差值？
- 能否说明 −0.32−(−0.05) 为何是负数，以及其单位表示什么？
- 是否检查了 −0.21、−0.20、−0.19 中哪些值被复核规则包含？
- 能否区分只改变阈值时哪些列改变、哪些列保持不变，并避免把 `review` 当作实际故障标签？

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `example`、`labeled example`、`feature`、`label`。它分开说明 feature 和 label 在一个 example 里的角色，因此支持本节把样本、特征、基准线、输出结构读成同一张表里的分工结构。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 它提供了“比较用参考区段”的一般概念，因此补充了本例中用参考值理解相对平时变化的说明。这并不意味着所有特征都必须与基准线比较才有意义。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. 它说明 derivation 和 activity context 应当一起保留，因此强化了本节的上位框架：输出结构是前面的样本设定、特征计算、基准线比较之后才生成的结果。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
