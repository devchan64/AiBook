# P2-13.3 比较并保存多个图

> Section ID: `P2-13.3`
> Version: `v2026.07.08`

P2-13.3 把基础绘图继续推进到“比较”和“留档”。关键不是图变多，而是把相关问题并排摆出来，并把结果保存为可复用材料。

## 本节范围

本节介绍 subplot、比较读取、legend 与 `savefig()`，并把它们放进可复现学习记录的语境里。

## 中心问题

多个图和保存出的图像文件，怎样帮助我们把视觉检查变成可复用记录？

![Subplots comparing loss and accuracy](../../../assets/part-02/chapter-13/subplot-loss-accuracy.png)

![Train and validation loss diverging](../../../assets/part-02/chapter-13/train-validation-loss-diverge.png)

## 记住的视角

- 多个图的价值在于让比较问题更明确。
- 当两组值适合并排看而不适合强行共用一条尺度时，应分到不同 `Axes`。
- `savefig()` 能把图保存成文件，但可复现性仍需要代码与数据上下文。
- 如果实验条件也被记录，保存下来的图才更像真正的学习记录。

## 简短检查

- 能说明为什么一个 `Figure` 里可以放多个 `Axes`。
- 能说明什么时候该分面比较，什么时候该放在同一坐标轴里比较。
- 能说明为什么只有一张图片文件还不算完整可复现记录。

## 来源与参考资料

- Matplotlib, [Creating multiple subplots](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
- Matplotlib, [savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
