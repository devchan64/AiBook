# P4-19.6 Supplementary Learning: How To Read Policy Gradient And The Likelihood Ratio Trick For The First Time

> Section ID: `P4-19.6`
> Version: `v2026.07.10`

Once readers study policy-based reinforcement learning in P4-19.2, the following names quickly appear.

- policy gradient theorem
- likelihood ratio trick

Rather than following the full rigorous proof all the way to the end, this supplementary Section first reads `why a change in policy parameters connects to a change in expected reward` and `why the form of log-probability appears so often`.

## Scope Of This Section

This Section answers the following questions.

- Why is policy gradient read as directly adjusting policy probabilities?
- Why does the likelihood ratio trick connect log-probability and expected-value calculation?
- How does this sense of formulas continue into the interpretation of REINFORCE and actor-critic?

This Section focuses on building an introductory feeling for policy-based formulas through three handles: `policy probability`, `expected reward`, and `log-probability gradient`.

## Goals Of This Section

- You can explain policy gradient as `a gradient that adjusts policy probabilities in the direction that increases expected reward`.
- You can explain the likelihood ratio trick as `a device that turns differentiation inside a probability distribution into a log-probability gradient so the calculation becomes easier to read`.
- You can describe why forms such as `log pi(a|s)` appear in REINFORCE and actor-critic.

## Why This Section Is Needed

Policy-based reinforcement learning is easy to follow as intuitive sentences, but once the formulas appear, it suddenly feels unfamiliar.

- Why does a log appear when differentiating expected reward?
- Why is the gradient of an action probability multiplied by reward?

That is exactly where the likelihood ratio trick appears.

So the core of this Section is to connect for the first time how the sentence `directly adjust the policy` becomes the formula reading `gradient of the log-probability`.

## What Is Policy Gradient Differentiating?

Policy-based reinforcement learning ultimately carries the following question.

`If the policy parameters change slightly, in what direction does long-term expected reward become larger?`

So, in a very short sentence, policy gradient is:

`the gradient for moving policy parameters in the direction that increases expected reward`

At an introductory level, it is enough to hold on to the following.

| Reading question | What policy gradient says |
| --- | --- |
| What is changing? | Policy parameters |
| Why change them? | To make expected reward larger |
| What signal is used? | Move in a direction where actions with good reward happen more often and actions with bad reward happen less often |

So policy gradient is best read as `an update that directly fine-tunes the policy distribution`.

## Why Does The Likelihood Ratio Trick Appear?

When a probability distribution sits inside an expectation, differentiation becomes awkward. The likelihood ratio trick is a standard transformation used at that point.

The core feeling is captured by one sentence.

`Instead of differentiating the probability directly, change it into the gradient of the log-probability, and the expression becomes easier to read inside the expectation.`

If only the form is written very briefly, it looks like this.

```text
grad p(x) = p(x) * grad log p(x)
```

The role of this expression is to `make a derivative of a probability distribution inside an expectation easier to connect to sample-based updates`.

So the reason a log appears is not decoration. It is to change the computational structure itself.

## Then How Should The REINFORCE Formula Be Read?

The REINFORCE intuition is usually read in a form like this.

`Strengthen the log-probability gradient of actions that gave good reward, and weaken the gradient of actions that gave bad reward.`

At an introductory level, the following comparison is the most important.

| The reward was good | The reward was bad |
| --- | --- |
| Adjust in the direction that makes that action appear more often again | Adjust in the direction that makes that action appear less often |
| The gradient of `log pi(a|s)` is used as a strengthening signal | The same gradient can act in the opposite direction as a weakening signal |

At this point, the likelihood ratio trick is the bridge that explains `why such an update is written in a log-probability form`.

## How Does This Continue Into Actor-Critic?

In P4-19.2, actor-critic was introduced as a structure that directly adjusts the policy while the critic provides a more stable evaluation signal. If this is read through formula intuition, it looks like this.

- actor: still adjusts by following the gradient of the policy's log-probability
- critic: provides a less noisy evaluation signal for how good an action was

So actor-critic does not abandon policy gradient. It can be read as `a direction that makes the evaluation signal multiplied onto that gradient more stable`.

## Cases And Examples

### Case 1. When You Want Good Ad-Display Ratios To Appear More Often And Bad Ones Less Often

Suppose an ad-display policy chooses ratios probabilistically, such as `discount banner 70% / recommendation banner 30%`. If raising the share of recommendation banners in a certain state leads to more long-term purchases after the click, the policy will want to increase that probability a bit more in that direction. On the other hand, if immediate clicks rise but refunds and churn also rise, then the probability of that action should move downward. Policy gradient can be read exactly as this adjustment problem: `raise good probabilities and lower bad ones`.

## What To Remember From This Section

- Policy gradient is the gradient that moves policy parameters in the direction of increasing expected reward.
- The likelihood ratio trick makes probability differentiation easier to read by turning it into a log-probability gradient.
- Both REINFORCE and actor-critic can be read on top of this same log-probability gradient intuition.
