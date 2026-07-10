# P3-9.11 If There Are Multiple Target Candidates or the Criteria Change, What Should Be Fixed First

> Section ID: `P3-9.11`
> Version: `v2026.07.10`

In operational data, only one target candidate may not be visible. Multiple candidates such as `review_needed`, `final_status`, `failure_type`, and `priority_bucket` may appear together, and even a target with the same name may follow different judgment criteria at different times. In that state, the problem itself becomes unstable unless you first fix which one is the representative problem and which version of the current definition is in use. If there are multiple target candidates or the criteria change, you should first write which target is the representative one and what the current definition version is.

| What should be fixed first | Why it is needed |
| --- | --- |
| Representative target | To make clear which problem is being solved first right now |
| Target definition version | To avoid mixing different criteria under the same name |
| Auxiliary target candidates | To leave room for later comparison or expansion |

| Common scene | Note that is needed |
| --- | --- |
| `review_needed` and `final_status` exist together | Which one should be the representative problem first |
| Last month and this month use different judgment criteria | The point of rule change and the version |
| `warning`, `review`, and `failure` exist together | Which level should be treated as the target |

So the real difficulty when there are many target candidates is not `name collision`, but that `the problem itself becomes unstable unless the representative result and the definition version are fixed together`. What is fixed here is the combination of `representative-result definition`, `definition-version management`, and `expansion-candidate management`, so that the central problem remains stable even when several target candidates arise from the same data.

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `proxy labels`, accessed 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, versioning and derivation overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }

