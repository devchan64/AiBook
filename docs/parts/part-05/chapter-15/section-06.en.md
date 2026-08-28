# P5-15.6 How Does a VAE Turn an Image into a Latent Representation?

> Section ID: `P5-15.6`
> Version: `v2026.08.28`

P5-15.4 presented diffusion as an algorithm that repeatedly restores noisy states, and P5-15.5 presented U-Net and DiT as choices for predicting that restoration direction. Latent diffusion performs repeated computation in a latent representation rather than directly in pixels. A VAE (variational autoencoder) family connects an image and that latent representation.

The question in this section is **how a VAE differs from an ordinary autoencoder, why it makes a latent space usable for generation, and which calculation it performs in latent diffusion**.

## An Autoencoder Learns a Representation That Can Be Reconstructed

An ordinary autoencoder maps an input image `x` to an often more compact representation `z` through an encoder, then uses a decoder to reconstruct a similar image `x_hat`. Its central signal is the difference between input and reconstruction. A latent representation does not always mean fewer dimensions; here we first read it as a representation space suitable for repeated generation computation.

| Component | What it does | First question to ask |
| --- | --- | --- |
| encoder | maps image `x` to latent `z` | what information remains in a smaller representation? |
| latent representation | intermediate coordinates left by the encoder | how might similar inputs be arranged? |
| decoder | reconstructs `x_hat` from `z` | how much of the original scene can the retained information restore? |
| reconstruction loss | measures the difference between `x` and `x_hat` | does learning preserve important input information? |

This is enough to learn reconstructable representations. But if the latent coordinates made by the encoder are scattered with large gaps, a randomly chosen coordinate may not decode into a natural image. **Reconstructing well** and **generating from a new coordinate** are different requirements.

## A VAE Produces a Distribution Rather Than One Fixed Coordinate

Instead of directly returning one latent coordinate for each image, a VAE encoder predicts a mean `mu` and spread `sigma` for a distribution associated with the image. A sample `z` from that distribution is sent to the decoder.

```mermaid
--8<-- "assets/part-05/chapter-15/vae-latent-diffusion-flow-en.mmd"
```

| VAE value | Meaning | Common confusion |
| --- | --- | --- |
| `mu` | center of the latent distribution for this input | not a finished image |
| `sigma` | spread around that center | not a quality score or predicted noise |
| `z` | latent sample made from `mu`, `sigma`, and randomness | not the same as a time-step diffusion noise state |
| `x_hat` | image reconstructed by the decoder from `z` | not always a diffusion model's final generated result |

During training, `z` is commonly constructed with random `epsilon` sampled from a standard normal distribution.

\[
z = \mu + \sigma \odot \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I)
\]

This is the reparameterization idea: sampling remains random, while the loss can still affect the encoder that produces `mu` and `sigma`. This `epsilon` creates a VAE latent sample; it is not the diffusion noise added to an image state at a time step in P5-15.4.

## Reconstruction and KL Loss Protect Different Requirements

A VAE training objective can be read as reconstruction loss plus a KL-divergence term.

\[
L = L_{reconstruction} + D_{KL}\bigl(q(z\mid x)\;||\;\mathcal{N}(0, I)\bigr)
\]

The useful point is to distinguish the failure each term prevents.

| Loss term | Problem it reduces | Risk when its influence is poorly balanced |
| --- | --- | --- |
| reconstruction loss | decoder loses important content or structure | weak reconstruction can blur outputs; overemphasis can leave irregular scattered coordinates |
| KL divergence | each input distribution drifts too far from a common normal reference | too much pressure can remove information needed for reconstruction |

The KL term does not force every image into one point. It links input-specific distributions to a reference distribution from which generation can sample. A VAE is therefore more than a compression tool: it aims for a latent space whose nearby coordinates remain usable.

## VAE and Diffusion Are Different Stages in Latent Diffusion

Latent diffusion runs its noise prediction and repeated restoration in the latent representation made by a VAE. The VAE moves between image and representation; the diffusion denoiser predicts a noise direction inside the latent state.

| Stage | Main model | Input to output | Question it answers |
| --- | --- | --- | --- |
| latent encoding | VAE encoder | image `x` -> latent `z` | how do we move an image to a workable representation? |
| latent generation | diffusion denoiser and scheduler | noisy latent -> restored latent | what should be removed at this step and how do we move next? |
| image decoding | VAE decoder | final latent -> image | how do we turn the latent result into a visible image? |

A VAE is neither a diffusion scheduler nor a U-Net or DiT denoiser, and not every diffusion model uses one. Pixel-space diffusion is also possible. Latent diffusion is one design that changes the space in which repeated computation happens.

## Check the Boundary with a Small Comparison

| Statement | Component | Why |
| --- | --- | --- |
| `turn an image into a latent representation` | VAE encoder | representation conversion before repeated diffusion |
| `predict noise from the current noisy latent` | U-Net or DiT | diffusion restoration-direction prediction |
| `calculate the next latent state from the prediction` | scheduler | generation-path rule, not learned weights |
| `turn the final latent into pixels` | VAE decoder | makes the result visible to people |

If these statements are distinguishable, we can avoid treating different calculations as one claim such as `the VAE makes the image` or `diffusion trains the VAE`.

## Checklist

- I can explain how an autoencoder uses an encoder, latent representation, decoder, and reconstruction loss.
- I can explain why a VAE encoder makes a latent distribution through `mu` and `sigma`.
- I can distinguish the jobs of reconstruction loss and KL divergence.
- I can keep VAE sampling `epsilon` separate from time-step diffusion noise.
- I can separate the VAE encoder, diffusion denoiser and scheduler, and VAE decoder in latent diffusion.

## Sources and Further Reading

- Diederik P. Kingma, Max Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114){: target="_blank" rel="noopener noreferrer" }, ICLR, 2014, accessed 2026-08-28.
- Robin Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752){: target="_blank" rel="noopener noreferrer" }, CVPR, 2022, accessed 2026-08-28.
