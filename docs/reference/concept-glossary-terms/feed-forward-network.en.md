<a id="feed-forward-network"></a>

## feed-forward network

- Meaning: A feed-forward network passes inputs forward through layers without recurrent feedback. In a Transformer block, it is the small network applied after attention to process each position's representation nonlinearly.
- Why it matters: This concept separates the step that reads relationships among tokens from the step that reprocesses each position's representation after context has been mixed in. It also keeps the broader neural-network idea of forward-only layer flow distinct from recurrent structures.
- Related concepts: `Transformer`, `self-attention`, `layer normalization`
- Core Section: `P5-14.6`
- Appears in: `P5-14.1`, `P5-14.2`, `P6-4.1`
