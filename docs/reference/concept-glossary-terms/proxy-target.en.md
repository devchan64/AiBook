<a id="proxy-target"></a>
<a id="glossary-proxy-target"></a>

### proxy target

- Meaning: A proxy target is a substitute column used like a target when the actual target cannot be observed directly or appears too late. It can make a learning problem possible, but it is not automatically equivalent to the actual target.
- Why it matters: Good performance on a proxy target does not guarantee that the original goal is being predicted well. This concept separates `we can build a problem now` from `we are directly solving the original goal`, and it forces the distance between the proxy and the actual target to be recorded.
- Related concepts: `actual target`, `proxy label`, `target candidate`, `label`
- Core Section: `P3-9.9`
- Appears in: `P3-9.9`
