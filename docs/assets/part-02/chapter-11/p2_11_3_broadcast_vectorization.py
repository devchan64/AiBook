import numpy as np


def show(title, value):
    print(f"\n## {title}")
    print(value)


scores = np.array([82, 75, 45])
show("scalar broadcasting: scores + 10", scores + 10)
show("scalar broadcasting: scores * 2", scores * 2)

features = np.array([
    [1.0, 0.2, 7.0],
    [0.8, 0.4, 6.5],
    [0.3, 0.9, 8.1],
    [0.5, 0.1, 5.8],
])

feature_offset = np.array([0.1, 0.2, 0.3])

show("features shape", features.shape)
show("feature_offset shape", feature_offset.shape)
show("features + feature_offset", features + feature_offset)

bad_offset = np.array([10, 20, 30, 40])
show("bad_offset shape", bad_offset.shape)

try:
    features + bad_offset
except ValueError as error:
    show("broadcasting error", error)

python_scores = [82, 75, 45]
adjusted_with_loop = []
for score in python_scores:
    adjusted_with_loop.append(score + 10)

show("Python loop result", adjusted_with_loop)
show("NumPy vectorized result", scores + 10)

column_mean = features.mean(axis=0)
centered = features - column_mean

show("column_mean", column_mean)
show("centered features", centered)
centered_mean = centered.mean(axis=0)
centered_mean = np.where(np.abs(centered_mean) < 1e-10, 0.0, centered_mean)
show("centered mean by column", centered_mean)
