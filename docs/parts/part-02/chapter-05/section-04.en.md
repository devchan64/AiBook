# P2-5.4 Checking Probability and Statistics with Small Data

> Section ID: `P2-5.4`
> Version: `v2026.07.20`

In P2-5.1, we looked at probability as a numeric language for dealing with uncertainty. In P2-5.2, we looked at distribution, mean, and variance as tools for reading the shape of a data bundle. In P2-5.3, we looked at sample, estimation, and error as "speaking about the whole from the part."

Here we place a small list of data on the table and check mean, deviation, variance, and changes in the sample mean in order.

Rather than memorizing many statistical formulas, this Section checks how numbers and code reveal the concepts from the previous Sections.

Here we reorganize `small data`, `mean`, `median`, `variance`, and `sample mean` together with code. If 5.2 and 5.3 were about reading the concepts, this Section is about how those concepts actually appear in numbers and output.

Rather than broadly learning how to use a statistics library, this Section focuses on rechecking the basic concepts of probability and statistics with small data and code. If you visually confirm mean, variance, and changes in the sample mean here, later statistics about datasets or evaluation numbers connect naturally to the concepts instead of floating apart from them.

![Flow for checking raw data, center, spread, and sample estimation separately on small data](/AiBook/assets/part-02/chapter-05/small-data-statistics-check-en.svg)

## Core Criteria: Checking Probability and Statistics with Small Data

- You can calculate the `mean` from a small data list.
- You can distinguish `mean` from `median`.
- You can check how far each value is from the mean.
- You can explain `variance` as "the spread around the mean."
- You can explain that population variance and sample variance can use different calculation settings.
- You can confirm through code that the `sample mean` can change when the sample changes.
- You can read code output by connecting it to conceptual explanation.

## Three Criteria

| Criterion | Why it matters | Needed level of understanding here |
| --- | --- | --- |
| Code reveals concepts through numbers and output | We need to check how mean, variance, and sample mean actually appear in calculation so the concepts connect to output. | Understand that statistical concepts appear as specific calculations and outputs on small numeric data. |
| Look at mean and median together | They both talk about the center, but they respond differently when outliers exist. | Understand that mean and median are both center-related concepts but have different behavior. |
| Variance adds information about spread | The center alone cannot fully explain the character of the data. | Understand variance as a value that shows how much values are spread around the mean. |

## Execution Environment

The code in this Section uses NumPy.

