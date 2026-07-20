# Part 1 Summary. Reviewing AI Introduction and the Landscape

> Section ID: `P1-summary`
> Version: `v2026.07.20`

Part 1 was the section for fixing the overall landscape before studying AI again. Rather than implementing detailed algorithms or proving formulas in depth, it first organized the terms and perspectives that keep returning in later learning.

This summary is not a document that repeats every concept from Part 1 at length. It is a closing page that helps you recall where the baseline for each idea was first fixed. If the terms become confusing again, return to the [Concept Glossary](/AiBook/reference/concept-glossary/) and the representative Sections listed there.

The most important goal here is not to see AI as one buzzword or one product name. AI is a broad field where rule-based approaches, search, heuristics, probabilistic judgment, data-driven learning, deep learning, generative AI, LLMs, agents, service operation, and social responsibility overlap.

## Grasping the Whole AI Map Again

The purpose of Part 1 was not to finish the technology in depth, but to establish a shared map so later Parts do not lose track of where the learning is heading.

The shortest way to hold that map again is the following five lines.

| Minimum point to keep first | Part where it is checked again later |
| --- | --- |
| AI is a broad field, and LLMs are one stream inside it. | Part 6 |
| Learning and model execution are different stages. | Part 2, Part 3 |
| Rules, search, probability, and learning are different solution styles. | Part 3 |
| Deep learning is a stream of representation learning, and the Transformer is one structure inside it. | Part 5 |
| In services, data, tools, and operational judgment outside the model also matter. | Part 6, Part 7 |

## Not Mixing Terms and Service Experience at the Same Level

After finishing Part 1, you should be able to stop mixing AI terms and service experience as if they belonged to one flat conceptual layer, and read them again inside a larger map.

## The Flow from Rules to Service Responsibility

The flow of Part 1 can be organized as follows.

1. It organizes the scope of the word AI.
2. It looks at rule-based approaches and symbolic AI.
3. It separates search, knowledge representation, and probabilistic reasoning.
4. It moves into machine learning that learns patterns from data.
5. It connects that flow to deep learning that learns representations.
6. It places generative AI and LLMs inside the larger map.
7. It continues into prompts, embeddings, RAG, and agents.
8. It keeps service architecture and operational constraints visible.
9. It ties ethics, copyright, security, practical use, and forecast review together.

This flow does not mean older techniques disappeared and new techniques completely replaced them. The dominant approach changed over time, and some concepts still remain in use under new names or new positions.

For example, `search` and `heuristic` were important in early AI problem solving, but they still return in modern AI as ways of reducing candidates and lowering computation cost. `Probability` and `uncertainty` also keep returning when we interpret prediction, classification, and generation results.

Part 1 also fixed an important boundary early. `Uncertainty`, `probability`, and `stochastic` are not the same thing, and a `heuristic` does not play the same role as a `probabilistic model`. That distinction has to be set first so that later Parts do not flatten classification scores, calibration, generation settings, and prompt heuristics into one level. The current structure keeps the detailed differences among calibration, confidence, and uncertainty estimation for the first explanation in the supplemental study of P4-6.4 and for the service-judgment connection in P4-15.3.

The relationship between generative AI and LLMs should be read the same way. `Generative AI` is the broader category that creates new content such as text, images, audio, and code, and `LLM` is a representative model stream inside it that developed around language modeling and the Transformer family. That boundary is checked again in Part 6 through the main line of `token -> Transformer -> GPT` and through the background axis of `LLM history` and `BERT-family comparison`.

Chapter 9 also separates direct lineage from surrounding evidence in the same way. CNNs, GPUs, YOLO, and WaveNet remain as surrounding evidence for the spread of deep learning, while the direct lineage of LLMs is kept with language modeling, Seq2Seq, Attention, and the Transformer. That boundary is what allows the later explanations of CNNs and Transformers in Part 5 and GPT and BERT in Part 6 to stay consistent.

Examples such as recommendation, ranking, control, search services, and autonomous driving should also be read by the same principle. In Part 1, those cases remain only as `small scenes that help distinguish problem types`, and they are not expanded into each domain's technical history or implementation detail.

The representative names for symbolic AI and rule-based approaches are treated the same way. Logic Theorist, GPS, MYCIN, and DENDRAL remain only as representative cases that help hold the early flow, and even modern rule-based systems stay at the level of general structures such as authority, policy, and procedure. That keeps Part 1 from reading like a catalog of cases.

## Concepts You Must Remember

The concept that should remain the longest from Part 1 is distinction.

The scope of the word AI should also be held that way. In the current edition, the first thing to hold is only the shared core shown by OECD, English-language dictionaries, SEP, and NIST: AI is both a broad field and a category of systems. More detailed comparison with Korean-language and Japanese-language dictionaries is left as optional reinforcement rather than essential definition work here.

