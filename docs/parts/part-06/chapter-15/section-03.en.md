# P6-16.3 Supplement: How Are Agent Workflows and Image-Generation Workflows Different?

> Section ID: `P6-16.3`
> Version: `v2026.08.03`

P6-16.1 examined a common format for connecting tools and resources, and P6-16.2 examined a harness for recording and explaining an execution. This supplement is a comparison map that rereads those ideas in another generative-AI scene.

> When both are called workflows, which flow chooses the next action and which transforms data and conditions?

InvokeAI and ComfyUI are not introduced here to teach installation, buttons, or node catalogs. They are examples that make an image-generation pipeline visible, so it is not confused with an agent's control flow. Actual runs and comparison records belong to Part 7.

## The Word Workflow Does Not Name One Structure

An agent workflow is a **control flow** that changes its next action after looking at a goal and intermediate observations. An image-generation workflow is a **data-transformation flow** among prompts, reference conditions, models, latent representations, and images.

| Type | What moves first | Key question | Representative record |
| --- | --- | --- | --- |
| agent workflow | next action | After an observation, should it search, call a tool, or hand off to a person? | goal, observation, next_action, stop_reason |
| image-generation workflow | conditions and intermediate representations | Which conditions and transformations made the final image? | model, prompt, seed, control, output |
| harness | explainability of an execution | Can the same run and failure be read again? | trace, environment, approval, replay |

So a graph with many nodes is not automatically an agent. An image-generation graph can run a fixed data path, whereas an agent can change that path itself in response to observations.

## Reading an Image-Generation Pipeline at Minimum Scope

A minimum Stable Diffusion-family flow can be written as follows.

```text
prompt and reference conditions
-> text condition
-> latent and iterative restoration
-> image conversion
-> output review and execution record
```

This restates P5-15.4's `text condition -> latent noise -> repeated restoration -> image` in the language of an execution environment. It does not explain every implementation detail or every argument of a particular node.

ComfyUI presents such a flow with nodes and links. Its documentation defines a workflow as a graph of connected nodes and explains that it can be saved in image metadata or JSON. [ComfyUI Workflow](https://docs.comfy.org/development/core-concepts/workflow){: target="_blank" rel="noopener noreferrer" }

InvokeAI handles image generation and editing through Canvas and workflow environments. A Canvas project can save layers, masks, reference images, generation settings, and LoRAs in one project file, making it a useful example of recording which conditions were compared. [InvokeAI Canvas Projects](https://invoke.ai/features/canvas/canvas-projects/){: target="_blank" rel="noopener noreferrer" }

## What to Separate When the Same Word Is Used

| Scene | How to read the flow | Confusion caused by mixing it with agents |
| --- | --- | --- |
| ComfyUI node graph | inspect how models, conditions, latents, and images connect | node links can be mistaken for goal judgment or replanning |
| InvokeAI Canvas | inspect image-editing conditions and comparison state | Canvas operations can be confused with model-internal reasoning or agent action |
| AI agent | inspect whether observations choose the next tool, retry, or stop | every multistep run can be flattened into the same data pipeline |

The two image environments help expose generation conditions and transformation paths. Receiving a prompt alone does not automatically create a system that decomposes a goal or autonomously chooses a new tool after seeing a result.

## Leaving a Pipeline Card

Before running a tool, fill in the following five fields. They help avoid leaving only one output image.

| Record field | What to write for an image-generation pipeline | What to compare with an agent pipeline |
| --- | --- | --- |
| input | prompt, reference image, mask, seed | Are the goal and current observation separate? |
| transformation | model, LoRA, control, sampler, steps | Is this data transformation rather than next-action selection? |
| output | generated image and review criterion | How is it different from a final answer or execution result? |
| change | one condition changed at a time | Which observation changed the next action? |
| reproduction | workflow, project file, metadata | What must be left in a trace and replay? |

This card does not rank models or tools. It is the minimum record for explaining which point in a pipeline changed a result and what must remain for the next comparison.

## Boundary Handed to Part 7

- Part 6 compares workflow types and the roles of connection, transformation, and recording.
- Part 7 changes one actual input in environments such as ComfyUI or InvokeAI and records result differences and failure signals.
- Installation, custom-node catalogs, model rankings, and image-making tips are outside this section.

## Checklist

- I can distinguish an agent workflow as closer to control flow and an image-generation workflow as closer to data transformation.
- I can explain ComfyUI and InvokeAI as execution environments for observing and recording a pipeline, not as the model itself.
- I can separately record input, transformation, output, change, and reproduction for image generation.
- I can explain that actual tool operations and condition-comparison exercises belong to Part 7.

## Sources and Further Reading

- ComfyUI, [Workflow](https://docs.comfy.org/development/core-concepts/workflow){: target="_blank" rel="noopener noreferrer" }, official documentation, accessed 2026-08-03.
- ComfyUI, [Nodes](https://docs.comfy.org/development/core-concepts/nodes){: target="_blank" rel="noopener noreferrer" }, official documentation, accessed 2026-08-03.
- InvokeAI, [Canvas Projects](https://invoke.ai/features/canvas/canvas-projects/){: target="_blank" rel="noopener noreferrer" }, official documentation, accessed 2026-08-03.
