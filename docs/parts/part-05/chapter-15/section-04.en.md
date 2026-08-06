# P5-15.4 How Does Stable Diffusion Restore an Image from a Text Condition?

> Section ID: `P5-15.4`
> Version: `v2026.08.03`

The earlier sections separated generated artifacts, candidate distributions, and text sampling. Image generation is also generative modeling, but it is not best understood as appending next tokens from left to right.

> When a prompt arrives, through which intermediate states and repeated process does Stable Diffusion make an image?

This section explains the minimum flow: `text condition -> latent noise -> repeated restoration -> image`. It does not cover installation or image-making techniques.

It prepares readers to interpret later Part 7 settings such as seed, sampler, steps, and LoRA by their computational roles.

## It Does Not Draw a Pixel Image All at Once

Stable Diffusion is a representative text-to-image application of latent diffusion. A `latent` is a compressed computational space rather than the pixel image people see. The model starts with random noise in that space, repeatedly reduces noise under the prompt condition, and finally turns the restored latent representation into an image.

| Stage | Minimum role | Question to keep in view here |
| --- | --- | --- |
| text condition | turns the prompt into a computable condition representation | What condition says what to make? |
| initial latent noise | provides a starting state before an image is visible | From which starting point does restoration begin? |
| repeated restoration | repeatedly estimates noise to reduce in the current latent representation | What changes a little at a time while consulting the condition? |
| image restoration | turns the final latent representation into a visible image | What result appears as the actual artifact? |

A prompt is therefore not a pixel layout. It is a condition consulted during restoration; the initial noise and the restoration path also affect the final image.

## Separate Four Components by Their Roles

An implementation contains many more components, but at an introductory level separating their roles matters more than memorizing their names.

| Component | Role | Do not confuse it with |
| --- | --- | --- |
| text encoder | turns a prompt into a condition representation | an instruction that completely fixes an image |
| U-Net | predicts noise to reduce at the current step | one computation that finishes an image |
| scheduler / sampler | sets the rule for moving to the next latent state | a text top-k or top-p word selector |
| VAE decoder | turns a restored latent representation into pixels | the sole judge of image quality |

The text condition normally enters restoration through cross-attention. At this level, it is enough to know that the U-Net consults both the noisy latent state and the prompt condition.

The equations and implementation details of cross-attention are outside this section's scope.

## Why the Same Prompt Can Produce Different Images

| Value | What it changes |
| --- | --- |
| seed | the starting point of initial latent noise |
| steps | how many times denoising is repeated |
| sampler | the rule for moving to the next latent state |
| guidance | how strongly the text condition is consulted |
| base model | the learned image-pattern foundation |

The purpose is not to find one universally best value. It is to separate whether a result changed because of the prompt, starting noise, restoration rule, or model itself.

When comparing images, fix or record these values so the source of a difference can be discussed.

## LoRA and Condition Control Belong to Different Layers

LoRA adds small adjustment weights instead of retraining an entire base model. It can adapt a model toward a subject or style. Condition-control paths such as ControlNet or IP-Adapter can add non-text information, including pose, outlines, or reference images, to restoration.

| Layer | Role to read first |
| --- | --- |
| base model | which image patterns can be restored by default |
| LoRA | how some base-model representations are adjusted |
| ControlNet / IP-Adapter | how additional structural or reference conditions are added |

Changing a LoRA weight and a ControlNet condition together makes it difficult to explain which change produced the result difference.

## Checklist

- I can explain Stable Diffusion as iterative restoration of latent noise rather than one-shot pixel drawing.
- I can distinguish the roles of the prompt, initial noise, repeated restoration, and image restoration.
- I can separate the roles of the text encoder, U-Net, scheduler/sampler, and VAE decoder.
- I do not treat text token sampling and an image-diffusion sampler as the same algorithm.
- I can record whether seed, steps, sampler, guidance, or base model changed.
- I do not treat LoRA and non-text condition control as the same layer.

## Sources and Further Reading

- Robin Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752){: target="_blank" rel="noopener noreferrer" }, arXiv, 2021, accessed 2026-08-03.
- Jonathan Ho, Ajay Jain, Pieter Abbeel, [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-08-03.
- CompVis, [Stable Diffusion official implementation](https://github.com/CompVis/stable-diffusion){: target="_blank" rel="noopener noreferrer" }, GitHub, accessed 2026-08-03.
