<a id="role-aware-reading-across-heterogeneous-scales"></a>
<a id="glossary-role-aware-reading-across-heterogeneous-scales"></a>

### 跨异质尺度的角色感知阅读(role-aware reading across heterogeneous scales)

- 含义：面对单位和范围不同的数值列时，不直接比较原始数值大小，而是按每一列的角色，以及同一列相对基准线的变化来读取。持续时间、压力、波动性、变化率属于不同测量轴时，数值更大并不自动表示更重要。
- 为什么重要：同一张特征表里的列，也可能有不同单位、范围和变动宽度。这个视角帮助读者避免把大数字误认为更重要的特征，也为理解距离模型这类对尺度敏感的模型为什么会在缩放后改变行为做好准备。
- 相关概念：`特征`，`基准线`，`k-NN`，`预处理`
- 中心 Section：`P3-6.5`
- 出现 Section：`P3-6.5`
