"""P2-3.5 NumPy linear algebra examples.

Run:
    python docs/assets/part-02/chapter-03/p2_3_5_numpy_linear_algebra.py
"""

import numpy as np


def show(title, value):
    print(f"\n## {title}")
    print(value)


def main():
    x = np.array([2, 3])
    W = np.array(
        [
            [4, 1],
            [5, 2],
        ]
    )

    show("Vector x", x)
    show("x.shape", x.shape)
    show("Matrix W", W)
    show("W.shape", W.shape)

    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])

    show("Vector addition: a + b", a + b)
    show("Scalar multiplication: 2 * a", 2 * a)
    show("Element-wise multiplication: a * b", a * b)

    y = x @ W

    show("Matrix multiplication: x @ W", y)
    show("(x @ W).shape", y.shape)

    X = np.array(
        [
            [2, 3],
            [1, 4],
        ]
    )

    Y = X @ W

    show("Batch input X", X)
    show("X.shape", X.shape)
    show("Batch matrix multiplication: X @ W", Y)
    show("(X @ W).shape", Y.shape)

    bad_x = np.array([2, 3, 4])
    show("Shape mismatch example", f"bad_x.shape={bad_x.shape}, W.shape={W.shape}")
    print("bad_x @ W would fail because the input length and W's input size do not match.")


if __name__ == "__main__":
    main()
