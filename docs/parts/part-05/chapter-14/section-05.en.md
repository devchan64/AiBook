# P5-14.5 How Do Sequential State And Direct Re-Reference Split In Long Context?

> Section ID: `P5-14.5`
> Version: `v2026.07.20`

In P5-14.4, we saw how RNN sequential state passing and Transformer relation computation differ from the viewpoint of parallel processing. The observation point in P5-14.5 is not GPU efficiency, but how the final judgment in a long context attaches earlier cues again as evidence.

In long context, is the important thing remembering for a long time, or referring again to the earlier position that is needed?

The comparison target is not the full Transformer implementation. It is the difference between `compressing an earlier rule into one state and carrying it forward` and `letting the current question find the earlier sentence it needs again`. We closed the computational efficiency of parallel processing in P5-14.4, and here we look only at the path by which a distant cue is attached again to the final judgment.

## Questions Handled By Long-Context Re-Reference And The Experiment

- Why can sequential state passing weaken in long context?
- Why does self-attention give the feeling that it can refer more directly to a faraway earlier position?
- How can sequential state and direct re-reference make different final judgments even in the same long context?

## Comparing Sequential Passing And Direct Re-Reference

In an RNN, distant information has to pass through several steps of state before reaching the current point. In self-attention, by contrast, the current token can refer more directly even to a faraway token.

```mermaid
--8<-- "assets/part-05/chapter-14/long-context-direct-reference-en.mmd"
```

If we compare the same request again only through the two computation paths, it can be read as follows.

```mermaid
--8<-- "assets/part-05/chapter-14/sequential-vs-direct-baseline-en.mmd"
```

| Viewpoint | Sequential State Passing | Direct Re-Reference |
| --- | --- | --- |
| movement of earlier cue | passed through intermediate state | the current position looks again at the earlier position it needs |
| long-context risk | the cue can weaken as intermediate information grows | the relevant earlier position is more likely to be brought back up |
| final judgment | depends on cue strength left inside the state | depends on relation computation between the current request and earlier evidence |

If we read the long-context problem only as `memory`, we only ask whether the model keeps holding earlier content for a long time. But the more important feeling in the Transformer structure is whether the current position can refer again to the earlier position it needs.

## Cases And Examples

### Case. Restart Request While Pressure Has Not Returned

Consider a long work-permit question and answer.

| Candidate Cue | Relation to the Final Judgment | Direct Re-Reference View |
| --- | --- | --- |
| `Do not restart line 3 before pressure is relieved` | restart blocking rule | earlier cue that must be called again |
| `Current pressure has not yet returned to the safe range` | state where the rule still applies | earlier cue that must be called again |
| `Sensor calibration was completed in the morning` | does not mean pressure returned to the safe range | weak cue that can be confused |
| `Shift handoff records were updated` | weak direct relation to restart-safety judgment | cue to push away from the judgment center |
| `Can line 3 restart be approved now?` | current question | position that must attach the earlier rule and state again |

The easy criterion a person may use first is `the model read a lot, so it should remember the earlier content`. But the result to confirm in this case is not `did it remember a lot?` It is whether the blocking rule and current pressure state were attached again as evidence at the final judgment point.

The sequential-state method tries to compress the earlier rule into one state and carry it to the end. As intermediate logs increase, the blocking-rule axis can weaken. The direct re-reference method finds the rule line and pressure-state line again at the final request point.

The judgment sentence in this case should close as follows.

| Method | Judgment Sentence |
| --- | --- |
| only weak sequential state remains | the earlier blocking rule may not remain strongly enough until the final request, so the judgment can become uncertain |
| direct re-reference found the needed cues | the final request attaches the blocking rule and current pressure state again as evidence, so it judges toward blocking the restart |

## Practice And Example

### Practice. Separate Needed Earlier Cues And Distracting Cues

Classify each candidate cue below as `needed`, `weak`, or `close to distracting`.

| Candidate Cue | Classification | Explanation |
| --- | --- | --- |
| `Do not restart line 3 before pressure is relieved` | needed | this rule directly blocks the final restart-approval question |
| `Current pressure has not yet returned to the safe range` | needed | this checks whether the blocking rule still applies |
| `Sensor calibration was completed in the morning` | weak | sensor calibration is not the same as pressure returning to the safe range |
| `Packaging material replenishment was separately approved` | close to distracting | even though it contains the word approved, it has weak direct relation to line-3 restart approval |

Explanation: The learning point in a long-context problem is not `it read a lot`, but `it attached the evidence needed for the final judgment again`. We must not only choose the needed cues, but also push cues with weak direct relation away from the judgment center.

### Example. Comparing A Sequential Reader And A Direct Reference Reader

This example is not a Transformer implementation. It is an experiment comparing what observations two reference methods leave in long-context judgment.

