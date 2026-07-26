## Transformer

- Meaning: A Transformer is a family of neural network architectures that uses attention so multiple positions in a sequence can refer to one another without recurrence. Instead of passing information only step by step from front to back, it compares relationships among positions in parallel and builds contextual representations.
- Why it matters: Transformers are a core structural basis of modern LLMs, but they need to be read together with pretraining, scaling, and deployment choices. This concept helps explain that an LLM is not merely a large model; it is the result of combining attention-based architecture with large-scale learning strategies. It also clarifies why language modeling shifted away from RNN-style sequential processing toward architectures that can compare long-range context more directly.
- Related concepts: `Attention`, `language modeling`, `direct lineage`
- Core Section: `P1-11.3`
- Appears in: `P1-9.3`, `P5-13.2`, `P5-14.1`, `P5-14.2`, `P5-15.1`, `P6-4.1`, `P6-4.2`, `P6-4.3`
