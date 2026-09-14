"""P2-3.6: vector comparisons and input/output shapes with NumPy.

Run from the repository root:
    python docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py
Change candidates["a"] or add a row to X to compare the outputs.
"""

import numpy as np

x = np.array([2, 3])
W = np.array([[4, 1], [5, 2]])
print(x.shape)
print(W.shape)
print(x @ W)

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)
print(2 * a)
print(a * b)
print(a @ b)

q = np.array([1, 1])
candidates = {
    "a": np.array([2, 2]),
    "b": np.array([1, 0]),
    "c": np.array([10, 10]),
}
for name, v in candidates.items():
    dot = q @ v
    norm = np.linalg.norm(v)
    distance = np.linalg.norm(v - q)
    cosine = dot / (np.linalg.norm(q) * norm)
    print(f"{name}: dot={dot}, norm={norm:.3f}, "
          f"distance={distance:.3f}, cosine={cosine:.3f}")

X = np.array([
    [2, 3],
    [1, 4],
    [0, 1],
])
W = np.array([
    [4, 1, 1, 0],
    [5, 2, 0, 1],
])
Y = X @ W
print(X.shape, W.shape, Y.shape)
print(Y)

bad_x = np.array([2, 3, 4])
try:
    bad_x @ W
except ValueError:
    print("ValueError: input components = 3, weight rows = 2")

W_fixed = np.vstack([W, [1, 0, 0, 1]])
print(W_fixed.shape)
print(bad_x @ W_fixed)
