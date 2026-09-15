# Part 2 Chapter 11 Assets

- Korean, English, and Simplified Chinese manuscripts include matching `-ko.mmd`, `-en.mmd`, and `-zh.mmd` files through `pymdownx.snippets`.
- Each diagram has the same data and graph structure in all three languages. Update the variants together.
- Array selection, axis reduction, shape, and broadcasting diagrams use Mermaid. Superseded SVG files are removed.
- Rendered previews are temporary validation files and are not committed.

## Python examples

- `p2_11_1_numpy_arrays.py`: shape, ndim, dtype conversion, elementwise products, matrix–vector products, and weight-order/shape checks.
- `p2_11_2_index_slice_axis.py`: indexing, slicing, axis preservation, bounds, and student/subject reductions.
- `p2_11_3_broadcast_vectorization.py`: scalar/column/row broadcasting, expected shape errors, vectorization, and centering with keepdims.
- `p2_11_4_views_shapes.py`: views, advanced-indexing copies, new axes, reshape, transpose, and memory sharing.

Run each script with Python from the repository root. NumPy is required; expected shape/index errors are caught in the examples.
