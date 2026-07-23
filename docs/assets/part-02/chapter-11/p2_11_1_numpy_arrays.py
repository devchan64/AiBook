"""P2-11.1 NumPy array examples.

Run:
    python docs/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py
"""

import numpy as np


def show(name, value):
    print(f"\n{name}")
    print(value)
    print("shape:", value.shape)
    print("ndim:", value.ndim)
    print("dtype:", value.dtype)


vector = np.array([0.12, -0.03, 0.44, 0.18])

matrix = np.array(
    [
        [82, 75, 45],
        [90, 61, 70],
    ]
)

features = np.array(
    [
        [1.0, 0.2],
        [0.8, 0.4],
        [0.3, 0.9],
    ]
)

weights = np.array([0.6, 0.4])

show("vector", vector)
show("matrix", matrix)
show("features", features)
show("weights", weights)

scores = features @ weights

show("scores = features @ weights", scores)
print("features.shape and weights.shape line up as (3, 2) @ (2,) -> (3,).")

print("\nfirst row:", features[0])
print("second column:", features[:, 1])
print("mean score:", scores.mean())

python_scores = [82, 75, 45]
numpy_scores = np.array([82, 75, 45])

print("\nPython list + Python list")
print(python_scores + python_scores)

print("\nNumPy array + NumPy array")
print(numpy_scores + numpy_scores)

print("\nElement-wise NumPy operations")
print("numpy_scores * 2:", numpy_scores * 2)
print("numpy_scores.mean():", numpy_scores.mean())
