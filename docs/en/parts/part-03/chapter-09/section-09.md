# P3-9.9 How Should the Actual Target and a Proxy Target Be Distinguished

> Section ID: `P3-9.9`
> Version: `v2026.07.10`

In real data, the result you truly want to predict is often not directly visible. So it becomes tempting to use an intermediate operational judgment or a substitute column as a temporary target. The distinction needed here is between `actual target` and `proxy target`. You should first write whether the target currently in use is the result you truly want to know, or a substitute column used in its place.

| Target type | Meaning |
| --- | --- |
| Actual target | The result you truly want to know and ultimately want to reduce |
| Proxy target | A substitute column used because the actual target cannot be seen directly or is seen too late |

For example, if `confirmed failure` cannot be observed directly, `review needed` may be used first as a target candidate. But the two do not mean the same thing. A proxy target can become a starting point, but it does not automatically become the same thing as the actual target.

| Note to write first | Why it is needed |
| --- | --- |
| What is the result you really want to know? | To avoid hiding the original purpose of the problem |
| Why is the current column a proxy target? | To leave the distance and limitation relative to the actual target |
| How will it later be reconnected to the actual target? | To preserve the limitation of the proxy target and the distance back to the actual target |

A proxy target is therefore not a temporary convenient name, but a device that explicitly states that a different observable is being used in place of the original goal. The core here is to leave together `the result you truly want to know`, `the proxy column you can observe now`, and `a record of the distance between them`, so that the limitation of the proxy goal stays preserved inside the structure.

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `proxy labels`, accessed 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }

