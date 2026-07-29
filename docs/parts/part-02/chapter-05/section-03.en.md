# P2-5.3 Sample, Estimation, and Error

> Section ID: `P2-5.3`
> Version: `v2026.07.26`

In P2-5.2, we looked at the shape of a data bundle as a distribution, its center as the mean, and its spread as the variance. Now we shift the question one step.

What if we cannot see all the data? Can we say something about the whole from only part of it? And how likely is that statement to be wrong?

This is where `sample`, `estimation`, and `error` appear.

Here we reorganize `population`, `sample`, `estimation`, `error`, and `sampling bias`. If 5.2 was about reading the shape and center of a data bundle, this Section is about the limits that appear when the data we have is only part of the whole.

| Term | English | Core question |
| --- | --- | --- |
| population | population | What is the whole we want to know? |
| sample | sample | What is the part we actually observed? |
| estimation | estimation | How do we guess a value about the whole from the part? |
| error | error | How far might that guess be from reality? |

This flow is also very important in AI. A model never sees the whole of reality. The dataset we have is always only part of reality. So AI training continually carries the question, "How well can we speak about the whole situation from partial data?"

Rather than calculating formal formulas for statistical inference in detail, this Section focuses on reading the limits and errors that appear when we talk about the whole from partial data. If you secure the relationship among population, sample, estimation, and error here, you can read later topics like generalization, evaluation scores, and dataset bias much more carefully and accurately.

## Core Criteria: Sample, Estimation, and Error

- You can explain `population` as the whole target of interest.
- You can explain `sample` as the part actually observed from the population.
- You can explain `estimation` as calculating a value about the population from the sample.
- You can explain the gap between an estimate and the true value as `error`.
- You can explain that estimates may change when the sample changes.
- You can distinguish `sampling bias` from `random variation`.
- You can explain that AI training data is not the whole of reality but a sample.

## Three Criteria

| Criterion | Why it matters | Needed level of understanding here |
| --- | --- | --- |
| Distinguish population and sample | If you do not separate the whole from the part, it becomes unclear what the data represents. | Understand population as the whole and sample as the part that actually came into hand. |
| Estimation means speaking about the whole from the part | Guessing the property of the whole from the sample is the basic action of statistics and evaluation. | Understand estimation as cautiously speaking about the property of the whole after looking at the part. |
| See that a dataset is also a sample | Machine learning learns on collected partial data, not on the whole of reality. | Understand that a dataset is not the whole of reality but a sample. |

## A Population Is the Whole Target of Interest

The population is the whole target we want to know about.

For example, consider the following questions.

- What is the average usage time of all users of a certain service?
- What is the average math score of all high school students in the country?
- What is the repurchase rate among all buyers of a certain product?
- What proportion of all real-world incoming images contain pedestrians?

In these questions, the entire target of interest is the population. All users, all high school students in the country, all buyers, and all real-world incoming images can each become a population.

The problem is that we often cannot observe the whole population. The cost may be too high, it may take too long, the data may belong to the future and not exist yet, or the real world may keep changing.

So we need a sample.

## A Sample Is the Part Actually Observed

A sample is the part actually observed from the population. For example, logs from 10,000 users out of all users, 2,000 survey participants out of all high school students in the country, buyers who answered a survey out of all buyers, and a collected bundle of training images out of real-world images can all be examples of samples.

A sample is not the whole. If the sample represents the population well, that sample becomes a basis for estimating the properties of the whole.

The diagram below first shows the containment relationship between population and sample. A sample is not a separate world standing beside the population. It is the part actually observed from the population. A dataset can be seen as the result of organizing that observed sample into files, tables, or records.

```mermaid
--8<-- "assets/part-02/chapter-05/population-sample-dataset-flow-en.mmd"
```

The chart below shows the flow of drawing a sample from the whole population and then producing an estimate from that sample.

![Flow of drawing a sample from a population and producing an estimate from the sample](/AiBook/assets/part-02/chapter-05/population-sample-estimate-en.svg)

The most important question when looking at a sample is, "Does this sample represent the whole well?" So you should also examine whether the sample is too small, whether a specific group is included too heavily, whether any group is missing, and whether the collection method caused certain values to drop out.

If the sample does not represent the whole well, the estimate calculated from that sample can become unstable or skewed to one side.

