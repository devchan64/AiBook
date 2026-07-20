# P4-2.3 Reinforcement Learning

> Section ID: `P4-2.3`
> Version: `v2026.07.20`

P4-2.1 looked at supervised learning, which learns from data with labels, and P4-2.2 looked at unsupervised learning, which finds data structure without labels. This time we look at reinforcement learning, where a model takes an action, receives a reward from the result, and adjusts the next way of acting.

Reinforcement learning differs from `learning by looking at the correct label and matching it`. It does not always tell you immediately which action is good. Instead, it looks at the reward and next state that return after trying an action, and gradually finds a better way to act. So reinforcement learning deals not with one input-output pair, but with a flow of choices connected over time.

This Section explains the basic distinction among `reinforcement learning`, `state`, `action`, `reward`, and `policy`. Later Sections continue the current context using this handle, and the basic meaning of learning through long-term reward is connected again through this Section and the [concept glossary](/AiBook/reference/concept-glossary/).

## Scope Of This Section

This Section explains the basic structure of reinforcement learning. It does not cover the formulas or implementation of individual algorithms such as Q-learning, SARSA, policy gradient, or actor-critic here. Q-learning and SARSA return in P4-19.1 on value-based reinforcement learning, while policy gradient and actor-critic return in P4-19.2 on policy-based reinforcement learning. The key is to fix clearly first the relation among agent, environment, state, action, reward, and policy.

- How is reinforcement learning different from supervised and unsupervised learning?
- What are the agent and the environment?
- How do state, action, reward, and policy connect?
- Why is delayed reward difficult?
- Why are both exploration and exploitation necessary?

## Goals Of This Section

- You can explain reinforcement learning as an approach that learns a policy through actions and rewards.
- You can distinguish the roles of agent, environment, state, action, reward, and policy.
- You can understand that reinforcement learning is closer to sequential decision making than to one-time prediction.
- You can explain that immediate reward and long-term reward can differ.
- You can explain with examples why balance between exploration and exploitation is necessary.

## Understanding It First Through One Scene

Think of a small game. A character moves on a grid, and earns points when it reaches the goal.

| Element | Simple explanation | Game example |
| --- | --- | --- |
| agent | The subject that chooses the action | character |
| environment | The world where the agent acts | grid and rules |
| state | Information that represents the current situation | character position |
| action | A move that can be chosen | up, down, left, right |
| reward | A numeric signal received from the result of the action | goal reached `+10`, wall collision `-1` |
| policy | The way of deciding which action to take in each state | `move in the direction that gets closer to the goal` |

In supervised learning, there could already be labels such as `from this position, right is the correct move`. In reinforcement learning, the agent usually tries actions first and then adjusts the next way of acting using the rewards that come back.

## The Basic Flow Of Reinforcement Learning

The most basic flow in reinforcement learning is repeated interaction between the agent and the environment.

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-3-mermaid-01-en.mmd"
```

The important point in this diagram is the loop. Reinforcement learning is not a one-shot problem where one input is observed and one output is matched. The agent acts, the environment changes, a reward returns, and that experience affects the next action policy.

The Sutton and Barto textbook from MIT Press also explains reinforcement learning as a computational approach where an agent interacts with a complex, uncertain environment while trying to maximize the total reward it receives. Here that definition is rewritten so the reader can follow it as `learning by trying an action, seeing the result, and adjusting the next way of choosing`.

## Comparing Supervised, Unsupervised, And Reinforcement Learning

All three learning types are connected in that they learn something from data or experience. But the shape of the question is different.

| Category | Starting point | Central question | Simple example |
| --- | --- | --- | --- |
| supervised learning | input and label | What is the correct output for this input? | Is this email spam? |
| unsupervised learning | unlabeled input | What structure exists inside the data? | How do customers group together? |
| reinforcement learning | state, action, reward | What action policy makes long-term reward larger? | How should the character move in this game to get a higher score? |

Reinforcement learning can look like another kind of learning without labels, but it is also different from unsupervised learning. Unsupervised learning focuses on finding structure in data, while reinforcement learning focuses on changing a way of acting by choosing actions and receiving rewards from the results.

## Policy Is The Way Of Choosing Actions

Policy is a very important word in reinforcement learning. A policy is the way of deciding what action to take in a given state.

In a grid game, a policy can be read like the following.

| Current state | Available actions | Action chosen by the policy |
| --- | --- | --- |
| The goal is to the right | up, down, left, right | right |
| There is a wall directly ahead | up, down, left, right | down |
| The goal is still far away | several directions | a direction not tried enough yet |

The policy does not have to be a good rule from the beginning. In reinforcement learning, the agent improves the policy by trying different actions. The policy can be a hand-written rule, or it can be a function adjusted during learning.

## Reward Is Not An Immediate Answer

Reward is the numeric signal that evaluates the result of an action. But reward is not an answer sheet that tells you `this action is correct` every time, the way labels do in supervised learning.

Some actions can look like a loss right now but lead to a larger reward later. Conversely, an action that gains a few points immediately can be a poor choice in the long run.

For example, in a game, reaching the goal may require a temporary detour.

| Choice | Immediate result | Long-term result |
| --- | --- | --- |
| Take a nearby score item | immediate `+1` | reaching the goal may take longer |
| Take a route with no immediate point | immediate `0` | it may lead to `+10` by reaching the goal |

For this reason, reinforcement learning must separate `actions that look good right now` from `actions that create better outcomes later`. This is one of the central points that makes reinforcement learning both difficult and interesting.

If you rewrite it as a coupon-recommendation case, the point that it becomes a reinforcement-learning problem only when `immediate click` and `later purchase` are read together becomes even clearer.

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-3-mermaid-02-en.mmd"
```

