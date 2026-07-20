# P4-19.4 Supplementary Learning: Reading DQN, PPO, And RLHF Inside The Larger Reinforcement-Learning Flow

> Section ID: `P4-19.4`
> Version: `v2026.07.20`

After reading P4-19.1 through P4-19.3, readers quickly encounter many more names when they study reinforcement learning further.

- DQN
- PPO, TRPO, A2C, A3C
- safe reinforcement learning
- offline reinforcement learning
- domain randomization
- RLHF, preference optimization

These names came from different periods and different bottlenecks, but they often rush in all at once. This Section focuses not on learning each implementation, but on organizing the larger flow of `why did these names branch out?`

This supplementary learning Section does not explain the basic definition of reinforcement learning from the beginning again. The handle for value-based reinforcement learning remains in P4-19.1, the handle for policy-based reinforcement learning remains in P4-19.2, and the handle for application risk remains in P4-19.3 and the [concept glossary](/AiBook/reference/concept-glossary/). Here, only the later names are arranged as a genealogy.

## Scope Of This Supplementary Section

This Section answers the following questions.

- Why is DQN so often mentioned as the representative follow-up example after value-based reinforcement learning?
- What difficulty in policy-based reinforcement learning are PPO, TRPO, A2C, and A3C trying to reduce?
- Why did safe RL and offline RL become separate topics in real-world application contexts?
- How is domain randomization connected to sim-to-real problems?
- Why does RLHF connect general reinforcement-learning problems and LLM alignment?

The detailed training pipeline of RLHF and alignment practice returns in Part 5.

## Goals Of This Supplementary Section

- You can organize the later names of reinforcement learning into four branches: value-based expansion, policy-based stabilization, real-world reinforcement, and LLM-alignment connection.
- You can explain on what tradition DQN and PPO each stand.
- You can say that safe RL, offline RL, and domain randomization all connect to the problem of `not being able to try freely in reality`.
- You can understand RLHF not as `directly transplanting ordinary reinforcement learning into LLMs`, but as a later branch reshaped for alignment problems.

## First Draw The Large Map

The following table gives the large map.

| Name group | Question it mainly tries to answer |
| --- | --- |
| DQN | How can value-based reinforcement learning be extended into larger state spaces? |
| PPO, TRPO, A2C, A3C | Can a policy be learned directly without becoming too unstable? |
| safe RL, offline RL | Can dangerous or expensive exploration be reduced in reality? |
| domain randomization | Can a policy learned in simulation transfer to reality more robustly? |
| RLHF, preference optimization | Can LLM output become more desirable by reflecting human preference? |

So these later algorithm names are better read not as `smarter reinforcement learning`, but as `branches that let reinforcement learning operate under wider real-world constraints`.

When first reading this map, it is better to write together not only the names, but also `what intuition broke first?`

| Intuition that broke first | Name group that branches out from it |
| --- | --- |
| A Q-table cannot contain the whole state space | DQN |
| Direct policy updates shake too much | PPO, TRPO, A2C, A3C |
| Reality does not allow free exploration | safe RL, offline RL |
| Simulation performance does not survive in reality | domain randomization |
| Human preference cannot be given directly as a correct label | RLHF, preference optimization |

In this supplementary Section too, the names should not be listed alone. Even names inside the same reinforcement-learning family are trying to reduce different failure costs and different real-world constraints, so the problem signal must be written before the name.

| Name group | Problem signal that appeared first | Why that branch became necessary |
| --- | --- | --- |
| DQN | The state space is too large for a value table alone | To extend value-based intuition into larger problems |
| PPO, TRPO, A2C, A3C | Policy updates become unstable easily | To make policy adjustment more stable |
| safe RL, offline RL | Reality does not allow free exploration | To reduce failure cost and data constraints |
| domain randomization | Simulation performance breaks immediately in reality | To reduce the sim-to-real gap |
| RLHF | Human preference is hard to treat as a direct correct label | To connect human feedback to something reward-like |

## Which Follow-Up Branch Should Be Looked Up First?

When later reinforcement-learning names look numerous, the branch should be chosen not by the name, but by `what bottleneck is visible first right now?`

| Bottleneck visible first | Branch to think of first | Why |
| --- | --- | --- |
| The state space is so large that the Q-table intuition breaks | DQN family | The central problem is extending the value-based view with function approximation |
| Policy updates fluctuate often | PPO, TRPO, actor-critic family | This connects directly to making direct policy learning more stable |
| Reality does not allow free exploration | safe RL, offline RL | Reducing failure cost and data constraints is the more urgent issue |
| Simulation performance does not survive in reality | domain randomization, sim-to-real reinforcement | A strategy for shrinking the deployment-environment gap is needed first |
| Human preference must shape language-model outputs | RLHF, preference optimization | Alignment and interpretation of human feedback become more central than ordinary control |

So looking up later names is not the task of choosing `which algorithm is more famous`, but of classifying first `is the bottleneck state representation, policy stabilization, real-world constraint, or human-preference reflection?`

## Why Is DQN Mentioned So Often Separately?

The Q-learning of P4-19.1 has strong intuition, but once states and actions become large, a table can no longer hold all the values. DQN appears at that point.

So DQN is a line that `expresses the Q-value through a function approximator instead of a table, in order to handle larger state spaces`.

That is why DQN is not a completely new philosophy, but a representative case of extending value-based reinforcement learning into a larger problem.

That flow can be written more tightly like this.

| What stays from Q-learning intuition | What changes in DQN |
| --- | --- |
| It still asks `which action has the larger value?` | It expresses the value through approximation instead of a table |
| It still chooses through value comparison | It makes larger state spaces tractable |
| It keeps the value-based view | Once neural networks and other approximators enter, the interpretation becomes less direct |

So DQN is better read not as `a name that discarded value-based learning`, but as `a name that moved the value-based intuition into a larger state space`.

## Why Are PPO And The Actor-Critic Families Used So Widely?

The policy-based reinforcement learning of P4-19.2 has the advantage of adjusting the behavior directly, but the learning can easily become unstable. Names such as PPO, TRPO, A2C, and A3C are largely tied to that problem.

- We want the policy not to change too abruptly
- We want to reduce the fluctuation of the learning signal
- We want to use the division of roles between actor and critic more stably

| Family | Introductory reading |
| --- | --- |
| TRPO, PPO | A line that tries to avoid shaking the policy too much at once |
| A2C, A3C | A line that tries to operate the actor-critic structure more practically |

So these names are later answers to the problem that `policy-based reinforcement learning often shakes in practice`.

This can be read more directly like this.

| Difficulty visible first | What the later family is trying to reduce |
| --- | --- |
| One update changes the policy too much | Update size |
| Reward signals jump too much | Learning variance |
| We want direct policy learning but do not want to discard value information | Instability in dividing the roles of actor and critic |

So although PPO, TRPO, A2C, and A3C differ in name, they share the direction `keep the advantage of learning the policy directly, but do not let it collapse too unstably`.

## Why Did Safe RL And Offline RL Become Their Own Topics?

As P4-19.3 showed, exploration itself can be dangerous or expensive in reality. That is why two branches grew separately.

- safe RL: a line that tries to treat risk constraints more strictly even while exploration and policy improvement continue
- offline RL: a line that tries to learn the policy mostly from already collected data instead of making many new exploratory trials

Both came from the real-world problem that `we cannot simply try anything we want`.

It is useful to bundle them together while also leaving their difference.

| Branch | Risk it tries to reduce first | Basic idea |
| --- | --- | --- |
| safe RL | Direct danger that can happen during trying | Keep learning and exploration, but under stricter constraints |
| offline RL | The cost and risk that arise from new trials | Learn first inside the already collected data |

So both arise from real-world constraints, but safe RL is closer to `still try, but more safely`, while offline RL is closer to `try less, and learn first from existing data`.

## Why Is Domain Randomization Connected To Sim-To-Real?

One reason a policy learned well in simulation fails in reality is environmental difference. Domain randomization can be understood as a direction that intentionally shakes simulator conditions more widely, so that the policy becomes less brittle against real-world difference.

The core idea is this.

`If reality cannot be copied perfectly, then do not train only on one overly clean simulation setting.`

Made more concrete:

| When simulation is matched to only one condition | What we hope to gain by intentionally varying conditions |
| --- | --- |
| The policy adapts too much to one lighting, friction, or delay setting | We want a policy that is less sensitive to real-world difference |
| The score is high inside the simulator | We want to reduce the chance of sudden collapse in reality |

So domain randomization is better read not as a technique for maximizing simulator score, but as `a reinforcement that prevents the learner from seeing only an overly clean world inside the simulator`.

## Why Is RLHF Important Here Too, And Why Does It Return Again In Part 5?

RLHF, reinforcement learning from human feedback, looks by name like one branch of reinforcement learning. But in the LLM context, it is not a direct copy of ordinary game or robot-control problems.

- In LLMs, it is often hard to turn human preference or evaluation criteria directly into correct labels
- So a flow appeared that converts human feedback into something reward-like and adjusts the policy from it
- At that point, reinforcement-learning language and alignment language meet

So RLHF is part of general reinforcement-learning thinking, but because it belongs to the separate context of LLM alignment, it must be read again in more detail in Part 5.

Placed side by side with general reinforcement-learning problems:

| Comparison point | Reinforcement learning in general control problems | The side mainly handled by RLHF |
| --- | --- | --- |
| Action target | Movement, control, selection actions | Text-output policy |
| Link to human goals | Indirectly connected through reward design | Tries to reflect human preference feedback more directly |
| Why it is separately hard | Exploration and environment response are hard | Preference interpretation and alignment goals are hard |

So RLHF should be read not as `RL is also used for LLMs`, but as `a branch where the question of how human feedback should be interpreted like reward comes to the front`.

