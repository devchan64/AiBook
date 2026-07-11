# P4-19.2 Policy-Based Reinforcement Learning

> Section ID: `P4-19.2`
> Version: `v2026.07.11`

In P4-19.1, we looked at the view of learning `how good each action is in each state` as values through value-based reinforcement learning. If we change the question by one step, the next question becomes this.

Instead of choosing an action only after going through values, can the action pattern itself be adjusted directly?

That question is the starting point of policy-based reinforcement learning.

Policy-based reinforcement learning is an approach that learns to gain larger rewards by directly adjusting the probabilities and style of action choice instead of first building a scoreboard for actions.

This Section explains the basic meaning of `policy-based reinforcement learning`, `policy gradient`, and `actor-critic`. Later Sections continue the judgment in the current context from this handle, and the basic meaning of reinforcement learning that directly adjusts behavior reconnects through this Section and the [concept glossary](../../../reference/concept-glossary.md).

## Scope Of This Section

This Section answers the following questions.

- What does it mean to learn a policy directly?
- Where do value-based reinforcement learning and policy-based reinforcement learning differ?
- With what idea does policy gradient adjust a policy?
- Why did actor-critic appear?
- For what kinds of problems does policy-based reinforcement learning feel more natural?

This Section does not go deeply into the following topics.

- A rigorous derivation of the policy-gradient theorem
- Mathematical proofs of the likelihood ratio trick
- Detailed implementation of PPO, TRPO, A2C, and A3C
- Advanced formulas for continuous control

This Section focuses on understanding why policy-based reinforcement learning appeared and what it means to `adjust the behavior itself directly` without first passing through an `action scoreboard`. Constraints such as reward design, exploration cost, and the gap between simulation and reality continue in P4-19.3. The larger expansion map of PPO, TRPO, A2C, A3C, and continuous control is organized in P4-19.4. The minimum mathematical feel of policy gradient and the likelihood ratio trick is grouped again in the supplementary Section P4-19.6.

## Goals Of This Section

- You can explain policy-based reinforcement learning as `an approach that directly adjusts action probabilities and behavior patterns`.
- You can distinguish the difference in question between the value-based and policy-based approaches.
- You can explain policy gradient as `the idea of making well-rewarded actions appear more often and poorly rewarded actions appear less often`.
- You can explain why actor-critic uses policy adjustment and value estimation together.
- You can understand why policy-based reinforcement learning is often mentioned in continuous-action settings or in complex policy representations.

## Why Learn The Policy Directly?

Value-based reinforcement learning is powerful, but not every problem is easy to read like a Q-table.

- The number of actions can be too large.
- Actions can be continuous values.
- `Choose the single highest-scoring action` may not feel like a natural expression.

Imagine directly adjusting the angle of a robot arm.

- The actions are not just `left / right`
- They can be extremely many or effectively continuous, such as `0.1 degree`, `0.2 degree`, and `0.3 degree`

In such a case, the view of `writing the value of every action` feels less natural than the view of `deciding directly what action distribution to create from the current state`.

Read a little more operationally, the difference looks like this.

| Problem scene | Why the scoreboard approach feels cramped | Why the policy-based view reads more naturally |
| --- | --- | --- |
| Adjusting a robot-arm angle | There are too many possible actions | It is better to output the tendency of angle and force directly |
| Steering an autonomous vehicle | It is hard to divide it into only a few choices like `left/right` | It is more natural to handle continuous steering amounts directly |
| Probabilistic tactical choice | Choosing only one top action is too coarse | The action ratio itself can be adjusted by context |
| Exposure-ratio experiments in recommendation | It is hard to write separate values for every ratio | It is easier to handle directly how often each choice should be shown |

So policy-based reinforcement learning is closer to the following question.

`In this state now, what actions should be made to appear how often?`

