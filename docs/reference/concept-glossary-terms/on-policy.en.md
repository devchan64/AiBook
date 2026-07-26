<a id="on-policy"></a>

## on-policy

- Meaning: On-policy learning learns the value of the policy that is actually being followed to generate behavior. SARSA is a common example because it updates from the next action actually chosen.
- Why it matters: If exploration or mistake paths are part of the current behavior, on-policy learning can reflect those costs in the value estimate. This helps explain why SARSA can look more conservative than Q-learning in risky settings.
- Related concepts: `SARSA`, `off-policy`, `policy`, `exploration`
- Core Section: `P4-19.1`
- Appears in:
