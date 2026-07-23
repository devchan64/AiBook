# Part 2 Chapter 11 Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Python examples:
  - `p2_11_1_numpy_arrays.py`: checks array shape, ndim, dtype, and vector-matrix style weighted sums.
  - `p2_11_2_index_slice_axis.py`: compares indexing, slicing, row/column selection, and `axis=0`/`axis=1` reductions.
  - `p2_11_3_broadcast_vectorization.py`: compares scalar broadcasting, column offsets, broadcasting failure, loop calculation, and vectorized calculation.
- Current language sets:
  - `loop-to-vectorization-flow-en.mmd` / `loop-to-vectorization-flow-ko.mmd`
  - `shape-view-broadcast-flow-en.mmd` / `shape-view-broadcast-flow-ko.mmd`
