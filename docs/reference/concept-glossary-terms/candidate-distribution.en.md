<a id="candidate-distribution"></a>

## candidate distribution

- Meaning: A candidate distribution is the set of possible next candidates under the current context or condition, together with their relative plausibility. The candidates are not equally likely; some are stronger and some are weaker.
- Why it matters: LLM generation is not the retrieval of a complete sentence at once. It repeatedly creates a candidate distribution from the current context, selects an actual piece, and creates a new distribution from the updated context. This concept lets readers treat sampling, temperature, and next-token prediction as tools for reading the generation flow rather than as isolated settings.
- Related concepts: `sampling`, `next-token prediction`, `context`, `temperature`
- Core Section: `P6-1.3`
- Appears in: `P6-4.1`