## Estimation Means Speaking about the Whole from the Part

Estimation is the act of using a sample to calculate a value about the population.

For example, suppose you want to know the average usage time of all users of a service, but you cannot see all users. Instead, you draw logs from 10,000 users as a sample and compute the average. In that case, the value you want to know in the population is the average usage time of all users, the data you actually have is the usage time of the sampled 10,000 users, and estimation means using the sample mean to guess the population mean.

In statistics, the actual property of a population is often called a `parameter`, and the value calculated from a sample is often called a `statistic`.

| Category | English | Working explanation |
| --- | --- | --- |
| parameter | parameter | the actual property of the whole population |
| statistic | statistic | a value calculated from the sample |
| estimate | estimate | a value calculated to guess the parameter |

In AI contexts, the word `parameter` is also often used to mean a model parameter. So here we have to distinguish the statistical `parameter` from a model `parameter`. A statistical `parameter` means an actual property of the population, while a model `parameter` means a numeric value the model adjusts through learning.

The same English word can mean different things when the context changes.

## Error Is the Gap Between the Estimate and the True Value

Error is the difference between an estimate and the true value. For example, if the true overall mean is 50 and the mean estimated from the sample is 47, then the error is `-3`.

In the real world, we often do not know the true overall value. So we cannot always know the error exactly. But we still have to acknowledge that error may exist.

The chart below shows the flow of viewing the difference between the estimate and the true value as error.

![Chart showing the difference between the estimate and the true value as error](/AiBook/assets/part-02/chapter-05/estimate-error-gap-en.svg)

It is a mistake to understand error only as "failure." In statistics, error is the language that acknowledges the unavoidable gap that appears when we talk about the whole from the part. In other words, as long as we estimate from a sample, we cannot know the whole perfectly, a gap may appear, and we treat that gap as error.

The prediction error of an AI model can be viewed from a similar perspective. If the model's prediction and the actual value differ, error appears. In training, we transform this error into loss and try to reduce it.

## Estimate Also Changes When the Sample Changes

If we draw samples from the same population multiple times, we may not get the same sample every time. Then the sample mean can also change a little each time.

For example, even if the true average usage time of all users is 50 minutes, one sample may give 48 minutes, another may give 52, and another may give 49.

This difference is `sampling variation`. As long as we use samples, estimates contain this kind of variation.

The chart below shows that if you draw multiple samples from the same population, the estimate can fluctuate around the true value. This fluctuation is a natural issue that appears whenever you use samples.

![Chart comparing sampling variation and sampling bias](/AiBook/assets/part-02/chapter-05/sampling-variation-vs-bias-en.svg)

What matters is the point that "if the sample changes, the estimate can also change." You need this sense to read model evaluation results carefully too. A single evaluation score may not be an absolute truth, and a different test sample may produce a different score. If you can evaluate multiple times, you should look at the mean together with the variability.

## Sampling Bias Is More Dangerous

We need to distinguish natural fluctuation caused by a changing sample from the problem where the sample is skewed from the start.

Sampling bias is a state in which the sample does not represent the population well. For example, if only younger users were heavily collected, if data from only one region was gathered, if only people who responded were included in survey data, or if only successful cases remained in the logs, then you should suspect sampling bias.

If you estimate the whole from such a sample, the result can become systematically distorted. Random variation is the natural fluctuation that appears when drawing samples, while sampling bias is a problem skewed in a particular direction because of the collection method.

In AI, sampling bias is very important. If training data is skewed toward a certain group, situation, language, or device environment, the model can also become skewed in that direction.

Sampling variation and sampling bias both shake estimation, but their character is different.

| Category | English | Meaning | Response perspective |
| --- | --- | --- | --- |
| sampling variation | sampling variation | natural fluctuation that appears when drawing samples | more samples, repeated evaluation, checking variability |
| sampling bias | sampling bias | a problem where the sample is skewed because of the collection method | inspect the collection process, check missing groups, review data composition |

## A Dataset Is an Organized Form of a Sample

A dataset does not simply mean "a lot of data collected." In AI training contexts, it usually means a bundle that organizes collected samples so a model can read them. In other words, once we observe reality, record the needed fields, and organize them into files, tables, image folders, or label files, they become a dataset usable for training or evaluation.

