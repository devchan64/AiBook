## optimizer

- Meaning: An optimizer is the rule or procedure that decides how to update parameters using gradients computed by backpropagation. If a gradient indicates which direction reduces loss, the optimizer decides how far and in what manner to move in that direction. Training therefore needs an update rule in addition to a loss function and gradients.
- Why it matters: Loss and gradients alone do not complete learning, because the step size and update style strongly affect training speed and stability. This concept separates `which direction should we go?` from `how should we move?` It also explains why the same model can train differently under update rules such as SGD and Adam.
- Related concepts: `gradient`, `learning rate`, `loss function`
- Core Section: `P5-7.1`
- Appears in: `P5-6.1`, `P5-7.2`, `P5-7.3`