Check the execution environment based on P2-3.5, [Distinguish the execution environment first](../chapter-03/section-05.md#first-separate-the-runtime-environment). Here we do not explain Python installation again, and instead focus on checking statistical concepts through small code examples.

If you use Google Colab, you can prepare NumPy in a code cell like this.

Problem situation: prepare NumPy before running the statistics examples in this Section on Colab.
Input: the `%pip install numpy` command in a notebook code cell.
Expected output: NumPy is installed into the current Colab kernel.
Concept to check: before running statistical examples, the package-preparation step is separate from the calculation step.

```python
# This command installs NumPy inside a Colab/Jupyter code cell.
%pip install numpy
```

If you use a local PC, use the following command in your own terminal.

```bash
python -m pip install numpy
```

You can also inspect the full example code of this Section in the following file.

- [p2_5_4_small_statistics.py](/AiBook/assets/part-02/chapter-05/p2_5_4_small_statistics.py)

If you run it from the project root, you can use the following command.

```bash
python docs/assets/part-02/chapter-05/p2_5_4_small_statistics.py
```

## Creating Small Data

Start the calculation from a small data list.

Problem situation: first prepare a small bundle of numeric data for checking mean and variance.
Input: the NumPy array `data` containing 8 values.
Expected output: the whole data bundle and the number of elements `8` are printed.
Concept to check: statistical calculation must always begin by checking what data bundle it is based on.

```python
# This example imports NumPy to prepare mean, median, and variance calculations for small data.
import numpy as np

# data is the small score dataset used to check mean, median, and variance.
data = np.array([42, 55, 48, 63, 52, 50, 47, 70])

print(data)

# size shows how many values the dataset contains.
print(data.size)
```

You can read the output like this.

```text
[42 55 48 63 52 50 47 70]
8
```

Here, `data` is not the whole of reality. It is the small bundle of data we observed. In the language of the previous Section, it can be read like a `sample`.

At this stage, the important questions are what these numbers record, how they were collected, and whether they can be seen as representative of the whole.

Code can perform the calculation, but a person has to decide what the data means.

## The Mean Summarizes the Center into One Number

The `mean` summarizes the center of the data into one number.

Problem situation: check what number the mean is actually calculated as in the prepared data.
Input: the array `data` created above.
Expected output: the mean value `53.375` is printed.
Concept to check: the mean is a calculation that summarizes many values into one representative number.

```python
# mean_value is the mean that summarizes all values in data as one center value.
mean_value = np.mean(data)
print(mean_value)
```

The output is `53.375`.

This number stands in for the following calculation.

\[
\frac{42 + 55 + 48 + 63 + 52 + 50 + 47 + 70}{8} = 53.375
\]

The mean is convenient, but one mean alone cannot tell you the full shape of the data. The mean shows the center, but how widely the values are spread must be checked separately.

Also, the mean can be shaken by one extremely large or small value. One representative value you can look at together in that situation is the `median`.

## The Median Is the Middle Value After Sorting

The `median` is the value that sits in the middle after sorting the values in order.

In the next data, one value is unusually large.

Problem situation: compare how mean and median respond differently when an outlier exists.
Input: the array `skewed_data` that includes the large value `100`.
Expected output: the mean `30.0` and the median `13.0` are printed.
Concept to check: the mean can be shaken by an outlier, while the median is relatively less affected.

```python
# skewed_data includes the extreme value 100 to compare how mean and median react.
skewed_data = np.array([10, 12, 13, 15, 100])

print(np.mean(skewed_data))
print(np.median(skewed_data))
```

The output is `30.0`, `13.0`.

The mean becomes `30.0` because it is strongly affected by `100`. But the median is `13.0`, the middle of the sorted values.

Because the mean calculates the center by adding all values, it can be shaken by one extremely large or small value. The median, by contrast, looks at the middle position after sorting, so it is relatively less shaken by an `outlier`.

In real data, long one-sided distributions appear often. In data like user usage time, waiting time, response latency, or income, where some values can become very large, looking only at the mean can misread what the data typically looks like.

We do not treat the median deeply here. Summary values outside the mean, such as median, standard deviation, and confidence intervals, are reorganized again in the supplementary learning of P2-5.5. Still, when you look at the mean, remember together whether the mean shows the center well, whether the mean is being dragged to one side because of an outlier, and whether interpretation changes if you also look at the median.

If mean and median let us read the center, then next we need to see how far the values spread around that center. That is why variance is needed.

## Variance Looks at How Far Values Sit from the Mean

`Variance` is the number that looks at how widely values are spread around the mean.

First, subtract the mean from each value.

Problem situation: directly check how far each datum is from the mean.
Input: the array `data` and its mean.
Expected output: the array of deviations from the mean is printed rounded to the third decimal place.
Concept to check: before looking at variance, each value can first be expressed as a deviation from the mean.

```python
# centered shows how far each value is from the mean.
centered = data - np.mean(data)
print(np.round(centered, 3))
```

You can read the output like this.

```text
[-11.375   1.625  -5.375   9.625  -1.375  -3.375  -6.375  16.625]
```

These values show how far each datum is from the mean. For example, 42 is 11.375 below the mean, 70 is 16.625 above the mean, and 55 is 1.625 above the mean.

Next, square those distances.

Problem situation: square the gaps from the mean so spread can be compared without negative signs.
Input: the deviation array `centered` calculated above.
Expected output: the array of squared deviations is printed.
Concept to check: variance follows the flow of squaring deviations rather than simply adding them as they are.

```python
# squared_deviations squares the deviations so both negative and positive gaps count as spread.
squared_deviations = centered ** 2
print(np.round(squared_deviations, 3))
```

You can read the output like this.

```text
[129.391   2.641  28.891  92.641   1.891  11.391  40.641 276.391]
```

Variance can then be seen as the value obtained by averaging these squared gaps.

Problem situation: summarize the squared deviations into one number and calculate the variance.
Input: the array `data`.
Expected output: the variance value `72.984375` is printed.
Concept to check: variance is a value that summarizes the spread around the mean into one number.

```python
# np.var(data) summarizes the spread of data as one variance value.
print(np.var(data))
```

The output is `72.984375`.

What matters here is interpretation rather than the formula. The mean looks at the center, the differences from the mean show how far each value is from the center, and the variance summarizes those distances as a whole.

## Population Variance and Sample Variance Can Use Different Settings

By default, `np.var(data)` calculates variance by treating the whole data bundle as one population. In that case, it divides by \(N\), the number of values.

But in statistics, when a sample is used to estimate population variance, people often use `sample variance`, which divides by \(N - 1\). In NumPy, you can check it by specifying `ddof=1`.

Problem situation: compare how the same data can produce different values under population-variance and sample-variance settings.
Input: the array `data` and the two `ddof` settings.
Expected output: the population variance and the sample variance are printed in order.
Concept to check: the code is not wrong; the value can change because the calculation setting changes.

```python
# ddof=1 is the setting used when calculating sample variance.
print(np.var(data))
print(np.var(data, ddof=1))
```

The outputs are `72.984375`, `83.41071428571429`.

The two values are different. This does not mean the code is wrong. It means the calculation setting changes depending on whether you view `this data` as the whole or as a sample.

| Calculation | Code | Working interpretation |
| --- | --- | --- |
| population variance | `np.var(data)` | Calculate spread by viewing this data bundle as if it were the whole. |
| sample variance | `np.var(data, ddof=1)` | Calculate by viewing this data as a sample used to estimate the spread of a population. |

Here, memorizing `ddof` matters less than first asking whether the data you have is the whole or a sample used to estimate the whole.

## If You Change the Sample, the Mean Can Change Too

This time, make one small bundle of values that behaves like a near-whole, and then pick a few different samples from inside it.

Problem situation: directly check how the sample mean changes when you draw different samples.
Input: the near-population value bundle `population_like` and the three sample arrays `samples`.
Expected output: the whole mean and each sample mean are printed in order.
Concept to check: the sample mean can change depending on sampling, and that this is the basic feel of sampling variation.

```python
# population_like is the reference dataset treated as close to the whole group.
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
```

You can read the output like this.

```text
54.75
[42 47 50 55] 48.5
[48 52 63 70] 58.25
[45 55 58 66] 56.0
```

The mean of the near-whole value bundle is `54.75`. But depending on how you draw the sample, the sample mean changes to `48.5`, `58.25`, and `56.0`.

This is a small example of the `sampling variation` discussed in P2-5.3. The whole mean is one value, but the sample mean can change depending on the sample, so the sample mean is an estimate of the whole mean.

## Code Output Is Material, Not Judgment

Code calculates mean and variance quickly. But how to interpret the numbers is a separate issue.

For example, if the mean is `53.375`, it is risky to jump straight to conclusions like "the average of all users of this service is 53.375," "this data perfectly represents the whole," or "the variance is large, so the data is bad."

A more careful wording is closer to "the mean in this data bundle is 53.375," "the values are spread to some degree around the mean," and "whether this data represents the whole must be checked together with the collection method and sample composition."

The same attitude is needed in AI data. The mean of training data is a summary value calculated inside the training dataset, the score on test data is an evaluation value obtained from the test sample, and real-world performance is something that must be checked through separate samples, post-deployment observation, and continued evaluation.

## View It Through a Case

### Case 1. Can a Small List of Scores Restore Your Feel for Mean and Variance?

Suppose a learner feels that statistical formulas make sense while reading them, but the intuition fades when actual numbers appear. In that case, rather than starting with a large dataset, it is often clearer to place one small score list on the table and directly calculate the mean, median, and variance.

For example, once you calculate the mean from eight scores, the center is compressed into one number. But as soon as you also look at the median, the gaps from the mean, the squared deviations, and the variance, it becomes clear that `center`, `outlier influence`, and `spread` are different questions.

Also, if you draw a few different samples and calculate the mean again, you can visually confirm that even in a bundle of values from something like the same population, the sample mean can wobble a little. This is the smallest experimental version of the `sampling variation` discussed in the previous Section.

This case shows why small-data practice is needed. Statistical concepts remain far less abstract when you directly change a few numbers and watch how the output changes than when you only read formulas.

## Checklist

- You can make a small data list as a NumPy `array`.
- You can calculate the `mean` with `np.mean`.
- You can calculate the `median` with `np.median`.
- You can explain that the mean can be shaken by an `outlier`.
- You can check how far each value is from the mean.
- You can calculate the `variance` with `np.var`.
- You can explain that `ddof=1` can be used in sample-variance calculation.
- You can explain that the `sample mean` can change when the sample changes.
- You can separate code output from issues of data collection method, sample representativeness, and interpretation.
- You can explain that statistical code output is the start of interpretation, not the end of judgment.

## Sources and References

- NumPy Developers, [numpy.array](https://numpy.org/doc/stable/reference/generated/numpy.array.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, checked 2026-07-20. Used to confirm the example that creates a NumPy array from a small numeric list.
- NumPy Developers, [numpy.ndarray.size](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.size.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, checked 2026-07-20. Used to confirm the `data.size` example for reading the number of array elements.
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, checked 2026-07-20. Used to confirm arithmetic mean and array-mean calculations.
- NumPy Developers, [numpy.median](https://numpy.org/doc/stable/reference/generated/numpy.median.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, checked 2026-07-20. Used to confirm that the median is the middle value of a sorted copy, or the average of the two middle values for an even number of values.
- NumPy Developers, [numpy.var](https://numpy.org/doc/stable/reference/generated/numpy.var.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, checked 2026-07-20. Used to confirm variance, `ddof`, and the difference between population-variance and sample-variance calculation settings.
- Barbara Illowsky, Susan Dean, [Introductory Statistics, 1.2 Data, Sampling, and Variation in Data and Sampling](https://openstax.org/books/introductory-statistics/pages/1-2-data-sampling-and-variation-in-data-and-sampling){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used to confirm the statistical background that samples should represent the population and that sampling methods can introduce variation.
