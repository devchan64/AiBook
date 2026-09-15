# P3-7.5 基准线应该固定不动，还是应该按“最近的平时”一起更新

> Section ID: `P3-7.5`
> Version: `v2026.09.15`

在选好 [基准线(baseline)](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-baseline) 候选之后，还会留下另一个问题。`这个参考应该固定一段时间，还是应该和“最近的平时区间”一起移动？` 即使都已经选中了同条件下的区间，只要基准线的维护方式不同，比较句子的意义也会跟着变化。

基准线的维护方式，并不是一个要先固定“唯一正确答案”的问题。更自然的选择，会随着我们想看什么样的变化而改变。

| 基准线形式 | 更适合的问题 | 需要注意的地方 |
| --- | --- | --- |
| 固定基准线 | 相对某个特定参考点，我们改变了多少？ | 如果当前运行状态已经变了，它可能会变成过于陈旧的参考 |
| 最近平时基准线 | 在最近流程里，现在这个状态是不是特别不同？ | 如果区间抓得太短，基准线本身会变得不稳定 |

例如，如果我们想把设备校正之后的稳定区间长期保留为代表性参考，那么固定基准线就很自然。相反，如果运行环境是缓慢持续变化的系统，那么把“最近的平时区间”当作基准线，往往会更现实。真正重要的是，不管选哪一种方式，我们都应该能够用一句话说明：`现在到底是在拿当前状态和什么去比。`

## 移动的基准线可能掩盖长期变化

在一个虚构例子中，假设刚校准后的均值为 100，近期平时均值为 108，当前值为 110。与固定基准线的差为 +10，与近期平时状态的差为 +2。两种计算都正确，但前者表示校准以来的累计变化，后者表示相对近期状态的新增变化。基准线持续移动时，缓慢发生的变化可能看起来只有很小的差异。

构造近期平时基准线时，应先规定不把当前比较对象混入其中。例如，将当前值 130 与过去的 100、100 比较，差为 +30。如果把当前值也放进基准均值，基准就变成 110，差缩小为 +20。如果决定为每个预测时点使用过去窗口，也不能包含当前之后的记录。

NIST 的 EWMA 控制图介绍了对近期观测和过去信息加权的监控统计量。更新统计量与重新设定控制限是不同的事，不能把它当作持续将异常迹象接受为新常态的依据。更新基准线时，需要记录纳入的期间、排除的状态、更新时间和上一版本。

固定基准线可以用于追踪长期变化，近期平时基准线可以用于确认相对近期状态的偏离。在同一份报告中并排显示两种差值，就可以区分各自的比较目的。

## 用一个小图来看

这一节真正抓住的不是基准线形式本身，而是 `比较问题` 会让哪一种维护方式更自然。固定基准线和最近平时基准线更适合支撑不同的问题，因此比较语句的含义也会跟着改变。

--8<-- "assets/part-03/chapter-07/p3-7-5-mermaid-01-zh.mmd"

## 检查清单

- 你是否分别比较了当前值 110 与固定基准 100、移动基准 108？
- 你能否解释把异常区间纳入基准线为何会缩小差异？

## 来源与参考资料

- U.S. Bureau of Labor Statistics, `Base period`. 它提供了“把某个特定时间点或期间固定为比较参考”的一般原则，因此支持固定基准线所承担的角色。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- National Cancer Institute, `baseline`. 它把 baseline 解释为设定初始测量之后，用来比较随时间变化的参考，因此强化了本节的前提：基准线首先是用于比较的参考测量。 [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. 它说明 control chart 会把当前过程特性与过去表现比较，并且 control limit 只有在有正当且有力的理由时才应改变，因此直接支持本节的说明：基准线要固定还是更新，应根据比较问题和运行变化依据来决定。 [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Hyndman, Athanasopoulos et al., `Forecasting: Principles and Practice (3rd ed)`, `Time series cross-validation`. 它解释了 rolling forecasting origin 这种“参考会随着时间一起向前移动”的结构，因此可以作为一种类比性支持，说明像最近平时基准线这样的“参考区间一起移动”的运行方式是可能的。但因为这份资料属于预测评估语境，所以本节只借用其中 `移动中的参考` 这个更高层概念，而且只以类比方式使用。 [https://otexts.com/fpp3/tscv.html](https://otexts.com/fpp3/tscv.html){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

- [NIST EWMA Control Charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc324.htm){ target="_blank" rel="noopener noreferrer" }。用于确认对过去观测加权的更新基准与固定基准的区别。确认日期：2026-09-15。
