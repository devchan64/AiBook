# P2-5.5 Supplemental Learning: How to First Read Standard Deviation, Correlation, and Confidence Intervals

> Section ID: `P2-5.5`
> Version: `v2026.07.26`

If you read from P2-5.1 through P2-5.4, you can build the basic feel for probability, mean, variance, sample, estimation, and error. But once you start reading real statistics documents or machine-learning books, more unfamiliar names quickly follow.

- standard deviation
- covariance
- correlation coefficient
- standard error
- confidence interval
- hypothesis testing

This supplemental learning does not focus on calculating every one of these concepts. It focuses on connecting what additional thing each name is trying to see.

Here we cover a slow recovery flow for first reading `supplemental learning`, `standard deviation`, `correlation coefficient`, `standard error`, and `confidence interval`. If 5.1 through 5.4 established the main flow of probability and basic statistics, this Section more slowly organizes the differences in role among statistical terms that will appear often later.

Rather than fully mastering statistical testing procedures, this Section focuses on supplemental learning that lets you first read the statistical terms you will repeatedly meet later. If you distinguish the roles of standard error, confidence interval, and hypothesis testing here, then later experiment tables or evaluation reports will not break the reading flow simply because of unfamiliar words.

## First Reading Criteria: How to First Read Standard Deviation, Correlation, and Confidence Intervals

- You can explain standard deviation as the square root of variance and as a value that reads spread in a way closer to the original unit.
- You can explain covariance as a directional feel for how two values move together.
- You can explain the correlation coefficient as a degree of joint movement that is easier to compare than covariance.
- You can explain standard error as a value that shows how much the sample mean may wobble.
- You can explain confidence interval as a way of showing an uncertain range together with an estimate.
- You can explain hypothesis testing as a procedure that tries to distinguish `a visible difference` from `a difference that is hard to treat as chance alone`.

## A Criterion to Hold First

The first criterion to hold in this supplemental learning is that `each term looks at a different question`.

| Term | Question to hold first right now |
| --- | --- |
| standard deviation | How widely are values spread around the mean? |
| correlation coefficient | Can we compare the degree to which two things move together? |
| standard error | How much can an estimate like a sample mean wobble? |
| confidence interval | What range should be stated together instead of only one estimate? |
| hypothesis testing | Can the difference we currently see be treated as chance alone? |

In other words, this Section is not about adding more formulas. It is a Section that makes us read `spread`, `joint movement`, `wobble in estimation`, and `difference interpretation` as separate things.

## Three Criteria

| Criterion | Why it matters | Needed level of understanding here |
| --- | --- | --- |
| See why more is needed after mean and variance | We need to know what reinforcing concepts appear when one number is not enough. | Understand that standard deviation, correlation, standard error, and confidence interval handle questions outside mean and variance. |
| Distinguish the question each term looks at | Spread, joint movement, wobble in estimation, and interpretation of difference are different problems. | Understand that you are reading by distinguishing what each term is trying to see more of. |
| Look at role and interpretation before formulas | In later experiment tables and evaluation reports, interpretation is needed before calculation. | Understand at a level where you can explain the difference in role even without memorizing every formula. |

## First Secure the Big Map

All these concepts appear when `one number is no longer enough`.

| Name | Question to read first |
| --- | --- |
| standard deviation | How widely is it spread around the mean? |
| covariance | Do two values move in the same direction? |
| correlation coefficient | Can the degree of joint movement be read in a comparable way? |
| standard error | If we change the sample, how much does the mean estimate wobble? |
| confidence interval | Instead of stating only one estimate, what range should be stated together? |
| hypothesis testing | Is the difference we see now hard to explain by chance alone? |

So this supplemental learning is a Section that organizes `what we begin to look at beyond mean and variance`.

If we rewrite this big map in a more practical form, it becomes the following.

| What appears in an experiment table | First way to read it |
| --- | --- |
| a `±` value next to a mean | First distinguish whether it is spread or estimation wobble |
| a numeric relationship between two variables | First distinguish whether it is correlation or a causal explanation |
| a range notation | Read it as a device for not ending with a single estimate |
| the phrase `significant` | View it as a procedure for reading the difference more carefully |

