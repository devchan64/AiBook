<a id="vit-vision-transformer"></a>

## ViT, Vision Transformer

- 含义: Vision Transformer 是把图像切成小 patch token，再用 self-attention 读取 patch 之间关系的视觉模型系列。
- 为什么重要: CNN 通常从相邻像素的局部模式开始逐步扩大感受范围，而 ViT 从一开始就把图像当作 patch 序列来处理。理解 ViT，能帮助读者看清 Transformer 如何从语言扩展到图像，以及图像任务中“token”可以由什么承担。
- 相关概念: `CNN`, `self-attention`, `patch`
- 核心 Section: `P5-11.3`
- 出现 Section: `P5-11.1`, `P5-11.2`, `P6-19.2`
