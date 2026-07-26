<a id="query-key-value-qkv"></a>

## query-key-value, QKV

- Meaning: Query-key-value, or QKV, names the three roles in attention: the query represents what the current position is looking for, the key represents what each position can be matched by, and the value carries the content that will actually be mixed into the result.
- Why it matters: QKV turns attention from a vague idea of “looking somewhere” into a clearer calculation flow: ask a question, find matching positions, and bring back the relevant content. It also separates similarity information from the information actually passed forward.
- Related concepts: `self-attention`, `multi-head attention`, `Transformer`
- Core Section: `P5-13.3`
- Appears in: `P5-14.1`, `P6-4.3`, `P6-4.4`
