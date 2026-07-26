<a id="layer-normalization"></a>

## layer normalization

- Meaning: Layer normalization normalizes values inside a representation for one case so later layers receive more stable value scales.
- Why it matters: Deep Transformer blocks need stable value scales. Layer normalization helps repeated attention and feed-forward blocks remain trainable and usable.
- Related concepts: `Transformer`, `residual connection`, `feed-forward network`
- Core Section: `P5-14.8`
- Appears in: `P5-14.1`, `P5-14.2`
