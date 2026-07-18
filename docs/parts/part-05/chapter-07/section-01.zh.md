# P5-7.1 optimizer 的角色

Section ID: `P5-7.1`
Version: `v2026.07.17`

在 P5-6 章里，我们已经区分了学习循环、step/batch/epoch、学习（learning）与模型执行（inference），以及训练模式（training mode）与评估模式（evaluation mode）。走到这里，接下来就会留下一个非常直接的问题：既然已经把模型出错这件事算成了数字，那么模型内部的真实数字到底是在什么地方改变的？

损失也算了，gradient 也求了，那么到底是谁真正去改权重？

承担这个角色的，就是优化器（optimizer）。

优化器是接收反向传播算出的 gradient，并把参数真实更新到更可能减小损失方向上的规则。换句话说，前面的计算会告诉我们`朝这边改，损失可能会下降`，而 optimizer 则把这个结果继续变成`那么这一 step 里就把权重这样改`这样的真实调整。

如果后面又开始把 loss、gradient、update 的角色混在一起，更适合回到[英文概念词汇表里的 optimizer 条目](/AiBook/en/reference/concept-glossary/#optimizer)，重新按角色拆开。

如果把一次学习 step 非常粗略地说出来，模型会先做出预测，再计算这个预测错了多少，再计算这种错误与哪些权重有关，最后才真正改动权重数值。这里最后一个阶段，就是 optimizer 的位置。

读这条流程时，最好先抓住下面三句话。

- 损失会把错误变成数字。
- 反向传播会计算每个权重该往哪个方向改。
- 优化器会把这个信号变成真实更新。

## 本节范围

- optimizer 在学习过程里处在什么位置？
- 损失函数、反向传播、优化器之间分别承担什么角色？
- 为什么只有`算出了 gradient`还不够，还必须另外有`更新规则`？
- 如果不把 optimizer 看成某个实现函数，而看成`真实改动参数的角色`，应该先看什么？

这一节专注于闭合一个问题：`到底是谁真正去改参数？` 也就是说，这里先把`计算错误`、`计算 gradient`、`把 gradient 变成真实 update`这三个阶段分开来读。只有这条区分先清楚，下一节再看 learning rate 或 Adam 时，才不容易把不同层位的问题混成一团。

同时，这一节不会马上扩大的问题也要明确。同样的 gradient 在不同 learning rate 下为什么会出现不同步幅，会在下一节 P5-7.2 继续说明；Adam 这类自适应 optimizer 试图补什么，会在 P5-7.3 再说明；adaptive optimization 的收敛分析则会被单独放到 P5-7.4 补充学习。

## 本节目标

- 能把 optimizer 解释成`把 gradient 变成真实 update 的规则`。
- 能区分损失函数、反向传播、优化器分别结束的是哪一个阶段。
- 能解释为什么`算出了 gradient`和`参数真的变了`不是同一句话。
- 能通过一个很小的 Python 例子确认：gradient、update、参数变化本来就是不同步骤。

## optimizer 在学习过程里的什么位置

如果把 Part 5 前面的学习流程重新绑起来，深度学习训练通常会按下面顺序进行。

1. 用前向传播（forward pass）计算预测。
2. 用损失函数（loss function）把错误变成数字。
3. 用反向传播（backpropagation）计算 gradient。
4. 由优化器（optimizer）更新参数。

也就是说，optimizer 不是负责计算 gradient 的装置，而是`看着已经算出来的 gradient，决定下一个参数该怎么改的装置`。更直接地说，损失函数和反向传播负责计算`怎样改会更好`，而 optimizer 则把这个结果继续变成`这一步到底实际改多少`。

如果把这个流程画得非常简单，就是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-07/optimizer-loop-flow-zh.mmd"
```

只有先抓住这个区分，读训练代码时才不容易把不同问题捏成一步。看损失函数时，先问的是`哪里错了、错了多少`；看反向传播时，先问的是`这个错误会把怎样的方向信号传给各个参数`；看 optimizer 时，先问的是`这个信号有没有真的被变成 update，并应用到了参数上。`

如果把这三段混在一起读，就很容易把`loss 已经算出来了`、`gradient 已经出来了`、`模型已经更新了`读成同一个意思。但真实训练里，它们承担的是三种不同角色。因此更安全的阅读标准，是先把它们分成：`测错误`、`算责任`、`实际移动参数`。

- 损失函数：把哪里错了表达成数字
- 反向传播：算出谁对这个错误负多少责任
- 优化器：决定这次到底实际改多少

这三句话，就是 Part 5 里学习计算流程的最小地图。与其把术语分开死记，不如先按`错误 -> 责任 -> 真实修改`这个顺序绑起来。只要这条顺序固定，之后在代码里看到 `loss`、`backward`、`step` 时，也更容易判断它们各自结束的是哪一段。

## 为什么只有 gradient 还不够

gradient 提供的是方向（direction）信息。它通常告诉我们：`朝哪边走，损失更可能下降。` 只靠这个信号，已经能说明学习不是瞎猜。但在真实 update 里，只知道方向仍然不够。

原因很简单。真正改参数，不只是看到了箭头，而是还要决定：沿着这个箭头走多远、以什么方式走。地图告诉你`往这边下坡`，并不等于你已经自动决定好每一步要迈多大。即便是同一个 gradient，有时你几乎不动，有时能用比较合适的步幅靠近目标，有时也可能一下走得太大，直接越过更好的位置。也就是说，gradient 只是`下坡方向信号`，而真实学习还需要一条规则，把这个方向信号变成`真实移动。`

因此还会留下下面这些问题。

- 一次到底要走多大？
- 要不要参考前一步移动时的方向？
- 不同坐标是不是应该用不同速度？

这些问题都说明：在`知道方向`和`真实更新`之间，还多隔了一层。也就是说，gradient 更像地图，optimizer 更像移动规则。

用一句话压缩就是：

`如果 gradient 是方向标，optimizer 就是在决定：要以多快、用什么方式沿着这个方向真的走出去。`

把它换成更直白的语言，就是下面三句。

- gradient 会告诉你`该朝哪边走`
- optimizer 会决定`这个方向要怎样变成真实 update`，以及`这次到底走多大`
- 所以即使 gradient 相同，只要 optimizer 规则不同，实际学习的样子也可能不同

## 读 optimizer 时，到底要把什么看成 update

初学者最常见的误解之一，就是把`已经算出 gradient`和`模型已经变了`读成同一句话。但真实流程里，中间还隔着一步。

1. 先在当前参数位置上计算 gradient。
2. optimizer 读这个 gradient，做出 update。
3. 把这个 update 反映到参数上。

如果慢慢读这条顺序，就会看到：optimizer 的工作不是`把 gradient 原样传过去`，而是`把 gradient 变成可以真实应用到参数上的移动量。` gradient 还是一个计算结果，它只是在说：哪边更像下降方向。update 则是在这个结果之上，再次变成：`这一 step 到底真实移动多少。` 之后参数反映，则是这个移动量真正加到或减到权重数值上，使模型内部数字发生变化的步骤。

如果把这三件事压成一句话，就是：`方向信号`、`移动量计算`、`真实数字改变`。

也就是说，gradient 仍然只是`方向和强度的信号`，而 update 才是`真正会应用到参数上的移动量。` 即使出现同样的 `-16.0`，也不能把它直接读成`权重就会马上改 -16.0`。它仍然必须经过 optimizer 的规则，被重新解释成这一步里的真实移动量。

如果忽略这条区分，读训练日志或代码时就会把阶段混在一起。`gradient 算得很好`只说明方向信号已经出来了，而`update 已经应用`才说明这个信号真的被变成参数变化。因此，看 optimizer 时不要停在`有没有 gradient`，而要继续看：`这个 gradient 最后变成了什么 update 值，并且这个 update 是否真的被反映了。`

这条区分还会影响我们怎么诊断训练慢或不稳定。因为有时 gradient 本身没问题，但 update 太保守；也有时方向是对的，但 update 过于激烈。像这种步幅问题，会在下一节 P5-7.2 里与 learning rate 一起更直接地说明。

## 案例与示例

### 案例. loss 和 gradient 都算出来了，但 update 还没真的应用

读训练代码时，经常会遇到这样一种时刻：模型已经把错了多少算成了数字，也已经算出这些错误该怎样传给各个权重，但权重数值本身还没有变。代码里最典型的场景，就是 `loss.backward()` 已经结束，但 `optimizer.step()` 还没被调用的时候。人看到这里时，常会觉得学习几乎已经做完了，但实际上，此时只完成了`该怎样改`的计算，还不能说`真的改了`。

用 optimizer 视角重读这个场景，问题会变得更直接。我们不再停在`gradient 有没有算出来`，而是继续问：`这个 gradient 有没有真的被应用成 update？` loss 和 gradient 都是计算结果，而 optimizer step 则是把这些结果继续变成模型内部数字变化的最后一步。这个案例里真正要确认的结果，不是`做过 backward 了`，而是`有没有一直走到 optimizer step，并让参数真实变化。`

如果把这个场景再拆得更直接一点，大致是下面这样。

| 现在已经算出来的东西 | 还没有发生的东西 |
| --- | --- |
| 已经有预测值了 | 权重数值真的改变了 |
| 已经算出损失了 | 下一 step 的起始参数已经确定了 |
| 已经算出 gradient 了 | update 已经真实反映到参数上 |

也就是说，`有了 loss 和 gradient`只说明学习已经算出该往哪里走；`optimizer.step()` 结束了，才说明这个结果真的变成了模型内部数字变化。本节的中心边界，就在这里。

| 人最容易先看的标准 | 重新用 optimizer 视角读出来的标准 |
| --- | --- |
| gradient 已经出来了，所以学习应该已经结束了 | gradient 计算和 update 应用是两个不同阶段 |
| loss 打印出来了，所以模型应该已经变好了 | loss 只是状态数字，真实参数变化要由 optimizer 去完成 |
| 只看 backward 就够了 | 参数若要改变，optimizer step 必须真的执行 |

如果把这个案例再压缩一次，最先该读的 optimizer 流程就是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-07/optimizer-step-bridge-zh.mmd"
```

这张图不是为了重新讲一遍案例，而是为了把`gradient 已经算出来`和`真实 update 已经应用`这两件事再一次一口气分开抓住。至于同一个 gradient 在不同 learning rate 下为什么会变成不同步幅，会在下一节 P5-7.2 继续；Adam 一类方法为什么还会去看最近流向与按坐标调节，则会在 P5-7.3 继续。

## 练习与例子

这一节例子的目标，是把 gradient 计算与真实 update 应用分开来看。这里最重要的，不是马上比较 learning rate 的好坏，而是确认：`先算出 gradient，optimizer 再做出 update，之后参数才会改变。` 也就是说，这个例子不是在教你`哪一个 learning rate 更好`，而是在让你看清：代码与输出里，`gradient`、`update`、`参数变化`分别出现在不同位置。

输入：

- 当前风险权重 `risk_weight`
- 压力未恢复程度 `pressure_unrecovered`
- 目标阻断分数 `target_block_score`
- 固定学习率 `learning_rate`

输出：

- 预测得到的阻断分数
- 损失
- gradient
- optimizer 做出来的 update 值
- update 前后的风险权重与损失

问题场景：

- 仅仅算出 gradient，并不等于参数会自动改变
- 只有 optimizer 做出的 update 被真正应用时，模型内部数字才会变

需要确认的概念：

- gradient 是方向信号
- optimizer 会把这个信号变成 update 值
- 参数变化要等到 update 应用以后才会出现

在看代码之前，先把这个例子分成`更新前状态`和`更新后状态`来读，会更容易。

| 区间 | 这里要确认什么 |
| --- | --- |
| 更新前状态 | 当前预测与损失到底错得有多大 |
| gradient 计算 | 该朝哪个方向改 |
| optimizer update | 这一次到底实际移动多少 |
| 更新后状态 | 权重、预测值、损失真实发生了什么变化 |

```python
pressure_unrecovered = 2.0
target_block_score = 6.0
risk_weight_before = 1.0
learning_rate = 0.1

predicted_block_score_before = pressure_unrecovered * risk_weight_before
loss_before = (predicted_block_score_before - target_block_score) ** 2
gradient_risk_weight = 2 * (predicted_block_score_before - target_block_score) * pressure_unrecovered

optimizer_delta = -learning_rate * gradient_risk_weight
risk_weight_after = risk_weight_before + optimizer_delta
predicted_block_score_after = pressure_unrecovered * risk_weight_after
loss_after = (predicted_block_score_after - target_block_score) ** 2

print("[before update]")
print("predicted_block_score_before =", round(predicted_block_score_before, 3))
print("loss_before =", round(loss_before, 3))

print("[gradient and update]")
print("gradient_risk_weight =", round(gradient_risk_weight, 3))
print("optimizer_delta =", round(optimizer_delta, 3))

print("[after update]")
print("risk_weight_after =", round(risk_weight_after, 3))
print("predicted_block_score_after =", round(predicted_block_score_after, 3))
print("loss_after =", round(loss_after, 3))
```

```text
[before update]
predicted_block_score_before = 2.0
loss_before = 16.0

[gradient and update]
gradient_risk_weight = -16.0
optimizer_delta = 1.6

[after update]
risk_weight_after = 2.6
predicted_block_score_after = 5.2
loss_after = 0.64
```

这段输出最好按顺序来读。先看 `[before update]` 里的 `predicted_block_score_before` 与 `loss_before`，就能知道模型在 update 之前到底错得多厉害。接着看 `[gradient and update]` 里的 `gradient_risk_weight`，就会知道此时已经算出了一个方向信号：权重该往哪边改。但走到这里，还只是`知道该怎么改`，并不是参数已经真的变了。

接下来第一次出现 `optimizer_delta`。这个值，就是 optimizer 做出来的真实移动量。换句话说，如果 `gradient_risk_weight` 是方向信号，那么 `optimizer_delta` 就是在这一 step 里，权重真实要移动多少的数字表达。最后再看 `[after update]` 里的 `risk_weight_after`、`predicted_block_score_after`、`loss_after`，才会确认：这个移动量真的被应用之后，模型内部数字和损失到底怎样变了。

因此，这个输出里真正重要的阅读习惯，是把 `loss_before`、`gradient_risk_weight`、`optimizer_delta`、`risk_weight_after` 连成一条线去读。它们对应的顺序正是：`计算错误 -> 计算方向信号 -> 生成真实移动量 -> 反映到参数上。`

![update 应用前后的风险权重](/AiBook/assets/part-05/chapter-07/optimizer-step-before-after-weight-zh.png)

这张图展示的是：原本 `risk_weight_before = 1.0`，在 optimizer 做出的移动量被应用之后，真实变成了 `risk_weight_after = 2.6`。这里重要的，不只是`算出 gradient 了`，而是这个结果最终变成了权重数字变化。

![update 应用前后的阻断分数](/AiBook/assets/part-05/chapter-07/optimizer-step-before-after-score-zh.png)

这张图则说明：同一个 update 也会马上影响预测值。update 前的阻断分数是 `2.0`，但 update 之后变成 `5.2`，更接近目标值 `6.0`。也就是说，optimizer 不只是改内部权重，它还改变了下一次预测的出发点。

![update 应用前后的损失](/AiBook/assets/part-05/chapter-07/optimizer-step-before-after-loss-zh.png)

最后一张图确认：损失也从 `16.0` 降到了 `0.64`。把这条顺序用眼睛再读一遍，会更清楚地看到：在`gradient 计算`和`loss 降低`之间，确实存在`optimizer 做出真实 update 并应用`这个中间步骤。

所以这个例子里读者最该带走的是下面这些点。

- `gradient_risk_weight` 还不是参数本身
- `optimizer_delta` 是 optimizer 把 gradient 变成的真实移动量
- 参数变化要到 `risk_weight_after` 才真正看得见
- 因此，`算出了 gradient`和`模型已经更新了`并不是同一句话

这里真正要固定住的核心，就是：`gradient 出来了`与`模型真的变了`之间，确实隔着 optimizer 做出的中间步骤。至于同一个 gradient 在不同步幅下为什么会得到不同结果，会在下一节 P5-7.2 继续说明。

## 什么时候要先用 optimizer 视角来读

当一段说明只说`已经算出了 gradient`，但还无法闭合`参数到底怎么真实移动`时，就要先把这一节拿出来。

| 先出现的问题场景 | 为什么 optimizer 视角会先有用 | 紧接着要看的问题 |
| --- | --- | --- |
| gradient 能看懂了，但真实移动规则和幅度还看不见 | 它会迫使我们把 update 当成单独规则来读 | 接下来要看同一个 gradient 在不同 learning rate 下如何改变步幅 |
| loss、反向传播、更新糊成一团 | 可以把`错误 -> gradient -> 真实修改`的角色差异重新拆开 | update 的步幅与自适应修正要到后面几节继续看 |
| 直觉上不明白为什么同样的 gradient 也可能得到不同结果 | 可以先固定：optimizer 会改变学习动力学本身 | 后面还要去看 P5-7.2、P5-7.3 的步幅与自适应 update |

## 检查清单

- 能说明 optimizer 不是`计算 gradient 的阶段`，而是`把已经算出的 gradient 变成真实参数更新的阶段`吗？
- 能把损失函数、反向传播、优化器分别说成`错误计算`、`方向信号计算`、`真实修改应用`吗？
- 能区分为什么`算出了 gradient`和`参数真的改变了`是两句不同的话吗？
- 能说明：只有 optimizer 做出的 update 真正被应用之后，参数和损失的变化才会出现吗？
- 能知道：下一节 P5-7.2 会继续说明 learning rate 怎样改变 update 步幅，P5-7.3 会继续说明 Adam 类方法还补了什么吗？

## 出处与参考资料

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Léon Bottou, `Large-Scale Machine Learning with Stochastic Gradient Descent`, COMPSTAT, 2010, 确认日期: 2026-06-29.
- Sebastian Ruder, `An overview of gradient descent optimization algorithms`, arXiv, 2016, 确认日期: 2026-06-29.
