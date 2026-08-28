# P5-15.6 VAE 怎样把图像变成 latent 表示？

> Section ID: `P5-15.6`
> Version: `v2026.08.28`

P5-15.4 把扩散解释为反复复原含噪状态的算法，P5-15.5 则把 U-Net 和 DiT 解释为预测复原方向的网络选择。latent diffusion 不直接在像素中反复计算，而是在 latent 表示中计算。连接图像和 latent 表示的装置是 VAE（variational autoencoder）系列。

本节的问题是：**VAE 与一般 autoencoder 有何不同，为什么它能形成可用于生成的 latent 空间，以及它在 latent diffusion 中负责哪一步计算？**

## autoencoder 学习可重新构成的表示

一般 autoencoder 通过 encoder 把输入图像 `x` 变成通常更紧凑的表示 `z`，再让 decoder 从 `z` 复原相似图像 `x_hat`。核心学习信号是输入和复原结果的差异。latent 表示不一定总是维度更少；这里先把它看作适合重复生成计算的表示空间。

| 组件 | 做什么 | 首先要看的问题 |
| --- | --- | --- |
| encoder | 把图像 `x` 变为 latent `z` | 哪些信息留在更小的表示中？ |
| latent 表示 | encoder 留下的中间坐标 | 相似输入可能怎样排列？ |
| decoder | 从 `z` 复原 `x_hat` | 保留的信息能复原多少原始场景？ |
| 重构损失 | 衡量 `x` 与 `x_hat` 的差异 | 学习是否保住了重要输入信息？ |

这足以学习可复原的表示。但如果 encoder 产生的 latent 坐标散乱且空隙很多，随意挑一个坐标交给 decoder 时可能无法得到自然图像。**能很好复原**和**能从新坐标生成**不是同一个要求。

## VAE 产生分布，而不是固定坐标

VAE encoder 不直接为每张图像返回一个 latent 坐标，而是预测与该图像对应的分布均值 `mu` 和扩散程度 `sigma`。从这个分布采样的 `z` 会交给 decoder。

```mermaid
--8<-- "assets/part-05/chapter-15/vae-latent-diffusion-flow-zh.mmd"
```

| VAE 值 | 含义 | 常见混淆 |
| --- | --- | --- |
| `mu` | 此输入对应 latent 分布的中心 | 不是完成图像 |
| `sigma` | 中心周围的扩散程度 | 不是质量分数或预测噪声 |
| `z` | 用 `mu`、`sigma` 和随机性做出的 latent 样本 | 不等同于扩散时间步的噪声状态 |
| `x_hat` | decoder 从 `z` 复原的图像 | 不总等同于扩散模型最终生成结果 |

训练时通常用从标准正态分布抽取的随机 `epsilon` 来构造 `z`。

\[
z = \mu + \sigma \odot \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I)
\]

这体现了再参数化（reparameterization）：采样仍有随机性，但损失仍能影响产生 `mu` 和 `sigma` 的 encoder。这里的 `epsilon` 用来做 VAE latent 样本，不是 P5-15.4 中在时间步加入图像状态的扩散噪声。

## 重构损失和 KL 损失保护不同要求

VAE 的训练目标大致可读成重构损失加上 KL divergence 项。

\[
L = L_{reconstruction} + D_{KL}\bigl(q(z\mid x)\;||\;\mathcal{N}(0, I)\bigr)
\]

关键是区分每一项防止的失败。

| 损失项 | 要减少的问题 | 失衡时的风险 |
| --- | --- | --- |
| 重构损失 | decoder 丢失重要内容或结构 | 太弱会模糊；过度强调会让坐标不规则地散开 |
| KL divergence | 每个输入的分布离共同正态参照太远 | 压力太强会减少复原所需的信息 |

KL 项不会把所有图像挤到一个点。它把输入特定分布与生成时可采样的参照分布连接起来。因此 VAE 不只是压缩工具，也试图形成邻近坐标仍可使用的 latent 空间。

## 在 latent diffusion 中，VAE 与扩散是不同阶段

latent diffusion 在 VAE 产生的 latent 表示中进行噪声预测和重复复原。VAE 负责往返于图像和表示；扩散去噪器在 latent 状态中预测噪声方向。

| 阶段 | 主要模型 | 输入到输出 | 回答的问题 |
| --- | --- | --- | --- |
| latent 编码 | VAE encoder | 图像 `x` -> latent `z` | 怎样把图像移到可计算的表示？ |
| latent 生成 | 扩散去噪器和 scheduler | noisy latent -> restored latent | 当前步应去掉什么，下一步怎样移动？ |
| 图像解码 | VAE decoder | 最终 latent -> 图像 | 怎样把 latent 结果变成可见图像？ |

VAE 既不是扩散 scheduler，也不是 U-Net 或 DiT 去噪器，而且并非每个扩散模型都使用 VAE。也可以直接在像素空间做扩散；latent diffusion 只是改变重复计算所在空间的一种设计。

## 用小比较检查边界

| 说明 | 组件 | 原因 |
| --- | --- | --- |
| `把图像变成 latent 表示` | VAE encoder | 重复扩散前的表示转换 |
| `从当前 noisy latent 预测噪声` | U-Net 或 DiT | 扩散的复原方向预测 |
| `利用预测计算下一个 latent 状态` | scheduler | 生成路径规则，不是学得的权重 |
| `把最终 latent 变成像素` | VAE decoder | 把结果变成可见图像 |

能区分这四句话，就能避免把不同计算混为 `VAE 生成图像` 或 `扩散训练 VAE` 这样的说法。

## 检查清单

- 我能说明 autoencoder 如何用 encoder、latent 表示、decoder 和重构损失学习复原。
- 我能说明 VAE encoder 为什么用 `mu` 和 `sigma` 构成 latent 分布。
- 我能区分重构损失和 KL divergence 的作用。
- 我不会把 VAE 采样的 `epsilon` 与时间步扩散噪声混为同一角色。
- 我能区分 latent diffusion 中的 VAE encoder、扩散去噪器与 scheduler、VAE decoder。

## 来源与参考资料

- Diederik P. Kingma, Max Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114){: target="_blank" rel="noopener noreferrer" }, ICLR, 2014，确认日期：2026-08-28。
- Robin Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752){: target="_blank" rel="noopener noreferrer" }, CVPR, 2022，确认日期：2026-08-28。
