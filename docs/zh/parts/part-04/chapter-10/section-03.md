# P4-10.3 补充学习：第一次该怎样读回归诊断(regression diagnostics)

> Section ID: `P4-10.3`
> Version: `v2026.07.11`

读到 P4-10.2 为止，linear regression 的基本评价已经具备了。但在真实文档或课程里，读者很快还会碰到下面这些表达。

- statistical significance
- residual normality
- homoscedasticity
- multicollinearity

本节的目的，不是去学习这些概念的全部证明，而是整理 `这些词到底在担心什么`，让读者在看到 regression result 表时不要停住。

这段补充学习不会把 linear regression 的定义再扩展着重讲一遍。基本直觉和评价抓手仍然放在 P4-10.1、P4-10.2 与 [概念词汇表](../../../reference/concept-glossary.md) 里；这里的焦点只有一点：这些 regression diagnostic 术语各自在指向什么类型的风险。

## 本补充学习的范围

这一节回答下面这些问题。

- 为什么 regression diagnostics 会跟在线性回归后面出现？
- 读 statistical significance 时到底要小心什么？
- residual normality 与 homoscedasticity 分别在担心哪一类问题？
- 为什么 multicollinearity 会摇动 coefficient 的解释？

这一节不会深入讲下面这些内容。

- 各类检验统计量的公式推导
- 围绕 p-value 解读的完整历史争论
- VIF 练习与高级 regression package 的使用方法

这些步骤放在这本书当前正文范围之外。

## 本补充学习的目标

- 能把 regression diagnostics 解释成 `为了避免过度相信 linear regression 结果而做的检查`。
- 能区分 significance、normality、homoscedasticity、multicollinearity 分别在担心什么。
- 读 coefficient 表时，不会把 `有一个数字` 和 `解释是稳定的` 当成同一句话。

## 为什么回归诊断会被单独拿出来讲

linear regression 是一个去拟合直线的 model，但画出一条直线，并不代表解释就自动安全。所以 regression diagnostics 往往会继续追问下面这些问题。

1. 这条直线平均错了多少？
2. 这些误差会不会持续朝某一个方向偏？
3. 输入 feature 之间会不会重叠得太厉害，以至于 coefficient 解读不稳？
4. coefficient 表里的数字，到底能信到什么程度？

也就是说，regression diagnostics 不是 `性能分数` 的语言，而是 `解释稳定性` 的语言。

## statistical significance 在问什么

`这个 coefficient 或这种关系，会不会只是随机波动也能出现，还是说它在数据里看起来像一个相对一致的信号？`

重要的是，significance 不等于实际业务重要性，也不等于 prediction performance。

| 表达 | 入门式读取 |
| --- | --- |
| statistically significant | 很难只当作偶然波动来看待的信号 |
| practically important | 在实际决策里影响很大的关系 |

这两者可能不同。所以 significance 只是其中一个轴，它问的是 `这个数字为什么会出现`，并不能替代整个 model 质量。

## residual normality 在担心什么

用最简单的话说，residual normality 在担心的是：`误差会不会严重地往某个奇怪形状偏过去？`

在做 prediction 时，读者并不需要把 normality 感成绝对条件。但在 coefficient 解释或某些统计检验语境里，如果 residual 的形状严重向一边挤压，解释就可能变得不稳。

- 如果 residual 很长地拖向一边，解释要更谨慎
- 一个大的 outlier 就可能把 residual 形状强烈摇动

用一个很小的比较练习来看，可以读成下面这样。

```python
balanced_residuals = [-3, -1, 0, 1, 3]
skewed_residuals = [-1, 0, 1, 2, 12]

print("balanced residuals:", balanced_residuals)
print("skewed residuals  :", skewed_residuals)
print("balanced range    :", max(balanced_residuals) - min(balanced_residuals))
print("skewed range      :", max(skewed_residuals) - min(skewed_residuals))
```

