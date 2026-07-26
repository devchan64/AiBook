## WordPiece

- Meaning: WordPiece is a tokenizer family that chooses subword pieces with vocabulary efficiency in mind and represents rare words by combining smaller reusable pieces. Instead of memorizing every full word, it learns useful pieces and decomposes new words into those pieces.
- Why it matters: WordPiece shows that different tokenizer methods can split the same text into different computational units. This affects token count, model input length, and cost, so the tokenizer used by a pretrained model is not a minor implementation detail. It changes the input representation itself.
- Related concepts: `tokenization`, `Byte Pair Encoding`, `SentencePiece`
- Core Section: `P6-2.2`
- Appears in: `P6-2.2`, `P6-2.5`, `P7-4.1`
