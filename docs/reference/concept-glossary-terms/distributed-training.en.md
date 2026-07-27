<a id="distributed-training"></a>

## distributed training

- Meaning: Distributed training splits one training job across multiple compute resources or workers. In boosting, it is discussed when large data, many stages, or many validation combinations must be handled.
- Why it matters: Distributed training does not mainly change the model philosophy. It helps make long repetition and large data operationally manageable. In boosting, data partitioning, stage records, and restart rules must remain consistent for comparisons to stay meaningful.
- Related concepts: `GPU`, `training`, `validation data`
- Core Section: `P4-16.3`
- Appears in: `P4-16.3`