A dataset is not the whole of reality. A dataset is affected by the time of collection, the collection method, the recording format, the cleaning standard, and the labeling standard. So when you look at a dataset, you should ask together what is being treated as the population, how the sample was collected, whether there are missing groups or situations, what standard the labels follow, and how the data for training and the data for evaluation were separated.

This perspective becomes the basis for understanding later topics such as dataset preparation, labels, training data, and test data.

## Training Data Is Also a Sample of Reality

AI training data is not the whole of reality. It is a sample collected from reality. For example, the total behavior of all real-world users is closer to the population, the collected log data is the sample, and the training dataset is the sample the model actually sees.

So even if the model shows good performance on training data, you cannot immediately say it will always work well across the whole real world. Performing well on training data means it works well on that sample, and whether it also works well on new real-world data must be checked separately.

This problem leads into the larger machine-learning theme of `generalization`.

The diagram below shows the flow in which part of the real world is collected into a dataset, and that dataset is then divided again into training data and test data.

```mermaid
--8<-- "assets/part-02/chapter-05/dataset-train-test-flow-en.mmd"
```

## Why Keep Test Data Separate?

The reason we keep `test data` separate when evaluating a model can also be viewed through the perspective of sample and estimation.

A model can show good performance on training data even if it merely memorizes the training data. So we check the model on data that was not used for learning. In other words, the training data is the sample the model learns from, and the test data is a separate sample used to check the model.

Test performance is also an estimate of real-world performance. If the test data is not representative enough, the evaluation result can become unstable or miss real-world performance. A test score is an estimate of real-world performance, and the composition of the test data affects the reliability of that estimate.

This perspective becomes the basis for understanding later topics such as train/test split, validation data, and cross-validation.

## View It Through a Case

### Case 1. Can You Speak about All Users from Logs of 10,000 App Users?

Suppose a service team wants to understand the behavior of all users, but in reality it has only logs from 10,000 recent users. Even if 10,000 logs feel like a lot, you still cannot simply conclude that all user behavior is the same.

But from a statistical perspective, those logs from 10,000 users are also a `sample` of all users. You can calculate average usage time or churn rate from that sample, but the value is not the true value of the `population`. It is an `estimate`. If you draw a different sample, the result may change a little.

The bigger problem is sampling bias. For example, if the sample includes too many new users, or if logs from users in one region are collected much more heavily, the calculated result can systematically misrepresent overall user behavior. In that case, the issue goes beyond scores merely fluctuating. The sample itself is skewed to one side.

This case shows that AI datasets should also be read not as `the whole of reality` but as `a collected sample`. Training data and test data are also samples in the end, so model-performance numbers should be interpreted not as complete proof of real-world performance but as estimates calculated from samples.

## Checklist

- You can explain `population` as the whole target of interest.
- You can explain `sample` as the part actually observed from the population.
- You can explain `estimation` as guessing a value about the population from the sample.
- You can distinguish the statistical `parameter` from the `model parameter`.
- You can explain `error` as the gap between the estimate and the true value.
- You can distinguish `sampling variation` from `sampling bias`.
- You can explain `training data` and `test data` as samples of the whole real world.
- You can read model evaluation scores carefully as estimates of real-world performance.
- You can explain a dataset again by separating population and sample instead of treating it as the whole of reality.

## Sources and References

- Barbara Illowsky, Susan Dean, [Introductory Statistics, 1.2 Data, Sampling, and Variation in Data and Sampling](https://openstax.org/books/introductory-statistics/pages/1-2-data-sampling-and-variation-in-data-and-sampling){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used to confirm that samples are used when gathering information about an entire population is too costly or nearly impossible, and that a sample should share the characteristics of the population it represents.
- Barbara Illowsky, Susan Dean, [Introductory Statistics, 7 Introduction](https://openstax.org/books/introductory-statistics/pages/7-introduction){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used to confirm the context in which repeated sample means are read by their center and spread and connect to the central limit theorem.
- Barbara Illowsky, Susan Dean, [Introductory Statistics, 7.1 The Central Limit Theorem for Sample Means](https://openstax.org/books/introductory-statistics/pages/7-1-the-central-limit-theorem-for-sample-means-averages){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used as support for sample-mean sampling distributions, standard error, and how far sample means tend to fall from a population mean in repeated samples.
