# P6-21.2 本地执行环境与内存放置

> Section ID: `P6-21.2`
> Version: `v2026.08.29`

直接运行开放权重模型，并不只是把模型文件下载下来。使用者还必须决定模型要放在哪个设备上、用哪种数值表示来读取、一次处理多长的输入，以及在内存不足时怎样分配各部分。这一节的问题是：**在本地或直接管理的环境中运行开放权重模型时，怎样区分 GPU VRAM、CPU RAM、dtype、量化，以及 [CPU offloading](../../../reference/concept-glossary-pinyin/c.zh.md#cpu-offloading)**。

这里最重要的是不要把`跑起来了`和`效果好`混在一起。模型能够执行完，只能说明执行可行。输出是否符合目的，是另一层质量评价。模型越大、机器越小，就越需要把这两个判断分开。

## 模型执行就是为权重和中间计算安排位置

运行模型需要学好的权重、处理输入的中间 tensor，以及生成输出时用到的临时状态。GPU 能快速处理这类计算，但 VRAM 有限制。CPU RAM 通常更大，但 CPU 端计算比 GPU 慢，CPU 和 GPU 之间搬运数据也需要时间。

所以在本地执行时，先看下面这些问题。

| 要检查的内容 | 含义 | 失败时会看到什么 |
| --- | --- | --- |
| 模型大小 | 权重和结构占用的基本内存 | 在加载阶段失败，或启动非常慢 |
| dtype | 权重用哪种数值表示来读取 | 内存使用量和部分运算兼容性会改变 |
| context 或分辨率 | 一次处理多大的输入 | 长输入、大图像、大 batch 会让中间 tensor 变大 |
| 执行设备 | 使用 CPU、GPU，还是混合放置 | 速度、内存、成本都会明显改变 |
| offload 方式 | 暂时不用的部分放在哪里等待 | 可能能跑完，但变慢，或遇到 CPU RAM 瓶颈 |

这张表能避免只用排行榜来选择模型。即使是同一个模型，只要数值表示、输入长度、执行设备、offload 方式不同，执行记录也会不同。

## dtype、量化、CPU offloading 不是同一件事

本地执行说明中同时出现 `bfloat16`、`float16`、`INT8`、`4-bit`、`offload` 时，它们看起来都像是减少内存的说法。但每一项减少的对象和付出的代价都不同。

| 区分 | 改变什么 | 主要效果 | 注意点 |
| --- | --- | --- | --- |
| dtype 选择 | 权重和计算使用的数值表示 | 可以用更小的表示读取同一组权重，从而减少内存 | 速度和兼容性取决于设备和运算支持 |
| 量化 | 把权重转换或保存为更低 bit 的表示 | 可以明显减小模型文件和内存使用量 | 质量、速度、稳定性要按模型、runtime、量化方式分别检查 |
| CPU offloading | 模型部分组件所在的设备位置 | 可以用 CPU RAM 绕开 GPU VRAM 不足 | GPU 和 CPU 之间移动变多，执行可能变慢 |
| 缩小输入规模 | context 长度、分辨率、batch、step | 减少中间计算量和临时内存 | 缩得过多时，任务本身可能已经改变 |

例如，用 `torch_dtype=torch.bfloat16` 读取模型，是选择用更小的表示来读取权重。相反，`enable_sequential_cpu_offload()` 是一种执行放置选择：需要时把 pipeline 的细分 module 移到 GPU，不需要时放在 CPU 侧。两者可以一起使用，但不能互相替代。

## CPU offloading 用时间换内存

当很难把所有组件同时留在 GPU VRAM 中时，就会使用 CPU offloading。Diffusers 和 Accelerate 文档说明了这样的方式：把 inactive layer 或 model component 放在 CPU 侧，在执行时按需要移动到 accelerator。这样可以减少 GPU 内存，但设备之间的移动和同步会增加，运行时间也可能变长。

代表性的 offload 方式可以这样区分。

| 方式 | 移动单位 | 内存节省 | 速度倾向 | 阅读标准 |
| --- | --- | --- | --- | --- |
| model CPU offload | pipeline 的大组件单位 | 中等 | 相对较快 | 在交替使用大 module 的 pipeline 中先检查 |
| sequential CPU offload | 细分 module 或 leaf module 单位 | 大 | 较慢 | VRAM 非常紧张、先确保能执行时使用 |
| group offloading | 分组后的 layer | 中等到较大 | 中间 | 要和模型结构、库支持状态一起确认 |

sequential CPU offload 能节省较多内存，但可能较慢。它会在 pipeline 上安装带状态的 hook。因此，它不是在设备放置已固定的 pipeline 上追加的辅助调用，而是决定执行路径的一种选择。

## 在组装完成的 pipeline 上只设置一次顺序 CPU offload

对于 P7-5.1~P7-5.3 和 P7-5.11 那样的 Diffusers pipeline，按下面的顺序操作。

1. 用 `from_pretrained(...)` 创建 pipeline。
2. 连接 ControlNet、IP-Adapter 等属于该 pipeline 的全部附加组件，并设置所需的 VAE 或 attention 内存选项。
3. 只有在 VRAM 特别紧张时，才**一次**调用 `enable_sequential_cpu_offload()`。该调用借助 `Accelerate` 将 module 权重留在 CPU，只在实际 forward 时把所需的小单元放到 GPU。
4. 不要先用 `pipe.to("cuda")` 把整个 pipeline 放到 GPU。这样会让顺序 offload 的内存节省效果变得很小。调用之后也不要再用 `.to("cuda")` 移动整个 pipeline。
5. 在学习记录中，model CPU offload 和 sequential CPU offload 选择其中一种执行。优先速度时选择前者，优先节省 VRAM 时选择后者，再比较执行条件。若 pipeline 已通过 `device_map` 放置，先用 `reset_device_map()` 清除该放置，再作此选择。

例如，P7-5.1~P7-5.3 的 FLUX 运行会在加载权重后开启顺序 offload，并一次生成一个场景。P7-5.11 的 SDXL 比较会先连接 ControlNet 和 IP-Adapter，再开启顺序 offload。这样 offload hook 才能覆盖实际运行的完整 pipeline。不过，各模型支持的组件和兼容性不同；一次调用成功，并不说明所有 adapter 组合都会以相同方式工作。

逐行生成后出现的 `torch.cuda.empty_cache()` 也要分开理解。它只释放未使用的 PyTorch 缓存内存，让其他 GPU 应用可以使用；不会把正在使用的 pipeline 权重或 tensor 移到 CPU。因此应把它记录为行之间的缓存清理，而不是 offload 方式或 VRAM 节省的证据。

## 分开执行可行性 gate 与质量 gate

本地模型实验中常见的混淆，是把`图像生成出来了`、`回答生成出来了`直接记录为成功。在受限内存环境中，应先确认执行可行性 gate 是否通过，再单独评价质量。

| gate | 要问的问题 | 代表记录 |
| --- | --- | --- |
| 执行可行性 gate | 这个设置能不能让模型跑完？ | model ID、dtype、量化、offload 方式、输入规模、peak memory、elapsed time、错误 |
| 质量 gate | 输出是否满足目的和标准？ | 是否包含期望答案、风格·pose·identity 保持、证据充分性、人工检查结果 |
| 运营 gate | 这种负担能否重复执行？ | 平均延迟、吞吐量、CPU RAM 使用量、存储空间、重试成本 |

这个区分能让下一步行动更准确。如果是 OOM，就要调整内存放置或缩小输入规模。如果输出质量不对，就要重新看 prompt、参考输入、模型选择或评价标准。如果结果正确但太慢，则要检查 batch、cache、更快的 runtime 或更小的模型。

## 用失败信号决定下一项选择

一次执行出现错误或结果很慢时，如果同时改动所有设置，就无法知道哪一项产生了效果。先选定一个观察到的信号，再为下一次执行选定一个要改动的轴，并把它记录下来。

| 观察到的信号 | 优先改动的轴 | 保持不变并确认的内容 |
| --- | --- | --- |
| 加载或生成时 GPU OOM | 输入规模缩小、量化、offload 方式三者之一 | 模型 ID、质量标准、上一次执行时间 |
| 执行结束但速度过慢 | offload 单位、更小的模型、输入规模三者之一 | 输出质量、设备配置、相同输入 |
| 可以执行但输出未达到质量标准 | 模型、prompt、参考输入、评价标准四者之一 | 内存放置和执行是否成功 |

这样就不会把“无法执行”“很慢”“质量不达标”混成同一种失败。下一次 trial 应同时留下一个改动值和保持不变的条件，才能比较执行环境中的取舍。

## 记录格式

本地执行实验如果只保存输出，之后就很难重新阅读。至少要把下面这些值一起留下。

```text
run_id:
model_id:
model_revision:
weight_format:
dtype:
quantization:
runtime:
device:
offload_mode:
offload_api:
pipeline_moved_to_cuda:
device_map:
attached_components:
input_size:
context_length:
width:
height:
batch_size:
steps:
peak_vram:
peak_ram:
elapsed_seconds:
status:
quality_note:
next_trial:
```

如果是 LLM 实验，`context_length`、`input_tokens`、`output_tokens` 会变得重要。如果是图像生成实验，`width`、`height`、`steps`、`guidance`、`seed` 会变得重要。但无论是哪种情况，原则都一样：把`执行条件`、`执行负担`、`质量记录`分开留下。

## 与 Part 7 的连接

Part 7 的当前模型执行实习，会把这一节的概念变成实际记录。

| Part 7 位置 | 要带过去的标准 |
| --- | --- |
| P7-5.1~P7-5.3 与 P7-5.11 图像实验 | 把 sequential CPU offload 读成确保执行可行性的装置，并一起记录模型文件、dtype、参考输入、分辨率、人工检查 ledger |
| P7-6.1 本地 LLM 实验 | 用同一组问题比较量化、context 长度、执行时间和回答稳定性 |
| P7-7.1 视觉模型实验 | 把 prompt 输入结构和执行负担，与 mask 质量判断分开 |

因此，直接处理开放权重模型，不只是`在我的电脑上跑一次`。它还包括确认模型公开范围、固定执行条件、记录内存放置，并把质量判断单独留下。

## 检查清单

- 能否把 dtype、量化、CPU offloading 解释成不同层次？
- 是否把模型跑起来的事实，与输出满足质量标准的事实分开记录？
- 是否没有把 GPU VRAM 不足、CPU RAM 瓶颈、执行缓慢、质量失败混成同一种失败？
- 是否根据观察到的失败信号，为下一次 trial 选定一个要改动的轴，并记录其余条件？
- 如果用了 offload 方式，能否说明 CPU 和 GPU 之间移动的单位是什么？
- 如果使用了 sequential CPU offload，是否先连接附加组件、只设置一次，并避免把整个 pipeline 移到 `cuda`？
- 是否把 `torch.cuda.empty_cache()` 与 CPU offloading 分开记录？
- 进入 Part 7 实验时，能否把执行条件和质量检查项目留在同一张表中？

## 来源与参考资料

- Hugging Face Diffusers, [Reduce memory usage](https://huggingface.co/docs/diffusers/optimization/memory){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-08-11。
- Hugging Face Diffusers, [Pipelines overview](https://huggingface.co/docs/diffusers/api/pipelines/overview){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-08-11。
- Hugging Face Accelerate, [Working with large models](https://huggingface.co/docs/accelerate/en/package_reference/big_modeling){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-08-11。
- PyTorch, [torch.cuda.memory.empty_cache](https://docs.pytorch.org/docs/main/generated/torch.cuda.memory.empty_cache.html){: target="_blank" rel="noopener noreferrer" }, 确认日期：2026-08-11。
