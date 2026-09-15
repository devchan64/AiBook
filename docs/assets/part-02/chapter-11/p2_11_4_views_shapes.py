"""P2-11.4 Views, copies, new axes, reshape, and transpose.

Run:
    python docs/assets/part-02/chapter-11/p2_11_4_views_shapes.py
"""

import numpy as np

scores = np.array([82, 75, 45, 90, 61])
middle = scores[1:4]

middle[0] = 999

print(scores)
print(middle)


scores = np.array([82, 75, 45, 90, 61])

picked = scores[[1, 3, 4]]
high_scores = scores[scores >= 80]

picked[0] = 500
high_scores[0] = 700

print(scores)
print(picked)
print(high_scores)


scores = np.array([82, 75, 45])

print(scores.shape)
print(scores[:, np.newaxis].shape)
print(scores[np.newaxis, :].shape)


a = np.array([10, 20, 30])
b = np.array([1, 2])

diff = a[:, np.newaxis] - b[np.newaxis, :]

print(a[:, np.newaxis].shape)
print(b[np.newaxis, :].shape)
print(diff)


matrix = np.array([[10, 11, 12], [20, 21, 22]])
print(matrix.reshape(3, 2))
print(matrix.T)


matrix = np.array([[10, 11, 12], [20, 21, 22]])
reshaped = matrix.reshape(3, 2)
transposed_flat = matrix.T.reshape(-1)

print(np.shares_memory(matrix, reshaped))
print(np.shares_memory(matrix, transposed_flat))


scores = np.array([82, 75, 45, 90, 61])
adjusted = scores[1:4].copy()
adjusted += 10

print(scores)
print(adjusted)
