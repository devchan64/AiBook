## SentencePiece

- Meaning: SentencePiece is a tokenizer family that learns and applies subword pieces from the source string itself, including whitespace markers, instead of assuming whitespace is already a fixed word boundary.
- Why it matters: In inputs that mix languages, numbers, and symbols, whitespace alone may not define stable computational pieces. SentencePiece helps readers understand tokenizer-family differences as differences in how the whole string, including spaces, is handled.
- Related concepts: `tokenization`, `Byte Pair Encoding`, `WordPiece`
- Core Section: `P6-2.5`
- Appears in: `P6-2.5`, `P7-4.1`
