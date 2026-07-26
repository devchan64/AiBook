## sparse attention

- Meaning: Sparse attention is an attention design direction that reduces computation by keeping only selected connections instead of comparing every token pair with the same density. It is a structural tradeoff between full self-attention and a more limited pattern that prioritizes nearby or important positions.
- Why it matters: Attention comparisons grow quickly as context becomes longer, so long-input systems need practical compromises. Sparse attention helps readers see that long-context support is not only a matter of model size; it is also a design question about which relationships to keep and which to skip.
- Related concepts: `multi-head attention`, `context window`, `long-context`
- Core Section: `P6-4.5`
- Appears in: `P6-4.1`, `P6-4.2`, `P6-4.3`
