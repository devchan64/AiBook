<a id="source-event"></a>
<a id="glossary-source-event"></a>

### source event

- Meaning: A source event is the original real event unit before it is cut into input windows or summary rows. Examples include one action, one alert, or one session that becomes the starting point for derived input pieces.
- Why it matters: If many overlapping input windows are made from the same source event, the number of model-input pieces grows, but the number of real events does not. The concept keeps derived window counts from being read as stronger evidence than they are, and it helps track related pieces from the same event during representativeness checks and evaluation splitting.
- Related concepts: `input window`, `source data`, `sample`, `dataset`, `data leakage`
- Core Section: `P3-5.6`
- Appears in: `P3-5.6`, `P3-5.7`
