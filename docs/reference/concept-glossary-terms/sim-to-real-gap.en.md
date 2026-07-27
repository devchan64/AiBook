<a id="sim-to-real-gap"></a>

## sim-to-real gap

- Meaning: The sim-to-real gap is the difference that appears when a policy trained or evaluated in simulation is moved into the real world, where noise, delay, friction, lighting, and rare cases can differ. Deliberately varying simulation conditions is one sub-strategy for reducing overfitting to a single simulated setting.
- Why it matters: Simulation often makes reinforcement-learning experiments possible, but it is not a complete copy of reality. This concept prevents reading `success in simulation` as automatic real-world success.
- Related concepts: `simulation`, `real world`, `safe reinforcement learning`, `deployment`
- Core Section: `P4-19.3`
- Appears in: `P4-19.4`
