# P6-1.4 Generation Does Not Follow a Single Iteration Pattern

> Section ID: `P6-1.4`
> Version: `v2026.08.28`

In P6-1.3, we saw that an LLM generates by calculating next-token candidates from the current context and appending the selected token to that context. This is an important account of text generation, but it is not a procedure shared by all generative AI. Image diffusion, introduced in Part 5, repeatedly restores an entire state of random noise instead of selecting the next token one at a time.

The question in this section is **what counts as one step in autoregressive LLM generation and iterative image-diffusion restoration, and what can be changed to control the result**.

## Different Units Behind the Same Word: Iteration

Both models use patterns learned from training data to produce results that meet conditions, and both perform repeated computations during generation. What changes at each iteration, however, is different.

| Perspective | Autoregressive LLM | Image diffusion |
| --- | --- | --- |
| Unit of iteration | One next token | One restoration step over the entire image or latent representation |
| Starting state | Input context and tokens already generated | Random initial noise |
| Core computation in one step | A distribution over next-token candidates | Prediction of noise in the current state or of a restoration direction |
| State after one step | New context with the selected token appended | A new, slightly less noisy state |
| Stopping criterion | Generation rules such as an end token, length limit, or tool call | Completion of the specified reverse steps |

When an LLM chooses a continuation such as `delayed` after `The delivery was`, the new token is added to the context and changes the next candidate distribution. Diffusion does not start by appending separate candidates like pieces of a sentence. It takes the entire current image state and time step `t`, predicts noise, and lets the scheduler use that prediction to calculate the next state.

## Control Values Do Not Play the Same Roles Either

The settings on a generation screen may look like the same kind of control because they all change the result. To explain differences in results, though, we need to distinguish which state each value changes.

| Control perspective | Representative autoregressive LLM values | Representative image-diffusion values | First question to ask |
| --- | --- | --- | --- |
| Starting conditions | System instructions, prompt, document context | Text, reference images, structural conditions | What should the model refer to? |
| Output variation | temperature, top-k, top-p | seed | What different starting points or selections are possible under the same conditions? |
| Iteration method | Token-selection and stopping rules | steps, scheduler | How many times, and by what rule, is the next state updated? |
| Strength of adherence to conditions | Instruction structure, context organization, postprocessing rules | guidance | What trade-off arises between satisfying conditions and natural variation? |

`temperature` is used to make an LLM's next-token candidate distribution broader or narrower. A `scheduler`, by contrast, is a numerical rule that moves a diffusion noise state to the next restoration state. Both may affect diversity and stability, but one should not be read as the other under a different name.

## Record the Run Before Focusing on a Single Image or Sentence

With either generation method, looking only at the result makes it easy to lose track of the cause. To interpret a result again, record the input context and selection rules for an LLM, and the seed, steps, scheduler, and conditions for diffusion.

| When a result changes | First records to check for an LLM | First records to check for diffusion |
| --- | --- | --- |
| Content or scene changes | System instructions, document context, prompt, selection rules | prompt, conditioning input, seed, guidance |
| Length or iteration pattern changes | max tokens, stopping rules, temperature | steps, scheduler, resolution |
| Attempting to reproduce the same result | Model version, complete input, sampling settings | Model version, seed, complete conditions, scheduler settings |

Starting with P6-2, we will examine the computational units an LLM uses to read text. P6-21.3 covers running an open diffusion model and recording what happens when one value changes. The key here is to avoid treating an LLM's next-token selection and a diffusion restoration step as interchangeable explanations.

## Checklist

- I can explain an LLM's next-token selection and image diffusion's restoration of the entire state as different units of iteration.
- I can distinguish an LLM starting from context and generated tokens from diffusion starting from initial noise.
- I can avoid grouping temperature, top-k, and top-p with seed, steps, scheduler, and guidance as if they played the same roles.
- I can explain why each generation method's execution conditions must be recorded to account for differences in results.

## Sources and References

- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed: 2026-08-28. Used as a source for autoregressive language models that predict the next token conditioned on the preceding token context.
- Jonathan Ho, Ajay Jain, Pieter Abbeel, [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed: 2026-08-28. Used as a source for iterative reverse generation starting from a noisy state.