If this is drawn very simply, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-01-en.mmd"
```

This diagram shows that a policy is not only something that outputs `one correct action`, but can directly create the tendency or strength of several action candidates after seeing a state. That is why policy-based reinforcement learning is read as a view that adjusts the action distribution itself without passing through a scoreboard.

The key point of this picture is that a policy is not only `a switch that picks one action`, but can be an expression that produces a tendency or distribution across several action candidates.

## What Does It Mean To Learn A Policy Directly?

In P4-2.3, a policy was defined as `a way of deciding what action to take in each state`. In policy-based reinforcement learning, this policy itself is treated as the direct target of adjustment.

Put simply:

- Value-based reinforcement learning: build an action scoreboard, then choose from that scoreboard.
- Policy-based reinforcement learning: gradually change the action pattern itself.

Placed side by side:

| View | Central question | Representative intuition |
| --- | --- | --- |
| Value-based | What is the long-term score of this action? | Choose after reading the scoreboard |
| Policy-based | What action distribution should be created in this state? | Adjust the behavior itself directly |

In policy-based approaches, the policy is often expressed like a probability distribution.

For example, in the same state:

- Probability 0.7 of going right
- Probability 0.2 of going up
- Probability 0.1 of going left

The policy itself becomes a model that contains the `tendency of action choice`.

That example can be made a little more concrete like this.

| State | Action candidates | Current policy interpretation |
| --- | --- | --- |
| Driving state just after passing an obstacle | `go straight 0.6`, `slight left steer 0.3`, `slight right steer 0.1` | Go straight most of the time, but left correction is often needed |
| Grasping state slightly misaligned with a box | `weak grasp 0.2`, `medium grasp 0.5`, `strong grasp 0.3` | Medium force is most often favorable, but stronger force is also sometimes needed |

The core of this table is that a policy does not speak only about `one correct action`, but also about what action tendency should appear more often in the current state.

What matters then is that a policy is not `a list of action names`, but `the way actions come out`.

| Question for the same state | What the value-based side reads first | What the policy-based side reads first |
| --- | --- | --- |
| What is good right now? | The long-term score of each action | Which action should come out how often? |
| What changes after the update? | The value of a specific action | The probability of actions or the tendency of control output |
| When failure happens, what is checked again? | Why was the score estimate wrong? | Which action tendency should be reduced, and by how much? |

The difference becomes clearer when the same scene is split into a value-based and a policy-based view.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-02-en.mmd"
```

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-03-en.mmd"
```

The first diagram shows `choosing by comparing action values`, while the second shows `expressing the probability structure by which actions come out`.

## What Is Policy Gradient Trying To Do?

Policy gradient is a representative method that directly adjusts policy parameters to increase expected return.

`Revise the policy little by little in the direction where actions that brought good rewards come out more often, and actions that brought bad rewards come out less often.`

So policy gradient does not try to finish a value table first. Instead, it directly adjusts `the handle that moves the policy`.

That feeling can be compressed even more like this.

| Reward experience that appears first | Policy-based interpretation |
| --- | --- |
| Some action repeatedly created good results | Push the policy so that action appears more often |
| Some action repeatedly created failure | Pull the policy so that action appears less often |
| A single good result occurred but the whole pattern is noisy | Do not trust it too much at once; gather more experience and adjust the tendency |

Compressed into a diagram, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-04-en.mmd"
```

The key point of this picture is that a policy is read not as `an output rule`, but as `an adjustable action tendency`.

REINFORCE can be seen as the most direct introductory example of the policy-gradient flow above. It gathers the actions and rewards from one episode, then adjusts the next policy so that the choices that helped in the end receive higher probability.

In a small intuitive example:

- In the same state, trying `go straight` several times led to faster arrival in the long run
- By contrast, `sharp turn` had some successes but on average created more collisions and penalties

Then the REINFORCE-style intuition is to raise the probability of `go straight` and lower the probability of `sharp turn`.

## Why Does REINFORCE Appear So Often Together With It?

In introductory literature, REINFORCE appears frequently when policy gradient is explained. REINFORCE is one of the most representative early algorithms in policy-based reinforcement learning.

`A method that follows one episode and adjusts the policy in the direction of raising the probability of the choices that ended up producing better rewards`

That means REINFORCE shows the basic philosophy of the policy-based approach in the most direct form.

- Actions that worked well should appear more often
- Actions that did not work well should appear less often

