<a id="bpe-byte-pair-encoding"></a>
<a id="bpebyte-pair-encoding"></a>

## BPE, Byte Pair Encoding

- Meaning: Byte Pair Encoding is a tokenizer method that builds a subword vocabulary by repeatedly merging character pieces or fragments that often appear together. It starts from small units and gradually treats frequent combinations as larger token units.
- Why it matters: BPE shows why tokenization is not simple whitespace splitting. The learned vocabulary affects token counts, cost, and how rare or frequent words are divided, so the length a user sees and the length a model computes can differ.
- Related concepts: `tokenization`, `WordPiece`, `SentencePiece`
- Core Section: `P6-2.2`
- Appears in: `P6-2.2`, `P6-2.5`, `P7-4.1`
