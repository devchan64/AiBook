# P4-19.6 Supplementary Learning: How To Read Policy Gradient And The Likelihood Ratio Trick For The First Time

> Section ID: `P4-19.6`
> Version: `v2026.07.12`

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

Suppose an ad-display policy chooses ratios probabilistically, such as `discount banner 70% / recommendation banner 30%`. The first human-friendly rule is usually something like `keep using the banner mix that worked well this time more often next time`.

That intuition points in the right direction, but it quickly becomes blurry once formulas appear. Questions like `why are we changing probabilities directly?`, `why does log-probability appear?`, and `why can the same action move in opposite directions depending on the reward sign?` appear immediately. Policy gradient and the likelihood ratio trick connect that point by turning the intuition `raise good probabilities and lower bad ones` into a readable formula.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-6-mermaid-01-en.mmd"
```

| Problem scene | The first human-friendly rule | The limit that appears soon | The interpretation this Section adds |
| --- | --- | --- | --- |
| A higher share of recommendation banners increased long-term purchases | Use that ratio more often next time | It is still unclear how to describe the probability update in calculation | Read it as a policy gradient that moves in the direction of increasing expected reward |
| Clicks rose, but refunds and churn rose too | Reduce that ratio | It becomes hard to explain with formulas why the same action now receives an opposite signal | Read it through the reward sign and the gradient of log-probability |
| The formula contains `log pi(a|s)` | It looks like difficult mathematical decoration | The link between probability differentiation and sample-based update is still missing | Read it through the likelihood ratio trick |

The checkable result of this case is whether the sentence `good ratios should appear more often, and bad ratios less often` can now be reread through three handles: `expected reward`, `log-probability gradient`, and `reward sign`. In other words, the formulas should not erase the policy-based intuition. They should make that intuition more precise.

## Practice And Example

This exercise focuses on reading directly, with small numbers, `good reward -> strengthen the probability of the chosen action`, `bad reward -> weaken it`, and `why log-probability appears together`.

Problem situation:

- policy gradient and the likelihood ratio trick may sound abstract by name, but in practice they are devices for calculating which direction the probability of the chosen action should be pushed

Input:

- probability of the chosen action `0.7`
- log-probability `log(0.7)`
- a positive reward and a negative reward for the same action

Expected output:

- the value of the log-probability
- the direction of interpretation that changes with the sign of the reward

Concepts to check:

- log-probability is a reading device that connects the chosen-action probability to the update calculation
- if the reward sign changes, the adjustment direction for the same action changes too

```python
import math

chosen_prob = 0.7
log_prob = math.log(chosen_prob)

positive_reward = 2.0
negative_reward = -2.0

print("log pi(a|s) =", round(log_prob, 3))
print("positive signal =", round(positive_reward * log_prob, 3))
print("negative signal =", round(negative_reward * log_prob, 3))
```

An example result can be read like this.

```text
log pi(a|s) = -0.357
positive signal = -0.713
negative signal = 0.713
```

The key point of this example is not to memorize the signs themselves.

1. `log pi(a|s)` is the reading handle that connects the chosen-action probability to the update calculation.
2. Even for the same action, a good reward should be read as moving in the direction that makes it appear more often, while a bad reward should be read as moving in the direction that makes it appear less often.
3. The likelihood ratio trick changes `probability differentiation` into `log-probability gradient` so that this connection becomes easier to read.

### Judge It Directly

Read the observations below and choose which interpretation is safer first.

| Observation | Rushed conclusion | Safer interpretation |
| --- | --- | --- |
| `log pi(a|s)` is negative | The policy is wrong | If probability is below 1, the log can be negative, and what matters is the adjustment direction after it is multiplied by reward |
| The sign of the signal changed when positive reward and negative reward were multiplied by the same action | The formula is unstable | The reward sign changes whether that action should appear more often or less often |
| Log-probability appears in the formula | It is only mathematical decoration | It is a device that makes it easier to connect probability differentiation inside an expectation to a sample-based update |

The purpose of this table is not to prove the formula. It is to hold on to interpretation: `how policy probability is pushed and pulled`, and `why log-probability is needed for that connection`.

## Checklist

- Can you explain that policy gradient is the gradient that moves policy parameters in the direction of increasing expected reward?
- Can you explain that the likelihood ratio trick makes probability differentiation easier to read by turning it into a log-probability gradient?
- Can you explain that both REINFORCE and actor-critic can be read on top of this same log-probability gradient intuition?
- Can you explain that positive reward and negative reward make the probability of the chosen action move in different directions?
