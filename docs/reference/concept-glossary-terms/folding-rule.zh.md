<a id="folding-rule"></a>
<a id="glossary-folding-rule"></a>

### 折叠规则(folding rule)

- 含义：折叠规则是把多行、多个事件或多个值缩减成一个代表结果列时使用的明确规则。例如，它决定多个后续事件应该按 `any`、`first`、`worst` 还是 `count` 保留下来。
- 为什么重要：即使源事件和后续事件相同，只要折叠规则不同，结果列的含义也会不同。这个概念帮助读者看到，结果列不只是数据里自然出现的值，而是应用代表规则和阈值之后形成的解释结构。写清折叠规则，也能降低把报告用结果和目标标签候选混在一起的风险。
- 相关概念：`源事件(source event)`, `样本(sample)`, `标签(label)`, `目标标签候选(target candidate)`, `阈值(threshold)`
- 中心 Section：`P3-5.7`
- 出现 Section：`P3-5.7`
