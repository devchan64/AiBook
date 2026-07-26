<a id="maximum-likelihood-estimation-mle"></a>

### 最大似然估计(maximum likelihood estimation, MLE)

- 含义：maximum likelihood estimation 是选择一组参数，让观察到的数据在当前 model 下尽可能显得合理的估计方式。在 logistic regression 中，可以先读成选择能给正确 class 更高 probability 的参数。
- 为什么重要：它让 classification training 不只看 `猜对了多少个 label`，还会看 `给正确答案分配了多高的 probability`。理解 MLE 后，也能把最大化 log-likelihood 和最小化 log loss 读成同一个学习目标的两个方向。
- 相关概念：`logistic regression`, `log loss`, `likelihood`
- 中心 Section：`P4-11.3`
- 出现 Section：`P4-11.4`
