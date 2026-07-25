<a id="augmentation"></a>

## augmentation

- Meaning: In RAG, augmentation is the step that attaches retrieved material to the current input context so the model can use it when generating an answer. It is more than finding documents; it is arranging the found material as usable context.
- Why it matters: Retrieval alone does not guarantee a grounded answer. The quality of a RAG system depends on what is attached, how much is attached, and in what order or format it is placed in the prompt. Augmentation helps readers separate finding information from making that information available to generation.
- Related concepts: `retrieval-augmented generation`, `generation`, `prompt`
- Core Section: `P1-13.3`
- Appears in: `P1-14.1`
