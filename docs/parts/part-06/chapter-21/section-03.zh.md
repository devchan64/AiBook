# P6-21.3 每次改变一个条件来评估公开扩散模型

> Section ID: `P6-21.3`
> Version: `v2026.08.28`

P6-21.1 讨论了模型公开了什么，以及许可证和公开范围；P6-21.2 则区分了运行可行性、内存放置和质量判断。现在把这些标准应用到公开扩散模型的小型比较实验中。目的不是选出最漂亮的图像，而是确认 Part 5 学到的 seed、steps、scheduler 和条件如何体现在实际运行记录与结果差异中。

本节的问题是：**在公开扩散模型中每次只改变一个值时，如何分别评估输出差异、运行负担和可复现性**？

## 比较前要固定的共同条件

如果在一次运行中同时改变 prompt、seed、steps 和 scheduler，即使图像变了，也无法知道是哪个值造成的影响。先记录以下条件，并在同一组比较中保持不变。

| 要固定的内容 | 记录原因 |
| --- | --- |
| 模型 ID、revision、许可证检查结果 | 确认比较使用的是相同权重和使用条件 |
| prompt、negative prompt、分辨率 | 保持场景要求和输入规模一致 |
| dtype、设备、offload 方式 | 避免把速度或内存差异误认为模型设置差异 |
| 评估标准 | 区分个人是否喜欢结果与结果是否满足条件 |

评估标准可以设为“条件符合度”“结构保持”“不必要的失真”“运行时间”“内存”和“可复现性”。这些标准不是给模型排出绝对名次的评分表，而是用来观察一个改动值造成了什么差异的记录栏。

## 每次只改变一项的四个比较轴

下面四个轴并不是必须全部完成的测试清单，而是帮助你选出符合当前问题的一个比较轴。在同一组比较中，只改变某一行“要改变的值”一栏中的内容，其余条件保持不变。

| 测试轴 | 固定值 | 要改变的值 | 要观察的问题 |
| --- | --- | --- | --- |
| 起点 | 模型、prompt、steps、scheduler、guidance | seed | 不同初始噪声如何改变场景变体？ |
| 迭代路径 | 模型、prompt、seed、guidance | steps 或 scheduler 中的一项 | 迭代次数或更新规则会怎样影响时间、结构和细节？ |
| 条件强度 | 模型、prompt、seed、steps、scheduler | guidance | 条件符合度与失真、多样性之间有什么权衡？ |
| 条件类型 | 模型、seed、分辨率、评估标准 | 仅文本／参考图像／结构条件 | 新增条件固定了什么，又减少了哪些自由度？ |

例如，比较 seed 时如果也改变 steps，起点和迭代路径就会同时变化。比较 `seed=12` 与 `seed=34` 时，要保持 prompt、模型 revision、分辨率、steps、scheduler 和 guidance 相同。这样才能把图像发生变化这一事实，与“初始噪声起点”这一个解释联系起来。

```mermaid
--8<-- "assets/part-06/chapter-21/p6-21-3-one-variable-test-flow-zh.mmd"
```

## 运行成功与结果评价要分栏记录

生成完成这一事实属于运行可行性的记录。是否遵循条件、是否保持结构，属于质量记录。运行时间过长或内存不足，属于运用记录。把这三者合并成一句话，会让下一步选择变得模糊。

| 类别 | 检查问题 | 记录示例 |
| --- | --- | --- |
| 运行可行性 | 是否没有报错并完成了生成？ | status、错误信息、dtype、device |
| 质量 | 是否能看到符合所改条件的差异？ | condition match、structure preservation、artifact note |
| 运用负担 | 时间和内存需求是否允许重复运行？ | elapsed seconds、peak memory、重试成本 |
| 可复现性 | 在相同条件下重新运行时，哪些内容保持不变？ | seed、revision、scheduler、reproducibility note |

模型库、硬件和计算方式不同，未必总能复现完全相同的像素。即使如此，也不要只记录“seed 相同但结果不同”，还应把模型 revision、设备、dtype、scheduler 和库版本列为待检查项。

## 用最小记录模板完成比较

下面的 CSV 是每行对应一次运行的最小模板。可以按需添加图像保存路径或详细的人工检查备注，但不能遗漏比较中改变的值与固定的值。

[P6-21.3 运行记录 CSV 模板](/AiBook/assets/part-06/chapter-21/p6-21-3-diffusion-test-record-template.csv){ .csv-preview }

填写记录后，尝试回答以下三个问题来说明结果。

1. 这一组比较改变了什么值？
2. 其余哪些条件保持不变？
3. 输出、运行时间、内存和可复现性方面观察到了什么差异？

如果答案只有“更漂亮了”，就需要重新审视比较。例如，应当把改动值与观察结果联系起来：“只把 guidance 从 5 改为 9 后，prompt 中的颜色条件更明确了，但边缘失真增加，运行时间则几乎不变。”这样，公开扩散模型的实际测试就在 Part 6 中形成包含学习、运行与评估记录的完整过程。

## 检查清单

- 能在比较前固定并记录模型 ID、revision、许可证、输入和运行环境。
- 能解释为什么 seed、steps、scheduler、guidance 和条件输入每次只能改变一项。
- 能将运行成功、输出质量、运用负担和可复现性的判断分栏记录。
- 能把结果差异与改动的一个值联系起来，提出下一次测试的问题。

## 来源与参考资料

- Hugging Face Diffusers, [Reproducible pipelines](https://huggingface.co/docs/diffusers/using-diffusers/reusing_seeds){: target="_blank" rel="noopener noreferrer" }, 官方文档，查阅日期：2026-08-28。用于参考如何通过 generator 和 seed 管理扩散流水线的随机起点。
- Hugging Face Diffusers, [Schedulers](https://huggingface.co/docs/diffusers/using-diffusers/schedulers){: target="_blank" rel="noopener noreferrer" }, 官方文档，查阅日期：2026-08-28。用于说明 scheduler 是改变生成过程迭代路径的设置。
