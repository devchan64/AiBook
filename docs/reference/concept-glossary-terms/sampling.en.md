<a id="sampling"></a>

## sampling

- Meaning: Sampling is the procedure that selects one actual output piece from the candidate distribution computed by a model. After the model estimates `which candidates are how plausible`, sampling decides which candidate is actually taken. In a language model, this means choosing one of the next-token candidates; in image generation, it can mean following a probabilistic denoising path at the next step.
- Why it matters: Sampling explains why the same input can produce different generated outputs, and why probability calculation and actual output selection must be separated. It also shows why generation quality is not determined only by model weights; the final choice procedure and settings such as temperature or top-k can strongly affect the result. Understanding sampling helps separate `what the model has made plausible` from `what was actually selected`.
- Related concepts: `next-token prediction`, `token`, `diffusion model`
- Core Section: `P5-15.3`
- Appears in: `P1-5.2`, `P1-10.2`, `P5-15.1`, `P5-15.2`, `P6-1.3`, `P6-4.1`, `P6-6.1`, `P6-6.2`
