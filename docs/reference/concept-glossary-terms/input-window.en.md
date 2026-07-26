<a id="input-window"></a>
<a id="glossary-input-window"></a>

### input window

- Meaning: An input window is the time range cut from a source time series or continuous record and treated as one learning input. It includes the start point, end point, length criterion, and alignment criterion, so it is broader than simply matching array length.
- Why it matters: Changing the input window changes what signals the model can see, which ranges disappear, and which samples can be compared. The concept helps readers distinguish feeding raw source data from defining the boundary of one input for the current question. Whether the next step produces summary features or an order-preserving input, the window rule must be clear for interpretation and reproducibility.
- Related concepts: `input`, `input unit`, `sample`, `summary table`, `feature`, `source data`
- Core Section: `P3-5.4`
- Appears in: `P3-5.4`, `P3-5.6`
