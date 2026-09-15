"""P2-5.4: run the manuscript examples in order (NumPy required)."""


def main() -> None:
    # This example imports NumPy to prepare mean, median, and variance calculations for small data.
    import numpy as np

    # data is the small score dataset used to check mean, median, and variance.
    data = np.array([42, 55, 48, 63, 52, 50, 47, 70])

    print(data)

    # size shows how many values the dataset contains.
    print(data.size)

    at_least_60 = data >= 60
    count_at_least_60 = np.count_nonzero(at_least_60)
    observed_ratio = count_at_least_60 / data.size
    print(at_least_60)
    print(count_at_least_60)
    print(observed_ratio)

    # mean_value is the mean that summarizes all values in data as one center value.
    mean_value = np.mean(data)
    print(mean_value)

    print(np.sort(data))
    print(np.median(data))

    # skewed_data includes the extreme value 100 to compare how mean and median react.
    skewed_data = np.array([10, 12, 13, 15, 100])

    print(np.mean(skewed_data))
    print(np.median(skewed_data))

    # centered shows how far each value is from the mean.
    centered = data - np.mean(data)
    print(np.round(centered, 3))

    # squared_deviations squares the deviations so both negative and positive gaps count as spread.
    squared_deviations = centered ** 2
    print(np.round(squared_deviations, 3))

    # np.var(data) summarizes the spread of data as one variance value.
    print(np.var(data))

    print(np.var(data))
    print(np.var(data, ddof=1))

    # The 12 values in population_like are the small population in this example.
    population_like = np.array([42, 45, 47, 48, 50, 52, 55, 58, 61, 63, 66, 70])

    # samples are smaller groups used as if we observed only part of population_like.
    samples = np.array([
        [42, 47, 50, 55],
        [48, 52, 63, 70],
        [45, 55, 58, 66],
    ])

    print(np.mean(population_like))

    # Check each sample in order to see whether its mean changes.
    for sample in samples:
        print(sample, np.mean(sample))

    for last_value in [1000, 14]:
        changed_data = skewed_data.copy()
        changed_data[-1] = last_value
        print(last_value, np.mean(changed_data), np.median(changed_data))


if __name__ == "__main__":
    main()
