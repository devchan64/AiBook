<a id="adapter"></a>

## adapter

- Meaning: An adapter is a small additional module inserted around or between parts of a base model so the model can be adapted without retraining the whole body. It collects task-specific changes in a smaller component while the main model remains largely shared.
- Why it matters: Adapter methods belong to the broader family of efficient adaptation techniques. They are related to LoRA and fine-tuning, but differ in where the added structure sits and how updates are stored. This helps readers see efficient tuning as a family of design choices, not a single method name.
- Related concepts: `LoRA`, `fine-tuning`, `parameter`
- Core Section: `P6-9.5`
