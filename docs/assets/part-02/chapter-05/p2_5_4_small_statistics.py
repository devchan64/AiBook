"""Small examples for P2-5.4.

Run:
    python docs/assets/part-02/chapter-05/p2_5_4_small_statistics.py
"""

import numpy as np


def main() -> None:
    data = np.array([42, 55, 48, 63, 52, 50, 47, 70])

    print("data:", data)
    print("count:", data.size)
    print("mean:", round(float(np.mean(data)), 3))
    print("median:", round(float(np.median(data)), 3))
    print("population variance:", round(float(np.var(data)), 3))
    print("sample variance:", round(float(np.var(data, ddof=1)), 3))

    skewed_data = np.array([10, 12, 13, 15, 100])
    print("\nskewed data:", skewed_data)
    print("skewed mean:", round(float(np.mean(skewed_data)), 3))
    print("skewed median:", round(float(np.median(skewed_data)), 3))

    centered = data - np.mean(data)
    print("centered values:", np.round(centered, 3))
    print("squared deviations:", np.round(centered**2, 3))

    population_like = np.array([42, 45, 47, 48, 50, 52, 55, 58, 61, 63, 66, 70])
    samples = np.array(
        [
            [42, 47, 50, 55],
            [48, 52, 63, 70],
            [45, 55, 58, 66],
        ]
    )

    print("\npopulation-like values:", population_like)
    print("population-like mean:", round(float(np.mean(population_like)), 3))

    for index, sample in enumerate(samples, start=1):
        print(f"sample {index}:", sample, "mean:", round(float(np.mean(sample)), 3))


if __name__ == "__main__":
    main()