## Exploration And Exploitation

In reinforcement learning, exploration and exploitation must be considered together.

Exploration means trying actions that are not yet well known. Exploitation means choosing an action that already looks good based on what has been learned so far.

| Choice mode | Meaning | Strength | Risk |
| --- | --- | --- | --- |
| exploration | Try a new action | A better path may be discovered | Reward can be low for now |
| exploitation | Choose an action that already looks good | Reward can be gained more stably | A better option may never be found |

The restaurant analogy makes this clearer. If you go to a restaurant you already like, the chance of failure is low. But if you never try a new restaurant, it is hard to discover something better. Reinforcement learning is similar. It must use what it already knows while still trying enough new actions.

## Points To Be Careful About In Real Problems

Reinforcement learning appears often when explaining problems where action and result are connected, such as games, robots, and autonomous-driving simulations. But applying it directly to reality is not easy.

- If reward is designed poorly, the system can learn unwanted behavior.
- If exploration is done recklessly in the real environment, cost or risk can become large.
- If the result appears late, it becomes hard to know which action created the good outcome.
- A policy that works well in simulation cannot automatically be assumed to work equally well in reality.
- The word agent here is not always the same as the word agent used for LLM services.

The last point matters especially. In reinforcement learning, the agent is the learning subject that sees a state, chooses an action inside an environment, and receives a reward. In LLM services, the word agent often refers to an execution structure that breaks a goal into tasks and calls tools. The two usages can connect, but if they are mixed as if they were the same word, confusion appears.

## Where It Meets LLM Again

Reinforcement learning reappears in Part 5 when LLMs and generative AI are discussed. In particular, the flow of adjusting model output using human preferences returns in P5-10.1 on instruction tuning and P5-10.2 on the basic problem of alignment.

But this Section does not explain LLM alignment or RLHF deeply. What matters now is simply to distinguish reinforcement learning as `learning that adjusts a way of acting through reward`.

The question of whether something is reinforcement learning becomes clearer if you first check `is the current problem being read through sequential decision making and reward flow?`

| Current state | Read it as reinforcement learning? | Why |
| --- | --- | --- |
| An action is taken, a reward returns, and the next choice continues from it | yes | Because sequential decision making is central rather than one-time answer matching |
| Long-term reward matters more than the immediate score | yes | Because the tension between immediate and long-term reward sits at the center of the problem |
| Inputs and correct labels already exist together, and one-time prediction is the core | usually no | Because the problem is more directly supervised learning |

## Cases And Examples

### Case 1. When A Coupon Recommendation Must Choose Between Raising Immediate Clicks And Raising Long-Term Purchases

Suppose a service wants to decide automatically which coupon should be shown to a user first. At first glance, people may think it is enough to keep showing whichever coupon gets the highest click rate.

But a high click right now does not necessarily mean better long-term sales or return visits. Some coupons can draw fewer immediate clicks but lead to later purchases, while others can get many clicks right away but still be harmful in the long run.

This kind of problem differs from supervised learning, where one input and one correct label are matched. Here the reward flow after the action must be read together. That is why reinforcement learning is explained through state, action, reward, and policy, and why both immediate reward and long-term reward must be considered together.

The checkable result appears when policies are compared. If the policy with the higher click rate differs from the policy with the higher long-term purchase reward, then the problem is already closer to sequential decision making and reward design than to simple classification.

```mermaid
--8<-- "assets/part-04/chapter-02/p4-2-3-mermaid-03-en.mmd"
```

## Checklist

- Can you explain in what state a problem should be read as reinforcement learning rather than supervised learning?
- Can you explain why reward is not a signal that tells the immediate correct answer the way a label does?
- Can you explain why the reinforcement-learning agent and the LLM-service agent should not be used as if they were the same meaning?
- Can you explain that reinforcement learning is learning in which an agent improves a policy using rewards while interacting with an environment?
- Can you explain why state, action, reward, and policy are the basic words for reading reinforcement learning?
- Can you explain that without balance between exploration and exploitation, it becomes hard both to find better actions and to gain reward stably?

## Sources And References

- Richard S. Sutton and Andrew G. Barto, `Reinforcement Learning: An Introduction`, 2nd ed., MIT Press, 2018, accessed 2026-06-25. [https://mitpress.mit.edu/9780262039246/reinforcement-learning/](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }
- Olivier Buffet, Olivier Pietquin, Paul Weng, `Reinforcement Learning`, arXiv, 2020, accessed 2026-06-25. [https://arxiv.org/abs/2005.14419](https://arxiv.org/abs/2005.14419){: target="_blank" rel="noopener noreferrer" }