一个示例输出如下。

```text
balanced residuals: [-3, -1, 0, 1, 3]
skewed residuals  : [-1, 0, 1, 2, 12]
balanced range    : 6
skewed range      : 13
```

这个比较不能替代 normality test，但它能马上 보여주는 것은：`误差大致平衡地散开` 的场景，与 `一侧拖出很长尾巴` 的场景之间到底有什么不同。入门层面上，只要把 residual normality 读成一种语言：`它首先担心误差会不会往一边拖得太长，从而摇动解释`，就已经够用了。

## homoscedasticity 在担心什么

homoscedasticity 在担心的是：误差的 spread 会不会随着输入区间不同而变化太大。

例如，在较小取值区间里 error 很小，但随着值变大，error 也越来越大，那么下面这些问题就会出现。

- model 是否只在某个区间特别不稳定？
- 这里是不是藏着一条直线很难解释的结构？

也就是说，homoscedasticity 的视角是在问：`误差在各区间里的 spread 是否大体相似？`

一个很小的比较表可以这样读。

| 输入区间 | residual 示例 | 先出现的担心 |
| --- | --- | --- |
| 较低价格段 | `-2, 1, 0` | 误差 spread 相对较小 |
| 较高价格段 | `-15, 12, 18` | 某个区间里的误差 spread 明显更大 |

在这种场景里，比起停在 `平均性能还可以`，读者更应该先去确认 `到底是哪个区间的解释开始崩掉`。

## 为什么 multicollinearity 会摇动 coefficient 解读

multicollinearity 出现在输入 feature 之间携带了太多重叠信息的时候。

例如，像下面这种强烈重叠的 feature：

- `monthly_spend`
- `quarterly_spend`
- `yearly_spend`

如果一起放进来，model 的 prediction 也许仍然还行，但 `到底哪个 feature 的 coefficient 真正更重要` 这件事就会变得更难稳定地说明。

核心点就是下面这句。

`能做 prediction` 和 `coefficient 的解释稳定` 不是同一句话。`

## 案例及示例

### 案例 1. 房价预测好像还行，但 coefficient 解释总在摇

一个房地产分析团队正在搭建房价预测回归式。人们先看的问题是 `面积越大是否越贵`、`越靠近车站是否价格越高`、`越新房是否价值越高`。

但即使输入列里没有像 `monthly_spend` 这样明显的重复名，`套内面积`、`供应面积`、`房间数`、`客厅数` 这样的信息仍然会强烈重叠地一起进入。prediction 本身可能看起来不错，但某次实验里面积 coefficient 更大，另一次实验里房间数 coefficient 又更大，甚至 coefficient 的方向也会不稳。在这种场景里，prediction performance 和 coefficient interpretation stability 绝不能当成同一句话。

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-3-mermaid-01-en.mmd"
```

这时 regression diagnostics 问的是：`这个数字到底能信到哪里？` multicollinearity 会因为相似 feature 彼此分摊解释角色，而让 coefficient 解读变得不稳；如果 homoscedasticity 破了，某些价格区间里的 error spread 会更大；如果 residual 形状向一侧偏去，解释也要更加谨慎。所以，得到一条直线，并不等于整个 coefficient 表立刻就是一个安全解释。

## 本节要记住的观念

- regression diagnostics 与其说是提高分数的技术，不如说是让解释更谨慎的检查。
- significance 主要摇动关系解释信号，homoscedasticity 摇动误差 spread，multicollinearity 则最明显地摇动 coefficient interpretation stability。
- 读 linear regression 表时，不只要问 `有没有数字`，还要问 `这个数字到底能信到什么程度`。

## 出处与参考资料

- statsmodels developers, [Regression diagnostics](https://www.statsmodels.org/stable/examples/notebooks/generated/regression_diagnostics.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-01.
- Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, [An Introduction to Statistical Learning](https://www.statlearning.com/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-01.
