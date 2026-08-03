# P5-15.4 Stable Diffusion 怎样从文本条件恢复图像？

> Section ID: `P5-15.4`
> Version: `v2026.08.03`

前几节区分了生成物、候选分布和文本采样。图像生成也是生成模型的一种案例，但不能把它理解成从左到右接续下一 token。

> prompt 进入后，Stable Diffusion 会经过哪些中间状态和重复过程来生成图像？

本节只抓住最小流程：`文本条件 -> 潜在噪声 -> 重复恢复 -> 图像`，不讲安装或图像制作技巧。

它为日后在 Part 7 中按计算角色理解 seed、sampler、steps、LoRA 等设置作准备。

## 它不是一次画出像素图像

Stable Diffusion 是 latent diffusion 用于 text-to-image 的代表案例。`latent`是比人直接看到的像素图像更压缩的计算空间。模型从这个空间的随机噪声开始，在 prompt 条件下反复减少噪声，最后把恢复后的潜在表征变成图像。

| 阶段 | 最小作用 | 本节要抓住的问题 |
| --- | --- | --- |
| 文本条件 | 把 prompt 变成可计算的条件表征 | 条件要求生成什么？ |
| 初始潜在噪声 | 提供图像尚未显现时的出发状态 | 从哪个出发点开始恢复？ |
| 重复恢复 | 反复预测当前潜在表征中要减少的噪声 | 参考条件时，什么会一点点改变？ |
| 图像恢复 | 把最终潜在表征变成可见图像 | 哪个结果会成为实际产物？ |

因此，prompt 不是像素布局表。它是恢复过程参考的条件；初始噪声和恢复路径也会影响最后图像。

## 按角色区分四个组成部分

实现中还有许多组成部分，但在入门阶段，按角色区分比记住名称更重要。

| 组成部分 | 作用 | 不要混同为 |
| --- | --- | --- |
| text encoder | 把 prompt 变成条件表征 | 完全固定图像的命令 |
| U-Net | 预测当前步骤要减少的噪声 | 一次完成图像的计算 |
| scheduler / sampler | 规定移向下一潜在状态的规则 | 文本的 top-k 或 top-p 词选择器 |
| VAE decoder | 把恢复的潜在表征变成像素 | 图像质量的唯一判断者 |

文本条件通常通过 cross-attention 进入恢复过程。入门时只需知道 U-Net 同时参考带噪潜在状态和 prompt 条件。

cross-attention 的公式和实现细节不在本节范围内。

## 为什么同一 prompt 会得到不同图像

| 值 | 改变什么 |
| --- | --- |
| seed | 初始潜在噪声的出发点 |
| steps | 去噪重复次数 |
| sampler | 移向下一潜在状态的规则 |
| guidance | 参考文本条件的强度 |
| base model | 学到的图像模式基础 |

目的不是找出永远最好的一个值，而是区分结果变化来自 prompt、初始噪声、恢复规则，还是模型本身。

比较图像时，应固定或记录这些值，才能讨论差异来自哪里。

## LoRA 与条件控制属于不同层

LoRA 不重新训练整个 base model，而是加上小的调整权重，可把模型适应到某个对象或风格。ControlNet、IP-Adapter 等条件控制路径则可以把 pose、轮廓、参考图像等非文本信息加入恢复过程。

| 层 | 首先要读的作用 |
| --- | --- |
| base model | 默认能恢复哪些图像模式 |
| LoRA | 怎样调整部分 base model 表征 |
| ControlNet / IP-Adapter | 怎样加入额外结构或参考条件 |

同时改变 LoRA weight 和 ControlNet 条件，会很难说明究竟哪个变化造成了结果差异。

## 检查清单

- 我可以把 Stable Diffusion 解释为潜在噪声的重复恢复，而不是一次画出像素。
- 我可以区分 prompt、初始噪声、重复恢复和图像恢复的作用。
- 我可以区分 text encoder、U-Net、scheduler/sampler、VAE decoder 的最小作用。
- 我不会把文本 token 采样和图像 diffusion 的 sampler 当成同一种算法。
- 我可以记录 seed、steps、sampler、guidance 或 base model 是否改变。
- 我不会把 LoRA 和非文本条件控制当成同一层。

## 出处与参考资料

- Robin Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752){: target="_blank" rel="noopener noreferrer" }, arXiv, 2021，确认日期：2026-08-03。
- Jonathan Ho, Ajay Jain, Pieter Abbeel, [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020，确认日期：2026-08-03。
- CompVis, [Stable Diffusion 官方实现](https://github.com/CompVis/stable-diffusion){: target="_blank" rel="noopener noreferrer" }, GitHub，确认日期：2026-08-03。