But if it is done only that way, the learning signal can become unstable. Exactly at this point, actor-critic appears.

## Why Did Actor-Critic Appear?

Adjusting the policy directly is natural, but if the policy is corrected immediately only from reward signals, the variation can become large. It becomes easy to waver over whether an action was really good or only looked good by accident.

So the idea appears of placing together `the side that adjusts the policy (actor)` and `the side that evaluates how acceptable the current choice was (critic)`.

Actor-critic should be read as follows.

- Actor: the side that adjusts the actual behavior pattern
- Critic: the side that gives an evaluation signal for how acceptable that action was

So actor-critic is a structure that mixes a policy-based approach and a value-estimation approach.

If the roles are broken down further, it is better to read them like this.

| Component | What it does | A common misunderstanding | Standard for rereading |
| --- | --- | --- | --- |
| Actor | Produces the real action distribution or control output | Thinking that the critic chooses the action instead | The actor holds the actual policy |
| Critic | Gives an evaluation signal for how acceptable the current choice was | Thinking that the critic tells the correct action | The critic is an evaluator, not the direct chooser |
| Actor-critic combination | Uses policy adjustment and evaluation signals together | Thinking it is only two separate algorithms forced together | Read it as a division of roles for reducing variation |

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-05-en.mmd"
```

In this diagram, the critic is not a being that decides the action instead. It gives the evaluation signal that makes the actor update happen more stably.

## Are The Value-Based And Policy-Based Approaches Only In Competition?

Readers easily interpret the two approaches as if `only one of them can be the right way`. But in practice, they reflect different kinds of problem intuition.

| Question | When the value-based view feels more natural | When the policy-based view feels more natural |
| --- | --- | --- |
| Are the action candidates few and clear? | Yes | Less so |
| Are the actions continuous or extremely many? | Harder to handle | Relatively natural |
| Is it easy to choose through a scoreboard? | Yes | Not necessarily |
| Do you want to control the action probability itself? | Indirect | Direct |

So policy-based reinforcement learning does not replace value-based reinforcement learning. It offers a more natural expression under different conditions.

## Where Does It Especially Come To Mind Often?

Policy-based reinforcement learning is often mentioned in the following scenes.

- Problems with continuous actions, such as robot control
- Problems where the whole action distribution matters more than `one best action`
- Problems where stochastic policies should be handled directly
- Problems that need large state spaces and complex function approximation

Read as more realistic examples:

| Problem scene | Why the policy-based view fits well |
| --- | --- |
| Robot-arm control | Actions such as angle, force, and speed can be continuous |
| Steering and acceleration of autonomous vehicles | Continuous control is more natural than a few discrete actions |
| Probabilistic tactical choice in games | A mixed strategy by situation may be needed rather than one fixed action |
| Exploration policy in advertising and recommendation experiments | It may be necessary to handle directly how much of each choice to expose |

For example, in a service-operation analogy:

- The value-based view feels like building `a scoreboard for each response option`
- The policy-based view feels more like directly adjusting `with what probability each response intensity should be used by situation`

Of course, this is only an analogy for intuition, and the design of a real service policy should not be mixed directly with a reinforcement-learning policy.

The robot-arm case is especially important. In a problem with only a few actions such as `left` and `right`, the value-based view can be intuitive. But when it is necessary to decide `how much`, `at what speed`, and `at what angle`, the side that outputs the policy directly may be read more naturally.

At the same time, it would be wrong to conclude that policy-based reinforcement learning is always better for every problem. If the action candidates are few and can be compared clearly through a scoreboard, the value-based approach may be simpler and more explanatory.

That comparison can be written more directly like this.

| Scene | Why the value-based side comes to mind first | Why the policy-based side comes to mind first |
| --- | --- | --- |
| Moving up/down/left/right in a maze | The action candidates are few and easy to compare | It is possible if one intentionally wants to treat a probabilistic movement policy |
| Fine angle adjustment of a robot arm | The action count is hard to handle through a value table | The control amount itself is easier to output directly |
| Tactical choice in a game | If it is a simple choice, value comparison works | If the strategy should be mixed by situation, it is more natural |
| Exposure-ratio experiment in advertising | If there are few exposure choices, score comparison is possible | The exposure ratio itself is easy to adjust like a policy |

## When Should The Policy-Based View Come First?

Policy-based reinforcement learning reads more naturally when `the structure of scoring values and then choosing the top action` starts to feel awkward.

| Problem scene that appears first | Why it is fine to start from the policy-based view | What to guard first |
| --- | --- | --- |
| The action is continuous | It is more natural for the policy to output the control value directly than to list the value of every action | Even if the policy looks good right away, learning instability and safety must be checked separately |
| The action distribution itself must be designed | Because the key issue is how often each action should be used | The action with higher probability can still create side effects |
| The state is complex and policy representation is important | The center becomes `how do we create the behavior tendency?` rather than `what should we do?` | If the policy is corrected immediately without value estimation, variation can grow |
| A division of roles like actor-critic feels natural | Splitting policy adjustment and evaluation signals helps understanding | The existence of a critic does not automatically remove real-world deployment risk |

## Rereading Actor-Critic With Operational Intuition

Actor-critic is often used because practitioners want both `the freedom of adjusting the policy directly` and `the stabilizing signal that value estimation can provide`.

- If only the actor exists: it is easy to change the policy directly, but variation can be large
- If the critic is added: it can provide a better signal about whether the current modification is moving in an acceptable direction

So actor-critic should be understood not as opposing policy-based and value-based learning, but as `a structure that lets the two roles cooperate by splitting them`.

If an operational analogy is attached very carefully:

- The actor is the side that proposes the actual execution
- The critic is the side that gives feedback about whether that execution was better or worse than expected

Again, this is only an analogy to help the structural feeling. If the human roles inside a real organization are matched one-to-one with reinforcement-learning components, misunderstanding will appear.

## Cases And Examples

### Case 1. Why It Is More Natural To Learn The Policy Directly When A Robot Arm Must Adjust The Grasping Angle Little By Little

When a robot arm picks up a box, it is not choosing only a few actions like `left` or `right`. It must continuously decide how much angle and force to apply. In that situation, instead of writing scores for every possible action in a table, it feels more natural to adjust the policy itself so that certain angles and forces appear more often in the current state. Policy-based reinforcement learning directly refines the action distribution by raising the probability of successful grasping motions and lowering the probability of failed ones. That is why, in complex continuous-control problems, `changing the behavior directly` may fit better than `building a scoreboard and selecting the top value`.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-2-mermaid-06-en.mmd"
```