| What is fixed now in Part 4 | What returns again in Part 5 |
| --- | --- |
| Why RLHF is connected to the reinforcement-learning genealogy | Where RLHF sits inside the LLM training pipeline |
| The idea that human feedback can be treated in a reward-like way | Reward models, preference data, and alignment procedures |

## Cases And Examples

### Case 1. If DQN, PPO, And RLHF Appear Together, What Should Be Separated First?

When beginners look for reinforcement-learning material, they often encounter DQN in game-performance examples, PPO in policy-stabilization explanations, and RLHF in the context of LLM alignment almost side by side.
A person first tends to group them with criteria such as `reinforcement-learning names that appear often these days` or `stronger recent algorithms`.

But that criterion quickly shows its limit.
If the names are grouped only by recency, `why DQN appeared`, `why PPO became widely used`, and `why RLHF must be read differently from ordinary control problems` all become blurred.
In reality, the three names do not appear together because they are all just `improved reinforcement learning`.
They branched out as answers to different bottlenecks.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-4-mermaid-01-en.mmd"
```

| Name encountered | Criterion a reader first tends to group by | Limit that soon appears | Interpretation this Section switches to |
| --- | --- | --- | --- |
| DQN | a famous game-reinforcement-learning algorithm | it hides why it appeared inside the value-based line | read it as the line where Q-tables broke under larger state spaces |
| PPO | a high-performing recent RL algorithm | it hides that policy stabilization was the core problem | read it as the line that reduces instability in policy updates |
| RLHF | a name that attached reinforcement learning to LLMs | it erases the problems of human preference and alignment | read it as an alignment branch that connects human feedback like reward |

If this case is compressed like a handoff memo, it can be written as follows.

| Name encountered | Problem statement to read first | Connection to check next |
| --- | --- | --- |
| DQN | How was the value-based view extended into a larger state space? | Function approximation and its bridge to neural networks |
| PPO | How were policy updates made less unstable? | actor-critic and policy stabilization |
| RLHF | How was human feedback connected to something reward-like? | Part 5 alignment and preference optimization |

The more names appear in the same place, the more important it becomes to record first not `what does it compute?`, but `what problem came first?`
The visible result in this case is not `I know DQN, PPO, and RLHF`, but `did the bottleneck question that should come first change for each name?`
That is exactly the purpose of this supplementary Section.

## Practice And Example

This practice focuses on rereading later reinforcement-learning names not as `memorizing algorithm names`, but as `bottlenecks and branches`.

Problem situation:

- when names such as DQN, PPO, offline RL, and RLHF appear together, they can easily look like one bundle called `better reinforcement learning`

Input:

- four bottlenecks that appeared first
- candidate follow-up branches that respond to each bottleneck

Expected output:

- a matching table for which branch should be looked up first

Concept to check:

- later algorithm names should be read first by `what bottleneck produced them`, not by fame
- value-based expansion, policy stabilization, real-world constraint reinforcement, and LLM-alignment connection are different branches

| Bottleneck visible first | Name that is easy to attach too quickly | Branch that should be matched first |
| --- | --- | --- |
| The state space becomes so large that the Q-table breaks | PPO | DQN family |
| Policy updates shake too much | DQN | PPO, TRPO, A2C, A3C |
| It is not possible to do many new exploratory trials in reality | RLHF | safe RL, offline RL |
| Human preference must be reflected in language-model output | DQN | RLHF, preference optimization |

### Try Judging Directly

Look at the observations below and choose first which interpretation is safer.

| Observation | Hasty conclusion | Safer interpretation |
| --- | --- | --- |
| DQN and PPO are both mentioned often | They are both the same kind of performance upgrade | One is a value-based expansion, and the other is a policy-stabilization line |
| offline RL branched out separately | It is only a name that appeared because data were scarce | It is directly tied to the constraint that reality does not allow many new exploratory trials |
| RLHF appears in a reinforcement-learning list | Ordinary control-problem RL was transferred to LLMs as it was | It has to be reread as an alignment problem that connects human preference like reward |

The point of this table is not to memorize names.
It is to build the habit of classifying immediately `what bottleneck appeared first` and `which branch should be checked first because of it`.

## Checklist

- Can you explain that DQN is a line that extends value-based reinforcement learning into large state spaces, while PPO, TRPO, A2C, and A3C are lines that try to reduce instability in policy-based reinforcement learning?
- Can you explain that safe RL, offline RL, and domain randomization are branches that appeared because of real-world constraints and deployment risk?
- Can you explain that RLHF is a point where reinforcement learning meets LLM alignment?
- When several names appear at once, have you formed the habit of asking first `what bottleneck produced this name?`?

## Sources And References

- Richard S. Sutton, Andrew G. Barto, [Reinforcement Learning: An Introduction, 2nd ed.](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }, checked on 2026-07-01.
- Volodymyr Mnih et al., [Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236){: target="_blank" rel="noopener noreferrer" }, checked on 2026-07-01.
- John Schulman et al., [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347){: target="_blank" rel="noopener noreferrer" }, checked on 2026-07-01.
- Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155){: target="_blank" rel="noopener noreferrer" }, checked on 2026-07-01.
