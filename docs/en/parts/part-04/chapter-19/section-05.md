# P4-19.5 Supplementary Learning: How To Read The Bellman Equation, Convergence, And Function Approximation For The First Time

> Section ID: `P4-19.5`
> Version: `v2026.07.10`

Once readers begin studying value-based reinforcement learning in P4-19.1, the following names quickly appear next to it.

- Bellman equation
- convergence
- function approximation

Rather than unfolding these names through a long sequence of rigorous proofs, this supplementary Section first connects `why the score table of value-based reinforcement learning is written recursively`, `why repeated updates are checked for stability`, and `why large problems move from a table to a function`.

## Scope Of This Section

This Section answers the following questions.

- Why is the Bellman equation read as something like `current reward + value of the next state`?
- What does it mean to say we are checking convergence, and what is becoming less unstable?
- Why does function approximation appear instead of a Q-table?
- As what kind of extension of value-based reinforcement learning should DQN be read?

This Section focuses on reading the expansion background of reinforcement learning through three handles: `recursive value reading`, `stabilization of repeated updates`, and `moving from a table to a function`.

## Goals Of This Section

- You can explain the Bellman equation as `an equation that connects current reward and future value`.
- You can explain convergence as `the question of whether repeated update results stabilize near some value`.
- You can explain function approximation as `a way of expressing values with a model instead of a table when the state space is large`.
- You can explain DQN as `a representative extension that moves value-based intuition into a large state space`.

## Why This Section Is Needed

The intuition of Q-learning and SARSA is useful, but two walls appear quickly.

- Why can we say an update formula like this is valid?
- If the number of states becomes huge, can every value really be written into a table?

That is where the Bellman equation, convergence, and function approximation appear.

So the core of this Section is to connect for the first time `where Q-table intuition obtains its mathematical form, where it meets computational limits, and what extension it moves into next`.

## Why Does The Bellman Equation Appear?

The key idea of value-based reinforcement learning is simple.

`A good action is not just an action with a large immediate reward, but an action that also leads to a good next state.`

If that idea is read as a formula, the following structure appears naturally.

- reward obtained now
- future value that continues from the next state

So the Bellman equation is a more compressed way of writing the sentence `value is not only one current gain, but also the goodness of the choices that continue afterward`.

At an introductory level, it is enough to read it like this.

| Reading question | What the Bellman form says |
| --- | --- |
| Why is this action good right now? | Because not only the immediate reward, but also the next state's value, is large |
| Why does value look recursive? | Because the next state's value is defined again in the same way |
| Why does the calculation not end in one step? | Because future value connects again to future value |

So before the complicated symbols, it is more important to grasp the Bellman equation as `a score table that already includes the future`.

## What Does It Mean To Check Convergence?

Q-learning and SARSA do not complete all values in one shot. They update them little by little as experience accumulates. So the following question appears naturally.

`If these values keep being revised, do they eventually become stable to some degree?`

That question is convergence.

At an introductory level, convergence can be read like this.

`As the updates are repeated, do the values stop swinging wildly and gather near a relatively stable value?`

| Sense that points toward good convergence | Sense that should make us doubt convergence |
| --- | --- |
| The amount of change in the same state-action value shrinks as updates repeat | The value still swings a lot after a long time |
| The score table becomes more stable as more experience accumulates | Because of exploration, learning-rate, or representation problems, the value keeps shaking |
| Policy comparison becomes more consistent | Which action is better keeps reversing often |

There is no need in this Section to follow a full convergence proof. But it is still important to secure `why repeated updates connect not to intuition alone, but to a question about stability`.

## Why Does Function Approximation Appear?

In a small maze, the number of states and actions is small, so a Q-table can be written directly. But real problems are different.

- Games whose state is the whole screen of pixels
- Robot control with many sensor values
- Recommendation problems with too many combinations

In scenes like these, it becomes difficult to write the value of every state-action pair directly in a table.

That is when function approximation appears.

`Instead of writing a value into every cell, use a function or model that receives the input and predicts the value.`

| Q-table | Function approximation |
| --- | --- |
| A value is written directly into each state-action cell | A model estimates the value when the state is given |
| The intuition is clear in a small problem | Large state spaces become easier to handle |
| The table grows too quickly as the number of states grows | Generalization becomes possible, but learning stability can become harder |

So function approximation does not abandon value-based reinforcement learning. It is `a change in representation for moving that intuition into a larger problem`.

## How Should DQN Be Read?

DQN is a representative example in this flow of function approximation.

In a very short sentence:

`A reinforcement-learning method that approximates the Q-value with a neural network instead of a table, so larger state spaces can be handled`

So DQN should be read not as a completely new philosophy, but as `the name of an extension that expands value-based reinforcement learning into larger problems`.

| What remains from Q-learning | What changes in DQN |
| --- | --- |
| It still asks which action has the larger value | It expresses values with a function approximator instead of a table |
| The value of the next state still enters the current update | It reads large state inputs through a neural network |
| It still uses value-based intuition | Additional devices for learning stabilization become more important |

So DQN is not `a name that abandons value-based learning`, but `a name that lifts value-based learning into larger state spaces`. That overall line can be read again in the larger map of P4-19.4.

## Cases And Examples

### Case 1. When A Table Works In A Small Maze But Breaks Down In A Screen-Based Game

In a small maze problem, there are not many combinations of `current cell` and `move direction`, so a Q-table is sufficient. But once the problem shifts to a screen-based game, where the state is the whole visual scene, the table approach hits a wall immediately because almost every scene would need a new cell of its own. At that point, what is needed is not `make one more cell for this scene`, but `use a function that estimates which action value will be large when this scene is given as input`. Value-based reinforcement learning does not end there. It continues by changing form toward function approximation and neural networks.

## What To Remember From This Section

- The Bellman equation is a recursive value expression that reads current reward together with future value.
- Convergence is the question of whether repeated update results gradually stabilize.
- Function approximation is a change in representation that moves Q-table intuition into larger state spaces.
- DQN is a representative extension in the value-based reinforcement-learning line.