## Standard Deviation Makes Variance Easier to Read Again

In P2-5.2, we saw `variance` as a value that looks at spread around the mean. But because variance is the average of squared differences, its unit can be read in a squared form.

For example, if the data unit is `score`, `second`, or `won`, variance may not immediately feel intuitive in that unit. That is why `standard deviation` appears together with it.

Here we understand variance as a value convenient for calculating spread, and standard deviation as a value that reads that spread in a way closer to the original feel of the data scale.

So standard deviation is not `a new concept competing with variance`. It is `a companion concept that reads variance from another angle`.

## Covariance Looks at the Direction of Joint Movement

If mean and variance looked at the center and spread of one value, `covariance` looks at the direction in which two values move together.

For example, suppose we look at advertising cost and click count together.

- As advertising cost increases, does click count also increase?
- As advertising cost increases, does click count instead decrease?
- Is there no clear joint movement between the two?

Covariance opens these questions.

Here we first look at the following distinction.

| Covariance feel | Meaning |
| --- | --- |
| positive direction | the two generally move in the same direction |
| negative direction | when one grows, the other tends to shrink |
| close to 0 | clear joint movement may be weak |

For now, the sense of `joint movement of two variables` matters more than the formula.

## Correlation Coefficient Makes Joint Movement Easier to Compare

Covariance is useful, but because of the effects of unit and scale, it may be hard to compare directly across different pairs of data. That is why the `correlation coefficient` appears often.

Here we understand that if covariance gives a feel for direction, the correlation coefficient is a value that expresses that joint movement on a scale that is easier to compare.

In other words, the correlation coefficient often appears when we want to compare `how related two things seem to be`.

But when people see a correlation coefficient, they easily jump straight to `cause`. We need to be careful here.

That is, saying there is correlation means joint movement appears. It does not mean we can immediately conclude causation.

## Standard Error Looks at the Wobble of the Sample Mean

In P2-5.3, we saw that if the sample changes, the estimate can change too. `Standard error` connects directly to that feel of wobble.

Here we understand that if standard deviation looks at the spread of the raw data values, standard error looks at how much an estimate like the sample mean can wobble.

So standard error is closer to the question `how unstable can the estimate be?` than to `are the data spread out?`

If you distinguish this difference, the following becomes less confusing.

| Name | What it looks at first |
| --- | --- |
| standard deviation | the spread of the data values themselves |
| standard error | the wobble of the estimate |

## Confidence Interval Stops Us from Stating Only One Estimate

Suppose the sample mean came out as 53.4. Saying only that number is neat, but we already saw that if the sample changes, the value can change too. That is why `confidence interval` appears.

Here we understand it as a way of presenting not only one estimate but also the range within which that value should be read.

This concept reveals more honestly that `we do not know the whole exactly; we are estimating it from a sample`.

For now, the next questions matter more than calculation.

- If we look at only one estimate, are we speaking too definitively?
- If we also show a range, do we express uncertainty better?

## Hypothesis Testing Asks Whether the Difference Is Explained by Chance Alone

When the means of two groups look a little different, `hypothesis testing` is the procedure that asks whether the difference is merely sample chance or whether it is a difference worth treating as more meaningful.

Here we summarize it in one sentence as a procedure that examines whether the visible difference can be fully produced just by the accidental wobble of samples.

So hypothesis testing is not a device that instantly declares `difference / no difference`. It is a procedure that asks `can this difference be seen as chance alone?`

At this stage, the following distinction matters more than calculating p-values.

- a small difference seems visible
- whether we have enough basis to trust that difference is a separate question

## Why These Concepts Reappear in AI

The concepts in this supplemental learning continue to reappear in the contexts of P3-6 metrics, P3-7 preprocessing and features, P3-8 model selection, P3-9 experiment comparison and tuning, and project validation in Part 6.

| Concept | Scene where it reappears later |
| --- | --- |
| standard deviation | feature scale, normalization, interpretation of distribution spread |
| correlation coefficient | exploration of variable relationships, feature analysis |
| standard error, confidence interval | interpretation of evaluation results, experiment comparison, report reading |
| hypothesis testing | experiment comparison, A/B testing, interpretation of performance differences |

