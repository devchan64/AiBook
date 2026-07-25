<a id="hold-state"></a>

## hold state

- Meaning: Hold state is a run state in which execution pauses because an external condition is not yet open, such as missing approval, a pending human response, or an unmet permission boundary. It is not the same as a tool failure.
- Why it matters: Treating hold state as ordinary failure obscures the next action. This concept helps readers distinguish retrying a broken step from waiting for approval, reporting a pause, or preserving state until a safe next step is allowed.
- Related concepts: `approval policy`, `approval`, `state`, `retry`, `run record`
- Core Section: `P7-6.3`
- Appears in: `P7-6.1`, `P7-6.2`
