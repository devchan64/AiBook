<a id="residual-connection"></a>

## residual connection

- Meaning: A residual connection adds the original input representation to the newly computed result before passing it to the next layer. Instead of forcing every layer to overwrite the previous representation completely, it keeps an additional path through which the earlier information can continue to flow.
- Why it matters: Deep neural networks can become unstable when earlier representations are repeatedly overwritten. Residual connections help Transformer blocks stack deeply while preserving information flow and making learning less brittle. The key idea is `add the new computation without cutting off the original path`.
- Related concepts: `Transformer`, `layer normalization`, `feed-forward network`
- Core Section: `P5-14.7`
- Appears in: `P5-14.1`, `P5-14.2`
