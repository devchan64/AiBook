# P4-19.5 Supplementary Learning: How To Read The Bellman Equation, Convergence, And Function Approximation For The First Time

> Section ID: `P4-19.5`
> Version: `v2026.07.20`

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

In a small maze problem, there are not many combinations of `current cell` and `move direction`, so a Q-table is often enough. The first human-friendly rule is simple: `there are only a few cells, so write one value per state and update the table`.

That rule works well in a small toy problem. In a 5x5 grid, for example, the overall picture still fits in view even if values are written for `current cell -> up/down/left/right` and updated repeatedly. At that stage, the Bellman view also attaches directly as `current reward + value of the next cell`.

But once the problem moves to a game whose state is the whole screen of pixels, the situation changes. Now the rule `add one more cell for this new scene` breaks down quickly. Even scenes that look similar appear in huge numbers, and a tiny visual change can make the state effectively new again. At that point, the main question changes from `should I add one more entry to the table?` to `do I need a shared rule that can estimate values across similar scenes?`

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-5-mermaid-01-en.mmd"
```

| Problem scene | The first human-friendly rule | The limit that appears soon | The interpretation this Section adds |
| --- | --- | --- | --- |
| 5x5 maze | Write one value per state cell | The table is still small enough to manage | Good for learning Bellman form and repeated updates through a table |
| Early screen-based game | Add a new cell when a new scene appears | The number of scenes becomes too large to manage as a table | Value representation has to move toward function approximation |
| Environment with constantly changing but similar scenes | Record almost every similar scene separately | Generalization fails, and learning becomes slow and unstable | A model that reads shared patterns becomes necessary |

So in this case, function approximation is not an extra device that abandons value-based reinforcement learning. It is `a change in representation that moves the same judgment into a larger state space once the table can no longer carry it`.

The checkable conclusion of this case is the following. In a small maze, `writing each state-action value directly into a table` can still support stable comparison of which action is better. But once the number of states explodes, as in a screen-based game, `adding more cells` no longer preserves that comparison well. The point to confirm is not `the value-based intuition became wrong`, but `the time has come to move that intuition from a table into a function`.

## Practice And Example

This exercise follows Case 1 directly and focuses on checking why the same Bellman reading, `current reward + next value`, splits into `keep a table` versus `move to function approximation` depending on the size of the state space.

The values to inspect are current reward `1.0`, discount factor `0.9`, next-state value `0.8`, and the number of states. What should be read as the output is not a single calculation result, but the judgment that the same current-value interpretation leads to a Q-table in a small state space and to function approximation in a large state space.

Therefore, this exercise ties the Bellman equation, convergence, and function approximation into one flow instead of memorizing them separately. The Bellman form is the recursive structure that reads `current reward + next value`, convergence is the question of whether the amount of change shrinks as this value is updated, and function approximation changes the representation that carries the same judgment in a large state space.

| Scene | Calculation | Current value reading | Number of states | More natural representation |
| --- | --- | ---: | ---: | --- |
| `small_maze` | `1.0 + 0.9 * 0.8` | 1.72 | 25 | Q-table |
| `screen_game` | `1.0 + 0.9 * 0.8` | 1.72 | 1,000,000 | function approximator |

What should be read from this example is the following.

1. Both the small maze and the screen-based game still read current value through the same Bellman structure: `current reward + next value`.
2. In other words, a large state space does not erase the value-based intuition itself.
3. What changes is `where to put that value`, and when the number of states grows, the same intuition has to move into function approximation.

### Table View: What Becomes Uncomfortable First As The State Count Grows?

This time, keep reward and discount factor the same, and only increase the number of states to see when the table-based intuition becomes uncomfortable. Because this scene reads the representation choice by state count, a comparison table is clearer than code.

| Number of states | Current value reading | What becomes uncomfortable first | Representation |
| ---: | ---: | --- | --- |
| 25 | 1.72 | State-action values can still be written in a table | Q-table |
| 2,500 | 1.72 | The table grows difficult to manage | function approximation |
| 250,000 | 1.72 | Directly storing every value becomes difficult | function approximation |

What does not change here is the interpretation `current reward + future value`. What breaks first is the representation `write it directly into a table`. So the main point to confirm is not `the Bellman view stopped working`, but `the same judgment now has to move into a different representation`.

### Judge It Directly

Read the observations below and choose which interpretation is safer first.

| Observation | Rushed conclusion | Safer interpretation |
| --- | --- | --- |
| The `bellman view` is the same for the small maze and the screen-based game | The Bellman equation is not used in a large state space | The current-value reading stays the same, and only the value representation changes |
| The representation changed when the number of states went from 25 to 2500 | Value-based reinforcement learning stopped being valid | The table became uncomfortable, and the need to move into function approximation appeared |
| The amount of change shrinks after repeated updates | The formula is finished and there is nothing more to ask | It continues into the convergence question of whether the value is stabilizing |

The purpose of this table is not to memorize mathematical names. It is to hold one flow together: `why present value connects to the future`, `why a stability question appears`, and `why the form of representation changes`.

## Checklist

- Can you explain that the Bellman equation is a recursive value expression that reads current reward and future value together?
- Can you explain convergence as the question of whether repeated update results become more stable?
- Can you explain function approximation as a change in representation that moves Q-table intuition into a larger state space?
- Can you explain DQN as a representative extension line in value-based reinforcement learning?

## Sources And References

- Richard S. Sutton and Andrew G. Barto, `Reinforcement Learning: An Introduction`, 2nd ed., The MIT Press, 2018. Consulted for the Bellman equation, value-based methods, convergence, and function approximation flow. Accessed 2026-07-19. [https://mitpress.mit.edu/9780262039246/reinforcement-learning/](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }
- Volodymyr Mnih et al., `Human-level control through deep reinforcement learning`, Nature, 2015. Consulted as a representative case connecting DQN to high-dimensional sensory input and Q-value function approximation. Accessed 2026-07-19. [https://doi.org/10.1038/nature14236](https://doi.org/10.1038/nature14236){: target="_blank" rel="noopener noreferrer" }