| Distinction | Perspective to remember |
| --- | --- |
| AI and machine learning | AI is the broader field, and machine learning is an approach that learns patterns from data. |
| Machine learning and deep learning | Deep learning is a major stream of machine learning that learns representations through neural networks. |
| Deep learning and LLMs | LLMs are a stream within deep learning that grew strongly around language modeling and the Transformer family. |
| Learning and model execution | Learning changes internal model values, and model execution uses the trained model. |
| Expressions around `inference` | Read `inference` first as model execution, `reasoning` as a thinking process, `prediction` as model output, and `generation` as generated result. |
| Prompt and model | A prompt is an input that specifies model behavior. It is not a device that completely controls the model's internal knowledge or behavior. |
| RAG and agent | RAG is a structure that retrieves external information and adds it to the input, and an agent is a structure that carries a goal through multiple task flows. |
| Model and service | A real AI service is not one model alone. It is a structure where apps, data, tools, permissions, logs, evaluation, and operational constraints work together. |

Once these distinctions are fixed, later Parts on math, code, models, data, and service structure become easier to place on the larger map.

Concepts already explained in detail within the same Part are not defined again at length here. The role of this summary page is to rebuild `what should be remembered`, not to replace the detailed explanation of the representative Sections.

## Easy Places to Misunderstand

The misunderstandings to be especially careful about in Part 1 are the following.

- Do not treat AI and LLM as the same thing.
- Do not describe generative AI as if it were the final form of all AI.
- Do not see rule-based approaches only as outdated methods that disappeared.
- Do not mix heuristics with probabilistic models.
- Do not understand a label only as the answer.
- Do not mistake an embedding for a semantic definition that humans can directly read.
- Do not mistake a prompt for a command that fully controls the model.
- Do not define an agent as a system of unlimited autonomous execution.
- Do not write AI forecasts from personal speculation or AI-generated text alone.

This book reduces such misunderstandings by checking Korean expressions together with the English originals. In particular, words such as `inference`, `model`, `parameter`, `generation`, and `level` need to stay distinguished because their meaning changes by context.

Among them, `inference` is the word that most often needs to be checked again. In Part 1, `inference` is first separated into model execution, `reasoning` into logical reasoning, `prediction` into model output, and `generation` into generated content. That distinction becomes necessary again in Part 6 when reading next-token prediction, responses that look like reasoning, and evaluation contexts that refer to model results.

## The Landscape Part 1 Closes and the Detailed Calculations It Leaves for Later

Part 1 focused on explaining the overall terrain of AI and the shared vocabulary around it. So it does not finish detailed algorithmic formulas, internal deep-learning computation, or implementation details of LLM services here, and leaves them to later Parts.

## Questions Later Parts Will Recover

Part 1 intentionally leaves the following questions open.

- How should these concepts be checked again through math and code?
- What is the common computational structure of machine learning and deep learning?
- How do LLMs and generative AI work inside service structure?

These questions are recovered through actual explanations and practice in later Parts.

## Major Distinctions to Check Before Part 2

Before moving into Part 2, check whether you can answer the following questions.

- Can you explain the relationship among AI, machine learning, deep learning, generative AI, and LLMs as a big picture?
- Can you explain the difference between a rule-based approach and a learning-based approach?
- Can you roughly explain the relationship among data, feature, representation, model, parameter, learning, and model execution?
- Can you explain that uncertainty, probability, and stochastic process are not the same thing?
- Can you explain that prompt, embedding, vector search, RAG, and agent have different roles?
- Can you explain that an AI service is not built from one model alone?
- Can you distinguish between a personal working hypothesis and a factual claim with external evidence?

You do not need perfect answers to all of these questions. The purpose of Part 1 is not to memorize final answers, but to build a map that later learning can keep returning to.

There are also things it is normal not to know yet after reading Part 1.

- It is fine if you still cannot explain loss functions and gradients with formulas.
- It is fine if you do not yet know the internal computation of the Transformer and attention in detail.
- It is fine if you cannot yet write implementation code for RAG, tool use, and agents yourself.
- What matters is being able to explain the big picture of `how the problem is divided`, `what the model is responsible for`, and `what the service still has to add`.

## Closing Part 1

If you have finished Part 1, you are now ready to see AI not as one word, but as concepts spread across multiple levels.

Two attitudes matter next.

First, do not throw away personal intuition. Old memories from learning, questions felt in practice, and the sense formed while using recent tools are all good starting points for study.

Second, do not treat that intuition as fact. Adjust your understanding by checking it through standard terminology, external evidence, actual code, and small practice.

These two attitudes tie together the front and back of Part 1. The front required the ability to keep models, data, probability, and service structure from collapsing into one level. The back required the habit of reading sentences about bias, safety, accountability, and forecasts together with evidence. In the end, the minimum standard Part 1 tries to leave is that `explaining AI well` and `reading claims about AI with evidence` are two sides of the same learning attitude.

From Part 2 onward, that attitude is kept while rebuilding math, code, and data computation.

## Sources and References

This document is an original summary of the full Part 1 content. It does not directly quote external sources.