If this case is compressed like a project memo, it can be written like this.

| Current state | Action the policy made more frequent | Failure costs to inspect together | Next question |
| --- | --- | --- | --- |
| Box position is slightly tilted | A somewhat larger rotation angle and a stronger grasping force | Slipping, excessive force, equipment wear | Does this probability distribution remain stable under other position errors too? |
| Repetitive work that needs continuous control | The combination of control values with higher success probability | Rare failures can accumulate into large damage | Should critic signals or extra safety constraints be added? |

### Case 2. When An Advertising Exposure Ratio Must Be Treated As A Distribution Rather Than As One Correct Answer

Suppose an experiment platform shows users three banner candidates. There are scenes where it is more natural not to show only one banner to every user all the time, but to expose them with different ratios like A 60%, B 30%, and C 10% by state. In such a case, the policy-based view does not ask only `which banner is best?`, but directly handles `which banner should appear how often in which state?`

| User state | Question read first from the policy-based side | What must be guarded together |
| --- | --- | --- |
| New user | What banner ratio balances exploration and conversion? | Is the policy over-concentrating after trusting one high click rate too much? |
| Returning user | Which banner should be shown more often for long-term conversion? | Are short-term clicks and long-term satisfaction being mixed carelessly? |

This case shows that policy-based reinforcement learning fits better not to `choose the single best action`, but to `design the action distribution itself`.

For example, suppose the current policy behaves like this in the new-user state.

| Banner | Current exposure probability | Question to review after observation |
| --- | --- | --- |
| A | 0.5 | Clicks are high, but does churn rise together? |
| B | 0.3 | Clicks are lower, but is purchase conversion more stable? |
| C | 0.2 | Should the exploratory share be reduced further or kept? |

