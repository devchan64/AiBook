# P6-9.4 Supplement: The Adjustment Delta That LoRA's Low Rank Represents Compactly

> Section ID: `P6-9.4`
> Version: `v2026.07.23`

In P6-8.2, we saw LoRA as `a method that reduces the burden of full fine-tuning by adding a small adjustment delta on top of a large base model`. That explanation is enough to get the broad cost intuition, but real documents soon bring in names such as `Low-Rank Adaptation`, `rank`, `adapter`, and `QLoRA`. If we explain all of these names at once, the supplementary study itself becomes too large, and beginners can easily miss what to hold first.

This Section first focuses on LoRA itself. The goal is not to implement LoRA. It is to read the name LoRA by separating `what it tries to represent compactly` and `what it adapts for a purpose`, and to hold that low-rank is a phrase attached to `the way an update is represented`, not to the size of the model body. The detailed comparison among adapter, LoRA, and QLoRA continues in the next supplementary study, P6-9.5.

## Reading Low-Rank Adaptation by Splitting the Name First

LoRA is short for Low-Rank Adaptation. If we try to follow the linear-algebra meaning of `rank` or matrix factorization formulas from the beginning, implementation details become larger than the main line. For now, it is enough to enter with the name read as follows.

| Name piece | Meaning to hold first |
| --- | --- |
| Low-Rank | Instead of learning the entire large change as-is, it tries to represent the change in a smaller form |
| Adaptation | It does not create a base model from scratch, but adapts an existing model to a purpose |

Here, `small` does not mean that the model body becomes small. The base model is still large. What LoRA tries to reduce is `the burden of changing the whole base model again at large scale`. In other words, the idea is to keep the huge body as much as possible, then separately learn and attach only the changes needed for the purpose as a small adjustment delta.

## Why the Name `Low-Rank` Is Used

Very simply, LoRA is the idea: `Do not rewrite the whole large weight; approximate it with a smaller adjustment structure.`

At this stage, we can understand it as follows.

- The original weight matrix is very large.
- But the entire change needed for task adaptation does not always have to be that large.
- So the idea appears: express the `delta` as the product of two smaller adjustment matrices.

In other words, LoRA starts from the view that `the part that changes for the task` can have a smaller structure than `the whole base model`.

`LoRA is an attempt to represent only the needed delta in a smaller structure, rather than relearning the whole large model.`

The important point here is that LoRA does not mean creating a separate `small model`. The core idea is to avoid rewriting the existing large weights and instead represent the update needed for task adaptation in a smaller structure. So low-rank is attached more to `the way the update is represented` than to the model size itself.

## Where LoRA Is Attached in the Model

When first reading about LoRA, it is common to get stuck on whether `LoRA is attached outside the model or inside it`.

A safer explanation is as follows.

- The original weights of the base model are mostly kept fixed.
- Small trainable adjustment deltas are placed around core linear transformation layers such as attention.
- The actual output can be understood as `calculation result from the original weight + calculation result from the small adjustment delta`.

In other words, LoRA is not about making a completely separate second model. It is closer to adding a `small correction device` to some linear transformations inside the base model.

## Exercise and Example

The goal of this example is not to implement real LoRA. It is to compare the scale difference between a `whole large matrix` and a `small rank adjustment delta` across rank values.

The code below uses a base weight size and several rank values. In the result, we check the number of parameters in the whole matrix, the number of LoRA adjustment parameters for each rank, and the ratio to the whole matrix.

The key result to check is that the core of LoRA is to greatly reduce the number of needed parameters by learning only a small rank adjustment delta instead of the whole matrix.

Before looking at the example, it helps to predict the following first.

| Comparison scene | Change to predict before running | Why this prediction matters |
| --- | --- | --- |
| From `rank=4` to `rank=32` | The number and ratio of adjustment parameters both increase | Rank increases room for expression, but also raises cost. |
| Comparing the whole matrix with the LoRA adjustment delta | The LoRA adjustment-delta ratio is very small | This helps us read `efficient adjustment` as a scale difference, not a slogan. |
| Looking at several ranks side by side | Smaller ranks can help fast experiments, but may allow less room for expression | The number does not mean `smaller is always better`. |

```python
# Compare the whole weight matrix with LoRA update parameters by rank
# to build intuition for the scale of a low-rank adjustment delta.
hidden_size = 4096
ranks = [4, 8, 16, 32]

full_matrix_params = hidden_size * hidden_size

print("full_matrix_params =", full_matrix_params)

for rank in ranks:
    lora_update_params = hidden_size * rank + rank * hidden_size
    ratio = lora_update_params / full_matrix_params
    print(
        f"rank={rank:>2}: "
        f"lora_update_params={lora_update_params}, "
        f"ratio={ratio:.4f}"
    )
```

I ran this example with the local `.venv` Python and confirmed that the output matches the manuscript.

The example output can be read as follows.

```text
full_matrix_params = 16777216
rank= 4: lora_update_params=32768, ratio=0.0020
rank= 8: lora_update_params=65536, ratio=0.0039
rank=16: lora_update_params=131072, ratio=0.0078
rank=32: lora_update_params=262144, ratio=0.0156
```

These numbers do not claim the actual setting of a particular product. They simply show the following intuition.

- The whole weight matrix is very large.
- A small rank adjustment delta can be much smaller.
- If rank increases, the adjustment expression capacity can increase, but the size of the adjustment delta also increases.

This difference helps explain why the phrase `efficient adjustment` appeared.

The chart below again shows how the LoRA adjustment-delta ratio increases as rank grows. The key is not only that the adjustment delta is smaller than the whole matrix, but also that rank choice is a handle that changes both cost and room for expression.

![LoRA adjustment-delta ratio to the whole matrix by rank](/AiBook/assets/part-06/chapter-09/lora-rank-ratio-en.png)

After the example, it is more important to translate the numbers back into a structural choice.

| What to read directly from the number | Misunderstanding if the number is read badly | Question that leads to the next judgment |
| --- | --- | --- |
| As rank increases, the adjustment-delta size also increases | It can be misunderstood that increasing rank is still `light for free` | Is the current bottleneck lack of expression capacity or resource constraint? |
| The adjustment-delta ratio is very small compared with the whole matrix | LoRA can be misunderstood as `making a new small model` | Do we need the advantage of keeping the base model and separating only the delta? |
| Small-rank comparison alone cannot determine quality | The numbers can be mistaken as enough to choose the final method immediately | Is this stage final performance confirmation or fast exploration? |

## Checklist

- You should be able to unpack LoRA as `Low-Rank Adaptation`.
- You should be able to explain low-rank as an update-representation axis, not a model-body-size axis.
- You should be able to read the fact that rank growth also increases the adjustment-delta size as a balance between cost and room for expression.

## Sources and References

- Edward J. Hu et al., [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685){: target="_blank" rel="noopener noreferrer" }, arXiv, 2021, accessed 2026-07-19.
