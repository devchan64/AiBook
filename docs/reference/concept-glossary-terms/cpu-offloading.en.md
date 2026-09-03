<a id="cpu-offloading"></a>

## CPU offloading

- Meaning: CPU offloading is a memory management strategy that keeps model parts or weights outside GPU VRAM when they are not immediately needed, then moves them to the GPU at execution time.
- Why it matters: It helps separate the question of whether a large model can run on limited GPU memory from the question of whether the generated output is good. CPU offloading can reduce out-of-memory failures, but it does not directly improve prompt following, pose control, or output quality.
- Related concepts: `computational limit`, `tensor`, `inference`, `open-weight model`
- Core Section: `P6-21.2`
- Appears in: `P7-5.1`, `P7-5.3`, `P7-5.5`, `P7-5.11`
