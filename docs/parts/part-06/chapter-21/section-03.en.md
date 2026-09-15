# P6-21.3 Evaluating Open Diffusion Models by Changing One Condition at a Time

> Section ID: `P6-21.3`
> Version: `v2026.08.28`

P6-21.1 examined what is made available in an open model, along with its license and scope of release. P6-21.2 separated execution feasibility, memory placement, and quality judgment. We now apply these criteria to a small comparison experiment with an open diffusion model. The purpose is not to choose the most impressive image, but to see how the seed, steps, scheduler, and conditions learned in Part 5 appear in actual run records and differences between results.

The question in this section is **how to evaluate output differences, execution demands, and reproducibility separately while changing only one value in an open diffusion model**.

## Common Conditions to Fix Before Comparing

If the prompt, seed, steps, and scheduler all change in one run, a different image will not tell us which value caused the difference. Record the following conditions first, and keep them unchanged within a comparison set.

| What to fix | Why to record it |
| --- | --- |
| Model ID, revision, and license-check result | Confirm that the comparison uses the same weights and terms of use |
| prompt, negative prompt, resolution | Keep the scene requirements and input size consistent |
| dtype, device, offload method | Avoid mistaking speed or memory differences for differences in model settings |
| Evaluation criteria | Separate personal preference from whether the conditions are satisfied |

For example, evaluation criteria can include `condition match`, `structure preservation`, `unwanted distortion`, `execution time`, `memory`, and `reproducibility`. These are observation fields for understanding the difference caused by one changed value, rather than a scorecard for ranking models absolutely.

## Four Axes for Changing One Thing at a Time

The four axes below are not a list of tests that must all be completed. They help you choose the one axis that fits the current question. Within a set, change only the entry in one row's `Value to change` column and hold everything else fixed.

| Test axis | Values to hold fixed | Value to change | Question to observe |
| --- | --- | --- | --- |
| Starting point | Model, prompt, steps, scheduler, guidance | seed | How does different initial noise change scene variation? |
| Iteration path | Model, prompt, seed, guidance | Either steps or scheduler | How does the iteration count or update rule affect time, structure, and detail? |
| Conditioning strength | Model, prompt, seed, steps, scheduler | guidance | What trade-off arises between condition match, distortion, and diversity? |
| Conditioning type | Model, seed, resolution, evaluation criteria | Text only / reference image / structural condition | What does an added condition fix, and which degrees of freedom does it reduce? |

For example, changing steps while comparing seeds changes both the starting point and the iteration path. To compare `seed=12` with `seed=34`, keep the prompt, model revision, resolution, steps, scheduler, and guidance the same. This lets you connect the fact that the image changed to one explanation: the starting point in initial noise.

```mermaid
--8<-- "assets/part-06/chapter-21/p6-21-3-one-variable-test-flow-en.mmd"
```

## Record Execution Success and Result Evaluation in Separate Fields

Completing generation is a record of execution feasibility. Whether the result follows conditions and preserves structure is a quality record. Excessive execution time or insufficient memory is an operational record. Combining these three into one sentence makes the next choice less clear.

| Category | Question to check | Example records |
| --- | --- | --- |
| Execution feasibility | Did generation finish without errors? | status, error message, dtype, device |
| Quality | Is the expected difference visible for the changed condition? | condition match, structure preservation, artifact note |
| Operational demands | Are time and memory requirements manageable for repeated runs? | elapsed seconds, peak memory, retry cost |
| Reproducibility | What remains the same when rerunning under the same conditions? | seed, revision, scheduler, reproducibility note |

Depending on model libraries, hardware, and computation methods, identical pixels cannot always be guaranteed. Even then, do not stop at “the result differed despite the same seed.” Keep the model revision, device, dtype, scheduler, and library versions on the list of items to check.

## Complete the Comparison with a Minimal Record Template

The CSV below is a minimal template with one run per row. Add image storage paths or detailed human-review notes as needed, while retaining both the changed value and the fixed values in the comparison.

[P6-21.3 Run Record CSV Template](/AiBook/assets/part-06/chapter-21/p6-21-3-diffusion-test-record-template.csv)

After filling in the records, explain the result by answering these three questions.

1. What value changed in this set?
2. What other conditions were held fixed?
3. What differences were observed in output, execution time, memory, and reproducibility?

If the only answer is “it looked better,” revisit the comparison. Connect the changed value to the observation: for example, “Changing only guidance from 5 to 9 made the prompt's color condition clearer, but increased edge distortion; execution time stayed almost the same.” This completes the actual testing of an open diffusion model within Part 6, including records of learning, execution, and evaluation.

## Checklist

- I can fix and record the model ID, revision, license, inputs, and execution environment before a comparison.
- I can explain why only one of seed, steps, scheduler, guidance, or conditioning input should change at a time.
- I can record judgments about execution success, output quality, operational demands, and reproducibility in separate fields.
- I can connect a difference in results to the one changed value and formulate the next test question.

## Sources and References

- Hugging Face Diffusers, [Reproducible pipelines](https://huggingface.co/docs/diffusers/using-diffusers/reusing_seeds){: target="_blank" rel="noopener noreferrer" }, official documentation, accessed: 2026-08-28. Used as a reference for managing the random starting point of a diffusion pipeline with a generator and seed.
- Hugging Face Diffusers, [Schedulers](https://huggingface.co/docs/diffusers/using-diffusers/schedulers){: target="_blank" rel="noopener noreferrer" }, official documentation, accessed: 2026-08-28. Used as a reference for explaining the scheduler as a setting that changes the iterative path of generation.
