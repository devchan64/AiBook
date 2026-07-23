"""P2-11.2 NumPy indexing, slicing, and axis examples.

Run:
    python docs/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py
"""

import numpy as np


data = np.array(
    [
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        [30, 31, 32, 33],
    ]
)

print("data")
print(data)
print("shape:", data.shape)

print("\nIndexing: one value")
print("data[1, 2] =", data[1, 2])

print("\nSlicing: one row")
print("data[2, :] =", data[2, :])

print("\nSlicing: one column")
print("data[:, 3] =", data[:, 3])

print("\nSlicing: sub-array")
print("data[0:2, 1:3] =")
print(data[0:2, 1:3])

scores = np.array([82, 75, 45, 90, 61, 70])

print("\nOne-dimensional slicing")
print("scores:", scores)
print("scores[1:5] =", scores[1:5])
print("scores[1:5:2] =", scores[1:5:2])
print("scores[:3] =", scores[:3])
print("scores[-2:] =", scores[-2:])

print("\nReduction along axes")
print("data.sum(axis=0) =", data.sum(axis=0))
print("data.sum(axis=1) =", data.sum(axis=1))
print("data.mean(axis=0) =", data.mean(axis=0))
print("data.mean(axis=1) =", data.mean(axis=1))

features = np.array(
    [
        [1.0, 0.2, 7.0],
        [0.8, 0.4, 6.5],
        [0.3, 0.9, 8.1],
        [0.5, 0.1, 5.8],
    ]
)

print("\nDataset-style row and column selection")
print("features")
print(features)
print("features shape:", features.shape)
print("features[1, :] =", features[1, :])
print("features[:, 1] =", features[:, 1])
print("features[:, 1].mean() =", features[:, 1].mean())
print("features.mean(axis=0) =", features.mean(axis=0))
print("features.mean(axis=1) =", features.mean(axis=1))
print("axis=0 summarizes each column; axis=1 summarizes each row.")
