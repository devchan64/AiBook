## positional encoding

- Meaning: Positional encoding is information that tells a model where a token appears in a sequence, separate from the token's own meaning vector. It lets the model distinguish whether the same word appears near the beginning, middle, or end of a sentence.
- Why it matters: Positional encoding is a basic mechanism that lets Transformers reflect word order without recurrent processing. Even if self-attention compares tokens well, order is hard to distinguish unless position information is supplied. This concept joins `what token is this?` with `where is it placed?`
- Related concepts: `Transformer`, `self-attention`, `token`
- Core Section: `P1-11.3`
- Appears in: `P6-4.3`
