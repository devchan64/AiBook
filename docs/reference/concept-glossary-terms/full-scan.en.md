<a id="full-scan"></a>

## full scan

- Meaning: A full scan compares every candidate vector without skipping any candidates in order to find the nearest items.
- Why it matters: Full scan is simple and safe when candidate count is small, but comparison cost and latency grow as candidate count grows. It helps readers understand ANN as a tradeoff for reducing full-comparison cost, not as careless search.
- Related concepts: `nearest neighbor`, `ANN, approximate nearest neighbor`, `recall`
- Core Section: `P6-3.4`
- Appears in: `P6-3.4`

