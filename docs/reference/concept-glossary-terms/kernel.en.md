<a id="kernel"></a>

## kernel

- Meaning: A core function that takes two inputs and computes how similar or close they are in a richer representation space. In the SVM context, it is read as the idea of getting the comparison effect of a new feature space through calculations in the original space, without explicitly building every new feature.
- Why it matters: When a linear boundary feels awkward in the original coordinate space, the problem may be the representation space rather than the boundary alone. The kernel helps explain nonlinear structure as `changing the space used to read the data`, not merely `drawing a more complicated line`.
- Related concepts: `feature space`, `SVM`, `polynomial kernel`, `RBF kernel`
- Core Section: `P4-13.2`
- Appears in: `P4-13.2`