So the goal now is not to become a calculation expert, but to build the footing for reading the statistical expressions that appear later.

## View It Through a Case

### Case 1. Why Do Confidence Intervals and Correlation Coefficients Suddenly Appear Together in an Experiment Table?

Suppose a learner is reading a machine-learning experiment report or a table in a paper and suddenly meets a place where words like `standard deviation`, `confidence interval`, and `correlation coefficient` are all attached at once beside a mean score. At the stage where only the mean was being read, all of these terms can feel like brand-new calculations.

But once you divide the questions, the roles become visible. Standard deviation asks how widely the results are spread around the mean, the correlation coefficient asks whether there is a degree of joint movement between two values, and the confidence interval asks not to end with only one estimate but to also show what range should be read together with it.

This case clearly shows the purpose of the supplemental learning. The goal here is not to calculate every formula. It is to be able to classify, when these words appear later, whether `this value is trying to look at spread`, `joint movement`, or `wobble in estimation`.

In other words, this Section provides a map of terms for reading statistical documents without getting stuck. Once you secure what you start to look at beyond mean and variance, the experiment comparisons and evaluation interpretation after Part 3 become much less unfamiliar.

## Questions to Ask Again When You Get Stuck

| Stuck scene | Question to ask again |
| --- | --- |
| a small number is attached next to a mean | Is this data spread, or estimation wobble? |
| the correlation coefficient is high | Is this joint movement, or cause? |
| the confidence interval is wide | Is the range of wobble in estimation large? |
| it says the difference is significant | Is it saying the difference is hard to see as chance alone? |

## Checklist

- Can you explain standard deviation by connecting it to variance?
- Can you explain covariance as the direction of joint movement of two values?
- Can you explain the correlation coefficient as a degree of joint movement that is easier to compare than covariance?
- Can you explain standard error by connecting it to the wobble of an estimate?
- Can you explain confidence interval as a way of showing the range of estimation together?
- Can you explain hypothesis testing as a procedure that makes interpretation of differences more careful?
- Can you classify first whether the value you need now is about spread, joint movement, or wobble in estimation when mean and variance are no longer enough?
- Can you distinguish the impression that there seems to be a difference from the question of how much that difference should be trusted?

## Sources and References

- Barbara Illowsky, Susan Dean, [Introductory Statistics, 2.7 Measures of the Spread of the Data](https://openstax.org/books/introductory-statistics/pages/2-7-measures-of-the-spread-of-the-data){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used to confirm that standard deviation measures how far data values are from their mean, is the square root of variance, and connects spread back to the original data unit.
- NIST/SEMATECH, [Dataplot Reference: CORRELATION](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/correlat.htm){: target="_blank" rel="noopener noreferrer" }, NIST, checked 2026-07-20. Used as support for joint movement and correlation-coefficient interpretation through the cross-deviation term \(S_{xy}\) and the correlation formula.
- Barbara Illowsky, Susan Dean, [Introductory Statistics, 7.1 The Central Limit Theorem for Sample Means](https://openstax.org/books/introductory-statistics/pages/7-1-the-central-limit-theorem-for-sample-means-averages){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used as support for sampling distributions of sample means and standard error as a description of how far sample means tend to fall from the population mean in repeated samples.
- Barbara Illowsky, Susan Dean, [Introductory Statistics, 8 Introduction](https://openstax.org/books/introductory-statistics/pages/8-introduction){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used to confirm point estimates, interval estimates, confidence intervals, and margin of error as devices that prevent interpretation from ending with one estimate.
- Barbara Illowsky, Susan Dean, [Introductory Statistics, 9 Introduction](https://openstax.org/books/introductory-statistics/pages/9-introduction){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used to confirm hypothesis testing as a procedure that evaluates sample data and decides whether there is sufficient evidence to reject the null hypothesis.
- Barbara Illowsky, Susan Dean, [Introductory Statistics 2e, 12.4 Testing the Significance of the Correlation Coefficient](https://openstax.org/books/introductory-statistics-2e/pages/12-4-testing-the-significance-of-the-correlation-coefficient){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used to confirm that the correlation coefficient describes strength and direction of a linear relationship, while reliability must be read together with sample size.