This small example makes it clearer that the policy-based approach is not only asking `is A the best?`, but directly handling `in what ratio should A, B, and C be shown together?`

## Practice And Example

This example focuses on confirming with numbers the core feeling of policy-based reinforcement learning: `raise the probability of actions that received good rewards`. It does not stop at raising a probability once. It also checks how the policy moves in the opposite direction when the sign of the reward changes.

Problem situation:

- Policy-based reinforcement learning changes not only an action scoreboard, but the probability with which an action is selected

Input:

- Current action scores in the policy
- The action chosen in this episode
- The reward received as a result

Expected output:

- Action scores before the update
- Action scores after reflecting the reward signal
- New action probabilities after normalization

Concepts to confirm:

- An action that received a good reward can be adjusted to appear more often in the next policy
- In policy-based reinforcement learning, it is important to read action scores as a probability distribution
- The focus is on changing the action tendency itself rather than only estimating values

```python
import math

action_scores = {
    "left": 0.20,
    "right": 0.40,
}

chosen_action = "right"
reward_signal = 1.5
step_size = 0.3

print("before update:", action_scores)

# Slightly raise the score of the chosen action.
updated_scores = action_scores.copy()
updated_scores[chosen_action] += step_size * reward_signal

print("score after reward:", updated_scores)

# Normalize with softmax so the scores can be read like probabilities.
exp_left = math.exp(updated_scores["left"])
exp_right = math.exp(updated_scores["right"])
total = exp_left + exp_right

new_policy = {
    "left": round(exp_left / total, 3),
    "right": round(exp_right / total, 3),
}

print("new policy:", new_policy)
```

An example execution result can be read like this.

```text
before update: {'left': 0.2, 'right': 0.4}
score after reward: {'left': 0.2, 'right': 0.85}
new policy: {'left': 0.343, 'right': 0.657}
```

This is not a rigorous implementation of policy gradient, but it shows the central idea of policy-based reinforcement learning.

- The score of `right`, which received the good reward, was raised
- As a result, the probability of `right` became larger in the new policy

So policy-based reinforcement learning directly adjusts `the tendency for actions to come out` in this direction.

### Try Changing One Value: If The Same Action Receives A Bad Reward, How Does Its Probability Change?

This time, choose the same action `right`, but change the reward signal to `-1.0`.

```python
import math

action_scores = {
    "left": 0.20,
    "right": 0.40,
}

chosen_action = "right"
reward_signal = -1.0
step_size = 0.3

updated_scores = action_scores.copy()
updated_scores[chosen_action] += step_size * reward_signal

exp_left = math.exp(updated_scores["left"])
exp_right = math.exp(updated_scores["right"])
total = exp_left + exp_right

new_policy = {
    "left": round(exp_left / total, 3),
    "right": round(exp_right / total, 3),
}

print("score after reward:", updated_scores)
print("new policy:", new_policy)
```

```text
score after reward: {'left': 0.2, 'right': 0.1}
new policy: {'left': 0.525, 'right': 0.475}
```

Under a good reward, the probability of `right` rose, but under a bad reward, the probability of the same action fell. This comparison makes clear that policy-based reinforcement learning is not `a way of reading action scores`, but `a way of pushing and pulling action tendencies`. So when learning the policy-based approach, it is better to read first what feedback changed what action distribution, rather than reading only the size of one score.

### How Does This Exercise Recover The Goal Of Part 4?

This exercise recovers the goal of Part 4 at the level of policy representation. The problem is not only `what should be done`, but also `what actions should be made to appear often`. The evaluation is then read through `how does the reward change alter the action distribution in practice?` If the goal still did not feel concrete after running the example, it is usually not because the word policy is too abstract, but because there was too little chance to compare `the scene where the probability distribution changed` before and after.

| Common recording language | What to record immediately from this exercise |
| --- | --- |
| Visible structure | Even for the same action, once the sign of the reward changed, the policy probability moved in the opposite direction |
| Interpretation boundary | An action whose probability rose does not immediately become safe or desirable in the real world |
| Next question | Does this policy-distribution adjustment remain under other states or constraints too? |

