# P5-15.5 What Do Attention and Transformers Do in Diffusion Models?

> Section ID: `P5-15.5`
> Version: `v2026.08.28`

P5-15.4 explained the algorithm: make noisy states, train a model to predict noise, and repeatedly move noise toward data at generation time. That algorithm alone does not decide what kind of network makes the prediction or how a text condition reaches it.

The question in this section is **how a diffusion model connects conditions, the current noisy state, and a denoising network, and where attention and Transformers fit in that structure**.

## A Condition Is Not the Denoiser

A text prompt, reference image, or structural guide is first converted into a representation the model can calculate with. The denoising network then receives that condition together with the current noisy image or latent state and the time step.

```mermaid
--8<-- "assets/part-05/chapter-15/diffusion-conditioning-structure-en.mmd"
```

| Component | Main role | Do not confuse it with |
| --- | --- | --- |
| condition encoder | turns text or a reference condition into a usable representation | a device that lays pixels out directly |
| noisy state | current image or latent state to restore | the condition itself |
| denoising network | predicts noise or a restoration direction from state, time, and condition | a scheduler |
| scheduler | calculates the next state from the prediction | learned model weights |

The same denoising network is used repeatedly at different time steps. A condition can guide every prediction, but the condition encoder does not replace the repeated restoration algorithm.

## Self-Attention and Cross-Attention Answer Different Questions

Attention is often described as one feature. In a conditional diffusion model, two questions should be separated.

| Mechanism | What it connects | Useful question |
| --- | --- | --- |
| self-attention | positions or patches inside the current image/latent representation | what distant image regions should be considered together? |
| cross-attention | the current image/latent representation and a condition representation such as text | which condition words or reference features should influence this region? |

For example, self-attention can relate a small object in one region to a matching background region elsewhere. Cross-attention can connect a text condition such as `red umbrella` to relevant image regions. Both are possible structure choices; neither changes the basic diffusion loop into token-by-token text generation.

## U-Net and DiT Are Alternative Denoisers

The diffusion algorithm does not require one fixed denoiser architecture. U-Net is a widely used network that combines multiple spatial scales. A Diffusion Transformer (DiT) can split a latent representation into patches and process their relationships with Transformer blocks.

```mermaid
--8<-- "assets/part-05/chapter-15/diffusion-denoiser-comparison-en.mmd"
```

| Comparison point | U-Net-based denoiser | DiT-based denoiser |
| --- | --- | --- |
| internal processing unit | feature maps at several spatial scales | latent patches processed by Transformer blocks |
| use of attention | may add attention at selected resolutions | uses Transformer attention as a central processing structure |
| common input | noisy state, time step, optional condition | noisy latent patches, time step, optional condition |
| common output | predicted noise or restoration direction | predicted noise or restoration direction |

The comparison is not a ranking. Both sit in the same place in the diffusion loop: they read the current state, time, and condition, then make a prediction used by the scheduler.

## The Connection to Latent Diffusion

Diffusion can operate in pixel space or in a smaller latent space. In latent diffusion, a VAE-family encoder and decoder are added to move between image and latent representations, but they do not replace the denoising network that predicts noise or the scheduler.

P5-15.6 explains how a VAE differs from a general autoencoder and why a latent space must have a usable distribution for generation. This section keeps its focus on conditions, U-Net or DiT, and attention as structures that **predict noise from the current state**.

## Checklist

- I can explain the connection among a condition encoder, noisy state, denoising network, scheduler, and generated result.
- I can distinguish self-attention from cross-attention.
- I can describe U-Net and DiT as different denoiser choices.
- I can explain why VAE-family encoders and decoders are optional latent-diffusion components rather than denoisers.
- I can distinguish the scheduler from the learned denoising network.

## Sources and Further Reading

- Robin Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, accessed 2026-08-28.
- William Peebles, Saining Xie, [Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748){: target="_blank" rel="noopener noreferrer" }, arXiv, 2023, accessed 2026-08-28.
