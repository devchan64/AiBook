## self-attention

- Meaning: Self-attention is an attention mechanism in which each token in the same sequence calculates relationships with other tokens and updates its own representation. Instead of looking only at the current position, it mixes information from other positions with learned weights.
- Why it matters: Self-attention is a core mechanism that lets Transformers compute contextual relationships directly without sequential recurrence. It helps explain why a token representation can reflect other tokens in the same sequence and why Transformers can mix relationships among many positions within one layer.
- Related concepts: `Transformer`, `Attention`, `positional encoding`
- Core Section: `P5-13.2`
- Appears in: `P1-11.3`, `P5-14.1`, `P5-14.2`, `P6-4.1`
