# P5-15.5 注意力和 Transformer 在扩散模型中负责什么？

> Section ID: `P5-15.5`
> Version: `v2026.08.28`

P5-15.4 已经说明算法：构造含噪状态，训练模型预测噪声，并在生成时反复把噪声移向数据。算法本身并不规定哪个网络负责预测，也不规定文本条件怎样进入网络。

本节的问题是：**扩散模型怎样连接条件、当前噪声状态和去噪网络，注意力与 Transformer 又处在什么位置？**

## 条件不是去噪器

文本提示、参考图像或结构引导会先变成可计算的表示。去噪网络再同时接收条件、当前含噪图像或潜在状态，以及时间步。

```mermaid
--8<-- "assets/part-05/chapter-15/diffusion-conditioning-structure-zh.mmd"
```

| 组件 | 主要作用 | 不要混同为 |
| --- | --- | --- |
| 条件编码器 | 把文本或参考条件变成可使用的表示 | 直接排布像素的装置 |
| 含噪状态 | 当前要复原的图像或潜在状态 | 条件本身 |
| 去噪网络 | 根据状态、时间和条件预测噪声或复原方向 | scheduler |
| scheduler | 根据预测计算下一状态 | 学得的模型权重 |

同一个去噪网络会在多个时间步反复使用。条件可以指导每次预测，但条件编码器不能替代反复复原算法。

## self-attention 和 cross-attention 回答不同问题

注意力常被当成一个笼统功能。在条件扩散模型中，至少要分开两个问题。

| 机制 | 连接什么 | 有用的问题 |
| --- | --- | --- |
| self-attention | 当前图像/潜在表示内部的位置或 patch | 哪些远距离图像区域需要一起考虑？ |
| cross-attention | 当前图像/潜在表示与文本等条件表示 | 哪些条件词或参考特征应影响这个区域？ |

例如，self-attention 能关联远处相互对应的图像区域；cross-attention 能把 `red umbrella` 这样的文本条件连到有关图像区域。两者都是结构选择，不能把基本扩散循环变成逐 token 的文本生成。

## U-Net 和 DiT 是可替换的去噪器

扩散算法不要求固定的去噪器结构。U-Net 是结合多个空间尺度的常用网络。Diffusion Transformer（DiT）可以把潜在表示切成 patch，用 Transformer block 处理它们的关系。

```mermaid
--8<-- "assets/part-05/chapter-15/diffusion-denoiser-comparison-zh.mmd"
```

| 比较点 | 基于 U-Net 的去噪器 | 基于 DiT 的去噪器 |
| --- | --- | --- |
| 内部处理单位 | 多种空间尺度的 feature map | 由 Transformer block 处理的 latent patch |
| 注意力的使用 | 可在部分分辨率加入注意力 | 把 Transformer 注意力作为核心处理结构 |
| 共同输入 | 含噪状态、时间步、可选条件 | 含噪 latent patch、时间步、可选条件 |
| 共同输出 | 预测噪声或复原方向 | 预测噪声或复原方向 |

这不是排名比较。二者都在扩散循环中的同一位置：读取当前状态、时间和条件，做出供 scheduler 使用的预测。

## 连接到 latent diffusion

扩散可以在像素空间运行，也可以在更小的 latent 空间运行。latent diffusion 会加入 VAE 系列的 encoder 和 decoder 来往返于图像与 latent 表示，但它们不替代预测噪声的去噪网络或 scheduler。

P5-15.6 会说明 VAE 与一般 autoencoder 的区别，以及为什么用于生成的 latent 空间需要有可用的分布。本节只保留条件、U-Net 或 DiT、attention 作为**从当前状态预测噪声的结构**这一重点。

## 检查清单

- 我能说明条件编码器、含噪状态、去噪网络、scheduler 和生成结果的连接。
- 我能区分 self-attention 和 cross-attention。
- 我能把 U-Net 和 DiT 说明为不同的去噪器选择。
- 我能说明 VAE 系列 encoder 和 decoder 是 latent diffusion 的可选组件，而不是去噪器。
- 我能区分 scheduler 与学得的去噪网络。

## 来源与参考资料

- Robin Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022，确认日期：2026-08-28。
- William Peebles, Saining Xie, [Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748){: target="_blank" rel="noopener noreferrer" }, arXiv, 2023，确认日期：2026-08-28。