This Section also should not leave only policy explanation. It must also leave what action distribution was proposed and what failure costs should be guarded. Even if two rewards look similar, one policy can create certain failures more often and another can behave more conservatively, so the action distribution and the failure pattern must be read together.

| Item to leave together | What this Section writes | Why it is needed |
| --- | --- | --- |
| Policy proposal | What action was made to appear with what probability in the current state | To make clear that the policy is an action tendency, not a scoreboard |
| Expected-reward standard | What reward raised the probability of a certain action | To connect action-distribution adjustment and goal definition |
| Failure-cost boundary | What side effects the higher-probability action can create in the real environment | Because policy updates do not immediately imply safety |
| Next validation question | Can this distribution survive under other states or real constraints? | To hand the policy-based choice over to follow-up review |

## Viewpoints To Remember In This Section

- Policy-based reinforcement learning is an approach that directly adjusts the policy itself in order to raise expected reward.
- If value-based reinforcement learning is strong at building an action scoreboard, policy-based reinforcement learning is natural at directly handling action probabilities and behavior patterns.
- Policy gradient modifies the policy parameters in the direction that reinforces action tendencies with good rewards.
- REINFORCE is a representative introductory algorithm that shows the basic philosophy of policy-based reinforcement learning.
- Actor-critic is a structure that splits the roles of actor and critic so that policy adjustment and evaluation signals are handled together.

The core of this Section is not memorizing policy-based names, but fixing what it means to change a policy directly.

| What must be read together | The question read first in this Section | Where it connects immediately next |
| --- | --- | --- |
| Difference from the value-based view | Should the scoreboard be learned first, or should the behavior itself be changed directly? | P4-19.1 Value-Based Reinforcement Learning |
| Policy gradient and actor-critic | In what way is the policy corrected, and who gives the evaluation signal? | P4-19.4 Follow-up Algorithm Map |
| Continuous actions and large state spaces | Why is it more natural to handle the policy itself? | P4-19.3 Real-world deployment and control problems |
| Failure-cost boundary | What side effects can the higher-probability action create in real scenes? | safe RL, sim-to-real, and offline review |

## Short Check

- Can you explain why it is more natural to treat the policy itself directly in continuous-action problems?
- Can you explain that policy gradient adjusts action tendencies rather than a scoreboard?
- Can you distinguish that the critic in actor-critic does not choose the policy instead, but gives the evaluation signal?

## When Should This View Come To Mind First?

- When continuous actions or large state spaces make it more natural to handle the action tendency itself than to keep a scoreboard, the policy-based view should come first.
- When explaining policy gradient leaves behind only vague optimization language, return to the sentence that it directly adjusts the policy so that good actions appear more often.
- When the roles of actor and critic are mixed, separate again the side that proposes the execution and the side that gives the evaluation signal.

## Sources And References

- Richard S. Sutton and Andrew G. Barto, `Reinforcement Learning: An Introduction`, 2nd ed., The MIT Press, 2018, checked on 2026-06-27. [https://mitpress.mit.edu/9780262039246/reinforcement-learning/](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }
- Ronald J. Williams, `Simple statistical gradient-following algorithms for connectionist reinforcement learning`, Machine Learning, 1992, checked on 2026-06-27. [https://link.springer.com/article/10.1007/BF00992696](https://link.springer.com/article/10.1007/BF00992696){: target="_blank" rel="noopener noreferrer" }
- Richard S. Sutton, David McAllester, Satinder Singh, Yishay Mansour, `Policy Gradient Methods for Reinforcement Learning with Function Approximation`, NeurIPS 1999, checked on 2026-06-27. [https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Vijay R. Konda, John N. Tsitsiklis, `On Actor-Critic Algorithms`, SIAM Journal on Control and Optimization, 2003, checked on 2026-06-27. [https://doi.org/10.1137/S0363012901385691](https://doi.org/10.1137/S0363012901385691){: target="_blank" rel="noopener noreferrer" }
