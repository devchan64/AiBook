# Part 1 Summary. Reviewing Introduction to AI and the Landscape

> Section ID: `P1-summary`
> Version: `v2026.07.07`

Part 1 was the section for rebuilding the overall terrain before studying AI again. Instead of implementing detailed algorithms or proving formulas in depth, it first organized the terms and viewpoints that will return repeatedly in later learning.

This summary is not meant to repeat every concept from Part 1 at full length. Its role is to help the reader recall where the baseline for each major concept was fixed. If a term becomes unstable again, return to the [Concept Glossary](../../reference/concept-glossary.md) and the representative sections listed there.

The most important goal here is not to treat AI as a buzzword or as the name of one product. AI is a broad field in which rule-based approaches, search, heuristics, probabilistic judgment, data-driven learning, deep learning, generative AI, LLMs, agents, service operation, and social responsibility overlap.

## Purpose of This Part

The purpose of Part 1 was not to finish the technology in depth. It was to establish a common map that keeps later Parts from losing track of where each explanation belongs.

The shortest version of that map is the following:

| Minimum point to keep | Part where it is revisited |
| --- | --- |
| AI is a broad field, and LLMs are one stream inside it. | Part 6 |
| Learning and model execution are different stages. | Part 2, Part 3 |
| Rules, search, probability, and learning are different solution styles. | Part 3 |
| Deep learning is a stream of representation learning, and the Transformer is one structure inside it. | Part 5 |
| In services, data, tools, and operational judgment outside the model also matter. | Part 6, Part 7 |

## Goal of This Part

After Part 1, AI-related terms and service experiences should no longer be mixed as if they belonged to one flat conceptual layer. They should be readable again inside a larger map.

## The Core Flow Covered in This Part

The flow of Part 1 can be summarized like this:

1. It clarifies the scope of the word AI.
2. It reviews rule-based approaches and symbolic AI.
3. It separates search, knowledge representation, and probabilistic reasoning.
4. It moves to machine learning as the practice of learning patterns from data.
5. It connects that flow to deep learning as representation learning.
6. It places generative AI and LLMs on the same large map.
7. It continues into prompts, embeddings, RAG, and agents.
8. It keeps service architecture and operational constraints visible.
9. It ties that technical map to ethics, copyright, security, real-world use, and forecasting.

This does not mean that older techniques vanished and were fully replaced by newer ones. The center of gravity changed over time, and some concepts returned in new names and new positions.

For example, `search` and `heuristics` mattered in early AI problem solving, but they still reappear in modern AI as ways of reducing candidates and lowering computational cost. `Probability` and `uncertainty` keep returning whenever predictions, classifications, or generated outputs have to be interpreted.

There are also boundaries that Part 1 deliberately closed early. `Uncertainty`, `probability`, and `stochastic process` are not the same thing, and a `heuristic` does not play the same role as a `probabilistic model`. That distinction is needed before later Parts discuss classification scores, calibration, generation settings, and prompt heuristics without flattening them into one level.

The relationship between generative AI and LLMs should be read the same way. `Generative AI` is the broader category that produces new content such as text, images, audio, or code. An `LLM` is one major stream inside that broader category, especially around language modeling and Transformer-based development. Part 6 returns to that boundary through the main line of `token -> Transformer -> GPT` and through the background comparison with BERT-style models.

The direct lineage of LLMs and the surrounding evidence for their rise also need to stay separate. CNNs, GPUs, YOLO, and WaveNet remain useful as surrounding evidence for the spread of deep learning, but the direct lineage of LLMs is kept with language modeling, Seq2Seq, Attention, and the Transformer. That is why later explanations of CNNs, Transformers, GPT, and BERT do not collide.

Examples such as recommendation, ranking, control, search services, and autonomous driving should also be read through the same principle. In Part 1 they are kept only as short scenes that help separate problem types, not as full domain histories or implementation guides.

## Concepts That Must Remain

The concept that should last the longest from Part 1 is distinction.

The scope of the word AI should be held in the same way. In the current edition, the baseline is simply that sources such as OECD, English-language dictionaries, the Stanford Encyclopedia of Philosophy, and NIST all support the idea that AI is both a broad field and a category of systems. More detailed cross-language dictionary comparison is left as optional reinforcement rather than treated as essential definition work here.

| Distinction | View to keep |
| --- | --- |
| AI and machine learning | AI is the broader field, while machine learning is an approach that learns patterns from data. |
| Machine learning and deep learning | Deep learning is a major stream of machine learning that learns representations through neural networks. |
| Deep learning and LLMs | LLMs are one fast-growing stream inside deep learning, especially around language modeling and Transformer-based development. |
| Learning and model execution | Learning changes internal model values, while model execution uses the already learned model. |
| Terms around `inference` | Read `inference` first as model execution, `reasoning` as a thinking process, `prediction` as model output, and `generation` as content creation. |
| Prompts and the model | A prompt is an input that guides model behavior. It is not complete control over the model's internal knowledge or behavior. |
| RAG and agents | RAG is a structure that retrieves external information and adds it to the input. An agent is a structure that carries a goal through multiple task steps. |
| Model and service | A real AI service is not only a model. It is a structure where apps, data, tools, permissions, logs, evaluation, and operational constraints also work together. |

When those distinctions remain, later Parts on mathematics, code, models, data, and service structure are easier to place on the whole map.

Like the rest of the Part, this summary page does not repeat definitions in full where they were already explained in detail. Its role is to rebuild what must be remembered, not to replace the representative sections.

