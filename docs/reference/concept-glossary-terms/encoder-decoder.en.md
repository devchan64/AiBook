<a id="encoder-decoder"></a>

## Encoder-Decoder

- Meaning: An Encoder-Decoder separates reading an input sequence from generating an output sequence.
- Why it matters: It explains why translation and summarization models can be read as two linked roles: first encoding the source sequence, then decoding a new sequence from that representation. It also makes the fixed-length bottleneck and the later need for attention easier to understand.
- Related concepts: `encoder`, `decoder`, `Attention`
- Core Section: `P1-11.2`
- Appears in: `P1-11.3`, `P6-5.1`