| Value to Manipulate | Output to Observe | Question to Check |
| --- | --- | --- |
| `decay` | `sequential_support`, `final_state` | how quickly does the earlier rule weaken inside sequential state? |
| number of intermediate `Log:` lines | final value of the `block` axis | does sequential state shake more as unrelated intermediate sentences increase? |
| final `Request:` sentence | `direct_decision`, top matched lines | does the current request contain cues that call the earlier rule again? |

```python
# This example compares how sequential state weakens in long context and how direct reference finds the earlier rule again.
context = [
    "Rule: unstable pressure state must not be restarted.",
    "Log: sensor calibration completed for line 3.",
    "Log: packaging material restocked this morning.",
    "State: pressure has not fully returned to safe range.",
    "Log: operator schedule updated for tomorrow.",
    "Request: restart line 3 now.",
]

def sequential_reader(lines, decay=0.55):
    state = {"pressure_risk": 0.0, "restart": 0.0, "block": 0.0}
    history = []
    for idx, line in enumerate(lines, start=1):
        lowered = line.lower()
        for key in state:
            state[key] *= decay
        if "pressure" in lowered or "unstable" in lowered:
            state["pressure_risk"] += 1.0
        if "restart" in lowered:
            state["restart"] += 1.0
        if "must not" in lowered:
            state["block"] += 1.0
        snapshot = {key: round(value, 3) for key, value in state.items()}
        history.append((idx, line, snapshot))
    support = round(min(state.values()), 3)
    decision = "block_restart" if support >= 0.8 else "uncertain"
    return history, {key: round(value, 3) for key, value in state.items()}, support, decision

def direct_reference_reader(lines):
    request = lines[-1].lower()
    keywords = {"restart", "pressure", "unstable", "must", "not"}
    scored = []
    for idx, line in enumerate(lines[:-1], start=1):
        words = set(line.lower().replace(".", "").replace(":", "").split())
        score = len(words & keywords)
        scored.append((score, idx, line))
    top_matches = sorted(scored, reverse=True)[:2]
    matched_lines = [line.lower() for _, _, line in top_matches]
    decision = (
        "block_restart"
        if any("must not be restarted" in line for line in matched_lines)
        and any("pressure" in line or "unstable" in line for line in matched_lines)
        and "restart" in request
        else "allow"
    )
    return top_matches, decision

history, final_state, sequential_support, sequential_decision = sequential_reader(context)
top_matches, direct_decision = direct_reference_reader(context)

print("[sequential reader]")
for idx, line, snapshot in history:
    print(f"{idx}. {line}")
    print("   state =", snapshot)
print("final_state =", final_state)
print("sequential_support =", sequential_support)
print("sequential_decision =", sequential_decision)
print()

print("[direct reference reader]")
for score, idx, line in top_matches:
    print(f"matched line {idx} (score={score}): {line}")
print("direct_decision =", direct_decision)
```

Read the example output as follows.

```text
final_state = {'pressure_risk': 0.353, 'restart': 1.05, 'block': 0.05}
sequential_support = 0.05
sequential_decision = uncertain

matched line 1 (score=4): Rule: unstable pressure state must not be restarted.
matched line 4 (score=2): State: pressure has not fully returned to safe range.
direct_decision = block_restart
```

The first output shows how sequential state weakens while passing through context. The `block` axis starts strongly at the rule line, but only `0.05` remains by the final request.

![Sequential state decay](/AiBook/assets/part-05/chapter-14/sequential-state-decay-en.png)

The second output shows which lines the direct re-reference method brings back at the final request. Since the rule line and pressure-state line rise again as strong evidence, the change to read in this example is not merely that the two decision names differ. It is the difference between the earlier cue `weakening inside the state` and `being called again by the current request`.

![Direct re-reference scores](/AiBook/assets/part-05/chapter-14/direct-reference-match-scores-en.png)

### Practice. Change Values And Check The Difference

| Value to Change | Expected Output Change | Explanation |
| --- | --- | --- |
| raise `decay` from `0.55` to `0.8` | `sequential_support` may grow | because sequential state keeps the earlier cue longer, the `block` axis created at the rule line weakens less by the final request |
| add three more intermediate logs | the sequential-state side can shake more easily | as intermediate lines increase, earlier cues inside state continue to decay, while direct re-reference can keep the judgment if it can find the matching earlier lines |
| remove the word `restart` from the final request | `direct_decision` can change | if the current request loses the key word connected to the earlier rule, direct re-reference also weakens in knowing which earlier cue to call |

Explanation: This practice is not saying that direct re-reference always guarantees the right answer. The core is to distinguish through output changes whether earlier cues `weaken inside the state` or `are called again by the current request` in long context.

## Checklist

- Can you explain the long-context problem as a difference between sequential state passing and direct re-reference?
- Can you say that self-attention gives the feeling of referring more directly to distant positions?
- Can you explain the difference between `sequential_support` and `direct_decision`?
- Can you say that in long context, final judgment can change depending on how evidence is called?

## Sources And References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