## Places Where Misunderstanding Is Easy

Part 1 especially needed to resist the following misunderstandings:

- Do not treat AI and LLM as the same term.
- Do not describe generative AI as if it were the final form of all AI.
- Do not treat rule-based approaches only as obsolete methods.
- Do not mix heuristics with probabilistic models.
- Do not read labels only as “correct answers.”
- Do not mistake embeddings for human-readable semantic definitions.
- Do not mistake prompts for commands that completely control a model.
- Do not define agents as systems of unlimited autonomous execution.
- Do not write AI forecasts from private speculation or AI-generated prose alone.

The book reduces these misunderstandings by keeping Korean terms tied to their English originals where needed. Terms such as `inference`, `model`, `parameter`, `generation`, and `level` need continued distinction because their meaning shifts by context.

Among them, `inference` is the one that most often needs to be checked again. In Part 1, `inference` is first separated as model execution, `reasoning` as logical or cognitive-style reasoning, `prediction` as model output, and `generation` as generated result. That distinction becomes necessary again in Part 6 when reading next-token prediction, responses that look like reasoning, and evaluation contexts that talk about model outputs.

## What This Part Explains and What It Does Not

Part 1 focused on explaining the overall terrain of AI and the shared language around it. It therefore did not try to finish detailed algorithmic formulas, internal deep-learning calculations, or implementation-level LLM service design here.

## Connection to Later Parts

Part 1 is the first main body part of the book, so its main role was not to connect back to earlier technical parts but to establish the starting standard for all later learning.

The map built in Part 1 is reused across Part 2, Part 3, Part 5, Part 6, and Part 7.

In shorter form:

| Question first established in Part 1 | Part where it is read again |
| --- | --- |
| How are models, data, parameters, learning, and inference translated into the language of calculation? | Part 2 |
| How do the differences among labels, structure, and reward appear in real machine-learning problems? | Part 3 |
| Why do representation learning and neural architectures branch into CNNs, RNNs, and Transformers? | Part 5 |
| Why do tokens, GPT, RAG, and agents connect into one service structure? | Part 6 |
| How should evaluation, records, and retrospectives be kept in real project documents? | Part 7 |

If that table remains clear, it also becomes easier to accept that Part 1 did not need to complete every detail. The role of this summary is not to end the explanation, but to keep the reader from losing track of what should be revisited later.

## Questions This Part Intentionally Leaves Open

Part 1 intentionally leaves the following questions open:

- How should these concepts be checked again through mathematics and code?
- What is the shared computational structure of machine learning and deep learning?
- How do LLMs and generative AI work inside service structure?

Those questions are recovered later through fuller explanation and practice.

## Questions to Check Before Moving to the Next Part

Before moving to Part 2, check whether you can roughly answer the following:

- Can you explain the broad relationship among AI, machine learning, deep learning, generative AI, and LLMs?
- Can you explain the difference between rule-based and learning-based approaches?
- Can you roughly explain the relationship among data, features, representations, models, parameters, learning, and model execution?
- Can you explain that uncertainty, probability, and stochasticity are not the same thing?
- Can you explain that prompts, embeddings, vector search, RAG, and agents play different roles?
- Can you explain that an AI service is not built from one model alone?
- Can you distinguish between personal working hypotheses and claims that have external evidence?

You do not need perfect answers to every question. The purpose of Part 1 is not memorizing final answers. It is building the map you can return to during later study.

There are also things it is completely normal not to know yet after Part 1.

- It is fine if you still cannot explain loss functions and gradients with formulas.
- It is fine if you do not yet know the internal calculations of Transformers and attention in detail.
- It is fine if you cannot yet implement RAG, tool use, and agent code yourself.
- What matters is being able to state the big picture: how the problem is divided, what the model is responsible for, and what the service must add around it.

## Perspective for the Next Part

Part 2 moves into foundational recovery. The foundation there is not the ability to prove mathematics deeply. It is the minimum language needed to read AI documents and code.

The model, data, representation, parameter, learning, and model execution introduced in Part 1 reappear in Part 2 through formulas and code.

1. A model receives input.
2. That input is expressed as numbers, vectors, and matrices.
3. Learning adjusts values.
4. That adjustment is described through loss and optimization.
5. Probability and statistics become the language for uncertain data.
6. Code becomes the tool that reproduces those calculations.

So Part 2 is not where AI is turned into mathematics for its own sake. It is where the map built in Part 1 starts to be checked again in actual computational language.

## Closing Part 1

When Part 1 is complete, the reader should be ready to see AI not as a single word but as concepts spread across multiple levels.

Two attitudes matter next.

First, personal intuition should not be discarded. Old classroom memories, practical questions from work, and impressions formed through recent tools are good starting points for learning.

Second, that intuition should not be treated as established fact without checking. It has to be adjusted through standard terminology, external evidence, actual code, and small experiments.

Those two attitudes tie together the beginning and the end of Part 1. The front half needed the ability to keep models, data, probability, and service structure from collapsing into one flat category. The back half needed the habit of reading claims about bias, safety, accountability, and forecasts with evidence.

In the end, the minimum standard Part 1 leaves behind is this:

> explaining AI well  
> and  
> reading claims about AI critically
>
> are two sides of the same study attitude

Part 2 continues from there into mathematics, code, and data calculation.

## Sources and References

This document is an original summary of Part 1 as a whole. It does not directly quote external sources.
