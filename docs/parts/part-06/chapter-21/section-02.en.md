# P6-21.2 Local Runtime Environments and Memory Placement

> Section ID: `P6-21.2`
> Version: `v2026.09.03`

Running an open-weight model directly does not end with downloading a model file. The user also has to decide which device will hold the model, which numeric representation will be used, how much input will be processed at once, and how limited memory will be divided. The question of this Section is **how to distinguish GPU VRAM, CPU RAM, dtype, quantization, and [CPU offloading](../../../reference/concept-glossary-alpha/c.en.md#cpu-offloading) when running an open-weight model locally or in a directly managed environment**.

The important point is not to mix `it runs` with `it is good`. The fact that a model runs is evidence of execution feasibility. Whether the output fits the purpose is a separate quality evaluation. The larger the model and the smaller the machine, the more carefully these two judgments must be separated.

## Model Execution Places Weights and Intermediate Computation Somewhere

Running a model requires learned weights, intermediate tensors that process the input, and temporary state used to generate the output. A GPU processes this computation quickly, but VRAM is limited. CPU RAM is usually larger, but CPU-side computation is slower than GPU computation, and moving data between CPU and GPU also takes time.

So in local execution, begin with these questions.

| What to check | Meaning | What failure looks like |
| --- | --- | --- |
| Model size | Basic memory occupied by the weights and structure | The model fails while loading or starts too slowly |
| dtype | Which numeric representation the weights use | Memory use and some operation compatibility change |
| context or resolution | How much input is processed at once | Intermediate tensors grow with long input, large images, or large batches |
| execution device | Whether CPU, GPU, or mixed placement is used | Speed, memory, and cost change substantially |
| offload mode | Where unused parts wait | The run may complete but become slow or hit a CPU RAM bottleneck |

This table keeps model choice from becoming only a leaderboard decision. Even with the same model, execution records change when numeric representation, input length, execution device, or offload mode changes.

## dtype, Quantization, and CPU Offloading Are Not the Same Thing

When local execution explanations mention `bfloat16`, `float16`, `INT8`, `4-bit`, and `offload` together, they can all look like words for reducing memory. But each one reduces a different thing and pays a different cost.

| Distinction | What it changes | Main effect | Caution |
| --- | --- | --- | --- |
| dtype choice | Numeric representation used for weights and computation | Can reduce memory by reading the same weights in a smaller representation | Speed or compatibility depends on device and operation support |
| quantization | Converts or stores weights in a lower-bit representation | Can greatly reduce model file size and memory use | Quality, speed, and stability must be checked for each model, runtime, and quantization method |
| CPU offloading | Device placement for parts of the model | Can route around limited GPU VRAM by using CPU RAM | More movement between GPU and CPU can make execution slower |
| reducing input scale | context length, resolution, batch, or steps | Reduces intermediate computation and temporary memory | If reduced too far, the task itself may change |

For example, reading a model with `torch_dtype=torch.bfloat16` chooses a smaller representation for the weights. By contrast, `enable_sequential_cpu_offload()` is an execution-placement choice that moves detailed pipeline modules to the GPU when needed and keeps them on the CPU side when they are not needed. The two can be used together, but one does not replace the other.

## CPU Offloading Saves Memory by Spending Time

CPU offloading is used when it is hard to keep every component in GPU VRAM at the same time. Diffusers and Accelerate explain patterns where inactive layers or model components are kept on the CPU side and moved to the accelerator when needed at execution time. This can reduce GPU memory, but the extra movement and synchronization between devices can increase runtime.

Representative offload modes can be separated as follows.

| Mode | Movement unit | Memory saving | Speed tendency | How to read it |
| --- | --- | --- | --- | --- |
| model CPU offload | large pipeline component | medium | relatively faster | Check first in pipelines that alternate large modules |
| sequential CPU offload | detailed module or leaf module | large | slower | Use when VRAM is very constrained and execution feasibility comes first |
| group offloading | grouped layers | medium to large | middle | Check together with model structure and library support |

Sequential CPU offload can save a large amount of memory, but it can be slow. This method installs stateful hooks on a pipeline. Treat it as a choice that defines the execution path, not as an extra call added to a pipeline whose device placement is already fixed.

## Enable Sequential CPU Offload Once, After Assembling the Pipeline

For a Diffusers pipeline such as those in P7-5.1 through P7-5.11, use this order.

1. Create the pipeline with `from_pretrained(...)`.
2. Attach every additional component that belongs to the pipeline, such as ControlNet or IP-Adapter, and apply any needed VAE or attention memory settings.
3. Only when VRAM is especially constrained, call `enable_sequential_cpu_offload()` **once**. Through `Accelerate`, this keeps module weights on the CPU and loads only the small unit needed for an actual forward pass onto the GPU.
4. Do not first move the whole pipeline to the GPU with `pipe.to("cuda")`. Doing so makes the memory saving from sequential offload minimal. Do not move the complete pipeline to `.to("cuda")` again after the call either.
5. For a learning record, run with either model CPU offload or sequential CPU offload. Choose the former when speed matters more, or the latter when VRAM savings matter more, then compare the conditions. If a pipeline was placed with `device_map`, first clear that placement with `reset_device_map()` before making this choice.

For example, the FLUX runs in P7-5.1 through P7-5.3 and P7-5.5 enable sequential offload after loading the weights and generate one scene at a time. The SDXL comparisons in P7-5.11 attach ControlNet and IP-Adapter first, then enable sequential offload. This lets the offload hooks cover the complete pipeline used for the run. Model support and component compatibility still differ, so a successful call does not prove that every adapter combination works the same way.

`torch.cuda.empty_cache()` seen after row-by-row generation must also be kept distinct. It releases unused cached memory so that other GPU applications can use it; it does not move the active pipeline's weights or tensors to the CPU. Record it as cache cleanup between rows, not as an offload mode or evidence of VRAM reduction.

## Separate the Feasibility Gate from the Quality Gate

A common mistake in local model experiments is to record `an image was produced` or `an answer was produced` as success. In a constrained memory environment, first check whether the feasibility gate passed, then evaluate quality separately.

| Gate | Question | Representative record |
| --- | --- | --- |
| feasibility gate | Does the model finish running with this setting? | model ID, dtype, quantization, offload mode, input scale, peak memory, elapsed time, error |
| quality gate | Does the output satisfy the purpose and criteria? | expected answer seen, style·pose·identity preservation, groundedness, human review result |
| operation gate | Is the burden repeatable? | average latency, throughput, CPU RAM use, storage, retry cost |

This separation also makes the next action clearer. If the run fails with OOM, reduce memory placement or input scale. If output quality is wrong, revisit the prompt, reference input, model choice, or evaluation criteria. If the result is correct but slow, review batching, caching, a faster runtime, or a smaller model.

## Use the failure signal to choose the next change

When one run produces an error or a slow result, changing every setting at once makes it impossible to tell what helped. First choose one observed signal, then choose one axis to change in the next run and record it.

| Observed signal | First axis to change | Keep fixed and check |
| --- | --- | --- |
| GPU OOM during loading or generation | One of input-size reduction, quantization, or offload mode | Model ID, quality criterion, and prior elapsed time |
| The run finishes but is excessively slow | One of offload granularity, a smaller model, or input size | Output quality, device configuration, and the same input |
| The run finishes but output misses the quality criterion | One of model, prompt, reference input, or evaluation criterion | Memory placement and whether execution succeeded |

This prevents `does not run`, `slow`, and `quality miss` from being treated as one failure. In the next trial, record the one changed value together with the conditions that stayed fixed so that the trade-off can be compared.

## Record Format

If a local execution experiment stores only the output, it is hard to reread later. At minimum, keep the following values together.

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

For LLM experiments, `context_length`, `input_tokens`, and `output_tokens` become important. For image generation experiments, `width`, `height`, `steps`, `guidance`, and `seed` become important. In both cases, the principle is the same: keep `execution conditions`, `execution burden`, and `quality notes` separate.

## Connection to Part 7

Part 7 turns the concepts in this Section into actual records in current-model execution practice.

| Part 7 location | Standard to carry forward |
| --- | --- |
| P7-5.1–P7-5.3, P7-5.5, and P7-5.11 image experiments | Read sequential CPU offload as a device for execution feasibility, and record model file, dtype, reference input, resolution, and human-review ledger together |
| P7-6.1 local LLM experiment | Compare quantization, context length, execution time, and answer stability with the same questions |
| P7-7.1 vision model experiment | Separate prompt input structure and execution burden from mask-quality judgment |

So handling an open-weight model directly means more than `running it once on my computer`. It includes checking the model's openness scope, fixing execution conditions, recording memory placement, and leaving quality judgment separately.

## Checklist

- Can you explain dtype, quantization, and CPU offloading as different layers?
- Did you record the fact that the model ran separately from the fact that the output satisfied the quality criteria?
- Did you avoid grouping GPU VRAM shortage, CPU RAM bottleneck, slow execution, and quality failure as the same failure?
- Based on the observed failure signal, did you choose one axis to change in the next trial and record the remaining conditions?
- If you used an offload mode, can you explain which unit moves between CPU and GPU?
- If you used sequential CPU offload, did you attach extra components first, enable it only once, and avoid moving the entire pipeline to `cuda`?
- Did you record `torch.cuda.empty_cache()` separately from CPU offloading?
- When moving into Part 7 experiments, can you keep execution conditions and quality-review fields in the same table?

## Sources and References

- Hugging Face Diffusers, [Reduce memory usage](https://huggingface.co/docs/diffusers/optimization/memory){: target="_blank" rel="noopener noreferrer" }, accessed 2026-08-11.
- Hugging Face Diffusers, [Pipelines overview](https://huggingface.co/docs/diffusers/api/pipelines/overview){: target="_blank" rel="noopener noreferrer" }, accessed 2026-08-11.
- Hugging Face Accelerate, [Working with large models](https://huggingface.co/docs/accelerate/en/package_reference/big_modeling){: target="_blank" rel="noopener noreferrer" }, accessed 2026-08-11.
- PyTorch, [torch.cuda.memory.empty_cache](https://docs.pytorch.org/docs/main/generated/torch.cuda.memory.empty_cache.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-08-11.
