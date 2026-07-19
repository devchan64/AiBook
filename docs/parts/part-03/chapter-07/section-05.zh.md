# P3-7.5 基准线应该固定不动，还是应该按“最近的平时”一起更新

> Section ID: `P3-7.5`
> Version: `v2026.07.20`

在选好基准线候选之后，还会留下另一个问题。`这个参考应该固定一段时间，还是应该和“最近的平时区间”一起移动？` 即使都已经选中了同条件下的区间，只要基准线的维护方式不同，比较句子的意义也会跟着变化。

基准线的维护方式，并不是一个要先固定“唯一正确答案”的问题。更自然的选择，会随着我们想看什么样的变化而改变。

| 基准线形式 | 更适合的问题 | 需要注意的地方 |
| --- | --- | --- |
| 固定基准线 | 相对某个特定参考点，我们改变了多少？ | 如果当前运行状态已经变了，它可能会变成过于陈旧的参考 |
| 最近平时基准线 | 在最近流程里，现在这个状态是不是特别不同？ | 如果区间抓得太短，基准线本身会变得不稳定 |

例如，如果我们想把设备校正之后的稳定区间长期保留为代表性参考，那么固定基准线就很自然。相反，如果运行环境是缓慢持续变化的系统，那么把“最近的平时区间”当作基准线，往往会更现实。真正重要的是，不管选哪一种方式，我们都应该能够用一句话说明：`现在到底是在拿当前状态和什么去比。`

如果把这个选择一般化来看，它其实是在处理 `参考要保持不动，还是要一起往前滚动` 的问题。BLS 的 `base period` 展示了“固定一个参考点来做比较”的一般原则，而 FPP3 里的 rolling forecasting origin 则说明：随着时间向前移动，作为参考的过去区间本身也可以一起向前移动。这里并不需要把这些概念原样搬过来，只要保留到这样一个层级就够了：`问题本身会决定参考应如何被维护。`

## 外部依据是怎样和正文主张连接起来的

在附上外部依据时，安全的做法不是只抓住 `baseline` 这个词，而是把它和“参考所承担的角色”连接起来。

| 正文里的核心主张 | 从一般化视角需要什么依据 | 当前可以附上的依据扮演什么角色 |
| --- | --- | --- |
| 基准线应当是用来比较的参考区间 | 解释 baseline 或 base period 是“比较参考点”的说明 | NCI 对 baseline 的定义和 BLS 对 base period 的定义支持这一点 |
| 基准线可以按问题选择固定或随最近区间更新 | 需要说明“参考也可以随着时间移动”的比较结构 | FPP3 的 rolling forecasting origin 提供了一个类似点：参考并不一定永远固定 |

rolling origin 本来属于预测评估语境，所以这里不会把它直接等同起来。在这本书里，它只被当成一种类比性支持：用来说明为什么 `最近平时基准线` 也可能是一种自然选择。

## 这里不会直接断言的事情

下面这些说法，并不会在本节里被直接断言。

- 基准线应该始终不断更新到最近区间
- 样本数标准在任何领域都应该用同一个数字
- 固定基准线永远比最近平时基准线更可靠

如果基准线的维护方式选得不好，那么比较报告和当前比较句子的意义就会一起晃动。即使是同一种变化，只要“拿什么去比”这件事本身变了，那么像 `需要复核`、`注意`、`正常/异常候选` 这样的当前判断权重也会跟着改变。如果把这一节重新读成 `参考维护策略(reference maintenance strategy)` 的问题，而不是“固定基准线”和“最近平时基准线”之间的偏好之争，那么会更清楚：基准线维护不是一场“唯一正确答案”的竞争，而是在为比较问题选择最合适的参考维护方式。

## 用一个小图来看

这一节真正抓住的不是基准线形式本身，而是 `比较问题` 会让哪一种维护方式更自然。固定基准线和最近平时基准线更适合支撑不同的问题，因此比较语句的含义也会跟着改变。

--8<-- "assets/part-03/chapter-07/p3-7-5-mermaid-01-zh.mmd"

## 来源与参考资料

- U.S. Bureau of Labor Statistics, `Base period`. 它提供了“把某个特定时间点或期间固定为比较参考”的一般原则，因此支持固定基准线所承担的角色。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- National Cancer Institute, `baseline`. 它把 baseline 解释为设定初始测量之后，用来比较随时间变化的参考，因此强化了本节的前提：基准线首先是用于比较的参考测量。 [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. 它说明 control chart 会把当前过程特性与过去表现比较，并且 control limit 只有在有正当且有力的理由时才应改变，因此直接支持本节的说明：基准线要固定还是更新，应根据比较问题和运行变化依据来决定。 [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Hyndman, Athanasopoulos et al., `Forecasting: Principles and Practice (3rd ed)`, `Time series cross-validation`. 它解释了 rolling forecasting origin 这种“参考会随着时间一起向前移动”的结构，因此可以作为一种类比性支持，说明像最近平时基准线这样的“参考区间一起移动”的运行方式是可能的。但因为这份资料属于预测评估语境，所以本节只借用其中 `移动中的参考` 这个更高层概念，而且只以类比方式使用。 [https://otexts.com/fpp3/tscv.html](https://otexts.com/fpp3/tscv.html){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
