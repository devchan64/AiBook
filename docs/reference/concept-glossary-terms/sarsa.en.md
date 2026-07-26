<a id="sarsa"></a>

## SARSA

- Meaning: SARSA is a value-based reinforcement-learning algorithm that updates a Q-value from the sequence state, action, reward, next state, and next action. It uses the value of the next action that was actually chosen.
- Why it matters: SARSA is a representative on-policy example. Because it reflects the behavior policy actually being followed, it helps readers compare exploration cost and failure cost against the more optimistic Q-learning update.
- Related concepts: `Q-value`, `Q-learning`, `on-policy`, `exploration`
- Core Section: `P4-19.1`
- Appears in:
