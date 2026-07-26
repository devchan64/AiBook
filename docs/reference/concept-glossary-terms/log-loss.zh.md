<a id="log-loss"></a>

### log loss

- 含义：log loss 是一种损失。model 给正确答案的 probability 越低，它就越大；如果错误预测还很自信，惩罚会更强。
- 为什么重要：log loss 常出现在 classification model、logistic regression 和 neural network 输出解释中。它能说明为什么训练会推动 model 提高正确 class 的 probability，也能说明为什么自信地犯错会付出更大的代价。
- 相关概念：`logarithm`, `loss function`, `logistic regression`, `maximum likelihood estimation`
- 中心 Section：`P2-2.4`
- 出现 Section：`P4-11.3`
